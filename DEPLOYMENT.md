# 使用 Docker 映像檔部署到綠聯 DXP4800 Plus

本專案使用 `uv` 進行 Python 環境管理，並支援 Docker 化部署。

## 1. 準備工作
在 Mac 上，建議使用 Docker Desktop。由於 DXP4800 Plus 使用 Intel (x86_64) 架構，如果您使用的是 Apple Silicon (M1/M2/M3) 的 Mac，**必須**在建置時指定平台。

## 2. 建置 Docker 映像檔

在專案根目錄執行以下指令：

```bash
# 建置支援 x86_64 的映像檔 (用於 NAS)
docker build --platform linux/amd64 -t moze-bot:latest .
```

## 3. 在 Mac 上進行本地測試 (選用)
在將映像檔部署到 NAS 之前，建議先在 Mac 上測試是否能正常運作。

### 3.1 建置本地測試映像檔
如果您的 Mac 是 Apple Silicon (M1/M2/M3)，直接建置（不指定平台）會更快且適合本地執行：
```bash
docker build -t moze-bot:test .
```

### 3.2 執行容器
使用 `--env-file` 載入環境變數（確保目錄下有 `.env` 檔案）：
```bash
docker run -d --name moze-test --env-file .env moze-bot:test
```

### 3.3 查看日誌與停止
```bash
# 查看執行日誌
docker logs -f moze-test

# 停止並移除測試容器
docker stop moze-test && docker rm moze-test
```

## 4. 匯出與傳輸 (手動方式)
如果您不使用 Docker Hub，可以將映像檔匯出成檔案再上傳到 NAS：

```bash
# 匯出映像檔
docker save moze-bot:latest > moze-bot.tar
```
然後將 `moze-bot.tar` 上傳到 NAS 的共享資料夾。

## 5. 在綠聯 NAS (UGOS) 上部署

### 方法 A：使用 Docker 介面 (GUI)
1.  開啟 **Docker** 應用程式。
2.  進入 **映像檔** -> **新增** -> **從本地匯入**，選擇 `moze-bot.tar`。
3.  匯入完成後，選擇該映像檔並點擊 **部署**。
4.  **網路設定**：建議選擇 `bridge`。
5.  **環境變數**：
    *   新增 `DISCORD_TOKEN`，填入您的 Bot Token。
6.  **自動重啟**：勾選「當容器異常退出時自動重啟」。

### 方法 B：使用 Docker Compose (推薦)
1.  將 `docker-compose.yml` 上傳到 NAS。
2.  在 NAS 上建立一個 `.env` 檔案並填入 `DISCORD_TOKEN`。
3.  使用 SSH 登入 NAS 或使用專案管理介面執行：
    ```bash
    docker-compose up -d
    ```

## 6. 注意事項
- **架構相容性**：務必確認使用 `linux/amd64` 平台建置，否則 NAS 可能無法啟動容器。
- **權限**：若有掛載本地目錄，請確保 NAS 上的目錄權限正確。
