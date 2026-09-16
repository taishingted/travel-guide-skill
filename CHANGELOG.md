# Changelog

All notable changes to this project. Format based on [Keep a Changelog](https://keepachangelog.com/).

## [v2.4.0] - 2026-09-16

**Route maps you can read at a glance** — see the one-way flow and where each stop sits.

### Added
- `scripts/make_route_map.py` — auto-draws route maps from `trip.json`: a real OSM basemap with
  **numbered pins in visiting order joined by direction arrows**. Writes `assets/map_dayN.png` (per day,
  pin color follows the day theme) and `assets/map_overview.png` (one pin per day across the whole region).
- New `"geo": [lng, lat]` field on stops (and optionally days) drives the maps — documented in
  `references/data-checklist.md`. Stops without `geo` are simply skipped; needs internet at build time,
  and degrades gracefully (map skipped, guide still builds) if tiles/staticmap are unavailable.
- SKILL step **2b** documents the map step; `staticmap` added to `check_env.py` + `requirements.txt`.

### Changed
- Step 5 (Deliver): when a GitHub Pages host is set up, publish to **both** and give **both** links —
  the Artifact URL (instant, on the user's account) and the GitHub Pages URL (permanent, user-owned,
  no-login, best for LINE). Locked the "never share the raw .html file" rule in harder.

## [v2.3.0] - 2026-09-16

**Deliver a shareable link, not just a file.**

### Changed
- **Step 5 (Deliver) now says: publish the self-contained HTML as a hosted page / Artifact and give the
  user its share link**, instead of only handing over the `.html` file. A bare file card has no Share
  button and is awkward to forward; this closes a real "the guide looks fine but I can't share it" gap.
  Falls back to handing over the file + GitHub Pages guidance when publishing isn't available. PDF still
  provided for print/offline.

## [v2.2.0] - 2026-09-16

**Portable & self-healing** — runs on a fresh machine without dying.

### Added
- `scripts/check_env.py` — checks and **auto-installs** Pillow + PyMuPDF, and detects a browser.
- `requirements.txt`; a "Setup on a fresh machine" section in README and SKILL.

### Changed
- **Graceful degradation everywhere**: `build_html.py` needs only the standard library (the guide always
  builds); `process_images.py` and `verify_pdf.py` now exit with a one-line install hint instead of
  crashing when Pillow / PyMuPDF are missing; `make_pdf.py` already falls back to browser printing.

## [v2.1.0] - 2026-09-16

**Global coverage.**

### Added
- **Automatic fonts & text direction by language.** `build_html.py` picks the matching Noto font from
  `trip.json` `lang` — Latin/European, zh-Hant, zh-Hans, ja, ko, th, ar, he — and sets `dir="rtl"` for
  Arabic/Hebrew. Any language renders; add one line to `FONT_PROFILES` for a new script.
- **China map fallback** (Google Maps is blocked there): tested name-based links — Amap
  `amap.com/search?query=…` / Baidu `map.baidu.com/search/…` per stop.
- Weather localized to the destination country; descriptions sourced from local-language sites.

## [v2.0.0] - 2026-09-16

**V2 — plan from 3 inputs.** The skill can now plan the trip, not just format it.

### Added
- **PLAN mode**: from just **dates + start→end range + party/personas**, the agent plans a **one-way,
  persona-fit** itinerary, **web-verifies every fact**, shows a **draft to confirm**, then builds.
- `references/planning.md` — the planning brain: persona-fit rules, one-way routing & pacing, the
  confirmation checkpoint, photo/route strategy for AI-chosen stops, and an anti-fabrication table.
- `references/example-plan.zh-TW.json` — a persona-planned sample (elderly-friendly Taipei→Sanyi→Taichung).
- Day route can now be a **Google Maps directions link** (`map.link`) when no drawn map exists —
  `build_html.py` renders a route button.
- **Global support** documented: maps worldwide except China (use Amap/Baidu there); weather localized to
  the destination country; descriptions from local-language sources; local road vocabulary; font/RTL notes
  for non-Latin scripts.

### Design decision
- The **planner is the agent itself + web search — no external model, no API key**. A one-shot small-model
  call can't look anything up and would fabricate addresses, which this skill must never do.

## [v1.1.0] - 2026-09-16

### Changed
- **Internationalized.** All docs, code comments and script output are now in English.
- Output language is configurable via `trip.json` `lang` + `labels` (English by default).
- Font stack and `<html lang>` generalized for Latin + CJK.

### Added
- `references/example-trip.json` — a default **English** sample (Kyoto one-day).
- `references/example-trip.zh-TW.json` — the Tainan · Chiayi trip as a Traditional-Chinese sample (shows the `lang`/`labels` override).
- `index.html` + GitHub Pages: a one-tap live demo at https://taishingted.github.io/travel-guide-skill/

## [v1.0.0] - 2026-09-15

第一版（V1）。從一次真實成果（台南・嘉義兩天一夜）反向拆解而成。

### 功能
- 五步流程：蒐集資料 → 處理照片 → 產出 HTML → 印 PDF 並驗證 → 交付
- 產出**自包含 HTML**（單檔、圖片內嵌，可分享）＋ **A4 PDF**（校稿）
- 涵蓋：封面、行前天氣＋攜帶清單、每日路線地圖、時間軸（到達–停留–離開）、
  每站地址／電話／營業時間／介紹／照片／Google Map／停車場／官網、站間交通與走哪條路、開車路線提醒
- `verify_pdf.py`：自動偵測「照片被無頭匯出畫小」的頁（下緣空白比例判定）
- `references/example-trip.json`：台南嘉義完整範例（schema ＋ 測試資料）
- `demo/`：台南嘉義範例成品（HTML ＋ PDF），展示實際效果

### 之後想做（V2 候選）
- （待補：使用者要加的優化功能）
