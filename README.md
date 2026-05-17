# Moze-Split-Record-Tool

MOZE Discord 記帳機器人。透過 Slash Command 輸入共同花費，計算 AA 制金額，並回傳帶有 MOZE URL Scheme 的按鈕。

## 1. 開發環境建置

### 安裝 uv
本專案使用 `uv` 管理。若尚未安裝，請參考 [uv 官網](https://github.com/astral-sh/uv)。

### 套件安裝
使用 `uv` 同步套件：
```bash
uv sync
```

### 環境變數設定
請複製 `.env.example` 並重新命名為 `.env`，填入你的 Discord Bot Token：
```bash
cp .env.example .env
```
編輯 `.env`：
```
DISCORD_TOKEN=YOUR_TOKEN_HERE
```

## 2. 執行機器人
```bash
uv run main.py
```

## 3. URL Scheme Redirector (GitHub Pages)
本專案提供了一個簡單的 HTML 頁面作為 URL Scheme 的中轉站，用於解決部分平台（如 Discord）無法直接點擊開啟 `moze://` 或 `moze3://` 連結的問題。

- **檔案路徑**: `docs/index.html`
- **使用說明**: 詳細參數設定請參考 [docs/USAGE.md](./docs/USAGE.md)

## 4. 測試
使用 `pytest` 執行單元測試：
```bash
uv run pytest
```
