#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THE DERO UNIVERSE — one big surfable map.
Zones: 1 The Engine (live protocol) -> 2 The Repos Today -> 3 Live Use Cases
       -> 4 What Can Be Born (hypothetical)  |  5 Speculation (future rails)
Solid borders = live today. Dashed = hypothetical / speculation.
"""
import xml.sax.saxutils as sax
import datetime, html

TITLE_COLOR = "#4277BB"
INK, GRAY = "#22303C", "#5A6B7A"
ZONE_COLORS = {
    "engine":   ("#1E88E5", "#E3F2FD", "1 \u00b7 THE ENGINE \u2014 DHEBP LAYER 1 (LIVE)"),
    "repos":    ("#00838F", "#E0F7FA", "2 \u00b7 THE REPOS TODAY \u2014 COMMUNITY BUILDERS"),
    "usecases": ("#2E7D32", "#E8F5E9", "3 \u00b7 LIVE USE CASES \u2014 WHAT YOU CAN DO TODAY"),
    "born":     ("#F9A825", "#FFF8E1", "4 \u00b7 WHAT CAN BE BORN \u2014 END-WORLD RESULTS (HYPOTHETICAL)"),
    "spec":     ("#8E24AA", "#F3E5F5", "5 \u00b7 SPECULATION \u2014 NEW RAILS (NOT BUILT YET)"),
}
W, H = 2600, 1720

ENGINE = [
    ("Encrypted ledger", "homomorphic balances, 66 B/account, never decrypted"),
    ("\u03a3-block PoW", "AstroBWTv3 \u00b7 18 s blocks \u00b7 9+1 mini-blocks \u00b7 network IS the pool"),
    ("DVM", "smart contracts in DVM-BASIC, private state"),
    ("GravitonDB", "encrypted key/value store, merkle-proved, prunable"),
    ("TLS P2P network", "encrypted gossip \u00b7 erasure-coded blocks (48\u219216 chunks)"),
    ("6 bound proofs", "ring 8 \u00b7 bulletproofs \u00b7 provability without exposure"),
    ("Sound supply", "~20.89M hard cap \u00b7 halving every 4 years"),
    ("No trusted setup", "open source, fully auditable, community-run"),
]
REPOS = [
    ("DEROFDN/derohe", "community-maintained node \u2014 active dev home"),
    ("DEROFDN/Engram", "smart wallet + TELA browser"),
    ("g45w", "universal wallet, mobile UI"),
    ("dero-am/astrobwt-miner", "community CPU miner"),
    ("dSlate (dMulti-c)", "visual dApp builder & tester"),
    ("Gnomon (civilware)", "local chain indexer"),
    ("dvm-basic-vscode", "DVM-BASIC language support"),
    ("dero-rpc-bridge", "safe wallet\u2194website bridge (Chrome)"),
    ("xswd-api (JS/Go)", "XSWD protocol clients"),
    ("DERO-SC-Standards", "community contract standards"),
    ("civilware/tela", "TELA \u2014 Decentralized Web Standard"),
    ("DHEBP/DeroPay", "accept DERO \u2014 payment stack"),
    ("DHEBP/DeroAuth", "log in with your DERO wallet"),
    ("DHEBP/HOLOGRAM", "explore the decentralized web"),
    ("SovereignSearch", "local TELA site discovery"),
    ("PureWolf ext", "browser \u2194 local TELA services"),
    ("TELATOMIC Swaps", "DERO \u2194 PulseChain atomic swaps"),
    ("dReam-dApps/dReams", "suite of on-chain services"),
]
USECASES = [
    ("Private payments", "send DERO \u2014 amount & identity hidden"),
    ("Tokens & NFTs", "Artificer NFA \u00b7 Dero Seals \u00b7 Deroscapes"),
    ("DEX & swaps", "cldex / dero_swap \u00b7 ETH\u2194DERO bridge"),
    ("Lotteries & games", "dero_lotto \u00b7 dreamtables baccarat & poker"),
    ("On-chain web", "TELA sites \u00b7 Hologram \u00b7 no servers"),
    ("Sign-in & pay", "DeroAuth \u00b7 DeroPay \u00b7 no passwords"),
    ("Marketplaces & assets", "ORED asset manager \u00b7 deronfts"),
    ("Data & analytics", "Gnomon \u00b7 derohist \u00b7 derostats"),
]
BORN = [
    ("Private banking for the unbanked", "self-custody money \u2014 no gatekeeper, no freeze, no KYC wall"),
    ("Censorship-proof media", "encrypted social & publishing that cannot be taken down"),
    ("Encrypted health records", "private by default, provable access, patient-controlled"),
    ("DAO governance, private ballots", "encrypted votes, verifiable counts, no coercion"),
    ("Insurance & prediction pools", "DVM escrow \u2014 payouts by code, not by adjuster"),
    ("Tokenized real-world assets", "ownership on-chain, private, transferable"),
    ("Machine-to-machine payments", "agents & IoT paying each other in DERO"),
    ("Instant global remittances", "private, near-free, no correspondent banks"),
]
SPEC = [
    ("DERO-QR", "quantum-resistant upgrade \u2014 Captain\u2019s stated plan; GravitonDB as migration substrate"),
    ("Inter-contract calls", "smart contracts calling smart contracts (community-testnet idea)"),
    ("Private DeFi suite", "lending, staking, AMMs with hidden amounts"),
    ("Confidential compute", "running logic over encrypted data at scale"),
    ("L2s & sidechains", "scaling rails that keep L1 privacy (repo\u2019s stated future)"),
    ("TELA social networks", "web3 social at wallet scale, no ads surveillance"),
    ("IoT micropayments", "machines transacting dust amounts, automatically"),
    ("Encrypted AI marketplaces", "private data in, private models out"),
]

ZONES = [
    ("engine",   60,   150, 1060, 430, 2, ENGINE),
    ("repos",    1160, 150, 1380, 430, 3, REPOS),
    ("usecases", 60,   640, 2480, 300, 4, USECASES),
    ("born",     60,   1020, 1260, 560, 2, BORN),
    ("spec",     1380, 1020, 1160, 560, 2, SPEC),
]

def esc(s):
    return sax.escape(s, {"'": "&apos;"})

def val(s):
    return s.replace("<", "&lt;").replace(">", "&gt;")

def svg_esc(s):
    return html.escape(s)

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

CHIP_W, CHIP_H = 235, 92

def chip_positions(zone, count):
    key, zx, zy, zw, zh, cols, _ = zone
    inner_w = zw - 40
    cw = CHIP_W
    gap = (inner_w - cols * cw) // (cols - 1) if cols > 1 else 0
    rows = (count + cols - 1) // cols
    pos = []
    for i in range(count):
        r, c = divmod(i, cols)
        pos.append((zx + 20 + c * (cw + gap), zy + 46 + r * (CHIP_H + 14)))
    return pos

def build_page1():
    cells = []
    add = cells.append
    add(f'<mxCell id="u-t1" value="THE DERO UNIVERSE \u2014 ONE NETWORK, EVERYTHING ON IT" style="text;html=1;align=center;fontSize=34;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="24" width="2560" height="46" as="geometry"/></mxCell>')
    add(f'<mxCell id="u-t2" value="From the DHEBP engine, through the community\u2019s repos today, to the world they can grow into.  Solid borders = live now \u00b7 dashed borders = hypothetical / speculation.  Grounded in derod.org + the derohe repos." style="text;html=1;align=center;fontSize=14.5;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="74" width="2560" height="24" as="geometry"/></mxCell>')
    # zone containers + chips
    for key, zx, zy, zw, zh, cols, chips in ZONES:
        acc, tint, label = ZONE_COLORS[key]
        dashed = "dashed=1;" if key in ("born", "spec") else ""
        add(f'<mxCell id="u-z-{key}" value="" style="rounded=1;html=1;fillColor={tint};fillOpacity=35;strokeColor={acc};strokeWidth=2.5;{dashed}verticalAlign=top;" vertex="1" parent="1"><mxGeometry x="{zx}" y="{zy}" width="{zw}" height="{zh}" as="geometry"/></mxCell>')
        add(f'<mxCell id="u-zt-{key}" value="{esc(label)}" style="text;html=1;align=left;fontSize=16;fontStyle=1;fontColor={acc};" vertex="1" parent="1"><mxGeometry x="{zx+18}" y="{zy+12}" width="{zw-36}" height="24" as="geometry"/></mxCell>')
        for i, (name, desc) in enumerate(chips):
            cx, cy = chip_positions((key, zx, zy, zw, zh, cols, chips), len(chips))[i]
            db = "dashed=1;" if key in ("born", "spec") else ""
            dlines = wrap(desc, CHIP_W - 16, 9.5)
            desc_text = " ".join(dlines)
            add(f'<mxCell id="u-c-{key}-{i}" value="{val(f"<font color=&quot;{acc}&quot;><b>{esc(name)}</b></font><br><font color=&quot;#66727E&quot;>{esc(desc_text)}</font>")}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={acc};strokeWidth=1.8;{db}fontSize=10.5;fontColor={INK};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="{cx}" y="{cy}" width="{CHIP_W}" height="{CHIP_H}" as="geometry"/></mxCell>')
    # arrows between zones
    def arrow(eid, p1, p2, label, dashed=False):
        db = "dashed=1;" if dashed else ""
        add(f'<mxCell id="{eid}" value="{esc(label)}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=classicThin;endFill=1;strokeColor={TITLE_COLOR};strokeWidth=3;{db}fontSize=12;fontStyle=1;fontColor={TITLE_COLOR};labelBackgroundColor=#FFFFFF;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{p1[0]}" y="{p1[1]}" as="sourcePoint"/><mxPoint x="{p2[0]}" y="{p2[1]}" as="targetPoint"/><Array as="points">{""}</Array></mxGeometry></mxCell>')
    arrow("u-a1", (700, 580), (1200, 580), "built by the community")          # engine -> repos
    arrow("u-a2", (2000, 580), (2000, 640), "enable")                          # repos -> use cases
    arrow("u-a3", (700, 940), (700, 1020), "grow into")                        # use cases -> born
    arrow("u-a4", (2000, 940), (2000, 1020), "could lead to", dashed=True)     # use cases -> spec
    return f'<mxGraphModel dx="1800" dy="1100" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel>"

def build_svg():
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<defs><marker id="uar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{TITLE_COLOR}"/></marker></defs>')
    A(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')
    A(f'<text x="{W/2}" y="60" text-anchor="middle" font-size="34" font-weight="700" fill="{TITLE_COLOR}">THE DERO UNIVERSE \u2014 ONE NETWORK, EVERYTHING ON IT</text>')
    A(f'<text x="{W/2}" y="92" text-anchor="middle" font-size="14.5" fill="{GRAY}">From the DHEBP engine, through the community\u2019s repos today, to the world they can grow into.  Solid borders = live now \u00b7 dashed borders = hypothetical / speculation.  Grounded in derod.org + the derohe repos.</text>')
    for key, zx, zy, zw, zh, cols, chips in ZONES:
        acc, tint, label = ZONE_COLORS[key]
        dash = 'stroke-dasharray="10 7"' if key in ("born", "spec") else ""
        A(f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" rx="14" fill="{tint}" fill-opacity="0.35" stroke="{acc}" stroke-width="2.5" {dash}/>')
        A(f'<text x="{zx+18}" y="{zy+32}" font-size="16" font-weight="700" fill="{acc}">{svg_esc(label)}</text>')
        for i, (name, desc) in enumerate(chips):
            cx, cy = chip_positions((key, zx, zy, zw, zh, cols, chips), len(chips))[i]
            A(f'<rect x="{cx}" y="{cy}" width="{CHIP_W}" height="{CHIP_H}" rx="9" fill="#FFFFFF" stroke="{acc}" stroke-width="1.8" {dash}/>')
            A(f'<text x="{cx+CHIP_W/2}" y="{cy+24}" text-anchor="middle" font-size="10.5" font-weight="700" fill="{acc}">{svg_esc(name)}</text>')
            dy = cy + 42
            for ln in wrap(desc, CHIP_W - 16, 9.5):
                A(f'<text x="{cx+CHIP_W/2}" y="{dy}" text-anchor="middle" font-size="9.5" fill="#66727E">{svg_esc(ln)}</text>')
                dy += 14
    # arrows
    A(f'<line x1="700" y1="580" x2="1160" y2="580" stroke="{TITLE_COLOR}" stroke-width="3" marker-end="url(#uar)"/>')
    A(f'<text x="930" y="566" text-anchor="middle" font-size="12" font-weight="600" fill="{TITLE_COLOR}" stroke="#FFF" stroke-width="3" paint-order="stroke">built by the community</text>')
    A(f'<line x1="2000" y1="580" x2="2000" y2="640" stroke="{TITLE_COLOR}" stroke-width="3" marker-end="url(#uar)"/>')
    A(f'<text x="2040" y="616" font-size="12" font-weight="600" fill="{TITLE_COLOR}" stroke="#FFF" stroke-width="3" paint-order="stroke">enable</text>')
    A(f'<line x1="700" y1="940" x2="700" y2="1020" stroke="{TITLE_COLOR}" stroke-width="3" marker-end="url(#uar)"/>')
    A(f'<text x="740" y="986" font-size="12" font-weight="600" fill="{TITLE_COLOR}" stroke="#FFF" stroke-width="3" paint-order="stroke">grow into</text>')
    A(f'<line x1="2000" y1="940" x2="2000" y2="1020" stroke="{TITLE_COLOR}" stroke-width="3" stroke-dasharray="10 7" marker-end="url(#uar)"/>')
    A(f'<text x="2040" y="986" font-size="12" font-weight="600" fill="{TITLE_COLOR}" stroke="#FFF" stroke-width="3" paint-order="stroke">could lead to</text>')
    A('</svg>')
    return "\n".join(out)

if __name__ == "__main__":
    import os
    d = os.path.dirname(os.path.abspath(__file__))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device">\n'
           f'  <diagram id="universe" name="The DERO Universe">\n{inject_draft(build_page1())}\n  </diagram>\n'
           '</mxfile>\n')
    with open(os.path.join(d, "DERO.UNIVERSE.drawio"), "w", encoding="utf-8") as f:
        f.write(xml)
    svg = inject_draft_svg(build_svg())
    with open(os.path.join(d, "preview_universe.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    with open(os.path.join(d, "preview_universe.html"), "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;}}</style></head><body>{svg}</body></html>')
    print("written OK")
