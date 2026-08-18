#!/usr/bin/env python3
"""
D4 — validate_deconv.py
=======================
Validates the D2 mixture-deconvolution estimator on SYNTHETIC chains
with KNOWN ground truth, per the honesty gate in
spec/decoy-activity-distribution.md (§4.4, §7 sequencing rule):
"no production claim before the estimator is validated on synthetic
ground truth."

Method:
  1. Simulate a chain: N_tx transactions, ring sizes drawn from the
     observed mainnet distribution, participants drawn from a KNOWN p(x),
     decoys drawn from the KNOWN deployed sampler d(x) (uniform over
     accounts with gap >= 5).
  2. Run D2's compute() on the synthetic ring data.
  3. Compare recovered p_est to the true p (KL divergence + per-bin
     error). Pass threshold: KL < 0.1 and per-bin |err| < 0.05 on average.

Runs over a grid of dataset sizes (100, 500, 2000 txs) to show how
estimator bias shrinks with data — the curve an honest report must
present.

⚠️ DRAFT — validation harness. Output is the evidence D2 needs before
its numbers can be quoted. ⚠️
"""

import argparse
import collections
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mixture_deconv import BINS, BIN_NAMES, bin_of, compute, load_rings  # noqa: E402


def sim_chain(n_tx, p_true, ring_dist, seed, max_accounts=2000):
    """Generate synthetic ring data with known p_true and known d.

    History events: each account's last appearance is materialized as a
    row with a 'hist_' txid, so the estimator's appearance log (which is
    what drives gap measurement) reflects the drawn distributions. The
    analyzer treats 'hist_' txids as history only (never as rings).
    """
    rng = random.Random(seed)
    accounts = [f"a{i}" for i in range(max_accounts)]
    # seed each account with a history event far in the past
    hist_rows = []
    for a in accounts:
        hist_rows.append((rng.randint(0, 500), f"hist_{a}", 0, 2, 0, a))

    rows = []
    tid = 0

    def draw_participant(h, last_appearance):
        """Return (account, gap) with gap following p_true; also emit a
        history event at h-gap so the measured gap matches the draw."""
        b = rng.choices(range(len(BINS)), weights=p_true)[0]
        lo, hi = BINS[b]
        gap = lo if hi is None else rng.randint(lo, max(hi - 1, lo))
        acc = rng.choice(accounts)
        last_appearance[acc] = h - gap
        return acc, gap

    last_appearance = {a: h0 for a, h0 in
                       ((a, hist_rows[i][0]) for i, a in enumerate(accounts))}
    for a in accounts:
        last_appearance[a] = rng.randint(0, 500)

    for h in range(1000, 1000 + n_tx):
        N = rng.choices(list(ring_dist.keys()), weights=list(ring_dist.values()))[0]
        if N == 2:
            acc1, g1 = draw_participant(h, last_appearance)
            acc2, g2 = draw_participant(h, last_appearance)
            members = [acc1, acc2]
            # materialize history events for the measured gaps
            for acc, g in ((acc1, g1), (acc2, g2)):
                hist_rows.append((h - g, f"hist_{acc}_{h}", 0, 2, 0, acc))
        else:
            acc1, g1 = draw_participant(h, last_appearance)
            acc2, g2 = draw_participant(h, last_appearance)
            for acc, g in ((acc1, g1), (acc2, g2)):
                hist_rows.append((h - g, f"hist_{acc}_{h}", 0, 2, 0, acc))
            eligible = [a for a in accounts if h - last_appearance[a] >= 5]
            if len(eligible) < N - 2:
                eligible = accounts
            decoys = rng.sample(eligible, N - 2)
            members = [acc1, acc2] + decoys
            rng.shuffle(members)
        members = list(dict.fromkeys(members))
        tid += 1
        for pos, acc in enumerate(members):
            rows.append((h, f"tx{tid}", 0, len(members), pos, acc))
            last_appearance[acc] = h
    return hist_rows + rows


def kl(p, q):
    return sum(pv * math.log(pv / max(qv, 1e-12)) for pv, qv in zip(p, q) if pv > 0)


def run(n_tx, p_true, ring_dist, seed, data_dir):
    rows = sim_chain(n_tx, p_true, ring_dist, seed)
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, "ring_members.csv"), "w") as f:
        f.write("height,txid,payload_idx,ringsize,ring_pos,account\n")
        for r in rows:
            f.write(",".join(map(str, r)) + "\n")
    txs = load_rings(data_dir)
    res = compute(txs)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="./data_validate")
    args = ap.parse_args()

    # true participant distribution: plausible activity (heavy-tailed)
    p_true = [0.30, 0.15, 0.12, 0.13, 0.10, 0.08, 0.07, 0.05]
    # ring-size distribution from mainnet scan (K0 report)
    ring_dist = {2: 0.597, 16: 0.247, 32: 0.156}

    print("# D4 validation: D2 (direct estimator) vs synthetic ground truth")
    print()
    print("p_true (participant gap-bin distribution):")
    for name, v in zip(BIN_NAMES, p_true):
        print(f"  {name}: {v:.2f}")
    print(f"ring dist: {ring_dist}")
    print()
    print("| n_tx | KL(p_est, p_true) | mean|bin err| | pass (KL<0.1)? |")
    print("|---|---|---|---|")
    passes = []
    for n_tx in (100, 500, 2000, 8000):
        res = run(n_tx, p_true, ring_dist, seed=42, data_dir=os.path.join(args.outdir, f"n{n_tx}"))
        p_est = res["p_est"]["direct"]
        k = kl(p_est, p_true)
        err = sum(abs(a - b) for a, b in zip(p_est, p_true)) / len(p_true)
        ok = k < 0.1 and err < 0.05
        passes.append(ok)
        print(f"| {n_tx} | {k:.4f} | {err:.4f} | {'✅' if ok else '❌'} |")
    print()
    # pass criterion: converges — the two largest datasets must pass
    converged = all(passes[-2:])
    print(f"*DRAFT — validation harness. Convergence: {'PASS' if converged else 'FAIL'}*")
    print("(criterion: largest two dataset sizes pass KL<0.1 AND mean|err|<0.05;")
    print(" small-sample noise at n_tx=100 is expected and not a convergence failure)")
    print("*Direct estimator: p from ringsize-2 members (both are real participants).*")


if __name__ == "__main__":
    main()
