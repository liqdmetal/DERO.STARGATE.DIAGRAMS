# DERO HE — Formal Specification of the Transaction Relation

**STATUS: ⚠️ DRAFT — NOT VERIFIED — WORK IN PROGRESS ⚠️**

> This document is a *skeleton* of a formal specification for the DERO HE
> (Stargate) transaction relation, extracted directly from the
> `derohe-Release151` source tree (v3.6.0-151, tag `898730e`).
>
> **It has NOT been reviewed by any cryptographer. It is NOT an audit.
> It is a structured starting point whose every predicate must be
> independently verified against the code, the original papers
> (Groth–Bootle one-out-of-many, Bulletproofs), and by formal-methods
> tooling before it can carry any authority.**
>
> Purpose: turn "encrypted state is safe" from a marketing claim into a
> checkable artifact, and scope the audit work. All code references are
> `file:line` into the Release 151 tree.

---

## 1. Scope and goals

The DERO HE chain stores each account's balance as an ElGamal ciphertext
and updates balances homomorphically. A transaction must prove, without
revealing amounts, sender, or receiver:

1. **Membership** — the sender is *one* of the ring members (one-out-of-many).
2. **Receiver hiding** — the receiver is also *one* of the ring members,
   at an index the observer cannot determine.
3. **Balance conservation** — the sum of encrypted balance changes is zero
   (what the sender loses, the receiver gains, fees excluded).
4. **Non-negativity** — after the transfer, the sender's balance is still in
   range (no negative balances, no inflation).
5. **Binding** — the proof is bound to the specific transaction (txid) and
   the specific chain state (roothash).

This document defines the exact relation the verifier checks and the exact
witness the prover holds. It does **not** (yet) prove security properties;
it pins down *what is being claimed*.

---

## 2. Notation

### 2.1 Groups and generators

| Symbol | Meaning |
|---|---|
| $\mathbb{G}$ | prime-order group (bn256 curve, order $q$) |
| $G, H$ | base generators, NUMS-derived: `HashToPoint(HashtoNumber("DERO"+"G"))` / `"DERO"+"H"` (`const.go:27`, `generatorparams.go`) |
| $G_i, H_i$ | vector generators, $i = 0..2m{-}1$: `HashToPoint("DERO"+"G" + hex(i))` etc. |
| $H_{2m}, H_{2m+1}$ | extra generators used in the one-out-of-many pairing check |
| $\mathbb{F}_q$ | scalar field |

All generators are **hash-to-point derived from the constant string
`"DERO"`** — i.e., no trusted setup, NUMS-style. **This must be confirmed
as a security claim**: the discrete-log relationship between any two
generators must be unknown (provable via the hash-to-point construction).

### 2.2 Hash functions

| Symbol | Definition | Code |
|---|---|---|
| `HashtoNumber` | bytes → $\mathbb{F}_q$ | `crypto/hash.go` |
| `HashToPoint` | bytes → $\mathbb{G}$ | `crypto/hashtopoint.go` |
| `reducedhash` | bytes → $\mathbb{F}_q$ (Fiat–Shamir challenge) | `crypto/hash.go` |
| `graviton.Sum` | bytes → 32B (key-pointer hashing) | `blockchain/graviton` |
| `sha3.Sum256` | block-header commitment | `miniblocks_consensus.go:43` |

**TODO (gap):** pin the exact byte-serialization conventions of every hash
input. The transcript order is security-critical and currently only defined
by the code.

### 2.3 ElGamal over $\mathbb{G}$

Balance ciphertext for account with public key $P$:

$$\mathrm{ElGamal}(P, v) = (C_L, C_R) = (P^{r} \cdot G^{v},\; G^{r})$$

with randomness $r \in \mathbb{F}_q$ (see `ConstructElGamal`,
`algebra_elgamal.go`). Homomorphic: $\mathrm{ElGamal}(P,a) \cdot
\mathrm{ElGamal}(P,b) = \mathrm{ElGamal}(P, a+b)$.

