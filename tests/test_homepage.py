import pytest
from pages.homepage import HomePage

@pytest.mark.functional
@pytest.mark.smoke
class TestHomePage:
    """Test cases for the-internet.herokuapp.com homepage"""
    
    def test_homepage_title(self, driver):
        """Test homepage title is correct"""
        home_page = HomePage(driver)
        home_page.navigate_to_homepage()
        
        expected_title = "The Internet"
        actual_title = home_page.get_page_title()
        assert expected_title == actual_title, f"Expected title '{expected_title}', but got '{actual_title}'"
    
    def test_homepage_main_heading(self, driver):
        """Test homepage main heading"""
        home_page = HomePage(driver)
        home_page.navigate_to_homepage()
        
        main_heading = home_page.get_page_title_text()
        assert "Welcome to the-internet" in main_heading
    
    def test_homepage_subtitle(self, driver):
        """Test homepage subtitle"""
        home_page = HomePage(driver)
        home_page.navigate_to_homepage()
        
        subtitle = home_page.get_subtitle_text()
        assert "Available Examples" in subtitle
    
    def test_homepage_has_example_links(self, driver):
        """Test homepage contains example links"""
        home_page = HomePage(driver)
        home_page.navigate_to_homepage()
        
        example_links = home_page.get_all_example_links()
        assert len(example_links) > 0, "No example links found on homepage"
        
        # Check for specific examples
        expected_examples = [
            "Basic Auth",
            "Form Authentication", 
            "Checkboxes",
            "Dropdown",
            "Dynamic Content",
            "JavaScript Alerts",
            "File Download",
            "File Upload"
        ]
        
        for example in expected_examples:
            assert example in example_links, f"Example '{example}' not found in homepage links"
    
    @pytest.mark.navigation
    def test_navigation_to_basic_auth(self, driver):
        """Test navigation to Basic Auth page"""
        home_page = HomePage(driver)
        home_page.navigate_to_homepage()
        home_page.click_basic_auth_link()
        
        # Should be redirected to basic auth page
        current_url = home_page.get_current_url()
        assert "basic_auth" in current_url
    
    @pytest.mark.navigation
    def test_navigation_to_form_authentication(self, driver):
        """Test navigation to Form Authentication page"""
        home_page = HomePage(driver)
        home_page.navigate_to_homepage()
        home_page.click_form_authentication_link()
        
        current_url = home_page.get_current_url()
        assert "login" in current_url
    
    @pytest.mark.navigation
    def test_navigation_to_checkboxes(self, driver):
        """Test navigation to Checkboxes page"""
        home_page = HomePage(driver)
        home_page.navigate_to_homepage()
        home_page.click_checkboxes_link()
        
        current_url = home_page.get_current_url()
        assert "checkboxes" in current_url
    
    @pytest.mark.navigation
    def test_navigation_to_dropdown(self, driver):
        """Test navigation to Dropdown page"""
        home_page = HomePage(driver)
        home_page.navigate_to_homepage()
        home_page.click_dropdown_link()
        
        current_url = home_page.get_current_url()
        assert "dropdown" in current_url
    
    @pytest.mark.ui
    def test_homepage_responsive_design(self, driver):
        """Test homepage responsive design"""
        home_page = HomePage(driver)
        home_page.navigate_to_homepage()
        
        # Test different window sizes
        original_size = driver.get_window_size()
        
        try:
            # Test mobile size
            driver.set_window_size(375, 667)
            assert home_page.is_element_visible(home_page.PAGE_TITLE)
            
            # Test tablet size
            driver.set_window_size(768, 1024)
            assert home_page.is_element_visible(home_page.PAGE_TITLE)
            
            # Test desktop size
            driver.set_window_size(1920, 1080)
            assert home_page.is_element_visible(home_page.PAGE_TITLE)
            
        finally:
            # Restore original size
            driver.set_window_size(original_size['width'], original_size['height'])
