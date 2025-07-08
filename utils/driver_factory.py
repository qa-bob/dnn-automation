from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from config.settings import Config
import os

class DriverFactory:
    @staticmethod
    def get_driver(browser_name=None, headless=None):
        browser = browser_name or Config.DEFAULT_BROWSER
        is_headless = headless if headless is not None else Config.HEADLESS
        
        # Create screenshots directory if it doesn't exist
        os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
        
        if browser.lower() == "chrome":
            return DriverFactory._get_chrome_driver(is_headless)
        elif browser.lower() == "firefox":
            return DriverFactory._get_firefox_driver(is_headless)
        else:
            raise Exception(f"Unsupported browser: {browser}. Supported browsers: chrome, firefox")
    
    @staticmethod
    def _get_chrome_driver(headless):
        options = webdriver.ChromeOptions()
        
        # Basic Chrome options
        options.add_argument("--start-maximized")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--remote-debugging-port=9222")
        
        # User agent for better compatibility
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Headless mode
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        
        # Performance options
        options.add_argument("--disable-logging")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        
        # Set download directory
        prefs = {
            "download.default_directory": os.path.abspath("downloads"),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        
        # Enable logging for debugging
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Create driver
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Set timeouts
        driver.implicitly_wait(Config.DEFAULT_TIMEOUT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        driver.set_script_timeout(Config.SCRIPT_TIMEOUT)
        
        return driver
    
    @staticmethod
    def _get_firefox_driver(headless):
        options = webdriver.FirefoxOptions()
        
        # Basic Firefox options
        if headless:
            options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
        
        # Performance options
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        
        # Set download directory
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", os.path.abspath("downloads"))
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
        
        # Create driver
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        # Set timeouts
        driver.implicitly_wait(Config.DEFAULT_TIMEOUT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        driver.set_script_timeout(Config.SCRIPT_TIMEOUT)
        
        # Maximize window if not headless
        if not headless:
            driver.maximize_window()
        
        return driver
