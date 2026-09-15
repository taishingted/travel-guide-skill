#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Print an HTML file to an A4 PDF using the system's headless Edge/Chrome.
Usage: python make_pdf.py guide_files.html guide.pdf
Note: always print the "external-image" HTML (built with --files), NOT the base64 version.
      See references/gotchas.md #2.
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
        print("No Edge/Chrome found. Open the HTML in a browser and use Print -> Save as PDF."); sys.exit(1)
    url = "file:///" + html_in.replace("\\", "/")
    cmd = [br, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
           "--virtual-time-budget=8000", "--print-to-pdf=" + pdf_out, url]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(pdf_out):
        print("OK -> %s (%.1f KB)" % (pdf_out, os.path.getsize(pdf_out) / 1024))
        print("Next: python verify_pdf.py \"%s\"" % pdf_out)
    else:
        print("Print failed. Open the HTML in a browser and use Print -> Save as PDF.")

if __name__ == "__main__":
    main()
