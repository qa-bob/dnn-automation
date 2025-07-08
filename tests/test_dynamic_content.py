import pytest
from pages.dynamic_content_pages import (
    CheckboxesPage, DropdownPage, DynamicContentPage, 
    DynamicControlsPage, DynamicLoadingExample1Page, DynamicLoadingExample2Page
)

@pytest.mark.dynamic_content
@pytest.mark.functional
class TestCheckboxes:
    """Test cases for Checkboxes functionality"""
    
    def test_checkbox_initial_states(self, driver):
        """Test initial states of checkboxes"""
        checkboxes_page = CheckboxesPage(driver)
        checkboxes_page.navigate_to_checkboxes()
        
        # Check initial states
        assert not checkboxes_page.is_first_checkbox_checked(), "First checkbox should be unchecked initially"
        assert checkboxes_page.is_second_checkbox_checked(), "Second checkbox should be checked initially"
    
    def test_check_first_checkbox(self, driver):
        """Test checking the first checkbox"""
        checkboxes_page = CheckboxesPage(driver)
        checkboxes_page.navigate_to_checkboxes()
        
        checkboxes_page.check_first_checkbox()
        assert checkboxes_page.is_first_checkbox_checked(), "First checkbox should be checked after clicking"
    
    def test_uncheck_second_checkbox(self, driver):
        """Test unchecking the second checkbox"""
        checkboxes_page = CheckboxesPage(driver)
        checkboxes_page.navigate_to_checkboxes()
        
        checkboxes_page.uncheck_second_checkbox()
        assert not checkboxes_page.is_second_checkbox_checked(), "Second checkbox should be unchecked after clicking"
    
    def test_toggle_checkboxes(self, driver):
        """Test toggling both checkboxes"""
        checkboxes_page = CheckboxesPage(driver)
        checkboxes_page.navigate_to_checkboxes()
        
        # Toggle first checkbox (uncheck -> check)
        initial_state_1 = checkboxes_page.is_first_checkbox_checked()
        checkboxes_page.check_first_checkbox()
        assert checkboxes_page.is_first_checkbox_checked() != initial_state_1
        
        # Toggle second checkbox (check -> uncheck)
        initial_state_2 = checkboxes_page.is_second_checkbox_checked()
        checkboxes_page.uncheck_second_checkbox()
        assert checkboxes_page.is_second_checkbox_checked() != initial_state_2
    
    def test_all_checkbox_states(self, driver):
        """Test getting all checkbox states"""
        checkboxes_page = CheckboxesPage(driver)
        checkboxes_page.navigate_to_checkboxes()
        
        states = checkboxes_page.get_all_checkbox_states()
        assert len(states) == 2, "Should have exactly 2 checkboxes"
        assert isinstance(states[0], bool), "First state should be boolean"
        assert isinstance(states[1], bool), "Second state should be boolean"

@pytest.mark.dynamic_content
@pytest.mark.functional
class TestDropdown:
    """Test cases for Dropdown functionality"""
    
    def test_dropdown_default_selection(self, driver):
        """Test dropdown default selection"""
        dropdown_page = DropdownPage(driver)
        dropdown_page.navigate_to_dropdown()
        
        selected_option = dropdown_page.get_selected_option()
        assert "Please select an option" in selected_option
    
    def test_select_option_1(self, driver):
        """Test selecting Option 1"""
        dropdown_page = DropdownPage(driver)
        dropdown_page.navigate_to_dropdown()
        
        dropdown_page.select_option_1()
        selected_option = dropdown_page.get_selected_option()
        assert selected_option == "Option 1"
    
    def test_select_option_2(self, driver):
        """Test selecting Option 2"""
        dropdown_page = DropdownPage(driver)
        dropdown_page.navigate_to_dropdown()
        
        dropdown_page.select_option_2()
        selected_option = dropdown_page.get_selected_option()
        assert selected_option == "Option 2"
    
    def test_select_by_value(self, driver):
        """Test selecting options by value"""
        dropdown_page = DropdownPage(driver)
        dropdown_page.navigate_to_dropdown()
        
        dropdown_page.select_option_by_value("1")
        selected_option = dropdown_page.get_selected_option()
        assert selected_option == "Option 1"
        
        dropdown_page.select_option_by_value("2")
        selected_option = dropdown_page.get_selected_option()
        assert selected_option == "Option 2"
    
    @pytest.mark.negative
    def test_select_invalid_option(self, driver):
        """Test selecting invalid option (should not change selection)"""
        dropdown_page = DropdownPage(driver)
        dropdown_page.navigate_to_dropdown()
        
        # First select a valid option
        dropdown_page.select_option_1()
        assert dropdown_page.get_selected_option() == "Option 1"
        
        # Try to select invalid option - this should raise an exception
        with pytest.raises(Exception):
            dropdown_page.select_option_by_text("Invalid Option")

