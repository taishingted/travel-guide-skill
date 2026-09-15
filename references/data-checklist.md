# 蒐集資料清單（寫進 trip.json 前逐欄過）

分兩類：**使用者一定要給的**、**你自己補的**。缺哪一欄就去補，別留空。

## 🟦 使用者一定要給的

### 整趟
- `title`（主標，如「台南・嘉義 兩天一夜」）、`subtitle`（一句副標）
- `eyebrow`（封面英文小字，如「TAINAN · CHIAYI · 2 DAYS 1 NIGHT」）
- `counties`（縣市清單，用來組天氣連結與對應地圖）
- `route_summary`（封面一排路線節點，如 ["台南高鐵","新化 大目降",...]）
- `cover_meta`（封面 2–3 個資訊塊：出發集合、住宿、回程）

### 每一天
- `no`（第幾天）、`date`（如「9/18（五）」，**要含星期**）、`flow`（如「台南 → 嘉義」）、`range`（經過鄉鎮）
- `theme`：`"green"`（預設）或 `"wood"`（第二天以後換色，視覺分段）
- `map`：`{"img":"map_day1","caption":"..."}` — 路線底圖＋圖說（走法、經過哪些鄉鎮、走哪些國道/縣道、是否順路）
- `backup`（選填）：備案行程一句話

### 每一站（items 裡 type=stop）
- `name`、`zone`（鄉鎮區）、`tag`（類別：spot 景點／food 美食／nat 自然賞景／stay 住宿／trans 交通）
- `arr`（到達）、`lbl`（時間標籤：到達／午餐到達／集合／入住…）、`stay`（停留時長，選填）、`dep`（出發，選填）
- `photos`：照片編號陣列，如 `["2-1","2-2"]`（**站號-序號**；聊天室貼的圖讀不到，一定要存檔）

### 站與站之間（items 裡 type=leg）
- `time`（如「約 27 分」）、`road`（走哪條路，如「台86快速 / 台19甲 往北」）、`icon`（選填，🚗 或 🚶）

## 🟩 你自己補的（別要使用者查）

- `info`：每站的地址📍、電話☎、營業時間🕘（**上網查證**；查不到寫「請自行確認」，**絕不瞎編**——長輩會被導到錯地方）
- `desc`：景點介紹 1–3 句（在地特色、招牌、必看）
- `links`：按鈕陣列。慣例：
  - Google Map → `{"text":"🗺 Google Map","url":"https://www.google.com/maps/search/?api=1&query=<店名或地址>"}`（不給 cls＝預設藍）
  - 停車場 → `{"cls":"park","text":"🅿️ 停車場","url":"<停車場 Google Map 連結>"}`（橘）
  - 官網／介紹 → `{"cls":"ghost","text":"🔗 官方網站","url":"..."}`（綠）
- `warn`（選填）：一句橘色提醒，如「⚠️ 導航到定點就停」
- `subspots`（選填）：一站含多個小點（如賞蓮兩處），每個 `{"st":"標題","html":"內文含地址電話與 Map 連結"}`
- `route_note`（選填）：站內開車路線提醒＋一張路線圖 → `{"html":"...","img":"route_8"}`
- 整趟的 `weather`（用縣市組 `https://www.google.com/search?q=<縣市>+一週天氣預報`）
- 整趟的 `packing`：依季節＋行程性質建議（賞花→防曬防蚊、夜景、過夜→盥洗衣物、山區→薄外套…）

## Google Map 連結怎麼組
只給店名時：`https://www.google.com/maps/search/?api=1&query=` + 店名（含地區）。使用者若已有 `maps.app.goo.gl` 短連結，直接用他的。
