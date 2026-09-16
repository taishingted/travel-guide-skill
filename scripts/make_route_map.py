#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-generate route maps (real OSM basemap + numbered pins + direction arrows) from trip.json.

Why: a "tap to open Google Maps" button doesn't show, at a glance, that the trip runs
one-way and where each stop sits locally. This draws that picture.

For each day it renders assets/map_dayN.png = that day's stops, numbered in visiting order,
joined by arrows. It also renders assets/map_overview.png = one pin per day across the whole
region, arrowed in day order, so the reader sees the whole corridor at once.

Coordinates come from trip.json:
  - each stop may carry   "geo": [lng, lat]      (decimal degrees; lng first, WGS84)
  - each day may carry     "geo": [lng, lat]      (the day's label point for the overview;
                                                   if absent, the mean of that day's stops is used)
Stops without geo are skipped (the map still builds from the ones that have it). No geo at
all in a day -> that day's map is skipped, gracefully.

Usage:
  python make_route_map.py trip.json assets

Then reference the images from trip.json like any other map image:
  "map": { "img": "map_day2", "caption": "..." }      # per-day
  "map": { "img": "map_overview", "caption": "..." }   # e.g. on Day 1 as a whole-trip orientation

Needs: staticmap + Pillow (check_env.py installs them). Requires internet at build time to
fetch map tiles; if tiles can't be fetched it prints a clear hint and skips the map (the guide
still builds without it).
"""
import sys, os, json, math

try:
    from staticmap import StaticMap, Line
    from staticmap.staticmap import _lon_to_x, _lat_to_y
except Exception:
    print("[skip] staticmap not installed - run check_env.py. Maps skipped; guide still builds.")
    sys.exit(0)
try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    print("[skip] Pillow not installed - run check_env.py. Maps skipped.")
    sys.exit(0)

TILE = "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"

# day theme -> pin color (matches the guide's green/wood day accent)
THEME_COLOR = {"green": (37, 122, 90), "wood": (176, 114, 54)}
OVERVIEW_COLOR = (198, 94, 63)   # warm terracotta, like the sample's route arrows


def _font(size):
    for name in ("arialbd.ttf", "arial.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _fit_zoom(pts, w, h, margin=0.80):
    """Largest zoom where the (padded) extent of pts still fits the canvas."""
    lons = [p[0] for p in pts]; lats = [p[1] for p in pts]
    if len(pts) == 1:
        return 12  # single point: a sensible city-level zoom
    for z in range(16, 1, -1):
        xs = [_lon_to_x(lo, z) for lo in lons]
        ys = [_lat_to_y(la, z) for la in lats]
        span_x = (max(xs) - min(xs)) * 256
        span_y = (max(ys) - min(ys)) * 256
        if span_x <= w * margin and span_y <= h * margin:
            return z
    return 2


def _center(pts):
    lons = [p[0] for p in pts]; lats = [p[1] for p in pts]
    return ((min(lons) + max(lons)) / 2.0, (min(lats) + max(lats)) / 2.0)


def _arrow(draw, p1, p2, color, width=6, at=0.58, head=16):
    """Line p1->p2 with an arrowhead pointing toward p2, placed 'at' fraction along."""
    draw.line([p1, p2], fill=color, width=width)
    ax = p1[0] + (p2[0] - p1[0]) * at
    ay = p1[1] + (p2[1] - p1[1]) * at
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    for s in (1, -1):
        bx = ax - head * math.cos(ang - s * math.radians(28))
        by = ay - head * math.sin(ang - s * math.radians(28))
        draw.line([(ax, ay), (bx, by)], fill=color, width=width)


def _pin(draw, xy, n, color, r=17):
    """Numbered circular pin at pixel xy."""
    x, y = xy
    draw.ellipse([x - r - 2, y - r - 2, x + r + 2, y + r + 2], fill=(255, 255, 255))
    draw.ellipse([x - r, y - r, x + r, y + r], fill=color, outline=(255, 255, 255), width=3)
    f = _font(int(r * 1.15))
    t = str(n)
    try:
        bb = draw.textbbox((0, 0), t, font=f); tw, th = bb[2] - bb[0], bb[3] - bb[1]
        oy = bb[1]
    except Exception:
        tw, th, oy = f.getsize(t)[0], f.getsize(t)[1], 0
    draw.text((x - tw / 2, y - th / 2 - oy), t, font=f, fill=(255, 255, 255))


def render_map(pts, out_path, color, w=920, h=640, line_color="#3b6fd6"):
    """pts = [(lng,lat), ...] in order. Renders basemap + arrowed route + numbered pins."""
    if not pts:
        return False
    m = StaticMap(w, h, url_template=TILE, padding_x=40, padding_y=40)
    center = _center(pts)
    zoom = _fit_zoom(pts, w, h)
    if len(pts) >= 2:
        m.add_line(Line(pts, line_color, 5))   # keeps extent sane; arrows drawn on top
    try:
        img = m.render(zoom=zoom, center=center).convert("RGBA")
    except Exception as e:
        print("  [skip] tile fetch failed (%s) - need internet at build time." % type(e).__name__)
        return False
    px = [(m._x_to_px(_lon_to_x(lo, m.zoom)), m._y_to_px(_lat_to_y(la, m.zoom))) for lo, la in pts]
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for a, b in zip(px, px[1:]):
        _arrow(d, a, b, color, width=6)
    for i, xy in enumerate(px, 1):
        _pin(d, xy, i, color)
    out = Image.alpha_composite(img, ov).convert("RGB")
    out.save(out_path, quality=90)
    return True


def day_points(day):
    pts = []
    for it in day.get("items", []):
        if it.get("type") == "stop" and it.get("geo"):
            g = it["geo"]; pts.append((float(g[0]), float(g[1])))
    return pts


def main():
    trip_path, assets = sys.argv[1], sys.argv[2]
    os.makedirs(assets, exist_ok=True)
    trip = json.load(open(trip_path, encoding="utf-8"))
    made = []

    # per-day maps
    for d in trip.get("days", []):
        pts = day_points(d)
        if len(pts) < 2:
            continue
        color = THEME_COLOR.get(d.get("theme", "green"), THEME_COLOR["green"])
        out = os.path.join(assets, "map_day%s.png" % d.get("no"))
        if render_map(pts, out, color):
            made.append(os.path.basename(out))

    # overview map: one point per day (day.geo, else mean of the day's stops)
    ov_pts = []
    for d in trip.get("days", []):
        if d.get("geo"):
            g = d["geo"]; ov_pts.append((float(g[0]), float(g[1])))
        else:
            pts = day_points(d)
            if pts:
                ov_pts.append((sum(p[0] for p in pts) / len(pts),
                               sum(p[1] for p in pts) / len(pts)))
    if len(ov_pts) >= 2:
        out = os.path.join(assets, "map_overview.png")
        if render_map(ov_pts, out, OVERVIEW_COLOR, w=920, h=900):
            made.append(os.path.basename(out))

    print("OK -> %d map(s): %s" % (len(made), ", ".join(made) if made else "(none)"))


if __name__ == "__main__":
    main()
