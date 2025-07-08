import pytest
from pages.authentication_pages import BasicAuthPage, FormAuthenticationPage, SecureAreaPage
from config.settings import Config

@pytest.mark.authentication
@pytest.mark.functional
class TestBasicAuthentication:
    """Test cases for Basic Authentication"""
    
    def test_basic_auth_success(self, driver):
        """Test successful basic authentication"""
        basic_auth_page = BasicAuthPage(driver)
        basic_auth_page.navigate_to_basic_auth()
        
        assert basic_auth_page.is_authenticated(), "Basic authentication failed"
        
        page_title = basic_auth_page.get_page_title()
        assert "Basic Auth" in page_title
        
        success_message = basic_auth_page.get_success_message()
        assert "Congratulations" in success_message
    
    @pytest.mark.negative
    def test_basic_auth_without_credentials(self, driver):
        """Test basic auth without providing credentials"""
        # Try to access basic auth page without credentials
        basic_auth_page = BasicAuthPage(driver)
        basic_auth_page.go_to_url(f"{Config.BASE_URL}/basic_auth")
        
        # Should show authentication dialog or fail
        page_title = driver.title
        assert page_title != "The Internet"  # Should not show normal page

@pytest.mark.authentication
@pytest.mark.functional
class TestFormAuthentication:
    """Test cases for Form Authentication"""
    
    def test_form_auth_success(self, driver):
        """Test successful form authentication"""
        login_page = FormAuthenticationPage(driver)
        login_page.navigate_to_form_auth()
        
        login_page.login(Config.FORM_AUTH_USERNAME, Config.FORM_AUTH_PASSWORD)
        
        assert login_page.is_login_successful(), "Form authentication failed"
        
        # Should be redirected to secure area
        secure_page = SecureAreaPage(driver)
        assert secure_page.is_on_secure_area(), "Not redirected to secure area"
    
    @pytest.mark.negative
    def test_form_auth_invalid_username(self, driver):
        """Test form authentication with invalid username"""
        login_page = FormAuthenticationPage(driver)
        login_page.navigate_to_form_auth()
        
        login_page.login("invalid_user", Config.FORM_AUTH_PASSWORD)
        
        assert login_page.is_login_failed(), "Login should have failed with invalid username"
        flash_message = login_page.get_flash_message()
        assert "username is invalid" in flash_message
    
    @pytest.mark.negative
    def test_form_auth_invalid_password(self, driver):
        """Test form authentication with invalid password"""
        login_page = FormAuthenticationPage(driver)
        login_page.navigate_to_form_auth()
        
        login_page.login(Config.FORM_AUTH_USERNAME, "invalid_password")
        
        assert login_page.is_login_failed(), "Login should have failed with invalid password"
        flash_message = login_page.get_flash_message()
        assert "password is invalid" in flash_message
    
    @pytest.mark.negative
    def test_form_auth_empty_credentials(self, driver):
        """Test form authentication with empty credentials"""
        login_page = FormAuthenticationPage(driver)
        login_page.navigate_to_form_auth()
        
        login_page.login("", "")
        
        assert login_page.is_login_failed(), "Login should have failed with empty credentials"
    
    def test_form_auth_logout(self, driver):
        """Test logout functionality"""
        login_page = FormAuthenticationPage(driver)
        login_page.navigate_to_form_auth()
        
        # First login
        login_page.login(Config.FORM_AUTH_USERNAME, Config.FORM_AUTH_PASSWORD)
        assert login_page.is_login_successful()
        
        # Then logout
        secure_page = SecureAreaPage(driver)
        secure_page.click_logout()
        
        # Should be back on login page
        assert login_page.is_logout_successful(), "Logout failed"
        current_url = login_page.get_current_url()
        assert "login" in current_url
    
    @pytest.mark.ui
    def test_login_form_elements(self, driver):
        """Test login form UI elements"""
        login_page = FormAuthenticationPage(driver)
        login_page.navigate_to_form_auth()
        
        # Check form elements are present
        assert login_page.is_element_present(login_page.USERNAME_INPUT), "Username input not found"
        assert login_page.is_element_present(login_page.PASSWORD_INPUT), "Password input not found"
        assert login_page.is_element_present(login_page.LOGIN_BUTTON), "Login button not found"
        
        # Check form elements are visible
        assert login_page.is_element_visible(login_page.USERNAME_INPUT), "Username input not visible"
        assert login_page.is_element_visible(login_page.PASSWORD_INPUT), "Password input not visible"
        assert login_page.is_element_visible(login_page.LOGIN_BUTTON), "Login button not visible"
    
    @pytest.mark.ui
    def test_secure_area_elements(self, driver):
        """Test secure area UI elements"""
        # Login first
        login_page = FormAuthenticationPage(driver)
        login_page.navigate_to_form_auth()
        login_page.login(Config.FORM_AUTH_USERNAME, Config.FORM_AUTH_PASSWORD)
        
        secure_page = SecureAreaPage(driver)
        
        # Check secure area elements
        page_title = secure_page.get_page_title()
        assert "Secure Area" in page_title
        
        secure_message = secure_page.get_secure_message()
        assert len(secure_message) > 0, "Secure area message not found"
        
        # Check logout button is present
        assert secure_page.is_element_present(secure_page.LOGOUT_BUTTON), "Logout button not found"
    
    @pytest.mark.performance
    def test_login_performance(self, driver):
        """Test login performance"""
        import time
        
        login_page = FormAuthenticationPage(driver)
        login_page.navigate_to_form_auth()
        
        start_time = time.time()
        login_page.login(Config.FORM_AUTH_USERNAME, Config.FORM_AUTH_PASSWORD)
        end_time = time.time()
        
        login_duration = end_time - start_time
        assert login_duration < 5.0, f"Login took too long: {login_duration} seconds"
        
        assert login_page.is_login_successful(), "Login failed"

