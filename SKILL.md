---
name: travel-guide
description: Turn a rough trip outline (dates, stops, order) into a polished, shareable travel guide — a self-contained HTML page (images inlined, one file) plus a print-ready A4 PDF. Covers, per stop, the address, phone, opening hours, official site, photos, description, Google Map and parking links; an arrive–stay–leave timeline; drive time and which road between stops; per-day route maps; pre-trip weather links and a packing list. Output language follows the user (set trip.json "lang"/"labels"). Use this whenever the user asks to "make a travel itinerary / trip guide / travel brochure / trip plan", "turn this rough plan into something nice for fellow travelers", "生成旅遊說明書 / 旅遊手冊 / 行程表 / 把行程排漂亮的 / 給旅伴看的手冊", or hands over a draft itinerary to polish into a finished deliverable.
---

# travel-guide

Turn a rough itinerary into a polished, information-rich, **shareable** travel guide:
a **self-contained HTML** file (single file, images inlined — opens with one tap) **plus** an **A4 PDF** for proofing.

> Reply to the user in their own language. Explain steps in plain words (say which button / which file), not paths or jargon. Work semi-automatically: show a short plan first, then build.

## Five-step flow (in order; a "state" decides when a step is done)

### 1. Gather trip data → write `trip.json`
Collect every field per `references/data-checklist.md`. Two kinds:
- **User must supply**: dates/day count, meet & return, each stop's name/area/category/order, arrive–stay–leave, drive time + which road between stops, **the photo files**, and per-county route-map base images.
- **You fill in**: address / phone / hours / description (look them up on the web; **if not found, write "please verify" — never fabricate**), Google Map links (build from the place name), weather links (from the county), packing list (suggest from season & trip type).
Set `"lang"` and, for non-English output, a `"labels"` object (see `references/example-trip.zh-TW.json`).

### 2. Collect photos → run `scripts/process_images.py`
**Images pasted into chat have no file path you can read** — ask the user up front to save photos into a `photos/` folder named **`stop-seq`** (e.g. stop 2 photo 1 = `2-1.jpg`); route maps `map_day1.png`; a per-stop route-hint image `route_<stop>.png`.
```
python scripts/process_images.py photos assets
```
(Gallery photos are auto-cropped to a uniform 3:2; maps keep their aspect.)

### 3. Build HTML → run `scripts/build_html.py`
```
python scripts/build_html.py trip.json assets guide.html            # self-contained (base64) = the file to share
python scripts/build_html.py trip.json assets guide_files.html --files   # external images = use THIS to print the PDF
```

### 4. Make PDF + verify → `make_pdf.py` then `verify_pdf.py`
```
python scripts/make_pdf.py guide_files.html guide.pdf
python scripts/verify_pdf.py guide.pdf
```
`verify_pdf.py` flags any page where a photo rendered too small. **If flagged → see `references/gotchas.md` #2: ask the user to re-save that one image**, then redo step 2.

### 5. Deliver
- Hand over the **self-contained HTML** as the deliverable and explain how to share it (see `gotchas.md` #5: mobile cache / publish a fresh link each version / GitHub Pages).
- Before delivering, walk through `references/gotchas.md` once.

## Follow the design system — don't freestyle
Layout, colors, cards, buttons and the timeline are specified in `references/design-system.md` (CSS lives in `assets/template.html`). This is a taste-type rule: follow the template; don't change colors or layout.

## Always test at the end
Run one real trip end to end, see where it breaks, then fix the files.
