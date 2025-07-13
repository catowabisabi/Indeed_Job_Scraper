import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
from demo_data.fake_job import fake_job_url

def test_scraper():
    # API 端點
    url = "http://localhost:5000/scrape"
    
    # 請求參數
    payload = {
        "url": fake_job_url,
        "use_debugging": True,  # 使用已登入的Chrome實例
        "headless": False      # 顯示瀏覽器視窗
    }
    
    print("🌐 發送爬蟲請求...")
    print(f"目標網址: {payload['url']}")
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ 爬蟲成功!")
            try:    
                print(f"頁面標題: {data['title']}")
                
            except:
                pass

                
            print(f"HTML 長度: {len(data['html'])} 字元")

            print(f"摘要: {data['processed_text']}")
            print(f"全文: {data['full_text']}")
            
            # 保存結果
            with open("result.html", "w", encoding="utf-8") as f:
                f.write(data['html'])
            print("💾 結果已保存至 result.html")
            
        elif response.status_code == 429:
            data = response.json()
            if data.get("status") == "captcha_detected":
                print("⚠️ 檢測到驗證碼，需要人工處理")
            else:
                print("⚠️ 伺服器繁忙，請稍後再試")
        else:
            print(f"❌ 錯誤: {response.status_code}")
            #print(response.json().get("error", "未知錯誤"))
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到爬蟲服務器，請確認 Flask 服務是否運行中")
    except Exception as e:
        print(f"❌ 發生錯誤: {str(e)}")

if __name__ == "__main__":
    test_scraper() 