# Decoy Selection Fix — Batch RPC + Client-Side Selection

**STATUS: ⚠️ DRAFT — NOT IMPLEMENTED — DESIGN PROPOSAL ⚠️**

> Design for killing the active-account narrowing heuristic (K1) and the
> daemon-ring-leak (K2) from the transaction-relation spec. No consensus
> change required — wallet↔daemon protocol change only. Companion to
> `spec/derohe-transaction-relation-spec.md`.

---

## 1. Problem recap (verified in Release 151)

**K1 — Active-account narrowing.** `DERO.GetRandomAddress`
(`cmd/derod/rpc/rpc_dero_getrandomaddress.go:82-111`) samples the balance
tree uniformly but **skips any account whose ciphertext changed in the
last 5 blocks** (`bytes.Compare(v, v_old) != 0 → continue`). Since decoys
are *guaranteed* untouched for 5 blocks, any ring member that *was*
touched is, by construction, sender or receiver. An observer computing
per-block balance-tree diffs can read this signal off public state.

**K2 — Daemon learns the ring.** The wallet fetches the encrypted balance
of every decoy candidate it keeps via `DERO.GetEncryptedBalance` with the
address **in plaintext** (`walletapi/daemon_communication.go:404-410`,
called per-candidate from `wallet_transfer.go:343-360`). A daemon sees:
wallet's own address (constant polling), receiver address, and every decoy
re-queried milliseconds after serving it. Node-controlled decoys + clear
balance fetches = daemon reconstructs the ring and often infers
sender/receiver from query order and timing.

**K3 — Single-daemon trust.** All candidates come from one daemon. A
malicious node controls the entire candidate pool.

---

## 2. Design: split by trust domain

### Principle

- **Node side = raw material only.** The daemon provides a large,
  unbiased batch of *real registered accounts* with their encrypted
  balances, sampled from the balance tree. It must not be able to learn
  which subset becomes the ring.
- **Wallet side = selection.** The wallet verifies the batch (registration,
  balance present) and picks the final ring uniformly at random,
  client-side, with its own CSPRNG. The node's posterior over the true
  ring after serving a batch of size $B$ for a ring of size $R$ is
  $1/\binom{B}{R}$ — its information advantage is destroyed.
- **The 5-block filter is removed** in the batch path (replaced by a weak
  age floor that cannot act as a discriminator — see §4).

### 2.1 New RPC: `DERO.GetRandomAddressBatch`

```
Request:
{
  "scid":  "0x00...",          // asset tree; zero = base DERO tree
  "count": 512,                // desired batch size (cap: 512)
  "exclude_recent_blocks": 1,  // weak floor: exclude only current block's
                               // touched set (default 1, NOT 5)
  "state_root": "0x..."        // optional: pin the balance-tree state root
                               // the wallet wants the batch from
}

Response:
{
  "state_root": "0x...",       // balance-tree top hash the batch is from
  "topoheight": 123456,        // so the wallet can cross-check state
  "candidates": [
    {
      "address": "deto1...",           // full address
      "registered": true,              // verified present in balance tree
      "encrypted_balance": "0x..."     // serialized ElGamal ciphertext
    }, ...
  ]
}
```

### 2.2 Wallet-side algorithm (client)

```
ring_select(batch, ringsize, sender, receiver):
  1. verify batch: every candidate has valid address format,
     registered == true, balance present (reject batch on any failure —
     fail-closed against ghost/zero injection)
  2. drop sender, receiver, duplicates
  3. if len(valid) < ringsize - 2:  fetch another batch (different daemon
     if available), merge, retry; else abort tx
  4. CSPRNG: draw (ringsize - 2) candidates uniformly from valid set
  5. build ring, proceed with existing BuildTransaction path (unchanged)
```

### 2.3 Multi-daemon option (K3)

Wallet configured with N daemon endpoints (or uses `add-exclusive-node`
peers): request batches from ≥2 daemons, merge, select. A single malicious
node then cannot control the pool unless all N are colluding. Cost: extra
RPC round-trips; make it configurable (`--decoys-from-peers` style), not
mandatory.

---

## 3. Security argument (informal)

1. **No active-account signal (K1 fixed):** decoys are drawn from the full
   registered set including recently-active accounts; "recently touched"
   is no longer a predictor of sender/receiver membership. The only
   remaining filter (current block's touched set) is too small a window to
   build a posterior against — verify this claim with the OSPEAD-style
   analysis in §4.
2. **Daemon cannot reconstruct ring (K2 fixed):** daemon sees one batch
   request; the wallet's selection happens offline. Daemon posterior over
   the ring is uniform over $\binom{B}{R}$ subsets.
3. **No ghost injection (K3 fixed):** wallet verifies `registered` +
   balance for every candidate; a zero-balance fake is rejected
   (eliminates the silent zero-fabrication path at
   `daemon_communication.go:419-427`).
4. **No consensus impact:** decoy selection is not consensus-enforced
   today; the change is RPC surface + wallet logic. Ships in a normal
   release, no hard fork.

### 3.1 What this does NOT fix (honest limits)

- The receiver's *activity pattern* may still differ from the decoy
  population (e.g., a monthly-active receiver among mostly-daily-active
  decoys). Uniform sampling fixes sender-selection statistics, not
  activity-distribution matching. That is the OSPEAD-style research step.
- Timing/network metadata (first-seen, IP) — orthogonal; see Dandelion
  discussion.
- Bounded ring (K4) — separate research track (graviton-tree membership).

---

## 4. Open question: uniform vs activity-matched selection

Uniform-over-registered-accounts is a large improvement but not provably
optimal. Monero's literature (OSPEAD, arXiv:2408.05332) shows decoys
should match the *real spend distribution*. For DERO's account model the
analog is: match the distribution of (sender, receiver) *activity* — e.g.,
account age, touch frequency, touch recency — so that an observer cannot
distinguish real participants from decoys by activity alone.

Proposed follow-up: instrument the chain (offline analysis of the public
balance-tree diffs, which reveal *touch events* but not amounts) to
measure the real activity distribution, then define the decoy sampling
distribution to match it. **This is research, not a code fix — do not ship
it as part of the batch RPC.**

---

## 5. Implementation sketch (diff-level)

| File | Change |
|---|---|
| `cmd/derod/rpc/rpc_dero_getrandomaddress.go` | Add `GetRandomAddressBatch` handler; parameterize the recency floor; return `registered` + `encrypted_balance` per candidate; cap 512 |
| `cmd/derod/rpc/websocket_server.go` | Register `getrandomaddressbatch` |
| `walletapi/daemon_communication.go` | Add `Random_ring_members_batch()`; no more per-member `GetEncryptedBalance` calls during ring assembly |
| `walletapi/wallet_transfer.go:343-360` | Replace loop with batch fetch + client-side CSPRNG selection |
| `rpc/` | Add `GetRandomAddressBatch_Params/Result` structs |
| `config/` | Optional `--decoys-batch-size`, `--decoys-daemons` (multi-daemon) |

Estimated effort: 1–2 weeks including tests. No hard fork, no consensus
change, no wallet-file format change.

---

*⚠️ DRAFT — NOT IMPLEMENTED — design proposal for review. Verify the
recency-floor reasoning and the $\binom{B}{R}$ posterior claim before
implementation.*
