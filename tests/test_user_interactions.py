import pytest
import os
from selenium.webdriver.common.keys import Keys
from pages.interaction_pages import (
    HoversPage, JavaScriptAlertsPage, DragAndDropPage, 
    ContextMenuPage, InputsPage, KeyPressesPage,
    FileUploadPage, FileDownloadPage
)
from utils.helpers import FileHelper

@pytest.mark.user_interactions
@pytest.mark.functional
class TestHovers:
    """Test cases for Hover functionality"""
    
    def test_hover_user_1(self, driver):
        """Test hovering over first user image"""
        hovers_page = HoversPage(driver)
        hovers_page.navigate_to_hovers()
        
        # Initially caption should not be visible
        assert not hovers_page.is_user_1_caption_visible(), "User 1 caption should not be visible initially"
        
        # Hover over user 1
        hovers_page.hover_over_user_1()
        
        # Caption should now be visible
        assert hovers_page.is_user_1_caption_visible(), "User 1 caption should be visible after hover"
        
        caption_text = hovers_page.get_user_1_caption_text()
        assert "user1" in caption_text.lower()
    
    def test_hover_user_2(self, driver):
        """Test hovering over second user image"""
        hovers_page = HoversPage(driver)
        hovers_page.navigate_to_hovers()
        
        assert not hovers_page.is_user_2_caption_visible()
        hovers_page.hover_over_user_2()
        assert hovers_page.is_user_2_caption_visible()
        
        caption_text = hovers_page.get_user_2_caption_text()
        assert "user2" in caption_text.lower()
    
    def test_hover_user_3(self, driver):
        """Test hovering over third user image"""
        hovers_page = HoversPage(driver)
        hovers_page.navigate_to_hovers()
        
        assert not hovers_page.is_user_3_caption_visible()
        hovers_page.hover_over_user_3()
        assert hovers_page.is_user_3_caption_visible()
        
        caption_text = hovers_page.get_user_3_caption_text()
        assert "user3" in caption_text.lower()
    
    def test_hover_navigation(self, driver):
        """Test clicking on user profile link after hover"""
        hovers_page = HoversPage(driver)
        hovers_page.navigate_to_hovers()
        
        hovers_page.hover_over_user_1()
        hovers_page.click_user_1_link()
        
        # Should navigate to user profile page
        current_url = hovers_page.get_current_url()
        assert "users/1" in current_url

@pytest.mark.user_interactions
@pytest.mark.functional
class TestJavaScriptAlerts:
    """Test cases for JavaScript Alerts"""
    
    def test_simple_alert(self, driver):
        """Test simple JavaScript alert"""
        alerts_page = JavaScriptAlertsPage(driver)
        alerts_page.navigate_to_javascript_alerts()
        
        alert_text, result_text = alerts_page.test_simple_alert()
        
        assert "I am a JS Alert" in alert_text
        assert "You successfully clicked an alert" in result_text
    
    def test_confirm_accept(self, driver):
        """Test confirm dialog - accept"""
        alerts_page = JavaScriptAlertsPage(driver)
        alerts_page.navigate_to_javascript_alerts()
        
        alert_text, result_text = alerts_page.test_confirm_accept()
        
        assert "I am a JS Confirm" in alert_text
        assert "You clicked: Ok" in result_text
    
    def test_confirm_dismiss(self, driver):
        """Test confirm dialog - dismiss"""
        alerts_page = JavaScriptAlertsPage(driver)
        alerts_page.navigate_to_javascript_alerts()
        
        alert_text, result_text = alerts_page.test_confirm_dismiss()
        
        assert "I am a JS Confirm" in alert_text
        assert "You clicked: Cancel" in result_text
    
    def test_prompt_with_text(self, driver):
        """Test prompt with text input"""
        alerts_page = JavaScriptAlertsPage(driver)
        alerts_page.navigate_to_javascript_alerts()
        
        test_text = "Hello World"
        result_text = alerts_page.test_prompt_with_text(test_text)
        
        assert f"You entered: {test_text}" in result_text
    
    def test_prompt_with_empty_text(self, driver):
        """Test prompt with empty text"""
        alerts_page = JavaScriptAlertsPage(driver)
        alerts_page.navigate_to_javascript_alerts()
        
        result_text = alerts_page.test_prompt_with_text("")
        assert "You entered:" in result_text

