"""
爬蟲 API 模組
整合所有組件並提供 Web API 介面
"""

import logging
import logging.config
import threading
import socket
import requests
import subprocess
import time
import random
from datetime import datetime
from flask import Flask, request, jsonify
from config.settings import (
    CHROME_PATH,
    CHROME_PORT,
    MAX_RETRIES,
    LOG_CONFIG
)
from .chrome_driver import create_driver
from .human_behavior import random_actions, is_captcha_present
from .text_processor import TextProcessor
import os

class WebScraperAPI:
    def __init__(self):
        """初始化爬蟲 API"""
        self.app = Flask(__name__)
        self._setup_routes()
        self.chrome_session_lock = threading.Lock()
        self.chrome_session_running = False
        self.request_semaphore = threading.Semaphore(3)
        self.start_time = None
        self.max_retries = MAX_RETRIES
        self.text_processor = TextProcessor()

    def _setup_routes(self):
        """設置 API 路由"""
        @self.app.route("/", methods=["GET"])
        def home():
            return "✅ Flask 爬蟲 API 已成功啟動！"

        @self.app.route("/scrape", methods=["POST"])
        def scrape():
            if not self.request_semaphore.acquire(blocking=False):
                return jsonify({"error": "伺服器繁忙，請稍後再試"}), 429

            try:
                data = request.json
                url = data.get("url")
                use_session = data.get("use_session", True)
                # 從環境變數獲取 headless 設置，如果請求中沒有指定的話
                headless = data.get("headless", os.getenv('SCRAPER_HEADLESS', 'true').lower() == 'true')

                if not url:
                    return jsonify({"error": "缺少必要的 'url' 參數"}), 400

                logging.info(f"收到爬蟲請求：{url} (headless: {headless})")
                self.start_time = datetime.now()

                if use_session:
                    self._launch_chrome_session()

                driver = None
                try:
                    driver = create_driver(use_session_port=use_session, headless=headless)
                    result = self._scrape_with_retry(driver, url)
                    return jsonify(result)
                    
                except Exception as e:
                    logging.error(f"爬蟲錯誤：{str(e)}")
                    return jsonify({"error": str(e)}), 500
                finally:
                    if driver and not use_session:
                        try:
                            driver.quit()
                            logging.info("已關閉 WebDriver")
                        except Exception as e:
                            logging.warning(f"關閉 WebDriver 發生錯誤：{str(e)}")
                    self.start_time = None
            finally:
                self.request_semaphore.release()

    def _is_port_in_use(self, port: int) -> bool:
        """檢查端口是否被使用"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return False
            except socket.error:
                return True

    def _is_chrome_session_alive(self) -> bool:
        """檢查 Chrome 工作階段是否存活"""
        try:
            r = requests.get(f"http://127.0.0.1:{CHROME_PORT}/json/version", timeout=2)
            return r.status_code == 200
        except:
            return False

    def _launch_chrome_session(self):
        """啟動 Chrome 工作階段"""
        with self.chrome_session_lock:
            if self.chrome_session_running and self._is_chrome_session_alive():
                logging.info(f"Chrome 埠 {CHROME_PORT} 已在運作中")
                return

            if not self._is_port_in_use(CHROME_PORT):
                logging.info("啟動 Chrome 工作階段...")
                try:
                    # 先嘗試關閉可能存在的 Chrome 進程
                    try:
                        subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], 
                                     capture_output=True, timeout=10)
                        time.sleep(2)
                    except:
                        pass
                    
                    # 啟動 Chrome
                    chrome_process = subprocess.Popen([
                        CHROME_PATH,
                        f"--remote-debugging-port={CHROME_PORT}",
                        "--user-data-dir=chrome-data",
                        "--start-maximized",
                        "--disable-gpu",
                        "--no-sandbox",
                        "--disable-dev-shm-usage"
                    ], creationflags=subprocess.CREATE_NEW_CONSOLE)

                    # 等待 Chrome 啟動，增加等待時間
                    for i in range(30):  # 增加到 30 秒
                        if self._is_chrome_session_alive():
                            self.chrome_session_running = True
                            logging.info("Chrome 工作階段啟動成功")
                            return
                        time.sleep(1)
                        if i % 5 == 0:
                            logging.info(f"等待 Chrome 啟動... ({i+1}/30)")
                    
                    # 如果超時，終止進程
                    try:
                        chrome_process.terminate()
                        chrome_process.wait(timeout=5)
                    except:
                        chrome_process.kill()
                    
                    raise Exception("Chrome 啟動超時")
                    
                except Exception as e:
                    logging.error(f"啟動 Chrome 失敗：{str(e)}")
                    self.chrome_session_running = False
                    raise
            else:
                logging.info("Chrome 埠已被使用")
                self.chrome_session_running = True

    def _monitor_chrome_session(self):
        """監控 Chrome 工作階段狀態"""
        while True:
            time.sleep(10)
            with self.chrome_session_lock:
                if self.chrome_session_running and not self._is_chrome_session_alive():
                    logging.warning("Chrome 工作階段已失效，嘗試重啟...")
                    self.chrome_session_running = False
                    try:
                        self._launch_chrome_session()
                    except Exception as e:
                        logging.error(f"Chrome 重啟失敗：{str(e)}")

    def _print_timer(self):
        """顯示執行時間"""
        if self.start_time:
            elapsed = datetime.now() - self.start_time
            logging.info(f"執行時間: {elapsed.seconds}秒")

    def _scrape_with_retry(self, driver, url):
        """帶重試機制的爬蟲"""
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                driver.get(url)
                
                # 執行3-5次隨機操作
                num_actions = random.randint(3, 5)
                for _ in range(num_actions):
                    random_actions(driver)
                    self._print_timer()
                
                # 檢查是否有驗證碼
                if is_captcha_present(driver):
                    retry_count += 1
                    logging.warning(f"檢測到驗證碼！重試次數: {retry_count}")
                    
                    if retry_count >= self.max_retries:
                        return {
                            "status": "captcha_detected",
                            "message": "驗證碼重試次數超過上限"
                        }
                    
                    time.sleep(random.uniform(5, 10))
                    continue
                
                # 獲取並處理文本
                pure_text = self.text_processor.get_pure_text(driver)
                processed_text = self.text_processor.process_with_chatgpt(pure_text)
                full_text = self.text_processor.process_with_chatgpt_md(pure_text)
                
                logging.info(f"處理結果: {processed_text}")
                logging.info(f"完整分析: {full_text}")
                
                # 檢查並提取摘要和完整文本
                summary = ""
                markdown = ""
                
                try:
                    if isinstance(processed_text, dict) and "summary" in processed_text:
                        summary = processed_text["summary"]
                    if isinstance(full_text, dict) and "markdown" in full_text:
                        markdown = full_text["markdown"]
                except Exception as e:
                    logging.error(f"提取處理結果時出錯: {str(e)}")
                
                return {
                    "status": "success",
                    "title": driver.title,
                    "html": driver.page_source,
                    "processed_text": summary,
                    "full_text": markdown
                }
                
            except Exception as e:
                retry_count += 1
                logging.error(f"爬蟲錯誤 (重試 {retry_count}): {str(e)}")
                if retry_count >= self.max_retries:
                    return {"error": str(e)}, 500
                time.sleep(random.uniform(2, 5))
        
        return {"error": "超過最大重試次數"}, 500

    def run(self, debug=False, host="0.0.0.0", port=5000):
        """運行 API 服務器"""
        # 設置日誌
        if not debug:
            logging.config.dictConfig(LOG_CONFIG)
        
        # 啟動 Chrome 監控線程
        monitor_thread = threading.Thread(target=self._monitor_chrome_session, daemon=True)
        monitor_thread.start()
        
        # 使用 threaded=True 來支持多線程
        self.app.run(
            debug=debug,
            host=host,
            port=port,
            threaded=True,
            use_reloader=False  # 禁用重載器以避免在非調試模式下的問題
        ) 