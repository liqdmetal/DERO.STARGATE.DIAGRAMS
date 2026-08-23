#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DERO.MASTER.drawio — the DERO Universe, reskinned with the 'DHEBP Night'
template system (dero_style.py). Same content as DERO.UNIVERSE, new skin."""
import datetime, os
import dero_style as S

W, H = 2600, 1580

ENGINE = [
    ("Encrypted ledger", "homomorphic balances \u00b7 66 B/account \u00b7 never decrypted", "blue"),
    ("\u03a3-block PoW", "AstroBWTv3 \u00b7 18 s blocks \u00b7 9+1 mini-blocks \u00b7 network IS the pool", "blue"),
    ("DVM", "smart contracts in DVM-BASIC \u00b7 private state", "purple"),
    ("GravitonDB", "encrypted key/value \u00b7 merkle-proved \u00b7 prunable", "teal"),
    ("TLS P2P + erasure codes", "encrypted gossip \u00b7 blocks rebuilt from any 16 of 48 chunks", "blue"),
    ("6 bound proofs", "ring 8 \u00b7 bulletproofs \u00b7 provable without exposure", "purple"),
    ("Sound supply", "~20.89M hard cap \u00b7 halving every 4 years", "green"),
    ("No trusted setup", "open source \u00b7 auditable \u00b7 community-run", "gray"),
]
REPOS_GROUPS = [
    ("Core & wallets", "green", [
        ("DEROFDN/derohe", "community node \u2014 dev home"),
        ("DEROFDN/Engram", "smart wallet + TELA browser"),
        ("DHEBP/dhebp", "L1 private dApp platform"),
    ]),
    ("Build & index", "blue", [
        ("dSlate", "visual dApp builder"),
        ("Gnomon / HyperGnomon", "chain & TELA indexers"),
        ("xswd-api (JS/Go)", "wallet bridge clients"),
    ]),
    ("Web3 & media", "purple", [
        ("civilware/tela", "Decentralized Web Standard"),
        ("DHEBP/HOLOGRAM", "explore the DERO web"),
        ("DeroBeats", "music \u2014 EPOCH mining to artists"),
    ]),
    ("Mint & earn", "orange", [
        ("civilware/epoch", "Crowd Mining protocol"),
        ("tnn-miner", "open AstroBWTv3 miner"),
        ("cldex / dero_swap", "decentralized exchange"),
    ]),
]
USECASES = [
    ("Private payments", "send DERO \u2014 amount & identity hidden", "green"),
    ("Tokens & NFTs", "Artificer NFA \u00b7 Dero Seals \u00b7 Deroscapes", "green"),
    ("DEX & swaps", "cldex \u00b7 dero_swap \u00b7 ETH\u2194DERO bridge", "green"),
    ("Lotteries & games", "dero_lotto \u00b7 dreamtables", "orange"),
    ("On-chain web", "TELA sites \u00b7 no servers", "purple"),
    ("Sign-in & pay", "DeroAuth \u00b7 DeroPay", "green"),
    ("Marketplaces", "ORED \u00b7 deronfts", "orange"),
    ("Data & analytics", "Gnomon \u00b7 derohist \u00b7 derostats", "blue"),
    ("Crowdfunded apps", "EPOCH + DeroBeats + tela-gateway", "orange"),
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

ZONES = [
    ("engine", 60, 150, 1060, 430, 2, ENGINE, "blue", "1 \u00b7 THE ENGINE \u2014 DHEBP LAYER 1 (LIVE)", False),
    ("repos", 1160, 150, 1380, 430, 4, REPOS_GROUPS, "teal", "2 \u00b7 THE REPOS TODAY \u2014 CURATED", False),
    ("usecases", 60, 650, 2480, 300, 5, USECASES, "green", "3 \u00b7 LIVE USE CASES \u2014 WHAT YOU CAN DO TODAY", False),
    ("born", 60, 1010, 1260, 440, 2, BORN, "orange", "4 \u00b7 WHAT CAN BE BORN \u2014 END-WORLD RESULTS (HYPOTHETICAL)", True),
    ("spec", 1380, 1010, 1160, 440, 2, SPEC, "purple", "5 \u00b7 SPECULATION \u2014 NEW RAILS (NOT BUILT YET)", True),
]

def build_drawio():
    cells = []
    add = cells.append
    for c in S.d_header("u-t", 20, 22, 2560, "THE DERO UNIVERSE", "How to read: 1-3 = live today (solid) \u00b7 4 = what can be born \u00b7 5 = speculation (dashed) \u2014 deep dives in the other diagrams", font=34):
        add(c)
    for key, zx, zy, zw, zh, cols, content, acc, label, dashed in ZONES:
        for c in S.d_zone(f"z-{key}", zx, zy, zw, zh, acc, label, num=ZONES.index((key, zx, zy, zw, zh, cols, content, acc, label, dashed))+1, dashed=dashed, sub=None):
            add(c)
        if key == "repos":
            colw = (zw - 40 - 3 * 14) / 4
            for gi, (gname, gcol, items) in enumerate(content):
                gx = zx + 20 + gi * (colw + 14)
                for ii, (name, desc) in enumerate(items):
                    cy = zy + 66 + ii * (S.CHIP_H if hasattr(S, "CHIP_H") else 96)
                    for c in S.d_chip(f"rc{gi}-{ii}", gx, cy, colw, 96, gcol, name, desc, font=10.5):
                        add(c)
            more_label = S.esc("\U0001F4E6 40+ more projects \u2192 DERO.TELA.drawio p3")
            add(f'<mxCell id="z-repos-more" value="{more_label}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("teal")[0]};strokeWidth=1.2;dashed=1;fontSize=11;fontStyle=1;fontColor={S.accent("teal")[0]};align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="{zx+20}" y="{zy+zh-48}" width="{zw-40}" height="32" as="geometry"/></mxCell>')
        else:
            cols_n = cols
            inner_w = zw - 40
            gap = (inner_w - cols_n * 235) // (cols_n - 1) if cols_n > 1 else 0
            rows = (len(content) + cols_n - 1) // cols_n
            for i, item in enumerate(content):
                name, desc = item[0], item[1]
                r, c = divmod(i, cols_n)
                cx = zx + 20 + c * (235 + gap)
                cy = zy + 64 + r * 108
                db = dashed
                for chip in S.d_chip(f"c-{key}-{i}", cx, cy, 235, 92, acc, name, desc, font=10.5, dashed=db):
                    add(chip)
    # arrows
    for eid, p1, p2, label, acc, dashed in [
        ("a1", (700, 580), (1160, 580), "built by the community", "blue", False),
        ("a2", (2000, 580), (2000, 650), "enable", "teal", False),
        ("a3", (700, 950), (700, 1010), "grow into", "orange", False),
        ("a4", (2000, 950), (2000, 1010), "could lead to", "purple", True),
    ]:
        for c in S.d_arrow(eid, [p1, p2], accent_key=acc, label=label, dashed=dashed):
            add(c)
    # TL;DR
    add(f'<mxCell id="tldr" value="{S.esc("THE 30-SECOND VERSION")}" style="text;html=1;align=left;fontSize=15;fontStyle=1;fontColor={S.accent("brand")[0]};" vertex="1" parent="1"><mxGeometry x="60" y="1480" width="300" height="22" as="geometry"/></mxCell>')
    tldr_txt = "One encrypted ledger runs money, contracts and apps. The network mines itself (\u03a3-blocks, CPU-only). Apps live on-chain (TELA) and wallets approve every interaction (XSWD). EPOCH turns app usage into funding. Everything private \u2014 nothing to take down."
    add(f'<mxCell id="tldr-b" value="{S.esc(tldr_txt)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("brand")[0]};strokeWidth=1.5;shadow=1;fontSize=14;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="60" y="1508" width="2480" height="56" as="geometry"/></mxCell>')
    return S.d_graph(W, H, cells)

def build_svg():
    out = S.svg_open(W, H, "THE DERO UNIVERSE", "How to read: 1-3 = live today (solid) \u00b7 4 = what can be born \u00b7 5 = speculation (dashed)")
    for key, zx, zy, zw, zh, cols, content, acc, label, dashed in ZONES:
        num = ZONES.index((key, zx, zy, zw, zh, cols, content, acc, label, dashed)) + 1
        out += S.svg_zone(zx, zy, zw, zh, acc, label, num=num, dashed=dashed)
        if key == "repos":
            colw = (zw - 40 - 3 * 14) / 4
            for gi, (gname, gcol, items) in enumerate(content):
                gx = zx + 20 + gi * (colw + 14)
                for ii, (name, desc) in enumerate(items):
                    cy = zy + 66 + ii * 96
                    out += S.svg_chip(gx, cy, colw, 96, gcol, name, desc)
            out.append(f'<rect x="{zx+20}" y="{zy+zh-48}" width="{zw-40}" height="32" rx="8" fill="#18233D" stroke="{S.accent("teal")[0]}" stroke-width="1.2" stroke-dasharray="6 5"/>')
            more_txt = "\U0001F4E6 40+ more projects \u2192 DERO.TELA.drawio p3"
            out.append(f'<text x="{zx+zw/2}" y="{zy+zh-28}" text-anchor="middle" font-size="11" font-weight="700" fill="{S.accent("teal")[0]}">{more_txt}</text>')
        else:
            cols_n = cols
            inner_w = zw - 40
            gap = (inner_w - cols_n * 235) // (cols_n - 1) if cols_n > 1 else 0
            for i, item in enumerate(content):
                name, desc = item[0], item[1]
                r, c = divmod(i, cols_n)
                cx = zx + 20 + c * (235 + gap)
                cy = zy + 64 + r * 108
                out += S.svg_chip(cx, cy, 235, 92, acc, name, desc, dashed=dashed)
    for eid, p1, p2, label, acc, dashed in [
        ("a1", (700, 580), (1160, 580), "built by the community", "blue", False),
        ("a2", (2000, 580), (2000, 650), "enable", "teal", False),
        ("a3", (700, 950), (700, 1010), "grow into", "orange", False),
        ("a4", (2000, 950), (2000, 1010), "could lead to", "purple", True),
    ]:
        out += S.svg_arrow([p1, p2], accent_key=acc, label=label, dashed=dashed)
    out.append(f'<text x="60" y="1496" font-size="15" font-weight="700" fill="{S.accent("brand")[0]}">THE 30-SECOND VERSION</text>')
    out.append(f'<rect x="60" y="1508" width="2480" height="56" rx="12" fill="{S.TH["panel"]}" stroke="{S.accent("brand")[0]}" stroke-width="1.5"/>')
    out.append(f'<text x="1300" y="1540" text-anchor="middle" font-size="14" fill="{S.TH["ink"]}">One encrypted ledger runs money, contracts and apps. The network mines itself (\u03a3-blocks, CPU-only). Apps live on-chain (TELA) and wallets approve</text>')
    out += S.svg_draft(H)
    return S.svg_close(out)

if __name__ == "__main__":
    import sys
    theme = sys.argv[1] if len(sys.argv) > 1 else "dark"
    S.set_theme(theme)
    d = os.path.dirname(os.path.abspath(__file__))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device" background="{S.TH["bg0"]}">\n'
           f'  <diagram id="master" name="The DERO Universe (v2 skin)">\n{S.inject_draft(build_drawio())}\n  </diagram>\n'
           '</mxfile>\n')
    with open(os.path.join(d, "DERO.MASTER.drawio"), "w", encoding="utf-8") as f:
        f.write(xml)
    svg = build_svg()
    with open(os.path.join(d, f"preview_master_{theme}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    with open(os.path.join(d, f"preview_master_{theme}.html"), "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;background:{S.TH["bg0"]};}}</style></head><body>{svg}</body></html>')
    print(f"written OK (theme={theme})")
