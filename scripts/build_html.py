#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 trip.json + assets/ 組成旅遊說明書 HTML。
用法:
  python build_html.py trip.json assets 行程.html            # 自包含(base64)，要分享的成品
  python build_html.py trip.json assets 行程_files.html --files  # 外部圖檔版，拿去印 PDF 用
圖片命名慣例(process_images.py 產出):
  畫廊照片 id "2-1"  -> assets/ph_2-1.jpg
  地圖/路線 id "map_day1"/"route_8" -> assets/map_day1.jpg / route_8.jpg
"""
import sys, os, json, base64, html
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

def esc(s):
    return html.escape(str(s), quote=False)

class Builder:
    def __init__(self, assets, embed):
        self.assets = assets
        self.embed = embed

    def _find(self, *cands):
        for c in cands:
            p = os.path.join(self.assets, c)
            if os.path.exists(p):
                return p
        return None

    def img_src(self, img_id, photo=False):
        base = ("ph_" + img_id) if photo else img_id
        p = self._find(base + ".jpg", base + ".png", base + ".jpeg")
        if not p:
            return ""  # 缺圖時留空，不炸
        if not self.embed:
            return self.assets.rstrip("/\\").split(os.sep)[-1] + "/" + os.path.basename(p)
        ext = os.path.splitext(p)[1].lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        b64 = base64.b64encode(open(p, "rb").read()).decode()
        return "data:%s;base64,%s" % (mime, b64)

    # ---------- components ----------
    def cover(self, t):
        route = ""
        nodes = t.get("route_summary", [])
        for i, n in enumerate(nodes):
            route += '<span class="node">%s</span>' % esc(n)
            if i < len(nodes) - 1:
                route += '<span class="arw">→</span>'
        chips = "".join(
            '<div class="chip"><b>%s</b>%s</div>' % (esc(c.get("b", "")), esc(c.get("text", "")))
            for c in t.get("cover_meta", [])
        )
        return (
            '<header class="cover">\n'
            '  <div class="eyebrow">%s</div>\n'
            '  <h1>%s</h1>\n'
            '  <div class="sub">%s</div>\n'
            '  <div class="route">%s</div>\n'
            '  <div class="meta">%s</div>\n'
            '</header>\n'
        ) % (esc(t.get("eyebrow", "")), esc(t.get("title", "")),
             esc(t.get("subtitle", "")), route, chips)

    def preflight(self, t):
        wb = ""
        for w in t.get("weather", []):
            cls = " c2" if w.get("c2") else ""
            wb += ('<a class="wbtn%s" href="%s" target="_blank">%s<small>%s</small></a>'
                   % (cls, esc(w.get("url", "")), esc(w.get("label", "")),
                      esc(w.get("small", "點我看一週預報"))))
        note = ('<p class="note">%s</p>' % t["weather_note"]) if t.get("weather_note") else ""
        packing = "".join("<li>%s</li>" % esc(p) for p in t.get("packing", []))
        return (
            '<section class="panel">\n'
            '  <h2><span class="ic">🎒</span>行前提醒　天氣 &amp; 攜帶工具</h2>\n'
            '  <div class="two">\n'
            '    <div><div style="font-weight:800;color:var(--green-d);margin-bottom:6px;">出發前先看天氣</div>'
            '<div class="weatherbtns">%s</div>%s</div>\n'
            '    <div><div style="font-weight:800;color:var(--green-d);margin-bottom:6px;">建議攜帶</div>'
            '<ul class="wlist">%s</ul></div>\n'
            '  </div>\n'
            '</section>\n'
        ) % (wb, note, packing)

    def leg(self, it):
        icon = esc(it.get("icon", "🚗"))
        car = '<span class="car">%s %s</span>' % (icon, esc(it.get("time", "")))
        rd = ('<span class="rd">%s</span>' % esc(it["road"])) if it.get("road") else ""
        return '<div class="leg"><span class="hr"></span>%s%s<span class="hr"></span></div>\n' % (car, rd)

    def stop(self, it):
        # timecol
        tc = '<div class="lbl">%s</div><div class="arr">%s</div>' % (
            esc(it.get("lbl", "到達")), esc(it.get("arr", "")))
        if it.get("stay"):
            tc += '<div class="stay">%s</div>' % esc(it["stay"])
        if it.get("dep"):
            tc += '<div class="dep">出發 <b>%s</b></div>' % esc(it["dep"])
        # name line
        tag = it.get("tag", {})
        tagspan = ('<span class="tag %s">%s</span>' % (esc(tag.get("cls", "spot")), esc(tag.get("text", "")))) if tag else ""
        zone = ('<span class="zone">%s</span>' % esc(it["zone"])) if it.get("zone") else ""
        name = '<div class="name">%s %s %s</div>' % (esc(it.get("name", "")), tagspan, zone)
        # info
        info = ""
        if it.get("info"):
            info = '<ul class="info">%s</ul>' % "".join(
                '<li><span class="i">%s</span>%s</li>' % (esc(x.get("i", "•")), x.get("text", ""))
                for x in it["info"])
        desc = ('<p class="desc">%s</p>' % it["desc"]) if it.get("desc") else ""
        subs = "".join(
            '<div class="subspot"><div class="st">%s</div>%s</div>' % (esc(s.get("st", "")), s.get("html", ""))
            for s in it.get("subspots", []))
        # links + warn
        links = ""
        for a in it.get("links", []):
            cls = (' class="%s"' % a["cls"]) if a.get("cls") else ""
            links += '<a href="%s" target="_blank"%s>%s</a>' % (esc(a.get("url", "")), cls, esc(a.get("text", "")))
        warn = ('<span class="warn">%s</span>' % esc(it["warn"])) if it.get("warn") else ""
        pill = ('<div class="pill-links">%s%s</div>' % (links, warn)) if (links or warn) else ""
        body = '<div class="body">%s%s%s%s%s</div>' % (name, info, desc, subs, pill)
        # gallery
        gal = ""
        photos = it.get("photos", [])
        if photos:
            imgs = "".join('<img src="%s" alt="%s">' % (self.img_src(pid, photo=True), esc(it.get("name", "")))
                           for pid in photos)
            solo = " solo" if len(photos) == 1 else ""
            gal = '<div class="gallery%s">%s</div>' % (solo, imgs)
        # route note
        rn = ""
        if it.get("route_note"):
            r = it["route_note"]
            rimg = ('<img src="%s" alt="路線圖">' % self.img_src(r["img"])) if r.get("img") else ""
            rn = '<div class="routewrap"><div class="roadnote">%s</div>%s</div>' % (r.get("html", ""), rimg)
        return '<article class="stop"><div class="top"><div class="timecol">%s</div>%s</div>%s%s</article>\n' % (
            tc, body, gal, rn)

    def day(self, d, idx):
        cls = "day"
        if d.get("theme") == "wood":
            cls += " day2"
        if idx > 0:
            cls += " day-break"
        head = ('<div class="dayhead"><span class="d">Day %s</span>'
                '<span class="dt">%s　%s</span><span class="rt">%s</span></div>'
                % (esc(d.get("no", idx + 1)), esc(d.get("date", "")),
                   esc(d.get("flow", "")), esc(d.get("range", ""))))
        mp = ""
        if d.get("map"):
            m = d["map"]
            mp = ('<figure class="mapfig"><img src="%s" alt="路線圖"><figcaption>%s</figcaption></figure>'
                  % (self.img_src(m.get("img", "")), m.get("caption", "")))
        items = ""
        for it in d.get("items", []):
            items += self.leg(it) if it.get("type") == "leg" else self.stop(it)
        backup = ('<div class="backup">%s</div>' % d["backup"]) if d.get("backup") else ""
        return '<section class="%s">%s%s<div class="timeline">%s</div>%s</section>\n' % (
            cls, head, mp, items, backup)

    def footer(self, t):
        return '<div class="footer">%s</div>' % t.get(
            "footer", "行程時間為預估，實際依當日交通與現場狀況彈性調整；資訊出發前建議再次確認。")

    def build(self, t):
        parts = [self.cover(t), self.preflight(t)]
        for i, d in enumerate(t.get("days", [])):
            parts.append(self.day(d, i))
        parts.append(self.footer(t))
        return "\n".join(parts)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    embed = "--files" not in sys.argv
    trip_path, assets, out = args[0], args[1], args[2]
    trip = json.load(open(trip_path, encoding="utf-8"))
    tpl_path = os.path.join(os.path.dirname(__file__), "..", "assets", "template.html")
    tpl = open(tpl_path, encoding="utf-8").read()
    content = Builder(assets, embed).build(trip)
    html_out = tpl.replace("%%TITLE%%", esc(trip.get("title", "旅遊行程"))).replace("<!--CONTENT-->", content)
    open(out, "w", encoding="utf-8").write(html_out)
    mb = len(html_out.encode()) / 1048576
    print("OK -> %s (%.2f MB, embed=%s)" % (out, mb, embed))


if __name__ == "__main__":
    main()
