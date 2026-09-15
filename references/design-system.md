# Design system (taste-type: follow the template, don't freestyle)

The full CSS lives in `assets/template.html` (`<style>`). `build_html.py` only emits these existing classes. **Don't invent colors or change the layout** — ask the user first if a change is needed.

## Role
A travel guide for fellow travelers (and older relatives): warm, clear, information-dense but not cramped. Big text (readable on a phone), color-coded buttons, clean equal-height photos.

## Palette (warm: cypress green + lotus pink + sunset orange)
- Primary green `--green #2f5d50`; from day 2, switch to cypress brown (`.day2`) to separate days
- Ground `--cream #faf6ee`; white cards; text `--ink #332f29`
- Buttons: **Map = blue `#2f6fb3`**, **Website/info = green `#2f7d5f`**, **Parking = orange `#d1791f`** (color itself is the signal)
- Caution box `.roadnote` = orange with a left border; "don't go…" text uses red `.no`

## Components (build_html emits these)
1. `.cover`: gradient cover (title/subtitle, route nodes, 2–3 info chips)
2. `.panel` pre-trip: left = weather buttons (`.wbtn`, second one `.wbtn.c2` a different hue) + right = packing list `.wlist`
3. Per day: `.dayhead` (big "Day N") → `.mapfig` (route map + caption) → `.timeline`
4. Inside `.timeline`, alternating: `.leg` (🚗 drive time + which road) and `.stop` (stop card)
5. `.stop`: left `.timecol` (big arrival time / stay pill / leave) + right `.body` (name + category tag + zone, `.info` address/phone/hours, `.desc`, `.subspot` sub-points, `.pill-links` buttons + `.warn`) + below `.gallery` (photos; add `.solo` for a single photo) + optional `.routewrap` (route hint + image)
6. `.backup` fallback, `.footer`

## Type scale (already enlarged for readability — don't shrink)
body 17.5px, stop name 23px, arrival time 27px, buttons 15.5px, body text 16px.

## Print
`@media print` sets A4, a page break before each later day (`.day-break`), and keeps cards from splitting. Text drops to ~14px.

## Fonts / i18n
Font stack covers Latin + CJK (Noto Sans/Serif + Noto Sans/Serif TC + system fallbacks). `<html lang>` comes from `trip.json` `lang`. UI strings come from `labels` (English defaults).

## Responsive
At ≤560px the `.timecol` becomes a top row — still clean on a phone.
