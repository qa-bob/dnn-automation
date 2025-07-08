import pytest
import os
from datetime import datetime
from utils.driver_factory import DriverFactory
from utils.helpers import ScreenshotHelper, FileHelper
from config.settings import Config

def pytest_addoption(parser):
    """Add command line options"""
    parser.addoption("--browser", action="store", default="chrome", 
                     help="Browser to execute tests (chrome or firefox)")
    parser.addoption("--headless", action="store", default="true", 
                     help="Run tests in headless mode (true/false)")
    parser.addoption("--env", action="store", default="dev", 
                     help="Environment to run tests against (dev/staging/prod)")

@pytest.fixture(scope="session")
def driver(request):
    """Setup WebDriver instance"""
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless").lower() == "true"
    
    # Create necessary directories
    os.makedirs(Config.REPORT_DIR, exist_ok=True)
    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
    
    driver_instance = DriverFactory.get_driver(browser, headless)
    yield driver_instance
    driver_instance.quit()

@pytest.fixture(scope="function")
def page(driver):
    """Page fixture for individual tests"""
    return driver

@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request, driver):
    """Automatically capture screenshot on test failure"""
    yield
    if request.node.rep_call.failed and Config.SCREENSHOT_ON_FAILURE:
        test_name = request.node.name
        class_name = request.node.parent.name if hasattr(request.node, 'parent') else "unknown"
        filename = f"{class_name}_{test_name}_failed"
        ScreenshotHelper.take_screenshot(driver, filename)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot functionality"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment(request):
    """Setup test environment"""
    env = request.config.getoption("--env")
    os.environ['TEST_ENV'] = env
    
    # Clean up downloads directory before tests
    FileHelper.cleanup_downloads()
    
    yield
    
    # Clean up after tests
    FileHelper.cleanup_downloads()

@pytest.fixture(scope="session")
def test_config(request):
    """Provide test configuration"""
    return {
        'browser': request.config.getoption("--browser"),
        'headless': request.config.getoption("--headless").lower() == "true",
        'environment': request.config.getoption("--env"),
        'base_url': Config.BASE_URL
    }

# Pytest HTML report customization
def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Test Automation Framework - Test Results"

def pytest_html_results_summary(prefix, summary, postfix):
    """Customize HTML report summary"""
    prefix.extend([f"<p>Test Environment: {Config.ENVIRONMENT}</p>"])
    prefix.extend([f"<p>Base URL: {Config.BASE_URL}</p>"])
    prefix.extend([f"<p>Test Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"])

# Custom markers for test categorization
def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "functional: mark test as functional test")
    config.addinivalue_line("markers", "ui: mark test as UI test")
    config.addinivalue_line("markers", "performance: mark test as performance test")
    config.addinivalue_line("markers", "cross_browser: mark test as cross-browser test")
    config.addinivalue_line("markers", "accessibility: mark test as accessibility test")
    config.addinivalue_line("markers", "negative: mark test as negative test")
    config.addinivalue_line("markers", "authentication: mark test as authentication test")
    config.addinivalue_line("markers", "dynamic_content: mark test as dynamic content test")
    config.addinivalue_line("markers", "user_interactions: mark test as user interactions test")
    config.addinivalue_line("markers", "file_operations: mark test as file operations test")
    config.addinivalue_line("markers", "navigation: mark test as navigation test")
    config.addinivalue_line("markers", "advanced: mark test as advanced test")
