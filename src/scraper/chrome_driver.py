"""
Chrome 驅動模組
處理所有與 Chrome 瀏覽器相關的功能
"""

import logging
import random
import json
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import (
    CHROME_PATH,
    USER_AGENTS,
    CHROME_PORT,
    PAGE_LOAD_TIMEOUT
)

class ChromeWithPrefs(webdriver.Chrome):
    """自定義 Chrome 類別，確保 preferences 正確設置"""
    
    def __init__(self, *args, **kwargs):
        options = kwargs.get('options', None)
        if options:
            if "prefs" in options._experimental_options:
                self._handle_prefs(options)
        super().__init__(*args, **kwargs)
    
    def _handle_prefs(self, options):
        """處理 Chrome preferences"""
        prefs = options._experimental_options["prefs"]
        
        # 建立臨時用戶資料目錄
        user_data_dir = os.path.normpath(tempfile.mkdtemp())
        options.add_argument(f"--user-data-dir={user_data_dir}")
        
        # 確保 Default 目錄存在
        default_dir = os.path.join(user_data_dir, "Default")
        os.makedirs(default_dir, exist_ok=True)
        
        # 將點號分隔的鍵轉換為巢狀字典
        def convert_dot_keys(prefs):
            result = {}
            for key, value in prefs.items():
                parts = key.split('.')
                target = result
                for part in parts[:-1]:
                    target = target.setdefault(part, {})
                target[parts[-1]] = value
            return result
        
        # 寫入 Preferences 檔案
        prefs_file = os.path.join(default_dir, "Preferences")
        converted_prefs = convert_dot_keys(prefs)
        with open(prefs_file, 'w') as f:
            json.dump(converted_prefs, f)
        
        # 避免 Selenium 重複處理
        del options._experimental_options["prefs"]

def create_chrome_options(headless=False):
    """創建 Chrome 選項"""
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")

    # 進階反檢測參數
    chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    chrome_options.add_argument("--enable-automation=false")
    
    # 使用arguments來禁用自動化提示
    chrome_options.add_argument("--disable-automation")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # 進階偏好設定
    prefs = {
        "profile.default_content_settings.popups": 0,
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.images": 1,
        "profile.default_content_setting_values.javascript": 1,
        "profile.managed_default_content_settings.javascript": 1,
        "profile.default_content_setting_values.plugins": 1,
        "profile.default_content_setting_values.geolocation": 2,
        "profile.default_content_setting_values.media_stream": 2,
        "profile.managed_default_content_settings.images": 1,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.managed_default_content_settings.cookies": 1,
        "profile.default_content_setting_values.cookies": 1,
        "profile.managed_default_content_settings.plugins": 1,
        "profile.default_content_settings.state.flash": 0,
        "profile.content_settings.exception_patterns": {},
        "download.directory_upgrade": True,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    return chrome_options

def create_driver(use_session_port=False, headless=False):
    """創建並配置 Chrome WebDriver"""
    chrome_options = create_chrome_options(headless)
    
    if use_session_port:
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{CHROME_PORT}")
    
    service = Service(ChromeDriverManager().install())
    driver = ChromeWithPrefs(service=service, options=chrome_options)
    
    # 注入反檢測腳本
    inject_evasion_scripts(driver)
    
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver

def inject_evasion_scripts(driver):
    """注入反檢測腳本"""
    # 基本的 webdriver 檢測規避
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            // 基本 webdriver 檢測
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // 模擬真實瀏覽器特徵
            Object.defineProperty(navigator, 'plugins', {
                get: () => {
                    return [
                        {
                            0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"},
                            description: "Portable Document Format",
                            filename: "internal-pdf-viewer",
                            length: 1,
                            name: "Chrome PDF Plugin"
                        },
                        {
                            0: {type: "application/pdf", suffixes: "pdf", description: ""},
                            description: "",
                            filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                            length: 1,
                            name: "Chrome PDF Viewer"
                        }
                    ];
                }
            });
            
            // 模擬語言設定
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en', 'zh-TW']
            });
            
            // 模擬 Chrome 運行時
            window.chrome = {
                app: {
                    isInstalled: false,
                    InstallState: {
                        DISABLED: 'DISABLED',
                        INSTALLED: 'INSTALLED',
                        NOT_INSTALLED: 'NOT_INSTALLED'
                    },
                    RunningState: {
                        CANNOT_RUN: 'CANNOT_RUN',
                        READY_TO_RUN: 'READY_TO_RUN',
                        RUNNING: 'RUNNING'
                    }
                },
                runtime: {
                    OnInstalledReason: {
                        CHROME_UPDATE: 'chrome_update',
                        INSTALL: 'install',
                        SHARED_MODULE_UPDATE: 'shared_module_update',
                        UPDATE: 'update'
                    },
                    OnRestartRequiredReason: {
                        APP_UPDATE: 'app_update',
                        OS_UPDATE: 'os_update',
                        PERIODIC: 'periodic'
                    },
                    PlatformArch: {
                        ARM: 'arm',
                        ARM64: 'arm64',
                        MIPS: 'mips',
                        MIPS64: 'mips64',
                        X86_32: 'x86-32',
                        X86_64: 'x86-64'
                    },
                    PlatformNaclArch: {
                        ARM: 'arm',
                        MIPS: 'mips',
                        MIPS64: 'mips64',
                        X86_32: 'x86-32',
                        X86_64: 'x86-64'
                    },
                    PlatformOs: {
                        ANDROID: 'android',
                        CROS: 'cros',
                        LINUX: 'linux',
                        MAC: 'mac',
                        OPENBSD: 'openbsd',
                        WIN: 'win'
                    },
                    RequestUpdateCheckStatus: {
                        NO_UPDATE: 'no_update',
                        THROTTLED: 'throttled',
                        UPDATE_AVAILABLE: 'update_available'
                    }
                }
            };
            
            // 模擬硬體特徵
            Object.defineProperty(navigator, 'hardwareConcurrency', {
                get: () => 8
            });
            Object.defineProperty(navigator, 'deviceMemory', {
                get: () => 8
            });
            Object.defineProperty(screen, 'colorDepth', {
                get: () => 24
            });
            
            // 模擬 WebGL
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return 'Intel Inc.'
                }
                if (parameter === 37446) {
                    return 'Intel(R) Iris(TM) Graphics 6100'
                }
                return getParameter.apply(this, [parameter]);
            };
            
            // 模擬其他瀏覽器特徵
            Object.defineProperty(navigator, 'platform', {
                get: () => 'Win32'
            });
            Object.defineProperty(navigator, 'maxTouchPoints', {
                get: () => 0
            });
            Object.defineProperty(navigator, 'vendor', {
                get: () => 'Google Inc.'
            });
        """
    })
    
    # 使用 CDP 命令來禁用自動化標記
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        "source": """
            Object.defineProperty(window, 'navigator', {
                value: new Proxy(navigator, {
                    has: (target, key) => (key === 'webdriver' ? false : key in target),
                    get: (target, key) =>
                        key === 'webdriver' ?
                        false :
                        typeof target[key] === 'function' ?
                        target[key].bind(target) :
                        target[key]
                })
            });
        """
    }) 