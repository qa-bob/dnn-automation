from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from config.settings import Config
import os

class HoversPage(BasePage):
    """Page Object for Hovers example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/hovers"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h3")
    USER_IMAGES = (By.CSS_SELECTOR, ".figure img")
    USER_1_IMAGE = (By.CSS_SELECTOR, ".figure:nth-of-type(1) img")
    USER_2_IMAGE = (By.CSS_SELECTOR, ".figure:nth-of-type(2) img")
    USER_3_IMAGE = (By.CSS_SELECTOR, ".figure:nth-of-type(3) img")
    
    USER_1_CAPTION = (By.CSS_SELECTOR, ".figure:nth-of-type(1) .figcaption")
    USER_2_CAPTION = (By.CSS_SELECTOR, ".figure:nth-of-type(2) .figcaption")
    USER_3_CAPTION = (By.CSS_SELECTOR, ".figure:nth-of-type(3) .figcaption")
    
    USER_1_LINK = (By.CSS_SELECTOR, ".figure:nth-of-type(1) .figcaption a")
    USER_2_LINK = (By.CSS_SELECTOR, ".figure:nth-of-type(2) .figcaption a")
    USER_3_LINK = (By.CSS_SELECTOR, ".figure:nth-of-type(3) .figcaption a")
    
    def navigate_to_hovers(self):
        """Navigate to hovers page"""
        self.go_to_url(self.url)
    
    def hover_over_user_1(self):
        """Hover over first user image"""
        self.hover_over_element(self.USER_1_IMAGE)
    
    def hover_over_user_2(self):
        """Hover over second user image"""
        self.hover_over_element(self.USER_2_IMAGE)
    
    def hover_over_user_3(self):
        """Hover over third user image"""
        self.hover_over_element(self.USER_3_IMAGE)
    
    def is_user_1_caption_visible(self):
        """Check if user 1 caption is visible"""
        return self.is_element_visible(self.USER_1_CAPTION)
    
    def is_user_2_caption_visible(self):
        """Check if user 2 caption is visible"""
        return self.is_element_visible(self.USER_2_CAPTION)
    
    def is_user_3_caption_visible(self):
        """Check if user 3 caption is visible"""
        return self.is_element_visible(self.USER_3_CAPTION)
    
    def get_user_1_caption_text(self):
        """Get user 1 caption text"""
        return self.get_text(self.USER_1_CAPTION)
    
    def click_user_1_link(self):
        """Click user 1 profile link"""
        self.click(self.USER_1_LINK)

class JavaScriptAlertsPage(BasePage):
    """Page Object for JavaScript Alerts example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/javascript_alerts"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h3")
    JS_ALERT_BUTTON = (By.CSS_SELECTOR, "button[onclick='jsAlert()']")
    JS_CONFIRM_BUTTON = (By.CSS_SELECTOR, "button[onclick='jsConfirm()']")
    JS_PROMPT_BUTTON = (By.CSS_SELECTOR, "button[onclick='jsPrompt()']")
    RESULT_TEXT = (By.ID, "result")
    
    def navigate_to_javascript_alerts(self):
        """Navigate to JavaScript alerts page"""
        self.go_to_url(self.url)
    
    def click_js_alert_button(self):
        """Click JS Alert button"""
        self.click(self.JS_ALERT_BUTTON)
    
    def click_js_confirm_button(self):
        """Click JS Confirm button"""
        self.click(self.JS_CONFIRM_BUTTON)
    
    def click_js_prompt_button(self):
        """Click JS Prompt button"""
        self.click(self.JS_PROMPT_BUTTON)
    
    def handle_alert_and_accept(self):
        """Handle alert and accept it"""
        return self.accept_alert()
    
    def handle_alert_and_dismiss(self):
        """Handle alert and dismiss it"""
        return self.dismiss_alert()
    
    def handle_prompt_with_text(self, text):
        """Handle prompt with specific text"""
        self.send_keys_to_alert(text)
    
    def get_result_text(self):
        """Get result text"""
        return self.get_text(self.RESULT_TEXT)
    
    def test_simple_alert(self):
        """Test simple alert functionality"""
        self.click_js_alert_button()
        alert_text = self.handle_alert_and_accept()
        return alert_text, self.get_result_text()
    
    def test_confirm_accept(self):
        """Test confirm dialog - accept"""
        self.click_js_confirm_button()
        alert_text = self.handle_alert_and_accept()
        return alert_text, self.get_result_text()
    
    def test_confirm_dismiss(self):
        """Test confirm dialog - dismiss"""
        self.click_js_confirm_button()
        alert_text = self.handle_alert_and_dismiss()
        return alert_text, self.get_result_text()
    
    def test_prompt_with_text(self, text):
        """Test prompt with specific text"""
        self.click_js_prompt_button()
        self.handle_prompt_with_text(text)
        return self.get_result_text()

