from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.helpers import WaitHelpers, ScreenshotHelper, ActionHelper, AlertHelper, SelectHelper
from config.settings import Config
import time

class BasePage:
    """Base page class containing common functionality for all pages"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait_helper = WaitHelpers(driver)
        self.action_helper = ActionHelper(driver)
        self.alert_helper = AlertHelper(driver)
        self.screenshot_helper = ScreenshotHelper()
    
    # Navigation methods
    def go_to_url(self, url):
        """Navigate to specified URL"""
        self.driver.get(url)
        self.wait_for_page_to_load()
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get current page title"""
        return self.driver.title
    
    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        self.wait_for_page_to_load()
    
    def go_back(self):
        """Navigate back in browser history"""
        self.driver.back()
    
    def go_forward(self):
        """Navigate forward in browser history"""
        self.driver.forward()
    
    # Element finding methods
    def find_element(self, locator, timeout=None):
        """Find element with explicit wait"""
        wait_helper = WaitHelpers(self.driver, timeout) if timeout else self.wait_helper
        return wait_helper.wait_for_element_present(locator)
    
    def find_elements(self, locator):
        """Find multiple elements"""
        return self.driver.find_elements(*locator)
    
    def find_element_visible(self, locator, timeout=None):
        """Find element and wait for it to be visible"""
        wait_helper = WaitHelpers(self.driver, timeout) if timeout else self.wait_helper
        return wait_helper.wait_for_element_visible(locator)
    
    def find_element_clickable(self, locator, timeout=None):
        """Find element and wait for it to be clickable"""
        wait_helper = WaitHelpers(self.driver, timeout) if timeout else self.wait_helper
        return wait_helper.wait_for_element_clickable(locator)
    
    def is_element_present(self, locator):
        """Check if element is present without waiting"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator):
        """Check if element is visible"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait for element to disappear"""
        wait_helper = WaitHelpers(self.driver, timeout) if timeout else self.wait_helper
        wait_helper.wait_for_element_to_disappear(locator)
    
    # Interaction methods
    def click(self, locator):
        """Click on element"""
        element = self.find_element_clickable(locator)
        element.click()
    
    def double_click(self, locator):
        """Double click on element"""
        element = self.find_element_clickable(locator)
        self.action_helper.double_click(element)
    
    def right_click(self, locator):
        """Right click on element"""
        element = self.find_element_clickable(locator)
        self.action_helper.right_click(element)
    
    def hover_over_element(self, locator):
        """Hover over element"""
        element = self.find_element_visible(locator)
        self.action_helper.hover_over_element(element)
    
    def enter_text(self, locator, text):
        """Enter text into input field"""
        element = self.find_element_visible(locator)
        element.clear()
        element.send_keys(text)
    
    def clear_text(self, locator):
        """Clear text from input field"""
        element = self.find_element_visible(locator)
        element.clear()
    
    def get_text(self, locator):
        """Get text from element"""
        element = self.find_element_visible(locator)
        return element.text
    
    def get_attribute(self, locator, attribute_name):
        """Get attribute value from element"""
        element = self.find_element(locator)
        return element.get_attribute(attribute_name)
    
    # Dropdown methods
    def select_dropdown_by_text(self, locator, text):
        """Select dropdown option by visible text"""
        element = self.find_element_visible(locator)
        SelectHelper.select_by_text(element, text)
    
    def select_dropdown_by_value(self, locator, value):
        """Select dropdown option by value"""
        element = self.find_element_visible(locator)
        SelectHelper.select_by_value(element, value)
    
    def get_selected_dropdown_text(self, locator):
        """Get selected dropdown option text"""
        element = self.find_element_visible(locator)
        return SelectHelper.get_selected_option_text(element)
    
    # Checkbox and radio button methods
    def check_checkbox(self, locator):
        """Check checkbox if not already checked"""
        element = self.find_element_clickable(locator)
        if not element.is_selected():
            element.click()
    
    def uncheck_checkbox(self, locator):
        """Uncheck checkbox if checked"""
        element = self.find_element_clickable(locator)
        if element.is_selected():
            element.click()
    
    def is_checkbox_checked(self, locator):
        """Check if checkbox is selected"""
        element = self.find_element(locator)
        return element.is_selected()
    
    # Alert methods
    def accept_alert(self):
        """Accept alert dialog"""
        return self.alert_helper.accept_alert()
    
    def dismiss_alert(self):
        """Dismiss alert dialog"""
        return self.alert_helper.dismiss_alert()
    
    def get_alert_text(self):
        """Get alert text"""
        return self.alert_helper.get_alert_text()
    
    def send_keys_to_alert(self, text):
        """Send keys to alert prompt"""
        self.alert_helper.send_keys_to_alert(text)
    
    # Screenshot methods
    def take_screenshot(self, filename=None):
        """Take screenshot of current page"""
        return self.screenshot_helper.take_screenshot(self.driver, filename)
    
    def take_element_screenshot(self, locator, filename=None):
        """Take screenshot of specific element"""
        element = self.find_element_visible(locator)
        return self.screenshot_helper.take_element_screenshot(self.driver, element, filename)
    
    # Scroll methods
    def scroll_to_element(self, locator):
        """Scroll to element"""
        element = self.find_element(locator)
        self.action_helper.scroll_to_element(element)
    
    def scroll_to_top(self):
        """Scroll to top of page"""
        self.driver.execute_script("window.scrollTo(0, 0);")
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Window and frame methods
    def switch_to_frame(self, frame_locator):
        """Switch to iframe"""
        frame = self.find_element(frame_locator)
        self.driver.switch_to.frame(frame)
    
    def switch_to_default_content(self):
        """Switch back to default content from iframe"""
        self.driver.switch_to.default_content()
    
    def switch_to_window(self, window_handle):
        """Switch to specific window"""
        self.driver.switch_to.window(window_handle)
    
    def get_window_handles(self):
        """Get all window handles"""
        return self.driver.window_handles
    
    def close_current_window(self):
        """Close current window"""
        self.driver.close()
    
    # Wait methods
    def wait_for_page_to_load(self, timeout=None):
        """Wait for page to load completely"""
        timeout = timeout or Config.PAGE_LOAD_TIMEOUT
        self.driver.implicitly_wait(timeout)
    
    def wait_for_text_in_element(self, locator, text, timeout=None):
        """Wait for specific text to appear in element"""
        wait_helper = WaitHelpers(self.driver, timeout) if timeout else self.wait_helper
        wait_helper.wait_for_text_in_element(locator, text)
    
    def wait_for_url_contains(self, url_part, timeout=None):
        """Wait for URL to contain specific text"""
        wait_helper = WaitHelpers(self.driver, timeout) if timeout else self.wait_helper
        wait_helper.wait_for_url_contains(url_part)
    
    def wait(self, seconds):
        """Simple wait for specified seconds"""
        time.sleep(seconds)
    
    # JavaScript execution methods
    def execute_script(self, script, *args):
        """Execute JavaScript"""
        return self.driver.execute_script(script, *args)
    
    def execute_async_script(self, script, *args):
        """Execute asynchronous JavaScript"""
        return self.driver.execute_async_script(script, *args)
