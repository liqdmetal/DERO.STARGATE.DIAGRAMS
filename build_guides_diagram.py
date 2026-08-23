#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DERO.GUIDES.drawio — onboarding & safety diagrams (3 pages).
Page 1: Where Do I Begin?  (one entry -> branch to the right diagram)
Page 2: Choose Your Wallet   (decision tree)
Page 3: Self-Custody Security Poster  (protect the seed, DERO has no recovery)
Tight template (dero_style) - light + dark via argv.
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
    header(cells, add, "WHERE DO I BEGIN?", "One entry point \u2192 branch to the right diagram.  Everything else in this set is a deep dive.")
    # start node
    add(f'<mxCell id="p1-start" value="{S.esc("I want to use DERO")}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={S.accent("brand")[0]};strokeColor=none;fontSize=15;fontStyle=1;fontColor=#FFFFFF;shadow=1;" vertex="1" parent="1"><mxGeometry x="790" y="100" width="220" height="60" as="geometry"/></mxCell>')
    branches = [
        ("Pay or receive money", "green", "Journey diagram \u2192 then the Wallet guide (p2)"),
        ("Mine & earn", "orange", "Mining diagram \u2192 then the Node runbook"),
        ("Build a dApp", "purple", "TELA diagram \u2192 then the DVM cheat-sheet"),
        ("Run a node / explorer", "blue", "Node runbook \u2192 then the Systems reference"),
        ("Just understand DERO", "teal", "The Universe map \u2192 then Journey \u2192 then this set"),
    ]
    bx = 120
    for i, (name, acc, deep) in enumerate(branches):
        x = 120 + i * 330
        add(f'<mxCell id="p1-b{i}" value="{S.esc(name)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent(acc)[0]};strokeWidth=1.5;shadow=1;fontSize=14;fontStyle=1;fontColor={S.accent(acc)[0]};align=center;verticalAlign=middle;spacing=8;" vertex="1" parent="1"><mxGeometry x="{x}" y="240" width="300" height="64" as="geometry"/></mxCell>')
        add(f'<mxCell id="p1-d{i}" value="{S.esc(deep)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent(acc)[0]};strokeWidth=1;dashed=1;fontSize=11;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;spacing=8;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y if False else 320}" width="300" height="80" as="geometry"/></mxCell>')
        for c in S.d_arrow(f"p1-a{i}", [(900, 160), (x+150, 240)], accent_key=acc, width=2.5):
            add(c)
    # footer note
    foot_txt = "Every diagram is a draft \u2014 not verified or audited. The links above tell you which page to open next; all files are editable draw.io."
    add(f'<mxCell id="p1-f" value="{S.esc(foot_txt)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("brand")[0]};strokeWidth=1.2;fontSize=13;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="120" y="700" width="1560" height="56" as="geometry"/></mxCell>')
    return S.d_graph(PAGE_W, PAGE_H, cells)