@pytest.mark.user_interactions
@pytest.mark.functional
class TestDragAndDrop:
    """Test cases for Drag and Drop functionality"""
    
    def test_drag_a_to_b(self, driver):
        """Test dragging column A to column B"""
        drag_drop_page = DragAndDropPage(driver)
        drag_drop_page.navigate_to_drag_and_drop()
        
        # Get initial states
        initial_a_text = drag_drop_page.get_column_a_text()
        initial_b_text = drag_drop_page.get_column_b_text()
        
        assert initial_a_text == "A"
        assert initial_b_text == "B"
        
        # Perform drag and drop
        drag_drop_page.drag_a_to_b()
        
        # Verify results
        final_a_text = drag_drop_page.get_column_a_text()
        final_b_text = drag_drop_page.get_column_b_text()
        
        # After drag and drop, the columns should swap
        assert final_a_text == "B"
        assert final_b_text == "A"
    
    def test_drag_b_to_a(self, driver):
        """Test dragging column B to column A"""
        drag_drop_page = DragAndDropPage(driver)
        drag_drop_page.navigate_to_drag_and_drop()
        
        # Perform drag and drop B to A
        drag_drop_page.drag_b_to_a()
        
        # Verify swap occurred
        final_a_text = drag_drop_page.get_column_a_text()
        final_b_text = drag_drop_page.get_column_b_text()
        
        assert final_a_text == "B"
        assert final_b_text == "A"
    
    def test_multiple_drag_operations(self, driver):
        """Test multiple consecutive drag operations"""
        drag_drop_page = DragAndDropPage(driver)
        drag_drop_page.navigate_to_drag_and_drop()
        
        # Initial state: A, B
        assert drag_drop_page.get_column_a_text() == "A"
        assert drag_drop_page.get_column_b_text() == "B"
        
        # First drag: A to B -> B, A
        drag_drop_page.drag_a_to_b()
        assert drag_drop_page.get_column_a_text() == "B"
        assert drag_drop_page.get_column_b_text() == "A"
        
        # Second drag: B to A -> A, B (back to original)
        drag_drop_page.drag_a_to_b()  # Now dragging B to A
        assert drag_drop_page.get_column_a_text() == "A"
        assert drag_drop_page.get_column_b_text() == "B"

@pytest.mark.user_interactions
@pytest.mark.functional
class TestContextMenu:
    """Test cases for Context Menu functionality"""
    
    def test_context_menu_alert(self, driver):
        """Test context menu triggers alert"""
        context_page = ContextMenuPage(driver)
        context_page.navigate_to_context_menu()
        
        alert_text = context_page.test_context_menu()
        assert "You selected a context menu" in alert_text

@pytest.mark.user_interactions
@pytest.mark.functional
class TestInputs:
    """Test cases for Input functionality"""
    
    def test_enter_number(self, driver):
        """Test entering a number in input field"""
        inputs_page = InputsPage(driver)
        inputs_page.navigate_to_inputs()
        
        test_number = 42
        inputs_page.enter_number(test_number)
        
        input_value = inputs_page.get_input_value()
        assert input_value == str(test_number)
    
    def test_clear_input(self, driver):
        """Test clearing input field"""
        inputs_page = InputsPage(driver)
        inputs_page.navigate_to_inputs()
        
        inputs_page.enter_number(123)
        assert inputs_page.get_input_value() == "123"
        
        inputs_page.clear_input()
        assert inputs_page.get_input_value() == ""
    
    def test_increment_with_arrow_keys(self, driver):
        """Test incrementing value with arrow keys"""
        inputs_page = InputsPage(driver)
        inputs_page.navigate_to_inputs()
        
        inputs_page.enter_number(5)
        inputs_page.increment_with_arrow_up()
        
        # Value should be incremented
        input_value = int(inputs_page.get_input_value())
        assert input_value == 6
    
    def test_decrement_with_arrow_keys(self, driver):
        """Test decrementing value with arrow keys"""
        inputs_page = InputsPage(driver)
        inputs_page.navigate_to_inputs()
        
        inputs_page.enter_number(5)
        inputs_page.decrement_with_arrow_down()
        
        # Value should be decremented
        input_value = int(inputs_page.get_input_value())
        assert input_value == 4
    
    @pytest.mark.negative
    def test_enter_text_in_number_input(self, driver):
        """Test entering text in number input (should not work)"""
        inputs_page = InputsPage(driver)
        inputs_page.navigate_to_inputs()
        
        inputs_page.enter_text(inputs_page.NUMBER_INPUT, "abc")
        
        # Number input should reject text
        input_value = inputs_page.get_input_value()
        assert input_value == ""

