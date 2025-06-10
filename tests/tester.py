import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pprint import pprint
import time
import logging
from demo_data.fake_job import fake_job_url

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('tester.log')
    ]
)

def test_scraper(url, headless=True):
    """測試爬蟲 API"""
    logging.info(f"開始測試爬蟲: {url} (headless: {headless})")
    print("=" * 50)
    
    api_url = "http://localhost:5000/scrape"
    payload = {
        "url": url,
        "headless": headless,  # 確保傳遞 headless 參數
        "use_debugging": False
    }
    
    try:
        logging.info(f"發送請求... (headless: {headless})")
        response = requests.post(api_url, json=payload)
        result = response.json()
        
        logging.info(f"收到響應 (狀態碼: {response.status_code})")
        
        if result.get("status") == "success":
            logging.info(f"標題: {result['title']}")
            
            processed = result["processed_text"]
            if isinstance(processed, dict):
                if "summary" in processed:
                    print("\nChatGPT 總結:")
                    print("-" * 30)
                    print(processed["summary"])
                    print("-" * 30)
                if "error" in processed:
                    logging.error(f"ChatGPT 處理錯誤: {processed['error']}")
                print("\n原始文本:")
                print("=" * 30)
                print(processed.get("raw_text", "無文本"))
                print("=" * 30)
            else:
                print("\n處理後的文本:")
                print(processed)
                
        elif result.get("status") == "captcha_detected":
            logging.warning("檢測到驗證碼！")
            logging.warning(f"訊息: {result.get('message')}")
            
        else:
            logging.error("發生錯誤:")
            logging.error(json.dumps(result, indent=2, ensure_ascii=False))
            
    except Exception as e:
        logging.error(f"請求失敗: {str(e)}")

if __name__ == "__main__":
    # 測試不同的網站
    test_urls = [
        #"https://www.example.com",
       # "https://news.ycombinator.com",
        fake_job_url
        # 添加更多測試網址
    ]
    
    # 設置是否使用 headless 模式
    headless_mode = False
    
    for i, url in enumerate(test_urls, 1):
        logging.info(f"測試進度: {i}/{len(test_urls)}")
        test_scraper(url, headless=headless_mode)
        if i < len(test_urls):
            logging.info("等待 5 秒後測試下一個網址...")
            time.sleep(5) 