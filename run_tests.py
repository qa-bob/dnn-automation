#!/usr/bin/env python3
"""
Test Automation Framework - Test Runner
Comprehensive test execution script with advanced features
"""
import pytest
import sys
import os
import argparse
from datetime import datetime
from config.settings import Config

def setup_directories():
    """Create necessary directories"""
    os.makedirs(Config.REPORT_DIR, exist_ok=True)
    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
    os.makedirs("downloads", exist_ok=True)

def get_pytest_args(args):
    """Convert command line arguments to pytest arguments"""
    pytest_args = []
    
    # Add HTML report
    if args.html_report:
        pytest_args.extend([
            "--html", Config.HTML_REPORT_FILE,
            "--self-contained-html"
        ])
    
    # Add browser option
    pytest_args.extend(["--browser", args.browser])
    
    # Add headless option
    pytest_args.extend(["--headless", str(args.headless).lower()])
    
    # Add environment option
    pytest_args.extend(["--env", args.environment])
    
    # Add parallel execution
    if args.parallel and args.workers > 1:
        pytest_args.extend(["-n", str(args.workers)])
    
    # Add markers filter
    if args.markers:
        pytest_args.extend(["-m", args.markers])
    
    # Add test path
    if args.test_path:
        pytest_args.append(args.test_path)
    
    # Add keyword filter
    if args.keyword:
        pytest_args.extend(["-k", args.keyword])
    
    # Add verbose output
    if args.verbose:
        pytest_args.extend(["-v", "-s"])
    
    # Add reruns for flaky tests
    if args.reruns > 0:
        pytest_args.extend(["--reruns", str(args.reruns)])
    
    # Add capture option
    if args.capture == "no":
        pytest_args.append("-s")
    
    # Add failure handling
    if args.stop_on_first_failure:
        pytest_args.append("-x")
    
    if args.max_failures > 0:
        pytest_args.extend(["--maxfail", str(args.max_failures)])
    
    return pytest_args

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Test Automation Framework - Advanced Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tests with HTML report
  python run_tests.py --html-report
  
  # Run smoke tests in parallel with Firefox
  python run_tests.py -m smoke --browser firefox --parallel --workers 4
  
  # Run specific test file with verbose output
  python run_tests.py tests/test_authentication.py --verbose
  
  # Run tests matching keyword in headless mode
  python run_tests.py -k "login" --headless
  
  # Run regression tests with reruns for flaky tests
  python run_tests.py -m regression --reruns 2
        """
    )
    
    # Browser options
    parser.add_argument(
        "--browser", 
        choices=["chrome", "firefox"], 
        default="chrome",
        help="Browser to run tests on (default: chrome)"
    )
    
    parser.add_argument(
        "--headless", 
        action="store_true", 
        default=True,
        help="Run tests in headless mode (default: True)"
    )
    
    parser.add_argument(
        "--no-headless", 
        dest="headless", 
        action="store_false",
        help="Run tests in non-headless mode"
    )
    
    # Environment options
    parser.add_argument(
        "--env", "--environment",
        dest="environment",
        choices=["dev", "staging", "prod"],
        default="dev",
        help="Environment to run tests against (default: dev)"
    )
    
    # Test selection options
    parser.add_argument(
        "test_path",
        nargs="?",
        help="Specific test file or directory to run"
    )
    
    parser.add_argument(
        "-k", "--keyword",
        help="Run tests matching the given substring expression"
    )
    
    parser.add_argument(
        "-m", "--markers",
        help="Run tests matching given mark expression"
    )
    
    # Execution options
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel"
    )
    
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel workers (default: 4)"
    )
    
    # Reporting options
    parser.add_argument(
        "--html-report",
        action="store_true",
        default=True,
        help="Generate HTML report (default: True)"
    )
    
    parser.add_argument(
        "--no-html-report",
        dest="html_report",
        action="store_false",
        help="Disable HTML report generation"
    )
    
    # Output options
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "--capture",
        choices=["yes", "no"],
        default="yes",
        help="Capture stdout/stderr (default: yes)"
    )
    
    # Failure handling
    parser.add_argument(
        "--reruns",
        type=int,
        default=0,
        help="Number of times to rerun failed tests (default: 0)"
    )
    
    parser.add_argument(
        "-x", "--stop-on-first-failure",
        action="store_true",
        help="Stop on first failure"
    )
    
    parser.add_argument(
        "--maxfail",
        dest="max_failures",
        type=int,
        default=0,
        help="Stop after N failures (default: 0 = no limit)"
    )
    
    # Predefined test suites
    parser.add_argument(
        "--smoke",
        action="store_const",
        const="smoke",
        dest="markers",
        help="Run smoke tests"
    )
    
    parser.add_argument(
        "--regression",
        action="store_const",
        const="regression",
        dest="markers",
        help="Run regression tests"
    )
    
    parser.add_argument(
        "--functional",
        action="store_const",
        const="functional",
        dest="markers",
        help="Run functional tests"
    )
    
    parser.add_argument(
        "--ui",
        action="store_const",
        const="ui",
        dest="markers",
        help="Run UI tests"
    )
    
    parser.add_argument(
        "--performance",
        action="store_const",
        const="performance",
        dest="markers",
        help="Run performance tests"
    )
    
    parser.add_argument(
        "--auth",
        action="store_const",
        const="authentication",
        dest="markers",
        help="Run authentication tests"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Setup environment
    print(f"🚀 Test Automation Framework")
    print(f"📅 Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Browser: {args.browser}")
    print(f"👻 Headless: {args.headless}")
    print(f"🌍 Environment: {args.environment}")
    print(f"⚙️ Base URL: {Config.BASE_URLS[args.environment]}")
    
    if args.parallel:
        print(f"🔄 Parallel Execution: {args.workers} workers")
    
    if args.markers:
        print(f"🏷️ Test Markers: {args.markers}")
    
    if args.keyword:
        print(f"🔍 Keyword Filter: {args.keyword}")
    
    if args.test_path:
        print(f"📁 Test Path: {args.test_path}")
    
    print("=" * 60)
    
    # Setup directories
    setup_directories()
    
    # Add project root to Python path
    sys.path.insert(0, '.')
    
    # Convert arguments to pytest format
    pytest_args = get_pytest_args(args)
    
    # Add any additional arguments passed to the script
    pytest_args.extend([arg for arg in sys.argv[1:] if arg.startswith('-') and arg not in [
        '--browser', '--headless', '--no-headless', '--env', '--environment',
        '--parallel', '--workers', '--html-report', '--no-html-report',
        '--smoke', '--regression', '--functional', '--ui', '--performance', '--auth'
    ]])
    
    print(f"🏃 Running pytest with args: {' '.join(pytest_args)}")
    print("=" * 60)
    
    # Run pytest
    exit_code = pytest.main(pytest_args)
    
    print("=" * 60)
    if exit_code == 0:
        print("✅ All tests passed successfully!")
    else:
        print(f"❌ Tests failed with exit code: {exit_code}")
    
    if args.html_report:
        print(f"📊 HTML Report: {Config.HTML_REPORT_FILE}")
    
    print(f"📸 Screenshots: {Config.SCREENSHOT_DIR}")
    print("=" * 60)
    
    return exit_code

if __name__ == '__main__':
    sys.exit(main())
