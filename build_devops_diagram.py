#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DERO.DEVOPS.drawio — operator & builder reference diagrams (4 pages).
Page 1: Node Operator Runbook
Page 2: XSWD Permission Model  (dApp <-> wallet)
Page 3: DVM-BASIC Cheat-Sheet
Page 4: Bridges & Interop
Tight template - light + dark via argv.
"""
import datetime, os, sys
import dero_style as S

PAGE_W, PAGE_H = 1800, 1020

def header(cells, add, title, sub):
    for c in S.d_header("t", 40, 24, PAGE_W-80, title, sub, font=28):
        add(c)

def box(cells, add, x, y, w, h, acc, title, desc=None, dashed=False, font=13, tfont=13.5, bold=True):
    db = "dashed=1;" if dashed else ""
    v = f"<font color=&quot;{S.accent(acc)[0]}&quot;><b>{S.esc(title)}</b></font>"
    if desc:
        v += f"<br><font color=&quot;{S.TH['muted']}&quot;>{S.esc(desc)}</font>"
    add(f'<mxCell id="b-{len(cells)}" value="{S.val(v)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent(acc)[0]};strokeWidth=1.4;{db}fontSize={font};fontColor={S.TH["ink"]};align=center;verticalAlign=middle;spacing=8;shadow=1;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

def txt(cells, add, x, y, w, acc, t, font=12):
    add(f'<mxCell id="t-{len(cells)}" value="{S.esc(t)}" style="text;html=1;align=left;fontSize={font};fontStyle=1;fontColor={S.accent(acc)[0]};whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{font+8}" as="geometry"/></mxCell>')

# ------------------------------------------------------------- page 1 -------
def page1():
    cells = []
    add = cells.append
    header(cells, add, "NODE OPERATOR RUNBOOK", "From download to a healthy, updated full node.  Each step is a box \u2014 follow top to bottom.")
    steps = [
        ("1 \u00b7 Download", "official release (DEROFDN/derohe) \u00b7 verify sha512 + GPG signature", "blue"),
        ("2 \u00b7 Configure", "--p2p-bind=0.0.0.0:10101 (pin it) \u00b7 keep RPC 10102 local", "blue"),
        ("3 \u00b7 Sync", "start derod \u00b7 fast-sync with a recent snapshot \u00b7 watch status", "teal"),
        ("4 \u00b7 Serve", "open only the P2P port in the firewall \u00b7 never expose RPC", "green"),
        ("5 \u00b7 Monitor", "derod status \u00b7 chain height \u00b7 peer count \u00b7 disk usage", "green"),
        ("6 \u00b7 Update", "new release \u2192 stop \u2192 backup data-dir \u2192 swap binary \u2192 restart", "amber"),
        ("7 \u00b7 Hard-Fork readiness", "HF3 activated at block 7,504,640 \u2014 run Release153+ to stay in sync (Release153 fixed false-parity sync)", "red"),
        ("8 \u00b7 Troubleshoot", "clock drift \u2192 install chrony \u00b7 MBR rising \u2192 check miner + time sync", "red"),
        ("9 \u00b7 Backup", "data-dir copy off-host \u00b7 wallet seeds separate from node", "purple"),
    ]
    for i, (t, d, acc) in enumerate(steps):
        y = 130 + i * 78
        box(cells, add, 120, y, 1560, 62, acc, t, d)
    return S.d_graph(PAGE_W, PAGE_H, cells)

# ------------------------------------------------------------- page 2 -------
def page2():
    cells = []
    add = cells.append
    header(cells, add, "XSWD \u2014 HOW dApps TALK TO YOUR WALLET", "Decentralized web apps get NO direct access to your keys \u2014 every interaction is a permissioned request through the wallet.")
    # flow
    box(cells, add, 120, 140, 340, 90, "purple", "dApp / TELA page", "wants to read balance, sign a tx, or call a smart contract")
    box(cells, add, 720, 140, 340, 90, "teal", "XSWD bridge", "WebSocket \u00b7 routes the request to your wallet \u00b7 nothing else")
    box(cells, add, 1320, 140, 340, 90, "green", "Your wallet", "pops up a permission request \u2014 YOU decide")
    for c in S.d_arrow("x1", [(460, 185), (720, 185)], accent_key="blue", label="ask", width=2.5):
        add(c)
    for c in S.d_arrow("x2", [(1060, 185), (1320, 185)], accent_key="blue", label="request", width=2.5):
        add(c)
    # permissions
    box(cells, add, 120, 320, 1560, 50, "amber", "You choose per request:  ASK  \u00b7  ACCEPT ALWAYS  \u00b7  DENY ALWAYS", "never hand a dApp \u2018accept always\u2019 you don\u2019t trust")
    # what methods
    txt(cells, add, 120, 410, 900, "blue", "WHAT XSWD CAN EXPOSE (methods you approve one by one)")
    methods = [
        ("get_info / get_balance", "read balances & chain info"),
        ("transfer / sc_invoke", "sign a transfer or smart-contract call"),
        ("install_sc", "deploy a new smart contract"),
        ("register_address / name service", "manage your DERO identity"),
    ]
    for i, (m, d) in enumerate(methods):
        y = 452 + i * 70
        box(cells, add, 120, y, 780, 54, "blue", m, d, font=12)
    txt(cells, add, 980, 410, 700, "red", "SECURITY RULES")
    rules = [
        ("Only approve what you\u2019re using", "a dApp can only do what you allow"),
        ("Prefer ASK over ACCEPT ALWAYS", "one-time approval, not standing access"),
        ("Check the method + SCID", "make sure it\u2019s the contract you expect"),
        ("Revoke when done", "most wallets let you clear permissions"),
    ]
    for i, (t, d) in enumerate(rules):
        y = 452 + i * 70
        box(cells, add, 980, y, 700, 54, "red", t, d, font=12)
    return S.d_graph(PAGE_W, PAGE_H, cells)

# ------------------------------------------------------------- page 3 -------
def page3():
    cells = []
    add = cells.append
    header(cells, add, "DVM-BASIC \u2014 SMART-CONTRACT CHEAT-SHEET", "The essentials to read or write a DERO contract.  DRAFT \u2014 verify against the DVM docs before shipping anything.")
    basics = [
        ("install_sc \u2192 SCID", "deploy a contract, get its address (SCID)"),
        ("RETURN 0 = success", "state commits only on 0 \u00b7 nonzero rolls back"),
        ("IF \u2026 THEN GOTO", "control flow \u2014 no else, no loops, just gotos"),
        ("STORE / LOAD", "persist and read contract state (private)"),
        ("SIGNED_BY_ENTRYPOINT", "require a valid signature to call"),
        ("block_height", "timelock a tx until a future block"),
        ("SEND_DERO_TO_ADDRESS", "move DERO from the contract \u2014 compressed key bytes, not bech32"),
        ("rpc.Argument", "uint64 literals need an explicit uint64() cast"),
    ]
    for i, (t, d) in enumerate(basics):
        y = 130 + (i % 4) * 110
        x = 120 + (i // 4) * 840
        box(cells, add, x, y, 800, 90, "purple", t, d, font=12.5)
    # gas line — numbers RE-GROUNDED in Release153 source (dvm/sc.go:238, dvm.go:522/994, dvm_functions.go)
    box(cells, add, 120, 590, 1560, 56, "amber", "GAS & LIMITS \u2014 mainnet (Release153): 10M compute gas/call \u00b7 line 5k \u00b7 expr 800 \u00b7 store 10k \u00b7 \u22481.7k statements/call", "verified dvm/sc.go:238 GasComputeLimit=10,000,000 \u00b7 dvm.go:522/994 \u00b7 dvm_functions.go (DRAFT: verify on next release)")
    # example
    ex = [
        "Function Initialize() Uint64",
        "  10 STORE(\"owner\", SIGNER())",
        "  20 RETURN 0",
        "Function Ping() Uint64",
        "  10 IF SIGNED_BY_ENTRYPOINT() == 0 THEN GOTO 40",
        "  20 STORE(\"last\", block_height)",
        "  30 RETURN 0",
        "  40 RETURN 1  \u2014 rollback",
    ]
    ex_txt = "\n".join(ex)
    add(f'<mxCell id="dvm-ex" value="{S.esc(ex_txt)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("green")[0]};strokeWidth=1.4;fontSize=11;fontColor={S.TH["ink"]};align=left;verticalAlign=middle;spacing=10;fontFamily=Consolas;shadow=1;" vertex="1" parent="1"><mxGeometry x="120" y="680" width="1560" height="170" as="geometry"/></mxCell>')
    return S.d_graph(PAGE_W, PAGE_H, cells)

# ------------------------------------------------------------- page 4 -------
def page4():
    cells = []
    add = cells.append
    header(cells, add, "BRIDGES & INTEROP \u2014 HONEST MAP", "How DERO connects to other chains \u2014 and where the risk is.  Bridges are the #1 place people lose money: trust matters.")
    live = [
        ("ETH \u2194 DERO bridge", "lock ETH \u2192 mint wrapped on DERO \u00b7 burn to unlock \u00b7 trust the bridge operators/audit", "green"),
        ("cldex / dero_swap", "on-DERO decentralized exchange \u2014 swap DERO tokens & wrapped assets", "green"),
        ("Artificer / ERC-20s", "tokens & NFTs issued directly on DERO (NFA, Seals, Deroscapes)", "green"),
    ]
    risky = [
        ("Trust assumption", "every bridge is a custodian at some layer \u2014 if it gets hacked, funds go with it"),
        ("Phishing surface", "fake bridge sites / fake wrapped-token addresses are common scams"),
        ("Interop limits", "not everything is bridgeable \u2014 check the bridge\u2019s supported assets before sending"),
    ]
    txt(cells, add, 120, 130, 700, "green", "LIVE / PARTIAL TODAY")
    for i, (t, d, acc) in enumerate(live):
        y = 166 + i * 96
        box(cells, add, 120, y, 1560, 76, acc, t, d, font=12.5)
    txt(cells, add, 120, 480, 700, "red", "WHERE THE RISK LIVES")
    for i, (t, d) in enumerate(risky):
        y = 516 + i * 96
        box(cells, add, 120, y, 1560, 76, "red", t, d, font=12.5)
    # good practice strip
    box(cells, add, 120, 830, 1560, 60, "amber", "GOOD PRACTICE: verify the official bridge contract/SCID from the project\u2019s docs \u00b7 send a tiny test amount first \u00b7 never click \u201cbridge\u201d links from DMs", "bridges concentrate value \u2014 that\u2019s where attackers aim", font=12.5)
    return S.d_graph(PAGE_W, PAGE_H, cells)

if __name__ == "__main__":
    theme = sys.argv[1] if len(sys.argv) > 1 else "light"
    S.set_theme(theme)
    d = os.path.dirname(os.path.abspath(__file__))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device" background="{S.TH["bg0"]}">\n'
           f'  <diagram id="runbook" name="Node Operator Runbook">\n{S.inject_draft(page1())}\n  </diagram>\n'
           f'  <diagram id="xswd" name="XSWD Permission Model">\n{S.inject_draft(page2())}\n  </diagram>\n'
           f'  <diagram id="dvm" name="DVM-BASIC Cheat-Sheet">\n{S.inject_draft(page3())}\n  </diagram>\n'
           f'  <diagram id="bridges" name="Bridges &amp; Interop">\n{S.inject_draft(page4())}\n  </diagram>\n'
           '</mxfile>\n')
    with open(os.path.join(d, "DERO.DEVOPS.drawio"), "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"written OK (theme={theme})")