@pytest.mark.dynamic_content
@pytest.mark.functional
class TestDynamicContent:
    """Test cases for Dynamic Content"""
    
    def test_dynamic_content_changes(self, driver):
        """Test that content changes when refreshed"""
        dynamic_page = DynamicContentPage(driver)
        dynamic_page.navigate_to_dynamic_content()
        
        result = dynamic_page.refresh_and_compare_content()
        
        # Content should change (though this might occasionally fail if same content is randomly selected)
        # We'll test multiple times to increase confidence
        changes_detected = False
        for _ in range(3):
            result = dynamic_page.refresh_and_compare_content()
            if result['content_changed'] or result['images_changed']:
                changes_detected = True
                break
        
        assert changes_detected, "Dynamic content should change after refresh"
    
    def test_dynamic_content_structure(self, driver):
        """Test that dynamic content maintains structure"""
        dynamic_page = DynamicContentPage(driver)
        dynamic_page.navigate_to_dynamic_content()
        
        content_texts = dynamic_page.get_all_content_text()
        image_sources = dynamic_page.get_all_image_sources()
        
        assert len(content_texts) > 0, "Should have content text elements"
        assert len(image_sources) > 0, "Should have image elements"
        
        # Refresh and check structure is maintained
        dynamic_page.click_refresh_content()
        dynamic_page.wait(2)  # Wait for content to load
        
        new_content_texts = dynamic_page.get_all_content_text()
        new_image_sources = dynamic_page.get_all_image_sources()
        
        assert len(new_content_texts) == len(content_texts), "Content structure should be maintained"
        assert len(new_image_sources) == len(image_sources), "Image structure should be maintained"

@pytest.mark.dynamic_content
@pytest.mark.functional
class TestDynamicControls:
    """Test cases for Dynamic Controls"""
    
    def test_remove_checkbox(self, driver):
        """Test removing checkbox"""
        controls_page = DynamicControlsPage(driver)
        controls_page.navigate_to_dynamic_controls()
        
        # Initially checkbox should be present
        assert controls_page.is_checkbox_present(), "Checkbox should be present initially"
        
        # Remove checkbox
        controls_page.remove_checkbox()
        
        # Checkbox should be gone
        assert not controls_page.is_checkbox_present(), "Checkbox should be removed"
        assert "It's gone!" in controls_page.get_checkbox_message()
    
    def test_add_checkbox(self, driver):
        """Test adding checkbox back"""
        controls_page = DynamicControlsPage(driver)
        controls_page.navigate_to_dynamic_controls()
        
        # Remove checkbox first
        controls_page.remove_checkbox()
        assert not controls_page.is_checkbox_present()
        
        # Add checkbox back
        controls_page.add_checkbox()
        
        # Checkbox should be present again
        assert controls_page.is_checkbox_present(), "Checkbox should be added back"
        assert "It's back!" in controls_page.get_checkbox_message()
    
    def test_enable_input(self, driver):
        """Test enabling input field"""
        controls_page = DynamicControlsPage(driver)
        controls_page.navigate_to_dynamic_controls()
        
        # Initially input should be disabled
        assert not controls_page.is_input_enabled(), "Input should be disabled initially"
        
        # Enable input
        controls_page.enable_input()
        
        # Input should be enabled
        assert controls_page.is_input_enabled(), "Input should be enabled"
        assert "It's enabled!" in controls_page.get_input_message()
    
    def test_disable_input(self, driver):
        """Test disabling input field"""
        controls_page = DynamicControlsPage(driver)
        controls_page.navigate_to_dynamic_controls()
        
        # Enable input first
        controls_page.enable_input()
        assert controls_page.is_input_enabled()
        
        # Disable input
        controls_page.disable_input()
        
        # Input should be disabled
        assert not controls_page.is_input_enabled(), "Input should be disabled"
        assert "It's disabled!" in controls_page.get_input_message()

