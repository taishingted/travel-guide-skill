---
name: travel-guide
description: 把一份粗略的旅遊行程（日期、景點、順序）變成排版精美、可對外分享的旅遊說明書網頁（自包含 HTML，可印 PDF）。涵蓋每站的地址／電話／營業時間／官網／照片／景點介紹／Google Map／停車場連結、到達–停留–離開時間軸、站與站之間的交通時間與走哪條路、縣市路線地圖、行前天氣連結與攜帶清單。當使用者說「幫我做旅遊行程表」「做旅遊說明書」「行程規劃」「把這個行程排成漂亮的」「給同行旅客參考的手冊」「生成旅遊手冊／旅遊 DM」「trip itinerary」「travel guide／brochure」，或丟一份行程草稿要你美化成給旅伴看的成品時，一定要用這支。
---

# travel-guide · 旅遊說明書生成

把使用者的粗略行程，做成一份**排版精美、資訊完整、可分享**的旅遊說明書：
一份**自包含 HTML**（單檔、圖片內嵌，傳出去一點就開）＋ 一份 **A4 PDF**（校稿用）。

> 使用者多半**無程式背景**，全程**繁體中文、白話**，**半自動**（先給計畫再動手）。所有回報講「按什麼、放哪裡」，不要丟路徑丟術語。

## 五步流程（照順序做；用「狀態」決定何時算完成）

### 1. 蒐集行程資料 → 寫成 `trip.json`
照 `references/data-checklist.md` 逐欄蒐集。分兩類：
- **使用者一定要給的**：日期/天數、集合與回程、每站的名稱/鄉鎮/類別/順序、到達-停留-離開、站間交通時間與走哪條路、**照片檔**、縣市路線地圖底圖。
- **你自己補的**：地址/電話/營業時間/景點介紹（上網查證，**查不到就誠實寫「請自行確認」，絕不瞎編**）、Google Map 連結（用店名自動組）、天氣連結（用縣市組）、攜帶清單（依季節與行程性質建議）。
把結果寫成 `trip.json`（schema 與完整範例見 `references/example-trip.json`）。

### 2. 收照片 → 跑 `scripts/process_images.py`
**聊天室貼的圖讀不到檔案**——第一時間就請使用者把照片存進 `旅遊圖片/` 資料夾，用 **`站號-序號`** 命名（例：第 2 站第 1 張 = `2-1.jpg`）；路線地圖用 `map_day1.png`、站內路線提醒圖用 `route_<站號>.png`。
```
python scripts/process_images.py 旅遊圖片 assets
```
（並排照片自動裁成統一 3:2；地圖類保留原比例。）

### 3. 產出 HTML → 跑 `scripts/build_html.py`
```
python scripts/build_html.py trip.json assets 行程.html          # 自包含(base64)＝要分享的成品
python scripts/build_html.py trip.json assets 行程_files.html --files   # 外部圖檔版＝拿去印 PDF 用
```

### 4. 印 PDF＋驗證 → `make_pdf.py` 然後 `verify_pdf.py`
```
python scripts/make_pdf.py 行程_files.html 行程.pdf
python scripts/verify_pdf.py 行程.pdf
```
`verify_pdf.py` 會逐頁揪出「照片被畫小／露白」的頁。**若被點名 → 見 `references/gotchas.md` 第 2 條：請使用者把那張圖重存一次**（實測重存就好），再回第 2 步。

### 5. 交付
- 把**自包含 HTML**當成品交給使用者，並教「怎麼分享」（見 `gotchas.md` 第 5 條：手機快取／每次給新連結／GitHub Pages）。
- 交付前**逐條過 `references/gotchas.md`**，確認沒踩雷。

## 設計要照範本，不要自由發揮
版面、配色、卡片、按鈕、時間軸的規格全在 `references/design-system.md`（CSS 在 `assets/template.html`）。這是**品味型**要求：照範本走，別自己改配色或版型。

## 收尾一定要裸跑測試（規律六）
拿一趟真實行程（例：台南嘉義兩天一夜）從頭跑一次，看它卡在哪再回頭修檔案。
