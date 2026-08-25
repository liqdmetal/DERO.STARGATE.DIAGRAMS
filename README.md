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

## 🗂️ Start here: `index.html`

The whole library on one page — every diagram with a preview thumbnail and
an **Open in drawio** link (via the diagrams.net viewer, no install needed).
Open `index.html` in a browser (it lives in this repo).

Every diagram ships as an editable `.drawio` file (open at
[app.diagrams.net](https://app.diagrams.net)) plus PNG previews. Each diagram
is written for laymen: numbered steps, swimlanes, and a "💡 in plain words"
line under every step.

## The diagrams (11 files, 30+ pages)

| File | What it shows |
|------|---------------|
| **`DERO.GUIDES.drawio`** | **Onboarding & safety** (3p): Where Do I Begin? · Choose Your Wallet · Self-Custody Security poster. |
| **`DERO.PROCESS.COMPLETE.drawio`** | **The Journey of One Transaction** (2p): user → wallet → node → network → miners → encrypted ledger → confirmation. |
| **`DERO.WORLD.drawio`** | **DERO's Place in the Modern World** (2p): 5 needs — old centralized vs DERO world + swap table. |
| **`DERO.MINING.drawio`** | **Mining: the Σ-block loop** (2p): network IS the pool, ~2s Σ-blocks, 18s blocks, 9+1, FAQ. |
| **`DERO.TELA.drawio`** | **From Idea to On-Chain App** (3p): DVM → install_sc → XSWD → TELA + dApp stack + **community ecosystem index (40+ repos)**. |
| **`DERO.MASTER.drawio`** | **The DERO Universe** (1p): engine → repos → live use cases → what can be born → speculation. Glanceable, dark/light. |
| **`DERO.EXPERIMENTS.drawio`** | **Real-world use cases** (3p): 12 use cases + FILLED BY project + 5-step experiment ramp + deep dives (M2M, insurance). |
| **`DERO.SYSTEMS.drawio`** | **Systems reference** (4p): full-node architecture · network topology & ports · protocol stack · derohe source-tree map. |
| **`DERO.PRIVACY.drawio`** | **Honest privacy & economics** (3p): What "private" actually means · DERO vs BTC vs XMR vs ETH · DERO Economics. |
| **`DERO.DEVOPS.drawio`** | **Operator & builder reference** (4p): node runbook · XSWD permission model · DVM cheat-sheet (Release153-grounded) · bridges & interop. |
| **`DERO.STYLE.drawio`** | **Template system showcase** (2p): DHEBP Night (dark) + DHEBP Paper (light) — all components. |
| `Stargate.High.Level` | Original high-level sketch. |
| `DERO.CLOUD.drawio` | Original cloud-architecture sketch. |

## Regenerating

Each diagram is generated from a Python data model. Pass `light` or `dark` for
the theme (DHEBP Paper / DHEBP Night):

```bash
python build_diagram.py light|dark          # -> DERO.PROCESS.COMPLETE.drawio
python build_world_diagram.py light|dark    # -> DERO.WORLD.drawio
python build_more_diagrams.py light|dark    # -> DERO.MINING.drawio + DERO.TELA.drawio
python build_master_diagram.py light|dark   # -> DERO.MASTER.drawio + preview
python build_experiments_diagram.py light|dark # -> DERO.EXPERIMENTS.drawio
python build_systems_diagram.py light|dark  # -> DERO.SYSTEMS.drawio
python build_guides_diagram.py light|dark   # -> DERO.GUIDES.drawio
python build_privacy_diagram.py light|dark  # -> DERO.PRIVACY.drawio
python build_devops_diagram.py light|dark   # -> DERO.DEVOPS.drawio
```

SVG previews for all diagrams (except MASTER/STYLE which have their own):
```bash
python render_drawio_svg.py DERO.*.drawio   # -> preview_DERO.*.svg
```

PNG screenshots are rendered from the SVG previews with headless Edge/Chromium.

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