@pytest.mark.dynamic_content
@pytest.mark.functional
class TestDynamicLoading:
    """Test cases for Dynamic Loading"""
    
    def test_dynamic_loading_example_1(self, driver):
        """Test dynamic loading example 1 (hidden element becomes visible)"""
        loading_page = DynamicLoadingExample1Page(driver)
        loading_page.navigate_to_example_1()
        
        # Click start and wait for completion
        loading_page.click_start()
        loading_page.wait_for_loading_to_complete()
        
        # Verify finish text is displayed
        finish_text = loading_page.get_finish_text()
        assert "Hello World!" in finish_text
    
    def test_dynamic_loading_example_2(self, driver):
        """Test dynamic loading example 2 (element rendered after fact)"""
        loading_page = DynamicLoadingExample2Page(driver)
        loading_page.navigate_to_example_2()
        
        # Initially finish element should not be present
        assert not loading_page.is_finish_element_present(), "Finish element should not be present initially"
        
        # Click start and wait for element to appear
        loading_page.click_start()
        loading_page.wait_for_element_to_appear()
        
        # Verify finish element is now present and has correct text
        assert loading_page.is_finish_element_present(), "Finish element should be present after loading"
        finish_text = loading_page.get_finish_text()
        assert "Hello World!" in finish_text
    
    @pytest.mark.performance
    def test_dynamic_loading_performance(self, driver):
        """Test dynamic loading performance"""
        import time
        
        loading_page = DynamicLoadingExample1Page(driver)
        loading_page.navigate_to_example_1()
        
        start_time = time.time()
        loading_page.click_start()
        loading_page.wait_for_loading_to_complete(timeout=15)
        end_time = time.time()
        
        loading_duration = end_time - start_time
        assert loading_duration < 10.0, f"Loading took too long: {loading_duration} seconds"
        
        finish_text = loading_page.get_finish_text()
        assert "Hello World!" in finish_text

@pytest.mark.dynamic_content
@pytest.mark.regression
class TestDynamicContentWorkflows:
    """Test complete dynamic content workflows"""
    
    def test_checkbox_and_dropdown_interaction(self, driver):
        """Test interaction between different dynamic elements"""
        # Test checkboxes
        checkboxes_page = CheckboxesPage(driver)
        checkboxes_page.navigate_to_checkboxes()
        checkboxes_page.check_first_checkbox()
        assert checkboxes_page.is_first_checkbox_checked()
        
        # Test dropdown
        dropdown_page = DropdownPage(driver)
        dropdown_page.navigate_to_dropdown()
        dropdown_page.select_option_1()
        assert dropdown_page.get_selected_option() == "Option 1"
        
        # Go back to checkboxes and verify state is reset (new page load)
        checkboxes_page.navigate_to_checkboxes()
        assert not checkboxes_page.is_first_checkbox_checked(), "Checkbox state should reset on new page load"
    
    def test_dynamic_controls_complete_workflow(self, driver):
        """Test complete dynamic controls workflow"""
        controls_page = DynamicControlsPage(driver)
        controls_page.navigate_to_dynamic_controls()
        
        # Test checkbox operations
        assert controls_page.is_checkbox_present()
        controls_page.remove_checkbox()
        assert not controls_page.is_checkbox_present()
        controls_page.add_checkbox()
        assert controls_page.is_checkbox_present()
        
        # Test input operations
        assert not controls_page.is_input_enabled()
        controls_page.enable_input()
        assert controls_page.is_input_enabled()
        controls_page.disable_input()
        assert not controls_page.is_input_enabled()
