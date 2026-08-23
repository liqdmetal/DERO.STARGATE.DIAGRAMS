#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_drawio_svg.py — generic drawio -> SVG preview renderer.

Parses a .drawio file's flat box layouts (the template-system diagrams)
and emits one SVG per page: rounded/ellipse rects, stripped-HTML text,
and straight edges. Used to produce quick preview PNGs without drawio.app.
Usage: python render_drawio_svg.py FILE.drawio [outdir]
"""
import sys, os, re, html as _html
import xml.etree.ElementTree as ET

def esc(s): return _html.escape(str(s), quote=True)

def strip_html(s):
    s = s.replace("<br>", "\n").replace("<br/>", "\n").replace("<BR>", "\n")
    s = re.sub(r"<font[^>]*>", "", s)
    s = re.sub(r"<b>", "", s).replace("</b>", "")
    s = re.sub(r"<i>", "", s).replace("</i>", "")
    s = s.replace("</font>", "")
    s = re.sub(r"<[^>]+>", "", s)
    s = _html.unescape(s)
    return s

def parse_style(style):
    d = {}
    for kv in style.split(";"):
        if "=" in kv:
            k, v = kv.split("=", 1)
            d[k] = v
    return d

def render_file(path, outdir):
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree = ET.parse(path)
    root = tree.getroot()
    ns = {"mx": "http://www.mxgraph.io/"}
    mxfile = root
    diagrams = mxfile.findall("diagram")
    out_svgs = []
    for di, diag in enumerate(diagrams):
        name = diag.get("name", f"page{di+1}")
        model = diag.find("mxGraphModel")
        if model is None:
            continue
        bg = model.get("background") or "#FFFFFF"
        pw = int(float(model.get("pageWidth", 1800)))
        ph = int(float(model.get("pageHeight", 1020)))
        cells = []
        for cell in model.find("root"):
            if cell.tag != "mxCell":
                continue
            cells.append(cell)
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{pw}" height="{ph}" viewBox="0 0 {pw} {ph}" font-family="Segoe UI, Arial, sans-serif">',
               f'<rect x="0" y="0" width="{pw}" height="{ph}" fill="{bg}"/>']
        # edges first
        for cell in cells:
            style = cell.get("style", "")
            if cell.get("edge") == "1" or "edgeStyle" in style or "endArrow" in style:
                geo = cell.find("mxGeometry")
                if geo is None:
                    continue
                def pt(tag):
                    e = geo.find(tag)
                    return (float(e.get("x")), float(e.get("y"))) if e is not None else None
                src, tgt = pt("sourcePoint"), pt("targetPoint")
                if src and tgt:
                    color = "#38BDF8"
                    m = re.search(r"strokeColor=([^;]+)", style)
                    if m: color = m.group(1)
                    sw = 2.5
                    m = re.search(r"strokeWidth=([\d.]+)", style)
                    if m: sw = float(m.group(1))
                    dash = "8 6" if "dashed=1" in style else None
                    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
                    svg.append(f'<line x1="{src[0]}" y1="{src[1]}" x2="{tgt[0]}" y2="{tgt[1]}" stroke="{color}" stroke-width="{sw}"{dash_attr} marker-end="url(#arr)"/>')
                    # label
                    lc = cell.find("mxGeometry/../mxCell")
                    # find edgeLabel child cell
                    for sub in root.iter("mxCell"):
                        if sub.get("parent") == cell.get("id") and "edgeLabel" in sub.get("style", ""):
                            lbl = strip_html(sub.get("value", ""))
                            g = sub.find("mxGeometry")
                            if lbl and g is not None:
                                lx = float(g.get("x", 0)) + (src[0]+tgt[0])/2
                                ly = float(g.get("y", 0)) + (src[1]+tgt[1])/2 - 8
                                svg.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-size="11" font-weight="700" fill="{color}" stroke="{bg}" stroke-width="4" paint-order="stroke">{esc(lbl)}</text>')
        # marker def
        svg.append(f'<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#38BDF8"/></marker></defs>')
        # shapes
        for cell in cells:
            style = cell.get("style", "")
            if cell.get("edge") == "1" or "edgeStyle" in style or "endArrow" in style:
                continue
            if "text;" in style and "html" not in style:
                # pure text
                geo = cell.find("mxGeometry")
                if geo is None: continue
                x = float(geo.get("x", 0)); y = float(geo.get("y", 0))
                w = float(geo.get("width", 400)); h = float(geo.get("height", 24))
                col = "#22303C"
                m = re.search(r"fontColor=([^;]+)", style)
                if m: col = m.group(1)
                fs = 14
                m = re.search(r"fontSize=([\d.]+)", style)
                if m: fs = float(m.group(1))
                txt = strip_html(cell.get("value", ""))
                if not txt: continue
                for li, line in enumerate(txt.split("\n")[:4]):
                    svg.append(f'<text x="{x}" y="{y+fs+li*fs*1.25}" font-size="{fs}" font-weight="700" fill="{col}">{esc(line)}</text>')
                continue
            geo = cell.find("mxGeometry")
            if geo is None: continue
            x = float(geo.get("x", 0)); y = float(geo.get("y", 0))
            w = float(geo.get("width", 200)); h = float(geo.get("height", 60))
            # skip draft cell & others too wide/special? include all.
            st = parse_style(style)
            fill = st.get("fillColor", "#FFFFFF")
            stroke = st.get("strokeColor", "#26334D")
            sw = float(st.get("strokeWidth", "1.4"))
            dashed = "dashed=1" in style
            dash = ' stroke-dasharray="8 6"' if dashed else ""
            is_ellipse = "ellipse" in style
            rx = 26 if is_ellipse else 10
            if is_ellipse:
                svg.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
            else:
                svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>')
            val = cell.get("value", "")
            if not val: continue
            # text: title (first <font>) then desc
            lines = []
            plain = strip_html(val)
            # color the first line with stroke
            for li, line in enumerate(plain.split("\n")[:4]):
                fy = y + 22 + li * 15
                fs = 12.5 if li == 0 else 10.5
                fw = 700 if li == 0 else 400
                col = stroke if li == 0 else "#5A6B7A"
                svg.append(f'<text x="{x+12}" y="{fy}" font-size="{fs}" font-weight="{fw}" fill="{col}">{esc(line)}</text>')
        svg.append("</svg>")
        fn = os.path.join(outdir, f"preview_{os.path.splitext(os.path.basename(path))[0]}_{di+1}_{re.sub(r'[^a-z0-9]+','',name.lower())[:20]}.svg")
        with open(fn, "w", encoding="utf-8") as f:
            f.write("\n".join(svg))
        out_svgs.append(fn)
    return out_svgs

if __name__ == "__main__":
    path = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(path))
    files = render_file(path, outdir)
    print("rendered:")
    for f in files:
        print(" ", f)
