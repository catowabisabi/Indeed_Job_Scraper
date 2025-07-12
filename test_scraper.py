#!/usr/bin/env python3
"""
簡單的爬蟲測試腳本
"""

import requests
import json
import time

def test_scraper():
    # API 端點
    url = "http://localhost:5000/scrape"
    
    # 測試數據
    data = {
        "url": "https://example.com",
        "use_session": True,
        "headless": True
    }
    
    try:
        print("發送爬蟲請求...")
        print(f"目標 URL: {data['url']}")
        print(f"使用會話: {data['use_session']}")
        print(f"無頭模式: {data['headless']}")
        
        response = requests.post(url, json=data, timeout=120)  # 增加超時時間
        
        print(f"狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("爬取成功！")
            print(f"網頁標題: {result.get('title', 'N/A')}")
            print(f"狀態: {result.get('status', 'N/A')}")
            
            # 保存結果
            with open('test_result.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print("結果已保存到 test_result.json")
            
        elif response.status_code == 429:
            print("服務器繁忙，請稍後重試")
            
        else:
            print(f"錯誤: {response.text}")
            
    except requests.exceptions.Timeout:
        print("請求超時，請檢查服務是否正常運行")
    except requests.exceptions.ConnectionError:
        print("連接錯誤，請確保爬蟲服務正在運行")
    except requests.exceptions.RequestException as e:
        print(f"請求錯誤: {e}")
    except Exception as e:
        print(f"其他錯誤: {e}")

def test_health_check():
    """測試服務健康狀態"""
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ 爬蟲服務運行正常")
            return True
        else:
            print(f"❌ 服務異常，狀態碼: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 無法連接到服務: {e}")
        return False

if __name__ == "__main__":
    print("=== 爬蟲測試 ===")
    
    # 先檢查服務狀態
    if not test_health_check():
        print("\n請先啟動爬蟲服務：")
        print("python src/main.py --headless")
        exit(1)
    
    print("\n開始測試爬蟲...")
    test_scraper() 