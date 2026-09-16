#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepare source photos into assets/.
Usage: python process_images.py photos assets
Naming (source files):
  gallery photo = stop-seq   e.g. 2-1.jpg / 2-2.png  -> crop to uniform 3:2 (780x520) -> assets/ph_2-1.jpg
  map           = map_dayN   e.g. map_day1.png        -> width<=1200, keep aspect      -> assets/map_day1.jpg
  route hint    = route_stop e.g. route_8.png         -> width<=1200, keep aspect      -> assets/route_8.jpg
Why pre-crop to 3:2: side-by-side photos with the same ratio auto-align to equal height, so the
page can use plain width:100% and avoid object-fit (which headless PDF export mishandles).
"""
import sys, os, re, glob
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
try:
    from PIL import Image
except Exception:
    print("This step needs Pillow.  Install:  pip install Pillow")
    print("(If you have no photos, you can skip this step — build_html works without images.)")
    sys.exit(0)

TARGET = 3 / 2  # 3:2

def crop_32(im):
    w, h = im.size
    if w / h > TARGET:
        nw = int(h * TARGET); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w / TARGET); y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
    return im.resize((780, 520), Image.LANCZOS)

def resize_w(im, maxw=1200):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    return im

def main():
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    n = 0
    for f in glob.glob(os.path.join(src, "*")):
        name, ext = os.path.splitext(os.path.basename(f))
        if ext.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
            continue
        try:
            im = Image.open(f).convert("RGB")
        except Exception as e:
            print("!! skip (unreadable):", f, e); continue
        # repaint onto a fresh white canvas to strip any residual metadata/quirks
        canvas = Image.new("RGB", im.size, (255, 255, 255)); canvas.paste(im, (0, 0)); im = canvas
        if re.fullmatch(r"\d+-\d+", name):          # gallery photo
            crop_32(im).save(os.path.join(dst, "ph_" + name + ".jpg"), quality=85)
            out = "ph_" + name + ".jpg"
        else:                                        # map / route / other
            resize_w(im).save(os.path.join(dst, name + ".jpg"), quality=88)
            out = name + ".jpg"
        n += 1
        print("  %-16s -> %s" % (os.path.basename(f), out))
    print("Done. Processed %d image(s) -> %s" % (n, dst))

if __name__ == "__main__":
    main()
