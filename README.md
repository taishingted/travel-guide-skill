# travel-guide

> A Claude Code / Claude Agent **Skill** that turns a rough trip outline into a polished, shareable travel guide — a **self-contained HTML** page (images inlined, one file) plus a print-ready **A4 PDF**.

Give it dates, stops and an order; it produces a finished guide with per-stop address, phone, hours, description, photos, Google Map / parking / website buttons, an **arrive–stay–leave** timeline, drive time and which road between stops, per-day **route maps**, pre-trip **weather links** and a **packing list**.

**Output language follows the user** — set `lang` and a `labels` object in `trip.json` (English by default; a full Traditional-Chinese override ships in `references/example-trip.zh-TW.json`).

Reverse-engineered on 2026-09-15 from a real deliverable (a two-day Tainan · Chiayi trip) and shaped with six skill-design rules.

---

## 🎬 Live demo (one tap)

**➡️ https://taishingted.github.io/travel-guide-skill/**

Opens the finished guide right in the browser — nothing to download or install. The `demo/` folder also has a downloadable PDF. (The demo output is in Traditional Chinese, showing the skill handles CJK end to end.)

---

## ✨ What it produces

- **Cover**: title/subtitle, route nodes, meet / getting-around / return chips
- **Pre-trip panel**: weather links (built from the location) + a packing list (suggested from season & trip type)
- **Per day**: a route map (highways/roads, areas passed) + a timeline
- **Per stop**: arrive–stay–leave times, address / phone / hours, description, photos, **color-coded buttons** (🗺 Google Map / 🅿️ Parking / 🔗 Website), driving-route hints
- **Two outputs, one template**: a self-contained HTML to share + a PDF to proof

## 📦 Structure

```
travel-guide/
├── SKILL.md                     # five-step flow (kept short; details in references/)
├── references/
│   ├── data-checklist.md        # fields to collect; what the user gives vs. what you fill in
│   ├── design-system.md         # layout / colors / components (follow the template)
│   ├── gotchas.md               # hard-won pitfalls (see below)
│   ├── example-trip.json        # default English sample = the data schema
│   └── example-trip.zh-TW.json  # Traditional-Chinese sample (shows lang + labels override)
├── scripts/
│   ├── process_images.py        # crop photos to a uniform 3:2, wash into assets/
│   ├── build_html.py            # build HTML from trip.json (base64 self-contained / --files external)
│   ├── make_pdf.py              # print an A4 PDF with headless Edge/Chrome
│   └── verify_pdf.py            # render pages + auto-flag any "photo drawn too small" page
└── assets/
    └── template.html            # page skeleton + CSS
```

## 🚀 Usage

1. Save photos into `photos/` named **`stop-seq`** (e.g. stop 2, photo 1 = `2-1.jpg`); route maps `map_day1.png`; per-stop route hints `route_<stop>.png`.
2. Have Claude collect the trip into `trip.json` per `references/data-checklist.md` (look up missing address/phone; **if not found, write "please verify" — never fabricate**).
3. Run:
   ```bash
   python scripts/process_images.py photos assets
   python scripts/build_html.py trip.json assets guide.html            # self-contained = the file to share
   python scripts/build_html.py trip.json assets guide_files.html --files   # external images = print the PDF from this
   python scripts/make_pdf.py guide_files.html guide.pdf
   python scripts/verify_pdf.py guide.pdf
   ```
4. If `verify_pdf.py` flags a page, ask the user to **re-save that source photo once**, then rerun.

**Requirements**: Python 3, [Pillow](https://pypi.org/project/pillow/), [PyMuPDF](https://pypi.org/project/PyMuPDF/), and system Edge or Chrome (for headless PDF printing).

## 🧠 Gotchas (highlights from `references/gotchas.md`)

1. **Some image files break Edge's headless PDF export** — a photo is drawn tiny with a white gap below. It's unrelated to columns/format/size/CSS; it depends only on that file's pixel data — **re-saving the file once fixes it**. `verify_pdf.py` detects it via the bottom-strip background ratio (good 0.01–0.05, broken = 1.0).
2. **Verify against a real render** (PyMuPDF per-page), not a headless full-page screenshot (large images band).
3. **Pre-crop side-by-side photos to a uniform 3:2** + `width:100%`; don't rely on `object-fit:cover` (headless export mishandles it).
4. **A phone showing an old version = cache** — publish a fresh URL per version, or host on GitHub Pages.

## Design philosophy

Shaped with six skill-design rules: description is bait (fires reliably), body is a map (short), deterministic work goes to scripts, explain *why* instead of shouting in caps, block the tempting shortcuts up front, and always dry-run test.

## License

[MIT](LICENSE)
