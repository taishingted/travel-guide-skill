#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
驗證 PDF: 把每頁轉成圖(給 Claude 眼睛看)，並自動點名「照片被畫小」的頁。
用法: python verify_pdf.py 行程.pdf [pdf_pages]

偵測原理(重要): 無頭匯出對某些圖檔會把照片畫在框內左上角、下面留一大片白(見 gotchas 第 2 條)。
  圖片「框」的尺寸好壞一樣，所以不能用框大小判斷；要看「框內下緣是不是一片空白」。
  實測: 正常照片下緣空白比例 0.01~0.05，被畫小的 = 1.0。門檻取 0.85。
被點名的頁 -> Claude 打開該頁 PNG 確認; 若真的縮了 -> 請使用者把那站來源圖『另存新檔』重存一次再重跑。
"""
import sys, os
import pymupdf
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
try:
    from PIL import Image
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False

ZOOM = 2.0
BG = (252, 250, 244)  # 近白/米色底

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
            if not (1.2 < ar < 1.8 and 120 < w / ZOOM < 340):   # 只看畫廊照片(排除地圖/路線圖)
                continue
            if near_bg_ratio(im, (int(x0), int(y1 - h * 0.22), int(x1), int(y1))) > 0.85:
                bad.append(i + 1)
                break
    print("已輸出每頁圖 -> %s/page_XX.png (共 %d 頁)" % (out, d.page_count))
    if not HAVE_PIL:
        print("(未安裝 Pillow，略過自動偵測；請打開含照片的頁 PNG 人工確認)")
    elif bad:
        print("\n[!] 偵測到照片被畫小的頁：第 " + "、".join(map(str, bad)) + " 頁")
        print("    -> 打開該頁 PNG 確認；確認縮了就請使用者把那站來源照片『另存新檔』重存一次，")
        print("       再重跑 process_images / build_html / make_pdf。")
    else:
        print("\n[OK] 未偵測到被畫小的照片。仍建議打開一兩張含照片的頁 PNG 最後確認。")

if __name__ == "__main__":
    main()