**Note (gap):** this is *additively* homomorphic ElGamal — NOT fully
homomorphic encryption. The "homomorphic encryption" marketing refers to
additive ElGamal on balances, which is the correct and sufficient primitive
for balance updates. The spec must state this precisely.

### 2.4 Chain state

- **Balance tree**: graviton key-value tree; key = 33-byte compressed
  account public key; value = serialized `NonceBalance`.
- `NonceBalance{NonceHeight uint64, Balance *ElGamal}`
  (`balance_serdes.go:29-32`).
- **Roothash**: top hash of the balance tree at a given state version —
  binds transactions to chain state.
- The chain resolves ring members by **key pointers**: the statement stores
  truncated hashes of ring-member public keys (`Bytes_per_publickey` bytes
  each), and the verifier re-expands them against the balance tree
  (`protocol_structures.go:34`, `transaction_execute.go:215-235`).

---

## 3. Transaction structure

### 3.1 Types

`PREMINE, REGISTRATION, COINBASE, NORMAL, BURN_TX, SC_TX`
(`transaction/transaction.go:30-40`). This spec covers **NORMAL** and
**SC_TX** (SC adds a DVM execution step; the balance relation is the same).

### 3.2 Statement (public input)

From `protocol_structures.go:29-39`:

$$s = (CLn,\; CRn,\; C,\; D,\; \texttt{Publickeylist},\; \texttt{Roothash},\; \texttt{Fees},\; \texttt{RingSize})$$

| Field | Type | Meaning |
|---|---|---|
| $CLn_i, CRn_i$ | $[\mathbb{G}]$, length $m$ | encrypted-balance *vectors* (for the anon-set linearization) |
| $C_i$ | $[\mathbb{G}]$, length $N=2^m$ | per-ring-member "change" commitment (left component) |
| $D$ | $\mathbb{G}$ | change commitment (right component) |
| `Publickeylist` | $[\mathbb{G}]$, length $N$ | the ring (sender + receiver + decoys) |
| `Roothash` | 32B | balance-tree top hash |
| `Fees` | $\mathbb{F}_q$ | **plaintext** fee (varint, serialized unencrypted) |
| `RingSize` | $N = 2^m$, $2 \le N \le 128$ | ring size (power of two) |

Serialization: `power` byte (`log2 N`), `Bytes_per_publickey`, fees varint,
$D$, key pointers, $C_i$, roothash (`protocol_structures.go:53-105`).

### 3.3 Witness (secret input)

From `protocol_structures.go:44-51` and `walletapi/transaction_build.go:321`:

$$w = (sk,\; r,\; \texttt{TransferAmount},\; \texttt{Balance},\; \texttt{Index})$$

| Field | Meaning |
|---|---|
| $sk$ | sender's secret key |
| $r$ | ElGamal randomness (deterministically derived, see §5.1) |
| `TransferAmount` | value sent (uint64) |
| `Balance` | sender's *post-transfer* balance (uint64) |
| `Index` | `[i_sender, i_receiver]` — positions in the ring |

---

## 4. The relation (informal statement)

> **R** — The prover knows $(sk, r, a, b, i_s, i_r)$ such that:
>
> 1. $a \in [0, 2^{64})$, $b \in [0, 2^{64})$ (range);
> 2. $sk$ is the secret key of $\texttt{Publickeylist}[i_s]$ (sender
>    membership);
> 3. $\texttt{Publickeylist}[i_r]$ is the receiver (receiver index hidden);
> 4. the balance changes sum to zero: sender loses $a + \texttt{Fees} +
>    \texttt{Burn}$, receiver gains $a$, all other ring members unchanged;
> 5. the proof is bound to `txid` and `Roothash`.

The *formal* relation is defined by the verifier's checks in §6. **A key
goal of this spec is to make (1)–(5) provably equivalent to those checks.**

