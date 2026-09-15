# Changelog

All notable changes to this project. Format based on [Keep a Changelog](https://keepachangelog.com/).

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
