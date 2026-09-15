#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把來源照片整理進 assets/。
用法: python process_images.py 旅遊圖片 assets
命名規則(來源檔):
  畫廊照片 = 站號-序號  例 2-1.jpg / 2-2.png  -> 裁成統一 3:2(780x520) -> assets/ph_2-1.jpg
  地圖     = map_dayN   例 map_day1.png         -> 縮寬<=1200 保留比例   -> assets/map_day1.jpg
  站內路線 = route_站號 例 route_8.png          -> 縮寬<=1200 保留比例   -> assets/route_8.jpg
為什麼要先裁成 3:2: 並排照片同比例才會自動等高、乾淨，網頁不必靠 object-fit(無頭匯出會出包)。
"""
import sys, os, re, glob
from PIL import Image
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

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
            print("!! 跳過(讀不到):", f, e); continue
        # 洗到全新白底畫布，去掉任何殘留屬性(避免無頭匯出出包)
        canvas = Image.new("RGB", im.size, (255, 255, 255)); canvas.paste(im, (0, 0)); im = canvas
        if re.fullmatch(r"\d+-\d+", name):          # 畫廊照片
            crop_32(im).save(os.path.join(dst, "ph_" + name + ".jpg"), quality=85)
            out = "ph_" + name + ".jpg"
        else:                                        # 地圖 / 路線 / 其他
            resize_w(im).save(os.path.join(dst, name + ".jpg"), quality=88)
            out = name + ".jpg"
        n += 1
        print("  %-16s -> %s" % (os.path.basename(f), out))
    print("完成，共處理 %d 張 -> %s" % (n, dst))

if __name__ == "__main__":
    main()
