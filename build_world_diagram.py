#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DERO World diagram generator.
Page 1: DERO's Place in the Modern World  (old world vs DERO world, by user need)
Page 2: The Swap Table (centralized service -> DERO replacement -> what changes)
Emits draw.io XML + SVG previews from one data model.
"""
import xml.sax.saxutils as sax
import datetime, html

# palette (same family as journey diagram)
NEED_A, NEED_T = "#F9A825", "#FFF8E1"     # amber   - what you need
OLD_A,  OLD_T  = "#C62828", "#FDECEA"     # red     - old world
DERO_A, DERO_T = "#2E7D32", "#E8F5E9"     # green   - DERO world
TOOL_A, TOOL_T = "#00838F", "#E0F7FA"     # teal    - toolbox
TITLE_COLOR = "#4277BB"
INK, GRAY = "#22303C", "#5A6B7A"
EDGE_GREEN = "#2E7D32"

W, H = 1920, 1400

ROWS = [
    dict(num=1, need_title="PAYING SOMEONE", need="Send money to anyone, anywhere",
         old_title="Bank or payment app",
         old="They see every payment, can freeze or censor you, charge fees, demand ID.",
         old_plain="The bank is the referee \u2014 and it keeps the ball.",
         dero_title="Direct private transfer (DHEBP)",
         dero="Amount + identity hidden by homomorphic encryption. Settled in ~1 min, tiny ~2.5 KB tx, tiny fee.",
         dero_plain="Only you and the recipient know what moved."),
    dict(num=2, need_title="MAKING A DEAL", need="Agree on terms both sides will honor",
         old_title="Lawyer, notary or platform",
         old="Holds the money and the trust: slow, costly, and you must trust them.",
         old_plain="Trust is rented from a third party.",
         dero_title="DVM smart contract (DeroScript)",
         dero="Code is the escrow: it runs on every node, nobody can break or rewrite it. Escrow, tokens, auctions, lotteries.",
         dero_plain="Trust is replaced by math everyone can check."),
    dict(num=3, need_title="STORING RECORDS", need="Keep data safe, private, permanent",
         old_title="Company cloud (AWS, Google\u2026)",
         old="They read, sell, or lose your data; one breach exposes everything.",
         old_plain="Your data in someone else\u2019s filing cabinet.",
         dero_title="Encrypted ledger + GravitonDB",
         dero="Accounts are 66 bytes of encrypted state, never decrypted, merkle-proved, prunable to a few GB.",
         dero_plain="A lockbox only you can open."),
    dict(num=4, need_title="RUNNING AN APP", need="Host software people can use",
         old_title="Web server + domain + hosting",
         old="One point of failure: can be blocked, hacked, or switched off.",
         old_plain="Your shop sits on someone else\u2019s land.",
         dero_title="TELA \u2014 apps on the chain",
         dero="Code and assets live on-chain, served by the network itself. No origin server to attack or censor.",
         dero_plain="Your shop is on everyone\u2019s land \u2014 and nobody owns it."),
    dict(num=5, need_title="PROVING WHO YOU ARE", need="Authenticate without being spied on",
         old_title="Passwords + emails + data brokers",
         old="Leaks, phishing, and your identity bought and sold.",
         old_plain="You flash your whole wallet to prove you\u2019re an adult.",
         dero_title="Wallet + DeroAuth + usernames",
         dero="Sign in with your wallet (XSWD bridge); the DVM Name Service gives human names; zero-knowledge proofs reveal only what\u2019s needed.",
         dero_plain="Prove you\u2019re over 18 without showing your ID."),
]

TOOLBOX = [
    ("DHEBP \u00b7 Layer 1", "encrypted chain \u00b7 PoW AstroBWTv3 \u00b7 18 s blocks"),
    ("DVM", "smart contracts \u00b7 DeroScript"),
    ("GravitonDB", "encrypted key/value state"),
    ("TELA", "on-chain apps & web \u2014 no server"),
    ("XSWD", "app \u2194 wallet bridge"),
    ("DeroAuth / DeroPay", "sign in \u00b7 pay with your wallet"),
    ("Name Service", "human usernames on-chain"),
]

# ------------------------------------------------------------- geometry -----
ROW_Y = [132, 316, 500, 684, 868]
ROW_H = 176
NEED_X, NEED_W = 30, 330
OLD_X, OLD_W = 390, 560
DERO_X, DERO_W = 980, 630
TOOL_X, TOOL_W = 1640, 250

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

def cell_lines(step, key, w):
    t = [step[key + "_title"]]
    b = wrap(step[key], w - 24, 11.0)
    p = wrap(step[key + "_plain"], w - 24, 10.5)
    return t, b, p

def cell_h(t, b, p):
    return 24 + 17 + len(b) * 16 + 6 + len(p) * 15 + 10

# ============================================================ draw.io XML ====
def esc(s):
    return sax.escape(s, {"'": "&apos;"})

def val(s):
    return s.replace("<", "&lt;").replace(">", "&gt;")

def hbox(parts, accent):
    return val("<br>".join(
        [f'<font color=&quot;{accent}&quot;><b>{esc(parts[0])}</b></font>']
        + [esc(x) for x in parts[1:-1]] if False else
        [f'<font color=&quot;{accent}&quot;><b>{esc(parts[0])}</b></font>']
        + [esc(x) for x in parts[1:-1]]))

def build_page1():
    cells = []
    def add(x):
        cells.append(x)
    # title
    add(f'<mxCell id="w-t1" value="DERO&apos;S PLACE IN THE MODERN WORLD" style="text;html=1;align=center;fontSize=30;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="42" as="geometry"/></mxCell>')
    add(f'<mxCell id="w-t2" value="Same everyday needs. Completely different plumbing. \u2014 How the DHEBP stack replaces banks, clouds and middlemen." style="text;html=1;align=center;fontSize=14;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    add(f'<mxCell id="w-t3" value="DERO \u00b7 DHEBP (Stargate) \u00b7 Layer 1 \u2192 2" style="rounded=1;html=1;fillColor=#EAF2FB;strokeColor={TITLE_COLOR};fontColor={TITLE_COLOR};fontSize=11;fontStyle=1;align=center;" vertex="1" parent="1"><mxGeometry x="1600" y="66" width="290" height="30" as="geometry"/></mxCell>')
    # legend strip
    add(f'<mxCell id="w-lg1" value="" style="rounded=1;html=1;fillColor={NEED_T};strokeColor={NEED_A};strokeWidth=2;" vertex="1" parent="1"><mxGeometry x="60" y="102" width="20" height="12" as="geometry"/></mxCell>')
    add(f'<mxCell id="w-lg1t" value="what you need" style="text;html=1;align=left;fontSize=11;fontColor={INK};" vertex="1" parent="1"><mxGeometry x="86" y="98" width="130" height="18" as="geometry"/></mxCell>')
    add(f'<mxCell id="w-lg2" value="" style="rounded=1;html=1;fillColor={OLD_T};strokeColor={OLD_A};strokeWidth=2;" vertex="1" parent="1"><mxGeometry x="240" y="102" width="20" height="12" as="geometry"/></mxCell>')
    add(f'<mxCell id="w-lg2t" value="old world \u2014 centralized" style="text;html=1;align=left;fontSize=11;fontColor={INK};" vertex="1" parent="1"><mxGeometry x="266" y="98" width="190" height="18" as="geometry"/></mxCell>')
    add(f'<mxCell id="w-lg3" value="" style="rounded=1;html=1;fillColor={DERO_T};strokeColor={DERO_A};strokeWidth=2;" vertex="1" parent="1"><mxGeometry x="480" y="102" width="20" height="12" as="geometry"/></mxCell>')
    add(f'<mxCell id="w-lg3t" value="DERO world \u2014 decentralized &amp; private" style="text;html=1;align=left;fontSize=11;fontColor={INK};" vertex="1" parent="1"><mxGeometry x="506" y="98" width="280" height="18" as="geometry"/></mxCell>')
    add(f'<mxCell id="w-lg4" value="\u2192 replaced by" style="text;html=1;align=left;fontSize=11;fontStyle=1;fontColor={EDGE_GREEN};" vertex="1" parent="1"><mxGeometry x="790" y="98" width="120" height="18" as="geometry"/></mxCell>')

    for i, r in enumerate(ROWS):
        y = ROW_Y[i]
        # need cell
        need_value = val(f"<font color=&quot;{NEED_A}&quot;><b>{r['num']} \u00b7 {esc(r['need_title'])}</b></font><br>{esc(r['need'])}")
        add(f'<mxCell id="w-n{i}" value="{need_value}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={NEED_T};strokeColor={NEED_A};strokeWidth=2;verticalAlign=top;align=left;spacing=10;spacingTop=16;fontSize=11.5;fontColor={INK};" vertex="1" parent="1"><mxGeometry x="{NEED_X}" y="{y}" width="{NEED_W}" height="{ROW_H}" as="geometry"/></mxCell>')
        # old cell
        ot, ob, op = cell_lines(r, "old", OLD_W)
        plain_old = ["\U0001F4A1 " + esc(x) for x in op]
        ovals = [f'<font color=&quot;{OLD_A}&quot;><b>{esc(ot[0])}</b></font>'] + [esc(x) for x in ob] + ["<br>"] + [f'<font color=&quot;#66727E&quot;><i>{p}</i></font>' for p in plain_old]
        old_value = val("<br>".join(ovals))
        add(f'<mxCell id="w-o{i}" value="{old_value}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={OLD_T};strokeColor={OLD_A};strokeWidth=2;verticalAlign=top;align=left;spacing=10;spacingTop=16;fontSize=11;fontColor={INK};" vertex="1" parent="1"><mxGeometry x="{OLD_X}" y="{y}" width="{OLD_W}" height="{ROW_H}" as="geometry"/></mxCell>')
        # dero cell
        dt, db, dp = cell_lines(r, "dero", DERO_W)
        plain_dero = ["\U0001F4A1 " + esc(x) for x in dp]
        dvals = [f'<font color=&quot;{DERO_A}&quot;><b>{esc(dt[0])}</b></font>'] + [esc(x) for x in db] + ["<br>"] + [f'<font color=&quot;#66727E&quot;><i>{p}</i></font>' for p in plain_dero]
        dero_value = val("<br>".join(dvals))
        add(f'<mxCell id="w-d{i}" value="{dero_value}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={DERO_T};strokeColor={DERO_A};strokeWidth=2;verticalAlign=top;align=left;spacing=10;spacingTop=16;fontSize=11;fontColor={INK};" vertex="1" parent="1"><mxGeometry x="{DERO_X}" y="{y}" width="{DERO_W}" height="{ROW_H}" as="geometry"/></mxCell>')
        # swap arrow old -> dero
        midy = y + ROW_H / 2
        add(f'<mxCell id="w-a{i}" value="{esc("replaced by")}" style="edgeStyle=none;rounded=0;html=1;endArrow=classicThin;endFill=1;strokeColor={EDGE_GREEN};strokeWidth=3;fontSize=11;fontStyle=1;fontColor={EDGE_GREEN};labelBackgroundColor=#FFFFFF;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{OLD_X+OLD_W}" y="{midy}" as="sourcePoint"/><mxPoint x="{DERO_X}" y="{midy}" as="targetPoint"/></mxGeometry><mxCell id="w-a{i}l" value="{esc("replaced by")}" style="edgeLabel;html=1;align=center;verticalAlign=middle;labelBackgroundColor=#FFFFFF;fontSize=11;fontStyle=1;fontColor={EDGE_GREEN};" vertex="1" connectable="0"><mxGeometry x="-0.5" y="0" relative="1" as="geometry"><mxPoint as="offset"/></mxGeometry></mxCell></mxCell>')
        # subtle row separator
        if i > 0:
            add(f'<mxCell id="w-sep{i}" value="" style="line;strokeWidth=1;strokeColor=#D8E2EC;html=1;" vertex="1" parent="1"><mxGeometry x="30" y="{y-8}" width="1880" height="1" as="geometry"/></mxCell>')

    # toolbox column
    add(f'<mxCell id="w-tool" value="THE DERO TOOLBOX" style="text;html=1;align=left;fontSize=14;fontStyle=1;fontColor={TOOL_A};" vertex="1" parent="1"><mxGeometry x="{TOOL_X+6}" y="140" width="220" height="22" as="geometry"/></mxCell>')
    ty = 170
    for name, desc in TOOLBOX:
        add(f'<mxCell id="w-tb-{name[:3]}" value="{val(f"<font color=&quot;{TOOL_A}&quot;><b>{esc(name)}</b></font><br><font color=&quot;#66727E&quot;>{esc(desc)}</font>")}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={TOOL_T};strokeColor={TOOL_A};strokeWidth=1.5;fontSize=10.5;fontColor={INK};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="{TOOL_X}" y="{ty}" width="{TOOL_W}" height="62" as="geometry"/></mxCell>')
        ty += 70

    # bottom band
    add(f'<mxCell id="w-f1" value="THE SAME JOB \u2014 NO MIDDLEMAN" style="text;html=1;align=left;fontSize=15;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="40" y="1095" width="420" height="22" as="geometry"/></mxCell>')
    add(f'<mxCell id="w-f2" value="Money, deals, data, apps, identity \u2014 the modern world runs them on banks, clouds and platforms. DERO runs them on one shared, private, tamper-proof network: every node does the job, and none of them can see your business." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F4F8FC;strokeColor={TITLE_COLOR};strokeWidth=1.5;fontSize=13.5;fontColor={INK};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="40" y="1120" width="1810" height="96" as="geometry"/></mxCell>')

    return f'<mxGraphModel dx="1500" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel>"

# ------------------------------------------------------------ page 2 ---------
SWAPS = [
    ("Bank transfer / payment app", "DERO transfer (DHEBP)", "Private, uncensorable, ~1 min settle"),
    ("Escrow / notary / legal fees", "DVM smart contract (DeroScript)", "Automatic escrow, unbreakable rules"),
    ("Cloud database (AWS, Google\u2026)", "Encrypted ledger + GravitonDB", "Encrypted, provable, 66 B per account"),
    ("Web hosting + domain", "TELA on-chain web", "No server to hack or censor"),
    ("Login / identity system", "Wallet + DeroAuth + Name Service", "Prove only what\u2019s needed"),
    ("Exchange / auction / lottery", "DVM tokens & contracts", "Transparent rules, private state"),
    ("Auditing & compliance", "Zero-knowledge proofs + public supply", "Verify without revealing secrets"),
]

def build_page2():
    cells = []
    def add(x):
        cells.append(x)
    H2 = 150 + 8 * 72 + 120
    add(f'<mxCell id="s-t1" value="THE SWAP TABLE" style="text;html=1;align=center;fontSize=28;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="40" as="geometry"/></mxCell>')
    add(f'<mxCell id="s-t2" value="Every centralized service you use today has a DERO-native replacement. Same job, no middleman." style="text;html=1;align=center;fontSize=13.5;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    headers = ["CENTRALIZED SERVICE TODAY", "DERO REPLACEMENT", "WHAT CHANGES FOR YOU"]
    xs = [60, 720, 1380]
    ws = [640, 640, 480]
    for j, htxt in enumerate(headers):
        add(f'<mxCell id="s-h{j}" value="{esc(htxt)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EAF2FB;strokeColor={TITLE_COLOR};strokeWidth=2;fontSize=13;fontStyle=1;fontColor={TITLE_COLOR};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="{xs[j]}" y="110" width="{ws[j]}" height="34" as="geometry"/></mxCell>')
    y = 152
    for i, (a, b, c) in enumerate(SWAPS):
        colors = [(OLD_A, OLD_T), (DERO_A, DERO_T), (TOOL_A, TOOL_T)]
        vals = [a, b, c]
        for j in range(3):
            add(f'<mxCell id="s-r{i}c{j}" value="{esc(vals[j])}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={colors[j][1]};strokeColor={colors[j][0]};strokeWidth=1.5;fontSize=12;fontColor={INK};align=center;verticalAlign=middle;spacing=8;" vertex="1" parent="1"><mxGeometry x="{xs[j]}" y="{y}" width="{ws[j]}" height="64" as="geometry"/></mxCell>')
        y += 72
    add(f'<mxCell id="s-f" value="DERO is a general-purpose, private, decentralized application platform \u2014 the DHEBP stack, end to end." style="text;html=1;align=center;fontSize=12;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="{y+16}" width="1880" height="20" as="geometry"/></mxCell>')
    return f'<mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1920" pageHeight="{H2}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel>"

def build_drawio():
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device">\n'
            f'  <diagram id="world" name="DERO Place in the Modern World">\n{build_page1()}\n  </diagram>\n'
            f'  <diagram id="swap" name="The Swap Table">\n{build_page2()}\n  </diagram>\n'
            '</mxfile>\n')

# ================================================================ SVG ========
def svg_esc(s):
    return html.escape(s)

def svg_cell(parts_lines, accent, x, y, w, h, title_font=12.5):
    """parts_lines: (title, [body lines], [plain lines])"""
    out = []
    A = out.append
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="{accent}" stroke-width="2"/>')
    ty = y + 26
    A(f'<text x="{x+12}" y="{ty}" font-size="{title_font}" font-weight="700" fill="{accent}">{svg_esc(parts_lines[0])}</text>')
    ty += 19
    for ln in parts_lines[1]:
        A(f'<text x="{x+12}" y="{ty}" font-size="11" fill="{INK}">{svg_esc(ln)}</text>')
        ty += 16
    ty += 6
    for ln in parts_lines[2]:
        A(f'<text x="{x+12}" y="{ty}" font-size="10.5" font-style="italic" fill="#66727E">\U0001F4A1 {svg_esc(ln)}</text>')
        ty += 15
    return "\n".join(out)

def build_svg_page1():
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<defs><marker id="arg2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{EDGE_GREEN}"/></marker></defs>')
    A(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')
    A(f'<text x="{W/2}" y="52" text-anchor="middle" font-size="30" font-weight="700" fill="{TITLE_COLOR}">DERO\u2019S PLACE IN THE MODERN WORLD</text>')
    A(f'<text x="{W/2}" y="82" text-anchor="middle" font-size="14" fill="{GRAY}">Same everyday needs. Completely different plumbing. \u2014 How the DHEBP stack replaces banks, clouds and middlemen.</text>')
    A(f'<rect x="1600" y="60" width="290" height="30" rx="8" fill="#EAF2FB" stroke="{TITLE_COLOR}"/>')
    A(f'<text x="1745" y="80" text-anchor="middle" font-size="11" font-weight="600" fill="{TITLE_COLOR}">DERO \u00b7 DHEBP (Stargate) \u00b7 Layer 1 \u2192 2</text>')
    # legend strip
    A(f'<rect x="60" y="100" width="20" height="12" rx="3" fill="{NEED_T}" stroke="{NEED_A}" stroke-width="2"/>')
    A(f'<text x="86" y="110" font-size="11" fill="{INK}">what you need</text>')
    A(f'<rect x="240" y="100" width="20" height="12" rx="3" fill="{OLD_T}" stroke="{OLD_A}" stroke-width="2"/>')
    A(f'<text x="266" y="110" font-size="11" fill="{INK}">old world \u2014 centralized</text>')
    A(f'<rect x="480" y="100" width="20" height="12" rx="3" fill="{DERO_T}" stroke="{DERO_A}" stroke-width="2"/>')
    A(f'<text x="506" y="110" font-size="11" fill="{INK}">DERO world \u2014 decentralized &amp; private</text>')
    A(f'<text x="790" y="110" font-size="11" font-weight="700" fill="{EDGE_GREEN}">\u2192 replaced by</text>')

    for i, r in enumerate(ROWS):
        y = ROW_Y[i]
        midy = y + ROW_H / 2
        # need cell (tinted fill, badge)
        A(f'<rect x="{NEED_X}" y="{y}" width="{NEED_W}" height="{ROW_H}" rx="10" fill="{NEED_T}" stroke="{NEED_A}" stroke-width="2"/>')
        A(f'<circle cx="{NEED_X+20}" cy="{y+22}" r="13" fill="{NEED_A}" stroke="#FFFFFF" stroke-width="2"/>')
        A(f'<text x="{NEED_X+20}" y="{y+27}" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">{r["num"]}</text>')
        A(f'<text x="{NEED_X+40}" y="{y+27}" font-size="12" font-weight="700" fill="{NEED_A}">{svg_esc(r["need_title"])}</text>')
        A(f'<text x="{NEED_X+12}" y="{y+52}" font-size="11" fill="{INK}">{svg_esc(r["need"])}</text>')
        # old cell
        ot, ob, op = cell_lines(r, "old", OLD_W)
        A(f'<rect x="{OLD_X}" y="{y}" width="{OLD_W}" height="{ROW_H}" rx="10" fill="{OLD_T}" stroke="{OLD_A}" stroke-width="2"/>')
        A(f'<text x="{OLD_X+12}" y="{y+26}" font-size="12.5" font-weight="700" fill="{OLD_A}">{svg_esc(ot[0])}</text>')
        ty = y + 46
        for ln in ob:
            A(f'<text x="{OLD_X+12}" y="{ty}" font-size="11" fill="{INK}">{svg_esc(ln)}</text>'); ty += 16
        ty += 6
        for ln in op:
            A(f'<text x="{OLD_X+12}" y="{ty}" font-size="10.5" font-style="italic" fill="#66727E">\U0001F4A1 {svg_esc(ln)}</text>'); ty += 15
        # dero cell
        dt, db, dp = cell_lines(r, "dero", DERO_W)
        A(f'<rect x="{DERO_X}" y="{y}" width="{DERO_W}" height="{ROW_H}" rx="10" fill="{DERO_T}" stroke="{DERO_A}" stroke-width="2"/>')
        A(f'<text x="{DERO_X+12}" y="{y+26}" font-size="12.5" font-weight="700" fill="{DERO_A}">{svg_esc(dt[0])}</text>')
        ty = y + 46
        for ln in db:
            A(f'<text x="{DERO_X+12}" y="{ty}" font-size="11" fill="{INK}">{svg_esc(ln)}</text>'); ty += 16
        ty += 6
        for ln in dp:
            A(f'<text x="{DERO_X+12}" y="{ty}" font-size="10.5" font-style="italic" fill="#66727E">\U0001F4A1 {svg_esc(ln)}</text>'); ty += 15
        # swap arrow
        A(f'<line x1="{OLD_X+OLD_W}" y1="{midy}" x2="{DERO_X}" y2="{midy}" stroke="{EDGE_GREEN}" stroke-width="3" marker-end="url(#arg2)"/>')
        A(f'<text x="{(OLD_X+OLD_W+DERO_X)/2}" y="{midy-8}" text-anchor="middle" font-size="11" font-weight="700" fill="{EDGE_GREEN}" stroke="#FFFFFF" stroke-width="3" paint-order="stroke">replaced by</text>')

    # toolbox
    A(f'<text x="{TOOL_X+6}" y="158" font-size="14" font-weight="700" fill="{TOOL_A}">THE DERO TOOLBOX</text>')
    ty = 172
    for name, desc in TOOLBOX:
        A(f'<rect x="{TOOL_X}" y="{ty}" width="{TOOL_W}" height="62" rx="8" fill="{TOOL_T}" stroke="{TOOL_A}" stroke-width="1.5"/>')
        A(f'<text x="{TOOL_X+TOOL_W/2}" y="{ty+24}" text-anchor="middle" font-size="11" font-weight="700" fill="{TOOL_A}">{svg_esc(name)}</text>')
        A(f'<text x="{TOOL_X+TOOL_W/2}" y="{ty+42}" text-anchor="middle" font-size="9.5" fill="#66727E">{svg_esc(desc)}</text>')
        ty += 70

    # bottom band
    A(f'<text x="40" y="1116" font-size="15" font-weight="700" fill="{TITLE_COLOR}">THE SAME JOB \u2014 NO MIDDLEMAN</text>')
    A(f'<rect x="40" y="1128" width="1810" height="96" rx="10" fill="#F4F8FC" stroke="{TITLE_COLOR}" stroke-width="1.5"/>')
    A(f'<text x="60" y="1162" font-size="13.5" fill="{INK}">Money, deals, data, apps, identity \u2014 the modern world runs them on banks, clouds and platforms. DERO runs them on one shared, private,</text>')
    A(f'<text x="60" y="1184" font-size="13.5" fill="{INK}">tamper-proof network: every node does the job, and none of them can see your business.</text>')
    A('</svg>')
    return "\n".join(out)

def build_svg_page2():
    out = []
    A = out.append
    H2 = 150 + 8 * 72 + 120
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="{H2}" viewBox="0 0 1920 {H2}" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<rect x="0" y="0" width="1920" height="{H2}" fill="#FFFFFF"/>')
    A(f'<text x="960" y="52" text-anchor="middle" font-size="28" font-weight="700" fill="{TITLE_COLOR}">THE SWAP TABLE</text>')
    A(f'<text x="960" y="82" text-anchor="middle" font-size="13.5" fill="{GRAY}">Every centralized service you use today has a DERO-native replacement. Same job, no middleman.</text>')
    xs = [60, 720, 1380]; ws = [640, 640, 480]
    headers = ["CENTRALIZED SERVICE TODAY", "DERO REPLACEMENT", "WHAT CHANGES FOR YOU"]
    for j, htxt in enumerate(headers):
        A(f'<rect x="{xs[j]}" y="110" width="{ws[j]}" height="34" rx="8" fill="#EAF2FB" stroke="{TITLE_COLOR}" stroke-width="2"/>')
        A(f'<text x="{xs[j]+ws[j]/2}" y="131" text-anchor="middle" font-size="13" font-weight="700" fill="{TITLE_COLOR}">{svg_esc(htxt)}</text>')
    y = 152
    colors = [(OLD_A, OLD_T), (DERO_A, DERO_T), (TOOL_A, TOOL_T)]
    for i, (a, b, c) in enumerate(SWAPS):
        for j, v in enumerate([a, b, c]):
            A(f'<rect x="{xs[j]}" y="{y}" width="{ws[j]}" height="64" rx="8" fill="{colors[j][1]}" stroke="{colors[j][0]}" stroke-width="1.5"/>')
            A(f'<text x="{xs[j]+ws[j]/2}" y="{y+37}" text-anchor="middle" font-size="12" fill="{INK}">{svg_esc(v)}</text>')
        y += 72
    A(f'<text x="960" y="{y+40}" text-anchor="middle" font-size="12" font-weight="700" fill="{TITLE_COLOR}">DERO is a general-purpose, private, decentralized application platform \u2014 the DHEBP stack, end to end.</text>')
    A('</svg>')
    return "\n".join(out)

# ================================================================ main ======
if __name__ == "__main__":
    import os
    d = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(d, "DERO.WORLD.drawio"), "w", encoding="utf-8") as f:
        f.write(build_drawio())
    for name, fn in [("preview_world1.svg", build_svg_page1), ("preview_world2.svg", build_svg_page2)]:
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(fn())
        with open(os.path.join(d, name.replace(".svg", ".html")), "w", encoding="utf-8") as f:
            f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;}}</style></head><body>{fn()}</body></html>')
    print("written OK")
