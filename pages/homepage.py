from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from config.settings import Config

class HomePage(BasePage):
    """Page Object for the-internet.herokuapp.com homepage"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h1")
    SUBTITLE = (By.TAG_NAME, "h2")
    AVAILABLE_EXAMPLES = (By.CSS_SELECTOR, "ul li a")
    
    # Specific example links
    BASIC_AUTH_LINK = (By.LINK_TEXT, "Basic Auth")
    FORM_AUTHENTICATION_LINK = (By.LINK_TEXT, "Form Authentication")
    CHECKBOXES_LINK = (By.LINK_TEXT, "Checkboxes")
    DROPDOWN_LINK = (By.LINK_TEXT, "Dropdown")
    DYNAMIC_CONTENT_LINK = (By.LINK_TEXT, "Dynamic Content")
    DYNAMIC_CONTROLS_LINK = (By.LINK_TEXT, "Dynamic Controls")
    DYNAMIC_LOADING_LINK = (By.LINK_TEXT, "Dynamic Loading")
    FILE_DOWNLOAD_LINK = (By.LINK_TEXT, "File Download")
    FILE_UPLOAD_LINK = (By.LINK_TEXT, "File Upload")
    HOVERS_LINK = (By.LINK_TEXT, "Hovers")
    JAVASCRIPT_ALERTS_LINK = (By.LINK_TEXT, "JavaScript Alerts")
    DRAG_AND_DROP_LINK = (By.LINK_TEXT, "Drag and Drop")
    CONTEXT_MENU_LINK = (By.LINK_TEXT, "Context Menu")
    INPUTS_LINK = (By.LINK_TEXT, "Inputs")
    KEY_PRESSES_LINK = (By.LINK_TEXT, "Key Presses")
    MULTIPLE_WINDOWS_LINK = (By.LINK_TEXT, "Multiple Windows")
    NOTIFICATION_MESSAGES_LINK = (By.LINK_TEXT, "Notification Messages")
    REDIRECT_LINK = (By.LINK_TEXT, "Redirect Link")
    SORTABLE_DATA_TABLES_LINK = (By.LINK_TEXT, "Sortable Data Tables")
    STATUS_CODES_LINK = (By.LINK_TEXT, "Status Codes")
    TYPOS_LINK = (By.LINK_TEXT, "Typos")
    WYSIWYG_EDITOR_LINK = (By.LINK_TEXT, "WYSIWYG Editor")
    
    def navigate_to_homepage(self):
        """Navigate to the homepage"""
        self.go_to_url(self.url)
    
    def get_page_title_text(self):
        """Get the main page title"""
        return self.get_text(self.PAGE_TITLE)
    
    def get_subtitle_text(self):
        """Get the subtitle"""
        return self.get_text(self.SUBTITLE)
    
    def get_all_example_links(self):
        """Get all available example links"""
        links = self.find_elements(self.AVAILABLE_EXAMPLES)
        return [link.text for link in links]
    
    def click_basic_auth_link(self):
        """Click on Basic Auth example"""
        self.click(self.BASIC_AUTH_LINK)
    
    def click_form_authentication_link(self):
        """Click on Form Authentication example"""
        self.click(self.FORM_AUTHENTICATION_LINK)
    
    def click_checkboxes_link(self):
        """Click on Checkboxes example"""
        self.click(self.CHECKBOXES_LINK)
    
    def click_dropdown_link(self):
        """Click on Dropdown example"""
        self.click(self.DROPDOWN_LINK)
    
    def click_dynamic_content_link(self):
        """Click on Dynamic Content example"""
        self.click(self.DYNAMIC_CONTENT_LINK)
    
    def click_dynamic_controls_link(self):
        """Click on Dynamic Controls example"""
        self.click(self.DYNAMIC_CONTROLS_LINK)
    
    def click_dynamic_loading_link(self):
        """Click on Dynamic Loading example"""
        self.click(self.DYNAMIC_LOADING_LINK)
    
    def click_file_download_link(self):
        """Click on File Download example"""
        self.click(self.FILE_DOWNLOAD_LINK)
    
    def click_file_upload_link(self):
        """Click on File Upload example"""
        self.click(self.FILE_UPLOAD_LINK)
    
    def click_hovers_link(self):
        """Click on Hovers example"""
        self.click(self.HOVERS_LINK)
    
    def click_javascript_alerts_link(self):
        """Click on JavaScript Alerts example"""
        self.click(self.JAVASCRIPT_ALERTS_LINK)
    
    def click_drag_and_drop_link(self):
        """Click on Drag and Drop example"""
        self.click(self.DRAG_AND_DROP_LINK)
    
    def click_context_menu_link(self):
        """Click on Context Menu example"""
        self.click(self.CONTEXT_MENU_LINK)
    
    def click_inputs_link(self):
        """Click on Inputs example"""
        self.click(self.INPUTS_LINK)
    
    def click_key_presses_link(self):
        """Click on Key Presses example"""
        self.click(self.KEY_PRESSES_LINK)
    
    def click_multiple_windows_link(self):
        """Click on Multiple Windows example"""
        self.click(self.MULTIPLE_WINDOWS_LINK)
    
    def click_notification_messages_link(self):
        """Click on Notification Messages example"""
        self.click(self.NOTIFICATION_MESSAGES_LINK)
    
    def click_redirect_link(self):
        """Click on Redirect Link example"""
        self.click(self.REDIRECT_LINK)
    
    def click_sortable_data_tables_link(self):
        """Click on Sortable Data Tables example"""
        self.click(self.SORTABLE_DATA_TABLES_LINK)
    
    def click_status_codes_link(self):
        """Click on Status Codes example"""
        self.click(self.STATUS_CODES_LINK)
    
    def click_typos_link(self):
        """Click on Typos example"""
        self.click(self.TYPOS_LINK)
    
    def click_wysiwyg_editor_link(self):
        """Click on WYSIWYG Editor example"""
        self.click(self.WYSIWYG_EDITOR_LINK)
