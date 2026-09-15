# Gotchas (walk through before delivering)

These are real, tested pitfalls — not theory. Skip any one and the guide breaks in front of the user.

## 1. Images pasted into chat have no readable file
When the user pastes photos into the conversation, **you have no file path to read**.
→ Up front, have them save photos into a `photos/` folder named `stop-seq` / `map_dayN` / `route_<stop>`. Don't spin a whole round only to find you can't reach the image.

## 2. Some image files break Edge's PDF export (photo drawn tiny, white below)
**Symptom**: the same HTML looks perfect in a real browser (phone/desktop), but exporting with headless Edge `--headless --print-to-pdf` draws **certain photos as a small block with a big white gap below**. It is unrelated to columns, format (JPG/PNG), size, or grid/flex — it depends only on that image file's pixel data (tested: re-saving the file once fixes it).
→ What to do:
- Always print the PDF from the **external-image HTML** (`--files`), never the base64 version.
- After printing, **always run `verify_pdf.py`**; for any flagged page, **ask the user to re-save that source image once** (Save As), then rerun from step 2.
- Don't waste time changing CSS / format / headless mode to fix it — that path doesn't work, already verified.

## 3. Verify against a real render, not a headless screenshot
A headless **full-page screenshot** distorts large images (exceeding the max drawing surface causes banding).
→ To confirm the layout is actually correct, use one of:
- `verify_pdf.py` (PyMuPDF renders each PDF page to an image — a true paginated render); or
- serve the folder over a local http server and open it in a real browser, then measure `img.getBoundingClientRect()` heights (>80px means filled).
- A hidden browser tab measures `window.innerWidth = 0` → all sizes read 0; set a viewport width first.

## 4. Pre-crop side-by-side photos; don't rely on object-fit
`process_images.py` center-crops all gallery photos to a uniform **3:2 (780×520)**. The page uses plain `width:100%`, **not `object-fit:cover`** (headless export mishandles cover). Same ratio + equal width = auto equal height, clean.

## 5. A phone showing the old version = cache; publish a fresh link per version
A claude.ai artifact gets locked by a service worker on mobile; appending `?v=5` **does not** beat it.
→ After an update, publish to a **brand-new URL** (a new file name = a new URL; a phone that never opened it has no old cache).
→ Long term: host on **GitHub Pages** (serves your HTML as-is, lives in your own repo — the closest thing to a permanent link).

## 6. Two outputs, one template
- **Self-contained HTML (base64)** = the file to share (single file, opens with one tap).
- **PDF** = for proofing (printed from the external-image version).
- Both come from one `template.html` + `build_html.py` — don't build two separate pipelines.

## 7. Be honest with data; never fabricate
If an address / phone / hours can't be found, write "please verify". **Fabricating sends people to the wrong place** — the one thing this skill must never do.
