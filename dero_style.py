#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dero_style.py — the DERO diagram template system (v2).

A shared design language for every diagram generator. Both the draw.io XML
and the SVG preview are emitted from the SAME helpers, so they can never
drift apart.

Two themes:
  THEME = "dark"  (default) — "DHEBP Night": deep navy canvas, glass panels,
                    gradient title, glowing badges, neon accents.
  THEME = "light" — "DHEBP Paper": soft white/indigo cards, crisp shadows,
                    rich saturated accents, ideal for print.
"""
import xml.sax.saxutils as sax
import html as _html
import re

THEME = "dark"

# ---------------------------------------------------------------- theme ----
_DARK = {
    "bg0": "#0B1220", "bg1": "#101A2E",          # canvas gradient
    "panel": "#141E36", "panel2": "#0F1930",     # glass panels
    "border": "#26334D",
    "ink": "#E8EEF7", "muted": "#8FA3BF",
    "brand": "#38BDF8",
    "chip": "#18233D",
    "onDark": "#FFFFFF",
    "amber":  ("#FBBF24", "#7C4A0B"),
    "green":  ("#34D399", "#065F46"),
    "blue":   ("#38BDF8", "#075985"),
    "teal":   ("#2DD4BF", "#0F766E"),
    "purple": ("#A78BFA", "#5B21B6"),
    "orange": ("#FB923C", "#9A3412"),
    "pink":   ("#F472B6", "#9D174D"),
    "red":    ("#F87171", "#991B1B"),
    "gray":   ("#94A3B8", "#475569"),
    "draft_bg": "#2A1216", "draft_stroke": "#F87171", "draft_ink": "#FCA5A5",
}
_LIGHT = {
    "bg0": "#F4F7FC", "bg1": "#E9EEF8",          # canvas gradient
    "panel": "#FFFFFF", "panel2": "#F7FAFF",     # cards
    "border": "#D7E0EE",
    "ink": "#1C2A3A", "muted": "#5A6B7A",
    "brand": "#2563EB",
    "chip": "#FFFFFF",
    "onDark": "#FFFFFF",
    "amber":  ("#F59E0B", "#B45309"),
    "green":  ("#10B981", "#065F46"),
    "blue":   ("#2563EB", "#1E40AF"),
    "teal":   ("#0D9488", "#0F766E"),
    "purple": ("#8B5CF6", "#5B21B6"),
    "orange": ("#F97316", "#C2410C"),
    "pink":   ("#EC4899", "#9D174D"),
    "red":    ("#DC2626", "#991B1B"),
    "gray":   ("#64748B", "#334155"),
    "draft_bg": "#FDEBEC", "draft_stroke": "#DC2626", "draft_ink": "#B91C1C",
}
TH = _DARK
DRAFT_BG, DRAFT_STROKE, DRAFT_INK = TH["draft_bg"], TH["draft_stroke"], TH["draft_ink"]

def set_theme(name):
    global TH, DRAFT_BG, DRAFT_STROKE, DRAFT_INK
    TH = _DARK if name == "dark" else _LIGHT
    DRAFT_BG, DRAFT_STROKE, DRAFT_INK = TH["draft_bg"], TH["draft_stroke"], TH["draft_ink"]

# ---------------------------------------------------------------- text ----
def esc(s):
    return sax.escape(str(s), {"'": "&apos;", '"': "&quot;"})

def val(s):
    return s.replace("<", "&lt;").replace(">", "&gt;")

def svg_esc(s):
    return _html.escape(str(s))

def wrap(text, width_px, font_px, factor=0.55):
    cap = max(8, int(width_px / (font_px * factor)))
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if len(cand) <= cap or not cur:
            cur = cand
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def accent(key):
    return TH.get(key, TH["blue"])

def _safe(s):
    return re.sub(r"[^A-Za-z0-9_]", "", str(s))

# ============================================================ draw.io =======
def d_zone(cid, x, y, w, h, accent_key, label, num=None, dashed=False, sub=None):
    """Glass zone panel with gradient header + optional big number badge."""
    col, colD = accent(accent_key)
    db = "dashed=1;" if dashed else ""
    cells = [
        f'<mxCell id="{cid}-bg" value="" style="rounded=1;html=1;fillColor={TH["panel"]};gradientColor={TH["panel2"]};gradientDirection=south;strokeColor={col};strokeWidth=1.5;{db}shadow=1;opacity=92;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>',
        f'<mxCell id="{cid}-strip" value="" style="rounded=1;html=1;fillColor={col};strokeColor=none;opacity=90;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="6" as="geometry"/></mxCell>',
    ]
    if num:
        cells.append(f'<mxCell id="{cid}-num" value="{num}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor={col};gradientColor={colD};gradientDirection=south;strokeColor=#0B1220;strokeWidth=2;shadow=1;fontColor=#FFFFFF;fontSize=20;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="{x+18}" y="{y+16}" width="40" height="40" as="geometry"/></mxCell>')
        lx = x + 70
    else:
        lx = x + 18
    cells.append(f'<mxCell id="{cid}-t" value="{esc(label)}" style="text;html=1;align=left;fontSize=16;fontStyle=1;fontColor={col};" vertex="1" parent="1"><mxGeometry x="{lx}" y="{y+24}" width="{w-lx+x-18}" height="24" as="geometry"/></mxCell>')
    if sub:
        cells.append(f'<mxCell id="{cid}-s" value="{esc(sub)}" style="text;html=1;align=left;fontSize=10.5;fontColor={TH["muted"]};" vertex="1" parent="1"><mxGeometry x="{lx}" y="{y+46}" width="{w-lx+x-18}" height="16" as="geometry"/></mxCell>')
    return cells

def d_chip(cid, x, y, w, h, accent_key, title, desc=None, icon=None, dashed=False, font=10.5):
    col, colD = accent(accent_key)
    db = "dashed=1;" if dashed else ""
    inner = []
    if icon:
        inner.append(f'{icon}')
    inner.append(f'<font color=&quot;{col}&quot;><b>{esc(title)}</b></font>')
    if desc:
        inner.append(f'<font color=&quot;{TH["muted"]}&quot;>{esc(desc)}</font>')
    v = val("<br>".join(inner))
    return [f'<mxCell id="{cid}" value="{v}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={TH["panel"]};gradientColor={TH["panel2"]};gradientDirection=south;strokeColor={col};strokeWidth=1.2;{db}shadow=1;fontSize={font};fontColor={TH["ink"]};align=center;verticalAlign=middle;spacing=8;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>']

def d_pill(cid, x, y, accent_key, text, w=None, h=24):
    col, _ = accent(accent_key)
    return [f'<mxCell id="{cid}" value="{esc(text)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={col};strokeColor=none;fontSize=10;fontStyle=1;fontColor=#FFFFFF;align=center;verticalAlign=middle;shadow=1;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w or 36+9*len(text)}" height="{h}" as="geometry"/></mxCell>']

def d_header(cid, x, y, w, title, subtitle=None, font=30):
    cells = [f'<mxCell id="{cid}" value="{esc(title)}" style="text;html=1;align=center;fontSize={font};fontStyle=1;fontColor={TH["ink"]};" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{font+14}" as="geometry"/></mxCell>']
    if subtitle:
        cells.append(f'<mxCell id="{cid}-s" value="{esc(subtitle)}" style="text;html=1;align=center;fontSize=13;fontColor={TH["muted"]};" vertex="1" parent="1"><mxGeometry x="{x}" y="{y+font+14}" width="{w}" height="22" as="geometry"/></mxCell>')
    return cells

def d_arrow(eid, pts, accent_key="brand", label=None, width=2.5, dashed=False):
    col, _ = accent(accent_key)
    db = "dashed=1;" if dashed else ""
    src, tgt = pts[0], pts[-1]
    way = "".join(f'<mxPoint x="{p[0]}" y="{p[1]}"/>' for p in pts[1:-1])
    lbl = ""
    if label:
        lbl = (f'<mxCell id="{eid}-l" value="{esc(label)}" style="edgeLabel;html=1;align=center;verticalAlign=middle;'
               f'labelBackgroundColor={TH["panel"]};fontSize=11;fontStyle=1;fontColor={col};" vertex="1" connectable="0">'
               f'<mxGeometry x="0.5" y="0.5" relative="1" as="geometry"><mxPoint as="offset"/></mxGeometry></mxCell>')
    return [f'<mxCell id="{eid}" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=classicThin;endFill=1;strokeColor={col};strokeWidth={width};{db}fontSize=10;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{src[0]}" y="{src[1]}" as="sourcePoint"/><mxPoint x="{tgt[0]}" y="{tgt[1]}" as="targetPoint"/><Array as="points">{way}</Array></mxGeometry>{lbl}</mxCell>']

def d_graph(w, h, cells, dx=1400, dy=850):
    return (f'<mxGraphModel dx="{dx}" dy="{dy}" grid="1" gridSize="10" guides="1" tooltips="1" '
            f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{w}" pageHeight="{h}" '
            f'background="{TH["bg0"]}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
            + "".join(cells) + "</root></mxGraphModel>")

def d_draft(h):
    return f'<mxCell id="draft" value="&#9888;&#65039; DRAFT &#8212; community draft \u2014 not verified, reviewed, or audited" style="rounded=1;whiteSpace=wrap;html=1;fillColor={DRAFT_BG};strokeColor={DRAFT_STROKE};strokeWidth=1.5;fontSize=11;fontStyle=1;fontColor={DRAFT_INK};align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="18" y="{h-46}" width="400" height="34" as="geometry"/></mxCell>'

def inject_draft(model):
    m = re.search(r'pageHeight="(\d+)"', model)
    h = int(m.group(1)) if m else 1400
    return model.replace('<mxCell id="1" parent="0"/>', '<mxCell id="1" parent="0"/>' + d_draft(h), 1)

# ================================================================ svg =======
def svg_open(w, h, title, subtitle=None):
    defs = f'''
<defs>
 <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0" stop-color="{TH['bg0']}"/><stop offset="1" stop-color="{TH['bg1']}"/>
 </linearGradient>
 <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">
   <stop offset="0" stop-color="{TH['brand']}"/><stop offset="0.5" stop-color="#A78BFA"/><stop offset="1" stop-color="{TH['green'][0]}"/>
 </linearGradient>
 <filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="12" flood-color="#000000" flood-opacity="0.55"/></filter>
</defs>'''
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Segoe UI, Arial, sans-serif">',
           defs,
           f'<rect x="0" y="0" width="{w}" height="{h}" fill="url(#bgGrad)"/>']
    ty = 58 if subtitle else 52
    if subtitle:
        out.append(f'<text x="{w/2}" y="46" text-anchor="middle" font-size="34" font-weight="800" fill="url(#titleGrad)" style="letter-spacing:1px">{svg_esc(title)}</text>')
        out.append(f'<text x="{w/2}" y="76" text-anchor="middle" font-size="13" fill="{TH["muted"]}">{svg_esc(subtitle)}</text>')
    else:
        out.append(f'<text x="{w/2}" y="{ty}" text-anchor="middle" font-size="34" font-weight="800" fill="url(#titleGrad)" style="letter-spacing:1px">{svg_esc(title)}</text>')
    return out

def svg_zone(x, y, w, h, accent_key, label, num=None, dashed=False, sub=None):
    col, colD = accent(accent_key)
    dash = 'stroke-dasharray="10 7"' if dashed else ""
    out = []
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{TH["panel"]}" stroke="{col}" stroke-opacity="0.55" stroke-width="1.5" {dash} filter="url(#soft)"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="6" rx="3" fill="{col}" fill-opacity="0.9"/>')
    if num:
        out.append(f'<circle cx="{x+38}" cy="{y+36}" r="20" fill="url(#titleGrad)" stroke="#0B1220" stroke-width="2" filter="url(#glow)"/>')
        out.append(f'<text x="{x+38}" y="{y+43}" text-anchor="middle" font-size="20" font-weight="800" fill="#FFFFFF">{num}</text>')
        lx = x + 70
    else:
        lx = x + 18
    out.append(f'<text x="{lx}" y="{y+42}" font-size="16" font-weight="700" fill="{col}">{svg_esc(label)}</text>')
    if sub:
        out.append(f'<text x="{lx}" y="{y+62}" font-size="10.5" fill="{TH["muted"]}">{svg_esc(sub)}</text>')
    return out

def svg_chip(x, y, w, h, accent_key, title, desc=None, icon=None, dashed=False, font=10.5):
    col, _ = accent(accent_key)
    dash = 'stroke-dasharray="6 5"' if dashed else ""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{TH["chip"]}" stroke="{col}" stroke-opacity="0.65" stroke-width="1.2" {dash}/>']
    ty = y + 24
    line = ""
    if icon:
        line += icon + "  "
    line += title
    out.append(f'<text x="{x+w/2}" y="{ty}" text-anchor="middle" font-size="{font}" font-weight="700" fill="{col}">{svg_esc(line)}</text>')
    if desc:
        ty += 19
        for ln in wrap(desc, w - 18, font - 1):
            out.append(f'<text x="{x+w/2}" y="{ty}" text-anchor="middle" font-size="{font-1}" fill="{TH["muted"]}">{svg_esc(ln)}</text>')
            ty += 15
    return out

def svg_pill(x, y, accent_key, text, w=None, h=22):
    col, _ = accent(accent_key)
    return [f'<rect x="{x}" y="{y}" width="{w or 34+8.2*len(text)}" height="{h}" rx="{h/2}" fill="{col}"/>',
            f'<text x="{x + (w or 34+8.2*len(text))/2}" y="{y+15}" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">{svg_esc(text)}</text>']

def svg_badge(cx, cy, accent_key, num, r=17):
    col, colD = accent(accent_key)
    return [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" stroke="#0B1220" stroke-width="2" filter="url(#glow)"/>',
            f'<text x="{cx}" y="{cy+6}" text-anchor="middle" font-size="15" font-weight="800" fill="#FFFFFF">{num}</text>']

def svg_arrow(pts, accent_key="brand", label=None, width=3, dashed=False):
    col, _ = accent(accent_key)
    dash = 'stroke-dasharray="8 6"' if dashed else ""
    mk = f"ar-{accent_key}"
    out = [f'<marker id="{mk}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>']
    d = " ".join(f"L {p[0]} {p[1]}" for p in pts[1:])
    out.append(f'<path d="M {pts[0][0]} {pts[0][1]} {d}" fill="none" stroke="{col}" stroke-width="{width}" {dash} marker-end="url(#{mk})"/>')
    if label:
        mid = pts[len(pts)//2]
        out.append(f'<text x="{mid[0]}" y="{mid[1]-8}" text-anchor="middle" font-size="11" font-weight="700" fill="{col}" stroke="#0B1220" stroke-width="4" paint-order="stroke">{svg_esc(label)}</text>')
    return out

def svg_draft(h):
    return [f'<rect x="18" y="{h-46}" width="400" height="34" rx="8" fill="{DRAFT_BG}" stroke="{DRAFT_STROKE}" stroke-width="1.5"/>',
            f'<text x="218" y="{h-24}" text-anchor="middle" font-size="11" font-weight="700" fill="{DRAFT_INK}">\u26A0\uFE0F DRAFT \u2014 community draft: not verified, reviewed, or audited</text>']

def svg_close(extra=None):
    out = list(extra or [])
    out.append('</svg>')
    return "\n".join(out)

# markers need to be deduped in the open block; we collect them via a registry
def svg_arrow_marker_decl(accent_key):
    col, _ = accent(accent_key)
    return f'<marker id="ar-{accent_key}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>'
