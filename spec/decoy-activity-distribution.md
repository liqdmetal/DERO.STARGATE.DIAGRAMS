# Decoy Activity-Distribution Analysis (OSPEAD for DERO)

**STATUS: ⚠️ DRAFT — RESEARCH PLAN — NOT EXECUTED ⚠️**

> The third track of the decoy-selection follow-up: replace
> uniform-over-registered-accounts decoy sampling with
> **activity-matched sampling**, so that an observer cannot distinguish
> real sender/receiver from decoys by on-chain activity alone.
> This is the DERO-account-model analog of Monero's OSPEAD work
> (Rucknium; getmonero.org 2025-04-05) and the arXiv:2408.05332
> traceability-heuristics line. This document is the *plan* — the
> measurement scripts, model, and validation methodology — not the
> results.

---

## 1. Motivation: what the corrected K1 analysis implies

From the transaction-relation spec (K1, P7): DERO's decoy pool is
effectively **"accounts not seen in any ring for the last 5 blocks"**,
because:

1. `DERO.GetRandomAddress` excludes any account whose serialized balance
   ciphertext changed in the last 5 blocks
   (`rpc_dero_getrandomaddress.go:88-95`);
2. since every ring appearance re-randomizes every member's ciphertext
   (`transaction_execute.go:238-241`, `C_i = G^{Δ_i}·P_i^r` even for
   decoys), "ciphertext changed" ⇔ "appeared in any ring".

**Consequence:** real participants — especially *recurring* ones (your
RelayOS settlement traffic: an AMM, a payroll contract, a market making
wallet) — appear in rings far more often than the 5-block-dormant accounts
that populate the decoy pool. An observer with full chain state can
compute, for every account, its ring-appearance history, and score each
ring member by "how unlike a decoy is this account's activity pattern?".
The posterior is skewed away from uniform; effective anonymity is smaller
than ring size.

**This is not the ciphertext-diff attack** (that one is dead — see P7).
It's a *distributional* attack: the decoy pool and the real-participant
population have different activity distributions, and that difference is
the leak.

**Goal:** make the decoy sampling distribution **match the real
participant distribution**, so that
$\Pr[\text{member } i \text{ is real} \mid \text{ring}, \text{history}]$
is uniform over ring members, regardless of the observer's activity model.

---

## 2. What an observer can actually see (threat model)

| Observable | Source | Notes |
|---|---|---|
| Ring membership per tx | public chain data | the ring is in the statement (key pointers → expanded) |
| "Account appeared in a ring at height H" | balance-tree ciphertext diffs per block | **complete** signal (all members re-randomized) |
| Last-appearance height (NonceHeight) | `NonceBalance.NonceHeight` is **plaintext** in the tree | coarser: updated only for `(i%2==0)==parity` members — but the diff signal is complete anyway |
| Account registration height | registration tx is public | account age |
| Block timestamps | public | wall-clock time of appearances |
| Amounts | **NOT observable** | ElGamal-encrypted; no amount signal exists on-chain |
| Fees | plaintext in statement | ring-size-correlated, not value-correlated |

So the observer's feature space is: **appearance times** (per account),
**account age**, **ring sizes** the account appears in. No amounts, no
balance magnitudes, no direction. This is both the constraint and the
opportunity: the decoy sampler only needs to match *activity*, which is
fully observable — so the match is verifiable.

---

## 3. The model

### 3.1 Formal setup

For a ring $R$ of size $N$ at block height $h$ with members
$m_1 \dots m_N$, exactly one member is the sender $s$, one is the
receiver $r$, and $N-2$ are decoys. The observer knows, for each member,
a feature vector $x_i$ (appearance history, age). The observer's
posterior:

$$\Pr[s = m_i \mid R, x] = \frac{\Pr[\text{participant} \mid x_i] \cdot \prod_{j \neq i} \Pr[\text{decoy} \mid x_j]}{\sum_k \Pr[\text{participant} \mid x_k] \cdot \prod_{j \neq k} \Pr[\text{decoy} \mid x_j]}$$

Writing $p(x) = \Pr[\text{participant} \mid x]$ (density of real
participant features) and $d(x) = \Pr[\text{decoy} \mid x]$ (density of
decoy features, which is the *sampling distribution we control*):

$$\Pr[s = m_i \mid R, x] = \frac{p(x_i) / d(x_i)}{\sum_k p(x_k)/d(x_k)}$$

