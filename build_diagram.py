#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DERO Process Diagram generator.
One data model -> both draw.io XML and SVG preview.
Page 1: The Journey of One DERO Transaction (user -> DLT consensus -> back).
Page 2 (drawio only): Plain-language translation tables.
"""
import xml.sax.saxutils as sax
import datetime, html

# ---------------------------------------------------------------- palette ---
ACCENT = {
    "user":    "#F9A825",  # amber
    "wallet":  "#43A047",  # green
    "node":    "#1E88E5",  # blue
    "network": "#8E24AA",  # purple
    "miners":  "#FB8C00",  # orange
    "ledger":  "#00838F",  # teal
    "confirm": "#2E7D32",  # dark green
}
TINT = {
    "user":    "#FFF8E1",
    "wallet":  "#E8F5E9",
    "node":    "#E3F2FD",
    "network": "#F3E5F5",
    "miners":  "#FFF3E0",
    "ledger":  "#E0F7FA",
}
EDGE_BLUE = "#0076BE"
TITLE_COLOR = "#4277BB"
INK = "#22303C"
GRAY = "#5A6B7A"

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
    ("r1", ret1, "#2E7D32", 3, None, None),
    ("r2", ret2, "#2E7D32", 3, None, None),
    ("r3", ret3, "#2E7D32", 3, "back to you \u2713", (1462, 235)),
]

# ============================================================ draw.io XML ====
def esc(s):
    return sax.escape(s, {"'": "&apos;"})

def val(s):
    """Final escape for drawio value attributes: tags as &lt;...&gt; (valid XML,
    rendered as HTML by drawio when html=1). Entities are left untouched."""
    return s.replace("<", "&lt;").replace(">", "&gt;")

def step_value(b):
    acc = ACCENT[b["lane"]]
    parts = [f'<font color=&quot;{acc}&quot;><b>{b["num"]} \u00b7 {esc(b["title"])}</b></font>']
    for ln in b["b"]:
        parts.append(esc(ln))
    parts.append("")
    for ln in b["p"]:
        parts.append(f'<font color=&quot;#66727E&quot;><i>\U0001F4A1 {esc(ln)}</i></font>')
    return val("<br>".join(parts))

def drawio_step_style(b):
    return ("rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=%s;"
            "strokeWidth=2;verticalAlign=top;align=left;spacing=10;spacingTop=18;"
            "fontSize=10.5;fontColor=%s;shadow=0;" % (ACCENT[b["lane"]], INK))

def build_page1():
    cells = []
    cid = [0]
    def add(cell_xml):
        cid[0] += 1
        cells.append(cell_xml)

    # title banner
    add(f'<mxCell id="t1" value="THE JOURNEY OF ONE DERO TRANSACTION" style="text;html=1;align=center;fontSize=30;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="42" as="geometry"/></mxCell>')
    add(f'<mxCell id="t2" value="From your wallet \u2192 through the network \u2192 into the encrypted ledger (DLT) \u2192 confirmation back to you.  Follow the numbers 1 \u2192 14." style="text;html=1;align=center;fontSize=14;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    add(f'<mxCell id="t3" value="DERO \u00b7 DHEBP (Stargate) \u00b7 Layer 1" style="rounded=1;html=1;fillColor=#EAF2FB;strokeColor={TITLE_COLOR};fontColor={TITLE_COLOR};fontSize=11;fontStyle=1;align=center;" vertex="1" parent="1"><mxGeometry x="1600" y="66" width="290" height="30" as="geometry"/></mxCell>')

    # lanes
    for k, label, sub, y, h in LANES:
        add(f'<mxCell id="lane-{k}" value="" style="rounded=0;html=1;fillColor={TINT[k]};strokeColor=#D8E2EC;strokeWidth=1;opacity=70;verticalAlign=top;pointerEvents=0;" vertex="1" parent="1"><mxGeometry x="{LANE_X0}" y="{y}" width="{LANE_X1-LANE_X0}" height="{h}" as="geometry"/></mxCell>')
        add(f'<mxCell id="lane-t-{k}" value="\U0001F464 {esc(label)}" style="text;html=1;align=left;fontSize=19;fontStyle=1;fontColor={ACCENT[k]};" vertex="1" parent="1"><mxGeometry x="28" y="{y+14}" width="200" height="26" as="geometry"/></mxCell>')
        add(f'<mxCell id="lane-s-{k}" value="{esc(sub)}" style="text;html=1;align=left;fontSize=11;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="28" y="{y+44}" width="200" height="18" as="geometry"/></mxCell>')

    # step boxes + badges
    for b in BOXES:
        add(f'<mxCell id="s{b["num"]}" value="{step_value(b)}" style="{drawio_step_style(b)}" vertex="1" parent="1"><mxGeometry x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" as="geometry"/></mxCell>')
        add(f'<mxCell id="bd{b["num"]}" value="{b["num"]}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={ACCENT[b["lane"]]};strokeColor=#FFFFFF;strokeWidth=2;fontColor=#FFFFFF;fontSize=14;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="{b["x"]-17}" y="{b["y"]-17}" width="34" height="34" as="geometry"/></mxCell>')

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
                   f'labelBackgroundColor=#FFFFFF;fontSize=10.5;fontStyle=1;fontColor={color};" vertex="1" connectable="0">'
                   f'<mxGeometry x="0.5" y="0.5" relative="1" as="geometry"><mxPoint x="{labpos[0]-mid[0]}" y="{labpos[1]-mid[1]}" as="offset"/></mxGeometry></mxCell>')
        add(f'<mxCell id="{eid}" style="{style}" edge="1" parent="1">'
            f'<mxGeometry relative="1" as="geometry">'
            f'<mxPoint x="{src[0]}" y="{src[1]}" as="sourcePoint"/><mxPoint x="{tgt[0]}" y="{tgt[1]}" as="targetPoint"/>'
            f'<Array as="points">{way}</Array></mxGeometry>{lbl}</mxCell>')

    # return-path big label box
    r1_label = val("\u2713 CONFIRMED (\u22481 MIN)<br>your wallet decrypts<br>your new balance \u2014<font color=&quot;#2E7D32&quot;><b>only you can read it</b></font>")
    add(f'<mxCell id="r1-lb" value="{r1_label}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#2E7D32;strokeWidth=2;fontSize=11;fontColor={INK};align=center;" vertex="1" parent="1"><mxGeometry x="1600" y="640" width="228" height="92" as="geometry"/></mxCell>')

    # footer banner
    add(f'<mxCell id="f1" value="THE WHOLE POINT" style="text;html=1;align=left;fontSize=15;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="40" y="1185" width="300" height="22" as="geometry"/></mxCell>')
    add(f'<mxCell id="f2" value="Your money never leaves your control. The network never sees your amount, your identity, or your balance \u2014 it only agrees, in math, that everything adds up. That is how DERO replaces banks, clouds and databases with one shared, private, tamper-proof notebook." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F4F8FC;strokeColor={TITLE_COLOR};strokeWidth=1.5;fontSize=13.5;fontColor={INK};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="40" y="1210" width="1500" height="96" as="geometry"/></mxCell>')

    # legend
    add(f'<mxCell id="lg" value="LEGEND" style="text;html=1;align=left;fontSize=14;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="1600" y="1185" width="200" height="22" as="geometry"/></mxCell>')
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
            add(f'<mxCell id="lg-chip-edge" value="" style="rounded=1;html=1;fillColor=#FFFFFF;strokeColor={EDGE_BLUE};strokeWidth=2;" vertex="1" parent="1"><mxGeometry x="1610" y="{ly+1}" width="22" height="14" as="geometry"/></mxCell>')
            add(f'<mxCell id="lg-t-edge" value="&#8595; {esc(txt)}" style="text;html=1;align=left;fontSize=10.5;fontColor={INK};" vertex="1" parent="1"><mxGeometry x="1640" y="{ly-2}" width="240" height="18" as="geometry"/></mxCell>')
        else:
            add(f'<mxCell id="lg-chip-{key}" value="" style="rounded=1;html=1;fillColor={ACCENT[key]};strokeColor=none;" vertex="1" parent="1"><mxGeometry x="1610" y="{ly+1}" width="22" height="14" as="geometry"/></mxCell>')
            add(f'<mxCell id="lg-t-{key}" value="{esc(txt)}" style="text;html=1;align=left;fontSize=10.5;fontColor={INK};" vertex="1" parent="1"><mxGeometry x="1640" y="{ly-2}" width="240" height="18" as="geometry"/></mxCell>')
        ly += 24

    return (
        f'<mxGraphModel dx="1500" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" '
        f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" '
        f'math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
        + "".join(cells) + "</root></mxGraphModel>"
    )

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
    add(f'<mxCell id="p2t" value="THE SAME JOURNEY IN PLAIN WORDS" style="text;html=1;align=center;fontSize=28;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="40" as="geometry"/></mxCell>')
    add(f'<mxCell id="p2s" value="Print or share this page with a non-technical audience \u2014 the companion to the \u2018Journey of One Transaction\u2019 diagram." style="text;html=1;align=center;fontSize=13.5;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    add(f'<mxCell id="p2h1" value="TECH SPEAK \u2192 PLAIN SPEAK" style="text;html=1;align=left;fontSize=17;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="60" y="115" width="500" height="26" as="geometry"/></mxCell>')
    add(f'<mxCell id="p2h2" value="KEY NUMBERS" style="text;html=1;align=left;fontSize=17;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="1180" y="115" width="500" height="26" as="geometry"/></mxCell>')
    y = 150
    for i, (tech, plain) in enumerate(TECH_PLAIN):
        add(f'<mxCell id="tp{i}" value="{val(f"<b>{esc(tech)}</b><br><font color=&quot;#66727E&quot;>{esc(plain)}</font>")}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C9D6E3;strokeWidth=1.5;fontSize=12;fontColor={INK};align=left;verticalAlign=middle;spacing=10;" vertex="1" parent="1"><mxGeometry x="60" y="{y}" width="1080" height="52" as="geometry"/></mxCell>')
        y += 60
    y2 = 150
    for i, (num, desc) in enumerate(KEY_NUMBERS):
        add(f'<mxCell id="kn{i}" value="{val(f"<font color=&quot;{TITLE_COLOR}&quot;><b>{esc(num)}</b></font><br><font color=&quot;#66727E&quot;>{esc(desc)}</font>")}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F4F8FC;strokeColor={TITLE_COLOR};strokeWidth=1.5;fontSize=12;fontColor={INK};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="1180" y="{y2}" width="660" height="52" as="geometry"/></mxCell>')
        y2 += 60
    add(f'<mxCell id="p2f" value="DHEBP = DERO Homomorphic Encryption Blockchain Protocol \u00b7 codename Stargate \u00b7 Diagram v1 \u2014 collaborative repo: github.com/liqdmetal/DERO.STARGATE.DIAGRAMS" style="text;html=1;align=center;fontSize=11;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="{max(y, y2) + 30}" width="1880" height="20" as="geometry"/></mxCell>')
    H2 = max(y, y2) + 80
    return f'<mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1920" pageHeight="{H2}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel>"

def build_drawio():
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device">\n'
        f'  <diagram id="journey" name="The Journey of One Transaction">\n{build_page1()}\n  </diagram>\n'
        f'  <diagram id="translation" name="Plain-Language Translation">\n{build_page2()}\n  </diagram>\n'
        '</mxfile>\n'
    )

# ================================================================ SVG ========
def svg_esc(s):
    return html.escape(s)

def build_svg():
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<defs>'
      f'<marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{EDGE_BLUE}"/></marker>'
      f'<marker id="arg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2E7D32"/></marker>'
      f'</defs>')
    A(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')

    # title
    A(f'<text x="{W/2}" y="52" text-anchor="middle" font-size="30" font-weight="700" fill="{TITLE_COLOR}">THE JOURNEY OF ONE DERO TRANSACTION</text>')
    A(f'<text x="{W/2}" y="82" text-anchor="middle" font-size="14" fill="{GRAY}">From your wallet \u2192 through the network \u2192 into the encrypted ledger (DLT) \u2192 confirmation back to you.  Follow the numbers 1 \u2192 14.</text>')
    A(f'<rect x="1600" y="60" width="290" height="30" rx="8" fill="#EAF2FB" stroke="{TITLE_COLOR}"/>')
    A(f'<text x="1745" y="80" text-anchor="middle" font-size="11" font-weight="600" fill="{TITLE_COLOR}">DERO \u00b7 DHEBP (Stargate) \u00b7 Layer 1</text>')

    # lanes
    for k, label, sub, y, h in LANES:
        A(f'<rect x="{LANE_X0}" y="{y}" width="{LANE_X1-LANE_X0}" height="{h}" rx="6" fill="{TINT[k]}" fill-opacity="0.55" stroke="#D8E2EC"/>')
        A(f'<text x="34" y="{y+36}" font-size="19" font-weight="700" fill="{ACCENT[k]}">\U0001F464 {svg_esc(label)}</text>')
        A(f'<text x="34" y="{y+62}" font-size="11" fill="{GRAY}">{svg_esc(sub)}</text>')

    # step boxes
    for b in BOXES:
        x, y, w, h = b["x"], b["y"], b["w"], b["h"]
        acc = ACCENT[b["lane"]]
        A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="{acc}" stroke-width="2"/>')
        A(f'<circle cx="{x}" cy="{y}" r="17" fill="{acc}" stroke="#FFFFFF" stroke-width="2.5"/>')
        A(f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF">{b["num"]}</text>')
        ty = y + 34
        A(f'<text x="{x+12}" y="{ty}" font-size="13" font-weight="700" fill="{acc}">{b["num"]} \u00b7 {svg_esc(b["title"])}</text>')
        ty += 21
        for ln in b["b"]:
            A(f'<text x="{x+12}" y="{ty}" font-size="10.5" fill="{INK}">{svg_esc(ln)}</text>')
            ty += 15
        ty += 6
        for ln in b["p"]:
            A(f'<text x="{x+12}" y="{ty}" font-size="10" font-style="italic" fill="#66727E">\U0001F4A1 {svg_esc(ln)}</text>')
            ty += 14

    # edges
    for eid, pts, color, width, label, labpos in EDGES:
        mk = "arg" if color == "#2E7D32" else "ar"
        d = " ".join(f'L {p[0]} {p[1]}' for p in pts[1:])
        A(f'<path d="M {pts[0][0]} {pts[0][1]} {d}" fill="none" stroke="{color}" stroke-width="{width}" marker-end="url(#{mk})"/>')
        if label:
            A(f'<text x="{labpos[0]}" y="{labpos[1]}" font-size="10.5" font-weight="600" fill="{color}" '
              f'stroke="#FFFFFF" stroke-width="3" paint-order="stroke">{svg_esc(label)}</text>')

    # return label box (clear of step 14: y 640..732)
    A(f'<rect x="1600" y="640" width="228" height="92" rx="10" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2"/>')
    A(f'<text x="1714" y="666" text-anchor="middle" font-size="12" font-weight="700" fill="#2E7D32">\u2713 CONFIRMED (\u22481 MIN)</text>')
    A(f'<text x="1714" y="688" text-anchor="middle" font-size="11" fill="{INK}">your wallet decrypts</text>')
    A(f'<text x="1714" y="706" text-anchor="middle" font-size="11" fill="{INK}">your new balance \u2014</text>')
    A(f'<text x="1714" y="724" text-anchor="middle" font-size="11" font-weight="700" fill="#2E7D32">only you can read it</text>')

    # footer
    A(f'<text x="40" y="1206" font-size="15" font-weight="700" fill="{TITLE_COLOR}">THE WHOLE POINT</text>')
    A(f'<rect x="40" y="1218" width="1500" height="96" rx="10" fill="#F4F8FC" stroke="{TITLE_COLOR}" stroke-width="1.5"/>')
    A(f'<text x="60" y="1252" font-size="13.5" fill="{INK}">Your money never leaves your control. The network never sees your amount, your identity, or your balance \u2014 it only agrees, in math,</text>')
    A(f'<text x="60" y="1272" font-size="13.5" fill="{INK}">that everything adds up. That is how DERO replaces banks, clouds and databases with one shared, private, tamper-proof notebook.</text>')

    # legend
    A(f'<text x="1600" y="1206" font-size="14" font-weight="700" fill="{TITLE_COLOR}">LEGEND</text>')
    ly = 1222
    for key, txt in [
        ("user", "YOU \u2014 the human"), ("wallet", "YOUR WALLET \u2014 the app"),
        ("node", "YOUR NODE \u2014 your daemon"), ("network", "THE NETWORK \u2014 every node"),
        ("miners", "MINERS \u2014 PoW consensus"), ("ledger", "THE LEDGER \u2014 shared DLT"),
        ("confirm", "\u21A9 Confirmation back to you"), ("edge", "\u2193 The transaction\u2019s journey"),
    ]:
        if key == "edge":
            A(f'<rect x="1610" y="{ly}" width="22" height="14" rx="4" fill="#FFFFFF" stroke="{EDGE_BLUE}" stroke-width="2"/>')
        else:
            A(f'<rect x="1610" y="{ly}" width="22" height="14" rx="4" fill="{ACCENT[key]}"/>')
        A(f'<text x="1642" y="{ly+12}" font-size="10.5" fill="{INK}">{svg_esc(txt)}</text>')
        ly += 24

    A('</svg>')
    return "\n".join(out)

def build_svg_page2():
    out = []
    A = out.append
    W2, H2 = 1920, 950
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<rect x="0" y="0" width="{W2}" height="{H2}" fill="#FFFFFF"/>')
    A(f'<text x="{W2/2}" y="52" text-anchor="middle" font-size="28" font-weight="700" fill="{TITLE_COLOR}">THE SAME JOURNEY IN PLAIN WORDS</text>')
    A(f'<text x="{W2/2}" y="82" text-anchor="middle" font-size="13.5" fill="{GRAY}">Print or share this page with a non-technical audience \u2014 the companion to the \u2018Journey of One Transaction\u2019 diagram.</text>')
    A(f'<text x="60" y="130" font-size="17" font-weight="700" fill="{TITLE_COLOR}">TECH SPEAK \u2192 PLAIN SPEAK</text>')
    A(f'<text x="1180" y="130" font-size="17" font-weight="700" fill="{TITLE_COLOR}">KEY NUMBERS</text>')
    y = 150
    for i, (tech, plain) in enumerate(TECH_PLAIN):
        A(f'<rect x="60" y="{y}" width="1080" height="52" rx="8" fill="#FFFFFF" stroke="#C9D6E3" stroke-width="1.5"/>')
        A(f'<text x="76" y="{y+22}" font-size="12.5" font-weight="700" fill="{INK}">{svg_esc(tech)}</text>')
        A(f'<text x="76" y="{y+40}" font-size="11.5" fill="#66727E">{svg_esc(plain)}</text>')
        y += 60
    y2 = 150
    for i, (num, desc) in enumerate(KEY_NUMBERS):
        A(f'<rect x="1180" y="{y2}" width="660" height="52" rx="8" fill="#F4F8FC" stroke="{TITLE_COLOR}" stroke-width="1.5"/>')
        A(f'<text x="1210" y="{y2+24}" font-size="15" font-weight="700" fill="{TITLE_COLOR}">{svg_esc(num)}</text>')
        A(f'<text x="1210" y="{y2+43}" font-size="11.5" fill="#66727E">{svg_esc(desc)}</text>')
        y2 += 60
    A(f'<text x="{W2/2}" y="{max(y, y2) + 30}" text-anchor="middle" font-size="11" fill="{GRAY}">DHEBP = DERO Homomorphic Encryption Blockchain Protocol \u00b7 codename Stargate \u00b7 Diagram v1 \u2014 collaborative repo: github.com/liqdmetal/DERO.STARGATE.DIAGRAMS</text>')
    A('</svg>')
    return "\n".join(out)

# ================================================================ main ======
if __name__ == "__main__":
    import os
    d = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(d, "DERO.PROCESS.COMPLETE.drawio"), "w", encoding="utf-8") as f:
        f.write(build_drawio())
    with open(os.path.join(d, "preview_page1.svg"), "w", encoding="utf-8") as f:
        f.write(build_svg())
    with open(os.path.join(d, "preview_page2.svg"), "w", encoding="utf-8") as f:
        f.write(build_svg_page2())
    with open(os.path.join(d, "preview_page1.html"), "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;}}</style></head><body>{build_svg()}</body></html>')
    with open(os.path.join(d, "preview_page2.html"), "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;}}</style></head><body>{build_svg_page2()}</body></html>')
    print("written OK")
    # report geometry stats
    for b in BOXES:
        print(f'step {b["num"]:>2}: y={b["y"]:>4} h={b["h"]:>3}  lane={b["lane"]:>7}  lines b={len(b["b"])} p={len(b["p"])}')
