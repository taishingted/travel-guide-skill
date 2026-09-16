# travel-guide

> A Claude Code / Claude Agent **Skill** that plans and produces a polished, shareable travel guide — a **self-contained HTML** page (images inlined, one file) plus a print-ready **A4 PDF**.

**Two ways in:**

- **🧠 Plan it (V2)** — give only **3 things**: dates, a start→end area, and who's going (personas). The skill plans a **one-way, persona-fit** route, **verifies the facts on the web**, shows you a draft to confirm, then builds it.
- **🎨 Polish it (V1)** — you already have the stops and times; the skill fills in details and makes it beautiful.

Either way it covers, per stop: address, phone, hours, official site, photos, description, Google Map / parking links; an **arrive–stay–leave** timeline; drive time and roads between stops; a per-day **route**; pre-trip **weather links** and a **packing list**. **Output language follows the user** (`lang` + `labels` in `trip.json`).

---

## 🎬 Live demo (one tap)

**➡️ https://taishingted.github.io/travel-guide-skill/**

Opens a finished guide right in the browser — nothing to download. The `demo/` folder has both a **detail-driven** sample (Tainan · Chiayi) and a **persona-planned** sample (Taipei → Sanyi → Taichung, elderly-friendly), plus downloadable PDFs.

---

## 🧠 V2 — plan from 3 inputs

Give the skill:
1. **Dates** (start + day count)
2. **Range** (start → rough area → end/turnaround)
3. **Party & personas** (group size + constraints, e.g. "70-yo, step-free only" or "kids who love animals")

The **agent itself is the planner** — it plans in-context and uses **web search to verify every real-world fact** (address, phone, hours, step-free access, season). No external model, **no API key** — this is deliberate: a one-shot small-model call can't look anything up and would fabricate addresses, which this skill must never do (see `references/gotchas.md` #7). Then it **shows you a short draft to confirm** before building (`references/planning.md`).

```
User: "Oct 15, one day. Taipei down to Sanyi/Dahu, ending Taichung West.
       4 adults incl. a 70-yo with knee trouble — step-free, own parking, scenic lunch."
Skill: → plans a one-way, step-free route, web-verifies each stop
       → shows a draft to confirm → builds the HTML + PDF
```

## 📦 Structure

```
travel-guide/
├── SKILL.md                        # five-step flow + the two doors (kept short)
├── references/
│   ├── planning.md                 # [V2] the planning brain: personas, one-way routing, confirm checkpoint
│   ├── data-checklist.md           # fields to collect; user-given vs. you-fill-in
│   ├── design-system.md            # layout / colors / components (follow the template)
│   ├── gotchas.md                  # hard-won pitfalls
│   ├── example-trip.json           # English sample (Kyoto) = the data schema
│   ├── example-trip.zh-TW.json     # Traditional-Chinese sample (Tainan · Chiayi)
│   └── example-plan.zh-TW.json     # [V2] persona-planned sample (route via Google Maps link, no photos)
├── scripts/
│   ├── process_images.py           # crop photos to a uniform 3:2, wash into assets/
│   ├── build_html.py               # build HTML from trip.json (base64 / --files); day route can be an image OR a Google Maps link
│   ├── make_pdf.py                 # print an A4 PDF with headless Edge/Chrome
│   └── verify_pdf.py               # render pages + auto-flag any "photo drawn too small" page
└── assets/
    └── template.html               # page skeleton + CSS
```

## 🚀 Pipeline

```bash
# (V2 only) plan + confirm the itinerary → write trip.json  [the agent does this with web search]
python scripts/process_images.py photos assets            # if you have photos (stop-seq naming)
python scripts/build_html.py trip.json assets guide.html            # self-contained = the file to share
python scripts/build_html.py trip.json assets guide_files.html --files   # external images = print the PDF from THIS
python scripts/make_pdf.py guide_files.html guide.pdf
python scripts/verify_pdf.py guide.pdf
```

### Setup on a fresh machine
```bash
python scripts/check_env.py     # auto-installs Pillow + PyMuPDF if missing; checks for a browser
```
**Requirements** are all optional and degrade gracefully — it won't die on a blank machine:
- **Python 3** (standard library only) → `build_html.py` always builds the guide.
- **[Pillow](https://pypi.org/project/pillow/)** → auto-crops photos (`process_images.py`); skip if you have no photos.
- **[PyMuPDF](https://pypi.org/project/PyMuPDF/)** → auto-verifies the PDF (`verify_pdf.py`); without it, eyeball the PDF in a browser.
- **Edge / Chrome** → prints the A4 PDF (`make_pdf.py`); without it, open the HTML and Print → Save as PDF.

## 🧠 Gotchas (from `references/gotchas.md`)

1. **Some image files break Edge's headless PDF export** (photo drawn tiny, white below) — depends only on the file's pixel data; re-saving it once fixes it. `verify_pdf.py` auto-detects via the bottom-strip background ratio.
2. **Verify against a real render** (PyMuPDF per-page), not a headless full-page screenshot.
3. **Pre-crop side-by-side photos to a uniform 3:2** + `width:100%`; don't rely on `object-fit:cover`.
4. **A phone showing an old version = cache** — publish a fresh URL per version, or use GitHub Pages.
5. **Never fabricate** an address/phone/hours — write "please verify". Wrong data sends people to the wrong place.

## Design philosophy

Shaped with six skill-design rules: description is bait (fires reliably), body is a map (short), deterministic work goes to scripts, explain *why* over shouting in caps, block the tempting shortcuts up front, and always dry-run test.

## License

[MIT](LICENSE)