The posterior is **uniform iff $p(x) = d(x)$** — i.e., iff decoys are
sampled from the same distribution as real participants. Any
distributional gap $\|p - d\|$ produces a non-uniform posterior and a
smaller *effective anonymity set*.

### 3.2 Effective anonymity set

Following the OSPEAD framing, define the effective set as:

$$N_{\text{eff}}(R) = \frac{1}{\max_i \Pr[s = m_i \mid R, x]}$$

For uniform posterior, $N_{\text{eff}} = N$ (full ring). The measurable
goal: **$N_{\text{eff}} \to N$** for the deployed decoy distribution.

### 3.3 What $p(x)$ looks like (hypotheses to test)

- **Appearance-interval distribution**: real participants likely have
  heavy-tailed inter-appearance gaps (many daily-active settlement
  accounts, some monthly). Decoys under the current scheme are
  *guaranteed* ≥5-block gaps — a sharp lower-tail cutoff that is itself a
  fingerprint.
- **Account age**: real participants skew newer (registrations grow over
  time; settlement wallets are recent). The decoy pool is uniform over all
  registered accounts — old accounts are over-represented.
- **Appearance regularity**: bots/AMMs appear on a near-periodic schedule
  (every $k$ blocks); human wallets are bursty. A uniform decoy sampler
  produces neither pattern.

All three are measurable from public data.

---

## 4. Measurement plan (executable, offline)

### 4.1 Data extraction

Requires a synced full node (or explorer API). Extract per block:

1. For each block $h$: the set of tx hashes; for each tx, the ring
   (expanded member addresses) and ring size.
2. Per account: registration height; ordered list of appearance heights
   (from ring membership; cross-checked against balance-tree ciphertext
   diffs and `NonceHeight`).
3. Timestamps from block headers.

**Deliverable D1:** `analysis/extract_activity.py` — dumps
`(account, reg_height, [appearance_heights])` to parquet/CSV.
(Cost: one full-chain scan; pruned chain suffices — the balance tree and
ring data are in the retained state.)

### 4.2 Estimating $p(x)$ (participant density)

We do **not** know which ring members are real — but we do know exactly
**two per ring are real** (sender + receiver) and $N-2$ are decoys. So
$p$ can be estimated by *deconvolution*: the observed mixture density over
all ring appearances is

$$f_{\text{obs}} = \frac{2}{N} p + \frac{N-2}{N} d$$

Given $d$ (known — it's the deployed sampler, or the candidate sampler in
simulation) and $f_{\text{obs}}$ (measured), solve for $p$. With two
distinct ring sizes (e.g., 16 and 32), the system is over-determined and
$p$ is identifiable. Validate with synthetic ground truth (§4.4).

**Deliverable D2:** `analysis/estimate_p.py` — mixture-deconvolution
estimator, outputting the fitted participant density $p$ (as a
parameterized family: e.g., log-normal / gamma inter-appearance
distribution, age distribution, regularity features).

### 4.3 Quantifying the current leak

- Compute the current $d_{\text{current}}$ exactly (it is *defined* by the
  code: uniform over accounts with no appearance in the last 5 blocks).
- Compute $N_{\text{eff}}$ per ring under the observed $f_{\text{obs}}$
  and the estimated $p$.
- Report: distribution of $N_{\text{eff}}$ across rings, and the fraction
  of rings where $N_{\text{eff}} < N/2$ (i.e., where the observer halves
  the anonymity set or worse).

**Deliverable D3:** `analysis/measure_leak.py` — leak report with
histograms and per-ring-type tables.

### 4.4 Validation with ground truth

The DERO simulator (`dvm/simulator.go`, `cmd/simulator`) can generate
chains with *known* sender/receiver assignments. Use it to:

1. Generate N simulated chains with realistic activity patterns (mixing
   settlement-bot, human, dormant accounts).
2. Run the extraction + deconvolution pipeline on simulated data where
   ground truth is known.
3. Measure estimator bias: does D2 recover $p$ within tolerance? Does D3's
   $N_{\text{eff}}$ match the true posterior (computed with ground truth)?

**Deliverable D4:** `analysis/sim_validation/` — simulation harness +
bias report. *This is the honesty gate: no production claim before the
estimator is validated on synthetic ground truth.*

---

## 5. The fix: activity-matched decoy sampling

### 5.1 Target distribution

Sample decoys from $\hat p$ (the validated estimate) instead of uniform.
Concretely, the sampler draws a candidate with:

