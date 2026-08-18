#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DERO Mining + TELA/dApps diagram generator.
Mining: 2 pages (Sigma-block loop | key numbers & FAQ)
TELA:   3 pages (idea -> on-chain app | dApp stack | community ecosystem index)
Emits draw.io XML + SVG previews from one data model.
Sources: derod.org corpus, derofoundation.org, DEROFDN/derohe + community repos.
"""
import xml.sax.saxutils as sax
import datetime, html

TITLE_COLOR = "#4277BB"
INK, GRAY = "#22303C", "#5A6B7A"
ACCENTS = {"user": "#F9A825", "green": "#2E7D32", "blue": "#1E88E5",
           "purple": "#8E24AA", "orange": "#FB8C00", "teal": "#00838F",
           "red": "#C62828", "gray": "#6E6F72"}
TINTS = {"user": "#FFF8E1", "green": "#E8F5E9", "blue": "#E3F2FD",
         "purple": "#F3E5F5", "orange": "#FFF3E0", "teal": "#E0F7FA",
         "red": "#FDECEA", "gray": "#F0F2F5"}
STATUS_COLORS = {"active": "#2E7D32", "developing": "#F9A825", "alpha": "#8E24AA",
                 "stale": "#6E6F72", "paused": "#C62828", "beta": "#1E88E5"}
W, H = 1920, 1400

def esc(s):
    return sax.escape(s, {"'": "&apos;"})

def val(s):
    return s.replace("<", "&lt;").replace(">", "&gt;")

import re
def _draft_cell(h):
    return ('<mxCell id="draft" value="&#9888;&#65039; DRAFT &#8212; community draft \u2014 not verified, reviewed, or audited" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FDECEA;strokeColor=#C62828;strokeWidth=2;fontSize=11;fontStyle=1;fontColor=#C62828;align=center;verticalAlign=middle;" vertex="1" parent="1">'
            f'<mxGeometry x="18" y="{h-44}" width="380" height="34" as="geometry"/></mxCell>')

def inject_draft(model):
    m = re.search(r'pageHeight="(\d+)"', model)
    h = int(m.group(1)) if m else 1400
    return model.replace('<mxCell id="1" parent="0"/>', '<mxCell id="1" parent="0"/>' + _draft_cell(h), 1)

def inject_draft_svg(svg):
    m = re.search(r'height="(\d+)"', svg)
    h = int(m.group(1)) if m else 1400
    chip = (f'<rect x="18" y="{h-44}" width="380" height="34" rx="8" fill="#FDECEA" stroke="#C62828" stroke-width="2"/>'
            f'<text x="208" y="{h-22}" text-anchor="middle" font-size="11" font-weight="700" fill="#C62828">\u26A0\uFE0F DRAFT \u2014 community draft: not verified, reviewed, or audited</text>')
    return svg.replace('</svg>', chip + '</svg>')

def svg_esc(s):
    return html.escape(s)

def wrap(text, width_px, font_px, factor=0.55):
    cap = max(8, int(width_px / (font_px * factor)))
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        cand = (cur + " " + w_).strip()
        if len(cand) <= cap or not cur:
            cur = cand
        else:
            lines.append(cur); cur = w_
    if cur:
        lines.append(cur)
    return lines

def html_cell(title, accent, body_lines, plain_lines, title_size=12.5):
    parts = [f'<font color=&quot;{accent}&quot;><b>{esc(title)}</b></font>']
    parts += [esc(x) for x in body_lines]
    parts += [""] if plain_lines else []
    parts += [f'<font color=&quot;#66727E&quot;><i>\U0001F4A1 {esc(x)}</i></font>' for x in plain_lines]
    return val("<br>".join(parts))

# ========================================================== MINING ==========
MINING_STEPS = [
    dict(n=1, title="SET UP (5 minutes)", acc="blue",
         body=["Run derod (the node) + the AstroBWTv3 miner on any CPU. Point it at your wallet:",
               "--integrator-address / --wallet-address."],
         plain="Mining is open to any PC \u2014 no ASICs, no GPUs, no pool."),
    dict(n=2, title="SOLVE THE PUZZLE", acc="orange",
         body=["The miner races to find a \u03a3-block (mini-block) by solving a memory-hard puzzle",
               "(\u2248256 MB per thread). Difficulty adjusts every block to hold the 18 s pace."],
         plain="A CPU lottery ticket every ~2 seconds."),
    dict(n=3, title="WIN A \u03a3-BLOCK (\u2248every 2 s)", acc="orange",
         body=["Found one: your mini-block is gossiped to the network. 9 regular \u03a3-blocks + a 10th",
               "high-difficulty FINAL \u03a3-block close the main block at 18 s."],
         plain="Each \u03a3-block has a winner \u2014 up to 10 miners get paid per block."),
    dict(n=4, title="THE NETWORK CHECKS (18 s block)", acc="purple",
         body=["The block is erasure-coded (48 chunks, any 16 rebuild it) and every node re-validates.",
               "Rewards are split evenly among the \u03a3-block winners + the block integrator."],
         plain="Everyone double-checks the page before it is bound into the notebook."),
    dict(n=5, title="YOU GET PAID", acc="green",
         body=["Your share of reward + fees lands in your encrypted balance. Big miners win more often;",
               "small miners still earn daily. No pool fees, no trust."],
         plain="Rewards arrive automatically \u2014 the network IS the pool."),
]

MINE_NUMBERS = [
    ("~2 s", "per \u03a3-block (mini-block) emission"),
    ("18 s", "main block \u2014 settles 10 \u03a3-blocks"),
    ("10", "\u03a3-blocks per block (9 + 1 final)"),
    ("~48,000", "\u03a3-blocks per day (4,800 blocks \u00d7 10)"),
    ("88.4 / 10 / 1.6", "reward split \u2014 miners / integrator / your pool fee"),
    ("\u2248256 MB", "AstroBWTv3 memory per thread \u00b7 CPU-only, ASIC/GPU resistant"),
    ("every block", "difficulty retarget \u2014 keeps the 18 s pace"),
    ("every ~4 years", "reward halving (7,000,000 blocks) \u00b7 hard cap \u224820.89M"),
]

MINE_FAQ = [
    ("Do I need a mining pool?", "No \u2014 DERO\u2019s \u03a3-block system makes the network the pool. Rewards are proportional to your hashrate share."),
    ("Can I mine on a laptop?", "Yes \u2014 AstroBWTv3 is CPU-only and memory-hard. You win less often than a big rig, but you still earn."),
    ("How much will I earn?", "Expected \u03a3-blocks/day = (your hashrate \u00f7 network hashrate) \u00d7 48,000. Check current hashrate in your daemon."),
    ("When do I get paid?", "Rewards are distributed every block (~18 s) to the \u03a3-block winners, proportional to their work."),
    ("What is the integrator bonus?", "Run a daemon with --integrator-address: you get 10% of every block you integrate + 1.6% if you run your own pool."),
    ("How do I start?", "Download derod + dero-miner from derod.org, sync the chain, set --integrator-address and --wallet-address, mine."),
]

def mining_p1_cells():
    cells = []
    add = cells.append
    add(f'<mxCell id="m-t1" value="HOW DERO MINING WORKS \u2014 THE \u03a3-BLOCK LOOP" style="text;html=1;align=center;fontSize=30;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="42" as="geometry"/></mxCell>')
    add(f'<mxCell id="m-t2" value="The network is the pool: every CPU miner earns \u2014 no pools, no ASICs, no trust.  (\u03a3-block = Sigma block = mini-block)" style="text;html=1;align=center;fontSize=14;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    # steps: snake layout 3 top + 2 bottom
    xs = [60, 520, 980, 300, 760]
    ys = [150, 150, 150, 620, 620]
    ws = 400
    hs = 330
    for i, s in enumerate(MINING_STEPS):
        x, y = xs[i], ys[i]
        b = wrap(" ".join(s["body"]), ws - 24, 11.0)
        p = wrap(s["plain"], ws - 24, 10.5)
        step_title = f"{s['n']} \u00b7 {s['title']}"
        add(f'<mxCell id="m-s{i}" value="{html_cell(step_title, ACCENTS[s["acc"]], b, p)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={ACCENTS[s["acc"]]};strokeWidth=2;verticalAlign=top;align=left;spacing=10;spacingTop=18;fontSize=11;fontColor={INK};" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{ws}" height="{hs}" as="geometry"/></mxCell>')
        add(f'<mxCell id="m-bd{i}" value="{s["n"]}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={ACCENTS[s["acc"]]};strokeColor=#FFFFFF;strokeWidth=2;fontColor=#FFFFFF;fontSize=15;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="{x-17}" y="{y-17}" width="34" height="34" as="geometry"/></mxCell>')
    # arrows
    def arrow(eid, p1, p2, label=None):
        add(f'<mxCell id="{eid}" value="{esc(label) if label else ""}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=classicThin;endFill=1;strokeColor={EDGE_BLUE};strokeWidth=2.5;fontSize=10.5;fontStyle=1;fontColor={EDGE_BLUE};labelBackgroundColor=#FFFFFF;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{p1[0]}" y="{p1[1]}" as="sourcePoint"/><mxPoint x="{p2[0]}" y="{p2[1]}" as="targetPoint"/></mxGeometry></mxCell>')
    arrow("m-a1", (460, 315), (520, 315))                     # 1->2
    arrow("m-a2", (920, 315), (980, 315))                     # 2->3
    arrow("m-a3", (1380, 340), (1380, 600), "the block settles")  # 3 down
    arrow("m-a4", (1380, 600), (500, 600))                    # to 4
    arrow("m-a5", (500, 650), (500, 620))                     # into 4 top? 4 at (300,620) -> arrow (500,600)->(500,620) hmm
    arrow("m-a6", (700, 785), (760, 785))                     # 4->5
    arrow("m-a7", (1160, 640), (1160, 1090), "reward + fees") # 5 down to bottom band
    # sigma numbers card (right)
    add(f'<mxCell id="m-num" value="THE MATH OF \u03a3-BLOCKS" style="text;html=1;align=left;fontSize=14;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="1440" y="150" width="300" height="22" as="geometry"/></mxCell>')
    ny = 180
    for num, desc in MINE_NUMBERS:
        add(f'<mxCell id="m-n-{num[:6]}" value="{val(f"<font color=&quot;{TITLE_COLOR}&quot;><b>{esc(num)}</b></font>  <font color=&quot;#66727E&quot;>{esc(desc)}</font>")}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F4F8FC;strokeColor={TITLE_COLOR};strokeWidth=1.5;fontSize=11.5;fontColor={INK};align=left;verticalAlign=middle;spacing=8;" vertex="1" parent="1"><mxGeometry x="1440" y="{ny}" width="430" height="56" as="geometry"/></mxCell>')
        ny += 64
    # bottom band
    add(f'<mxCell id="m-f1" value="WHY IT MATTERS" style="text;html=1;align=left;fontSize=15;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="40" y="1095" width="260" height="22" as="geometry"/></mxCell>')
    add(f'<mxCell id="m-f2" value="Old mining: small miners earn nothing, pools take 2\u20135% and centralize power. DERO: your hashrate share of ~48,000 daily \u03a3-blocks pays you proportionally \u2014 solo, trustless, fair." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F4F8FC;strokeColor={TITLE_COLOR};strokeWidth=1.5;fontSize=13.5;fontColor={INK};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="40" y="1120" width="1830" height="96" as="geometry"/></mxCell>')
    return cells

EDGE_BLUE = "#0076BE"

def mining_p2_cells():
    cells = []
    add = cells.append
    add(f'<mxCell id="mq-t" value="MINING \u2014 KEY NUMBERS &amp; FAQ" style="text;html=1;align=center;fontSize=28;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="40" as="geometry"/></mxCell>')
    add(f'<mxCell id="mq-s" value="Print or share with a non-technical audience \u2014 the companion to \u2018The \u03a3-Block Loop\u2019." style="text;html=1;align=center;fontSize=13.5;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    add(f'<mxCell id="mq-h1" value="KEY NUMBERS" style="text;html=1;align=left;fontSize=17;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="60" y="115" width="400" height="26" as="geometry"/></mxCell>')
    add(f'<mxCell id="mq-h2" value="FREQUENTLY ASKED (PLAIN SPEAK)" style="text;html=1;align=left;fontSize=17;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="1000" y="115" width="600" height="26" as="geometry"/></mxCell>')
    y = 150
    for i, (num, desc) in enumerate(MINE_NUMBERS):
        add(f'<mxCell id="mq-n{i}" value="{val(f"<font color=&quot;{TITLE_COLOR}&quot;><b>{esc(num)}</b></font><br><font color=&quot;#66727E&quot;>{esc(desc)}</font>")}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F4F8FC;strokeColor={TITLE_COLOR};strokeWidth=1.5;fontSize=12;fontColor={INK};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="60" y="{y}" width="880" height="56" as="geometry"/></mxCell>')
        y += 64
    y2 = 150
    for i, (q, a) in enumerate(MINE_FAQ):
        add(f'<mxCell id="mq-f{i}" value="{val(f"<b>{esc(q)}</b><br><font color=&quot;#66727E&quot;>{esc(a)}</font>")}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C9D6E3;strokeWidth=1.5;fontSize=12;fontColor={INK};align=left;verticalAlign=middle;spacing=10;" vertex="1" parent="1"><mxGeometry x="1000" y="{y2}" width="860" height="70" as="geometry"/></mxCell>')
        y2 += 78
    return cells, max(y, y2)

# =========================================================== TELA ===========
TELA_STEPS = [
    dict(n=1, title="WRITE THE CODE", acc="blue",
         body=["Smart contract in DVM-BASIC (DeroScript) + the app front-end (HTML/CSS/JS).",
               "dSlate gives a visual editor; the VSCode extension adds syntax highlighting."],
         plain="You write normal-looking code \u2014 the backend is the whole network."),
    dict(n=2, title="DEPLOY (install_sc)", acc="teal",
         body=["Send the code to the chain via RPC (install_sc) and get back an SCID.",
               "The contract now runs on every node. One-time fee \u2014 no hosting bill."],
         plain="Your program moves into a building everyone owns and nobody controls."),
    dict(n=3, title="CONNECT THE WALLET (XSWD)", acc="purple",
         body=["The app talks to the user\u2019s wallet over a WebSocket bridge. The user grants",
               "per-request permissions: ask / accept_always / deny_always."],
         plain="The app can\u2019t touch your money unless you approve \u2014 per request."),
    dict(n=4, title="USERS SIGN IN & PAY (DeroAuth / DeroPay)", acc="green",
         body=["Users log in with their wallet \u2014 no passwords \u2014 and pay in DERO, all inside",
               "the wallet (Engram). Payments and identity stay private."],
         plain="Signing in = approving with your wallet."),
    dict(n=5, title="TELA SERVES IT", acc="teal",
         body=["App code and assets are stored on-chain and rendered locally in Engram",
               "(wallet + browser). No origin server to hack, block, or censor."],
         plain="Your shop is on everyone\u2019s land \u2014 and nobody owns it."),
    dict(n=6, title="ITERATE & GROW", acc="orange",
         body=["New versions are registered on-chain; state stays encrypted (private DVM state);",
               "Gnomon indexes chain data for analytics."],
         plain="Software that can\u2019t be yanked away \u2014 upgradeable, private, unstoppable."),
]

STACK = [
    ("DHEBP \u00b7 Layer 1", "encrypted ledger + consensus", "privacy, settlement, security \u2014 18 s blocks, PoW AstroBWTv3"),
    ("DVM", "smart-contract VM (DVM-BASIC)", "business logic runs on every node, state encrypted"),
    ("GravitonDB", "encrypted key/value state", "66 B per account \u00b7 merkle-proved \u00b7 prunable"),
    ("TELA", "on-chain decentralized web", "HTML/CSS/JS stored in contracts, served by the network"),
    ("XSWD", "app \u2194 wallet WebSocket bridge", "per-request permissions: ask / accept_always / deny_always"),
    ("Engram", "smart wallet + browser", "users\u2019 window into dApps, TELA sites, and identity"),
    ("DeroAuth / DeroPay", "sign in & pay", "passwordless login, wallet-native payments"),
    ("Name Service", "human-readable names", "wallet addresses you can actually read"),
    ("Gnomon", "chain indexer", "query chain data and smart-contract state locally"),
]

ECO = [
    ("CORE PROTOCOL & WALLETS", "green", [
        ("DEROFDN/derohe", "active", "community-maintained node \u2014 where development lives"),
        ("DEROFDN/Engram", "alpha", "smart wallet + TELA browser"),
        ("g45w (g45t345rt)", "active", "universal wallet with mobile UI"),
        ("dero-am/astrobwt-miner", "active", "community CPU miner (formerly astrominer)"),
    ]),
    ("DEV TOOLS", "blue", [
        ("dSlate (dMulti-c)", "active", "visual dApp builder & test environment"),
        ("Gnomon (civilware)", "alpha", "local chain indexer"),
        ("dvm-basic-vscode", "active", "DVM-BASIC syntax highlighting for VSCode"),
        ("dero-rpc-bridge", "active", "Chrome extension \u2014 safe wallet\u2194website bridge"),
        ("dero-community/xswd-api", "active", "JS/TS + Go clients for the XSWD protocol"),
        ("DERO-SC-Standards", "active", "community smart-contract standards"),
    ]),
    ("DAPPS & SITES", "orange", [
        ("Hologram (DHEBP)", "active", "explore the DERO decentralized web"),
        ("dReams (dReam-dApps)", "active", "suite of products & services on DERO"),
        ("cldex / dero_swap", "active", "decentralized exchange \u2014 DERO swaps"),
        ("dero_lotto", "active", "on-chain lottery (derolotto.com)"),
        ("Baccarat & Poker (SixofClubs)", "active", "card games on dreamtables.net"),
        ("deronfts.com", "developing", "NFT trading on DERO"),
        ("dero_private_islands", "developing", "privateislands.fund"),
        ("ORED asset manager", "active", "TELA site asset management & trading"),
        ("TELATOMIC Swaps", "active", "DERO \u2194 PulseChain atomic swaps"),
    ]),
    ("WEB3 PRIVACY STACK", "purple", [
        ("civilware/tela", "active", "TELA: Decentralized Web Standard"),
        ("DHEBP/DeroPay", "active", "complete payment stack for accepting DERO"),
        ("DHEBP/DeroAuth", "active", "log in to sites with your DERO wallet"),
        ("SovereignSearch", "active", "local discovery & navigation for TELA sites"),
        ("PureWolf extension", "active", "browser extension \u2194 local TELA services"),
    ]),
    ("NFTs / ASSETS / BRIDGES", "teal", [
        ("Artificer NFA standard", "active", "civilware\u2019s NFT/asset standard"),
        ("Dero Seals", "active", "deroseals.com collectibles"),
        ("Deroscapes / AZYPC", "active", "Azylem\u2019s on-chain art projects"),
        ("eth_erc20 bridge", "active", "derobridge.net \u2014 ETH \u2194 DERO"),
    ]),
]

def tela_p1_cells():
    cells = []
    add = cells.append
    add(f'<mxCell id="t-t1" value="FROM IDEA TO ON-CHAIN APP" style="text;html=1;align=center;fontSize=30;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="42" as="geometry"/></mxCell>')
    add(f'<mxCell id="t-t2" value="Build a dApp on DERO: DVM smart contract + TELA front-end + XSWD wallet bridge \u2014 no server, no middleman, full privacy." style="text;html=1;align=center;fontSize=14;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    # 6 steps in 2 rows of 3
    xs = [60, 700, 1340]
    ys = [150, 640]
    ws, hs = 540, 380
    for i, s in enumerate(TELA_STEPS):
        r, c = divmod(i, 3)
        x, y = xs[c], ys[r]
        b = wrap(" ".join(s["body"]), ws - 24, 11.0)
        p = wrap(s["plain"], ws - 24, 10.5)
        step_title = f"{s['n']} \u00b7 {s['title']}"
        add(f'<mxCell id="t-s{i}" value="{html_cell(step_title, ACCENTS[s["acc"]], b, p)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={ACCENTS[s["acc"]]};strokeWidth=2;verticalAlign=top;align=left;spacing=10;spacingTop=18;fontSize=11;fontColor={INK};" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{ws}" height="{hs}" as="geometry"/></mxCell>')
        add(f'<mxCell id="t-bd{i}" value="{s["n"]}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={ACCENTS[s["acc"]]};strokeColor=#FFFFFF;strokeWidth=2;fontColor=#FFFFFF;fontSize=15;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="{x-17}" y="{y-17}" width="34" height="34" as="geometry"/></mxCell>')
    def arrow(eid, p1, p2, label=None):
        add(f'<mxCell id="{eid}" value="{esc(label) if label else ""}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=classicThin;endFill=1;strokeColor={EDGE_BLUE};strokeWidth=2.5;fontSize=10.5;fontStyle=1;fontColor={EDGE_BLUE};labelBackgroundColor=#FFFFFF;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{p1[0]}" y="{p1[1]}" as="sourcePoint"/><mxPoint x="{p2[0]}" y="{p2[1]}" as="targetPoint"/></mxGeometry></mxCell>')
    arrow("t-a1", (600, 340), (700, 340))
    arrow("t-a2", (1240, 340), (1340, 340))
    arrow("t-a3", (1610, 530), (1610, 640), "deployed & live")
    arrow("t-a4", (330, 700), (330, 640))
    arrow("t-a5", (970, 700), (970, 640))
    arrow("t-a6", (1610, 1020), (1610, 1090), "users in the wallet")
    # bottom band
    add(f'<mxCell id="t-f1" value="THE RESULT" style="text;html=1;align=left;fontSize=15;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="40" y="1105" width="260" height="22" as="geometry"/></mxCell>')
    add(f'<mxCell id="t-f2" value="A web app that cannot be taken down, whose users log in with their wallet, whose data is encrypted \u2014 hosted by the network itself. That is TELA." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F4F8FC;strokeColor={TITLE_COLOR};strokeWidth=1.5;fontSize=13.5;fontColor={INK};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="40" y="1130" width="1830" height="96" as="geometry"/></mxCell>')
    return cells

def tela_p2_cells():
    cells = []
    add = cells.append
    add(f'<mxCell id="st-t" value="THE DAPP STACK" style="text;html=1;align=center;fontSize=28;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="40" as="geometry"/></mxCell>')
    add(f'<mxCell id="st-s" value="Each layer of the DERO stack \u2014 from the encrypted ledger up to the user\u2019s wallet." style="text;html=1;align=center;fontSize=13.5;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    add(f'<mxCell id="st-h1" value="LAYER" style="text;html=1;align=center;fontSize=13;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="60" y="110" width="320" height="30" as="geometry"/></mxCell>')
    add(f'<mxCell id="st-h2" value="WHAT IT IS" style="text;html=1;align=center;fontSize=13;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="400" y="110" width="620" height="30" as="geometry"/></mxCell>')
    add(f'<mxCell id="st-h3" value="WHAT IT DOES" style="text;html=1;align=center;fontSize=13;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="1040" y="110" width="820" height="30" as="geometry"/></mxCell>')
    y = 148
    for i, (name, what, does) in enumerate(STACK):
        add(f'<mxCell id="st-r{i}c0" value="{esc(name)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0F7FA;strokeColor={ACCENTS["teal"]};strokeWidth=1.5;fontSize=12;fontStyle=1;fontColor={ACCENTS["teal"]};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="60" y="{y}" width="320" height="64" as="geometry"/></mxCell>')
        add(f'<mxCell id="st-r{i}c1" value="{esc(what)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C9D6E3;strokeWidth=1.5;fontSize=12;fontColor={INK};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="400" y="{y}" width="620" height="64" as="geometry"/></mxCell>')
        add(f'<mxCell id="st-r{i}c2" value="{esc(does)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F4F8FC;strokeColor={TITLE_COLOR};strokeWidth=1.5;fontSize=12;fontColor={INK};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="1040" y="{y}" width="820" height="64" as="geometry"/></mxCell>')
        y += 72
    return cells, y + 40

def tela_p3_cells():
    cells = []
    add = cells.append
    add(f'<mxCell id="e-t1" value="THE DERO COMMUNITY ECOSYSTEM" style="text;html=1;align=center;fontSize=28;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="40" as="geometry"/></mxCell>')
    add(f'<mxCell id="e-t2" value="Indexed from the community\u2019s own project list (Discord) + GitHub \u2014 February 2026. Status chips: active \u00b7 developing \u00b7 alpha \u00b7 stale." style="text;html=1;align=center;fontSize=13.5;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    y = 130
    for gi, (gname, gcolor, items) in enumerate(ECO):
        add(f'<mxCell id="e-g{gi}" value="{esc(gname)}" style="text;html=1;align=left;fontSize=16;fontStyle=1;fontColor={ACCENTS[gcolor]};" vertex="1" parent="1"><mxGeometry x="60" y="{y}" width="700" height="26" as="geometry"/></mxCell>')
        y += 32
        for name, status, desc in items:
            sc = STATUS_COLORS.get(status, "#6E6F72")
            add(f'<mxCell id="e-i{gi}-{esc(name[:10])}" value="{val(f"<font color=&quot;{INK}&quot;><b>{esc(name)}</b></font> <font color=&quot;{sc}&quot;>[{esc(status)}]</font><br><font color=&quot;#66727E&quot;>{esc(desc)}</font>")}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C9D6E3;strokeWidth=1.5;fontSize=11;fontColor={INK};align=left;verticalAlign=middle;spacing=8;" vertex="1" parent="1"><mxGeometry x="60" y="{y}" width="580" height="58" as="geometry"/></mxCell>')
        y += 66
    H3 = y + 30
    return cells, H3

# ========================================================== SVG (p1s) ========
def svg_step(cells, s, x, y, w, h):
    b = wrap(" ".join(s["body"]), w - 24, 11.0)
    p = wrap(s["plain"], w - 24, 10.5)
    acc = ACCENTS[s["acc"]]
    cells.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="{acc}" stroke-width="2"/>')
    cells.append(f'<circle cx="{x}" cy="{y}" r="17" fill="{acc}" stroke="#FFFFFF" stroke-width="2.5"/>')
    cells.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF">{s["n"]}</text>')
    ty = y + 34
    cells.append(f'<text x="{x+12}" y="{ty}" font-size="12.5" font-weight="700" fill="{acc}">{svg_esc(s["title"])}</text>')
    ty += 21
    for ln in b:
        cells.append(f'<text x="{x+12}" y="{ty}" font-size="11" fill="{INK}">{svg_esc(ln)}</text>'); ty += 16
    ty += 6
    for ln in p:
        cells.append(f'<text x="{x+12}" y="{ty}" font-size="10.5" font-style="italic" fill="#66727E">\U0001F4A1 {svg_esc(ln)}</text>'); ty += 15
    return cells

def svg_mining_p1():
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<defs><marker id="amb" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{EDGE_BLUE}"/></marker></defs>')
    A(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')
    A(f'<text x="{W/2}" y="52" text-anchor="middle" font-size="30" font-weight="700" fill="{TITLE_COLOR}">HOW DERO MINING WORKS \u2014 THE \u03a3-BLOCK LOOP</text>')
    A(f'<text x="{W/2}" y="82" text-anchor="middle" font-size="14" fill="{GRAY}">The network is the pool: every CPU miner earns \u2014 no pools, no ASICs, no trust.  (\u03a3-block = Sigma block = mini-block)</text>')
    xs = [60, 520, 980, 300, 760]; ys = [150, 150, 150, 620, 620]
    for i, s in enumerate(MINING_STEPS):
        svg_step(out, s, xs[i], ys[i], 400, 330)
    # arrows
    A(f'<line x1="460" y1="315" x2="520" y2="315" stroke="{EDGE_BLUE}" stroke-width="2.5" marker-end="url(#amb)"/>')
    A(f'<line x1="920" y1="315" x2="980" y2="315" stroke="{EDGE_BLUE}" stroke-width="2.5" marker-end="url(#amb)"/>')
    A(f'<path d="M 1380 340 L 1380 600" stroke="{EDGE_BLUE}" stroke-width="2.5" marker-end="url(#amb)"/>')
    A(f'<text x="1392" y="475" font-size="10.5" font-weight="600" fill="{EDGE_BLUE}" stroke="#FFF" stroke-width="3" paint-order="stroke">the block settles</text>')
    A(f'<line x1="1380" y1="600" x2="500" y2="600" stroke="{EDGE_BLUE}" stroke-width="2.5" marker-end="url(#amb)"/>')
    A(f'<line x1="700" y1="785" x2="760" y2="785" stroke="{EDGE_BLUE}" stroke-width="2.5" marker-end="url(#amb)"/>')
    A(f'<path d="M 1160 640 L 1160 1090" stroke="{EDGE_BLUE}" stroke-width="2.5" marker-end="url(#amb)"/>')
    A(f'<text x="1172" y="870" font-size="10.5" font-weight="600" fill="{EDGE_BLUE}" stroke="#FFF" stroke-width="3" paint-order="stroke">reward + fees</text>')
    # numbers card
    A(f'<text x="1440" y="170" font-size="14" font-weight="700" fill="{TITLE_COLOR}">THE MATH OF \u03a3-BLOCKS</text>')
    ny = 182
    for num, desc in MINE_NUMBERS:
        A(f'<rect x="1440" y="{ny}" width="430" height="56" rx="8" fill="#F4F8FC" stroke="{TITLE_COLOR}" stroke-width="1.5"/>')
        A(f'<text x="1456" y="{ny+22}" font-size="12" font-weight="700" fill="{TITLE_COLOR}">{svg_esc(num)}</text>')
        A(f'<text x="1456" y="{ny+40}" font-size="10.5" fill="#66727E">{svg_esc(desc)}</text>')
        ny += 64
    A(f'<text x="40" y="1116" font-size="15" font-weight="700" fill="{TITLE_COLOR}">WHY IT MATTERS</text>')
    A(f'<rect x="40" y="1128" width="1830" height="96" rx="10" fill="#F4F8FC" stroke="{TITLE_COLOR}" stroke-width="1.5"/>')
    A(f'<text x="60" y="1162" font-size="13.5" fill="{INK}">Old mining: small miners earn nothing, pools take 2\u20135% and centralize power. DERO: your hashrate share of ~48,000 daily \u03a3-blocks</text>')
    A(f'<text x="60" y="1184" font-size="13.5" fill="{INK}">pays you proportionally \u2014 solo, trustless, fair.</text>')
    A('</svg>')
    return "\n".join(out)

def svg_tela_p1():
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<defs><marker id="atb" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{EDGE_BLUE}"/></marker></defs>')
    A(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')
    A(f'<text x="{W/2}" y="52" text-anchor="middle" font-size="30" font-weight="700" fill="{TITLE_COLOR}">FROM IDEA TO ON-CHAIN APP</text>')
    A(f'<text x="{W/2}" y="82" text-anchor="middle" font-size="14" fill="{GRAY}">Build a dApp on DERO: DVM smart contract + TELA front-end + XSWD wallet bridge \u2014 no server, no middleman, full privacy.</text>')
    xs = [60, 700, 1340]; ys = [150, 640]
    for i, s in enumerate(TELA_STEPS):
        r, c = divmod(i, 3)
        svg_step(out, s, xs[c], ys[r], 540, 380)
    A(f'<line x1="600" y1="340" x2="700" y2="340" stroke="{EDGE_BLUE}" stroke-width="2.5" marker-end="url(#atb)"/>')
    A(f'<line x1="1240" y1="340" x2="1340" y2="340" stroke="{EDGE_BLUE}" stroke-width="2.5" marker-end="url(#atb)"/>')
    A(f'<path d="M 1610 530 L 1610 640" stroke="{EDGE_BLUE}" stroke-width="2.5" marker-end="url(#atb)"/>')
    A(f'<text x="1622" y="590" font-size="10.5" font-weight="600" fill="{EDGE_BLUE}" stroke="#FFF" stroke-width="3" paint-order="stroke">deployed &amp; live</text>')
    A(f'<path d="M 330 700 L 330 640" stroke="{EDGE_BLUE}" stroke-width="2.5" marker-end="url(#atb)"/>')
    A(f'<path d="M 970 700 L 970 640" stroke="{EDGE_BLUE}" stroke-width="2.5" marker-end="url(#atb)"/>')
    A(f'<path d="M 1610 1020 L 1610 1090" stroke="{EDGE_BLUE}" stroke-width="2.5" marker-end="url(#atb)"/>')
    A(f'<text x="1622" y="1060" font-size="10.5" font-weight="600" fill="{EDGE_BLUE}" stroke="#FFF" stroke-width="3" paint-order="stroke">users in the wallet</text>')
    A(f'<text x="40" y="1126" font-size="15" font-weight="700" fill="{TITLE_COLOR}">THE RESULT</text>')
    A(f'<rect x="40" y="1138" width="1830" height="96" rx="10" fill="#F4F8FC" stroke="{TITLE_COLOR}" stroke-width="1.5"/>')
    A(f'<text x="60" y="1172" font-size="13.5" fill="{INK}">A web app that cannot be taken down, whose users log in with their wallet, whose data is encrypted \u2014 hosted by the network</text>')
    A(f'<text x="60" y="1194" font-size="13.5" fill="{INK}">itself. That is TELA.</text>')
    A('</svg>')
    return "\n".join(out)

def svg_tela_p3():
    out = []
    A = out.append
    H3 = 150 + sum((1 + len(items)) * 66 for _, _, items in ECO) + 30
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="{H3}" viewBox="0 0 1920 {H3}" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<rect x="0" y="0" width="1920" height="{H3}" fill="#FFFFFF"/>')
    A(f'<text x="960" y="52" text-anchor="middle" font-size="28" font-weight="700" fill="{TITLE_COLOR}">THE DERO COMMUNITY ECOSYSTEM</text>')
    A(f'<text x="960" y="82" text-anchor="middle" font-size="13.5" fill="{GRAY}">Indexed from the community\u2019s own project list (Discord) + GitHub \u2014 February 2026. Status chips: active \u00b7 developing \u00b7 alpha \u00b7 stale.</text>')
    y = 130
    for gname, gcolor, items in ECO:
        A(f'<text x="60" y="{y}" font-size="16" font-weight="700" fill="{ACCENTS[gcolor]}">{svg_esc(gname)}</text>')
        y += 32
        for name, status, desc in items:
            sc = STATUS_COLORS.get(status, "#6E6F72")
            A(f'<rect x="60" y="{y}" width="580" height="58" rx="8" fill="#FFFFFF" stroke="#C9D6E3" stroke-width="1.5"/>')
            A(f'<text x="74" y="{y+22}" font-size="11.5" font-weight="700" fill="{INK}">{svg_esc(name)}</text>')
            A(f'<text x="{74 + 9.5*len(name) + 6}" y="{y+22}" font-size="10" font-weight="700" fill="{sc}">[{svg_esc(status)}]</text>')
            A(f'<text x="74" y="{y+41}" font-size="10.5" fill="#66727E">{svg_esc(desc)}</text>')
            y += 66
    A('</svg>')
    return "\n".join(out), H3

# ============================================================ main ==========
def build_drawio(diagrams):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    body = ""
    for did, name, cells in diagrams:
        body += f'  <diagram id="{did}" name="{esc(name)}">\n{inject_draft(cells)}\n  </diagram>\n'
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device">\n'
            + body + '</mxfile>\n')

def wrap_graph(cells, w=W, h=H):
    return f'<mxGraphModel dx="1400" dy="850" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{w}" pageHeight="{h}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel>"

if __name__ == "__main__":
    import os
    d = os.path.dirname(os.path.abspath(__file__))
    mp2, mp2h = mining_p2_cells()
    tp2, tp2h = tela_p2_cells()
    tp3, tp3h = tela_p3_cells()
    mining_diagrams = [
        ("mining", "The Sigma-Block Loop", wrap_graph(mining_p1_cells())),
        ("mining-faq", "Mining Key Numbers & FAQ", wrap_graph(mp2, h=max(mp2h, 620) + 40)),
    ]
    tela_diagrams = [
        ("tela", "From Idea to On-Chain App", wrap_graph(tela_p1_cells())),
        ("stack", "The dApp Stack", wrap_graph(tp2, h=max(tp2h, 720) + 40)),
        ("eco", "The Community Ecosystem", wrap_graph(tp3, h=tp3h)),
    ]
    with open(os.path.join(d, "DERO.MINING.drawio"), "w", encoding="utf-8") as f:
        f.write(build_drawio(mining_diagrams))
    with open(os.path.join(d, "DERO.TELA.drawio"), "w", encoding="utf-8") as f:
        f.write(build_drawio(tela_diagrams))
    for name, fn in [("preview_mining1.svg", svg_mining_p1), ("preview_tela1.svg", svg_tela_p1)]:
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(inject_draft_svg(fn()))
        with open(os.path.join(d, name.replace(".svg", ".html")), "w", encoding="utf-8") as f:
            f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;}}</style></head><body>{inject_draft_svg(fn())}</body></html>')
    svg3, h3 = svg_tela_p3()
    with open(os.path.join(d, "preview_tela3.svg"), "w", encoding="utf-8") as f:
        f.write(inject_draft_svg(svg3))
    with open(os.path.join(d, "preview_tela3.html"), "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;}}</style></head><body>{inject_draft_svg(svg3)}</body></html>')
    print("written OK")
