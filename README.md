# DERO.STARGATE.DIAGRAMS

> ## ⚠️ DRAFT — NOT VERIFIED OR AUDITED
>
> These diagrams are a **community draft, work in progress**. They have **not**
> been technically verified, reviewed, or audited — not by the DERO team, not
> by auditors, and not by the community at large. Treat every figure as
> *"probably roughly right"* and **verify anything important against the
> primary sources** — [derod.org](https://derod.org) docs, the
> [deroproject/derohe](https://github.com/deroproject/derohe) source, and the
> projects' own repos — before relying on it. Dashed-border zones are
> explicitly hypothetical. Corrections and pull requests are very welcome.

Plain-language process diagrams explaining how DERO (DHEBP / Stargate) works —
from a single transaction, to the network's place in the modern world, to the
community ecosystem building on it today and what it can grow into.

Every diagram ships as an editable `.drawio` file (open at
[app.diagrams.net](https://app.diagrams.net)) plus PNG previews. Each diagram
is written for laymen: numbered steps, swimlanes, and a "💡 in plain words"
line under every step.

## The diagrams

| File | What it shows |
|------|---------------|
| **`DERO.PROCESS.COMPLETE.drawio`** | **The Journey of One DERO Transaction** — user → wallet → node → network → miners (AstroBWTv3 PoW) → encrypted ledger (DLT) → confirmation back to you. 2 pages: diagram + plain-language translation. |
| **`DERO.WORLD.drawio`** | **DERO's Place in the Modern World** — 5 everyday needs (paying, deals, data, apps, identity): centralized old world vs the DERO world. 2 pages: comparison + swap table. |
| **`DERO.MINING.drawio`** | **How DERO Mining Works — the Σ-block loop** — the network-is-the-pool design: ~2 s Σ-blocks, 18 s blocks, 9+1 mini-blocks, reward split, solo mining. 2 pages: loop + key numbers & FAQ. |
| **`DERO.TELA.drawio`** | **From Idea to On-Chain App** — building a dApp: DVM smart contract → `install_sc` → XSWD wallet bridge → TELA. 3 pages: flow + the dApp stack + **the community ecosystem index**. |
| **`DERO.UNIVERSE.drawio`** | **The DERO Universe** — one surfable map with a reading path: numbered zones (① engine → ② curated repos → ③ live use cases → ④ what can be born → ⑤ speculation), a "how to read" strip, and a 30-second TL;DR. Curated chips + pointers to the deep dives (full repo index lives on TELA p3; experimental use cases on the field guide). Solid borders = live now, dashed = hypothetical. |
| **`DERO.EXPERIMENTS.drawio`** | **Real-world use cases — the experimental field guide** — 12 use cases (gambling, patronage, DAO voting, private DeFi, marketplaces, supply chain, social, M2M payments, credentials, remittances, insurance, P2E) each with problem → DERO fit → status (live/partial/experimental) → FILLED BY (the real project in that slot, or "greenfield"). 3 pages: field guide + 5-step "run your own experiment" ramp + **deep dives: M2M payments & parametric insurance** (pattern, illustrative DVM-BASIC starter contract, honest blockers, simulator test path). |
| **`DERO.SYSTEMS.drawio`** | **Systems reference — how the whole stack fits together** — 4 pages: **full-node architecture** (derod internals: P2P/TLS, mempool, consensus core, GravitonDB, DVM, JSON-RPC, GETWORK + attached wallets/miners/services with ports), **network topology & ports** (who connects to whom, P2P 10101 / GETWORK 10100 / RPC 10102 / wallet 10103, security rules), **the protocol stack** (cryptography → consensus → ledger → VM → interfaces → applications), and **the derohe source-tree map** (each repo package and what it owns). |
| **`DERO.STYLE.drawio`** | **Template system showcase** — the shared design language for all diagrams. Two themes: **DHEBP Night** (dark, glass, glow — for sharing/cyber) and **DHEBP Paper** (light, print-friendly). Every component shown: gradient headers, zone panels, chips, number badges, status pills, arrows, TL;DR, draft stamp. Powered by `dero_style.py` — one file, both themes. |
| **`DERO.MASTER.drawio`** | **The DERO Universe (v2 skin)** — same content as DERO.UNIVERSE, rendered in the new template system. Generate dark or light with `python build_master_diagram.py dark|light`. |
| **`DERO.GUIDES.drawio`** | **Onboarding & safety** (3 pages): *Where Do I Begin?* (one entry → branch to the right diagram) · *Choose Your Wallet* (decision tree: CLI / Engram / g45w → seed backup) · *Self-Custody Security Poster* (DO/DON'T + threat model — DERO has no recovery). |
| **`DERO.PRIVACY.drawio`** | **Honest privacy & economics** (3 pages): *What 'Private' Actually Means* (hidden vs visible, honest limits — private ≠ anonymous) · *Privacy Scorecard* (DERO vs BTC vs Monero vs ETH, color-coded heuristic risk, DRAFT disclaimer) · *DERO Economics* (hard cap ~20.89M, emission, halving ~4yr, reward split — DRAFT numbers flagged). |
| **`DERO.DEVOPS.drawio`** | **Operator & builder reference** (4 pages): *Node Operator Runbook* (8 steps: download→sync→monitor→update→backup) · *XSWD Permission Model* (dApp↔wallet, ask/accept-always/deny-always, security rules) · *DVM-BASIC Cheat-Sheet* (install_sc, RETURN 0, STORE/LOAD, signatures, gas) · *Bridges & Interop* (ETH↔DERO, cldex, honest risk map). |
| `Stargate.High.Level` | Original high-level sketch (Layer 1 PoW → DVM). |
| `DERO.CLOUD.drawio` | Original cloud-architecture sketch. |

## Regenerating

Each diagram is generated from a **single Python data model** that emits both
the draw.io XML and the SVG preview, so the two can never drift apart.

```bash
python build_diagram.py          # -> DERO.PROCESS.COMPLETE.drawio
python build_world_diagram.py    # -> DERO.WORLD.drawio
python build_more_diagrams.py    # -> DERO.MINING.drawio + DERO.TELA.drawio
python build_universe_diagram.py # -> DERO.UNIVERSE.drawio
python build_experiments_diagram.py # -> DERO.EXPERIMENTS.drawio
python build_systems_diagram.py  # -> DERO.SYSTEMS.drawio
python build_guides_diagram.py   # -> DERO.GUIDES.drawio
python build_privacy_diagram.py  # -> DERO.PRIVACY.drawio
python build_devops_diagram.py   # -> DERO.DEVOPS.drawio
```

PNG previews are rendered from the SVGs with headless Chromium/Edge.

## Sources & verification

Facts are grounded in **derod.org** (full documentation corpus), the
**deroproject/derohe** source, and the community's own project index
(the "Dero Community" Discord list + GitHub):

- Chain parameters verified in `config/config.go`: `BLOCK_TIME = 18` (18 s
  blocks), `MINIBLOCK_HIGHDIFF = 9` → 10 mini-blocks per block (9 fast + 1
  final/high-diff), reward split verified in `transaction_execute.go`
  (equal shares across Σ-block winners + integrator, leftover dust to the
  integrator), halving every 7,000,000 blocks (~4 years).
- AstroBWTv3 CPU-only PoW (~256 MB/thread), TLS-encrypted P2P,
  erasure-coded blocks (48 → 16 chunks), homomorphic-encrypted balances
  (66 B/account, never decrypted), ring size 8, six bound proofs per
  transaction, hard cap ≈20.89M DERO.
- Ecosystem index (page 3 of `DERO.TELA.drawio`) covers the active community
  repos: **DEROFDN/derohe** (current dev home), DEROFDN/Engram, g45w,
  astrobwt-miner, tnn-miner, Dirtybird-C-Miner, dSlate, Gnomon/HyperGnomon,
  civilware/tela, **civilware/epoch** (crowd mining), xswd-api, DeroPay,
  DeroAuth, **Hologram**, **dReams**, **DeroBeats** (music), cldex/dero_swap,
  dero_lotto, dreamtables (baccarat & poker), deronfts, ORED, SovereignSearch,
  PureWolf/HyperWolf, tela-gateway, Dero Seals, Artificer NFA, Deroscapes,
  derobridge, DERO-Explorer-TELA and more.

## Mission

DERO has the technical capacity to replace centralized information technology
platforms in a secure, decentralized and private manner. This repository
brainstorms and diagrams how DERO will accomplish this — starting with the
Layer 1 network itself, and continuing toward interchain operations and
DERO layer 2 applications.
