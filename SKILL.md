---
name: travel-guide
description: Plan and produce a polished, shareable travel guide — a self-contained HTML page (images inlined) plus a print-ready A4 PDF. Two ways in. (1) PLAN IT: the user gives only dates, a start→end area, and party/personas (e.g. "elderly, step-free only" or "kids who love animals"); you plan a one-way, persona-fit itinerary, verify the facts, and build it. (2) POLISH IT: the user already has the stops/times and just wants it made nice. Either way it covers per stop the address, phone, hours, site, photos, description, Google Map and parking links; an arrive–stay–leave timeline; drive time and roads between stops; per-day route; weather links and a packing list. Output language follows the user. Use whenever the user says "plan me a trip / make a travel itinerary / trip guide / travel brochure", "just give you dates + area + who's going and you plan the route", "幫我規劃行程 / 排一趟旅遊 / 生成旅遊說明書 / 旅遊手冊 / 給旅伴看的行程 / 我只給日期地點人數幫我安排順路行程", or hands over a rough or detailed itinerary to turn into a finished deliverable.
---

# travel-guide

Produce a polished, information-rich, **shareable** travel guide: a **self-contained HTML** file (opens
with one tap) **plus** an **A4 PDF** for proofing. Reply in the user's language, plain words, semi-automatic
(show a short plan first, then build).

## Setup (first run on a new machine)
Run `python scripts/check_env.py` — it auto-installs Pillow + PyMuPDF if missing and checks for a browser.
Everything degrades gracefully: the guide **always builds with pure Python**; the PDF step falls back to
"print from a browser" if there's no Edge/Chrome; auto-verify is skipped if PyMuPDF is absent. So it won't
"die" on a blank machine — worst case a helper step is skipped with a one-line hint.

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
Add a `"geo": [lng, lat]` to each stop (and optionally each day) so step 2b can draw the route maps —
see `references/data-checklist.md`.

## 2. Photos → `scripts/process_images.py`
Pasted-in-chat images can't be read — have the user save photos into `photos/` named **`stop-seq`**
(`2-1.jpg`), maps `map_dayN.png`, route hints `route_<stop>.png`. In PLAN mode the stops are AI-chosen, so
either build a first draft **without photos** (galleries are optional) or collect them **after** the plan is
confirmed.
```
python scripts/process_images.py photos assets
```

## 2b. Route maps (numbered pins + direction arrows) → `scripts/make_route_map.py`
A "tap to open Google Maps" button doesn't show, at a glance, that the trip runs **one-way** and where
each stop sits **locally**. This draws that picture: a real OSM basemap with **numbered pins in visiting
order** joined by **arrows**. It reads the `geo` coords from `trip.json` and writes:
- `assets/map_dayN.png` — that day's stops, pinned 1,2,3… and arrowed (pin color follows the day theme).
- `assets/map_overview.png` — one pin per day across the whole region, arrowed in day order (the corridor).
```
python scripts/make_route_map.py trip.json assets
```
Then point each day's `map.img` at the image and keep the tappable route link inside the caption, e.g.
`"map": { "img": "map_day2", "caption": "…<br>🗺 <a href='https://www.google.com/maps/dir/…'>本日路線</a>" }`.
Put `map_overview` on Day 1 (the departure day) as a whole-trip orientation. Needs internet at build time
(tiles); if it can't fetch, it skips the map with a hint and the guide still builds. A user-supplied
`map_dayN.png` screenshot still wins if present (V1 behavior) — this only fills the gap when there isn't one.

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

## 5. Deliver — a tappable LINK is THE deliverable (do NOT hand over the HTML file to share)
**This is fixed, not a preference.** An HTML file sent as an attachment (Claude file card, email, and
especially **LINE / WhatsApp**) does **not** open inline — the phone treats it as a download, sometimes
wrapped in a **zip**, and the recipient can't just tap it. Every "it came as a zip / won't open in LINE"
complaint is this mistake. So:

1. **Publish the self-contained `guide.html` as a hosted page / Artifact and give the user the URL.** That
   link opens on any phone with one tap and forwards cleanly through LINE/WhatsApp. This link **is** the
   product — lead with it, paste it plainly.
2. **Re-publish to the SAME URL** on every later edit, so a link the user already forwarded keeps working
   (mobile-cache caveat: `gotchas.md` #5). Never announce a new URL for an edit of the same trip.
3. **Tell the user how to make it forwardable:** an Artifact is **private by default** — they must open the
   page's **Share** menu and turn on the public/shareable link once, then anyone they send it to can open it
   (no login). If they need a permanent public link they own, offer **GitHub Pages** (`gotchas.md` #5).
4. **Do NOT push the raw `.html` file as the way to share.** Only offer a file for one reason: the **PDF**,
   for printing / offline. If there is genuinely no way to publish a link in this environment, say so
   explicitly, hand over the HTML file, and give the GitHub Pages steps — don't silently fall back to a file.
5. **When a GitHub Pages host is set up, publish to BOTH and give BOTH links:** the **Artifact** URL (instant,
   lives on the user's Claude account, easy for you to re-edit) *and* the **GitHub Pages** URL (permanent,
   user-owned, opens for anyone with no login — the best link to forward in LINE). One repo, one folder per
   trip holding `index.html`, so the URL is clean (`…/travel-guides/<trip>/`); re-push the same folder to keep
   the same URL. Commit with the user's GitHub **noreply** email (a real email trips GitHub's push privacy block).

Walk through `references/gotchas.md` once before delivering.

## Follow the design system, and always test
Layout/colors/components are fixed in `references/design-system.md` (CSS in `assets/template.html`) — don't
freestyle. Run one real case end to end before saying it's done.