---

## 5. Prover construction (from code)

### 5.1 Deterministic ElGamal randomness $r$

`walletapi/transaction_build.go:123-130`:

$$r = \mathrm{ReducedHash}\!\left(\mathrm{HashToPoint}\!\left(\mathrm{HashtoNumber}\!\left(\texttt{"DERO"} \,\|\, \texttt{roothash} \,\|\, \big\|_i \texttt{pubkey}_i\right)\right)^{sk}\right)$$

Deterministic per (roothash, ring, sender key). **Security note (gap):**
this makes $r$ *derivable from public data + sender key* — it is not
uniform randomness over the ciphertext space for an observer, but the
observer cannot compute it without $sk$. Must be analyzed for
ciphertext-indistinguishability (harvest-now-decrypt-later exposure).

### 5.2 Ring assembly (wallet)

`walletapi/transaction_build.go:54-115`:

- Ring = sender at `witness_index[0]`, receiver at `witness_index[1]`,
  then decoys; `witness_index` is a **shuffled** permutation with the
  constraint that sender and receiver indices have **opposite parity**
  (line 57-62: `witness_index[0]%2 != witness_index[1]%2`).
- Decoys come from `DERO.GetRandomAddress` (daemon-side uniform sample of
  the balance tree, **currently excluding accounts touched in the last 5
  blocks** — see §8, known issue K1).
- Per-member encrypted balance fetched via `DERO.GetEncryptedBalance`
  (**in the clear** — see K2).

### 5.3 Change commitments

For ring member $i$ (`transaction_build.go:140-200`):

- sender ($i = i_s$): change = $-(a + \texttt{fees} + \texttt{burn})$
- receiver ($i = i_r$): change = $+a$
- others: change = 0

Stored as $C_i = G^{\Delta_i}$ and $D$ (group element form); the verifier
reconstructs $\mathrm{ElGamal}(C_i, D)$.

### 5.4 The 128-bit range proof

`proof_generate.go:475-510`: the prover packs

$$n = a + (b \ll 64)$$

i.e. `TransferAmount` in the low 64 bits and post-transfer `Balance` in the
high 64 bits, and proves $n \in [0, 2^{128})$ via a Bulletproofs-style
inner-product argument over a 128-bit binary decomposition
(`proof_innerproduct.go` — hard-coded 7 recursion entries = $2^7 = 128$
bits, per the comment at `proof_innerproduct.go:38`).

**This simultaneously proves**: amount non-negative, post-balance
non-negative, both fit in 64 bits. Elegant, but the *semantic* claim
"balance after transfer ≥ 0" depends on `Balance` being the true
post-transfer balance — which is only enforced by the balance-conservation
check (§6.7). **This coupling is the single most important thing for an
auditor to verify.**

### 5.5 The one-out-of-many (membership)

`proof_generate.go:516-560, 600-740`:

- The index vector of length $2m$ encodes **both** `witness.Index[0]`
  (sender, low $m$ bits) and `witness.Index[1]` (receiver, high $m$ bits).
- The prover builds a 2-out-of-$N$... **TODO (gap):** confirm whether this
  is a *single* one-out-of-many over a $2m$-bit index (proving both sender
  and receiver positions) or two combined statements. The parity constraint
  and the special positions $i=0, i=m$ in the `aa` vector
  (`proof_generate.go:525-540`) suggest a combined construction — **must be
  pinned down exactly**.

### 5.6 Fiat–Shamir transcript

From `proof_verify.go:98-150` (verifier recomputes):

1. `statementhash = reducedhash(txid)` — proof bound to txid.
2. $v = \mathrm{reducedhash}(\texttt{statementhash} \,\|\, BA \,\|\, BS
   \,\|\, A \,\|\, B)$
3. $w = \mathrm{hashmash1}(v)$ — folds in all the anon-set points
   (`proof_generate.go:440-450`, `hashmash1` at 406-430).
