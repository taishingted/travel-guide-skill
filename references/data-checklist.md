# Data checklist (fill every field before writing trip.json)

Two kinds: **the user must supply**, and **you fill in**. Don't leave gaps.

## 🟦 User must supply

### Whole trip
- `title`, `subtitle`, `eyebrow` (small caps on the cover, e.g. "KYOTO · JAPAN · 1 DAY")
- `lang` (e.g. "en", "zh-Hant") and, for non-English output, a `labels` object to translate UI strings
- `counties` (used to build weather links & pick the matching map)
- `route_summary` (the node chips on the cover, e.g. ["Kyoto Station","Fushimi Inari",...])
- `cover_meta` (2–3 info blocks: meet, getting around, return)

### Each day
- `no`, `date` (include the weekday if relevant), `flow` (e.g. "Kyoto"), `range` (areas passed)
- `theme`: `"green"` (default) or `"wood"` (switch color from day 2 to visually separate days)
- `map`: `{"img":"map_day1","caption":"..."}` — route base image + caption (how you drive, which areas, which highways/roads, whether it doubles back)
- `backup` (optional): a one-line fallback plan

### Each stop (`items` with type=stop)
- `name`, `zone` (area/district), `tag` (`cls`: spot / food / nat / stay / trans, plus `text`)
- `arr`, `lbl` (time label: Arrive / Lunch / Start / Check-in …), `stay` (optional), `dep` (optional)
- `photos`: array of photo ids, e.g. `["2-1","2-2"]` (**stop-seq**; pasted images can't be read — they must be saved as files)

### Between stops (`items` with type=leg)
- `time` (e.g. "~27 min"), `road` (which road, e.g. "JR Nara Line → Inari"), `icon` (optional 🚗 🚆 🚌 🚶)

## 🟩 You fill in (don't make the user look these up)

- `info`: per-stop address 📍, phone ☎, hours 🕘 (**look up & verify**; if not found write "please verify" — **never fabricate**; a wrong address sends people to the wrong place)
- `desc`: 1–3 sentence description (local highlight, signature dish, must-see)
- `links`: button array. Conventions:
  - Google Map → `{"text":"🗺 Google Map","url":"https://www.google.com/maps/search/?api=1&query=<place or address>"}` (no `cls` = blue)
  - Parking → `{"cls":"park","text":"🅿️ Parking","url":"<parking Google Map link>"}` (orange)
  - Official / info → `{"cls":"ghost","text":"🔗 Website","url":"..."}` (green)
- `warn` (optional): one orange caution line, e.g. "⚠️ Stop at the pin — don't drive past it"
- `subspots` (optional): a stop with several sub-points, each `{"st":"title","html":"body with address/phone/map link"}`
- `route_note` (optional): a driving-route hint + one route image → `{"html":"...","img":"route_8"}`
- Whole-trip `weather` (build `https://www.google.com/search?q=<place>+weather+forecast`)
- Whole-trip `packing`: suggest from season + trip type (flowers → sun/insect protection, night views, overnight → toiletries, mountains → light jacket…)

## Building Google Map links
When you only have a name: `https://www.google.com/maps/search/?api=1&query=` + place (with area). If the user already has a `maps.app.goo.gl` short link, use theirs.
