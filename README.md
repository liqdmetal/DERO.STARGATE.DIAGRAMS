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
| **`DERO.UNIVERSE.drawio`** | **The DERO Universe** — one large surfable map: the live DHEBP engine → the community's repos today → live use cases → **what can be born** (hypothetical end-world results) and **speculation on new rails**. Solid borders = live now, dashed = hypothetical. |
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
