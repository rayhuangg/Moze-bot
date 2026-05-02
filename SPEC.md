# MOZE Discord Bot 專案規格書

## 1. 專案目標
開發一個 Discord 記帳機器人。透過 Slash Command 輸入花費，並回傳帶有 MOZE URL Scheme 的按鈕，讓雙方一鍵寫入 iOS MOZE App，並且Bot 會將紀錄寫入 Google Sheets 備份。最終目標使用免費資源成功部署上線使用

## 2. 技術棧
- 語言：Python 3.10+
- 套件與專案管理：`uv` (用於安裝、管理與執行 Python 專案)
- 框架：`discord.py` (需使用 app_commands 實作斜線指令)
- 環境變數：`python-dotenv` 讀取 `.env` 檔中的 `DISCORD_TOKEN`

## 3. 核心功能：`/expense` 指令
- `subcategory` (必填，字串選項)：只能選擇以下類別：早餐、午餐、晚餐、點心、飲料、消夜、採購、食材、水果。
- `amount` (必填，整數 Integer)：總金額。
- `store` (選填，字串 String)：店家名稱。若使用者未填寫，則預設為 None。
- 以下為選填項目，提供預設選項，以及允許使用者自訂輸入：
  - date, Format: YYYY.MM.dd，預設為目前時間
  - time, Format: HH:mm，預設為目前時間
  - currency ： TWD
  - note: 你覺得是其他內容的東西

## 4. URL 產生邏輯

根據 [https://urlscheme.moze.app/](https://urlscheme.moze.app/) moze URL Scheme 的規範
統一使用以下格式，並且最終網址都需要經過URL編碼
Open Record Page
moze://new

同時提供兩種URL開頭格式，分別為 moze3:// 和 moze://，以對應不同版本的 MOZE App 使用者。

### POC 需求
網址1：moze3://new?amount=20&account=錢包& category=交通&subcategory=捷運&project=生活開銷
網址2：moze://new?amount=20&account=錢包& category=交通&subcategory=捷運&project=生活開銷



## 5. UI 回覆 (Discord Message)
當接收到指令並成功寫入 Google Sheet 後，機器人須回覆一個 Embed 訊息，包含：
- 標題：[{item}] 記帳確認
- 描述：總額 {amount} , 店家 {store} (如果有提供)，日期時間 {date} {time}，備註 {note} (如果有提供)
- 下方附加兩個 URL Button (使用 `discord.ui.View` 和 `discord.ui.Button`)：
  - 按鈕1：👩 moze3記帳
  - 按鈕2：👦 moze記帳