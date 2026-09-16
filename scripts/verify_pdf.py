#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify a PDF: render each page to an image (for a human/Claude to eyeball) and auto-flag pages
where a photo rendered too small.
Usage: python verify_pdf.py guide.pdf [pdf_pages]

Detection (important): headless export sometimes draws certain photos in the top-left of their box
with a big white gap below (see gotchas.md #2). The image *box* size is identical whether good or
broken, so box size can't tell them apart — instead check whether the bottom strip of the box is
nearly all background. Measured: good photo bottom-strip background ratio 0.01-0.05, broken = 1.0.
Threshold = 0.85.
A flagged page -> open its PNG to confirm; if it really shrank -> ask the user to re-save that
source photo once (Save As) and rerun process_images / build_html / make_pdf.
"""
import sys, os
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
try:
    import pymupdf
except Exception:
    print("This step needs PyMuPDF.  Install:  pip install PyMuPDF")
    print("(Skipping auto-verify — open the PDF/HTML in a browser to eyeball the photos.)")
    sys.exit(0)
try:
    from PIL import Image
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False

ZOOM = 2.0
BG = (252, 250, 244)  # near white / cream ground

def near_bg_ratio(im, box):
    data = im.crop(box).resize((40, 10)).convert("RGB").tobytes()
    n = len(data) // 3
    if n == 0:
        return 0.0
    hit = sum(1 for j in range(0, n * 3, 3)
              if abs(data[j]-BG[0]) + abs(data[j+1]-BG[1]) + abs(data[j+2]-BG[2]) < 40)
    return hit / n

def main():
    pdf = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "pdf_pages"
    os.makedirs(out, exist_ok=True)
    d = pymupdf.open(pdf)
    bad = []
    for i in range(d.page_count):
        page = d[i]
        page.get_pixmap(dpi=90).save(os.path.join(out, "page_%02d.png" % (i + 1)))
        if not HAVE_PIL:
            continue
        pix = page.get_pixmap(matrix=pymupdf.Matrix(ZOOM, ZOOM))
        im = Image.frombytes("RGB" if pix.n < 4 else "RGBA",
                             (pix.width, pix.height), pix.samples).convert("RGB")
        for info in page.get_image_info():
            x0, y0, x1, y1 = [v * ZOOM for v in info["bbox"]]
            w, h = x1 - x0, y1 - y0
            ar = w / max(h, 1)
            if not (1.2 < ar < 1.8 and 120 < w / ZOOM < 340):   # gallery photos only (skip maps/route images)
                continue
            if near_bg_ratio(im, (int(x0), int(y1 - h * 0.22), int(x1), int(y1))) > 0.85:
                bad.append(i + 1)
                break
    print("Rendered pages -> %s/page_XX.png (%d pages)" % (out, d.page_count))
    if not HAVE_PIL:
        print("(Pillow not installed; skipped auto-detection. Open pages with photos to check by eye.)")
    elif bad:
        print("\n[!] Photos look shrunk on page(s): " + ", ".join(map(str, bad)))
        print("    -> Open that page PNG to confirm; if shrunk, ask the user to re-save that stop's")
        print("       source photo once (Save As), then rerun process_images / build_html / make_pdf.")
    else:
        print("\n[OK] No shrunk photos detected. Still worth eyeballing a page or two with photos.")

if __name__ == "__main__":
    main()
