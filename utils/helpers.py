"""
Helper utilities for test automation framework
"""
import os
import time
import json
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.settings import Config

class WaitHelpers:
    """Helper class for explicit waits"""
    
    def __init__(self, driver, timeout=None):
        self.driver = driver
        self.timeout = timeout or Config.DEFAULT_TIMEOUT
        self.wait = WebDriverWait(driver, self.timeout)
    
    def wait_for_element_visible(self, locator):
        """Wait for element to be visible"""
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator):
        """Wait for element to be clickable"""
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_element_present(self, locator):
        """Wait for element to be present in DOM"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_text_in_element(self, locator, text):
        """Wait for specific text to appear in element"""
        return self.wait.until(EC.text_to_be_present_in_element(locator, text))
    
    def wait_for_url_contains(self, url_part):
        """Wait for URL to contain specific text"""
        return self.wait.until(EC.url_contains(url_part))
    
    def wait_for_alert_present(self):
        """Wait for alert to be present"""
        return self.wait.until(EC.alert_is_present())
    
    def wait_for_element_to_disappear(self, locator):
        """Wait for element to disappear from DOM"""
        return self.wait.until_not(EC.presence_of_element_located(locator))

class ScreenshotHelper:
    """Helper class for taking screenshots"""
    
    @staticmethod
    def take_screenshot(driver, filename=None):
        """Take screenshot and save to file"""
        if not Config.SCREENSHOT_ON_FAILURE:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if filename:
            screenshot_name = f"{filename}_{timestamp}.png"
        else:
            screenshot_name = f"screenshot_{timestamp}.png"
        
        screenshot_path = os.path.join(Config.SCREENSHOT_DIR, screenshot_name)
        
        try:
            driver.save_screenshot(screenshot_path)
            return screenshot_path
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")
            return None
    
    @staticmethod
    def take_element_screenshot(driver, element, filename=None):
        """Take screenshot of specific element"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if filename:
            screenshot_name = f"{filename}_element_{timestamp}.png"
        else:
            screenshot_name = f"element_screenshot_{timestamp}.png"
        
        screenshot_path = os.path.join(Config.SCREENSHOT_DIR, screenshot_name)
        
        try:
            element.screenshot(screenshot_path)
            return screenshot_path
        except Exception as e:
            print(f"Failed to take element screenshot: {str(e)}")
            return None

class ActionHelper:
    """Helper class for complex actions"""
    
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)
    
    def hover_over_element(self, element):
        """Hover over an element"""
        self.actions.move_to_element(element).perform()
    
    def drag_and_drop(self, source_element, target_element):
        """Drag and drop from source to target"""
        self.actions.drag_and_drop(source_element, target_element).perform()
    
    def right_click(self, element):
        """Right click on element"""
        self.actions.context_click(element).perform()
    
    def double_click(self, element):
        """Double click on element"""
        self.actions.double_click(element).perform()
    
    def scroll_to_element(self, element):
        """Scroll to element"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

class AlertHelper:
    """Helper class for handling alerts"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait_helper = WaitHelpers(driver)
    
    def accept_alert(self):
        """Accept alert dialog"""
        alert = self.wait_helper.wait_for_alert_present()
        alert_text = alert.text
        alert.accept()
        return alert_text
    
    def dismiss_alert(self):
        """Dismiss alert dialog"""
        alert = self.wait_helper.wait_for_alert_present()
        alert_text = alert.text
        alert.dismiss()
        return alert_text
    
    def get_alert_text(self):
        """Get alert text without dismissing"""
        alert = self.wait_helper.wait_for_alert_present()
        return alert.text
    
    def send_keys_to_alert(self, text):
        """Send keys to alert prompt"""
        alert = self.wait_helper.wait_for_alert_present()
        alert.send_keys(text)
        alert.accept()

class SelectHelper:
    """Helper class for dropdown selections"""
    
    @staticmethod
    def select_by_text(element, text):
        """Select dropdown option by visible text"""
        select = Select(element)
        select.select_by_visible_text(text)
    
    @staticmethod
    def select_by_value(element, value):
        """Select dropdown option by value"""
        select = Select(element)
        select.select_by_value(value)
    
    @staticmethod
    def select_by_index(element, index):
        """Select dropdown option by index"""
        select = Select(element)
        select.select_by_index(index)
    
    @staticmethod
    def get_selected_option_text(element):
        """Get currently selected option text"""
        select = Select(element)
        return select.first_selected_option.text
    
    @staticmethod
    def get_all_options(element):
        """Get all available options"""
        select = Select(element)
        return [option.text for option in select.options]

class FileHelper:
    """Helper class for file operations"""
    
    @staticmethod
    def get_download_dir():
        """Get download directory path"""
        download_dir = os.path.abspath("downloads")
        os.makedirs(download_dir, exist_ok=True)
        return download_dir
    
    @staticmethod
    def wait_for_file_download(filename, timeout=30):
        """Wait for file to be downloaded"""
        download_dir = FileHelper.get_download_dir()
        file_path = os.path.join(download_dir, filename)
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            if os.path.exists(file_path):
                return file_path
            time.sleep(1)
        
        raise TimeoutException(f"File {filename} was not downloaded within {timeout} seconds")
    
    @staticmethod
    def cleanup_downloads():
        """Clean up downloaded files"""
        download_dir = FileHelper.get_download_dir()
        for file in os.listdir(download_dir):
            file_path = os.path.join(download_dir, file)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Failed to remove file {file_path}: {str(e)}")

class TestDataHelper:
    """Helper class for test data management"""
    
    @staticmethod
    def load_test_data(filename):
        """Load test data from JSON file"""
        file_path = os.path.join(Config.TEST_DATA_DIR, filename)
        with open(file_path, 'r') as file:
            return json.load(file)
    
    @staticmethod
    def save_test_data(data, filename):
        """Save test data to JSON file"""
        os.makedirs(Config.TEST_DATA_DIR, exist_ok=True)
        file_path = os.path.join(Config.TEST_DATA_DIR, filename)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
