#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DERO.STYLE.drawio — the DERO diagram template system showcase.

Displays both themes (DHEBP Night dark + DHEBP Paper light) with every
component: headers, zones, chips, badges, pills, arrows, draft notice.
Use this page to pick which template fits which diagram, then pass the
theme name to the generators (e.g. `python build_master_diagram.py light`).
"""
import datetime, os, sys
import dero_style as S

W, H = 2400, 1500

def build(theme):
    S.set_theme(theme)
    cells = []
    add = cells.append
    for c in S.d_header("t", 40, 30, 2320,
                        "DHEBP NIGHT" if theme == "dark" else "DHEBP PAPER",
                        f"Theme: {theme} \u2014 preview every template component here. Dark = share/cyber \u00b7 Light = print/reference.",
                        font=34):
        add(c)
    # zone demo
    for c in S.d_zone("z1", 60, 130, 1100, 340, "blue", "ZONE PANEL \u2014 live (solid)", num=1):
        add(c)
    for c in S.d_zone("z2", 60, 490, 1100, 300, "orange", "ZONE PANEL \u2014 hypothetical (dashed)", num=4, dashed=True):
        add(c)
    # chips demo
    for i, (name, desc, acc) in enumerate([
        ("CHIP \u00b7 blue", "default card", "blue"),
        ("CHIP \u00b7 green", "default card", "green"),
        ("CHIP \u00b7 teal", "default card", "teal"),
        ("CHIP \u00b7 purple", "default card", "purple"),
    ]):
        for c in S.d_chip(f"chip{i}", 1300 + (i % 2) * 420, 130 + (i // 2) * 130, 380, 110, acc, name, desc):
            add(c)
    # pills + badge demo
    for c in S.d_pill("pill1", 1300, 430, "green", "LIVE"):
        add(c)
    for c in S.d_pill("pill2", 1300, 470, "amber", "PARTIAL"):
        add(c)
    for c in S.d_pill("pill3", 1300, 510, "red", "EXPERIMENTAL"):
        add(c)
    # arrows demo
    for eid, p1, p2, label, acc in [
        ("ar1", (220, 900), (700, 900), "solid connector", "blue"),
        ("ar2", (900, 900), (1400, 900), "dashed = hypothetical", "purple"),
        ("ar3", (1600, 900), (2100, 900), "thick flow", "green"),
    ]:
        for c in S.d_arrow(eid, [p1, p2], accent_key=acc, label=label, width=3, dashed=(eid == "ar2")):
            add(c)
    # TL;DR panel
    add(f'<mxCell id="tldr" value="{S.esc("THE 30-SECOND VERSION")}" style="text;html=1;align=left;fontSize=15;fontStyle=1;fontColor={S.accent("brand")[0]};" vertex="1" parent="1"><mxGeometry x="60" y="1020" width="300" height="22" as="geometry"/></mxCell>')
    tldr_text = "The template system lives in dero_style.py \u2014 set S.set_theme(\u2018dark\u2019 / \u2018light\u2019) and every component (zone, chip, badge, pill, arrow, header, draft stamp) re-themes itself. Draw.io XML and SVG render from the same helpers."
    add(f'<mxCell id="tldr-b" value="{S.esc(tldr_text)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={S.TH["panel"]};gradientColor={S.TH["panel2"]};gradientDirection=south;strokeColor={S.accent("brand")[0]};strokeWidth=1.5;shadow=1;fontSize=14;fontColor={S.TH["ink"]};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="60" y="1048" width="2280" height="64" as="geometry"/></mxCell>')
    return S.d_graph(W, H, cells)

def build_svg(theme):
    S.set_theme(theme)
    out = S.svg_open(W, H, "DHEBP NIGHT" if theme == "dark" else "DHEBP PAPER",
                     f"Theme: {theme} \u2014 preview every template component here. Dark = share/cyber \u00b7 Light = print/reference.")
    out += S.svg_zone(60, 130, 1100, 340, "blue", "ZONE PANEL \u2014 live (solid)", num=1)
    out += S.svg_zone(60, 490, 1100, 300, "orange", "ZONE PANEL \u2014 hypothetical (dashed)", num=4, dashed=True)
    for i, (name, desc, acc) in enumerate([
        ("CHIP \u00b7 blue", "default card", "blue"),
        ("CHIP \u00b7 green", "default card", "green"),
        ("CHIP \u00b7 teal", "default card", "teal"),
        ("CHIP \u00b7 purple", "default card", "purple"),
    ]):
        out += S.svg_chip(1300 + (i % 2) * 420, 130 + (i // 2) * 130, 380, 110, acc, name, desc)
    out += S.svg_pill(1300, 440, "green", "LIVE")
    out += S.svg_pill(1400, 440, "amber", "PARTIAL")
    out += S.svg_pill(1520, 440, "red", "EXPERIMENTAL")
    for eid, p1, p2, label, acc, dashed in [
        ("ar1", (220, 900), (700, 900), "solid connector", "blue", False),
        ("ar2", (900, 900), (1400, 900), "dashed = hypothetical", "purple", True),
        ("ar3", (1600, 900), (2100, 900), "thick flow", "green", False),
    ]:
        out += S.svg_arrow([p1, p2], accent_key=acc, label=label, width=3, dashed=dashed)
    out.append(f'<text x="60" y="1036" font-size="15" font-weight="700" fill="{S.accent("brand")[0]}">THE 30-SECOND VERSION</text>')
    out.append(f'<rect x="60" y="1048" width="2280" height="64" rx="12" fill="{S.TH["panel"]}" stroke="{S.accent("brand")[0]}" stroke-width="1.5"/>')
    out.append(f'<text x="1200" y="1086" text-anchor="middle" font-size="14" fill="{S.TH["ink"]}">The template system lives in dero_style.py \u2014 set S.set_theme(\u2018dark\u2019 / \u2018light\u2019) and every component re-themes itself. Draw.io XML and SVG render from the same helpers.</text>')
    out += S.svg_draft(H)
    return S.svg_close(out)

if __name__ == "__main__":
    d = os.path.dirname(os.path.abspath(__file__))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    bodies = []
    for theme in ("dark", "light"):
        S.set_theme(theme)
        bodies.append(f'  <diagram id="style-{theme}" name="Style \u2014 {theme}">\n{S.inject_draft(build(theme))}\n  </diagram>\n')
        svg = build_svg(theme)
        with open(os.path.join(d, f"preview_style_{theme}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)
        with open(os.path.join(d, f"preview_style_{theme}.html"), "w", encoding="utf-8") as f:
            f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;background:{S.TH["bg0"]};}}</style></head><body>{svg}</body></html>')
    S.set_theme("dark")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<mxfile host="app.diagrams.net" modified="{now}" agent="Hermes-AI" version="24.4.8" type="device" background="{S.TH["bg0"]}">\n'
           + "".join(bodies) + '</mxfile>\n')
    with open(os.path.join(d, "DERO.STYLE.drawio"), "w", encoding="utf-8") as f:
        f.write(xml)
    print("written OK")
