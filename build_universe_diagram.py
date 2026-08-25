#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THE DERO UNIVERSE — digestible surfable map (v2).
Progressive disclosure: curated chips + reading path + pointers to deep dives.
Zones: 1 Engine (live) -> 2 Repos today -> 3 Live use cases
       4 What can be born (hypothetical) | 5 Speculation (future rails)
Solid = live today. Dashed = hypothetical / speculation.
"""
import xml.sax.saxutils as sax
import sys
import dero_style as S
S.set_theme(sys.argv[1] if len(sys.argv) > 1 else "light")
PANEL = S.TH["panel"]; PANEL2 = S.TH["panel2"]; BORDER = S.TH["border"]
BG0 = S.TH["bg0"]; MUTED = S.TH["muted"]
import datetime, html, re
import sys

TITLE_COLOR = S.TH["brand"]
INK, GRAY = S.TH["ink"], S.TH["muted"]
ZONE_COLORS = {
    "engine": (S.accent("blue")[0], S.TH["panel"], "THE ENGINE \u2014 DHEBP LAYER 1 (LIVE)"),
    "repos": (S.accent("teal")[0], S.TH["panel"], "THE REPOS TODAY \u2014 CURATED, FULL INDEX \u2192 DERO.TELA p3"),
    "usecases": (S.accent("green")[0], S.TH["panel"], "LIVE USE CASES \u2014 WHAT YOU CAN DO TODAY"),
    "born": (S.accent("amber")[0], S.TH["panel"], "WHAT CAN BE BORN \u2014 END-WORLD RESULTS (HYPOTHETICAL)"),
    "spec": (S.accent("purple")[0], S.TH["panel"], "SPECULATION \u2014 NEW RAILS (NOT BUILT YET)"),
}
W, H = 2600, 1580

ENGINE = [
    ("Encrypted ledger", "homomorphic balances \u00b7 66 B/account \u00b7 never decrypted"),
    ("\u03a3-block PoW", "AstroBWTv3 \u00b7 18 s blocks \u00b7 9+1 mini-blocks \u00b7 network IS the pool"),
    ("DVM", "smart contracts in DVM-BASIC \u00b7 private state"),
    ("GravitonDB", "encrypted key/value store \u00b7 merkle-proved \u00b7 prunable"),
    ("TLS P2P + erasure codes", "encrypted gossip \u00b7 blocks rebuilt from any 16 of 48 chunks"),
    ("6 bound proofs", "ring 8 \u00b7 bulletproofs \u00b7 provable without exposure"),
    ("Sound supply", "~20.89M hard cap \u00b7 halving every 4 years"),
    ("No trusted setup", "open source \u00b7 auditable \u00b7 community-run"),
]

REPOS_GROUPS = [
    ("Core & wallets", [
        ("DEROFDN/derohe", "community node \u2014 dev home"),
        ("DEROFDN/Engram", "smart wallet + TELA browser"),
        ("DHEBP/dhebp", "L1 private dApp platform"),
    ]),
    ("Build & index", [
        ("dSlate", "visual dApp builder"),
        ("Gnomon / HyperGnomon", "chain & TELA indexers"),
        ("xswd-api (JS/Go)", "wallet bridge clients"),
    ]),
    ("Web3 & media", [
        ("civilware/tela", "Decentralized Web Standard"),
        ("DHEBP/HOLOGRAM", "explore the DERO web"),
        ("DeroBeats", "music \u2014 EPOCH mining to artists"),
    ]),
    ("Mint & earn", [
        ("civilware/epoch", "Crowd Mining protocol"),
        ("tnn-miner", "open AstroBWTv3 miner"),
        ("cldex / dero_swap", "decentralized exchange"),
    ]),
]

USECASES = [
    ("Private payments", "send DERO \u2014 amount & identity hidden"),
    ("Tokens & NFTs", "Artificer NFA \u00b7 Dero Seals \u00b7 Deroscapes"),
    ("DEX & swaps", "cldex \u00b7 dero_swap \u00b7 ETH\u2194DERO bridge"),
    ("Lotteries & games", "dero_lotto \u00b7 dreamtables"),
    ("On-chain web", "TELA sites \u00b7 no servers"),
    ("Sign-in & pay", "DeroAuth \u00b7 DeroPay"),
    ("Marketplaces", "ORED \u00b7 deronfts"),
    ("Data & analytics", "Gnomon \u00b7 derohist \u00b7 derostats"),
    ("Crowdfunded apps", "EPOCH + DeroBeats + tela-gateway"),
]

BORN = [
    ("Private banking for the unbanked", "self-custody, no freeze, no KYC wall"),
    ("Censorship-proof media", "encrypted social that cannot be taken down"),
    ("Encrypted health records", "private by default, provable access"),
    ("Private DAO ballots", "encrypted votes, verifiable counts"),
    ("Machine-to-machine payments", "agents & IoT paying each other"),
    ("Engagement economy", "EPOCH at scale \u2014 apps funded by usage, no ads"),
]

SPEC = [
    ("DERO-QR", "quantum-resistant upgrade \u2014 stated plan"),
    ("Inter-contract calls", "smart contracts calling contracts"),
    ("Private DeFi suite", "lending, staking, AMMs, hidden amounts"),
    ("Confidential compute", "logic over encrypted data at scale"),
    ("L2s & sidechains", "scale while keeping L1 privacy"),
    ("Universal crowd mining", "EPOCH as the default monetization rail"),
]

# zones: (key, x, y, w, h, cols, chips_or_groups)
ZONES = [
    ("engine",   60,   150, 1060, 430, 2, ENGINE),
    ("repos",    1160, 150, 1380, 430, 4, REPOS_GROUPS),
    ("usecases", 60,   650, 2480, 300, 5, USECASES),
    ("born",     60,   1010, 1260, 440, 2, BORN),
    ("spec",     1380, 1010, 1160, 440, 2, SPEC),
]
NUM = {"engine": 1, "repos": 2, "usecases": 3, "born": 4, "spec": 5}

CHIP_W, CHIP_H = 235, 84

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

inject_draft = S.inject_draft
inject_draft_svg = lambda s: s

def chip_positions(zx, zy, zw, cols, count):
    inner = zw - 40
    gap = (inner - cols * CHIP_W) // (cols - 1) if cols > 1 else 0
    rows = (count + cols - 1) // cols
    pos = []
    for i in range(count):
        r, c = divmod(i, cols)
        pos.append((zx + 20 + c * (CHIP_W + gap), zy + 46 + r * (CHIP_H + 12)))
    return pos

def chip_value(name, desc, acc):
    return val(f"<font color=&quot;{acc}&quot;><b>{esc(name)}</b></font><br><font color=&quot;#66727E&quot;>{esc(desc)}</font>")

def build_page1():
    cells = []
    add = cells.append
    add(f'<mxCell id="u-t1" value="THE DERO UNIVERSE \u2014 ONE NETWORK, EVERYTHING ON IT" style="text;html=1;align=center;fontSize=34;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="24" width="2560" height="46" as="geometry"/></mxCell>')
    add(f'<mxCell id="u-read" value="\U0001F5FA\uFE0F HOW TO READ THIS MAP \u2014   \u2460 \u2461 \u2462 = what exists today (solid) \u00b7  \u2463 = what can be born from it \u00b7  \u2464 = rails that don&apos;t exist yet (dashed)   \u2014   deep dives: DERO.PROCESS.COMPLETE (tx) \u00b7 DERO.MINING (\u03a3-blocks) \u00b7 DERO.TELA p3 (full repo index)" style="rounded=1;whiteSpace=wrap;html=1;fillColor={PANEL};strokeColor={TITLE_COLOR};strokeWidth=1.5;fontSize=13;fontColor={INK};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="60" y="82" width="2480" height="44" as="geometry"/></mxCell>')

    for key, zx, zy, zw, zh, cols, content in ZONES:
        acc, tint, label = ZONE_COLORS[key]
        dashed = "dashed=1;" if key in ("born", "spec") else ""
        add(f'<mxCell id="u-z-{key}" value="" style="rounded=1;html=1;fillColor={tint};fillOpacity=35;strokeColor={acc};strokeWidth=2.5;{dashed}verticalAlign=top;" vertex="1" parent="1"><mxGeometry x="{zx}" y="{zy}" width="{zw}" height="{zh}" as="geometry"/></mxCell>')
        # big number badge + title
        add(f'<mxCell id="u-nb-{key}" value="{NUM[key]}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={acc};strokeColor=#FFFFFF;strokeWidth=2;fontColor=#FFFFFF;fontSize=18;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="{zx+16}" y="{zy+10}" width="36" height="36" as="geometry"/></mxCell>')
        add(f'<mxCell id="u-zt-{key}" value="{esc(label)}" style="text;html=1;align=left;fontSize=15;fontStyle=1;fontColor={acc};" vertex="1" parent="1"><mxGeometry x="{zx+62}" y="{zy+18}" width="{zw-80}" height="22" as="geometry"/></mxCell>')
        if key == "repos":
            # grouped columns: header + 3 chips per column
            col_w = (zw - 40 - 3 * 14) / 4
            for gi, (gname, items) in enumerate(content):
                gx = zx + 20 + gi * (col_w + 14)
                add(f'<mxCell id="u-g-{gi}" value="{esc(gname)}" style="text;html=1;align=left;fontSize=12;fontStyle=1;fontColor={acc};" vertex="1" parent="1"><mxGeometry x="{gx}" y="{zy+44}" width="{col_w}" height="20" as="geometry"/></mxCell>')
                for ii, (name, desc) in enumerate(items):
                    cy = zy + 66 + ii * (CHIP_H + 12)
                    add(f'<mxCell id="u-gc-{gi}-{ii}" value="{chip_value(name, desc, acc)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={PANEL};strokeColor={acc};strokeWidth=1.8;fontSize=10.5;fontColor={INK};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="{gx}" y="{cy}" width="{col_w}" height="{CHIP_H}" as="geometry"/></mxCell>')
            add(f'<mxCell id="u-gmore" value="\U0001F4E6 40+ more projects \u2192 DERO.TELA.drawio \u00b7 page 3 (full index)" style="rounded=1;whiteSpace=wrap;html=1;fillColor={PANEL};strokeColor={acc};strokeWidth=1.8;dashed=1;fontSize=11;fontStyle=1;fontColor={acc};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="{zx+20}" y="{zy+zh-52}" width="{zw-40}" height="36" as="geometry"/></mxCell>')
        elif key == "born":
            add(f'<mxCell id="u-bornmore" value="\U0001F9EA 12 experimental use cases + how to build them \u2192 DERO.EXPERIMENTS.drawio" style="rounded=1;whiteSpace=wrap;html=1;fillColor={PANEL};strokeColor={acc};strokeWidth=1.8;dashed=1;fontSize=11;fontStyle=1;fontColor={acc};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="{zx+20}" y="{zy+zh-52}" width="{zw-40}" height="36" as="geometry"/></mxCell>')
        else:
            for i, (name, desc) in enumerate(content):
                cx, cy = chip_positions(zx, zy, zw, cols, len(content))[i]
                db = "dashed=1;" if key in ("born", "spec") else ""
                add(f'<mxCell id="u-c-{key}-{i}" value="{chip_value(name, desc, acc)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={PANEL};strokeColor={acc};strokeWidth=1.8;{db}fontSize=10.5;fontColor={INK};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="{cx}" y="{cy}" width="{CHIP_W}" height="{CHIP_H}" as="geometry"/></mxCell>')

    # arrows
    def arrow(eid, p1, p2, label, dashed=False):
        db = "dashed=1;" if dashed else ""
        add(f'<mxCell id="{eid}" value="{esc(label)}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=classicThin;endFill=1;strokeColor={TITLE_COLOR};strokeWidth=3;{db}fontSize=12;fontStyle=1;fontColor={TITLE_COLOR};labelBackgroundColor={PANEL};" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{p1[0]}" y="{p1[1]}" as="sourcePoint"/><mxPoint x="{p2[0]}" y="{p2[1]}" as="targetPoint"/></mxGeometry></mxCell>')
    arrow("u-a1", (700, 580), (1160, 580), "built by the community")
    arrow("u-a2", (2000, 580), (2000, 650), "enable")
    arrow("u-a3", (700, 950), (700, 1010), "grow into")
    arrow("u-a4", (2000, 950), (2000, 1010), "could lead to", dashed=True)

    # TL;DR
    add(f'<mxCell id="u-tldr" value="THE 30-SECOND VERSION" style="text;html=1;align=left;fontSize=15;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="60" y="1485" width="300" height="22" as="geometry"/></mxCell>')
    add(f'<mxCell id="u-tldr2" value="One encrypted ledger runs money, contracts and apps. The network mines itself (\u03a3-blocks, CPU-only). Apps live on-chain (TELA) and wallets approve every interaction (XSWD). EPOCH turns app usage into funding. Everything private \u2014 nothing to take down." style="rounded=1;whiteSpace=wrap;html=1;fillColor={PANEL};strokeColor={TITLE_COLOR};strokeWidth=1.5;fontSize=14;fontColor={INK};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="60" y="1512" width="2480" height="52" as="geometry"/></mxCell>')

    return f'<mxGraphModel dx="1800" dy="1100" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" background="{BG0}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel>"

def build_svg():
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<defs><marker id="uar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{TITLE_COLOR}"/></marker></defs>')
    A(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')
    A(f'<text x="{W/2}" y="58" text-anchor="middle" font-size="34" font-weight="700" fill="{TITLE_COLOR}">THE DERO UNIVERSE \u2014 ONE NETWORK, EVERYTHING ON IT</text>')
    A(f'<rect x="60" y="82" width="2480" height="44" rx="10" fill="#F4F8FC" stroke="{TITLE_COLOR}" stroke-width="1.5"/>')
    A(f'<text x="1300" y="109" text-anchor="middle" font-size="13" fill="{INK}">\U0001F5FA\uFE0F HOW TO READ THIS MAP \u2014  \u2460 \u2461 \u2462 = what exists today (solid) \u00b7  \u2463 = what can be born from it \u00b7  \u2464 = rails that don\u2019t exist yet (dashed)   \u2014   deep dives: DERO.PROCESS.COMPLETE \u00b7 DERO.MINING \u00b7 DERO.TELA p3 (full index)</text>')
    for key, zx, zy, zw, zh, cols, content in ZONES:
        acc, tint, label = ZONE_COLORS[key]
        dash = 'stroke-dasharray="10 7"' if key in ("born", "spec") else ""
        A(f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" rx="14" fill="{tint}" fill-opacity="0.35" stroke="{acc}" stroke-width="2.5" {dash}/>')
        A(f'<circle cx="{zx+34}" cy="{zy+28}" r="18" fill="{acc}" stroke="#FFFFFF" stroke-width="2"/>')
        A(f'<text x="{zx+34}" y="{zy+34}" text-anchor="middle" font-size="18" font-weight="700" fill="#FFFFFF">{NUM[key]}</text>')
        A(f'<text x="{zx+62}" y="{zy+33}" font-size="15" font-weight="700" fill="{acc}">{svg_esc(label)}</text>')
        if key == "repos":
            col_w = (zw - 40 - 3 * 14) / 4
            for gi, (gname, items) in enumerate(content):
                gx = zx + 20 + gi * (col_w + 14)
                A(f'<text x="{gx}" y="{zy+58}" font-size="12" font-weight="700" fill="{acc}">{svg_esc(gname)}</text>')
                for ii, (name, desc) in enumerate(items):
                    cy = zy + 66 + ii * (CHIP_H + 12)
                    A(f'<rect x="{gx}" y="{cy}" width="{col_w}" height="{CHIP_H}" rx="9" fill="#FFFFFF" stroke="{acc}" stroke-width="1.8"/>')
                    A(f'<text x="{gx+col_w/2}" y="{cy+24}" text-anchor="middle" font-size="10.5" font-weight="700" fill="{acc}">{svg_esc(name)}</text>')
                    A(f'<text x="{gx+col_w/2}" y="{cy+44}" text-anchor="middle" font-size="9.5" fill="#66727E">{svg_esc(desc)}</text>')
            A(f'<rect x="{zx+20}" y="{zy+zh-52}" width="{zw-40}" height="36" rx="8" fill="#FFFFFF" stroke="{acc}" stroke-width="1.8" stroke-dasharray="6 5"/>')
            A(f'<text x="{zx+zw/2}" y="{zy+zh-29}" text-anchor="middle" font-size="11" font-weight="700" fill="{acc}">\U0001F4E6 40+ more projects \u2192 DERO.TELA.drawio \u00b7 page 3 (full index)</text>')
        elif key == "born":
            A(f'<rect x="{zx+20}" y="{zy+zh-52}" width="{zw-40}" height="36" rx="8" fill="#FFFFFF" stroke="{acc}" stroke-width="1.8" stroke-dasharray="6 5"/>')
            A(f'<text x="{zx+zw/2}" y="{zy+zh-29}" text-anchor="middle" font-size="11" font-weight="700" fill="{acc}">\U0001F9EA 12 experimental use cases + how to build them \u2192 DERO.EXPERIMENTS.drawio</text>')
        else:
            for i, (name, desc) in enumerate(content):
                cx, cy = chip_positions(zx, zy, zw, cols, len(content))[i]
                A(f'<rect x="{cx}" y="{cy}" width="{CHIP_W}" height="{CHIP_H}" rx="9" fill="#FFFFFF" stroke="{acc}" stroke-width="1.8" {dash}/>')
                A(f'<text x="{cx+CHIP_W/2}" y="{cy+24}" text-anchor="middle" font-size="10.5" font-weight="700" fill="{acc}">{svg_esc(name)}</text>')
                A(f'<text x="{cx+CHIP_W/2}" y="{cy+44}" text-anchor="middle" font-size="9.5" fill="#66727E">{svg_esc(desc)}</text>')
    # arrows
    A(f'<line x1="700" y1="580" x2="1160" y2="580" stroke="{TITLE_COLOR}" stroke-width="3" marker-end="url(#uar)"/>')
    A(f'<text x="930" y="572" text-anchor="middle" font-size="12" font-weight="600" fill="{TITLE_COLOR}" stroke="#FFF" stroke-width="3" paint-order="stroke">built by the community</text>')
    A(f'<line x1="2000" y1="580" x2="2000" y2="650" stroke="{TITLE_COLOR}" stroke-width="3" marker-end="url(#uar)"/>')
    A(f'<text x="2040" y="620" font-size="12" font-weight="600" fill="{TITLE_COLOR}" stroke="#FFF" stroke-width="3" paint-order="stroke">enable</text>')
    A(f'<line x1="700" y1="950" x2="700" y2="1010" stroke="{TITLE_COLOR}" stroke-width="3" marker-end="url(#uar)"/>')
    A(f'<text x="740" y="986" font-size="12" font-weight="600" fill="{TITLE_COLOR}" stroke="#FFF" stroke-width="3" paint-order="stroke">grow into</text>')
    A(f'<line x1="2000" y1="950" x2="2000" y2="1010" stroke="{TITLE_COLOR}" stroke-width="3" stroke-dasharray="10 7" marker-end="url(#uar)"/>')
    A(f'<text x="2040" y="986" font-size="12" font-weight="600" fill="{TITLE_COLOR}" stroke="#FFF" stroke-width="3" paint-order="stroke">could lead to</text>')
    A(f'<text x="60" y="1504" font-size="15" font-weight="700" fill="{TITLE_COLOR}">THE 30-SECOND VERSION</text>')
    A(f'<rect x="60" y="1512" width="2480" height="52" rx="10" fill="#F4F8FC" stroke="{TITLE_COLOR}" stroke-width="1.5"/>')
    A(f'<text x="1300" y="1532" text-anchor="middle" font-size="14" fill="{INK}">One encrypted ledger runs money, contracts and apps. The network mines itself (\u03a3-blocks, CPU-only). Apps live on-chain (TELA) and wallets</text>')
    A(f'<text x="1300" y="1552" text-anchor="middle" font-size="14" fill="{INK}">approve every interaction (XSWD). EPOCH turns app usage into funding. Everything private \u2014 nothing to take down.</text>')
    A('</svg>')
    return "\n".join(out)

if __name__ == "__main__":
    import os
    theme = sys.argv[1] if len(sys.argv) > 1 else "light"
    d = os.path.dirname(os.path.abspath(__file__))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device" background="{BG0}">\n'
           f'  <diagram id="universe" name="The DERO Universe">\n{inject_draft(build_page1())}\n  </diagram>\n'
           '</mxfile>\n')
    with open(os.path.join(d, "DERO.UNIVERSE.drawio"), "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"written OK (theme={theme})")
