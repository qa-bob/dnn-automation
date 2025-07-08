from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from config.settings import Config
import time

class CheckboxesPage(BasePage):
    """Page Object for Checkboxes example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/checkboxes"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h3")
    CHECKBOX_1 = (By.CSS_SELECTOR, "input[type='checkbox']:nth-of-type(1)")
    CHECKBOX_2 = (By.CSS_SELECTOR, "input[type='checkbox']:nth-of-type(2)")
    ALL_CHECKBOXES = (By.CSS_SELECTOR, "input[type='checkbox']")
    
    def navigate_to_checkboxes(self):
        """Navigate to checkboxes page"""
        self.go_to_url(self.url)
    
    def check_first_checkbox(self):
        """Check the first checkbox"""
        self.check_checkbox(self.CHECKBOX_1)
    
    def uncheck_first_checkbox(self):
        """Uncheck the first checkbox"""
        self.uncheck_checkbox(self.CHECKBOX_1)
    
    def check_second_checkbox(self):
        """Check the second checkbox"""
        self.check_checkbox(self.CHECKBOX_2)
    
    def uncheck_second_checkbox(self):
        """Uncheck the second checkbox"""
        self.uncheck_checkbox(self.CHECKBOX_2)
    
    def is_first_checkbox_checked(self):
        """Check if first checkbox is selected"""
        return self.is_checkbox_checked(self.CHECKBOX_1)
    
    def is_second_checkbox_checked(self):
        """Check if second checkbox is selected"""
        return self.is_checkbox_checked(self.CHECKBOX_2)
    
    def get_all_checkbox_states(self):
        """Get states of all checkboxes"""
        checkboxes = self.find_elements(self.ALL_CHECKBOXES)
        return [checkbox.is_selected() for checkbox in checkboxes]

class DropdownPage(BasePage):
    """Page Object for Dropdown example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/dropdown"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h3")
    DROPDOWN = (By.ID, "dropdown")
    
    def navigate_to_dropdown(self):
        """Navigate to dropdown page"""
        self.go_to_url(self.url)
    
    def select_option_by_text(self, text):
        """Select dropdown option by visible text"""
        self.select_dropdown_by_text(self.DROPDOWN, text)
    
    def select_option_by_value(self, value):
        """Select dropdown option by value"""
        self.select_dropdown_by_value(self.DROPDOWN, value)
    
    def get_selected_option(self):
        """Get currently selected option"""
        return self.get_selected_dropdown_text(self.DROPDOWN)
    
    def select_option_1(self):
        """Select Option 1"""
        self.select_option_by_text("Option 1")
    
    def select_option_2(self):
        """Select Option 2"""
        self.select_option_by_text("Option 2")

