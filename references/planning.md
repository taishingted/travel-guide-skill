# V2 planning brain — from 3 inputs to a confirmed itinerary

V2 lets the user give only **3 things** and have *you* (the agent) plan the trip, verify the facts, and
fill the V1 `trip.json`. **You are the planner — not an external model.** Plan in-context and use web
search to check every real-world fact. Do not fabricate.

## The 3 inputs
1. **Dates** — start date + number of days (e.g. "2026/10/15–16, 2 days 1 night").
2. **Range** — start point, rough area, end/turnaround point (e.g. "from Taipei down the Tai-3 road to Sanyi & Dahu, ending Taichung West").
3. **Party & personas** — group size + attributes/constraints (e.g. "4 adults incl. a 70-yo with knee trouble — needs flat, step-free, dedicated parking; prefers scenic restaurants").

## How to plan (do this, in order)

1. **Turn the range into a one-way corridor.** Lay stops along the main road (freeway / expressway /
   provincial road) in travel order. **No backtracking** — each leg moves toward the end point.
2. **Pace for the party.** With elderly/children along, keep each drive leg to **~45–60 min**; insert a
   rest stop / scenic toilet when a leg is longer. Don't over-pack a day; leave slack.
3. **Persona-fit filtering** (see table below) — pick stops that fit the constraints; drop the ones that don't.
4. **Assign realistic times**: arrive / stay / leave per stop, and a drive time + which road for each leg.
   If you are not sure of a distance, say so — don't invent precision.
5. **Verify every fact with web search**: address, phone, opening hours, whether it's step-free / has
   parking, seasonal availability (e.g. strawberry picking). If something can't be confirmed, write
   **"please verify"** — never guess.

## Persona-fit rules (extend as needed)

| Persona | Prefer | Avoid |
|---|---|---|
| **Elderly / limited mobility** | flat, step-free paths; dedicated parking; shaded seating; short walks; warm/light meals | long stair climbs; long walks; long single drives; rushed pacing |
| **Young children** | animal/petting farms, factory tours, lawns & playgrounds | long museum-only stops; tight schedules (leave nap/snack slack) |
| **Foodies / couples** | signature local food, scenic cafés/restaurants | generic chains |
| **Friends / active** | viewpoints, short hikes, markets | (few limits — just keep it one-way) |

State, in each stop's `desc` or a `warn`, *why* it fits (e.g. "flat boardwalk, step-free, own car park").

## The confirmation checkpoint (semi-automatic — do NOT skip)

Going straight from 3 inputs to a finished HTML will disappoint. Instead:

1. Produce a **plain-text draft** first: per day, the ordered stops with rough times, drive legs, and a
   one-line "why it fits the party". Keep it short and scannable.
2. **Show it to the user and ask them to confirm or tweak** (swap a stop, change pace, add a must-go).
   The user knows the region — they catch a non-one-way route or a bad fit instantly.
3. Only after they're happy, expand into the full `trip.json` (per `data-checklist.md`), then run the
   V1 pipeline.

> A "fast mode" (skip the checkpoint) is fine only if the user explicitly asks. Default = confirm first.

## Photos in V2 (the stops are AI-chosen, so plan first)
The user can't pre-name photos for stops they haven't seen yet. So:
- Build a **first draft with no photos** (galleries are optional — omit `photos` and the card still looks good), or
- After the plan is confirmed, ask the user to save photos for the chosen stops using the **`stop-seq`**
  naming from `data-checklist.md`, then rerun `process_images.py` + `build_html.py`.

## Route maps in V2 (no pre-drawn map exists)
Instead of a hand-drawn county map, give each day a **Google Maps directions link** so the route is still
tappable:
```json
"map": { "link": "https://www.google.com/maps/dir/?api=1&origin=<start>&destination=<end>&waypoints=<stop|stop|stop>&travelmode=driving",
         "caption": "One-way route: <start> → ... → <end>; mostly on <road>. Tap to open in Google Maps." }
```
`build_html.py` renders a "route" button when `map.link` is set and no `img` exists. The user can still
drop a screenshot named `map_dayN.png` later to add a visual map (V1 behavior).

## Global trips (this skill is not Taiwan-only)

The planning logic, rendering, and links are built to work worldwide. Adapt these per destination country:

- **Maps** — a Google Maps directions link works **worldwide except mainland China**. In China, use a local
  map instead (Amap 高德地图 / Baidu 百度地图) for both the day route link and per-stop map links.
- **Weather** — link to the **destination country's** forecast, not a fixed Taiwan source.
  `https://www.google.com/search?q=<city>+weather+forecast` auto-localizes and works everywhere **except
  China**; you may instead point at the national service where it's better known (e.g. JMA / tenki.jp in
  Japan, Met Office in the UK, weather.gov in the US, 中央氣象署 in Taiwan). For China, use a local site
  (e.g. weather.com.cn).
- **Descriptions & sources** — write each stop's `desc` from credible **local-language sources** for the
  destination (the official tourism board, local review/blog platforms — e.g. Japanese travel blogs /
  Tabelog, Korean Naver, local Google reviews), not only English or Taiwan sources. Prefer a local
  source for hours/closures too, and link a good one as the 🔗 info button.
- **Roads** — describe roads in the **local** vocabulary (Interstate / A-road / autoroute / 高速 / 국도),
  not Taiwan's 國道/縣道.
- **Currency & units** — use the local currency and units in prices/notes.
- **Output script & fonts** — `template.html`'s font stack covers Latin + Traditional Chinese. If the
  output language uses another script (Japanese kana, Korean, Thai, Arabic, Cyrillic, Devanagari…), add the
  matching Noto font to the Google-Fonts `<link>` in `assets/template.html`, and set `dir="rtl"` for
  right-to-left languages.

## Don't take these shortcuts (block them)

| Tempting shortcut / inner voice | Reality |
|---|---|
| "I'll just fill in a plausible address/phone" | Fabrication sends people to the wrong place. Search it, or write "please verify". |
| "The route looks roughly right, skip the check" | Roughly-right routes backtrack. Verify the geography or let the user confirm. |
| "The user gave 3 inputs — just output the final HTML" | The confirmation checkpoint is the point of V2. Show the draft first. |
| "This stop is famous, no need to check hours/season" | Hours and seasons change; strawberry fields close out of season. Check. |
| "It probably fits the elderly" | "Probably" isn't step-free. Confirm the access, or say it needs care. |
