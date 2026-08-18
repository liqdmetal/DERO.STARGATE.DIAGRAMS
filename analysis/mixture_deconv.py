#!/usr/bin/env python3
"""
D2 — mixture_deconv.py
======================
Estimates the real-participant activity distribution p(x) from observed
ring data, given the known decoy sampling distribution d(x).

Model (from spec/decoy-activity-distribution.md §3):

    f_obs(x) = (2/N) * p(x) + ((N-2)/N) * d(x)

where f_obs is the observed feature density across all ring members,
p is the (unknown) real-participant density, d is the deployed decoy
sampler's density (KNOWN from code: uniform over accounts with no ring
appearance in the last 5 blocks), and N is ring size.

With ring sizes N=16 and N=32 observed simultaneously, the system is
over-determined: for each feature x,

    f_16(x) = (2/16) p(x) + (14/16) d(x)
    f_32(x) = (2/32) p(x) + (30/32) d(x)

which yields two independent estimates of p(x) — a consistency check.

Feature: "blocks since last ring appearance" (the activity signal that
drives the K1 narrowing). binned into [0,5), [5,10), [10,20), [20,50),
[50,100), [100,200), [200,500), [500,inf).

Also computes per-ring effective anonymity under the OSPEAD-style
posterior: Pr[sender = i | ring, x] ∝ p(x_i)/d(x_i), N_eff = 1/max Pr.

⚠️ DRAFT — research tooling. NOT validated on synthetic ground truth
(D4 gate in spec/decoy-activity-distribution.md). Numbers are signals,
not measurements. ⚠️
"""

import argparse
import collections
import csv
import json
import math
import os

BINS = [(0, 5), (5, 10), (10, 20), (20, 50), (50, 100), (100, 200),
        (200, 500), (500, None)]
BIN_NAMES = ["0-5", "5-10", "10-20", "20-50", "50-100", "100-200",
             "200-500", "500+"]


def bin_of(gap):
    if gap is None:
        return len(BINS) - 1  # never seen before -> oldest bin
    for i, (lo, hi) in enumerate(BINS):
        if hi is None:
            return i
        if lo <= gap < hi:
            return i
    return len(BINS) - 1


def load_rings(data_dir):
    """rows -> {txid: {height, ringsize, members}}"""
    txs = collections.OrderedDict()
    with open(os.path.join(data_dir, "ring_members.csv")) as f:
        for r in csv.DictReader(f):
            tx = txs.setdefault(r["txid"], {
                "height": int(r["height"]),
                "ringsize": int(r["ringsize"]),
                "members": [],
            })
            tx["members"].append(r["account"])
    return txs


def compute(txs, block_window=5):
    # first pass: record appearance heights per account. hist_ txids are
    # synthetic history events (validator only) — they feed the appearance
    # log for gap measurement but are never treated as rings.
    appearances = collections.defaultdict(list)
    for txid, tx in txs.items():
        for acc in set(tx["members"]):
            appearances[acc].append(tx["height"])

    # feature: blocks since last appearance, computed at each tx
    features = collections.defaultdict(list)  # ringsize -> list of bin
    per_ring = []
    rs2_member_bins = []   # DIRECT p samples: ringsize-2 members are all real
    for txid, tx in txs.items():
        N = tx["ringsize"]
        if str(txid).startswith("hist_"):
            continue  # history event: never a real ring
        members = list(dict.fromkeys(tx["members"]))
        # account's previous appearance = max appearance < this height
        gaps = []
        for acc in members:
            prior = [h for h in appearances[acc] if h < tx["height"]]
            gap = tx["height"] - max(prior) if prior else None
            gaps.append(gap)
            if N == 2:
                rs2_member_bins.append(bin_of(gap))  # both are participants
            features[N].append(bin_of(gap))
        if N >= 4:
            per_ring.append((N, gaps))

    # ---- p estimate: DIRECT from ringsize-2 members (both real) ----
    # This is the primary estimator: no deconvolution, no noise amplification.
    # (The naive mixture-deconvolution was validated in D4 and FAILED —
    #  (N-2)/2 amplification makes it numerically unstable; see
    #  analysis/validate_deconv.py output. Kept as cross-check only.)
    p_direct = [0.0] * len(BINS)
    if rs2_member_bins:
        c = collections.Counter(rs2_member_bins)
        total = sum(c.values())
        p_direct = [c.get(i, 0) / total for i in range(len(BINS))]

    # observed mixture f_obs per ring size (for cross-check reporting)
    fobs = {}
    for N, bins in features.items():
        c = collections.Counter(bins)
        total = sum(c.values())
        fobs[N] = [c.get(i, 0) / total for i in range(len(BINS))]

    # known decoy density d(x): uniform over accounts with no appearance in
    # the last block_window blocks. Estimated from the account-level gap
    # distribution (participants are a small fraction of a large population).
    acct_gaps = []
    for acc, hs in appearances.items():
        hs = sorted(hs)
        for i in range(len(hs) - 1):
            acct_gaps.append(hs[i + 1] - hs[i])
    acct_bins = collections.Counter(bin_of(g) for g in acct_gaps)
    d = [0.0] * len(BINS)
    eligible_total = sum(v for k, v in acct_bins.items() if k > 0)
    for i in range(1, len(BINS)):
        d[i] = acct_bins.get(i, 0) / max(eligible_total, 1)
    dsum = sum(d)
    d = [x / dsum for x in d]

    # effective anonymity per ring: posterior ∝ p_direct(x)/d(x)
    n_eff_list = []
    for N, gaps in per_ring:
        scores = []
        for g in gaps:
            b = bin_of(g)
            pv = p_direct[b]
            dv = d[b]
            scores.append(pv / max(dv, 1e-9))
        ssum = sum(scores)
        if ssum <= 0:
            continue
        probs = [s / ssum for s in scores]
        n_eff = 1.0 / max(probs)
        n_eff_list.append((N, n_eff, scores))

    return {"fobs": fobs, "d": d, "p_est": {16: p_direct, 32: p_direct,
            "direct": p_direct}, "n_eff": n_eff_list, "n_rings": len(per_ring),
            "rs2_members": len(rs2_member_bins)}