@pytest.mark.authentication
@pytest.mark.regression
class TestAuthenticationWorkflow:
    """Test complete authentication workflows"""
    
    def test_complete_login_logout_workflow(self, driver):
        """Test complete login and logout workflow"""
        login_page = FormAuthenticationPage(driver)
        login_page.navigate_to_form_auth()
        
        # Step 1: Login
        login_page.login(Config.FORM_AUTH_USERNAME, Config.FORM_AUTH_PASSWORD)
        assert login_page.is_login_successful()
        
        # Step 2: Verify secure area access
        secure_page = SecureAreaPage(driver)
        assert secure_page.is_on_secure_area()
        
        # Step 3: Logout
        secure_page.click_logout()
        assert login_page.is_logout_successful()
        
        # Step 4: Verify back on login page
        current_url = login_page.get_current_url()
        assert "login" in current_url
    
    def test_multiple_login_attempts(self, driver):
        """Test multiple failed login attempts followed by successful login"""
        login_page = FormAuthenticationPage(driver)
        login_page.navigate_to_form_auth()
        
        # Failed attempts
        for i in range(3):
            login_page.login("invalid_user", "invalid_pass")
            assert login_page.is_login_failed()
            login_page.clear_text(login_page.USERNAME_INPUT)
            login_page.clear_text(login_page.PASSWORD_INPUT)
        
        # Successful attempt
        login_page.login(Config.FORM_AUTH_USERNAME, Config.FORM_AUTH_PASSWORD)
        assert login_page.is_login_successful()
    
    @pytest.mark.cross_browser
    def test_authentication_cross_browser_compatibility(self, driver):
        """Test authentication works across different browsers"""
        login_page = FormAuthenticationPage(driver)
        login_page.navigate_to_form_auth()
        
        # Test basic functionality works regardless of browser
        login_page.login(Config.FORM_AUTH_USERNAME, Config.FORM_AUTH_PASSWORD)
        assert login_page.is_login_successful()
        
        secure_page = SecureAreaPage(driver)
        assert secure_page.is_on_secure_area()
