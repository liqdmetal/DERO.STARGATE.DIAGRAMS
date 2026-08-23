#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DERO.PRIVACY.drawio — honest privacy & economics diagrams (3 pages).
Page 1: What 'Private' Actually Means  (hidden vs visible, honest limits)
Page 2: Privacy Scorecard  (DERO vs BTC vs Monero vs ETH)
Page 3: DERO Economics    (emission, halving, cap, reward split)
Tight template - light + dark via argv.
"""
import datetime, os, sys
import dero_style as S

PAGE_W, PAGE_H = 1800, 1020

def header(cells, add, title, sub):
    for c in S.d_header("t", 40, 24, PAGE_W-80, title, sub, font=28):
        add(c)

# ------------------------------------------------------------- page 1 -------
def page1():
    cells = []
    add = cells.append
    header(cells, add, "WHAT \u2018PRIVATE\u2019 ACTUALLY MEANS",
           "Grounded in the code, not the marketing.  DERO hides amounts and identities strongly \u2014 but \u201cprivate\u201d is not \u201canonymous.\u201d")
    hidden = [
        ("Your balances", "homomorphically encrypted \u2014 66 B/account, never decrypted on-chain"),
        ("Transaction amounts", "encrypted; provable without revealing the value"),
        ("Who sent to whom", "ring signatures (ring 8) mask the true sender/receiver link"),
        ("Contract / dApp state", "DVM state is encrypted \u2014 only what you approve is visible"),
    ]
    visible = [
        ("Transaction time & size", "the chain stores when and how big \u2014 metadata is public"),
        ("Node IP / network layer", "TLS protects content, but your node\u2019s IP is visible to peers"),
        ("Your node sees your txs", "if you run a node, it knows your wallet\u2019s activity"),
        ("What a dApp is approved to see", "XSWD exposes exactly the methods you accept \u2014 review them"),
    ]
    hidden_t = "HIDDEN \u2014 by the protocol"
    visible_t = "VISIBLE \u2014 metadata & you"
    add(f'<mxCell id="pv-h" value="{S.esc(hidden_t)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.accent("green")[0]};strokeColor=none;fontSize=16;fontStyle=1;fontColor=#FFFFFF;align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="120" y="130" width="360" height="44" as="geometry"/></mxCell>')
    for i, (t, d) in enumerate(hidden):
        y = 190 + i * 120
        add(f'<mxCell id="pv-h{i}" value="{S.esc(t)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("green")[0]};strokeWidth=1.4;fontSize=14;fontStyle=1;fontColor={S.accent("green")[0]};align=left;verticalAlign=middle;spacing=12;shadow=1;" vertex="1" parent="1"><mxGeometry x="120" y="{y}" width="740" height="80" as="geometry"/></mxCell>')
        add(f'<mxCell id="pv-h{i}d" value="{S.esc(d)}" style="text;html=1;align=left;fontSize=11;fontColor={S.TH["muted"]};whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="136" y="{y+40}" width="700" height="36" as="geometry"/></mxCell>')
    add(f'<mxCell id="pv-v" value="{S.esc(visible_t)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.accent("amber")[0]};strokeColor=none;fontSize=16;fontStyle=1;fontColor=#FFFFFF;align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="940" y="130" width="360" height="44" as="geometry"/></mxCell>')
    for i, (t, d) in enumerate(visible):
        y = 190 + i * 120
        add(f'<mxCell id="pv-v{i}" value="{S.esc(t)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("amber")[0]};strokeWidth=1.4;fontSize=14;fontStyle=1;fontColor={S.accent("amber")[0]};align=left;verticalAlign=middle;spacing=12;shadow=1;" vertex="1" parent="1"><mxGeometry x="940" y="{y}" width="740" height="80" as="geometry"/></mxCell>')
        add(f'<mxCell id="pv-v{i}d" value="{S.esc(d)}" style="text;html=1;align=left;fontSize=11;fontColor={S.TH["muted"]};whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="956" y="{y+40}" width="700" height="36" as="geometry"/></mxCell>')
    # honest footer
    foot_txt = "THE HONEST VERSION: DERO\u2019s account model (encrypted balances, no key images, no UTXO decoys) is structurally less heuristic-attackable than Monero\u2019s \u2014 but metadata analysis, node-level observation, and poor op-sec still leak.  \u201cPrivate by default\u201d \u2260 \u201cuntraceable.\u201d"
    add(f'<mxCell id="pv-f" value="{S.esc(foot_txt)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("brand")[0]};strokeWidth=1.5;fontSize=13;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="120" y="700" width="1560" height="76" as="geometry"/></mxCell>')
    return S.d_graph(PAGE_W, PAGE_H, cells)

# ------------------------------------------------------------- page 2 -------
def page2():
    cells = []
    add = cells.append
    header(cells, add, "PRIVACY SCORECARD \u2014 DERO vs BTC vs MONERO vs ETH",
           "What each chain actually hides.  Honest about residual weaknesses on every side \u2014 no marketing.")
    chains = [
        ("BITCOIN", "amber", [
            ("Balances", "public \u2014 every UTXO value on-chain"),
            ("Amounts", "public"),
            ("Sender \u2192 receiver", "public \u2014 pseudonymous addresses"),
            ("Heuristic risk", "HIGH \u2014 change outputs & clustering de-anonymize"),
        ]),
        ("MONERO", "teal", [
            ("Balances", "hidden (RingCT commitments)"),
            ("Amounts", "hidden"),
            ("Sender \u2192 receiver", "masked (ring sigs, stealth addresses)"),
            ("Heuristic risk", "MEDIUM \u2014 decoy-selection heuristics still studied"),
        ]),
        ("DERO", "blue", [
            ("Balances", "hidden \u2014 homomorphic encryption, 66 B/account"),
            ("Amounts", "hidden \u2014 provable without revealing"),
            ("Sender \u2192 receiver", "masked (ring 8, account model)"),
            ("Heuristic risk", "LOWER \u2014 no key images, no UTXO decoys"),
        ]),
        ("ETHEREUM", "purple", [
            ("Balances", "public \u2014 account balances & ERC-20 all visible"),
            ("Amounts", "public"),
            ("Sender \u2192 receiver", "public"),
            ("Heuristic risk", "HIGH \u2014 fully transparent by design"),
        ]),
    ]
    # column headers
    for i, (name, acc, _) in enumerate(chains):
        add(f'<mxCell id="pc-h{i}" value="{S.esc(name)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.accent(acc)[0]};strokeColor=none;fontSize=15;fontStyle=1;fontColor=#FFFFFF;align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="{200+i*390}" y="130" width="360" height="44" as="geometry"/></mxCell>')
    # row labels
    rows = ["Balances", "Amounts", "Sender \u2192 receiver", "Heuristic risk"]
    for ri, rname in enumerate(rows):
        y = 190 + ri * 110
        add(f'<mxCell id="pc-r{ri}" value="{S.esc(rname)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("gray")[0]};strokeWidth=1.2;fontSize=12.5;fontStyle=1;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;spacing=8;" vertex="1" parent="1"><mxGeometry x="40" y="{y}" width="150" height="86" as="geometry"/></mxCell>')
    for ci, (name, acc, rows_data) in enumerate(chains):
        for ri, (_, cell) in enumerate(rows_data):
            y = 190 + ri * 110
            isrisk = (ri == 3)
            col = "red" if (isrisk and "HIGH" in cell) else ("amber" if (isrisk and "MEDIUM" in cell) else ("green" if (isrisk and "LOWER" in cell) else acc))
            add(f'<mxCell id="pc-c{ci}-{ri}" value="{S.esc(cell)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent(col)[0]};strokeWidth=1.3;fontSize=11.5;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;spacing=8;" vertex="1" parent="1"><mxGeometry x="{200+ci*390}" y="{y}" width="360" height="86" as="geometry"/></mxCell>')
    foot_txt = "DRAFT \u2014 a comparison like this needs a real crypto review before anyone quotes it.  The DERO column reflects the account-model argument (no key images / no UTXO decoys), but \u201clower heuristic risk\u201d is a claim, not a proof."
    add(f'<mxCell id="pc-f" value="{S.esc(foot_txt)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("red")[0]};strokeWidth=1.3;fontSize=12;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="40" y="650" width="1700" height="56" as="geometry"/></mxCell>')
    return S.d_graph(PAGE_W, PAGE_H, cells)

# ------------------------------------------------------------- page 3 -------
def page3():
    cells = []
    add = cells.append
    header(cells, add, "DERO ECONOMICS",
           "The coin-side companion to the mining diagram \u2014 emission, halving, cap, and the reward split.")
    econ = [
        ("HARD CAP", "~20,890,694 DERO", "the absolute maximum that can ever exist \u2014 sound supply", "green"),
        ("EMISSION", "via mining rewards", "all coins are mined \u2014 PoW (\u03a3-blocks), CPU-only", "blue"),
        ("HALVING", "every ~7,000,000 blocks", "\u2248 every 4 years, rewards halve \u2014 deflationary curve", "amber"),
        ("REWARD SPLIT", "88.4 / 10 / 1.6", "miners / [pool or integrator & ecosystem] \u2014 DRAFT: verify against source", "purple"),
        ("FEES", "paid in DERO", "per-tx fees + SC install/registration costs", "teal"),
    ]
    for i, (name, big, small, acc) in enumerate(econ):
        x = 120 + i * 340
        add(f'<mxCell id="pe-{i}" value="{S.esc(name)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent(acc)[0]};strokeWidth=1.6;fontSize=13.5;fontStyle=1;fontColor={S.accent(acc)[0]};align=center;verticalAlign=middle;spacing=8;shadow=1;" vertex="1" parent="1"><mxGeometry x="{x}" y="170" width="300" height="52" as="geometry"/></mxCell>')
        add(f'<mxCell id="pe-{i}b" value="{S.esc(big)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent(acc)[0]};strokeWidth=1.4;fontSize=15;fontStyle=1;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;spacing=8;shadow=1;" vertex="1" parent="1"><mxGeometry x="{x}" y="230" width="300" height="70" as="geometry"/></mxCell>')
        add(f'<mxCell id="pe-{i}d" value="{S.esc(small)}" style="text;html=1;align=center;fontSize=10.5;fontColor={S.TH["muted"]};whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="{x}" y="304" width="300" height="52" as="geometry"/></mxCell>')
    # emission curve note
    pe_f = "Why it matters: fixed supply + mining-only emission + periodic halving = a predictable, deflationary monetary base \u2014 the same properties people look for in \u2018sound money.\u2019 Numbers are DRAFT \u2014 the exact reward split and halving block height should be verified against derohe source before anyone cites them."
    add(f'<mxCell id="pe-f" value="{S.esc(pe_f)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("brand")[0]};strokeWidth=1.3;fontSize=13;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="120" y="640" width="1560" height="76" as="geometry"/></mxCell>')
    return S.d_graph(PAGE_W, PAGE_H, cells)

if __name__ == "__main__":
    theme = sys.argv[1] if len(sys.argv) > 1 else "light"
    S.set_theme(theme)
    d = os.path.dirname(os.path.abspath(__file__))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device" background="{S.TH["bg0"]}">\n'
           f'  <diagram id="private" name="What Private Actually Means">\n{S.inject_draft(page1())}\n  </diagram>\n'
           f'  <diagram id="scorecard" name="Privacy Scorecard">\n{S.inject_draft(page2())}\n  </diagram>\n'
           f'  <diagram id="economics" name="DERO Economics">\n{S.inject_draft(page3())}\n  </diagram>\n'
           '</mxfile>\n')
    with open(os.path.join(d, "DERO.PRIVACY.drawio"), "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"written OK (theme={theme})")
