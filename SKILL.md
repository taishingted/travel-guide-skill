---
name: travel-guide
description: Plan and produce a polished, shareable travel guide — a self-contained HTML page (images inlined) plus a print-ready A4 PDF. Two ways in. (1) PLAN IT: the user gives only dates, a start→end area, and party/personas (e.g. "elderly, step-free only" or "kids who love animals"); you plan a one-way, persona-fit itinerary, verify the facts, and build it. (2) POLISH IT: the user already has the stops/times and just wants it made nice. Either way it covers per stop the address, phone, hours, site, photos, description, Google Map and parking links; an arrive–stay–leave timeline; drive time and roads between stops; per-day route; weather links and a packing list. Output language follows the user. Use whenever the user says "plan me a trip / make a travel itinerary / trip guide / travel brochure", "just give you dates + area + who's going and you plan the route", "幫我規劃行程 / 排一趟旅遊 / 生成旅遊說明書 / 旅遊手冊 / 給旅伴看的行程 / 我只給日期地點人數幫我安排順路行程", or hands over a rough or detailed itinerary to turn into a finished deliverable.
---

# travel-guide

Produce a polished, information-rich, **shareable** travel guide: a **self-contained HTML** file (opens
with one tap) **plus** an **A4 PDF** for proofing. Reply in the user's language, plain words, semi-automatic
(show a short plan first, then build).

## Which door? (pick at the start)

- **The user gave only rough inputs** — dates, a start→end area, and who's going → **PLAN mode**: do step 0
  first (`references/planning.md`), get their OK, then continue.
- **The user already listed stops & times** → skip step 0, go straight to step 1 (this is V1 behavior).

## 0. PLAN from 3 inputs (only in PLAN mode) — read `references/planning.md`
From **dates + start→end range + party/personas**, *you* plan a **one-way, persona-fit** itinerary and
**verify every fact with web search** (you are the planner — not an external model). Then **show a short
plain-text draft and get the user's confirmation/tweaks BEFORE building**. Never fabricate: if an address /
phone / hours can't be confirmed, write "please verify".

## 1. Gather into `trip.json` — see `references/data-checklist.md`
Fill the schema (see `references/example-trip.json`, and `references/example-trip.zh-TW.json` for a localized
one). Set `lang` + `labels` for the output language. In PLAN mode this is the confirmed plan expanded into
full detail; in POLISH mode it's the user's given stops plus the facts you look up.

## 2. Photos → `scripts/process_images.py`
Pasted-in-chat images can't be read — have the user save photos into `photos/` named **`stop-seq`**
(`2-1.jpg`), maps `map_dayN.png`, route hints `route_<stop>.png`. In PLAN mode the stops are AI-chosen, so
either build a first draft **without photos** (galleries are optional) or collect them **after** the plan is
confirmed.
```
python scripts/process_images.py photos assets
```

## 3. Build HTML → `scripts/build_html.py`
```
python scripts/build_html.py trip.json assets guide.html            # self-contained (base64) = the file to share
python scripts/build_html.py trip.json assets guide_files.html --files   # external images = print the PDF from THIS
```

## 4. PDF + verify → `make_pdf.py` then `verify_pdf.py`
```
python scripts/make_pdf.py guide_files.html guide.pdf
python scripts/verify_pdf.py guide.pdf
```
If `verify_pdf.py` flags a page, see `references/gotchas.md` #2: ask the user to re-save that one image, then redo step 2.

## 5. Deliver
Hand over the **self-contained HTML** and explain how to share it (`gotchas.md` #5). Walk through
`references/gotchas.md` once before delivering.

## Follow the design system, and always test
Layout/colors/components are fixed in `references/design-system.md` (CSS in `assets/template.html`) — don't
freestyle. Run one real case end to end before saying it's done.
