#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DERO EXPERIMENTS — real-world use-case field guide (experimental deep dive).
Page 1: 12 use-case cards (problem / DERO fit / status / try it).
Page 2: five-step ramp to run your own experiment + primitive cheat sheet.
Sources: derod.org corpus use-case taxonomy, community repos.
"""
import xml.sax.saxutils as sax
import datetime, html, re

TITLE_COLOR = "#4277BB"
INK, GRAY = "#22303C", "#5A6B7A"
STATUS = {"LIVE": ("#2E7D32", "\U0001F7E2 LIVE \u2014 USE IT TODAY"),
          "PARTIAL": ("#F9A825", "\U0001F7E1 PARTIAL \u2014 BUILD ON IT"),
          "EXP": ("#C62828", "\U0001F534 EXPERIMENTAL \u2014 PROTOTYPE IT")}
W, H = 1920, 1420

CARDS = [
    ("\U0001F3B0 Provably-fair gambling", "EXP",
     "Can you trust the casino\u2019s dice?",
     "DVM on-chain RANDOM() + private bets, hidden until reveal",
     "Fork SixofClubsss/Dero-Baccarat or the lottery.bas tutorial"),
    ("\U0001F3B5 Creator patronage", "LIVE",
     "Streaming pays artists cents; platforms sell your data",
     "DeroBeats: EPOCH mining to artists + instant DERO tips",
     "Use DeroBeats; register your own track on-chain"),
    ("\U0001F5F3\uFE0F Private DAO voting", "EXP",
     "Public ballots leak, get coerced, or get bought",
     "Encrypted SC state \u2014 votes hidden, counts verifiable",
     "Prototype: STORE votes + SIGNER(), reveal by threshold"),
    ("\U0001F3E6 Private lending & DeFi", "EXP",
     "Aave-style lending exposes your whole position",
     "Hidden collateral, encrypted positions, DVM escrow",
     "Build a collateralized-loan SC on the simulator"),
    ("\U0001F6D2 Anonymous marketplace", "PARTIAL",
     "Marketplaces know every buyer, seller, and price",
     "Private payments + TELA storefront + SC escrow",
     "Peppinux marketplace SC or wizard-grok/ORED"),
    ("\U0001F69A Supply chain, selective disclosure", "EXP",
     "Proving \u2018this is genuine\u2019 reveals your whole supplier network",
     "Reveal only what a buyer needs, prove it in math",
     "Sketch a provenance SC: STORE batch, signer proofs"),
    ("\U0001F4AC Censorship-proof social", "PARTIAL",
     "Platforms deplatform; posts vanish",
     "TELA hosting (no server) + DEchan boards + Hologram",
     "Open DEchan; publish your own TELA page"),
    ("\U0001F916 Machine-to-machine payments", "EXP",
     "No rails for devices paying devices (vending, EV, IoT)",
     "18 s finality, ~2.5 KB txs, dust-friendly",
     "Wallet RPC in a Pi script \u2014 auto-pay per use"),
    ("\U0001F393 Verifiable credentials", "PARTIAL",
     "Diplomas and IDs are forged; verification is slow",
     "DeroAuth + Name Service + signed claims on-chain",
     "Sign a credential claim; verify with DeroAuth"),
    ("\U0001F4B8 Private remittances", "PARTIAL",
     "Cross-border costs 5\u201310% and can be frozen",
     "Private ~1-min transfers, near-zero fees",
     "Send DERO wallet-to-wallet \u2014 no bank in the middle"),
    ("\U0001F6E1\uFE0F Parametric insurance", "EXP",
     "Claims need adjusters; payouts are slow and disputed",
     "DVM pays out by code when conditions are met (oracle)",
     "Model a flight-delay SC with an oracle entrypoint"),
    ("\U0001F3AE Play-to-earn, hidden inventories", "EXP",
     "Game economies leak: exploits, sniping, bots",
     "Encrypted game state \u2014 items & balances private",
     "Extend Dero-Baccarat with a private item registry"),
]

RAMP = [
    ("PICK A USE CASE", "From page 1 \u2014 or your own pain point. Write one sentence: \u2018I want X to happen without Y.\u2019", "blue"),
    ("MAP IT TO PRIMITIVES", "Money = DHEBP \u00b7 Logic = DVM \u00b7 State = GravitonDB \u00b7 UI = TELA \u00b7 Wallet = XSWD \u00b7 Funding = EPOCH \u00b7 Identity = DeroAuth/Name Service \u00b7 Privacy = zero-knowledge proofs", "teal"),
    ("RUN THE SIMULATOR", "derod --simulator spins up a local chain with pre-funded wallets \u2014 no risk, no cost, instant feedback.", "green"),
    ("START FROM EXISTING CODE", "Fork lottery.bas, Dero-Baccarat, the marketplace SC, DeroBeats, or a dSlate template \u2014 don\u2019t start from zero.", "orange"),
    ("DEPLOY & SHIP", "Testnet first (install_sc \u2192 SCID), then mainnet. Wire XSWD permissions (ask / accept_always / deny_always) and serve on TELA.", "purple"),
]

PRIMITIVES = [
    ("DHEBP \u00b7 L1", "money & settlement", "private payments, escrow, remittances"),
    ("DVM + DeroScript", "logic", "lotteries, loans, insurance, DAOs, markets"),
    ("GravitonDB", "encrypted state", "registries, inventories, credentials, votes"),
    ("TELA", "front-end", "storefronts, dashboards, uncensorable sites"),
    ("XSWD", "wallet bridge", "sign-in, pay, approve every dApp action"),
    ("EPOCH", "funding", "crowd mining \u2014 usage pays for the app"),
    ("Name Service", "identity", "human-readable addresses"),
    ("ZK proofs", "privacy", "prove without revealing \u2014 balance, age, origin"),
]

def esc(s):
    return sax.escape(s, {"'": "&apos;"})

def val(s):
    return s.replace("<", "&lt;").replace(">", "&gt;")

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

def card_value(name, status_key, problem, fit, tryit):
    sc, stxt = STATUS[status_key]
    return val(
        f"<b>{esc(name)}</b><br>"
        f"<font color=&quot;{sc}&quot;><b>{stxt}</b></font><br>"
        f"<font color=&quot;#5A6B7A&quot;>PROBLEM:</font> {esc(problem)}<br>"
        f"<font color=&quot;#5A6B7A&quot;>DERO:</font> {esc(fit)}<br>"
        f"<font color=&quot;#5A6B7A&quot;>TRY:</font> {esc(tryit)}")

def build_page1():
    cells = []
    add = cells.append
    add(f'<mxCell id="x-t1" value="REAL-WORLD USE CASES \u2014 THE EXPERIMENTAL FIELD GUIDE" style="text;html=1;align=center;fontSize=30;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="42" as="geometry"/></mxCell>')
    add(f'<mxCell id="x-t2" value="Twelve ways DERO could work in the real world \u2014 what problem each solves, which primitives fit, and where you can start building today.  Status: \U0001F7E2 live \u00b7 \U0001F7E1 partial \u00b7 \U0001F534 experimental.  Grounded in derod.org\u2019s use-case taxonomy + community repos." style="text;html=1;align=center;fontSize=13.5;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="68" width="1880" height="22" as="geometry"/></mxCell>')
    xs = [40, 700, 1360]
    ws = 640
    ys = [130, 430, 730, 1030]
    hs = 280
    for i, (name, status_key, problem, fit, tryit) in enumerate(CARDS):
        r, c = divmod(i, 3)
        x, y = xs[c], ys[r]
        add(f'<mxCell id="x-c{i}" value="{card_value(name, status_key, problem, fit, tryit)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={STATUS[status_key][0]};strokeWidth=2;verticalAlign=top;align=left;spacing=10;spacingTop=12;fontSize=10.5;fontColor={INK};" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{ws}" height="{hs}" as="geometry"/></mxCell>')
        sc, _ = STATUS[status_key]
        add(f'<mxCell id="x-bd{i}" value="{i+1}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={sc};strokeColor=#FFFFFF;strokeWidth=2;fontColor=#FFFFFF;fontSize=13;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="{x-15}" y="{y-15}" width="30" height="30" as="geometry"/></mxCell>')
    add(f'<mxCell id="x-f" value="Nothing here is a product claim \u2014 statuses are best-effort reads of what exists in the repos vs what is still an idea.  The point of this page is to give experiments a starting line." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F4F8FC;strokeColor={TITLE_COLOR};strokeWidth=1.5;fontSize=12;fontColor={GRAY};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="40" y="1330" width="1840" height="56" as="geometry"/></mxCell>')
    return f'<mxGraphModel dx="1400" dy="850" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel>"

def build_page2():
    cells = []
    add = cells.append
    add(f'<mxCell id="r-t1" value="RUN YOUR OWN EXPERIMENT \u2014 FIVE STEPS FROM IDEA TO ON-CHAIN" style="text;html=1;align=center;fontSize=28;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="40" as="geometry"/></mxCell>')
    add(f'<mxCell id="r-t2" value="The fastest path from \u2018what if\u2019 to a working contract. No funding, no permission, no trust required." style="text;html=1;align=center;fontSize=13.5;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    ACC = {"blue": "#1E88E5", "teal": "#00838F", "green": "#2E7D32", "orange": "#FB8C00", "purple": "#8E24AA"}
    y = 130
    for i, (title, body, color) in enumerate(RAMP):
        b = wrap(body, 1560 - 40, 12.5)
        btext = " ".join(b)
        step_html = f"<font color=&quot;{ACC[color]}&quot;><b>STEP {i+1} \u00b7 {esc(title)}</b></font><br>{esc(btext)}"
        add(f'<mxCell id="r-s{i}" value="{val(step_html)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={ACC[color]};strokeWidth=2;verticalAlign=top;align=left;spacing=10;spacingTop=14;fontSize=12.5;fontColor={INK};" vertex="1" parent="1"><mxGeometry x="60" y="{y}" width="1560" height="88" as="geometry"/></mxCell>')
        add(f'<mxCell id="r-bd{i}" value="{i+1}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={ACC[color]};strokeColor=#FFFFFF;strokeWidth=2;fontColor=#FFFFFF;fontSize=15;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="{60-15}" y="{y-15}" width="30" height="30" as="geometry"/></mxCell>')
        y += 100
    add(f'<mxCell id="r-h" value="WHEN TO REACH FOR WHICH PRIMITIVE" style="text;html=1;align=left;fontSize=17;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="60" y="{y}" width="600" height="26" as="geometry"/></mxCell>')
    y += 34
    for i, (name, role, when) in enumerate(PRIMITIVES):
        prim_html = f"<font color=&quot;{TITLE_COLOR}&quot;><b>{esc(name)}</b></font> <font color=&quot;#5A6B7A&quot;>\u2014 {esc(role)}</font><br><font color=&quot;#66727E&quot;>{esc(when)}</font>"
        add(f'<mxCell id="r-p{i}" value="{val(prim_html)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F4F8FC;strokeColor={TITLE_COLOR};strokeWidth=1.5;fontSize=12;fontColor={INK};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="{60 + (i%2)*940}" y="{y}" width="900" height="64" as="geometry"/></mxCell>')
        if i % 2 == 1:
            y += 74
    return f'<mxGraphModel dx="1400" dy="850" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1920" pageHeight="{y + 60}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel>"

def build_svg_p1():
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')
    A(f'<text x="{W/2}" y="52" text-anchor="middle" font-size="30" font-weight="700" fill="{TITLE_COLOR}">REAL-WORLD USE CASES \u2014 THE EXPERIMENTAL FIELD GUIDE</text>')
    A(f'<text x="{W/2}" y="84" text-anchor="middle" font-size="13.5" fill="{GRAY}">Twelve ways DERO could work in the real world \u2014 what problem each solves, which primitives fit, and where you can start building today.  Status: \U0001F7E2 live \u00b7 \U0001F7E1 partial \u00b7 \U0001F534 experimental.</text>')
    xs = [40, 700, 1360]; ws = 640; ys = [130, 430, 730, 1030]; hs = 280
    for i, (name, status_key, problem, fit, tryit) in enumerate(CARDS):
        r, c = divmod(i, 3)
        x, y, w, h = xs[c], ys[r], ws, hs
        sc, stxt = STATUS[status_key]
        A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="{sc}" stroke-width="2"/>')
        A(f'<circle cx="{x}" cy="{y}" r="15" fill="{sc}" stroke="#FFFFFF" stroke-width="2"/>')
        A(f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">{i+1}</text>')
        A(f'<text x="{x+14}" y="{y+26}" font-size="12.5" font-weight="700" fill="{INK}">{svg_esc(name)}</text>')
        A(f'<text x="{x+14}" y="{y+46}" font-size="10.5" font-weight="700" fill="{sc}">{svg_esc(stxt)}</text>')
        ty = y + 68
        A(f'<text x="{x+14}" y="{ty}" font-size="10.5" fill="{INK}"><tspan font-weight="700" fill="#5A6B7A">PROBLEM: </tspan>{svg_esc(problem)}</text>'); ty += 17
        for ln in wrap(fit, w - 28, 10.5):
            A(f'<text x="{x+14}" y="{ty}" font-size="10.5" fill="{INK}"><tspan font-weight="700" fill="#5A6B7A">DERO: </tspan>{svg_esc(ln)}</text>'); ty += 17
        for ln in wrap(tryit, w - 28, 10.5):
            A(f'<text x="{x+14}" y="{ty}" font-size="10.5" fill="{INK}"><tspan font-weight="700" fill="#5A6B7A">TRY: </tspan>{svg_esc(ln)}</text>'); ty += 17
    A(f'<rect x="40" y="1330" width="1840" height="56" rx="10" fill="#F4F8FC" stroke="{TITLE_COLOR}" stroke-width="1.5"/>')
    A(f'<text x="960" y="1360" text-anchor="middle" font-size="12" fill="{GRAY}">Nothing here is a product claim \u2014 statuses are best-effort reads of what exists in the repos vs what is still an idea. The point is to give experiments a starting line.</text>')
    A('</svg>')
    return "\n".join(out)

def build_svg_p2():
    out = []
    A = out.append
    H2 = 130 + 5 * 100 + 34 + 4 * 74 + 60
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="{H2}" viewBox="0 0 1920 {H2}" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<rect x="0" y="0" width="1920" height="{H2}" fill="#FFFFFF"/>')
    A(f'<text x="960" y="52" text-anchor="middle" font-size="28" font-weight="700" fill="{TITLE_COLOR}">RUN YOUR OWN EXPERIMENT \u2014 FIVE STEPS FROM IDEA TO ON-CHAIN</text>')
    A(f'<text x="960" y="82" text-anchor="middle" font-size="13.5" fill="{GRAY}">The fastest path from \u2018what if\u2019 to a working contract. No funding, no permission, no trust required.</text>')
    ACC = {"blue": "#1E88E5", "teal": "#00838F", "green": "#2E7D32", "orange": "#FB8C00", "purple": "#8E24AA"}
    y = 130
    for i, (title, body, color) in enumerate(RAMP):
        A(f'<rect x="60" y="{y}" width="1560" height="88" rx="10" fill="#FFFFFF" stroke="{ACC[color]}" stroke-width="2"/>')
        A(f'<circle cx="45" cy="{y+15}" r="15" fill="{ACC[color]}" stroke="#FFFFFF" stroke-width="2"/>')
        A(f'<text x="45" y="{y+20}" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">{i+1}</text>')
        A(f'<text x="80" y="{y+30}" font-size="13" font-weight="700" fill="{ACC[color]}">STEP {i+1} \u00b7 {svg_esc(title)}</text>')
        ty = y + 54
        for ln in wrap(body, 1500, 12.5):
            A(f'<text x="80" y="{ty}" font-size="12.5" fill="{INK}">{svg_esc(ln)}</text>'); ty += 17
        y += 100
    A(f'<text x="60" y="{y}" font-size="17" font-weight="700" fill="{TITLE_COLOR}">WHEN TO REACH FOR WHICH PRIMITIVE</text>')
    y += 34
    for i, (name, role, when) in enumerate(PRIMITIVES):
        A(f'<rect x="{60 + (i%2)*940}" y="{y}" width="900" height="64" rx="8" fill="#F4F8FC" stroke="{TITLE_COLOR}" stroke-width="1.5"/>')
        A(f'<text x="{70 + (i%2)*940}" y="{y+24}" font-size="12" font-weight="700" fill="{TITLE_COLOR}">{svg_esc(name)}</text>')
        A(f'<text x="{70 + (i%2)*940}" y="{y+44}" font-size="11" fill="#5A6B7A">\u2014 {svg_esc(role)}</text>')
        A(f'<text x="{70 + (i%2)*940}" y="{y+59}" font-size="10.5" fill="#66727E">{svg_esc(when)}</text>')
        if i % 2 == 1:
            y += 74
    A('</svg>')
    return "\n".join(out), y + 60

if __name__ == "__main__":
    import os
    d = os.path.dirname(os.path.abspath(__file__))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    p2, h2 = build_svg_p2()
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device">\n'
           f'  <diagram id="experiments" name="Experimental Field Guide">\n{inject_draft(build_page1())}\n  </diagram>\n'
           f'  <diagram id="ramp" name="Run Your Own Experiment">\n{inject_draft(build_page2())}\n  </diagram>\n'
           '</mxfile>\n')
    with open(os.path.join(d, "DERO.EXPERIMENTS.drawio"), "w", encoding="utf-8") as f:
        f.write(xml)
    svg1 = inject_draft_svg(build_svg_p1())
    svg2 = inject_draft_svg(p2)
    for name, svg in [("preview_experiments1.svg", svg1), ("preview_experiments2.svg", svg2)]:
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(svg)
        with open(os.path.join(d, name.replace(".svg", ".html")), "w", encoding="utf-8") as f:
            f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;}}</style></head><body>{svg}</body></html>')
    print("written OK")
