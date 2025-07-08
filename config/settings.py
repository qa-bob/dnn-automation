"""
Configuration settings for the test automation framework
"""
import os

class Config:
    # Base URLs for different environments
    BASE_URLS = {
        'dev': 'http://the-internet.herokuapp.com',
        'staging': 'http://the-internet.herokuapp.com', 
        'prod': 'http://the-internet.herokuapp.com'
    }
    
    # Default environment
    ENVIRONMENT = os.getenv('TEST_ENV', 'dev')
    BASE_URL = BASE_URLS[ENVIRONMENT]
    
    # Browser settings
    DEFAULT_BROWSER = os.getenv('BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'
    
    # Timeout settings
    DEFAULT_TIMEOUT = 10
    PAGE_LOAD_TIMEOUT = 30
    SCRIPT_TIMEOUT = 30
    
    # Screenshot settings
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_DIR = 'reports/screenshots'
    
    # Report settings
    REPORT_DIR = 'reports'
    HTML_REPORT_FILE = 'reports/test_report.html'
    
    # Test data
    TEST_DATA_DIR = 'test_data'
    
    # Authentication credentials
    BASIC_AUTH_USERNAME = 'admin'
    BASIC_AUTH_PASSWORD = 'admin'
    
    FORM_AUTH_USERNAME = 'tomsmith'
    FORM_AUTH_PASSWORD = 'SuperSecretPassword!'