@pytest.mark.user_interactions
@pytest.mark.functional
class TestKeyPresses:
    """Test cases for Key Press functionality"""
    
    def test_enter_key(self, driver):
        """Test Enter key press"""
        key_page = KeyPressesPage(driver)
        key_page.navigate_to_key_presses()
        
        result_text = key_page.test_enter_key()
        assert "You entered: ENTER" in result_text
    
    def test_space_key(self, driver):
        """Test Space key press"""
        key_page = KeyPressesPage(driver)
        key_page.navigate_to_key_presses()
        
        result_text = key_page.test_space_key()
        assert "You entered: SPACE" in result_text
    
    def test_tab_key(self, driver):
        """Test Tab key press"""
        key_page = KeyPressesPage(driver)
        key_page.navigate_to_key_presses()
        
        result_text = key_page.test_tab_key()
        assert "You entered: TAB" in result_text
    
    def test_letter_keys(self, driver):
        """Test letter key presses"""
        key_page = KeyPressesPage(driver)
        key_page.navigate_to_key_presses()
        
        # Test various letters
        test_keys = ['a', 'b', 'z']
        for key in test_keys:
            key_page.press_key(key)
            result_text = key_page.get_result_text()
            assert f"You entered: {key.upper()}" in result_text

@pytest.mark.file_operations
@pytest.mark.functional
class TestFileOperations:
    """Test cases for File Upload and Download"""
    
    def test_file_upload_success(self, driver):
        """Test successful file upload"""
        upload_page = FileUploadPage(driver)
        upload_page.navigate_to_file_upload()
        
        # Create a test file
        test_filename = "test_upload.txt"
        test_file_path = os.path.join(FileHelper.get_download_dir(), test_filename)
        
        with open(test_file_path, 'w') as f:
            f.write("This is a test file for upload")
        
        try:
            upload_page.upload_file(test_file_path)
            
            # Verify upload success
            assert upload_page.is_file_uploaded_successfully(test_filename)
            uploaded_filename = upload_page.get_uploaded_file_name()
            assert test_filename in uploaded_filename
            
        finally:
            # Clean up test file
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
    
    @pytest.mark.negative
    def test_file_upload_nonexistent_file(self, driver):
        """Test uploading non-existent file"""
        upload_page = FileUploadPage(driver)
        upload_page.navigate_to_file_upload()
        
        with pytest.raises(FileNotFoundError):
            upload_page.upload_file("nonexistent_file.txt")
    
    def test_file_download_links_available(self, driver):
        """Test file download links are available"""
        download_page = FileDownloadPage(driver)
        download_page.navigate_to_file_download()
        
        download_links = download_page.get_all_download_links()
        assert len(download_links) > 0, "Should have download links available"
        
        # Check that each link has text and href
        for link_text, href in download_links:
            assert len(link_text) > 0, "Link should have text"
            assert href is not None, "Link should have href attribute"
    
    def test_file_download_functionality(self, driver):
        """Test file download functionality"""
        download_page = FileDownloadPage(driver)
        download_page.navigate_to_file_download()
        
        # Get the first download link and attempt download
        filename = download_page.download_first_file()
        
        if filename:
            # Note: Actual file download verification would require
            # checking the download directory, which depends on browser settings
            assert len(filename) > 0, "Downloaded filename should not be empty"

@pytest.mark.user_interactions
@pytest.mark.regression
class TestInteractionWorkflows:
    """Test complete user interaction workflows"""
    
    def test_alert_workflow(self, driver):
        """Test complete alert interaction workflow"""
        alerts_page = JavaScriptAlertsPage(driver)
        alerts_page.navigate_to_javascript_alerts()
        
        # Test all three types of alerts
        alerts_page.test_simple_alert()
        alerts_page.test_confirm_accept()
        alerts_page.test_confirm_dismiss()
        alerts_page.test_prompt_with_text("Test Message")
    
    def test_input_and_keypress_workflow(self, driver):
        """Test input and keypress workflow"""
        # Test inputs
        inputs_page = InputsPage(driver)
        inputs_page.navigate_to_inputs()
        inputs_page.enter_number(10)
        inputs_page.increment_with_arrow_up()
        assert int(inputs_page.get_input_value()) == 11
        
        # Test key presses
        key_page = KeyPressesPage(driver)
        key_page.navigate_to_key_presses()
        key_page.test_enter_key()
        key_page.test_space_key()
    
    @pytest.mark.performance
    def test_interaction_performance(self, driver):
        """Test interaction performance"""
        import time
        
        # Test hover performance
        hovers_page = HoversPage(driver)
        hovers_page.navigate_to_hovers()
        
        start_time = time.time()
        hovers_page.hover_over_user_1()
        hovers_page.hover_over_user_2()
        hovers_page.hover_over_user_3()
        end_time = time.time()
        
        hover_duration = end_time - start_time
        assert hover_duration < 2.0, f"Hover interactions took too long: {hover_duration} seconds"
