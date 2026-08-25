#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DERO.WORLD.drawio — DERO's place in the modern world (new template).

Page 1: old world vs DERO world, by user need.
Page 2: The Swap Table.
Tight dero_style template - light + dark via argv. Previews via render_drawio_svg.
"""
import datetime, os, sys
import dero_style as S

PAGE_W, PAGE_H = 1920, 1400

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

SWAPS = [
    ("Bank transfer / payment app", "DERO transfer (DHEBP)", "Private, uncensorable, ~1 min settle"),
    ("Escrow / notary / legal fees", "DVM smart contract (DeroScript)", "Automatic escrow, unbreakable rules"),
    ("Cloud database (AWS, Google\u2026)", "Encrypted ledger + GravitonDB", "Encrypted, provable, 66 B per account"),
    ("Web hosting + domain", "TELA on-chain web", "No server to hack or censor"),
    ("Login / identity system", "Wallet + DeroAuth + Name Service", "Prove only what\u2019s needed"),
    ("Exchange / auction / lottery", "DVM tokens & contracts", "Transparent rules, private state"),
    ("Auditing & compliance", "Zero-knowledge proofs + public supply", "Verify without revealing secrets"),
]

def card(cells, add, x, y, w, h, acc, title, body_lines, plain_lines, align="left"):
    v = f"<font color=&quot;{S.accent(acc)[0]}&quot;><b>{S.esc(title)}</b></font><br>"
    v += "<br>".join(S.esc(l) for l in body_lines)
    if plain_lines:
        v += "<br>" + "<br>".join(f'<font color=&quot;{S.TH["muted"]}&quot;><i>\U0001F4A1 {S.esc(p)}</i></font>' for p in plain_lines)
    add(f'<mxCell id="c-{len(cells)}" value="{S.val(v)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent(acc)[0]};strokeWidth=1.5;shadow=1;fontSize=11.5;fontColor={S.TH["ink"]};align={align};verticalAlign=top;spacing=10;spacingTop=14;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

def wrap_plain(text, width_px, font_px=11.0):
    return S.wrap(text, width_px, font_px)

def build_page1():
    cells = []
    add = cells.append
    for c in S.d_header("w-t", 20, 22, PAGE_W-40, "DERO\u2019S PLACE IN THE MODERN WORLD",
                        "Same everyday needs \u00b7 completely different plumbing \u2014 how the DHEBP stack replaces banks, clouds and middlemen.", font=28):
        add(c)
    # legend
    ly = 102
    for i, (acc, label) in enumerate([("amber", "what you need"), ("red", "old world \u2014 centralized"), ("green", "DERO world \u2014 private"), ("brand", "\u2192 replaced by")]):
        x = 60 + i * 360
        add(f'<mxCell id="lg{i}" value="{S.esc(label)}" style="text;html=1;align=left;fontSize=11.5;fontStyle=1;fontColor={S.accent(acc)[0]};" vertex="1" parent="1"><mxGeometry x="{x}" y="{ly}" width="320" height="18" as="geometry"/></mxCell>')
    ROW_Y = [132, 316, 500, 684, 868]
    ROW_H = 176
    NEED_X, NEED_W = 30, 330
    OLD_X, OLD_W = 390, 560
    DERO_X, DERO_W = 980, 630
    TOOL_X, TOOL_W = 1640, 250
    for i, r in enumerate(ROWS):
        y = ROW_Y[i]
        need_lines = wrap_plain(r["need"], NEED_W - 24)
        card(cells, add, NEED_X, y, NEED_W, ROW_H, "amber", f"{r['num']} \u00b7 {r['need_title']}", need_lines, [])
        old_lines = wrap_plain(r["old"], OLD_W - 24)
        old_plain = wrap_plain(r["old_plain"], OLD_W - 24, 10.5)
        card(cells, add, OLD_X, y, OLD_W, ROW_H, "red", r["old_title"], old_lines, old_plain)
        dero_lines = wrap_plain(r["dero"], DERO_W - 24)
        dero_plain = wrap_plain(r["dero_plain"], DERO_W - 24, 10.5)
        card(cells, add, DERO_X, y, DERO_W, ROW_H, "green", r["dero_title"], dero_lines, dero_plain)
        midy = y + ROW_H // 2
        for c in S.d_arrow(f"a{i}", [(OLD_X + OLD_W + 4, midy), (DERO_X - 4, midy)], accent_key="green", label="replaced by", width=3):
            add(c)
    # toolbox
    add(f'<mxCell id="w-tool" value="{S.esc("THE DERO TOOLBOX")}" style="text;html=1;align=left;fontSize=15;fontStyle=1;fontColor={S.accent("teal")[0]};" vertex="1" parent="1"><mxGeometry x="{TOOL_X+6}" y="130" width="230" height="22" as="geometry"/></mxCell>')
    ty = 158
    for name, desc in TOOLBOX:
        tb_html = f"<font color=&quot;{S.accent('teal')[0]}&quot;><b>{S.esc(name)}</b></font><br><font color=&quot;{S.TH['muted']}&quot;>{S.esc(desc)}</font>"
        add(f'<mxCell id="tb-{name[:3]}" value="{S.val(tb_html)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("teal")[0]};strokeWidth=1.4;shadow=1;fontSize=10.5;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="{TOOL_X}" y="{ty}" width="{TOOL_W}" height="62" as="geometry"/></mxCell>')
        ty += 68
    # bottom band
    f1_txt = "THE SAME JOB \u2014 NO MIDDLEMAN"
    add(f'<mxCell id="w-f1" value="{S.esc(f1_txt)}" style="text;html=1;align=left;fontSize=15;fontStyle=1;fontColor={S.accent("brand")[0]};" vertex="1" parent="1"><mxGeometry x="40" y="1095" width="420" height="22" as="geometry"/></mxCell>')
    foot = "Money, deals, data, apps, identity \u2014 the modern world runs them on banks, clouds and platforms. DERO runs them on one shared, private, tamper-proof network: every node does the job, and none of them can see your business."
    add(f'<mxCell id="w-f2" value="{S.esc(foot)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("brand")[0]};strokeWidth=1.5;shadow=1;fontSize=13.5;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="40" y="1120" width="1810" height="96" as="geometry"/></mxCell>')
    return S.d_graph(PAGE_W, PAGE_H, cells)

def build_page2():
    cells = []
    add = cells.append
    H2 = 150 + 8 * 72 + 140
    for c in S.d_header("s-t", 20, 22, PAGE_W-40, "THE SWAP TABLE",
                        "Every centralized service you use today has a DERO-native replacement. Same job, no middleman.", font=28):
        add(c)
    headers = ["CENTRALIZED SERVICE TODAY", "DERO REPLACEMENT", "WHAT CHANGES FOR YOU"]
    xs = [60, 720, 1380]
    ws = [640, 640, 480]
    hacc = ["red", "green", "teal"]
    for j, htxt in enumerate(headers):
        add(f'<mxCell id="s-h{j}" value="{S.esc(htxt)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.accent(hacc[j])[0]};strokeColor=none;fontSize=13;fontStyle=1;fontColor=#FFFFFF;align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="{xs[j]}" y="110" width="{ws[j]}" height="34" as="geometry"/></mxCell>')
    y = 152
    for i, (a, b, c_) in enumerate(SWAPS):
        vals = [a, b, c_]
        accs = ["red", "green", "teal"]
        for j in range(3):
            add(f'<mxCell id="s-r{i}c{j}" value="{S.esc(vals[j])}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent(accs[j])[0]};strokeWidth=1.4;shadow=1;fontSize=12;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;spacing=8;" vertex="1" parent="1"><mxGeometry x="{xs[j]}" y="{y}" width="{ws[j]}" height="64" as="geometry"/></mxCell>')
        y += 72
    sf_txt = "DERO is a general-purpose, private, decentralized application platform \u2014 the DHEBP stack, end to end."
    add(f'<mxCell id="s-f" value="{S.esc(sf_txt)}" style="text;html=1;align=center;fontSize=12.5;fontStyle=1;fontColor={S.accent("brand")[0]};" vertex="1" parent="1"><mxGeometry x="20" y="{y+16}" width="1880" height="20" as="geometry"/></mxCell>')
    return S.d_graph(1920, H2, cells)

if __name__ == "__main__":
    theme = sys.argv[1] if len(sys.argv) > 1 else "light"
    S.set_theme(theme)
    d = os.path.dirname(os.path.abspath(__file__))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device" background="{S.TH["bg0"]}">\n'
           f'  <diagram id="world" name="DERO Place in the Modern World">\n{S.inject_draft(build_page1())}\n  </diagram>\n'
           f'  <diagram id="swap" name="The Swap Table">\n{S.inject_draft(build_page2())}\n  </diagram>\n'
           '</mxfile>\n')
    with open(os.path.join(d, "DERO.WORLD.drawio"), "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"written OK (theme={theme})")