# ------------------------------------------------------------- page 2 -------
def page2():
    cells = []
    add = cells.append
    header(cells, add, "CHOOSE YOUR WALLET", "What matters most: GUI + dApps, a light CLI, or minimal.  All hold your keys locally \u2014 DERO has no recovery, so the seed backup on p3 is not optional.")
    q1 = ("Comfortable with a command line?", 60, 200)
    add(f'<mxCell id="p2-q1" value="{S.esc(q1[0])}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("amber")[0]};strokeWidth=1.8;fontSize=15;fontStyle=1;fontColor={S.accent("amber")[0]};align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="620" y="180" width="560" height="70" as="geometry"/></mxCell>')
    add(f'<mxCell id="p2-q1-y" value="{S.esc("YES")}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={S.accent("green")[0]};strokeColor=none;fontSize=13;fontStyle=1;fontColor=#FFFFFF;shadow=1;" vertex="1" parent="1"><mxGeometry x="1220" y="200" width="60" height="40" as="geometry"/></mxCell>')
    add(f'<mxCell id="p2-q1-n" value="{S.esc("NO")}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={S.accent("red")[0]};strokeColor=none;fontSize=13;fontStyle=1;fontColor=#FFFFFF;shadow=1;" vertex="1" parent="1"><mxGeometry x="1220" y="360" width="60" height="40" as="geometry"/></mxCell>')
    for c in S.d_arrow("p2-a1", [(900, 250), (1220, 220)], accent_key="green"):
        add(c)
    for c in S.d_arrow("p2-a2", [(900, 250), (1220, 380)], accent_key="red"):
        add(c)
    # YES branch -> CLI
    cli = ("CLI \u00b7 dero-wallet-cli", "text-based \u00b7 powerful \u00b7 great for miners/power users \u00b7 keys local", "green")
    add(f'<mxCell id="p2-cli" value="{S.esc(cli[0])}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent(cli[2])[0]};strokeWidth=2;fontSize=15;fontStyle=1;fontColor={S.accent(cli[2])[0]};align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="1330" y="150" width="380" height="60" as="geometry"/></mxCell>')
    add(f'<mxCell id="p2-cli-d" value="{S.esc(cli[1])}" style="text;html=1;align=center;fontSize=11;fontColor={S.TH["muted"]};whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="1330" y="214" width="380" height="40" as="geometry"/></mxCell>')
    # NO -> q2 GUI+dapps
    add(f'<mxCell id="p2-q2" value="{S.esc("Want a GUI + TELA dApps?")}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("amber")[0]};strokeWidth=1.8;fontSize=15;fontStyle=1;fontColor={S.accent("amber")[0]};align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="560" y="420" width="560" height="70" as="geometry"/></mxCell>')
    for c in S.d_arrow("p2-a3", [(1280, 380), (900, 420)], accent_key="blue"):
        add(c)
    add(f'<mxCell id="p2-q2-y" value="{S.esc("YES")}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={S.accent("green")[0]};strokeColor=none;fontSize=13;fontStyle=1;fontColor=#FFFFFF;shadow=1;" vertex="1" parent="1"><mxGeometry x="1160" y="440" width="60" height="40" as="geometry"/></mxCell>')
    add(f'<mxCell id="p2-q2-n" value="{S.esc("NO")}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={S.accent("red")[0]};strokeColor=none;fontSize=13;fontStyle=1;fontColor=#FFFFFF;shadow=1;" vertex="1" parent="1"><mxGeometry x="1160" y="600" width="60" height="40" as="geometry"/></mxCell>')
    for c in S.d_arrow("p2-a4", [(840, 490), (1160, 460)], accent_key="green"):
        add(c)
    for c in S.d_arrow("p2-a5", [(840, 490), (1160, 620)], accent_key="red"):
        add(c)
    engram = ("ENGRAM \u00b7 smart wallet", "GUI + TELA browser + XSWD \u00b7 best for dApps & everyday use", "purple")
    add(f'<mxCell id="p2-engram" value="{S.esc(engram[0])}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent(engram[2])[0]};strokeWidth=2;fontSize=15;fontStyle=1;fontColor={S.accent(engram[2])[0]};align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="1270" y="390" width="380" height="60" as="geometry"/></mxCell>')
    add(f'<mxCell id="p2-engram-d" value="{S.esc(engram[1])}" style="text;html=1;align=center;fontSize=11;fontColor={S.TH["muted"]};whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="1270" y="454" width="380" height="40" as="geometry"/></mxCell>')
    g45 = ("g45w \u00b7 light wallet", "simple \u00b7 node-agnostic \u00b7 good when you just send/receive", "teal")
    add(f'<mxCell id="p2-g45" value="{S.esc(g45[0])}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent(g45[2])[0]};strokeWidth=2;fontSize=15;fontStyle=1;fontColor={S.accent(g45[2])[0]};align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="1270" y="570" width="380" height="60" as="geometry"/></mxCell>')
    add(f'<mxCell id="p2-g45-d" value="{S.esc(g45[1])}" style="text;html=1;align=center;fontSize=11;fontColor={S.TH["muted"]};whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="1270" y="634" width="380" height="40" as="geometry"/></mxCell>')
    # bottom: all paths converge
    seed_txt = "Every wallet \u2192 write down your SEED \u2192 verify restore \u2192 send a tiny test tx first"
    add(f'<mxCell id="p2-seed" value="{S.esc(seed_txt)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.accent("green")[0]};strokeColor=none;fontSize=15;fontStyle=1;fontColor=#FFFFFF;align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="440" y="760" width="920" height="60" as="geometry"/></mxCell>')
    return S.d_graph(PAGE_W, PAGE_H, cells)