class DragAndDropPage(BasePage):
    """Page Object for Drag and Drop example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/drag_and_drop"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h3")
    COLUMN_A = (By.ID, "column-a")
    COLUMN_B = (By.ID, "column-b")
    COLUMN_A_HEADER = (By.CSS_SELECTOR, "#column-a header")
    COLUMN_B_HEADER = (By.CSS_SELECTOR, "#column-b header")
    
    def navigate_to_drag_and_drop(self):
        """Navigate to drag and drop page"""
        self.go_to_url(self.url)
    
    def get_column_a_text(self):
        """Get column A header text"""
        return self.get_text(self.COLUMN_A_HEADER)
    
    def get_column_b_text(self):
        """Get column B header text"""
        return self.get_text(self.COLUMN_B_HEADER)
    
    def drag_a_to_b(self):
        """Drag column A to column B"""
        source = self.find_element(self.COLUMN_A)
        target = self.find_element(self.COLUMN_B)
        self.action_helper.drag_and_drop(source, target)
    
    def drag_b_to_a(self):
        """Drag column B to column A"""
        source = self.find_element(self.COLUMN_B)
        target = self.find_element(self.COLUMN_A)
        self.action_helper.drag_and_drop(source, target)
    
    def verify_drag_and_drop_result(self, expected_a_text, expected_b_text):
        """Verify drag and drop operation result"""
        actual_a_text = self.get_column_a_text()
        actual_b_text = self.get_column_b_text()
        return actual_a_text == expected_a_text and actual_b_text == expected_b_text

class ContextMenuPage(BasePage):
    """Page Object for Context Menu example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/context_menu"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h3")
    HOT_SPOT = (By.ID, "hot-spot")
    
    def navigate_to_context_menu(self):
        """Navigate to context menu page"""
        self.go_to_url(self.url)
    
    def right_click_hot_spot(self):
        """Right click on the hot spot"""
        self.right_click(self.HOT_SPOT)
    
    def handle_context_menu_alert(self):
        """Handle the context menu alert"""
        return self.accept_alert()
    
    def test_context_menu(self):
        """Test context menu functionality"""
        self.right_click_hot_spot()
        alert_text = self.handle_context_menu_alert()
        return alert_text

class InputsPage(BasePage):
    """Page Object for Inputs example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/inputs"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h3")
    NUMBER_INPUT = (By.CSS_SELECTOR, "input[type='number']")
    
    def navigate_to_inputs(self):
        """Navigate to inputs page"""
        self.go_to_url(self.url)
    
    def enter_number(self, number):
        """Enter number in input field"""
        self.enter_text(self.NUMBER_INPUT, str(number))
    
    def clear_input(self):
        """Clear input field"""
        self.clear_text(self.NUMBER_INPUT)
    
    def get_input_value(self):
        """Get current input value"""
        return self.get_attribute(self.NUMBER_INPUT, "value")
    
    def increment_with_arrow_up(self):
        """Increment value using arrow up key"""
        input_element = self.find_element(self.NUMBER_INPUT)
        input_element.send_keys(Keys.ARROW_UP)
    
    def decrement_with_arrow_down(self):
        """Decrement value using arrow down key"""
        input_element = self.find_element(self.NUMBER_INPUT)
        input_element.send_keys(Keys.ARROW_DOWN)

class KeyPressesPage(BasePage):
    """Page Object for Key Presses example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/key_presses"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h3")
    TARGET_INPUT = (By.ID, "target")
    RESULT_TEXT = (By.ID, "result")
    
    def navigate_to_key_presses(self):
        """Navigate to key presses page"""
        self.go_to_url(self.url)
    
    def press_key(self, key):
        """Press specific key"""
        input_element = self.find_element(self.TARGET_INPUT)
        input_element.send_keys(key)
    
    def get_result_text(self):
        """Get result text"""
        return self.get_text(self.RESULT_TEXT)
    
    def test_key_press(self, key, expected_result):
        """Test key press and verify result"""
        self.press_key(key)
        actual_result = self.get_result_text()
        return expected_result in actual_result
    
    def test_enter_key(self):
        """Test Enter key"""
        self.press_key(Keys.ENTER)
        return self.get_result_text()
    
    def test_space_key(self):
        """Test Space key"""
        self.press_key(Keys.SPACE)
        return self.get_result_text()
    
    def test_tab_key(self):
        """Test Tab key"""
        self.press_key(Keys.TAB)
        return self.get_result_text()

class FileUploadPage(BasePage):
    """Page Object for File Upload example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/upload"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h3")
    FILE_INPUT = (By.ID, "file-upload")
    UPLOAD_BUTTON = (By.ID, "file-submit")
    UPLOADED_FILES = (By.ID, "uploaded-files")
    
    def navigate_to_file_upload(self):
        """Navigate to file upload page"""
        self.go_to_url(self.url)
    
    def select_file(self, file_path):
        """Select file for upload"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_input = self.find_element(self.FILE_INPUT)
        file_input.send_keys(os.path.abspath(file_path))
    
    def click_upload_button(self):
        """Click upload button"""
        self.click(self.UPLOAD_BUTTON)
    
    def upload_file(self, file_path):
        """Complete file upload process"""
        self.select_file(file_path)
        self.click_upload_button()
    
    def get_uploaded_file_name(self):
        """Get uploaded file name"""
        return self.get_text(self.UPLOADED_FILES)
    
    def is_file_uploaded_successfully(self, expected_filename):
        """Check if file was uploaded successfully"""
        uploaded_filename = self.get_uploaded_file_name()
        return expected_filename in uploaded_filename

class FileDownloadPage(BasePage):
    """Page Object for File Download example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/download"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h3")
    DOWNLOAD_LINKS = (By.CSS_SELECTOR, ".example a")
    
    def navigate_to_file_download(self):
        """Navigate to file download page"""
        self.go_to_url(self.url)
    
    def get_all_download_links(self):
        """Get all download links"""
        links = self.find_elements(self.DOWNLOAD_LINKS)
        return [(link.text, link.get_attribute('href')) for link in links]
    
    def click_download_link(self, link_text):
        """Click specific download link"""
        link_locator = (By.LINK_TEXT, link_text)
        self.click(link_locator)
    
    def download_first_file(self):
        """Download the first file in the list"""
        links = self.find_elements(self.DOWNLOAD_LINKS)
        if links:
            first_link = links[0]
            filename = first_link.text
            first_link.click()
            return filename
        return None