- **Appearance-age match**: last appearance drawn from the estimated
  inter-appearance distribution (so decoys look like "someone who
  transacts with typical frequency", not "someone dormant for ≥5 blocks").
- **Age match**: registration-age distribution matched.
- **Regularity match (optional, v2)**: burstiness/periodicity features
  matched for decoys in rings where the sender is likely recurring
  (e.g., SC-invocation rings).

### 5.2 Where the model lives (trust note)

Two placement options, with a real trade-off:

- **(a) Daemon-side**: daemon samples from $\hat p$. Simple, but
  re-introduces the K2/K3 trust problem (daemon knows the ring and
  controls the distribution). Only acceptable combined with the batch RPC
  (wallet selects client-side from the batch).
- **(b) Wallet-side (recommended)**: the wallet maintains a compact
  activity model (a small table: quantiles of inter-appearance
  distribution, age distribution — kilobytes) synced/updated from a
  public dataset (e.g., a canonical model file published per epoch), and
  samples decoys itself from $\hat p$ over candidates obtained via the
  batch RPC. No daemon learns the ring; the model is public and
  verifiable.

### 5.3 Consensus impact

None — decoy selection is wallet/daemon-side; the chain verifies the
proof, not the sampling. The batch RPC (companion doc) is the enabling
protocol change; the activity model is pure client logic + a published
dataset.

---

## 6. Open research questions (must be answered before shipping)

1. **Identifiability of $p$**: is the 2/N-mixture deconvolution stable
   with real chain sizes and ring-size heterogeneity? (Validate in D4.)
2. **Feature sufficiency**: is (appearance time, age, regularity) enough,
   or do observers gain from *conditional* features (e.g., "appears in
   rings with the same SCID as this tx")? SC-specific activity may need
   per-asset models.
3. **Model drift**: how fast does $p$ change? If settlement traffic grows
   (RelayOS onboarding), the model must be re-published on a cadence;
   stale models re-create the leak.
4. **Adversarial response**: an observer knowing $\hat p$ exactly can
   still attack via *higher-order* features (pairwise correlations,
   co-appearance patterns). Does matching marginals suffice, or do we need
   pairwise/temporal matching? (Monero's OSPEAD stops at marginal age
   matching; DERO can do better because the feature space is smaller.)
5. **Ring-size heterogeneity**: rings are power-of-2 sizes 2..128; $p$ may
   differ by ring size (large rings used by privacy-conscious senders).
   Match per-size if measurable.

---

## 7. Deliverables and sequencing

| # | Artifact | Depends on | Est. effort |
|---|---|---|---|
| D1 | `extract_activity.py` (chain → activity dataset) | synced node | 3–5 days |
| D2 | `estimate_p.py` (mixture deconvolution) | D1 | 1–2 weeks |
| D3 | `measure_leak.py` (current $N_{\text{eff}}$ report) | D1, D2 | 3–5 days |
| D4 | simulator validation harness + bias report | D2, D3 | 1–2 weeks |
| D5 | activity-matched sampler (wallet, client-side) | D2, batch RPC | 1–2 weeks |
| D6 | canonical model publication (epoch-cadenced dataset) | D2 | ongoing |

Total: ~1–2 months of focused work for D1–D4 (the measurement + honesty
gate), before any production sampler (D5) is justified.

**Sequencing rule:** D5 is gated on D4 showing estimator bias within
tolerance on synthetic ground truth. The batch RPC (companion doc) can
ship independently and in parallel — it strictly improves the current
state even with uniform sampling.

---

## 8. Honest limitations

- This analysis is *activity-only*: amounts are invisible on-chain, so
  amount-correlation attacks (a real Monero concern) are structurally
  impossible here — that's a DERO advantage — but it also means the
  analysis cannot *prove* the absence of other, unforeseen signals.
- The plan assumes the observer's best model is the mixture
  decomposition; a more sophisticated observer (e.g., ML on the full
  appearance-sequence) may extract more. The validation (D4) should
  include an ML baseline to bound this.
- Small-chain statistics: DERO's real chain has far fewer accounts/txs
  than Monero; estimator variance will be higher. The report must quote
  confidence intervals, not point estimates.
- This is a *research plan*, not results. **No decoy-sampling change
  should ship on the strength of this document alone** — only on D4
  validation.

---

*⚠️ DRAFT — RESEARCH PLAN — NOT EXECUTED. Companion to
`derohe-transaction-relation-spec.md` (K1, P7) and
`decoy-selection-batch-rpc.md`. ⚠️*
