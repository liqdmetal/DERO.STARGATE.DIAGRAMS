#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DERO.SYSTEMS.drawio — systems reference diagrams.
Page 1: Full-node system architecture (derod internals + attached components)
Page 2: Network topology & ports
Page 3: Protocol / reference stack (crypto -> consensus -> ledger -> VM -> interfaces -> apps)
Page 4: derohe source-tree reference (repo layout mapped to roles)
Sources: derod.org corpus (daemon, ports, mining), deroproject/derohe repo layout.
"""
import xml.sax.saxutils as sax
import datetime, html, re

TITLE_COLOR = "#4277BB"
INK, GRAY = "#22303C", "#5A6B7A"
BLUE, BLUE_T = "#1E88E5", "#E3F2FD"
TEAL, TEAL_T = "#00838F", "#E0F7FA"
GREEN, GREEN_T = "#2E7D32", "#E8F5E9"
PURPLE, PURPLE_T = "#8E24AA", "#F3E5F5"
ORANGE, ORANGE_T = "#FB8C00", "#FFF3E0"
RED, RED_T = "#C62828", "#FDECEA"
GRAY_C = "#6E6F72"
W, H = 1920, 1420

def esc(s):
    return sax.escape(s, {"'": "&apos;", '"': "&quot;"})

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

# ============================================================ PAGE 1 ========
NODE_INTERNALS = [
    ("P2P \u00b7 TLS", "gossip + sync \u00b7 p2p/connection.go \u00b7 port 10101 (randomized)", BLUE),
    ("Mempool", "unconfirmed tx pool \u00b7 shared with peers", TEAL),
    ("Consensus core", "validate (transaction_verify.go) + execute (transaction_execute.go) \u00b7 \u03a3-block logic", BLUE),
    ("GravitonDB", "encrypted key/value state \u00b7 accounts \u00b7 merkle-proved \u00b7 prunable", TEAL),
    ("DVM", "DVM-BASIC contract runtime \u00b7 private SC state", PURPLE),
    ("JSON-RPC server", "daemon API \u00b7 port 10102 \u00b7 rpc/rpc_dero.go", GREEN),
    ("GETWORK server", "miner work + results \u00b7 port 10100 \u00b7 websocket", ORANGE),
]
ATTACHED = [
    ("WALLET \u2014 CLI / RPC (10103)", "dero-wallet-cli \u00b7 keys never leave the wallet \u00b7 builds & signs txs", GREEN),
    ("ENGRAM \u2014 smart wallet", "GUI + TELA browser \u00b7 XSWD bridge for dApps \u00b7 10103", GREEN),
    ("MINER \u2014 dero-miner / tnn-miner", "AstroBWTv3 work \u2192 GETWORK 10100 \u00b7 submits \u03a3-block shares", ORANGE),
    ("EXPLORER / INDEXERS", "Gnomon \u00b7 HyperGnomon \u00b7 derohist \u00b7 read RPC 10102", PURPLE),
    ("AI / MCP bridge", "dero-mcp-server \u00b7 read-only over RPC", PURPLE),
    ("dApp layer", "TELA \u00b7 DeroAuth \u00b7 DeroPay \u00b7 DeroBeats \u00b7 Hologram \u00b7 reach wallets via XSWD", TEAL),
]

def page1_cells():
    cells = []
    add = cells.append
    add(f'<mxCell id="s1t" value="DERO SYSTEMS REFERENCE \u2014 FULL-NODE ARCHITECTURE" style="text;html=1;align=center;fontSize=30;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="42" as="geometry"/></mxCell>')
    add(f'<mxCell id="s1s" value="Everything one DERO node runs, and everything that attaches to it.  Ports are mainnet defaults.  Grounded in derod.org + deroproject/derohe source layout." style="text;html=1;align=center;fontSize=13.5;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    # attached components: left column (wallets), right column (miner), bottom row (services)
    # WALLET left
    add(f'<mxCell id="s1-w1" value="{esc(ATTACHED[0][0])}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={GREEN_T};strokeColor={GREEN};strokeWidth=2;fontSize=12;fontStyle=1;fontColor={GREEN};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="40" y="130" width="360" height="60" as="geometry"/></mxCell>')
    add(f'<mxCell id="s1-w1d" value="{esc(ATTACHED[0][1])}" style="text;html=1;align=center;fontSize=10.5;fontColor={GRAY};whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="40" y="192" width="360" height="34" as="geometry"/></mxCell>')
    add(f'<mxCell id="s1-w2" value="{esc(ATTACHED[1][0])}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={GREEN_T};strokeColor={GREEN};strokeWidth=2;fontSize=12;fontStyle=1;fontColor={GREEN};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="40" y="236" width="360" height="60" as="geometry"/></mxCell>')
    add(f'<mxCell id="s1-w2d" value="{esc(ATTACHED[1][1])}" style="text;html=1;align=center;fontSize=10.5;fontColor={GRAY};whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="40" y="298" width="360" height="34" as="geometry"/></mxCell>')
    # MINER right
    add(f'<mxCell id="s1-m1" value="{esc(ATTACHED[2][0])}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={ORANGE_T};strokeColor={ORANGE};strokeWidth=2;fontSize=12;fontStyle=1;fontColor={ORANGE};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="1520" y="130" width="360" height="60" as="geometry"/></mxCell>')
    add(f'<mxCell id="s1-m1d" value="{esc(ATTACHED[2][1])}" style="text;html=1;align=center;fontSize=10.5;fontColor={GRAY};whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="1520" y="192" width="360" height="34" as="geometry"/></mxCell>')
    # daemon box
    add(f'<mxCell id="s1-d" value="DEROD \u2014 THE NODE" style="swimlane;fontStyle=1;horizontal=1;collapsible=0;startSize=30;fillColor=#F4F8FC;strokeColor={TITLE_COLOR};strokeWidth=2.5;fontColor={TITLE_COLOR};fontSize=15;verticalAlign=top;align=center;" vertex="1" parent="1"><mxGeometry x="440" y="120" width="1040" height="760" as="geometry"/></mxCell>')
    # internals as a 2-col grid inside
    ix = 460; iy = 165; iw = 490; ih = 120
    for i, (name, desc, color) in enumerate(NODE_INTERNALS):
        r, c = divmod(i, 2)
        x = ix + c * (iw + 20); y = iy + r * (ih + 16)
        add(f'<mxCell id="s1-n{i}" value="{val(f"<font color=&quot;{color}&quot;><b>{esc(name)}</b></font><br><font color=&quot;#66727E&quot;>{esc(desc)}</font>")}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={color};strokeWidth=1.8;fontSize=10.5;fontColor={INK};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{iw}" height="{ih}" as="geometry"/></mxCell>')
    # services bottom row
    sy = 920
    add(f'<mxCell id="s1-sh" value="ATTACHED SERVICES \u2014 what the ecosystem runs against the node" style="text;html=1;align=left;fontSize=14;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="40" y="{sy}" width="700" height="22" as="geometry"/></mxCell>')
    sx = 40; sw = 290; shh = 120
    for i, (name, desc, color) in enumerate(ATTACHED[3:]):
        x = sx + i * (sw + 12)
        add(f'<mxCell id="s1-a{i}" value="{val(f"<font color=&quot;{color}&quot;><b>{esc(name)}</b></font><br><font color=&quot;#66727E&quot;>{esc(desc)}</font>")}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={color};strokeWidth=1.8;fontSize=10.5;fontColor={INK};align=center;verticalAlign=middle;spacing=6;" vertex="1" parent="1"><mxGeometry x="{x}" y="{sy+28}" width="{sw}" height="{shh}" as="geometry"/></mxCell>')
    # connectors (simple orthogonal)
    def line(eid, p1, p2, color="#0076BE", width=2.5, label=None, dashed=False):
        db = "dashed=1;" if dashed else ""
        lbl = ""
        if label:
            lbl = (f'<mxCell id="{eid}-l" value="{esc(label)}" style="edgeLabel;html=1;align=center;verticalAlign=middle;labelBackgroundColor=#FFFFFF;fontSize=10.5;fontStyle=1;fontColor={color};" vertex="1" connectable="0"><mxGeometry x="0.5" y="0.5" relative="1" as="geometry"><mxPoint as="offset"/></mxGeometry></mxCell>')
        add(f'<mxCell id="{eid}" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=classicThin;endFill=1;strokeColor={color};strokeWidth={width};{db}fontSize=10;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{p1[0]}" y="{p1[1]}" as="sourcePoint"/><mxPoint x="{p2[0]}" y="{p2[1]}" as="targetPoint"/></mxGeometry>{lbl}</mxCell>')
    line("s1-l1", (400, 230), (440, 230), GREEN, 2.5, "local RPC 10102 / 10103")
    line("s1-l2", (400, 300), (440, 300), GREEN, 2.5)
    line("s1-l3", (1520, 210), (1480, 210), ORANGE, 2.5, "GETWORK 10100")
    line("s1-l4", (185, 400), (440, 400), PURPLE, 2.5)
    line("s1-l5", (185, 520), (440, 520), PURPLE, 2.5)
    line("s1-l6", (185, 640), (440, 640), TEAL, 2.5, "via XSWD \u2194 wallet")
    # node-to-node
    line("s1-l7", (1480, 700), (1520, 700), BLUE, 3, "TLS P2P \u2192 other nodes (10101)")
    return f'<mxGraphModel dx="1400" dy="850" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="1140" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel>"

# ============================================================ PAGE 2 ========
PORT_TABLE = [
    ("P2P", "10101", "node \u2194 node gossip + sync", "randomized at startup \u00b7 pin with --p2p-bind"),
    ("GETWORK", "10100", "miner \u2194 daemon work", "only if miners connect from outside"),
    ("RPC (daemon)", "10102", "daemon JSON-RPC API", "keep local (127.0.0.1) \u2014 never expose"),
    ("Wallet RPC", "10103", "wallet API for CLI/Engram", "local only \u00b7 keys never leave wallet"),
    ("XSWD", "via wallet", "dApp \u2194 wallet WebSocket", "per-request ask / accept / deny"),
]
TOPO = [
    ("YOUR NODE", "derod \u00b7 validates \u00b7 stores \u00b7 mines", BLUE),
    ("PEER NODES \u00d7 many", "the rest of the network \u2014 same software", BLUE),
    ("YOUR WALLET", "Engram / CLI \u2014 signs locally", GREEN),
    ("YOUR MINER", "dero-miner / tnn-miner / Dirtybird", ORANGE),
    ("INDEXER / EXPLORER", "Gnomon \u00b7 derohist \u00b7 explorer.dero.io", PURPLE),
    ("dApp / TELA", "on-chain web \u00b7 talks via XSWD", TEAL),
]

def page2_cells():
    cells = []
    add = cells.append
    add(f'<mxCell id="s2t" value="DERO SYSTEMS REFERENCE \u2014 NETWORK TOPOLOGY &amp; PORTS" style="text;html=1;align=center;fontSize=30;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="42" as="geometry"/></mxCell>')
    add(f'<mxCell id="s2s" value="Who connects to whom, over which port, and what to keep private.  Mainnet defaults \u00b7 testnet = +30300." style="text;html=1;align=center;fontSize=13.5;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    # central node
    add(f'<mxCell id="s2-c" value="DEROD \u2014 YOUR FULL NODE" style="rounded=1;whiteSpace=wrap;html=1;fillColor={BLUE_T};strokeColor={BLUE};strokeWidth=3;fontSize=16;fontStyle=1;fontColor={BLUE};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="760" y="300" width="400" height="120" as="geometry"/></mxCell>')
    # surrounding actors
    pos = [
        ("s2-p1", TOPO[0], 120, 120), ("s2-p2", TOPO[1], 1380, 120),
        ("s2-p3", TOPO[2], 120, 420), ("s2-p4", TOPO[3], 1380, 420),
        ("s2-p5", TOPO[4], 120, 720), ("s2-p6", TOPO[5], 1380, 720),
    ]
    for cid, (name, desc, color), x, y in pos:
        add(f'<mxCell id="{cid}" value="{val(f"<font color=&quot;{color}&quot;><b>{esc(name)}</b></font><br><font color=&quot;#66727E&quot;>{esc(desc)}</font>")}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={color};strokeWidth=2;fontSize=12;fontColor={INK};align=center;verticalAlign=middle;spacing=8;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="360" height="130" as="geometry"/></mxCell>')
    def line(eid, p1, p2, color, label, dashed=False):
        db = "dashed=1;" if dashed else ""
        lbl = f'<mxCell id="{eid}-l" value="{esc(label)}" style="edgeLabel;html=1;align=center;verticalAlign=middle;labelBackgroundColor=#FFFFFF;fontSize=10.5;fontStyle=1;fontColor={color};" vertex="1" connectable="0"><mxGeometry x="0.5" y="0.5" relative="1" as="geometry"><mxPoint as="offset"/></mxGeometry></mxCell>'
        add(f'<mxCell id="{eid}" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=classicThin;endFill=1;strokeColor={color};strokeWidth=2.5;{db}fontSize=10;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{p1[0]}" y="{p1[1]}" as="sourcePoint"/><mxPoint x="{p2[0]}" y="{p2[1]}" as="targetPoint"/></mxGeometry>{lbl}</mxCell>')
    line("s2-l1", (480, 185), (760, 340), BLUE, "TLS P2P \u00b7 10101")
    line("s2-l2", (1380, 340), (1740, 185), BLUE, "TLS P2P \u00b7 10101")
    line("s2-l3", (480, 480), (760, 380), GREEN, "RPC 10102 / 10103 (local)")
    line("s2-l4", (1380, 480), (1740, 470), ORANGE, "GETWORK \u00b7 10100")
    line("s2-l5", (480, 770), (760, 420), PURPLE, "read RPC \u00b7 10102")
    line("s2-l6", (1380, 770), (1740, 420), TEAL, "XSWD \u2194 wallet")
    # security panel
    add(f'<mxCell id="s2-sec" value="\U0001F6E1\uFE0F SECURITY RULES" style="text;html=1;align=left;fontSize=14;fontStyle=1;fontColor={RED};" vertex="1" parent="1"><mxGeometry x="40" y="900" width="300" height="22" as="geometry"/></mxCell>')
    add(f'<mxCell id="s2-secb" value="Never expose the RPC port (10102) to the internet \u2014 local only \u00b7 P2P port is randomized; pin it and open it in the firewall if you want inbound peers \u00b7 wallet keys never leave the wallet process \u00b7 use a VPN/SSH tunnel for remote RPC." style="rounded=1;whiteSpace=wrap;html=1;fillColor={RED_T};strokeColor={RED};strokeWidth=1.5;fontSize=12;fontColor={INK};align=left;verticalAlign=middle;spacing=10;" vertex="1" parent="1"><mxGeometry x="40" y="928" width="900" height="120" as="geometry"/></mxCell>')
    # port table
    add(f'<mxCell id="s2-ph" value="PORT REFERENCE" style="text;html=1;align=left;fontSize=14;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="1000" y="900" width="300" height="22" as="geometry"/></mxCell>')
    py = 930
    for name, port, purpose, note in PORT_TABLE:
        port_html = f"<font color=&quot;{TITLE_COLOR}&quot;><b>{esc(name)}</b></font> <font color=&quot;{GRAY}&quot;>{esc(port)}</font> \u2014 <font color=&quot;#66727E&quot;>{esc(purpose)}</font><br><font color=&quot;#8A97A3&quot;><i>{esc(note)}</i></font>"
        add(f'<mxCell id="s2-pt-{name}" value="{val(port_html)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C9D6E3;strokeWidth=1.5;fontSize=11;fontColor={INK};align=left;verticalAlign=middle;spacing=8;" vertex="1" parent="1"><mxGeometry x="1000" y="{py}" width="880" height="56" as="geometry"/></mxCell>')
        py += 64
    return f'<mxGraphModel dx="1400" dy="850" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="1250" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel>"

# ============================================================ PAGE 3 ========
STACK = [
    ("APPLICATIONS", TEAL, ["Wallets (Engram, CLI, g45w)", "TELA \u00b7 on-chain web", "DeroAuth / DeroPay", "DeroBeats \u00b7 dReams \u00b7 Hologram \u00b7 cldex"]),
    ("INTERFACES", GREEN, ["JSON-RPC (daemon 10102 / wallet 10103)", "GETWORK websocket (10100)", "XSWD \u2014 dApp \u2194 wallet bridge", "MCP server \u2014 AI read access"]),
    ("EXECUTION", PURPLE, ["DVM \u2014 DeroScript / DVM-BASIC", "smart contracts with private encrypted state", "tx generation <25 ms \u00b7 verification <25 ms"]),
    ("LEDGER & STATE", BLUE, ["DHEBP \u2014 homomorphic account model (66 B/account)", "GravitonDB key/value \u00b7 merkle-proved \u00b7 prunable", "blocks: 10 \u03a3-blocks (9+1) \u00b7 18 s \u00b7 erasure-coded 48\u219216", "mempool \u00b7 chain state \u00b7 pruning to a few GB"]),
    ("CONSENSUS", ORANGE, ["AstroBWTv3 PoW \u2014 CPU-only, \u2248256 MB/thread", "difficulty retarget every block \u00b7 18 s pace", "\u03a3-block rewards split to winners \u00b7 network IS the pool", "supply: halving ~4 yr \u00b7 hard cap \u224820.89M"]),
    ("CRYPTOGRAPHY", RED, ["Homomorphic encryption \u2014 compute on ciphertext", "ring signatures (ring 8 default) \u00b7 6 bound proofs", "Pedersen commitments + bulletproofs", "TLS \u00b7 AstroBWTv3 memory-hard PoW"]),
]

def page3_cells():
    cells = []
    add = cells.append
    add(f'<mxCell id="s3t" value="DERO SYSTEMS REFERENCE \u2014 THE PROTOCOL STACK" style="text;html=1;align=center;fontSize=30;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="42" as="geometry"/></mxCell>')
    add(f'<mxCell id="s3s" value="Six layers, bottom = the math, top = what users touch.  Each layer only trusts the one beneath it." style="text;html=1;align=center;fontSize=13.5;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    y = 120
    for name, color, items in STACK:
        safe = re.sub(r"[^A-Za-z0-9_]", "", name)
        add(f'<mxCell id="s3-{safe}" value="{esc(name)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={color};strokeColor=none;fontSize=15;fontStyle=1;fontColor=#FFFFFF;align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="60" y="{y}" width="300" height="150" as="geometry"/></mxCell>')
        items_html = val("<br>".join(esc(x) for x in items))
        add(f'<mxCell id="s3-{safe}-b" value="{items_html}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={color};strokeWidth=2;fontSize=11;fontColor={INK};align=left;verticalAlign=middle;spacing=10;" vertex="1" parent="1"><mxGeometry x="380" y="{y}" width="1480" height="150" as="geometry"/></mxCell>')
        add(f'<mxCell id="s3-{safe}-a" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=classicThin;endFill=1;strokeColor={TITLE_COLOR};strokeWidth=3;fontSize=10;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{360}" y="{y+75}" as="sourcePoint"/><mxPoint x="380" y="{y+75}" as="targetPoint"/></mxGeometry></mxCell>')
        y += 166
    add(f'<mxCell id="s3-f" value="Reading it bottom-up: the math (crypto) makes consensus honest \u2192 consensus writes a private ledger \u2192 the VM runs programs on it \u2192 interfaces expose it \u2192 applications use it." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F4F8FC;strokeColor={TITLE_COLOR};strokeWidth=1.5;fontSize=12.5;fontColor={GRAY};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="60" y="{y+16}" width="1800" height="60" as="geometry"/></mxCell>')
    return f'<mxGraphModel dx="1400" dy="850" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{y + 110}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel>"

# ============================================================ PAGE 4 ========
SRC_TREE = [
    ("cmd/", "binaries \u2014 derod, dero-wallet-cli, dero-miner, explorer", BLUE),
    ("config/", "constants \u2014 BLOCK_TIME=18, MINIBLOCK_HIGHDIFF=9, ports", BLUE),
    ("block/", "block & mini-block (\u03a3-block) structures, DAG collection", TEAL),
    ("blockchain/", "consensus, validation, execution, rewards (transaction_execute.go)", TEAL),
    ("p2p/", "TLS network, gossip, time-check (p2p/controller.go)", BLUE),
    ("rpc/", "daemon JSON-RPC + GETWORK websocket (rpc_dero.go)", GREEN),
    ("walletapi/", "wallet RPC + XSWD bridge (walletapi/xswd)", GREEN),
    ("cryptography/", "bn256, homomorphic enc, ring sigs, bulletproofs", RED),
    ("dvm/", "DeroScript / DVM-BASIC compiler + runtime", PURPLE),
    ("pow/ + astrobwt/", "PoW plumbing + AstroBWTv3 algorithm", ORANGE),
    ("premine/ + proof/", "genesis/premine \u00b7 transaction proof system", GRAY_C),
    ("metrics/ + glue/", "observability \u00b7 internal glue (rwc)", GRAY_C),
]

def page4_cells():
    cells = []
    add = cells.append
    add(f'<mxCell id="s4t" value="DERO SYSTEMS REFERENCE \u2014 SOURCE-TREE MAP" style="text;html=1;align=center;fontSize=30;fontStyle=1;fontColor={TITLE_COLOR};" vertex="1" parent="1"><mxGeometry x="20" y="22" width="1880" height="42" as="geometry"/></mxCell>')
    add(f'<mxCell id="s4s" value="The deroproject/derohe repository, mapped to what each package owns.  Where to look when you want to change a thing." style="text;html=1;align=center;fontSize=13.5;fontColor={GRAY};" vertex="1" parent="1"><mxGeometry x="20" y="66" width="1880" height="22" as="geometry"/></mxCell>')
    y = 130
    for i, (name, desc, color) in enumerate(SRC_TREE):
        r, c = divmod(i, 2)
        x = 60 + c * 930; yy = y + r * 160
        add(f'<mxCell id="s4-{name.strip("/")}" value="{val(f"<font color=&quot;{color}&quot;><b>{esc(name)}</b></font> &#160;<font color=&quot;#66727E&quot;>{esc(desc)}</font>")}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={color};strokeWidth=2;fontSize=12;fontColor={INK};align=left;verticalAlign=middle;spacing=10;fontFamily=Courier New;" vertex="1" parent="1"><mxGeometry x="{x}" y="{yy}" width="890" height="130" as="geometry"/></mxCell>')
    add(f'<mxCell id="s4-f" value="DEROFDN/derohe is now the single home for both development and releases. Current release: Release153 (Hard-Fork 3 follow-up, 21 Aug 2026) \u2014 HF3 activated at block 7,504,640; run Release153+ to stay in sync. deroproject/derohe is the upstream archive." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F4F8FC;strokeColor={TITLE_COLOR};strokeWidth=1.5;fontSize=12.5;fontColor={GRAY};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="60" y="860" width="1800" height="60" as="geometry"/></mxCell>')
    return f'<mxGraphModel dx="1400" dy="850" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="980" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel>"

# ============================================================ SVG p1 ========
def svg_p1():
    out = []
    A = out.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="1140" viewBox="0 0 {W} 1140" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<defs><marker id="s1a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0076BE"/></marker></defs>')
    A(f'<rect x="0" y="0" width="{W}" height="1140" fill="#FFFFFF"/>')
    A(f'<text x="{W/2}" y="52" text-anchor="middle" font-size="30" font-weight="700" fill="{TITLE_COLOR}">DERO SYSTEMS REFERENCE \u2014 FULL-NODE ARCHITECTURE</text>')
    A(f'<text x="{W/2}" y="82" text-anchor="middle" font-size="13.5" fill="{GRAY}">Everything one DERO node runs, and everything that attaches to it.  Ports are mainnet defaults.  Grounded in derod.org + deroproject/derohe source layout.</text>')
    # daemon box
    A(f'<rect x="440" y="120" width="1040" height="760" rx="12" fill="#F4F8FC" stroke="{TITLE_COLOR}" stroke-width="2.5"/>')
    A(f'<text x="960" y="144" text-anchor="middle" font-size="15" font-weight="700" fill="{TITLE_COLOR}">DEROD \u2014 THE NODE</text>')
    for i, (name, desc, color) in enumerate(NODE_INTERNALS):
        r, c = divmod(i, 2)
        x = 460 + c * 510; y = 165 + r * 136
        A(f'<rect x="{x}" y="{y}" width="490" height="120" rx="9" fill="#FFFFFF" stroke="{color}" stroke-width="1.8"/>')
        A(f'<text x="{x+14}" y="{y+26}" font-size="12" font-weight="700" fill="{color}">{svg_esc(name)}</text>')
        ty = y + 48
        for ln in wrap(desc, 460, 10.5):
            A(f'<text x="{x+14}" y="{ty}" font-size="10.5" fill="#66727E">{svg_esc(ln)}</text>'); ty += 16
    # attached left/right
    A(f'<rect x="40" y="130" width="360" height="60" rx="8" fill="{GREEN_T}" stroke="{GREEN}" stroke-width="2"/>')
    A(f'<text x="220" y="165" text-anchor="middle" font-size="12" font-weight="700" fill="{GREEN}">{svg_esc(ATTACHED[0][0])}</text>')
    A(f'<text x="220" y="185" text-anchor="middle" font-size="10" fill="{GRAY}">{svg_esc(ATTACHED[0][1])}</text>')
    A(f'<rect x="40" y="236" width="360" height="60" rx="8" fill="{GREEN_T}" stroke="{GREEN}" stroke-width="2"/>')
    A(f'<text x="220" y="271" text-anchor="middle" font-size="12" font-weight="700" fill="{GREEN}">{svg_esc(ATTACHED[1][0])}</text>')
    A(f'<text x="220" y="291" text-anchor="middle" font-size="10" fill="{GRAY}">{svg_esc(ATTACHED[1][1])}</text>')
    A(f'<rect x="1520" y="130" width="360" height="60" rx="8" fill="{ORANGE_T}" stroke="{ORANGE}" stroke-width="2"/>')
    A(f'<text x="1700" y="165" text-anchor="middle" font-size="12" font-weight="700" fill="{ORANGE}">{svg_esc(ATTACHED[2][0])}</text>')
    A(f'<text x="1700" y="185" text-anchor="middle" font-size="10" fill="{GRAY}">{svg_esc(ATTACHED[2][1])}</text>')
    # services bottom
    A(f'<text x="40" y="938" font-size="14" font-weight="700" fill="{TITLE_COLOR}">ATTACHED SERVICES \u2014 what the ecosystem runs against the node</text>')
    for i, (name, desc, color) in enumerate(ATTACHED[3:]):
        x = 40 + i * 302
        A(f'<rect x="{x}" y="948" width="290" height="120" rx="9" fill="#FFFFFF" stroke="{color}" stroke-width="1.8"/>')
        A(f'<text x="{x+14}" y="{y+26 if False else 974}" font-size="11.5" font-weight="700" fill="{color}">{svg_esc(name)}</text>')
        ty = 994
        for ln in wrap(desc, 265, 10.5):
            A(f'<text x="{x+14}" y="{ty}" font-size="10.5" fill="#66727E">{svg_esc(ln)}</text>'); ty += 15
    # connectors
    A(f'<line x1="400" y1="160" x2="440" y2="160" stroke="{GREEN}" stroke-width="2.5" marker-end="url(#s1a)"/>')
    A(f'<text x="420" y="152" text-anchor="middle" font-size="10" font-weight="700" fill="{GREEN}">RPC 10102/10103</text>')
    A(f'<line x1="1520" y1="160" x2="1480" y2="160" stroke="{ORANGE}" stroke-width="2.5" marker-end="url(#s1a)"/>')
    A(f'<text x="1500" y="152" text-anchor="middle" font-size="10" font-weight="700" fill="{ORANGE}">GETWORK 10100</text>')
    A(f'<line x1="1480" y1="700" x2="1520" y2="700" stroke="{BLUE}" stroke-width="3" marker-end="url(#s1a)"/>')
    A(f'<text x="1500" y="692" text-anchor="middle" font-size="10" font-weight="700" fill="{BLUE}">TLS P2P \u2192 peers</text>')
    A('</svg>')
    return "\n".join(out)

def svg_p2():
    out = []
    A = out.append
    H2 = 1250
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H2}" viewBox="0 0 {W} {H2}" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<defs><marker id="s2a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0076BE"/></marker></defs>')
    A(f'<rect x="0" y="0" width="{W}" height="{H2}" fill="#FFFFFF"/>')
    A(f'<text x="{W/2}" y="52" text-anchor="middle" font-size="30" font-weight="700" fill="{TITLE_COLOR}">DERO SYSTEMS REFERENCE \u2014 NETWORK TOPOLOGY &amp; PORTS</text>')
    A(f'<text x="{W/2}" y="82" text-anchor="middle" font-size="13.5" fill="{GRAY}">Who connects to whom, over which port, and what to keep private.  Mainnet defaults \u00b7 testnet = +30300.</text>')
    A(f'<rect x="760" y="300" width="400" height="120" rx="12" fill="{BLUE_T}" stroke="{BLUE}" stroke-width="3"/>')
    A(f'<text x="960" y="360" text-anchor="middle" font-size="16" font-weight="700" fill="{BLUE}">DEROD \u2014 YOUR FULL NODE</text>')
    pos = [(120,120),(1380,120),(120,420),(1380,420),(120,720),(1380,720)]
    for (x,y),(name,desc,color) in zip(pos, TOPO):
        A(f'<rect x="{x}" y="{y}" width="360" height="130" rx="10" fill="#FFFFFF" stroke="{color}" stroke-width="2"/>')
        A(f'<text x="{x+180}" y="{y+46}" text-anchor="middle" font-size="12" font-weight="700" fill="{color}">{svg_esc(name)}</text>')
        A(f'<text x="{x+180}" y="{y+70}" text-anchor="middle" font-size="10.5" fill="#66727E">{svg_esc(desc)}</text>')
    A(f'<line x1="480" y1="180" x2="760" y2="340" stroke="{BLUE}" stroke-width="2.5" marker-end="url(#s2a)"/>')
    A(f'<text x="600" y="240" font-size="10" font-weight="700" fill="{BLUE}">TLS P2P \u00b7 10101</text>')
    A(f'<line x1="1380" y1="340" x2="1740" y2="180" stroke="{BLUE}" stroke-width="2.5" marker-end="url(#s2a)"/>')
    A(f'<text x="1560" y="300" font-size="10" font-weight="700" fill="{BLUE}">TLS P2P \u00b7 10101</text>')
    A(f'<line x1="480" y1="480" x2="760" y2="380" stroke="{GREEN}" stroke-width="2.5" marker-end="url(#s2a)"/>')
    A(f'<text x="600" y="445" font-size="10" font-weight="700" fill="{GREEN}">RPC 10102/10103 (local)</text>')
    A(f'<line x1="1380" y1="480" x2="1740" y2="480" stroke="{ORANGE}" stroke-width="2.5" marker-end="url(#s2a)"/>')
    A(f'<text x="1370" y="472" text-anchor="end" font-size="10" font-weight="700" fill="{ORANGE}">GETWORK \u00b7 10100</text>')
    A(f'<line x1="480" y1="770" x2="760" y2="420" stroke="{PURPLE}" stroke-width="2.5" marker-end="url(#s2a)"/>')
    A(f'<text x="600" y="600" font-size="10" font-weight="700" fill="{PURPLE}">read RPC \u00b7 10102</text>')
    A(f'<line x1="1380" y1="770" x2="1740" y2="420" stroke="{TEAL}" stroke-width="2.5" marker-end="url(#s2a)"/>')
    A(f'<text x="1560" y="600" font-size="10" font-weight="700" fill="{TEAL}">XSWD \u2194 wallet</text>')
    A(f'<text x="40" y="918" font-size="14" font-weight="700" fill="{RED}">\U0001F6E1\uFE0F SECURITY RULES</text>')
    A(f'<rect x="40" y="930" width="900" height="120" rx="10" fill="{RED_T}" stroke="{RED}" stroke-width="1.5"/>')
    A(f'<text x="56" y="958" font-size="12" fill="{INK}">\u2022 Never expose the RPC port (10102) to the internet \u2014 local only</text>')
    A(f'<text x="56" y="980" font-size="12" fill="{INK}">\u2022 P2P port is randomized; pin it and open the firewall for inbound peers</text>')
    A(f'<text x="56" y="1002" font-size="12" fill="{INK}">\u2022 Wallet keys never leave the wallet process</text>')
    A(f'<text x="56" y="1024" font-size="12" fill="{INK}">\u2022 For remote RPC, use a VPN / SSH tunnel</text>')
    A(f'<text x="1000" y="918" font-size="14" font-weight="700" fill="{TITLE_COLOR}">PORT REFERENCE</text>')
    py = 932
    for name, port, purpose, note in PORT_TABLE:
        A(f'<rect x="1000" y="{py}" width="880" height="54" rx="8" fill="#FFFFFF" stroke="#C9D6E3" stroke-width="1.5"/>')
        A(f'<text x="1016" y="{py+22}" font-size="11.5" font-weight="700" fill="{TITLE_COLOR}">{svg_esc(name)}</text>')
        A(f'<text x="{1016 + 11*len(name) + 14}" y="{py+22}" font-size="11.5" fill="{GRAY}">{svg_esc(port)}</text>')
        A(f'<text x="1016" y="{py+40}" font-size="10.5" fill="#66727E">{svg_esc(purpose)} \u00b7 <tspan font-style="italic">{svg_esc(note)}</tspan></text>')
        py += 60
    A('</svg>')
    return "\n".join(out)

def svg_p3():
    out = []
    A = out.append
    H3 = 120 + 6 * 166 + 96
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H3}" viewBox="0 0 {W} {H3}" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<defs><marker id="s3a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{TITLE_COLOR}"/></marker></defs>')
    A(f'<rect x="0" y="0" width="{W}" height="{H3}" fill="#FFFFFF"/>')
    A(f'<text x="{W/2}" y="52" text-anchor="middle" font-size="30" font-weight="700" fill="{TITLE_COLOR}">DERO SYSTEMS REFERENCE \u2014 THE PROTOCOL STACK</text>')
    A(f'<text x="{W/2}" y="82" text-anchor="middle" font-size="13.5" fill="{GRAY}">Six layers, bottom = the math, top = what users touch.  Each layer only trusts the one beneath it.</text>')
    y = 120
    for name, color, items in STACK:
        A(f'<rect x="60" y="{y}" width="300" height="150" rx="10" fill="{color}"/>')
        A(f'<text x="210" y="{y+82}" text-anchor="middle" font-size="15" font-weight="700" fill="#FFFFFF">{svg_esc(name)}</text>')
        A(f'<rect x="380" y="{y}" width="1480" height="150" rx="10" fill="#FFFFFF" stroke="{color}" stroke-width="2"/>')
        ty = y + 34
        for it in items:
            A(f'<text x="398" y="{ty}" font-size="11.5" fill="{INK}">\u2022 {svg_esc(it)}</text>'); ty += 28
        A(f'<line x1="360" y1="{y+75}" x2="380" y2="{y+75}" stroke="{TITLE_COLOR}" stroke-width="3" marker-end="url(#s3a)"/>')
        y += 166
    A(f'<rect x="60" y="{y+16}" width="1800" height="60" rx="10" fill="#F4F8FC" stroke="{TITLE_COLOR}" stroke-width="1.5"/>')
    A(f'<text x="960" y="{y+53}" text-anchor="middle" font-size="12.5" fill="{GRAY}">Reading it bottom-up: the math (crypto) makes consensus honest \u2192 consensus writes a private ledger \u2192 the VM runs programs on it \u2192 interfaces expose it \u2192 applications use it.</text>')
    A('</svg>')
    return "\n".join(out)

def svg_p4():
    out = []
    A = out.append
    H4 = 980
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H4}" viewBox="0 0 {W} {H4}" font-family="Segoe UI, Arial, sans-serif">')
    A(f'<rect x="0" y="0" width="{W}" height="{H4}" fill="#FFFFFF"/>')
    A(f'<text x="{W/2}" y="52" text-anchor="middle" font-size="30" font-weight="700" fill="{TITLE_COLOR}">DERO SYSTEMS REFERENCE \u2014 SOURCE-TREE MAP</text>')
    A(f'<text x="{W/2}" y="82" text-anchor="middle" font-size="13.5" fill="{GRAY}">The deroproject/derohe repository, mapped to what each package owns.  Where to look when you want to change a thing.</text>')
    y = 130
    for i, (name, desc, color) in enumerate(SRC_TREE):
        r, c = divmod(i, 2)
        x = 60 + c * 930; yy = y + r * 160
        A(f'<rect x="{x}" y="{yy}" width="890" height="130" rx="10" fill="#FFFFFF" stroke="{color}" stroke-width="2"/>')
        A(f'<text x="{x+20}" y="{yy+52}" font-size="14" font-family="Consolas, monospace" font-weight="700" fill="{color}">{svg_esc(name)}</text>')
        ty = yy + 82
        for ln in wrap(desc, 840, 11.5):
            A(f'<text x="{x+20}" y="{ty}" font-size="11.5" fill="#66727E">{svg_esc(ln)}</text>'); ty += 17
    A(f'<rect x="60" y="860" width="1800" height="60" rx="10" fill="#F4F8FC" stroke="{TITLE_COLOR}" stroke-width="1.5"/>')
    A(f'<text x="960" y="896" text-anchor="middle" font-size="12.5" fill="{GRAY}">DEROFDN/derohe is now the single home for both development and releases. Current release: Release153 (Hard-Fork 3 follow-up, 21 Aug 2026) \u2014 HF3 activated at block 7,504,640; run Release153+ to stay in sync. deroproject/derohe is the upstream archive.</text>')
    A('</svg>')
    return "\n".join(out)

# ============================================================ main ==========
if __name__ == "__main__":
    import os
    d = os.path.dirname(os.path.abspath(__file__))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device">\n'
           f'  <diagram id="node-arch" name="Full-Node Architecture">\n{inject_draft(page1_cells())}\n  </diagram>\n'
           f'  <diagram id="topology" name="Network Topology and Ports">\n{inject_draft(page2_cells())}\n  </diagram>\n'
           f'  <diagram id="stack" name="Protocol Stack">\n{inject_draft(page3_cells())}\n  </diagram>\n'
           f'  <diagram id="src-tree" name="Source-Tree Map">\n{inject_draft(page4_cells())}\n  </diagram>\n'
           '</mxfile>\n')
    with open(os.path.join(d, "DERO.SYSTEMS.drawio"), "w", encoding="utf-8") as f:
        f.write(xml)
    svgs = [("preview_systems1.svg", inject_draft_svg(svg_p1())),
            ("preview_systems2.svg", inject_draft_svg(svg_p2())),
            ("preview_systems3.svg", inject_draft_svg(svg_p3())),
            ("preview_systems4.svg", inject_draft_svg(svg_p4()))]
    for name, svg in svgs:
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(svg)
        with open(os.path.join(d, name.replace(".svg", ".html")), "w", encoding="utf-8") as f:
            f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;}}</style></head><body>{svg}</body></html>')
    print("written OK")
