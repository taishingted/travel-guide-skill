#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a travel-guide HTML from trip.json + assets/.
Usage:
  python build_html.py trip.json assets guide.html            # self-contained (base64) -> the shareable file
  python build_html.py trip.json assets guide_files.html --files  # external image files -> use this one to print the PDF

Image naming convention (produced by process_images.py):
  gallery photo id "2-1"          -> assets/ph_2-1.jpg
  map / route id "map_day1"/"route_8" -> assets/map_day1.jpg / route_8.jpg

Localization: trip.json may set "lang" (default "en") and a "labels" object to override the
UI strings below in any language. See references/example-trip.zh-TW.json for a full override.
"""
import sys, os, json, base64, html
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

DEFAULT_LABELS = {
    "preflight_title": "Before You Go · Weather &amp; Packing",
    "weather_col": "Check the weather",
    "packing_col": "What to pack",
    "weather_small": "Tap for the forecast",
    "depart": "Leave",
    "route_link": "🗺 Open the day's route in Google Maps",
    "footer": "Times are estimates &mdash; adjust on the day for traffic and conditions. Please re-check opening hours before you go.",
}

# lang -> (script font families to load, sans primary, serif primary, rtl)
FONT_PROFILES = {
    "zh-hant": (["Noto Sans TC", "Noto Serif TC"], '"Noto Sans TC"', '"Noto Serif TC"', False),
    "zh-hans": (["Noto Sans SC", "Noto Serif SC"], '"Noto Sans SC"', '"Noto Serif SC"', False),
    "ja":      (["Noto Sans JP", "Noto Serif JP"], '"Noto Sans JP"', '"Noto Serif JP"', False),
    "ko":      (["Noto Sans KR", "Noto Serif KR"], '"Noto Sans KR"', '"Noto Serif KR"', False),
    "th":      (["Noto Sans Thai", "Noto Serif Thai"], '"Noto Sans Thai"', '"Noto Serif Thai"', False),
    "ar":      (["Noto Sans Arabic", "Noto Naskh Arabic"], '"Noto Sans Arabic"', '"Noto Naskh Arabic"', True),
    "he":      (["Noto Sans Hebrew", "Noto Serif Hebrew"], '"Noto Sans Hebrew"', '"Noto Serif Hebrew"', True),
}

def _norm_lang(lang):
    l = (lang or "en").lower().replace("_", "-")
    if l.startswith("zh"):
        return "zh-hans" if any(x in l for x in ("hans", "cn", "sg")) else "zh-hant"
    return l.split("-")[0]

def font_setup(lang):
    """Pick Google-Fonts <link>, font-family stacks and text direction from the output language."""
    prof = FONT_PROFILES.get(_norm_lang(lang))
    fams = ["Noto Sans", "Noto Serif"]            # Latin base (numbers / latin names) always loaded
    if prof:
        fams += prof[0]
    parts = []
    for f in fams:
        w = "wght@600;700;900" if "Serif" in f else "wght@400;500;700;900"
        parts.append("family=%s:%s" % (f.replace(" ", "+"), w))
    link = '<link href="https://fonts.googleapis.com/css2?%s&display=swap" rel="stylesheet">' % "&".join(parts)
    if prof:
        sans = '%s,"Noto Sans","Microsoft JhengHei",system-ui,sans-serif' % prof[1]
        serif = '%s,"Noto Serif","Georgia",serif' % prof[2]
        rtl = prof[3]
    else:
        sans = '"Noto Sans","Microsoft JhengHei",system-ui,sans-serif'
        serif = '"Noto Serif","Georgia",serif'
        rtl = False
    return link, sans, serif, ("rtl" if rtl else "ltr")

def esc(s):
    return html.escape(str(s), quote=False)

class Builder:
    def __init__(self, assets, embed, labels):
        self.assets = assets
        self.embed = embed
        self.L = {**DEFAULT_LABELS, **(labels or {})}

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
            return ""  # missing image: leave blank instead of crashing
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
                route += '<span class="arw">&rarr;</span>'
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
        ) % (t.get("eyebrow", ""), esc(t.get("title", "")),
             esc(t.get("subtitle", "")), route, chips)

    def preflight(self, t):
        wb = ""
        for w in t.get("weather", []):
            cls = " c2" if w.get("c2") else ""
            wb += ('<a class="wbtn%s" href="%s" target="_blank">%s<small>%s</small></a>'
                   % (cls, esc(w.get("url", "")), esc(w.get("label", "")),
                      esc(w.get("small", self.L["weather_small"]))))
        note = ('<p class="note">%s</p>' % t["weather_note"]) if t.get("weather_note") else ""
        packing = "".join("<li>%s</li>" % esc(p) for p in t.get("packing", []))
        return (
            '<section class="panel">\n'
            '  <h2><span class="ic">🎒</span>%s</h2>\n'
            '  <div class="two">\n'
            '    <div><div style="font-weight:800;color:var(--green-d);margin-bottom:6px;">%s</div>'
            '<div class="weatherbtns">%s</div>%s</div>\n'
            '    <div><div style="font-weight:800;color:var(--green-d);margin-bottom:6px;">%s</div>'
            '<ul class="wlist">%s</ul></div>\n'
            '  </div>\n'
            '</section>\n'
        ) % (self.L["preflight_title"], self.L["weather_col"], wb, note, self.L["packing_col"], packing)

    def leg(self, it):
        icon = esc(it.get("icon", "🚗"))
        car = '<span class="car">%s %s</span>' % (icon, esc(it.get("time", "")))
        rd = ('<span class="rd">%s</span>' % esc(it["road"])) if it.get("road") else ""
        return '<div class="leg"><span class="hr"></span>%s%s<span class="hr"></span></div>\n' % (car, rd)

    def stop(self, it):
        tc = '<div class="lbl">%s</div><div class="arr">%s</div>' % (
            esc(it.get("lbl", "")), esc(it.get("arr", "")))
        if it.get("stay"):
            tc += '<div class="stay">%s</div>' % esc(it["stay"])
        if it.get("dep"):
            tc += '<div class="dep">%s <b>%s</b></div>' % (esc(self.L["depart"]), esc(it["dep"]))
        tag = it.get("tag", {})
        tagspan = ('<span class="tag %s">%s</span>' % (esc(tag.get("cls", "spot")), esc(tag.get("text", "")))) if tag else ""
        zone = ('<span class="zone">%s</span>' % esc(it["zone"])) if it.get("zone") else ""
        name = '<div class="name">%s %s %s</div>' % (esc(it.get("name", "")), tagspan, zone)
        info = ""
        if it.get("info"):
            info = '<ul class="info">%s</ul>' % "".join(
                '<li><span class="i">%s</span>%s</li>' % (esc(x.get("i", "•")), x.get("text", ""))
                for x in it["info"])
        desc = ('<p class="desc">%s</p>' % it["desc"]) if it.get("desc") else ""
        subs = "".join(
            '<div class="subspot"><div class="st">%s</div>%s</div>' % (esc(s.get("st", "")), s.get("html", ""))
            for s in it.get("subspots", []))
        links = ""
        for a in it.get("links", []):
            cls = (' class="%s"' % a["cls"]) if a.get("cls") else ""
            links += '<a href="%s" target="_blank"%s>%s</a>' % (esc(a.get("url", "")), cls, esc(a.get("text", "")))
        warn = ('<span class="warn">%s</span>' % esc(it["warn"])) if it.get("warn") else ""
        pill = ('<div class="pill-links">%s%s</div>' % (links, warn)) if (links or warn) else ""
        body = '<div class="body">%s%s%s%s%s</div>' % (name, info, desc, subs, pill)
        gal = ""
        photos = it.get("photos", [])
        if photos:
            imgs = "".join('<img src="%s" alt="%s">' % (self.img_src(pid, photo=True), esc(it.get("name", "")))
                           for pid in photos)
            solo = " solo" if len(photos) == 1 else ""
            gal = '<div class="gallery%s">%s</div>' % (solo, imgs)
        rn = ""
        if it.get("route_note"):
            r = it["route_note"]
            rimg = ('<img src="%s" alt="route map">' % self.img_src(r["img"])) if r.get("img") else ""
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
            inner = ""
            if m.get("img"):
                src = self.img_src(m["img"])
                if src:
                    inner = '<img src="%s" alt="route map">' % src
            if not inner and m.get("link"):   # V2: no drawn map, just a Google Maps directions link
                inner = ('<div class="pill-links"><a href="%s" target="_blank">%s</a></div>'
                         % (esc(m["link"]), esc(self.L["route_link"])))
            cap = ('<figcaption>%s</figcaption>' % m["caption"]) if m.get("caption") else ""
            if inner or cap:
                mp = '<figure class="mapfig">%s%s</figure>' % (inner, cap)
        items = "".join(self.leg(it) if it.get("type") == "leg" else self.stop(it)
                        for it in d.get("items", []))
        backup = ('<div class="backup">%s</div>' % d["backup"]) if d.get("backup") else ""
        return '<section class="%s">%s%s<div class="timeline">%s</div>%s</section>\n' % (
            cls, head, mp, items, backup)

    def footer(self, t):
        return '<div class="footer">%s</div>' % t.get("footer", self.L["footer"])

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
    content = Builder(assets, embed, trip.get("labels")).build(trip)
    font_link, font_sans, font_serif, text_dir = font_setup(trip.get("lang", "en"))
    html_out = (tpl.replace("%%TITLE%%", esc(trip.get("title", "Travel Guide")))
                   .replace("%%LANG%%", esc(trip.get("lang", "en")))
                   .replace("%%DIR%%", text_dir)
                   .replace("%%FONT_LINK%%", font_link)
                   .replace("%%FONT_SANS%%", font_sans)
                   .replace("%%FONT_SERIF%%", font_serif)
                   .replace("<!--CONTENT-->", content))
    open(out, "w", encoding="utf-8").write(html_out)
    print("OK -> %s (%.2f MB, embed=%s)" % (out, len(html_out.encode()) / 1048576, embed))


if __name__ == "__main__":
    main()
