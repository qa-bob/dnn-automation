from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from config.settings import Config

class BasicAuthPage(BasePage):
    """Page Object for Basic Authentication example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/basic_auth"
    
    # Locators
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".example p")
    PAGE_TITLE = (By.TAG_NAME, "h3")
    
    def navigate_to_basic_auth(self):
        """Navigate to basic auth page with credentials"""
        auth_url = f"http://{Config.BASIC_AUTH_USERNAME}:{Config.BASIC_AUTH_PASSWORD}@the-internet.herokuapp.com/basic_auth"
        self.go_to_url(auth_url)
    
    def get_success_message(self):
        """Get the success message after authentication"""
        return self.get_text(self.SUCCESS_MESSAGE)
    
    def get_page_title(self):
        """Get the page title"""
        return self.get_text(self.PAGE_TITLE)
    
    def is_authenticated(self):
        """Check if authentication was successful"""
        return "Congratulations" in self.get_success_message()

class FormAuthenticationPage(BasePage):
    """Page Object for Form Authentication example"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/login"
    
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".radius")
    FLASH_MESSAGE = (By.ID, "flash")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, ".button.secondary.radius")
    PAGE_TITLE = (By.TAG_NAME, "h2")
    
    def navigate_to_form_auth(self):
        """Navigate to form authentication page"""
        self.go_to_url(self.url)
    
    def enter_username(self, username):
        """Enter username"""
        self.enter_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """Enter password"""
        self.enter_text(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)
    
    def login(self, username=None, password=None):
        """Perform complete login process"""
        username = username or Config.FORM_AUTH_USERNAME
        password = password or Config.FORM_AUTH_PASSWORD
        
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def get_flash_message(self):
        """Get flash message"""
        return self.get_text(self.FLASH_MESSAGE)
    
    def is_login_successful(self):
        """Check if login was successful"""
        flash_message = self.get_flash_message()
        return "You logged into a secure area!" in flash_message
    
    def is_login_failed(self):
        """Check if login failed"""
        flash_message = self.get_flash_message()
        return "Your username is invalid!" in flash_message or "Your password is invalid!" in flash_message
    
    def click_logout_button(self):
        """Click logout button"""
        self.click(self.LOGOUT_BUTTON)
    
    def logout(self):
        """Perform logout"""
        self.click_logout_button()
    
    def is_logout_successful(self):
        """Check if logout was successful"""
        flash_message = self.get_flash_message()
        return "You logged out of the secure area!" in flash_message

class SecureAreaPage(BasePage):
    """Page Object for Secure Area (post-login)"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{Config.BASE_URL}/secure"
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h2")
    SECURE_MESSAGE = (By.CSS_SELECTOR, ".example p")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, ".button.secondary.radius")
    FLASH_MESSAGE = (By.ID, "flash")
    
    def get_page_title(self):
        """Get secure area page title"""
        return self.get_text(self.PAGE_TITLE)
    
    def get_secure_message(self):
        """Get secure area message"""
        return self.get_text(self.SECURE_MESSAGE)
    
    def is_on_secure_area(self):
        """Check if currently on secure area"""
        return "Secure Area" in self.get_page_title()
    
    def click_logout(self):
        """Click logout button"""
        self.click(self.LOGOUT_BUTTON)
