## Indeed Job Scraper / 進階 Indeed 職缺爬蟲

簡介
這個專案是一個以 Selenium + Flask 為基礎的職缺爬蟲服務（範例：針對 Indeed/一般職缺頁面），具備基本的反檢測、可選無頭（headless）模式、日誌與設定管理，並示範如何整合文字處理（例如 OpenAI）。

主要功能
- 啟動一個簡單的 API 服務來接受爬取請求（`src/main.py`）。
- 支持 headless 與非 headless 模式（透過命令列參數或環境變數控制）。
- 基礎反檢測與選用的 Chrome 啟動參數（在 `config/settings.py` 中管理）。
- 日誌化：產生 `logs/scraper.log` 與 `logs/scraper_error.log`。
- 範例 demo 資料與測試（資料放在 `demo_data/` 與 `tests/`）。

需求
- Python 3.9+
- 參考 `requirements.txt`（包含 flask, selenium, webdriver_manager, requests, openai, python-dotenv, psutil）。

安裝
1. 建議建立並啟用虛擬環境：
   - Windows (PowerShell):

     ```powershell
     python -m venv .venv; .\.venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     ```

2. （選擇）建立 `.env` 放入密鑰，例如：
   OPENAI_API_KEY=your_openai_key
   CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe

使用說明
1. 啟動 API 服務（從專案根目錄）：

   ```powershell
   python .\src\main.py --port 5000 --host 0.0.0.0 --headless
   ```

   參數：
   - `--headless`：加入此參數會以無頭模式啟動瀏覽器（預設為非無頭，或由 `SCRAPER_HEADLESS` 環境變數覆蓋）。
   - `--debug`：啟用 Flask 的 debug 模式。
   - `--port`、`--host`：設定服務監聽位址與埠號。

2. 範例測試
   - 專案內含 `tests/test_scraper.py` 與 `test_scraper.py`，可用來手動或自動測試函式/流程。

設定（重要檔案與環境變數）
- `config/settings.py`：主要設定放置處，包含 Chrome 路徑偵測、啟動參數、日誌設定與驗證函式。
- 環境變數：
  - `OPENAI_API_KEY`：若要啟用 OpenAI 文字處理功能，需設定。
  - `CHROME_PATH`：如預設偵測不到 Chrome，請指定完整路徑。
  - `SCRAPER_HEADLESS`：可由程式或環境變數設定無頭模式（`true/false`）。

檔案與目錄說明
- `src/main.py`：專案入口，會建立 `logs/` 與 `chrome-data/`，並啟動 `WebScraperAPI` 服務。
- `src/scraper/`：爬蟲實作（API 路由與爬蟲邏輯）。
- `config/settings.py`：配置與日誌設定。
- `demo_data/`：範例資料（如 fake_job.py）。
- `logs/`：運行時產生的日誌檔案（`scraper.log`, `scraper_error.log`）。
- `chrome-data/`：Chrome 使用的資料目錄（profile）以便保留 cookies/session。

開發提示與常見問題
- Chrome/Chromium 必須安裝，若找不到，請在 `.env` 或系統環境變數設定 `CHROME_PATH` 指向 chrome.exe。Windows 常見路徑為 `C:\Program Files\Google\Chrome\Application\chrome.exe`。
- 若遇到 selenium driver 問題，請安裝或更新 `webdriver_manager`，或手動安裝對應版本的 chromedriver。
- 日誌位置：`logs/scraper.log`（INFO）、`logs/scraper_error.log`（ERROR）。

安全與倫理
- 本專案示範技術用途，請遵守目標網站的 robots.txt、服務條款與法律法規，不要用於未經授權的資料抓取或攻擊行為。

常見指令彙整（PowerShell）

```powershell
# 建立虛擬環境與安裝
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt

# 啟動 API (無頭)
python .\src\main.py --headless --port 5000

# 啟動 API (有畫面，除錯用)
python .\src\main.py --port 5000 --debug

# 查看日誌
Get-Content -Path .\logs\scraper.log -Tail 200 -Wait
```

後續建議（可選）
- 補上一份 `env.example` 說明必備與建議的環境變數。
- 在 `tests/` 中加入 CI 可跑的單元測試（mock Selenium）以便自動化檢查。
- 增加 README 範例 API 請求與回傳格式（若 API 路由確定）。

授權
MIT License

完成狀態
- 依目前程式碼撰寫 README 內容，若需要我可以把 README 調整為更細的 API 文件或加入實際的示例請求/回應。