# travel-guide · 旅遊說明書生成 Skill

> A Claude Code / Claude Agent **Skill** that turns a rough trip outline into a polished, shareable travel guide — a **self-contained HTML** page (images inlined, one file) plus a print-ready **A4 PDF**.

把一份**粗略的旅遊行程**（日期、景點、順序），變成一份**排版精美、可對外分享**的旅遊說明書：
一份**自包含 HTML**（單檔、圖片內嵌，傳出去一點就開）＋ 一份 **A4 PDF**（校稿用）。

這支 Skill 是 2026-09-15 從一次真實成果（台南・嘉義兩天一夜）**反向拆解**而成，並用 [AI Skill 六條設計規律](#設計理念) 打磨。

---

## 🎬 成品效果（Demo）

`demo/` 放了用這支 Skill 做出來的真實成品：

- 📄 [`demo/台南嘉義兩天一夜-範例成品.pdf`](demo/台南嘉義兩天一夜-範例成品.pdf) — A4 校稿版
- 🌐 [`demo/台南嘉義兩天一夜-範例成品.html`](demo/台南嘉義兩天一夜-範例成品.html) — 自包含網頁版（單檔、可直接分享）

---

## ✨ 產出涵蓋

- **封面**：主副標、路線節點、集合／住宿／回程資訊
- **行前提醒**：天氣連結（依縣市自動組）＋ 攜帶清單（依季節與行程性質建議）
- **每一天**：路線地圖（含國道／縣道、經過鄉鎮）＋ 時間軸
- **每一站**：到達–停留–離開時間、地址／電話／營業時間、景點介紹、照片、
  **有顏色辨識的按鈕**（🗺 Google Map／🅿️ 停車場／🔗 官網）、開車路線提醒
- **兩種輸出、一份範本**：分享用自包含 HTML ＋ 校稿用 PDF

## 📦 結構

```
travel-guide/
├── SKILL.md                  # 五步流程地圖（越短越好，細節推 references）
├── references/
│   ├── data-checklist.md     # 要蒐集哪些欄位、什麼你給、什麼 AI 自己補
│   ├── design-system.md      # 版面／配色／元件規格（照範本走）
│   ├── gotchas.md            # 血淚防呆（見下）
│   └── example-trip.json     # 完整範例 = 資料 schema + 測試資料
├── scripts/
│   ├── process_images.py     # 照片裁成統一 3:2、洗進 assets/
│   ├── build_html.py         # 由 trip.json 組 HTML（base64 自包含 / --files 外部圖檔）
│   ├── make_pdf.py           # 用系統 Edge/Chrome 無頭列印成 A4 PDF
│   └── verify_pdf.py         # 逐頁轉圖 + 自動偵測「照片被畫小」的頁
└── assets/
    └── template.html         # 版面骨架 + CSS
```

## 🚀 使用

1. 把景點照片存進 `旅遊圖片/`，用 **`站號-序號`** 命名（例：第 2 站第 1 張 = `2-1.jpg`）；
   路線地圖 `map_day1.png`、站內路線圖 `route_<站號>.png`。
2. 讓 Claude 依 `references/data-checklist.md` 把行程蒐集成 `trip.json`（缺的地址電話上網補，**查不到就寫「請自行確認」，絕不瞎編**）。
3. 依序跑：
   ```bash
   python scripts/process_images.py 旅遊圖片 assets
   python scripts/build_html.py trip.json assets 行程.html            # 自包含，要分享的成品
   python scripts/build_html.py trip.json assets 行程_files.html --files  # 外部圖檔版，印 PDF 用
   python scripts/make_pdf.py 行程_files.html 行程.pdf
   python scripts/verify_pdf.py 行程.pdf
   ```
4. `verify_pdf.py` 若點名某頁照片被畫小 → 把那站來源圖**另存新檔重存一次**，重跑即可。

**相依**：Python 3、[Pillow](https://pypi.org/project/pillow/)、[PyMuPDF](https://pypi.org/project/PyMuPDF/)、系統的 Edge 或 Chrome（無頭列印 PDF）。

## 🧠 血淚防呆（`references/gotchas.md` 精華）

真的踩過、值得別人避開的坑：

1. **某些圖檔會觸發 Edge 無頭匯出 PDF 的 bug**：照片被畫在框內左上角、下面一片白。與欄數／格式／尺寸／CSS 全無關，**只跟該圖檔的像素資料有關**——把圖檔重存一次就好。
   `verify_pdf.py` 用「圖框下緣是不是一片空白」自動偵測（正常 0.01~0.05、壞掉 = 1.0）。
2. **驗證要看真實渲染**（PyMuPDF 逐頁轉圖），別信無頭全頁截圖（大圖會分帶失真）。
3. **並排照片先裁成統一比例**（3:2）＋ `width:100%`，別靠 `object-fit:cover`（無頭匯出會出包）。
4. **手機看到舊版是快取**：改版就發布**全新連結**，長久放 GitHub Pages。

## 設計理念

用「AI Skill 六條設計規律」打磨：描述是誘餌（觸發準）、本文只放地圖（精簡）、確定的事交給腳本、講「為什麼」勝過用大寫壓人、會被抄的捷徑先堵、寫完一定裸跑測試。

## License

[MIT](LICENSE)
