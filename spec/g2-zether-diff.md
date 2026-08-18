# G2 Resolution — DERO Proof vs. Zether (FC'20): Construction Diff

**STATUS: ⚠️ DRAFT — EXTRACTION-LEVEL ANALYSIS — NOT A SECURITY PROOF ⚠️**

> Companion to `derohe-transaction-relation-spec.md` §5.7. Maps DERO's
> proof system onto the Zether construction (Bünz, Agrawal, Zamani,
> Boneh, "Zether: Towards Privacy in a Smart Contract World", FC 2020,
> ePrint 2019/191) and lists every deviation. The goal: give the auditor
> a published, security-proven reference to diff against. Deviations are
> where the formal-soundness argument must be re-derived.

---

## 1. The identification

The verifier code (`cryptography/crypto/proof_verify.go`) uses internal
names — `AnonSupport`, `ProtocolSupport`, `SigmaSupport`, and the
commented reference line at `proof_verify.go:366-368` referencing
`zetherAuxiliaries` / `sigmaAuxiliaries` — that match the Zether
construction's structure exactly. DERO's proof is a **Zether-lineage**
protocol:

| Component | Zether (FC'20) | DERO (R151) | Deviation? |
|---|---|---|---|
| Account model | ElGamal-encrypted balances per account | `NonceBalance{NonceHeight, Balance *ElGamal}` | ✔ same |
| Balance update | homomorphic add of change | `nb.Balance.Add(ConstructElGamal(C[i], D))` | ✔ same |
| Membership | one-out-of-many (Groth–Bootle) over account set | one-out-of-many over ring, `aa/ba/bspecial` vectors | ⚠️ see §2 |
| Range proof | Bulletproofs | Bulletproofs-style inner product, hard-coded 128-bit | ⚠️ see §3 |
| Transfer statement | sender proves balance ≥ amount | packed 128-bit: `amount | balance<<64` | ⚠️ see §3 |
| Receiver | public (address in tx) | **hidden in ring**, index encrypted in payload | ❌ major extension, see §4 |
| Fees | public | public in statement | ✔ same |
| Smart-contract integration | Zether is a contract module | native DVM | n/a |

---

## 2. One-out-of-many: the index encoding

### Zether
Zether's one-out-of-many proves the prover knows the secret key of **one**
account in a set of $N$ (the anonymity set / ring). The prover commits to
a binary vector $b \in \{0,1\}^m$, $m = \log_2 N$, encoding the index
$i$ of the true account.

### DERO (R151)
`proof_generate.go:516-560`: the index vector has length **2m** and
encodes **two indices**: `witness_index = reverse(bits(Index[1], m) ||
bits(Index[0], m))` — the sender's position in the low $m$ bits, the
receiver's in the high $m$ bits, then reversed. The `aa` vector has
special zero positions at $i = 0$ and $i = m$ (`proof_generate.go:525-540`).

**This is a two-index one-out-of-many**: a single proof shows the prover
knows the secret key for the sender position *and* that the receiver is
another (distinct) ring member. The parity constraint (sender/receiver at
opposite parity, `transaction_build.go:57-62`) and the verifier's parity
check (`w == f[0] or w == f[m]`, `proof_verify.go:137-145`) bind the two
indices together.

**Audit implication:** Zether's security proof covers the one-index case.
The 2m-bit two-index extension is DERO-specific and MUST have its own
soundness argument: does knowing $sk$ for one position + the commitment to
both positions prove the receiver index is *also* a real ring member
(rather than an arbitrary second position)? This is the **single most
important deviation to prove**.

---

## 3. The packed 128-bit range proof

### Zether
Zether proves $0 \le b \le \texttt{balance}$ with a range proof on the
balance minus amount (or via its own transfer statement), i.e., the
*relation between amount and balance* is established by arithmetic in the
statement.

### DERO (R151)
`proof_generate.go:475-510`: the prover packs
$n = \texttt{TransferAmount} + (\texttt{Balance} \ll 64)$ and proves
$n \in [0, 2^{128})$ via a Bulletproofs-style inner product over a 128-bit
binary decomposition (`proof_innerproduct.go`, hard-coded 7 recursion
levels = 128 bits).

**Effect:** one range proof simultaneously proves amount ∈ [0, 2⁶⁴) and
post-transfer balance ∈ [0, 2⁶⁴). The "balance after transfer ≥ 0" claim
is *implied* by the packing — there is no separate
$\texttt{balance} \ge \texttt{amount}$ arithmetic relation in the
statement.

**Audit implication:** the semantic claim "sender can't go negative" rests
entirely on: (a) the packing convention, (b) the balance-conservation check
(P7: change = -(amount+fees+burn) for sender, +amount for receiver, 0 for
others), and (c) the range proof. If an implementation ever desynchronized
the packing convention from the conservation rule, the negative-balance
guarantee would silently break while all proofs still verify. This is the
**second-most-important deviation to prove** — and the Zether mapping does
not cover it (Zether's range is on the balance-amount difference, not a
packed double).

---

## 4. Hidden receiver (major extension)

### Zether
The receiver is public: a Zether transfer lists the recipient address.

### DERO (R151)
The receiver is **also a ring member at a hidden position**:

- `transaction_build.go`: receiver placed at `witness_index[1]` in the
  shuffled ring; the position byte is encrypted into the payload under a
  shared secret derived from the receiver's public key
  (`transaction_build.go:145-155`: `payload := []byte{byte(witness_index[1])}`
  encrypted via `EncryptDecryptUserData` with
  `Keccak256(shared_key || receiver_pubkey)`).
- The one-out-of-many (2m-bit) binds the receiver index.

**Effect:** neither sender nor receiver is identifiable from the ring
alone. This is a genuine privacy improvement over Zether, and it is the
largest *unproven* surface: the payload-encryption scheme
(`EphemeralKey`/`GenerateSharedSecret`/`EncryptDecryptUserData`) and its
binding to the statement must be analyzed (does the receiver index byte
actually match the index committed in the proof? what prevents a
malleability attack that re-encrypts a different index?).

**Audit implication:** the payload encryption is essentially a stealth-
address mechanism layered on top of the Zether core. It needs: (a) a
soundness argument that the encrypted index equals the proven index;
(b) an IND-CPA-style argument for the payload ciphertext; (c) analysis of
the deterministic `r` derivation (`transaction_build.go:123-130`) for
harvest-now-decrypt-later exposure (G4).

---

## 5. Transcript and Σ-protocol structure

The Fiat–Shamir chain (§5.7 of the spec) matches the Zether Σ-protocol
shape: anon-set commitments → challenge `v` → folding `w` → the
`B^w·A` recovery → range challenges `y, z` → `x` (T₁,T₂) → the six
sigma commitments `A_y, A_D, A_b, A_X, A_t, A_u` → challenge `c` → final
inner-product challenge `o`. The `u`-point binding (`PROTOCOL_CONSTANT ||
Roothash || scid || scid_index`) is DERO's addition for smart-contract
asset binding (Zether binds to the contract address/instance instead).

**Deviations in detail:**

| Transcript element | Zether | DERO | Notes |
|---|---|---|---|
| Base binding | contract instance | `u` point = HashToPoint(SCID, roothash, index) × sk | DERO-specific; must verify it's bound into `c` (it is: `A_u = u^{s_sk} · u^{-c}`) |
| `w` fold | over anon-set points | `hashmash1` over 8 point-vectors (CLnG, CRnG, C_0G, DG, y_0G, gG, C_XG, y_XG) | order verified identical prover/verifier (§5.7) |
| Range challenges | Bulletproofs y,z over 64-bit | y,z over 128-bit with `twoTimesZSquared` | dimension differs |
| Sigma responses | s_sk, s_r, s_b, s_tau, t̂, μ | same six | ✔ matches |

---

## 6. What must be proved (the G2 audit scope, prioritized)

1. **[P0] Two-index one-out-of-many soundness** — prove that a valid proof
   implies: the prover knows sk for exactly one ring position AND the
   committed receiver position corresponds to a second ring member. (No
   Zether reference covers this.)
2. **[P0] Packed-range conservation coupling** — prove that (packing
   convention ∧ P7 conservation ∧ range proof) ⇒ sender balance ≥ 0
   post-transfer, with no missing relation between amount and balance.
3. **[P1] Hidden-receiver payload** — prove the encrypted index byte equals
   the proven index and the ciphertext is IND-CPA under the ephemeral key
   scheme.
4. **[P1] `u`-point binding** — prove the asset/roothash binding is
   effective (no cross-asset proof reuse).
5. **[P2] Full transcript conformance** — machine-check the §5.7 chain
   against the reference implementation (test vectors, §10.1 of the spec).
6. **[P2] Zether-diff completeness** — walk the Zether paper section by
   section, confirm no *other* deviation exists (this document is the
   start of that walk, not the end).

---

## 7. References

- Zether paper: https://eprint.iacr.org/2019/191 (FC 2020, pp. 423–443)
- DERO code (R151): `cryptography/crypto/proof_generate.go`,
  `proof_verify.go`, `proof_innerproduct.go`, `protocol_structures.go`,
  `walletapi/transaction_build.go`
- Spec: `derohe-transaction-relation-spec.md` (§5.7 transcript, §6
  predicates, §7 normative contract, §10.1 vectors)

*⚠️ DRAFT — extraction-level analysis. The deviations listed here are the
audit scope, not conclusions about soundness. Nothing here is a claim
that DERO's proof is or is not secure — that requires the formal work
described in §6. ⚠️*
