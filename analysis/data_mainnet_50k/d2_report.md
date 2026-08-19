# D2 participant-density estimate (50k-block scan, validated estimator)

**STATUS: ⚠️ DRAFT — estimator D4-validated on synthetic ground truth;
numbers are signals, confidence intervals pending ⚠️**

Model: p estimated DIRECTLY from ringsize-2 members (both are real
participants — the decoy loop only runs while ringsize != 2). The naive
mixture-deconvolution was rejected by D4 (numerical instability). See
`analysis/validate_deconv.py` and spec/decoy-activity-distribution.md.
Feature: blocks since last ring appearance.

## Decoy density d(x) (from deployed 5-block filter)

| bin | d |
|---|---|
| 0-5 | 0.0000 |
| 5-10 | 0.0995 |
| 10-20 | 0.0490 |
| 20-50 | 0.0954 |
| 50-100 | 0.0582 |
| 100-200 | 0.0538 |
| 200-500 | 0.0819 |
| 500+ | 0.5622 |

## Estimated participant density p(x) per ring size

| bin | p(16) | p(32) | d | p/d(16) |
|---|---|---|---|---|
| 0-5 | 0.1238 | 0.1238 | 0.0000 | inf |
| 5-10 | 0.1421 | 0.1421 | 0.0995 | 1.43 |
| 10-20 | 0.0436 | 0.0436 | 0.0490 | 0.89 |
| 20-50 | 0.0771 | 0.0771 | 0.0954 | 0.81 |
| 50-100 | 0.0193 | 0.0193 | 0.0582 | 0.33 |
| 100-200 | 0.0107 | 0.0107 | 0.0538 | 0.20 |
| 200-500 | 0.0502 | 0.0502 | 0.0819 | 0.61 |
| 500+ | 0.5332 | 0.5332 | 0.5622 | 0.95 |

p/d >> 1 in a bin = members there are far more likely to be
real participants than the sampler intends → posterior skew.

## Effective anonymity set per ring (provisional)

- rings ≥ 4 analyzed: 413
- N_eff mean: 20.4
- N_eff median: 16.0
- min / max: 1.0 / 32.0
- share with N_eff < half ring: 0%

*DRAFT — signals only; D4 validation required before any
production claim.*