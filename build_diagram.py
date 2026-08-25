#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DERO Process Diagram generator (new template).
One data model -> draw.io XML (theme-switchable) + previews via render_drawio_svg.
Page 1: The Journey of One DERO Transaction (user -> DLT consensus -> back).
Page 2: Plain-language translation tables.
"""
import xml.sax.saxutils as sax
import datetime, html, os, sys
import dero_style as S

# ------------------------------------------------------- accent per lane ----
# map lane keys -> dero_style accent names
LANE_ACC = {
    "user":    "amber",
    "wallet":  "green",
    "node":    "blue",
    "network": "purple",
    "miners":  "orange",
    "ledger":  "teal",
    "confirm": "green",
}
EDGE_BLUE = "#0076BE"
EDGE_GREEN = S.TH["green"][0]
TITLE_COLOR = S.TH["brand"]
INK = S.TH["ink"]
GRAY = S.TH["muted"]

# ------------------------------------------------------------- canvas -------
W, H = 1920, 1400
LANE_X0, LANE_X1 = 20, 1560      # lane rect span
LABEL_COL = 235                   # lane label column right edge
CONTENT_X0 = 250                  # steps start here

LANES = [
    # key, label, sub, y, h
    ("user",    "YOU",            "the human",                   130, 130),
    ("wallet",  "YOUR WALLET",    "the app on your device",      270, 200),
    ("node",    "YOUR NODE",      "your computer, on the network",480, 140),
    ("network", "THE NETWORK",    "every node worldwide",        630, 160),
    ("miners",  "MINERS",         "CPU puzzle solvers",          800, 180),
    ("ledger",  "THE LEDGER",     "the shared encrypted record (DLT)", 990, 170),
]
LANE_Y = {k: (y, y + h) for k, _, _, y, h in LANES}

# ---------------------------------------------------------------- steps -----
STEPS = [
    dict(num=1, lane="user",   x=CONTENT_X0, w=520, title="YOU want to send DERO (or use a dApp)",
         body="You open your wallet \u2014 CLI, GUI, web or mobile \u2014 enter an amount, or open a decentralized app built on DERO.",
         plain="You tap \u2018Send\u2019, like a banking app \u2014 but there\u2019s no bank, and nobody can see the amount."),
    dict(num=2, lane="wallet", x=CONTENT_X0, w=600, title="WALLET builds a sealed envelope (\u224825 ms)",
         body="Picks a ring of 8 accounts (yours + 7 decoys) \u00b7 hides the amount with homomorphic encryption + a Pedersen commitment \u00b7 attaches six bound zero-knowledge proofs (ring, range, balance\u2026) \u00b7 optional 28-byte message.",
         plain="The app wraps your payment in unbreakable math \u2014 identity and amount sealed, even from the network."),
    dict(num=3, lane="wallet", x=880, w=380, title="WALLET signs with your private key",
         body="Your key authorizes the tx on your device and never leaves it. Nobody can tell which of the 8 ring accounts is really yours.",
         plain="Only your key can approve a payment. It never leaves your phone or PC."),
    dict(num=4, lane="node", x=CONTENT_X0, w=430, title="YOUR NODE receives it (RPC)",
         body="The wallet hands the tx to your daemon over local RPC. Quick checks: format, fee, proofs.",
         plain="Your node = the post office that sends your envelope on its way."),
    dict(num=5, lane="node", x=700, w=430, title="YOUR NODE adds it to the mempool",
         body="The pool of unconfirmed transactions, shared with every peer.",
         plain="The waiting room. Your tx waits for a miner to pick it up."),
    dict(num=6, lane="network", x=CONTENT_X0, w=560, title="NETWORK broadcasts it (TLS P2P)",
         body="Nodes gossip the tx over TLS-encrypted connections (P2P port 10101). Within seconds, every node has a copy.",
         plain="A secret whisper spreads through the crowd \u2014 everyone hears it, the message stays sealed."),
    dict(num=7, lane="network", x=830, w=560, title="NETWORK verifies the envelope",
         body="Each node checks signature, zero-knowledge proofs and balance \u2014 computed on the ENCRYPTED data (homomorphic math) \u2014 plus the double-spend check. \u224825 ms.",
         plain="Every node checks your sealed envelope without ever opening it. Anything wrong \u2192 rejected."),
    dict(num=8, lane="miners", x=CONTENT_X0, w=380, title="MINERS race: AstroBWTv3 PoW",
         body="CPU-only, memory-hard puzzle. ASIC/GPU-resistant \u2192 any PC can mine. Difficulty re-targets every block.",
         plain="A CPU lottery. The winner writes the next page of the notebook \u2014 and earns DERO."),
    dict(num=9, lane="miners", x=650, w=380, title="MINERS pack the block & earn rewards",
         body="Verified txs are packed into a block \u2014 9 fast mini-blocks + 1 final (10 per block, one every ~2 sec), so up to 10 miners share each reward.",
         plain="Your envelope is now on the winning page \u2014 part of the official record."),
    dict(num=10, lane="miners", x=1060, w=460, title="Block spreads & every node re-checks",
         body="Erasure-coded into 48 chunks; any 16 rebuild the whole block. All nodes re-validate before accepting. Consensus: one agreed chain.",
         plain="The page is shredded into confetti \u2014 anyone with 16 pieces can rebuild and re-check the math."),
    dict(num=11, lane="ledger", x=CONTENT_X0, w=560, title="LEDGER updates (still encrypted)",
         body="Balances settle by homomorphic addition/subtraction on ciphertext \u2014 never decrypted, ever. Just 66 bytes per account. Smart contracts (DVM \u00b7 DeroScript) update encrypted state too.",
         plain="The notebook is updated. Your balance changed \u2014 but the number is still invisible to everyone but you."),
    dict(num=12, lane="ledger", x=830, w=430, title="The record becomes permanent",
         body="Blocks are chained and merkle-proved. Supply stays auditable (hard cap \u224820.89M DERO). History can be pruned to a few GB. The past cannot be rewritten.",
         plain="What\u2019s written stays written. No erasers on this notebook."),
    dict(num=13, lane="confirm", x=1600, w=290, y=300, title="CONFIRMED in ~1 minute",
         body="After a few 18-second blocks, your tx is confirmed. Your wallet reads the encrypted balance and decrypts it locally with your key.",
         plain="The network agrees \u2014 your app shows the new balance. Only your app can read it."),
    dict(num=14, lane="confirm", x=1600, w=290, y=480, title="You get a private receipt",
         body="Prove \u2018I sent exactly X\u2019 without revealing your identity or balance. dApps see their state update too.",
         plain="A receipt that shows the total \u2014 but not your name. Privacy AND proof."),
]

# ------------------------------------------------------------- wrapping -----
def wrap(text, width_px, font_px, factor=0.55):
    """Greedy word wrap approximating average char width."""
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

def layout(step):
    """Compute step box y + height from content. Returns dict with geometry."""
    lk = step["lane"]
    inner = step["w"] - 24
    t_lines = [step["title"]]
    b_lines = wrap(step["body"], inner, 10.5)
    p_lines = wrap(step["plain"], inner, 10.0)
    h = 26 + 17 + len(b_lines) * 15 + 6 + len(p_lines) * 14 + 12
    if lk in LANE_Y:
        y0, y1 = LANE_Y[lk]
        y = y0 + 14
        if y + h > y1 - 6:
            h = y1 - 6 - y          # clamp to lane
    else:
        y = step.get("y", 300)      # fixed column (return path)
    return {**step, "y": y, "h": h, "t": t_lines, "b": b_lines, "p": p_lines}

BOXES = [layout(s) for s in STEPS]
B = {b["num"]: b for b in BOXES}

def box_center(b, side):
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    return {"top": (x + w / 2, y), "bottom": (x + w / 2, y + h),
            "left": (x, y + h / 2), "right": (x + w, y + h / 2)}[side]

# --------------------------------------------------------------- edges ------
def elbow(p1, p2):
    """Orthogonal route between two points: returns polyline points."""
    (x1, y1), (x2, y2) = p1, p2
    if abs(x2 - x1) < 1:
        return [p1, p2]
    if abs(y2 - y1) < 1:
        return [p1, p2]
    mid = (x1 + x2) / 2
    if y2 > y1:                      # downward flow: elbow up high then across
        return [p1, (x1, y1 + 18), (mid, y1 + 18), (mid, y2 - 12), (x2, y2 - 12), p2]
    return [p1, (x1, y1 - 18), (mid, y1 - 18), (mid, y2 + 12), (x2, y2 + 12), p2]

def h_edge(a, b):
    return [box_center(a, "right"), box_center(b, "left")]

def v_edge(a, b):
    return elbow(box_center(a, "bottom"), box_center(b, "top"))

EDGES = [
    ("e1",  v_edge(B[1], B[2]),  EDGE_BLUE, 2, "sends the envelope",        (505, 252)),
    ("e2",  h_edge(B[2], B[3]),  EDGE_BLUE, 2, None, None),
    ("e3",  v_edge(B[3], B[4]),  EDGE_BLUE, 2, "to your node",              (1085, 470)),
    ("e4",  h_edge(B[4], B[5]),  EDGE_BLUE, 2, None, None),
    ("e5",  v_edge(B[5], B[6]),  EDGE_BLUE, 2, "broadcast to the network",  (940, 620)),
    ("e6",  h_edge(B[6], B[7]),  EDGE_BLUE, 2, None, None),
    ("e7",  v_edge(B[7], B[8]),  EDGE_BLUE, 2, "verified txs enter blocks", (1135, 782)),
    ("e8",  h_edge(B[8], B[9]),  EDGE_BLUE, 2, None, None),
    ("e9",  h_edge(B[9], B[10]), EDGE_BLUE, 2, None, None),
    ("e10", v_edge(B[10], B[11]), EDGE_BLUE, 2, "block accepted by all",    (1315, 960)),
    ("e11", h_edge(B[11], B[12]), EDGE_BLUE, 2, None, None),
]
# return path
ret1 = [box_center(B[12], "right"), (1830, box_center(B[12], "right")[1]), (1830, B[13]["y"])]
ret2 = [box_center(B[13], "bottom"), box_center(B[14], "top")]
ret3_start = box_center(B[14], "left")
ret3 = [ret3_start, (1450, ret3_start[1]), (1450, 185)]
EDGES += [
    ("r1", ret1, EDGE_GREEN, 3, None, None),
    ("r2", ret2, EDGE_GREEN, 3, None, None),
    ("r3", ret3, EDGE_GREEN, 3, "back to you \u2713", (1462, 235)),
]

def acc(key):
    return S.accent(LANE_ACC[key])[0]

# ============================================================ draw.io XML ====
def esc(s):
    return sax.escape(s, {"'": "&apos;", '"': "&quot;"})

def val(s):
    """Final escape for drawio value attributes: tags as &lt;...&gt; (valid XML,
    rendered as HTML by drawio when html=1). Entities are left untouched."""
    return s.replace("<", "&lt;").replace(">", "&gt;")

def step_value(b):
    c = acc(b["lane"])
    parts = [f'<font color=&quot;{c}&quot;><b>{b["num"]} \u00b7 {esc(b["title"])}</b></font>']
    for ln in b["b"]:
        parts.append(esc(ln))
    parts.append("")
    for ln in b["p"]:
        parts.append(f'<font color=&quot;{S.TH["muted"]}&quot;><i>\U0001F4A1 {esc(ln)}</i></font>')
    return val("<br>".join(parts))

def drawio_step_style(b):
    return (f"rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH['panel']};gradientColor={S.TH['panel2']};"
            f"gradientDirection=south;strokeColor={acc(b['lane'])};"
            f"strokeWidth=2;verticalAlign=top;align=left;spacing=10;spacingTop=18;"
            f"fontSize=10.5;fontColor={S.TH['ink']};shadow=1;")

def build_page1():
    cells = []
    cid = [0]
    def add(cell_xml):
        cid[0] += 1
        cells.append(cell_xml)

    # title banner
    t1_txt = "THE JOURNEY OF ONE DERO TRANSACTION"
    t2_txt = "From your wallet \u2192 through the network \u2192 into the encrypted ledger (DLT) \u2192 confirmation back to you.  Follow the numbers 1 \u2192 14 \u00b7 \U0001F4A1 lines = plain talk \u00b7 green arrows = confirmation back to you."
    t3_txt = "DERO \u00b7 DHEBP (Stargate) \u00b7 Layer 1"
    add(f'<mxCell id="t1" value="{esc(t1_txt)}" style="text;html=1;align=center;fontSize=30;fontStyle=1;fontColor={S.TH["ink"]};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="42" as="geometry"/></mxCell>')
    add(f'<mxCell id="t2" value="{esc(t2_txt)}" style="text;html=1;align=center;fontSize=14;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    add(f'<mxCell id="t3" value="{esc(t3_txt)}" style="rounded=1;html=1;fillColor={S.TH["panel"]};strokeColor={S.accent("brand")[0]};fontColor={S.accent("brand")[0]};fontSize=11;fontStyle=1;align=center;" vertex="1" parent="1"><mxGeometry x="1600" y="66" width="290" height="30" as="geometry"/></mxCell>')

    # lanes
    for k, label, sub, y, h in LANES:
        add(f'<mxCell id="lane-{k}" value="" style="rounded=0;html=1;fillColor={S.TH["panel2"]};strokeColor={S.TH["border"]};strokeWidth=1;opacity=70;verticalAlign=top;pointerEvents=0;" vertex="1" parent="1"><mxGeometry x="{LANE_X0}" y="{y}" width="{LANE_X1-LANE_X0}" height="{h}" as="geometry"/></mxCell>')
        add(f'<mxCell id="lane-t-{k}" value="\U0001F464 {esc(label)}" style="text;html=1;align=left;fontSize=19;fontStyle=1;fontColor={acc(k)};" vertex="1" parent="1"><mxGeometry x="28" y="{y+14}" width="200" height="26" as="geometry"/></mxCell>')
        add(f'<mxCell id="lane-s-{k}" value="{esc(sub)}" style="text;html=1;align=left;fontSize=11;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="28" y="{y+44}" width="200" height="18" as="geometry"/></mxCell>')

    # step boxes + badges
    for b in BOXES:
        add(f'<mxCell id="s{b["num"]}" value="{step_value(b)}" style="{drawio_step_style(b)}" vertex="1" parent="1"><mxGeometry x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" as="geometry"/></mxCell>')
        add(f'<mxCell id="bd{b["num"]}" value="{b["num"]}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={acc(b["lane"])};strokeColor=#0B1220;strokeWidth=2;fontColor=#FFFFFF;fontSize=14;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="{b["x"]-17}" y="{b["y"]-17}" width="34" height="34" as="geometry"/></mxCell>')

    # edges
    for eid, pts, color, width, label, labpos in EDGES:
        src, tgt = pts[0], pts[-1]
        mid = pts[len(pts)//2]
        way = "".join(f'<mxPoint x="{p[0]}" y="{p[1]}"/>' for p in pts[1:-1])
        style = (f'edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=classicThin;endFill=1;'
                 f'strokeColor={color};strokeWidth={width};fontSize=10;')
        lbl = ""
        if label:
            lbl = (f'<mxCell id="{eid}-l" value="{esc(label)}" style="edgeLabel;html=1;align=center;verticalAlign=middle;'
                   f'labelBackgroundColor={S.TH["panel"]};fontSize=10.5;fontStyle=1;fontColor={color};" vertex="1" connectable="0">'
                   f'<mxGeometry x="0.5" y="0.5" relative="1" as="geometry"><mxPoint x="{labpos[0]-mid[0]}" y="{labpos[1]-mid[1]}" as="offset"/></mxGeometry></mxCell>')
        add(f'<mxCell id="{eid}" style="{style}" edge="1" parent="1">'
            f'<mxGeometry relative="1" as="geometry">'
            f'<mxPoint x="{src[0]}" y="{src[1]}" as="sourcePoint"/><mxPoint x="{tgt[0]}" y="{tgt[1]}" as="targetPoint"/>'
            f'<Array as="points">{way}</Array></mxGeometry>{lbl}</mxCell>')

    # return-path big label box
    r1_label = val("\u2713 CONFIRMED (\u22481 MIN)<br>your wallet decrypts<br>your new balance \u2014" + f'<font color=&quot;{S.accent("green")[0]}&quot;><b>only you can read it</b></font>')
    add(f'<mxCell id="r1-lb" value="{r1_label}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("green")[0]};strokeWidth=2;fontSize=11;fontColor={S.TH["ink"]};align=center;shadow=1;" vertex="1" parent="1"><mxGeometry x="1600" y="640" width="228" height="92" as="geometry"/></mxCell>')

    # footer banner
    f1_txt = "THE WHOLE POINT"
    foot_txt = "Your money never leaves your control. The network never sees your amount, your identity, or your balance \u2014 it only agrees, in math, that everything adds up. That is how DERO replaces banks, clouds and databases with one shared, private, tamper-proof notebook."
    add(f'<mxCell id="f1" value="{esc(f1_txt)}" style="text;html=1;align=left;fontSize=15;fontStyle=1;fontColor={S.accent("brand")[0]};" vertex="1" parent="1"><mxGeometry x="40" y="1185" width="300" height="22" as="geometry"/></mxCell>')
    add(f'<mxCell id="f2" value="{esc(foot_txt)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("brand")[0]};strokeWidth=1.5;shadow=1;fontSize=13.5;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="40" y="1210" width="1500" height="96" as="geometry"/></mxCell>')

    # legend
    lg_txt = "LEGEND"
    add(f'<mxCell id="lg" value="{esc(lg_txt)}" style="text;html=1;align=left;fontSize=14;fontStyle=1;fontColor={S.accent("brand")[0]};" vertex="1" parent="1"><mxGeometry x="1600" y="1185" width="200" height="22" as="geometry"/></mxCell>')
    lg_rows = [
        ("user",    "\U0001F464 YOU \u2014 the human"),
        ("wallet",  "\U0001F4BC YOUR WALLET \u2014 the app"),
        ("node",    "\U0001F4E1 YOUR NODE \u2014 your daemon"),
        ("network", "\U0001F310 THE NETWORK \u2014 every node"),
        ("miners",  "\u26CF\uFE0F MINERS \u2014 PoW consensus"),
        ("ledger",  "\U0001F4D2 THE LEDGER \u2014 shared DLT"),
        ("confirm", "\u21A9 Confirmation back to you"),
        ("edge",    "\u2193 The transaction\u2019s journey"),
    ]
    ly = 1215
    for key, txt in lg_rows:
        if key == "edge":
            add(f'<mxCell id="lg-chip-edge" value="" style="rounded=1;html=1;fillColor={S.TH["panel"]};strokeColor={EDGE_BLUE};strokeWidth=2;" vertex="1" parent="1"><mxGeometry x="1610" y="{ly+1}" width="22" height="14" as="geometry"/></mxCell>')
            add(f'<mxCell id="lg-t-edge" value="&#8595; {esc(txt)}" style="text;html=1;align=left;fontSize=10.5;fontColor={S.TH["ink"]};" vertex="1" parent="1"><mxGeometry x="1640" y="{ly-2}" width="240" height="18" as="geometry"/></mxCell>')
        else:
            add(f'<mxCell id="lg-chip-{key}" value="" style="rounded=1;html=1;fillColor={acc(key)};strokeColor=none;" vertex="1" parent="1"><mxGeometry x="1610" y="{ly+1}" width="22" height="14" as="geometry"/></mxCell>')
            add(f'<mxCell id="lg-t-{key}" value="{esc(txt)}" style="text;html=1;align=left;fontSize=10.5;fontColor={S.TH["ink"]};" vertex="1" parent="1"><mxGeometry x="1640" y="{ly-2}" width="240" height="18" as="geometry"/></mxCell>')
        ly += 24

    return S.d_graph(W, H, cells)

# ------------------------------------------------------- page 2 (drawio) ----
TECH_PLAIN = [
    ("Homomorphic encryption", "Math you can add and subtract while it\u2019s still locked in a safe \u2014 balances stay secret."),
    ("Ring signatures (ring of 8)", "You stand in a crowd of 8 people. Nobody can tell which one is you."),
    ("Zero-knowledge proofs (Bulletproofs)", "\u2018Trust me, the math is right\u2019 \u2014 proven without revealing any secret."),
    ("Mempool", "The waiting room for payments that haven\u2019t been written into the ledger yet."),
    ("AstroBWTv3 proof-of-work", "A CPU puzzle lottery that keeps the network honest \u2014 any PC can play."),
    ("Mini-blocks (10 per block)", "One notebook page has 10 lines \u2014 up to 10 miners get paid per page."),
    ("Erasure-coded blocks (48 \u2192 16)", "The page is torn into 48 pieces of confetti; any 16 rebuild it. Faster and tougher."),
    ("DVM + DeroScript", "Programs (smart contracts) that run on every node and update the encrypted notebook together."),
    ("66 bytes per account", "Your whole account state is smaller than this sentence."),
    ("TLS-encrypted P2P network", "Nodes talk to each other over a secure, wiretap-proof line."),
    ("28-byte data payload", "A tiny note glued to a payment \u2014 a message that travels with it."),
    ("18 s blocks / ~1 min confirmation", "A new page every 18 seconds; your payment is officially settled in about a minute."),
]
KEY_NUMBERS = [
    ("18 s", "average block time"),
    ("10 (9+1)", "mini-blocks per block (\u22481 every 2 s)"),
    ("8", "default ring size (anonymity set)"),
    ("~2.5 KB", "transaction size (ring 8)"),
    ("< 25 ms", "generate / verify a transaction"),
    ("66 B", "on-chain state per account"),
    ("28 B", "max data payload per transaction"),
    ("48 \u2192 16", "erasure chunks \u2192 needed to rebuild"),
    ("\u224820.89 M", "hard cap \u00b7 halving every 4 years"),
    ("CPU-only", "AstroBWTv3 \u2014 ASIC/GPU resistant"),
]

def build_page2():
    cells = []
    cid = [0]
    def add(x):
        cid[0] += 1
        cells.append(x)
    p2t_txt = "THE SAME JOURNEY IN PLAIN WORDS"
    p2s_txt = "Print or share this page with a non-technical audience \u2014 the companion to the \u2018Journey of One Transaction\u2019 diagram."
    add(f'<mxCell id="p2t" value="{esc(p2t_txt)}" style="text;html=1;align=center;fontSize=28;fontStyle=1;fontColor={S.TH["ink"]};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="40" as="geometry"/></mxCell>')
    add(f'<mxCell id="p2s" value="{esc(p2s_txt)}" style="text;html=1;align=center;fontSize=13.5;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    h1_txt = "TECH SPEAK \u2192 PLAIN SPEAK"
    h2_txt = "KEY NUMBERS"
    add(f'<mxCell id="p2h1" value="{esc(h1_txt)}" style="text;html=1;align=left;fontSize=17;fontStyle=1;fontColor={S.accent("brand")[0]};" vertex="1" parent="1"><mxGeometry x="60" y="115" width="500" height="26" as="geometry"/></mxCell>')
    add(f'<mxCell id="p2h2" value="{esc(h2_txt)}" style="text;html=1;align=left;fontSize=17;fontStyle=1;fontColor={S.accent("brand")[0]};" vertex="1" parent="1"><mxGeometry x="1180" y="115" width="500" height="26" as="geometry"/></mxCell>')
    y = 150
    for i, (tech, plain) in enumerate(TECH_PLAIN):
        tp_html = f"<b>{esc(tech)}</b><br><font color=&quot;{S.TH['muted']}&quot;>{esc(plain)}</font>"
        add(f'<mxCell id="tp{i}" value="{val(tp_html)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.TH["border"]};strokeWidth=1.5;shadow=1;fontSize=12;fontColor={S.TH["ink"]};align=left;verticalAlign=middle;spacing=10;" vertex="1" parent="1"><mxGeometry x="60" y="{y}" width="1080" height="52" as="geometry"/></mxCell>')
        y += 60
    y2 = 150
    for i, (num, desc) in enumerate(KEY_NUMBERS):
        kn_html = f"<font color=&quot;{S.accent('brand')[0]}&quot;><b>{esc(num)}</b></font><br><font color=&quot;{S.TH['muted']}&quot;>{esc(desc)}</font>"
        add(f'<mxCell id="kn{i}" value="{val(kn_html)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("brand")[0]};strokeWidth=1.5;shadow=1;fontSize=12;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="1180" y="{y2}" width="660" height="52" as="geometry"/></mxCell>')
        y2 += 60
    p2f_txt = "DHEBP = DERO Homomorphic Encryption Blockchain Protocol \u00b7 codename Stargate \u00b7 collaborative repo: github.com/liqdmetal/DERO.STARGATE.DIAGRAMS"
    add(f'<mxCell id="p2f" value="{esc(p2f_txt)}" style="text;html=1;align=center;fontSize=11;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="{max(y, y2) + 30}" width="1880" height="20" as="geometry"/></mxCell>')
    H2 = max(y, y2) + 80
    return S.d_graph(1920, H2, cells)

def build_drawio():
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device" background="{S.TH["bg0"]}">\n'
        f'  <diagram id="journey" name="The Journey of One Transaction">\n{S.inject_draft(build_page1())}\n  </diagram>\n'
        f'  <diagram id="translation" name="Plain-Language Translation">\n{S.inject_draft(build_page2())}\n  </diagram>\n'
        '</mxfile>\n'
    )

# ================================================================ main ======
if __name__ == "__main__":
    theme = sys.argv[1] if len(sys.argv) > 1 else "light"
    S.set_theme(theme)
    d = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(d, "DERO.PROCESS.COMPLETE.drawio"), "w", encoding="utf-8") as f:
        f.write(build_drawio())
    print(f"written OK (theme={theme})")