4. $y = \mathrm{reducedhash}(w)$; $z = \mathrm{reducedhash}(y)$ — range
   proof challenges (`proof_generate.go:828-840`).

**TODO (gap):** produce the exact ordered byte-transcript for each of these
folds; this is the "transcript order" an auditor must verify against the
prover to rule out malleability.

---

## 6. Verification predicates (what consensus checks)

From `proof_verify.go:98+`, `transaction_verify.go`, `transaction_execute.go`.
Let $N = 2^m$ ring size.

### P1 — Sizes and shape
- $|C| = |\texttt{Publickeylist}| = N$ (`proof_verify.go:107`)
- $2 \le N \le 128$, $N$ power of two (`transaction_verify.go:300-305`)
- `len(f) = 2m` (`proof_verify.go:118`)

### P2 — Overflow guards
- `total_open_value = Fees + extra_value`, reject if overflow
  (`proof_verify.go:110-114`)

### P3 — Anonymity-set binding
- $v$ recomputed from (statementhash, BA, BS, A, B)
- $w = \mathrm{hashmash1}(v)$

### P4 — Parity condition
- Accept iff $w = f_0$ **or** $w = f_m$ (`proof_verify.go:137-145`)
- This enforces the bit-decomposition shape of the index commitment.

### P5 — One-out-of-many pairing check
- Recover: $\mathrm{stored} = B^w \cdot A$
- Compute: $\mathrm{computed} = \sum_k G_k^{f_{k,1}} \cdot
  H_k^{f_{k,1} f_{k,0}} \cdot H_{2m}^{f_{0,1} f_{m,1}} \cdot
  H_{2m+1}^{f_{0,0} f_{m,0}} \cdot H^{z_A}$
- Accept iff $\mathrm{stored} = \mathrm{computed}$ (`proof_verify.go:150-168`)

### P6 — Inner-product (range) proof
- Verify the 128-bit Bulletproofs inner product (`ip.Verify`).

### P7 — Balance conservation (consensus-level, `transaction_execute.go:214-241`)
For each ring member $i$: resolve key pointer → balance tree entry,
$b_i' = b_i + \mathrm{ElGamal}(C_i, D)$ (homomorphic add). **All ring
members' balances are updated** — and crucially, every ring member's
ciphertext is **re-randomized** even when the change is zero: the wallet
builds $C_i = G^{\Delta_i} \cdot P_i^{r}$ for *every* member
(`transaction_build.go:200-204`, where decoys get $\Delta_i = 0$ but still
receive $P_i^r$), with $D = G^r$. So the serialized balance of every ring
member changes on every appearance, and an observer **cannot** distinguish
"real participant" from "decoy" by comparing per-block ciphertext diffs.
This is a genuine privacy feature of the design — it defeats the naive
"which 2 members changed?" attack — and it has a second-order consequence:
the daemon's 5-block filter in `GetRandomAddress` (which compares
serialized ciphertexts) treats "appeared in any ring" as "touched", so the
decoy pool is effectively "accounts not seen in any ring for 5 blocks"
(see K1).

Non-negativity is guaranteed by P6 (the 128-bit packed range proof).

### P8 — State binding
- `Roothash` in the statement must match the balance-tree top hash at the
  block state version where the tx executes (`transaction_execute.go`,
  roothash checked in `BuildTransaction` → included in statement → bound
  via P3/P5 transcript).

---

## 7. Known deviations and gaps (must be resolved before formalization)

