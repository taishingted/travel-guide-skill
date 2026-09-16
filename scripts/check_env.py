#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check (and optionally install) what this skill needs, so it runs on a fresh machine.
Usage:
  python check_env.py            # check + auto-install missing pip packages
  python check_env.py --check    # check only, don't install

Everything degrades gracefully — nothing here is fatal:
  Pillow      -> process_images.py (auto-crop photos) + make_route_map.py (draw pins/arrows). No photos/maps? not needed.
  staticmap   -> make_route_map.py (real OSM basemap for the route maps). Missing/offline? maps are skipped.
  PyMuPDF     -> verify_pdf.py (auto-check the printed PDF). Missing? eyeball it in a browser.
  Edge/Chrome -> make_pdf.py (print the A4 PDF). Missing? open the HTML and Print > Save as PDF.
  build_html.py needs only the Python standard library, so the guide itself ALWAYS builds.
"""
import sys, os, subprocess, shutil
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

def have(mod):
    try:
        __import__(mod); return True
    except Exception:
        return False

def pip_install(pkg):
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", pkg],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False

def find_browser():
    cands = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for p in cands:
        if os.path.exists(p):
            return p
    for n in ("msedge", "chrome", "chromium", "google-chrome", "chromium-browser"):
        p = shutil.which(n)
        if p:
            return p
    return None

def main():
    do_install = "--check" not in sys.argv
    print("Python:", sys.version.split()[0])
    ok = True
    for mod, pkg in [("PIL", "Pillow"), ("pymupdf", "PyMuPDF"), ("staticmap", "staticmap")]:
        if have(mod):
            print("  [ok] %s" % pkg)
            continue
        if do_install:
            print("  [..] installing %s ..." % pkg)
            if pip_install(pkg) and have(mod):
                print("  [ok] %s" % pkg)
                continue
        ok = False
        print("  [!!] %s missing  ->  pip install %s" % (pkg, pkg))
    br = find_browser()
    if br:
        print("  [ok] browser for PDF: %s" % br)
    else:
        print("  [!!] no Edge/Chrome  ->  PDF step falls back to: open the HTML, Print > Save as PDF")
    print("\nCore build (build_html.py) uses only the standard library — the guide always builds.")
    if ok and br:
        print("Environment ready. ✅")

if __name__ == "__main__":
    main()
