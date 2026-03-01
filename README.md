# Moze-Split-Record-Tool

MOZE Discord 記帳機器人。透過 Slash Command 輸入共同花費，計算 AA 制金額，並回傳帶有 MOZE URL Scheme 的按鈕。

## 1. 開發環境建置

### 套件安裝
使用 `pip` 安裝：
```bash
pip install -r requirements.txt
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
python main.py
```

## 3. 測試
使用 `pytest` 執行單元測試：
```bash
pytest
```
