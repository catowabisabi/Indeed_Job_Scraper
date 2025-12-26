## Indeed Job Scraper / 進階 Indeed 職缺爬蟲

### Overview / 概觀
- **English**: A Selenium + Flask service that keeps long-lived Chrome sessions for Indeed job scraping. This guide explains how to containerise the app on TrueNAS SCALE with persistent Chrome profiles.
- **中文**：基於 Selenium 與 Flask 的職缺爬蟲服務，保留 Chrome 持久登入會話。本文示範如何在 TrueNAS SCALE 上透過 Docker / Docker Compose 佈署並保存 Chrome 登入狀態。

### Environment Topology / 環境拓撲
- **English**: TrueNAS SCALE hosts the Docker engine; the application runs inside a single container with Google Chrome installed; host datasets persist Chrome profile, login data, and logs.
- **中文**：TrueNAS SCALE 作為 Docker 主機；應用程式在含 Google Chrome 的單一容器中執行；主機資料集保存 Chrome 個人資料、登入資訊與日誌。

### Prerequisites / 先決條件
- Docker Compose 2.x available on TrueNAS SCALE shell (Apps → Launch Docker Compose).
- Accessible dataset path, e.g. `/mnt/pool/apps/indeed-job-scraper` for bind mounts.
- Optional `.env` with `OPENAI_API_KEY` if OpenAI features are needed.

### Folder Mapping / 目錄對應
| Host Path (Example) | Container Path | Purpose | 說明 |
|---------------------|----------------|---------|------|
| `/mnt/pool/apps/indeed/logs` | `/app/logs` | Runtime logs | 運行日誌 |
| `/mnt/pool/apps/indeed/chrome-data` | `/app/chrome-data` | Chrome user data (profile) | Chrome 使用者資料（包含 cookies/session）|
| `/mnt/pool/apps/indeed/chrome-login-data` | `/app/chrome-login-data` | Extra login artefacts if required | 額外登入資訊備份 |
| `/mnt/pool/apps/indeed/config` | `/app/config` | Settings files | 設定檔 |
| `/mnt/pool/apps/indeed/src` | `/app/src` | Application source | 程式碼 |
| `/mnt/pool/apps/indeed/demo_data` | `/app/demo_data` | Demo fixtures | 範例資料 |
| `/mnt/pool/apps/indeed/tests` | `/app/tests` | Automated tests | 測試腳本 |

> Adjust host paths to match your dataset layout before running `docker compose up`.

### Chrome Profile Persistence / Chrome 登入持久化
- **English**: Copy any existing Chrome profile (Default folder, cookies, etc.) into the host `chrome-data` directory before the first run. The container mounts `/app/chrome-data` and `/app/chrome-login-data`, so Chrome keeps cookies and sessions across restarts.
- **中文**：若已擁有 Chrome 個人資料（如 Default 目錄、cookies），請先放入主機的 `chrome-data` 目錄。容器掛載 `/app/chrome-data` 與 `/app/chrome-login-data`，重新啟動後登入狀態仍會保留。

### Deployment Steps / 部署步驟
1. **Prepare host directories / 建立主機目錄**
   ```bash
   mkdir -p /mnt/pool/apps/indeed/{logs,chrome-data,chrome-login-data,config,src}
   cp -r src config demo_data tests requirements.txt docker-compose.yml Dockerfile /mnt/pool/apps/indeed/
   ```
2. **Optional: copy Chrome profile / 選擇性：複製 Chrome 個人資料**
   Place profile contents (e.g. `Default/`, `Local State`) under `/mnt/pool/apps/indeed/chrome-data`.
3. **Build container / 建置容器**
   ```bash
   cd /mnt/pool/apps/indeed
   docker compose build
   ```
4. **Run services / 啟動服務**
   ```bash
   docker compose up -d
   ```
5. **Verify / 確認狀態**
   ```bash
   docker compose logs -f
   ```

### Environment Variables / 環境變數
- `SCRAPER_HEADLESS` (default `true`): Set to `false` if you need a visible Chrome UI (requires VNC or similar solution).
- `OPENAI_API_KEY`: Optional key for OpenAI integration; leave empty if unused.
- `CHROME_PATH` (default `/usr/bin/google-chrome`): Already set inside the container; override only if you install Chrome elsewhere.

### Useful Commands / 常用指令
```bash
# Stop / 停止
docker compose down

# Rebuild after code changes / 程式更新後重新建置
docker compose build scraper && docker compose up -d

# Check Chrome remote debugging endpoint
curl http://localhost:9222/json/version
```

### Updating / 升級流程
1. Pull latest source or edit code in the mounted `src` folder.
2. Rebuild with `docker compose build` to refresh Python dependencies.
3. Restart containers via `docker compose up -d`.

### Troubleshooting / 疑難排解
- **Chrome fails to start / Chrome 無法啟動**: Ensure `/mnt/pool/apps/indeed/chrome-data` has write permission for the container UID/GID (default 1000:1000). Adjust dataset ACLs or rebuild with different `APP_UID/APP_GID` build arguments.
- **Login not preserved / 登入未保留**: Confirm the bind mount points in `docker-compose.yml` still reference the persistent dataset and the container is not recreating fresh directories.
- **OpenAI features disabled / OpenAI 功能未啟用**: Set `OPENAI_API_KEY` in the compose environment section or `.env` file loaded by Docker Compose.

### License / 授權
MIT License