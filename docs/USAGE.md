# Redirector 使用說明

此頁面 (`index.html`) 用於將使用者從瀏覽器重新導向至 MOZE App 的 URL Scheme。這在 Discord 等平台上非常有用，因為直接點擊 URL Scheme 連結有時會被阻擋或無法正確開啟 App。

## 使用方式

在網址後方加上 `target` 參數，參數內容為完整的 MOZE URL Scheme（需經過 URL 編碼）。

### 基本格式
網域名稱：https://rayhuangg.github.io/Moze-bot/

`https://<你的網域名稱>/index.html?target=<URL_ENCODED_SCHEME>`

## 支援的 URL Scheme
目前支援以下兩種開頭的 Scheme：
1. `moze://` (適用於舊版 MOZE)
2. `moze3://` (適用於 MOZE 3.0+)

## 參數說明
| 參數名 | 說明 | 範例內容 |
| :--- | :--- | :--- |
| `target` | 必填。完整的目標 URL Scheme。 | `moze://new?amount=100&account=錢包` |

## 範例
若要開啟 MOZE 並新增一筆 100 元的記錄：

1. **原始 Scheme**: `moze://new?amount=100&account=錢包`
2. **URL 編碼後的 Scheme**: `moze%3A%2F%2Fnew%3Famount%3D100%26account%3D%25E9%258C%25A2%25E5%258C%2585`
3. **最終重導向網址**:
   `https://rayhuangg.github.io/Moze-bot/index.html?target=moze%3A%2F%2Fnew%3Famount%3D100%26account%3D%25E9%258C%25A2%25E5%258C%2585`

## 注意事項
- 請務必對 `target` 的值進行 URL 編碼，以確保特殊字元（如 `&`, `?`, `=`, `:`）能正確傳遞。
- 部分行動裝置瀏覽器可能會跳出確認視窗問是否要開啟 App，此為系統安全機制。
