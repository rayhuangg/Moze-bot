# 更新 Docker 映像檔方法

當 GitHub 倉庫有更新時，請依照以下步驟更新 NAS 上的映像檔。

## 1. 本地更新與重新建置

在您的 Mac 上獲取最新代碼並重新建置映像檔：

```bash
# 獲取最新代碼
git pull

# 重新建置 (版本號建議增加，例如 v1.1，或使用 latest)
docker build --platform linux/amd64 -t moze-bot:latest .
```

> **提示**：在部署前，建議先參考 `DEPLOYMENT.md` 中的「在 Mac 上進行本地測試」小節，確保新版本在本地執行無誤。

## 2. 更新方式

### 方法 A：手動重新匯入 (不使用 Docker Registry)
1.  重複 `DEPLOYMENT.md` 中的匯出步驟：
    ```bash
    docker save moze-bot:latest > moze-bot.tar
    ```
2.  上傳到 NAS。
3.  在 NAS Docker 介面中：
    *   停止並刪除舊容器。
    *   刪除舊映像檔。
    *   匯入新的 `moze-bot.tar`。
    *   重新部署。

### 方法 B：使用 Docker Hub (推薦的自動化方案)
如果您希望更方便地更新，建議將映像檔推送到 Docker Hub (私人或公開)：

1.  **在 Mac 上推送**：
    ```bash
    docker tag moze-bot:latest your-username/moze-bot:latest
    docker push your-username/moze-bot:latest
    ```
2.  **在 NAS 上更新**：
    *   進入 **映像檔**，點擊 **拉取** (Pull) 獲取最新版本。
    *   停止舊容器並點擊 **重置** (Reset) 或重新部署，它會自動使用新的映像檔。

## 3. GitHub Actions 自動化 (進階)
您可以設定 GitHub Actions，在每次 `push` 到 `main` 分支時，自動建置 `linux/amd64` 的映像檔並推送到 Docker Hub。這樣一來，您只需在 NAS 上點擊「拉取」即可完成更新。

範例流程：
1.  代碼 Push 到 GitHub。
2.  GitHub Actions 建置映像檔。
3.  NAS 收到通知 or 手動拉取新映像檔。
