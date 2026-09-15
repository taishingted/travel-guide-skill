#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 HTML 印成 A4 PDF(用系統的 Edge/Chrome 無頭列印)。
用法: python make_pdf.py 行程_files.html 行程.pdf
注意: 一定要用「外部圖檔版」HTML(build_html.py 加 --files 產的)來印，
      不要用 base64 版——見 references/gotchas.md 第 2 條。
"""
import sys, os, subprocess, shutil
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

def find_browser():
    for p in CANDIDATES:
        if os.path.exists(p):
            return p
    for name in ("msedge", "chrome", "chromium", "google-chrome", "chromium-browser"):
        p = shutil.which(name)
        if p:
            return p
    return None

def main():
    html_in, pdf_out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    br = find_browser()
    if not br:
        print("找不到 Edge/Chrome，請改用瀏覽器開 HTML → 列印 → 另存 PDF"); sys.exit(1)
    url = "file:///" + html_in.replace("\\", "/")
    cmd = [br, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
           "--virtual-time-budget=8000", "--print-to-pdf=" + pdf_out, url]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(pdf_out):
        print("OK -> %s (%.1f KB)" % (pdf_out, os.path.getsize(pdf_out) / 1024))
        print("下一步: python verify_pdf.py \"%s\"" % pdf_out)
    else:
        print("印失敗，請改用瀏覽器列印另存 PDF")

if __name__ == "__main__":
    main()
