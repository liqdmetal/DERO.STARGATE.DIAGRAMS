#!/usr/bin/env python3
"""
D1 — extract_activity.py
========================
Extract per-account ring-appearance activity from a DERO daemon RPC into a
flat dataset, for the decoy activity-distribution analysis
(spec/decoy-activity-distribution.md).

For every block in [start, end]:
  - getblock  -> tx_hashes
  - gettransactions -> expanded rings (txs[].ring[payload] = list of addresses)
  - record, per tx: height, timestamp, ringsize, ring members

Output: CSV (default) or parquet with one row per (tx, payload, ring index):

    height, topoheight, timestamp, txid, payload_idx, ringsize, ring_pos, account

Plus an aggregated per-account table:

    account, first_seen_height, last_seen_height, n_appearances,
    appearance_heights (JSON array)

Usage:
    python extract_activity.py --rpc http://127.0.0.1:10102 --start 0 --end 100
    python extract_activity.py --rpc http://127.0.0.1:20102 --start 0 --end 100 --outdir ./data --format csv

Requirements: requests (or stdlib urllib fallback).

⚠️ DRAFT — research tooling for spec/decoy-activity-distribution.md.
Not part of any release. ⚠️
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.request

try:
    import pandas as pd  # optional; falls back to CSV-only
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


def rpc_call(endpoint: str, method: str, params=None, timeout: float = 30.0):
    """JSON-RPC call to a DERO daemon. Params omitted entirely when None
    (DERO rejects 'params':[] for parameterless methods)."""
    if not endpoint.rstrip("/").endswith("/json_rpc"):
        endpoint = endpoint.rstrip("/") + "/json_rpc"
    payload = {"jsonrpc": "2.0", "id": "0", "method": method}
    if params is not None:
        payload["params"] = params
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode())
    if "error" in data:
        raise RuntimeError(f"RPC {method} error: {data['error']}")
    return data.get("result", {})


def get_topoheight(endpoint: str) -> int:
    info = rpc_call(endpoint, "get_info")
    return int(info.get("topoheight", 0))


def get_block(endpoint: str, height: int):
    """getblock by height. Returns block JSON (with tx_hashes) + header."""
    return rpc_call(endpoint, "getblock", {"height": height})


def get_txs(endpoint: str, tx_hashes):
    """gettransactions with expanded rings."""
    if not tx_hashes:
        return []
    res = rpc_call(endpoint, "gettransactions", {"txs_hashes": tx_hashes})
    return res.get("txs", [])


def extract_block(endpoint: str, height: int):
    """Return list of (height, txid, payload_idx, ringsize, ring) tuples."""
    blk = get_block(endpoint, height)
    blk_json = blk.get("json")
    if isinstance(blk_json, str):
        blk_json = json.loads(blk_json)
    tx_hashes = blk_json.get("tx_hashes", []) if blk_json else []
    rows = []
    if not tx_hashes:
        return rows
    txs = get_txs(endpoint, tx_hashes)
    by_hash = {t.get("tx_hash"): t for t in txs if t.get("tx_hash")}
    for txid in tx_hashes:
        t = by_hash.get(txid)
        if not t:
            continue
        ring_payloads = t.get("ring") or []
        for pi, ring in enumerate(ring_payloads):
            rows.append((height, txid, pi, len(ring), ring))
    return rows


def main():
    ap = argparse.ArgumentParser(description="Extract DERO ring-activity dataset")
    ap.add_argument("--rpc", default="http://127.0.0.1:10102")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--end", type=int, default=None, help="inclusive; default = current topoheight")
    ap.add_argument("--outdir", default="./data")
    ap.add_argument("--format", choices=["csv", "parquet"], default="csv")
    ap.add_argument("--sleep", type=float, default=0.0, help="per-block throttle (s)")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    end = args.end if args.end is not None else get_topoheight(args.rpc)
    print(f"scanning heights {args.start}..{end} via {args.rpc}", file=sys.stderr)

    ring_rows = []      # (height, txid, payload_idx, ringsize, pos, account)
    account_app = {}    # account -> list of heights
    t0 = time.time()

    for h in range(args.start, end + 1):
        try:
            rows = extract_block(args.rpc, h)
        except Exception as e:
            print(f"  height {h}: FAILED {e}", file=sys.stderr)
            continue
        for height, txid, pi, ringsize, ring in rows:
            for pos, acc in enumerate(ring):
                ring_rows.append((height, txid, pi, ringsize, pos, acc))
                account_app.setdefault(acc, []).append(height)
        if h % 100 == 0:
            dt = time.time() - t0
            rate = (h - args.start + 1) / max(dt, 1e-9)
            print(f"  {h}/{end} ({rate:.1f} blk/s, {len(account_app)} accounts)",
                  file=sys.stderr)
        if args.sleep:
            time.sleep(args.sleep)

    # per-account aggregation
    account_rows = []
    for acc, heights in account_app.items():
        account_rows.append({
            "account": acc,
            "first_seen_height": min(heights),
            "last_seen_height": max(heights),
            "n_appearances": len(heights),
            "appearance_heights": json.dumps(sorted(heights)),
        })
    account_rows.sort(key=lambda r: r["first_seen_height"])

    if args.format == "parquet" and HAS_PANDAS:
        pd.DataFrame(ring_rows, columns=[
            "height", "txid", "payload_idx", "ringsize", "ring_pos", "account"
        ]).to_parquet(os.path.join(args.outdir, "ring_members.parquet"))
        pd.DataFrame(account_rows).to_parquet(os.path.join(args.outdir, "accounts.parquet"))
    else:
        with open(os.path.join(args.outdir, "ring_members.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["height", "txid", "payload_idx", "ringsize", "ring_pos", "account"])
            w.writerows(ring_rows)
        with open(os.path.join(args.outdir, "accounts.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(account_rows[0].keys()) if account_rows else
                               ["account", "first_seen_height", "last_seen_height",
                                "n_appearances", "appearance_heights"])
            w.writeheader()
            w.writerows(account_rows)

    print(f"done: {len(ring_rows)} ring-member rows, {len(account_rows)} accounts "
          f"-> {args.outdir}", file=sys.stderr)


if __name__ == "__main__":
    main()
