#!/usr/bin/env python3
"""
run_analysis.sh equivalent (Windows-friendly): runs the full D1→D4
pipeline output for a dataset directory:
  1. activity_leak_report.py  -> report.md   (ring sizes, gaps, activity)
  2. mixture_deconv.py        -> d2_report.md (participant density p, N_eff)
Usage: python run_analysis.py --data <dir>
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    args = ap.parse_args()

    steps = [
        (["python", os.path.join(HERE, "activity_leak_report.py"),
          "--data", args.data, "--out", os.path.join(args.data, "report.md")],
         "activity report"),
        (["python", os.path.join(HERE, "mixture_deconv.py"),
          "--data", args.data, "--out", os.path.join(args.data, "d2_report.md")],
         "mixture deconvolution"),
    ]
    for cmd, name in steps:
        print(f"=== {name} ===", file=sys.stderr)
        r = subprocess.run(cmd)
        if r.returncode != 0:
            print(f"FAILED: {name}", file=sys.stderr)
            sys.exit(r.returncode)
    print("done: reports in", args.data)


if __name__ == "__main__":
    main()
