# 使用 Docker 映像檔部署到綠聯 DXP4800 Plus

本專案支援自動化 CI/CD 流程與手動部署兩種方式。

## 1. 自動化部署 (推薦方式)
利用 GitHub Actions，您只需將程式碼 `git push` 到 GitHub，映像檔就會自動建置並上傳至 Docker Hub。

### 1.1 設定 GitHub Secrets
在您的 GitHub 倉庫設定中 (Settings > Secrets and variables > Actions)，新增以下兩個 Secrets：
- `DOCKERHUB_USERNAME`: 您的 Docker Hub 帳號。
- `DOCKERHUB_TOKEN`: 您的 Docker Hub Access Token。

### 1.2 自動化流程
1.  **開發與推送**：在 Mac 上修改程式碼後執行 `git push`。
2.  **自動建置**：GitHub Actions 會自動建置支援 `linux/amd64` (NAS) 與 `linux/arm64` (Mac) 的映像檔並推送到 Docker Hub。
3.  **NAS 更新**：
    - **手動**：在 NAS Docker 介面點擊「拉取最新版本」，然後重置容器。
    - **自動 (推薦)**：在 NAS 上執行 [Watchtower](https://containrrr.dev/watchtower/)，它會自動偵測 Docker Hub 更新並重啟容器。

---

## 2. 準備工作 (手動部署)
在 Mac 上，建議使用 Docker Desktop。由於 DXP4800 Plus 使用 Intel (x86_64) 架構，如果您使用的是 Apple Silicon (M1/M2/M3) 的 Mac，**必須**在建置時指定平台。

## 3. 手動建置 Docker 映像檔
在專案根目錄執行以下指令：
```bash
# 建置支援 x86_64 的映像檔 (用於 NAS)
docker build --platform linux/amd64 -t moze-bot:latest .
```

## 4. 在 Mac 上進行本地測試 (選用)
在將映像檔部署到 NAS 之前，建議先在 Mac 上測試是否能正常運作。

### 4.1 建置本地測試映像檔
如果您的 Mac 是 Apple Silicon (M1/M2/M3)，直接建置（不指定平台）會更快且適合本地執行：
```bash
docker build -t moze-bot:test .
```

### 4.2 執行容器
使用 `--env-file` 載入環境變數（確保目錄下有 `.env` 檔案）：
```bash
docker run -d --name moze-test --env-file .env moze-bot:test
```

### 4.3 查看日誌與停止
```bash
# 查看執行日誌
docker logs -f moze-test

# 停止並移除測試容器
docker stop moze-test && docker rm moze-test
```

## 5. 匯出與傳輸 (手動方式)
如果您不使用 Docker Hub，可以將映像檔匯出成檔案再上傳到 NAS：

```bash
# 匯出映像檔
docker save moze-bot:latest > moze-bot.tar
```
然後將 `moze-bot.tar` 上傳到 NAS 的共享資料夾。

## 6. 在綠聯 NAS (UGOS) 上部署

### 方法 A：使用 Docker 介面 (GUI)
1.  開啟 **Docker** 應用程式。
2.  進入 **映像檔** -> **新增** -> **從本地匯入**，選擇 `moze-bot.tar`。
3.  匯入完成後，選擇該映像檔並點擊 **部署**。
4.  **網路設定**：建議選擇 `host` (避免無法對外連線問題)。
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

## 7. 注意事項
- **架構相容性**：務必確認使用 `linux/amd64` 平台建置，否則 NAS 可能無法啟動容器。
- **權限**：若有掛載本地目錄，請確保 NAS 上的目錄權限正確。