# ------------------------------------------------------------- page 3 -------
def page3():
    cells = []
    add = cells.append
    header(cells, add, "SELF-CUSTODY SECURITY POSTER", "DERO has NO recovery service \u2014 if you lose the seed or wallet password, the coins are gone forever.  This page is the difference between safe and sorry.")
    dos = [
        ("Write the seed on paper, offline", "never on a connected device"),
        ("Store 2-3 copies in separate places", "fire/flood/theft safe"),
        ("Test restoring from the seed once", "before putting real funds in"),
        ("Use a strong wallet password", "that you also can\u2019t forget"),
        ("Keep node + wallet on up-to-date releases", "and verify checksums / GPG"),
    ]
    donts = [
        ("Never type your seed into a website", "including \u201cverification\u201d sites"),
        ("Never screenshot or cloud-store it", "photos sync = exposure"),
        ("Never share it \u2014 support never asks", "support has no seed access"),
        ("Don\u2019t put big funds on a hot wallet", "use cold/offline storage"),
        ("Don\u2019t trust third-party \u201ccustody\u201d", "only you should hold keys"),
    ]
    # DO column
    add(f'<mxCell id="p3-do" value="{S.esc("DO")}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.accent("green")[0]};strokeColor=none;fontSize=18;fontStyle=1;fontColor=#FFFFFF;align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="120" y="130" width="220" height="46" as="geometry"/></mxCell>')
    for i, (t, d) in enumerate(dos):
        y = 190 + i * 100
        add(f'<mxCell id="p3-do{i}" value="{S.esc(t)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("green")[0]};strokeWidth=1.4;fontSize=13.5;fontStyle=1;fontColor={S.accent("green")[0]};align=left;verticalAlign=middle;spacing=12;shadow=1;" vertex="1" parent="1"><mxGeometry x="120" y="{y}" width="740" height="66" as="geometry"/></mxCell>')
        add(f'<mxCell id="p3-do{i}d" value="{S.esc(d)}" style="text;html=1;align=left;fontSize=11;fontColor={S.TH["muted"]};whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="136" y="{y+34}" width="700" height="30" as="geometry"/></mxCell>')
    # DON'T column
    dont_txt = "DON\u2019T"
    add(f'<mxCell id="p3-dont" value="{S.esc(dont_txt)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.accent("red")[0]};strokeColor=none;fontSize=18;fontStyle=1;fontColor=#FFFFFF;align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="940" y="130" width="220" height="46" as="geometry"/></mxCell>')
    for i, (t, d) in enumerate(donts):
        y = 190 + i * 100
        add(f'<mxCell id="p3-dont{i}" value="{S.esc(t)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("red")[0]};strokeWidth=1.4;fontSize=13.5;fontStyle=1;fontColor={S.accent("red")[0]};align=left;verticalAlign=middle;spacing=12;shadow=1;" vertex="1" parent="1"><mxGeometry x="940" y="{y}" width="740" height="66" as="geometry"/></mxCell>')
        add(f'<mxCell id="p3-dont{i}d" value="{S.esc(d)}" style="text;html=1;align=left;fontSize=11;fontColor={S.TH["muted"]};whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="956" y="{y+34}" width="700" height="30" as="geometry"/></mxCell>')
    # threat strip
    add(f'<mxCell id="p3-t" value="{S.esc("The threat model in one line")}" style="text;html=1;align=left;fontSize=14;fontStyle=1;fontColor={S.accent("amber")[0]};" vertex="1" parent="1"><mxGeometry x="120" y="720" width="300" height="20" as="geometry"/></mxCell>')
    threats = [("Phishing", "fake wallet sites & \u201csupport\u201d asking for seed"), ("Malware / keyloggers", "keep your OS clean, verify downloads"), ("Seed loss", "paper, metal, multiple copies \u2014 no recovery"), ("Custodian failure", "exchange hacks \u2014 self-custody avoids this")]
    for i, (name, desc) in enumerate(threats):
        x = 120 + i * 400
        add(f'<mxCell id="p3-t{i}" value="{S.esc(name)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("amber")[0]};strokeWidth=1.3;fontSize=13;fontStyle=1;fontColor={S.accent("amber")[0]};align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="{x}" y="748" width="360" height="56" as="geometry"/></mxCell>')
        add(f'<mxCell id="p3-t{i}d" value="{S.esc(desc)}" style="text;html=1;align=center;fontSize=10.5;fontColor={S.TH["muted"]};whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="{x}" y="808" width="360" height="40" as="geometry"/></mxCell>')
    return S.d_graph(PAGE_W, PAGE_H, cells)

if __name__ == "__main__":
    theme = sys.argv[1] if len(sys.argv) > 1 else "light"
    S.set_theme(theme)
    d = os.path.dirname(os.path.abspath(__file__))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device" background="{S.TH["bg0"]}">\n'
           f'  <diagram id="begin" name="Where Do I Begin">\n{S.inject_draft(page1())}\n  </diagram>\n'
           f'  <diagram id="wallet" name="Choose Your Wallet">\n{S.inject_draft(page2())}\n  </diagram>\n'
           f'  <diagram id="security" name="Self-Custody Security">\n{S.inject_draft(page3())}\n  </diagram>\n'
           '</mxfile>\n')
    with open(os.path.join(d, "DERO.GUIDES.drawio"), "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"written OK (theme={theme})")