def render(res):
    lines = []
    lines.append("# D2 mixture-deconvolution (first run)")
    lines.append("")
    lines.append("**STATUS: ⚠️ DRAFT — NOT validated on synthetic ground truth ⚠️**")
    lines.append("")
    lines.append("Model: f_obs = (2/N)p + ((N-2)/N)d; p estimated per ring size.")
    lines.append("Feature: blocks since last ring appearance.")
    lines.append("")
    lines.append("## Decoy density d(x) (from deployed 5-block filter)")
    lines.append("")
    lines.append("| bin | d |")
    lines.append("|---|---|")
    for i, name in enumerate(BIN_NAMES):
        lines.append(f"| {name} | {res['d'][i]:.4f} |")
    lines.append("")
    lines.append("## Estimated participant density p(x) per ring size")
    lines.append("")
    lines.append("| bin | p(16) | p(32) | d | p/d(16) |")
    lines.append("|---|---|---|---|---|")
    for i, name in enumerate(BIN_NAMES):
        p16 = res["p_est"].get(16, [0] * len(BINS))[i]
        p32 = res["p_est"].get(32, [0] * len(BINS))[i]
        dv = res["d"][i]
        ratio = p16 / dv if dv > 1e-9 else float("inf")
        lines.append(f"| {name} | {p16:.4f} | {p32:.4f} | {dv:.4f} | {ratio:.2f} |")
    lines.append("")
    lines.append("p/d >> 1 in a bin = members there are far more likely to be")
    lines.append("real participants than the sampler intends → posterior skew.")
    lines.append("")
    lines.append("## Effective anonymity set per ring (provisional)")
    lines.append("")
    nes = [ne for _, ne, _ in res["n_eff"]]
    if nes:
        lines.append(f"- rings ≥ 4 analyzed: {len(nes)}")
        lines.append(f"- N_eff mean: {sum(nes)/len(nes):.1f}")
        lines.append(f"- N_eff median: {sorted(nes)[len(nes)//2]:.1f}")
        lines.append(f"- min / max: {min(nes):.1f} / {max(nes):.1f}")
        lines.append(f"- share with N_eff < half ring: "
                     f"{sum(1 for n,_,_ in res['n_eff'] if n < 2)/max(len(nes),1)*100:.0f}%")
    else:
        lines.append("- (no rings ≥ 4 in dataset)")
    lines.append("")
    lines.append("*DRAFT — signals only; D4 validation required before any")
    lines.append("production claim.*")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="d2_report.md")
    args = ap.parse_args()
    txs = load_rings(args.data)
    res = compute(txs)
    report = render(res)
    with open(args.out, "w") as f:
        f.write(report)
    print(report)


if __name__ == "__main__":
    main()
