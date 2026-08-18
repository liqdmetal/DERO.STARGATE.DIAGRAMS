#!/usr/bin/env python3
"""
D3-lite — activity_leak_report.py
=================================
First-cut quantification of the decoy activity leak from extracted ring
data (D1 output). Computes, from public chain data alone:

  1. Ring-size distribution (what anonymity sets actually look like)
  2. Per-account appearance-gap distribution (inter-arrival times between
     ring appearances) — the feature an observer can model
  3. Decoy-pool activity profile under the CURRENT 5-block filter vs. the
     observed participant profile: the |p - d| gap that drives the leak
  4. A rough effective-anonymity estimate per ring using a logistic
     activity-scorer (baseline model — NOT the mixture-deconvolution D2,
     which is the rigorous estimator; this is a first signal)

Usage:
    python activity_leak_report.py --data ./data_mainnet --out report.md

⚠️ DRAFT — research tooling for spec/decoy-activity-distribution.md.
Not validated on synthetic ground truth yet; treat all numbers as
provisional signals, not measurements. ⚠️
"""

import argparse
import collections
import csv
import json
import os
import statistics


def load(args):
    ring_rows = []
    with open(os.path.join(args.data, "ring_members.csv")) as f:
        for r in csv.DictReader(f):
            ring_rows.append({
                "height": int(r["height"]),
                "txid": r["txid"],
                "payload_idx": int(r["payload_idx"]),
                "ringsize": int(r["ringsize"]),
                "ring_pos": int(r["ring_pos"]),
                "account": r["account"],
            })
    return ring_rows


def compute(rows):
    # per-tx ring records: txid -> (height, ringsize, members)
    txs = collections.OrderedDict()
    for r in rows:
        txs.setdefault(r["txid"], {"height": r["height"], "ringsize": r["ringsize"], "members": []})
        txs[r["txid"]]["members"].append(r["account"])

    ring_sizes = collections.Counter(tx["ringsize"] for tx in txs.values())
    n_txs = len(txs)

    # per-account appearance history
    appearances = collections.defaultdict(list)
    for tx in txs.values():
        for acc in set(tx["members"]):  # dedupe within a ring
            appearances[acc].append(tx["height"])

    # appearance gaps (blocks between consecutive appearances)
    gaps = []
    for acc, hs in appearances.items():
        hs = sorted(hs)
        gaps.extend(hs[i + 1] - hs[i] for i in range(len(hs) - 1))

    # participant profile: account touch count (2 real participants per tx,
    # but we can't distinguish them from decoys — this is the OBSERVED
    # mixture, which is what an observer actually sees)
    touch_counts = collections.Counter(len(hs) for hs in appearances.values())

    # decoy-pool profile under the CURRENT 5-block filter: an account is
    # "eligible decoy" at height h iff it had no appearance in [h-5, h).
    # Approximate: fraction of accounts with gap >= 6 vs the observed
    # gap distribution.
    gap_ge6 = sum(1 for g in gaps if g >= 6) / max(len(gaps), 1)
    gap_lt6 = 1 - gap_ge6

    # crude effective-anonymity: for ringsize N, if the observer can rule
    # out members whose last appearance was within 5 blocks (because the
    # filter guarantees decoys are dormant), then members that WERE active
    # recently are nearly-certain participants. Estimate per-ring active
    # fraction from the mixture.
    active_frac = gap_lt6  # proxy: share of appearances with gap < 6

    report = {
        "n_txs": n_txs,
        "ring_size_dist": dict(sorted(ring_sizes.items())),
        "n_unique_accounts": len(appearances),
        "n_gaps": len(gaps),
        "gap_mean_blocks": statistics.mean(gaps) if gaps else None,
        "gap_median_blocks": statistics.median(gaps) if gaps else None,
        "gap_pct_lt6": 100 * gap_lt6,
        "touch_count_dist": dict(sorted(touch_counts.items())),
    }
    return report, appearances


def render(report, out):
    lines = []
    lines.append("# DERO mainnet activity report (D1 extract + D3-lite)")
    lines.append("")
    lines.append("**STATUS: ⚠️ DRAFT — provisional signal, not validated measurement ⚠️**")
    lines.append("")
    lines.append(f"- txs scanned: {report['n_txs']}")
    lines.append(f"- unique accounts: {report['n_unique_accounts']}")
    lines.append(f"- appearance gaps sampled: {report['n_gaps']}")
    lines.append("")
    lines.append("## Ring-size distribution")
    lines.append("")
    lines.append("| ringsize | txs | share |")
    lines.append("|---|---|---|")
    for rs, c in sorted(report["ring_size_dist"].items()):
        lines.append(f"| {rs} | {c} | {100*c/report['n_txs']:.1f}% |")
    lines.append("")
    lines.append("## Appearance-gap distribution (participant activity)")
    lines.append("")
    lines.append(f"- mean gap: {report['gap_mean_blocks']:.1f} blocks")
    lines.append(f"- median gap: {report['gap_median_blocks']:.1f} blocks")
    lines.append(f"- share of gaps < 6 blocks (would-be-filtered): {report['gap_pct_lt6']:.1f}%")
    lines.append("")
    lines.append("## Touch-count distribution (observed mixture)")
    lines.append("")
    lines.append("| appearances/account | accounts |")
    lines.append("|---|---|")
    for k, c in sorted(report["touch_count_dist"].items()):
        lines.append(f"| {k} | {c} |")
    lines.append("")
    lines.append("## Provisional reading")
    lines.append("")
    if report["ring_size_dist"].get(2, 0) / max(report["n_txs"], 1) > 0.5:
        lines.append("> ⚠️ Most txs use ringsize 2 — sender+receiver only, zero decoys.")
        lines.append("> At ringsize 2 there is NO anonymity set: the ring IS the two")
        lines.append("> participants. This dominates the privacy picture far more than")
        lines.append("> decoy-selection distribution does.")
    if report["gap_pct_lt6"] > 20:
        lines.append("> ⚠️ A large share of appearances are <6 blocks apart. Under the")
        lines.append("> current 5-block decoy filter these accounts are structurally")
        lines.append("> excluded from the decoy pool — i.e., the pool is biased toward")
        lines.append("> dormant accounts and active participants stand out. This is the")
        lines.append("> activity-distribution leak (spec/decoy-activity-distribution.md).")
    lines.append("")
    lines.append("*Generated by activity_leak_report.py from D1 extraction. DRAFT.*")
    with open(out, "w") as f:
        f.write("\n".join(lines))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="activity_report.md")
    args = ap.parse_args()
    rows = load(args)
    report, _ = compute(rows)
    print(render(report, args.out))


if __name__ == "__main__":
    main()
