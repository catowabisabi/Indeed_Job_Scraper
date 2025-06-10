# Advanced Web Scraper 進階網頁爬蟲

A powerful web scraper with anti-detection, captcha solving, and text processing capabilities.
具有反檢測、驗證碼解決和文本處理功能的強大網頁爬蟲。

## Features 功能

- Headless mode support 無頭模式支援
- Anti-detection measures 反檢測措施
- Captcha solving (2captcha) 驗證碼解決（使用2captcha）
- Text processing (ChatGPT) 文本處理（使用ChatGPT）
- Natural mouse movements 自然滑鼠移動
- Random human-like actions 隨機人類行為模擬

## Installation 安裝

1. Clone the repository 克隆儲存庫
```bash
git clone [your-repo-url]
cd scraper
```

2. Install dependencies 安裝依賴
```bash
pip install -r requirements.txt
```

3. Set up environment variables 設置環境變數
```bash
cp env.example .env
# Edit .env with your API keys 編輯 .env 並填入你的 API 金鑰
```

## Usage 使用方法

1. Start the server 啟動伺服器
```bash
python fetcher.py
```

2. Run tests 運行測試
```bash
python tester.py
```

## API Endpoints API端點

### POST /scrape
Scrapes a webpage 爬取網頁

Request Body 請求內容:
```json
{
    "url": "https://example.com",
    "headless": true,
    "use_debugging": false
}
```

Response 回應:
```json
{
    "status": "success",
    "title": "Page Title",
    "html": "...",
    "processed_text": {
        "summary": "...",
        "raw_text": "..."
    }
}
```

## Environment Variables 環境變數

| Variable 變數 | Description 描述 | Required 必需 |
|--------------|-----------------|--------------|
| OPENAI_API_KEY | OpenAI API key OpenAI API金鑰 | Yes 是 |
| TWOCAPTCHA_API_KEY | 2captcha API key 2captcha API金鑰 | Yes 是 |
| PORT | Server port 伺服器端口 | No 否 |
| HOST | Server host 伺服器主機 | No 否 |
| DEBUG | Debug mode 調試模式 | No 否 |

## Error Handling 錯誤處理

- Captcha Detection 驗證碼檢測
- Rate Limiting 速率限制
- Connection Errors 連接錯誤
- API Errors API錯誤

## Logging 日誌記錄

Logs are stored in: 日誌存儲在：
- `scraper.log`: Server logs 伺服器日誌
- `tester.log`: Test logs 測試日誌

## Notes 注意事項

1. Requires Chrome browser Chrome瀏覽器要求
2. API keys needed API金鑰需求
3. Rate limits apply 適用速率限制
4. Use responsibly 負責任地使用

## License 授權
MIT License MIT授權 