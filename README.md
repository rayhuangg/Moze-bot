# Moze-Split-Record-Tool

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0%2B-blue)](https://discordpy.readthedocs.io/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

這是一個專為 MOZE 使用者設計的 Discord 記帳機器人。透過 Discord 的斜線指令 (Slash Command)，您可以快速記錄共同花費，機器人會回傳一鍵開啟 MOZE App 的記帳連結，讓 AA 制記帳變得極其簡單。

## 🌟 核心功能

- **斜線指令記帳**：直接在 Discord 輸入 `/expense` 即可開始記帳。
- **一鍵導向 MOZE**：支援 `moze://` 與 `moze3://` URL Scheme，點擊連結自動填寫金額、類別、店家與備註。
- **URL Scheme 重導向**：內建 GitHub Pages 中轉頁面，解決部分平台（如 Discord）無法直接開啟自訂 URL Scheme 的限制。
- **支援 Docker 部署**：針對 Mac (Apple Silicon) 與 NAS (x86_64) 提供優化的 Docker 建置流程。

---

## 🚀 快速開始

### 1. 環境需求
- Python 3.10 或以上版本
- [uv](https://github.com/astral-sh/uv) (推薦的 Python 套件管理器)

### 2. 安裝與設定
1. **複製專案**：
   ```bash
   git clone https://github.com/your-username/Moze-Split-Record-Tool.git
   cd Moze-Split-Record-Tool
   ```

2. **安裝依賴**：
   ```bash
   uv sync
   ```

3. **設定環境變數**：
   複製 `.env.example` 並填入您的 Discord Bot Token。
   ```bash
   cp .env.example .env
   ```
   編輯 `.env`：
   ```env
   DISCORD_TOKEN=你的_DISCORD_BOT_TOKEN
   ```

### 3. 執行機器人
```bash
uv run main.py
```

---

## 🛠️ 使用說明

### 斜線指令：`/expense`
在 Discord 頻道中輸入 `/expense` 並填寫以下參數：

| 參數 | 必填 | 說明 |
| :--- | :---: | :--- |
| `subcategory` | ✅ | 類別（例如：午餐、早餐、採購等） |
| `amount` | ✅ | 總金額（整數） |
| `store` | ✅ | 店家名稱 |
| `date` | ❌ | 日期，格式 `YYYY.MM.dd` (預設為當日) |
| `time` | ❌ | 時間，格式 `HH:mm` (預設為現在) |
| `currency` | ❌ | 幣別 (預設為 `TWD`) |
| `note` | ❌ | 備註內容 |

### URL Scheme 重導向 (docs/index.html)
由於 Discord 會阻擋 `moze://` 類型的連結，本專案提供了一個中轉網頁（預設部署在 GitHub Pages）。
- **網址**: `https://<your-username>.github.io/Moze-bot/index.html?target=<URL_ENCODED_MOZE_SCHEME>`
- 詳細設定請參考 [docs/USAGE.md](./docs/USAGE.md)。

---

## 🐳 Docker 部署與測試

本專案提供完整的 Docker 支援，詳細步驟請參閱 [DEPLOYMENT.md](./DEPLOYMENT.md)。

### 快速指令參考
- **Mac 本地測試**：
  ```bash
  docker build -t moze-bot:test .
  docker run -d --name moze-test --env-file .env moze-bot:test
  ```
- **建置 NAS (x86_64) 映像檔**：
  ```bash
  docker build --platform linux/amd64 -t moze-bot:latest .
  ```

---

## 🧪 測試

本專案使用 `pytest` 進行單元測試。

```bash
uv run pytest
```

---

## 📂 檔案結構

- `main.py`: 機器人主程式，處理 Discord 指令與互動。
- `utils.py`: 核心邏輯，負責產生 MOZE URL Schemes。
- `docs/`: 包含 GitHub Pages 中轉頁面與相關說明文件。
- `tests/`: 包含 `pytest` 測試案例。
- `DEPLOYMENT.md`: 詳細的 Docker 部署指南。
- `UPDATE_Docker.md`: Docker 映像檔更新流程。

---

## 📜 專案規格與開發規範
- [SPEC.md](./SPEC.md): 專案功能需求與技術規格。
- [RULE.md](./RULE.md): AI 助手開發與測試規範。