class DynamicContentPage(BasePage):
    """Page Object for Dynamic Content example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/dynamic_content"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h3")
    CLICK_HERE_LINK = (By.LINK_TEXT, "click here")
    CONTENT_ROWS = (By.CSS_SELECTOR, ".large-10.columns")
    IMAGES = (By.CSS_SELECTOR, ".large-2.columns img")
    
    def navigate_to_dynamic_content(self):
        """Navigate to dynamic content page"""
        self.go_to_url(self.url)
    
    def click_refresh_content(self):
        """Click to refresh dynamic content"""
        self.click(self.CLICK_HERE_LINK)
    
    def get_all_content_text(self):
        """Get all content text"""
        content_elements = self.find_elements(self.CONTENT_ROWS)
        return [element.text for element in content_elements]
    
    def get_all_image_sources(self):
        """Get all image sources"""
        images = self.find_elements(self.IMAGES)
        return [img.get_attribute("src") for img in images]
    
    def refresh_and_compare_content(self):
        """Refresh content and compare before/after"""
        original_content = self.get_all_content_text()
        original_images = self.get_all_image_sources()
        
        self.click_refresh_content()
        time.sleep(2)  # Wait for content to load
        
        new_content = self.get_all_content_text()
        new_images = self.get_all_image_sources()
        
        return {
            'content_changed': original_content != new_content,
            'images_changed': original_images != new_images
        }

class DynamicControlsPage(BasePage):
    """Page Object for Dynamic Controls example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/dynamic_controls"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h4")
    CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")
    REMOVE_ADD_BUTTON = (By.CSS_SELECTOR, "#checkbox-example button")
    CHECKBOX_MESSAGE = (By.CSS_SELECTOR, "#checkbox-example #message")
    
    INPUT_FIELD = (By.CSS_SELECTOR, "input[type='text']")
    ENABLE_DISABLE_BUTTON = (By.CSS_SELECTOR, "#input-example button")
    INPUT_MESSAGE = (By.CSS_SELECTOR, "#input-example #message")
    
    def navigate_to_dynamic_controls(self):
        """Navigate to dynamic controls page"""
        self.go_to_url(self.url)
    
    def click_remove_add_button(self):
        """Click remove/add button"""
        self.click(self.REMOVE_ADD_BUTTON)
    
    def wait_for_checkbox_message(self, expected_text, timeout=10):
        """Wait for specific message to appear"""
        self.wait_for_text_in_element(self.CHECKBOX_MESSAGE, expected_text, timeout)
    
    def is_checkbox_present(self):
        """Check if checkbox is present"""
        return self.is_element_present(self.CHECKBOX)
    
    def get_checkbox_message(self):
        """Get checkbox message"""
        return self.get_text(self.CHECKBOX_MESSAGE)
    
    def remove_checkbox(self):
        """Remove checkbox and wait for completion"""
        self.click_remove_add_button()
        self.wait_for_checkbox_message("It's gone!", timeout=10)
    
    def add_checkbox(self):
        """Add checkbox and wait for completion"""
        self.click_remove_add_button()
        self.wait_for_checkbox_message("It's back!", timeout=10)
    
    def click_enable_disable_button(self):
        """Click enable/disable button"""
        self.click(self.ENABLE_DISABLE_BUTTON)
    
    def wait_for_input_message(self, expected_text, timeout=10):
        """Wait for input message to appear"""
        self.wait_for_text_in_element(self.INPUT_MESSAGE, expected_text, timeout)
    
    def is_input_enabled(self):
        """Check if input field is enabled"""
        input_element = self.find_element(self.INPUT_FIELD)
        return input_element.is_enabled()
    
    def get_input_message(self):
        """Get input message"""
        return self.get_text(self.INPUT_MESSAGE)
    
    def enable_input(self):
        """Enable input field and wait for completion"""
        self.click_enable_disable_button()
        self.wait_for_input_message("It's enabled!", timeout=10)
    
    def disable_input(self):
        """Disable input field and wait for completion"""
        self.click_enable_disable_button()
        self.wait_for_input_message("It's disabled!", timeout=10)

class DynamicLoadingPage(BasePage):
    """Page Object for Dynamic Loading example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/dynamic_loading"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h3")
    EXAMPLE_1_LINK = (By.LINK_TEXT, "Example 1: Element on page that is hidden")
    EXAMPLE_2_LINK = (By.LINK_TEXT, "Example 2: Element rendered after the fact")
    
    def navigate_to_dynamic_loading(self):
        """Navigate to dynamic loading page"""
        self.go_to_url(self.url)
    
    def click_example_1(self):
        """Click on Example 1"""
        self.click(self.EXAMPLE_1_LINK)
    
    def click_example_2(self):
        """Click on Example 2"""
        self.click(self.EXAMPLE_2_LINK)

class DynamicLoadingExample1Page(BasePage):
    """Page Object for Dynamic Loading Example 1"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/dynamic_loading/1"
    
    # Locators
    START_BUTTON = (By.CSS_SELECTOR, "#start button")
    LOADING_INDICATOR = (By.ID, "loading")
    FINISH_TEXT = (By.ID, "finish")
    
    def navigate_to_example_1(self):
        """Navigate to example 1"""
        self.go_to_url(self.url)
    
    def click_start(self):
        """Click start button"""
        self.click(self.START_BUTTON)
    
    def wait_for_loading_to_complete(self, timeout=10):
        """Wait for loading to complete and element to be visible"""
        self.wait_for_element_visible(self.FINISH_TEXT, timeout)
    
    def get_finish_text(self):
        """Get the finish text"""
        return self.get_text(self.FINISH_TEXT)
    
    def is_loading_visible(self):
        """Check if loading indicator is visible"""
        return self.is_element_visible(self.LOADING_INDICATOR)

class DynamicLoadingExample2Page(BasePage):
    """Page Object for Dynamic Loading Example 2"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/dynamic_loading/2"
    
    # Locators
    START_BUTTON = (By.CSS_SELECTOR, "#start button")
    LOADING_INDICATOR = (By.ID, "loading")
    FINISH_TEXT = (By.ID, "finish")
    
    def navigate_to_example_2(self):
        """Navigate to example 2"""
        self.go_to_url(self.url)
    
    def click_start(self):
        """Click start button"""
        self.click(self.START_BUTTON)
    
    def wait_for_element_to_appear(self, timeout=10):
        """Wait for finish element to appear"""
        self.wait_for_element_present(self.FINISH_TEXT, timeout)
    
    def get_finish_text(self):
        """Get the finish text"""
        return self.get_text(self.FINISH_TEXT)
    
    def is_finish_element_present(self):
        """Check if finish element is present"""
        return self.is_element_present(self.FINISH_TEXT)