| ID | Issue | Severity | Where |
|---|---|---|---|
| G1 | Exact transcript byte-order for `hashmash1`, `v`, `y`, `z` folds not written down anywhere except code | High | `proof_generate.go:406-450, 828-840` |
| G2 | Whether the anon-set proof is one combined 2-index statement or two; the parity trick's formal role | High | `proof_generate.go:516-560` |
| G3 | NUMS claim for generators must be argued from `HashToPoint` construction | Medium | `generatorparams.go` |
| G4 | Security of deterministic $r$ (harvest-now-decrypt-later) | Medium | `transaction_build.go:123-130` |
| G5 | HF3 affected-tx whitelist (`hardfork_fixes.go`) — hard-coded parity overrides for ~17 txids; formal spec must model "exceptional" consensus states or the whitelist must be shown to be a pure bug-fix (no semantic change) | High | `blockchain/hardfork_fixes.go` |
| G6 | `max_bits` cap of 240 bits (`transaction_build.go:52`) — ring-size-dependent proof bound; formal bound? | Low | `transaction_build.go` |
| G7 | Silent zero-balance fabrication for unregistered accounts in `GetEncryptedBalanceAtTopoHeight` (`daemon_communication.go:419-427`) — a decoy can be a non-account with zero balance; does this weaken membership soundness? | Medium | `daemon_communication.go` |
| G8 | `retry_count % len(rings)` loop (`transaction_build.go:54`) re-randomizes `max_bits` — distributional effect on the proof, not semantic | Low | `transaction_build.go` |
| G9 | Fees plaintext: what exactly does `Fees` cover (per-payload? per-tx?), and the `(len+2)*FEE_PER_KB*(len/16+mult)` formula | Medium | `transaction_build.go:135-145` |
| G10 | Burn value interaction: `C_XG` computation folds `s.Fees + burn_value` into sender change — must be modeled as a third outflow | Medium | `proof_generate.go:710-735` |

---

## 8. Known privacy issues discovered during spec extraction

| ID | Issue | Fix direction |
|---|---|---|
| K1 | **Activity-based narrowing (corrected mechanism)**: daemon decoy selection excludes accounts whose ciphertext changed in the last 5 blocks (`rpc_dero_getrandomaddress.go:88-95`). Because *all* ring members are re-randomized (see P7 note), "changed" ⇔ "appeared in any ring" — so decoys are guaranteed **not seen in any ring for 5 blocks**, and any ring member that *was* in a ring recently is, with high probability, sender or receiver. This is the OSPEAD-style posterior skew, DERO-flavored. **Note: the naive ciphertext-diff attack (observe the 2 changed members) does NOT work — re-randomization changes every ring member's ciphertext.** | Remove/weaken filter; activity-matched sampling (see `decoy-activity-distribution.md`); wallet-side selection from a batch |
| K2 | **Daemon learns the ring**: wallet queries `DERO.GetEncryptedBalance` per candidate, in the clear (`daemon_communication.go:404-410`) → daemon can reconstruct the ring and often infer sender/receiver. | Batch balance RPC (`GetRandomAddressBatch` returning encrypted balances), wallet picks subset client-side |
| K3 | **Single-daemon trust**: decoys come from one daemon; a malicious node controls the candidate pool. | Multi-daemon sampling + client-side CSPRNG selection |
| K4 | **Bounded ring** (default 16, max 128) — no full-chain membership. | Research: membership against the graviton tree (the accumulator already exists) |

---

## 9. What "done" looks like (definition of completion for this spec)

1. Every predicate in §6 written as a formal statement (LaTeX/Coq-ready
   notation) with **exact** byte-level transcript definitions (resolves G1).
2. The anon-set statement pinned down (resolves G2) and matched against the
   Groth–Bootle / Bulletproofs literature.
3. Soundness & zero-knowledge claims *stated* per component, with
   assumptions listed (DDH for ElGamal, DL for membership, etc.).
4. G5–G10 resolved or explicitly deferred with rationale.
5. Cross-checked against a second reading of the code by an independent
   reviewer; then and only then, the DRAFT stamp is removed and an audit is
   scoped.

---

*Document generated from `derohe-Release151` source analysis. All
`file:line` references verified against the tree at extraction time.
This is a skeleton, not an audit. ⚠️ DRAFT — NOT VERIFIED ⚠️*
