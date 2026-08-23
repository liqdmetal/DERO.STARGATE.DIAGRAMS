#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DERO.MASTER.drawio — DERO Universe on the template system, TIGHT layout.

Sizing experiment (nothing committed until approved):
  - chips 185x72 (was 235x92) with 12px gaps
  - zone heights auto-computed from the chip grid (kills dead space)
  - zone headers compact (number badge inline in the strip, no circle below)
  - canvas auto-sized to content
  - light + dark themes via argv
"""
import datetime, os, sys
import dero_style as S

# --- content (same as before) ---
ENGINE = [
    ("Encrypted ledger", "homomorphic \u00b7 66 B/account \u00b7 never decrypted"),
    ("\u03a3-block PoW", "AstroBWTv3 \u00b7 18 s \u00b7 9+1 mini-blocks \u00b7 network IS the pool"),
    ("DVM", "DVM-BASIC contracts \u00b7 private state"),
    ("GravitonDB", "encrypted KV \u00b7 merkle-proved \u00b7 prunable"),
    ("TLS P2P + erasure", "encrypted gossip \u00b7 any 16 of 48 chunks rebuild"),
    ("6 bound proofs", "ring 8 \u00b7 bulletproofs \u00b7 provable"),
    ("Sound supply", "~20.89M cap \u00b7 halving ~4 yr"),
    ("No trusted setup", "open source \u00b7 auditable"),
]
REPOS_GROUPS = [
    ("Core & wallets", "green", [
        ("DEROFDN/derohe", "community node"),
        ("Engram", "smart wallet + TELA browser"),
        ("DHEBP/dhebp", "L1 private dApp platform"),
    ]),
    ("Build & index", "blue", [
        ("dSlate", "visual dApp builder"),
        ("Gnomon / HyperGnomon", "chain & TELA indexers"),
        ("xswd-api", "wallet bridge clients"),
    ]),
    ("Web3 & media", "purple", [
        ("civilware/tela", "Decentralized Web Std"),
        ("HOLOGRAM", "explore the DERO web"),
        ("DeroBeats", "music \u2014 EPOCH mining"),
    ]),
    ("Mint & earn", "orange", [
        ("civilware/epoch", "Crowd Mining"),
        ("tnn-miner", "open AstroBWTv3 miner"),
        ("cldex / dero_swap", "decentralized exchange"),
    ]),
]
USECASES = [
    ("Private payments", "amount & identity hidden"),
    ("Tokens & NFTs", "NFA \u00b7 Seals \u00b7 Deroscapes"),
    ("DEX & swaps", "cldex \u00b7 dero_swap \u00b7 ETH bridge"),
    ("Lotteries & games", "dero_lotto \u00b7 dreamtables"),
    ("On-chain web", "TELA sites \u00b7 no servers"),
    ("Sign-in & pay", "DeroAuth \u00b7 DeroPay"),
    ("Marketplaces", "ORED \u00b7 deronfts"),
    ("Data & analytics", "Gnomon \u00b7 derohist"),
    ("Crowdfunded apps", "EPOCH + DeroBeats"),
]
BORN = [
    ("Private banking", "self-custody, no freeze, no KYC wall"),
    ("Censorship-proof media", "encrypted social, unstoppable"),
    ("Encrypted health records", "private by default"),
    ("Private DAO ballots", "hidden votes, verifiable counts"),
    ("M2M payments", "agents & IoT paying each other"),
    ("Engagement economy", "EPOCH at scale, no ads"),
]
SPEC = [
    ("DERO-QR", "quantum-resistant upgrade"),
    ("Inter-contract calls", "contracts calling contracts"),
    ("Private DeFi suite", "lending, staking, AMMs"),
    ("Confidential compute", "logic over encrypted data"),
    ("L2s & sidechains", "scale, keep L1 privacy"),
    ("Universal crowd mining", "EPOCH as default rail"),
]

# chip grid constants — Option C: title-only chips, bigger type, glanceable
CW, CH = 210, 52
GAPX, GAPY = 12, 12
ZONE_HEADER = 54

def build_drawio():
    S.set_theme(THEME)
    cells = []
    add = cells.append
    # --- header ---
    for c in S.d_header("u-t", 20, 18, 2000, "THE DERO UNIVERSE",
                        "1-3 live (solid) \u00b7 4 what can be born \u00b7 5 speculation (dashed) \u2014 deep dives in the other diagrams", font=32):
        add(c)
    hdr_h = 84
    # --- layout ---
    margin = 40
    xL, xR = 20, 20
    wL = 990   # left column (engine, born)
    wR = 990   # right column (repos, spec)
    # usecases spans full width
    wU = 2000
    # engine: 2 cols x 4 rows
    eng_cols = 2
    eng_rows = (len(ENGINE) + eng_cols - 1) // eng_cols
    eng_h = S.d_zone_h(eng_rows, chip_h=CH, gap=GAPY, header=ZONE_HEADER)
    # repos: 4 col groups x 3 items, each item chip_h
    repos_h = S.d_zone_h(3, chip_h=CH, gap=GAPY, header=ZONE_HEADER) + 30  # +30 for group labels
    # usecases: 5 cols x 2 rows
    use_cols = 5
    use_rows = (len(USECASES) + use_cols - 1) // use_cols
    use_h = S.d_zone_h(use_rows, chip_h=CH, gap=GAPY, header=ZONE_HEADER)
    # born & spec: 2 cols x 3 rows
    born_rows = (len(BORN) + 1) // 2
    born_h = S.d_zone_h(born_rows, chip_h=CH, gap=GAPY, header=ZONE_HEADER)
    spec_h = S.d_zone_h(born_rows, chip_h=CH, gap=GAPY, header=ZONE_HEADER)

    # vertical layout
    GAP = 56
    y1 = 20 + hdr_h            # engine/repos row
    y2 = y1 + max(eng_h, repos_h) + GAP   # usecases
    y3 = y2 + use_h + GAP      # born/spec
    H = y3 + max(born_h, spec_h) + 80    # +TL;DR
    W = 20 + wU + 20

    # --- zones ---
    def zone(key, x, y, w, h, acc, label, num, dashed=False):
        for c in S.d_zone(f"z-{key}", x, y, w, h, acc, label, num=num, dashed=dashed, sub=None):
            add(c)
        return x, y, w, h

    zone("engine", xL, y1, wL, eng_h, "blue", "THE ENGINE \u2014 DHEBP L1 (LIVE)", 1)
    zone("repos",  xR + 20 + wL - 20, y1, wR, repos_h, "teal", "THE REPOS TODAY \u2014 CURATED", 2)
    zone("usecases", xL, y2, wU, use_h, "green", "LIVE USE CASES", 3)
    zone("born", xL, y3, wL, born_h, "orange", "WHAT CAN BE BORN (HYPOTHETICAL)", 4, dashed=True)
    zone("spec", xR + 20 + wL - 20, y3, wR, spec_h, "purple", "SPECULATION \u2014 NEW RAILS", 5, dashed=True)

    # --- chips ---
    def chips(zonekey, x, y, w, cols, items, acc, dashed, group_cols=None):
        if group_cols:  # repos grouped
            colw = (w - 24 - (group_cols - 1) * 12) / group_cols
            for gi, (gname, gcol, gitems) in enumerate(items):
                gx = x + 12 + gi * (colw + 12)
                add(f'<mxCell id="g-{gi}" value="{S.esc(gname)}" style="text;html=1;align=left;fontSize=11;fontStyle=1;fontColor={S.accent(gcol)[0]};" vertex="1" parent="1"><mxGeometry x="{gx}" y="{y+8}" width="{colw}" height="16" as="geometry"/></mxCell>')
                for ii, (name, desc) in enumerate(gitems):
                    cy = y + 30 + ii * (CH + GAPY)
                    for c in S.d_chip(f"{zonekey}-{gi}-{ii}", gx, cy, colw, CH, gcol, name, desc, font=9.5):
                        add(c)
        else:
            pos = S.d_chip_grid(x, y, w, cols, len(items), chip_w=CW, chip_h=CH, gap_x=GAPX, gap_y=GAPY, top=ZONE_HEADER - 4)
            for i, (name, desc) in enumerate(items):
                cx, cy = pos[i]
                for c in S.d_chip(f"{zonekey}-{i}", cx, cy, CW, CH, acc, name, desc, font=9.5, dashed=dashed):
                    add(c)

    chips("e", xL, y1, wL, 2, ENGINE, "blue", False)
    chips("r", xR + 20 + wL - 20, y1, wR, 0, REPOS_GROUPS, "teal", False, group_cols=4)
    chips("u", xL, y2, wU, 5, USECASES, "green", False)
    chips("b", xL, y3, wL, 2, BORN, "orange", True)
    chips("s", xR + 20 + wL - 20, y3, wR, 2, SPEC, "purple", True)

    # repos "more" pointer
    rx = xR + 20 + wL - 20; ry = y1 + repos_h - 30
    more_txt = S.esc("40+ more \u2192 DERO.TELA p3")
    add(f'<mxCell id="r-more" value="{more_txt}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("teal")[0]};strokeWidth=1;dashed=1;fontSize=10;fontStyle=1;fontColor={S.accent("teal")[0]};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="{rx+12}" y="{ry}" width="{wR-24}" height="22" as="geometry"/></mxCell>')

    # --- arrows (left col flow) ---
    for c in S.d_arrow("a1", [(xL+wL//2, y1+eng_h+8), (xL+wL//2, y2-8)], accent_key="blue", label="enable", width=3):
        add(c)
    for c in S.d_arrow("a3", [(xL+wL//2, y2+use_h+8), (xL+wL//2, y3-8)], accent_key="orange", label="grow into", width=3):
        add(c)
    for c in S.d_arrow("a4", [(xR+20+wL-20 + wR//2, y2+use_h+8), (xR+20+wL-20 + wR//2, y3-8)], accent_key="purple", label="could lead to", width=3, dashed=True):
        add(c)

    # --- TL;DR ---
    ty = y3 + max(born_h, spec_h) + 18
    add(f'<mxCell id="tldr" value="{S.esc("30-SECOND VERSION")}" style="text;html=1;align=left;fontSize=14;fontStyle=1;fontColor={S.accent("brand")[0]};" vertex="1" parent="1"><mxGeometry x="40" y="{ty}" width="260" height="20" as="geometry"/></mxCell>')
    tldr = "One encrypted ledger runs money, contracts and apps. The network mines itself (CPU-only). Apps live on-chain (TELA), wallets approve (XSWD), EPOCH funds usage. Private \u2014 nothing to take down."
    add(f'<mxCell id="tldr-b" value="{S.esc(tldr)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("brand")[0]};strokeWidth=1.5;shadow=1;fontSize=13;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="40" y="{ty+24}" width="{wU}" height="44" as="geometry"/></mxCell>')
    H = ty + 24 + 44 + 60

    return S.d_graph(W, H, cells), W, H

def build_svg():
    S.set_theme(THEME)
    # draw the tight layout directly to SVG (mirror of build_drawio geometry)
    CW, CH = 210, 52
    ZONE_HEADER = 54
    margin, hdr_h = 40, 84
    wL = wR = 990
    wU = 2000
    def zone_h(rows):
        return S.d_zone_h(rows, chip_h=CH, gap=12, header=ZONE_HEADER)
    eng_h = zone_h((len(ENGINE)+1)//2)
    repos_h = zone_h(3) + 30
    use_h = zone_h((len(USECASES)+4)//5)
    born_h = zone_h((len(BORN)+1)//2)
    spec_h = born_h
    GAP = 56  # room for arrows between rows
    y1 = hdr_h
    y2 = y1 + max(eng_h, repos_h) + GAP
    y3 = y2 + use_h + GAP
    ty = y3 + max(born_h, spec_h) + 18
    H = ty + 24 + 44 + 60
    W = 20 + wU + 20

    out = S.svg_open(W, H, "THE DERO UNIVERSE",
                     "1-3 live (solid) \u00b7 4 what can be born \u00b7 5 speculation (dashed)")
    def zone(key, x, y, w, h, acc, label, num, dashed=False):
        out.extend(S.svg_zone(x, y, w, h, acc, label, num=num, dashed=dashed))
    xR = 20 + 990 + 20
    zone("engine", 20, y1, wL, eng_h, "blue", "THE ENGINE \u2014 DHEBP L1 (LIVE)", 1)
    zone("repos", xR, y1, wR, repos_h, "teal", "THE REPOS TODAY \u2014 CURATED", 2)
    zone("usecases", 20, y2, wU, use_h, "green", "LIVE USE CASES", 3)
    zone("born", 20, y3, wL, born_h, "orange", "WHAT CAN BE BORN (HYPOTHETICAL)", 4, dashed=True)
    zone("spec", xR, y3, wR, spec_h, "purple", "SPECULATION \u2014 NEW RAILS", 5, dashed=True)
    # chips
    def chips(x, y, w, cols, items, acc, dashed):
        pos = S.d_chip_grid(x, y, w, cols, len(items), chip_w=CW, chip_h=CH, gap_x=12, gap_y=12, top=ZONE_HEADER-4)
        for i, (name, desc) in enumerate(items):
            cx, cy = pos[i]
            out.extend(S.svg_chip(cx, cy, CW, CH, acc, name, desc=None, dashed=dashed, font=11.5))
    def repos_chips(x, y, w):
        colw = (w - 24 - 3*12)/4
        for gi, (gname, gcol, gitems) in enumerate(REPOS_GROUPS):
            gx = x + 12 + gi*(colw+12)
            for ii, (name, desc) in enumerate(gitems):
                out.extend(S.svg_chip(gx, y+30+ii*(CH+12), colw, CH, gcol, name, desc=None, font=10.5))
    chips(20, y1, wL, 2, ENGINE, "blue", False)
    repos_chips(xR, y1, wR)
    chips(20, y2, wU, 5, USECASES, "green", False)
    chips(20, y3, wL, 2, BORN, "orange", True)
    chips(xR, y3, wR, 2, SPEC, "purple", True)
    # arrows
    out.extend(S.svg_arrow([(20+wL//2, y1+eng_h+8), (20+wL//2, y2-8)], accent_key="blue", label="enable"))
    out.extend(S.svg_arrow([(20+wL//2, y2+use_h+8), (20+wL//2, y3-8)], accent_key="orange", label="grow into"))
    out.extend(S.svg_arrow([(xR+wR//2, y2+use_h+8), (xR+wR//2, y3-8)], accent_key="purple", label="could lead to", dashed=True))
    # TL;DR
    out.append(f'<text x="40" y="{ty+16}" font-size="14" font-weight="700" fill="{S.accent("brand")[0]}">30-SECOND VERSION</text>')
    out.append(f'<rect x="40" y="{ty+24}" width="{wU}" height="44" rx="10" fill="{S.TH["panel"]}" stroke="{S.accent("brand")[0]}" stroke-width="1.5"/>')
    out.append(f'<text x="1040" y="{ty+52}" text-anchor="middle" font-size="13" fill="{S.TH["ink"]}">One encrypted ledger runs money, contracts and apps. The network mines itself (CPU-only). Apps live on-chain (TELA), wallets approve (XSWD), EPOCH funds usage. Private \u2014 nothing to take down.</text>')
    out.extend(S.svg_draft(H))
    return S.svg_close(out), W, H

if __name__ == "__main__":
    THEME = sys.argv[1] if len(sys.argv) > 1 else "light"
    S.set_theme(THEME)
    d = os.path.dirname(os.path.abspath(__file__))
    xml_graph, W, H = build_drawio()
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device" background="{S.TH["bg0"]}">\n'
           f'  <diagram id="master" name="The DERO Universe (tight)">\n{S.inject_draft(xml_graph)}\n  </diagram>\n'
           '</mxfile>\n')
    with open(os.path.join(d, "DERO.MASTER.drawio"), "w", encoding="utf-8") as f:
        f.write(xml)
    svg, W, H = build_svg()
    with open(os.path.join(d, f"preview_master_{THEME}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    with open(os.path.join(d, f"preview_master_{THEME}.html"), "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;background:{S.TH["bg0"]};}}</style></head><body>{svg}</body></html>')
    print(f"canvas {W}x{H} \u00b7 theme={THEME}")
