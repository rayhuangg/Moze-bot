# MOZE Discord Bot 專案規格書

## 1. 專案目標
開發一個 Discord 記帳機器人。透過 Slash Command 輸入共同花費，計算 AA 制金額，並回傳帶有 MOZE URL Scheme 的按鈕，讓雙方一鍵寫入 iOS MOZE App，並且Bot 會將紀錄寫入 Google Sheets 備份。

## 2. 技術棧
- 語言：Python 3.10+，並使用UV進行安裝package與系統
- 框架：`discord.py` (需使用 app_commands 實作斜線指令)
- 套件管理：`pip` + `requirements.txt`
- 環境變數：`python-dotenv` 讀取 `.env` 檔中的 `DISCORD_TOKEN`

## 3. 核心功能：`/expense` 指令
- `payer` (必填，字串選項 Choice)：只能選擇 "Ray" 或 "Moyichen"。
- `subcategory` (必填，字串選項)：只能選擇以下類別：早餐、午餐、晚餐、點心、飲料、消夜、採購、食材、水果。
- `amount` (必填，整數 Integer)：總金額。
- `store` (選填，字串 String)：店家名稱。若使用者未填寫，則預設為 None。

## 4. 計算與 URL 產生邏輯 (AA制)
男友 的 Discord user name為：RayHuang
女友 的 Discord user name為：moyichen
假如除以二有餘數，則由男友多負擔 1 元。

根據 [https://urlscheme.moze.app/](https://urlscheme.moze.app/) moze URL Scheme 的規範
統一使用以下格式，並且最終網址都需要經過URL編碼
Open Record Page
moze://new

男友的URL使用 moze3:// 開頭
女友為付費版，可完全使用 URL scheme中的 moze:// 開頭

### POC 需求
男友網址：moze3://new?amount=20&account=錢包& category=交通&subcategory=捷運&project=生活開銷
女友網址：moze://new?amount=20&account=錢包& category=交通&subcategory=捷運&project=生活開銷

### 實際需求（初步先忽略）
(假設總金額為 200，分攤為 100)
並且需要記帳的項目有兩筆，一是自己在這消費該花的錢，另一筆是對方應該付的錢（記為虛擬帳戶）。例如：
午餐200元，男友先付錢，則記帳項目會是
- 男友
  - 午餐: 100元
  - 轉帳給女友: 100元(等同於先花100借錢給女友吃這餐)
- 女友
  - 午餐: 100元
  - 收到男友轉帳: 100元(等同於先跟男友借100吃這餐)


所以轉為以下URL邏輯
- 若 payer 為 男友：
  - 男友
    - URL 1 (自己花費): `moze://new?&amount=200&account=BoyCash&receivable=100&receivableAccount=GirlDebt&name={item}`
    - URL 2 (轉帳給女友): `moze://new?&amount=100&account=BoyVirtual&name={item}`
  - 女友
    - URL 1 (自己花費): `moze://new?&amount=100&account=BoyCash&receivable=100&receivableAccount=GirlDebt&name={item}`
    - URL 2 (跟男友借錢): `moze://new?&amount=100&account=BoyVirtual&name={item}`
- 若 payer 為 男友：
  - 男友 URL: `moze://new?&amount=200&account=BoyCash&name={item}`
  - 女友 URL: `moze://new?&amount=100&account=BoyVirtual&name={item}`

## 5. UI 回覆 (Discord Message)
當接收到指令並成功寫入 Google Sheet 後，機器人須回覆一個 Embed 訊息，包含：
- 標題：[{item}] 記帳確認
- 描述：總額 {amount} / 由 {payer} 先墊
- 下方附加兩個 URL Button (使用 `discord.ui.View` 和 `discord.ui.Button`)：
  - 按鈕1：👩 女友記帳 (綁定 Girl URL)
  - 按鈕2：👦 男友記帳 (綁定 Boy URL)