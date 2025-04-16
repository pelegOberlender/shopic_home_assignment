import logging
import pytest
from playwright.sync_api import sync_playwright
from tests.pages.main_page import WebUser

_logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    """
        Adds CLI flag '--headless' to control browser mode.
        Default: headed mode.
    """
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode (default: headed)."
    )

@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """
        Sets global logging level and format for the test session.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s"
    )

@pytest.fixture(scope="function")
def web_user(web_context, web_url):
    """
        Initializes WebUser and navigates to base URL.
        Returned before each test.
    """
    user = WebUser(web_context)
    return user.navigate(web_url)

@pytest.fixture(scope="session")
def web_url():
    """
        Returns base URL of the tested web app.
    """
    return "http://localhost:8000"

@pytest.fixture(scope="session")
def web_context(request):
    """
        Launches browser context (headless or headed).
        Enables tracing. Yields Playwright page object.
        Ensures full cleanup on exit.
    """
    _logger.info("Launching browser session")

    is_headless = request.config.getoption("--headless")
    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(headless=is_headless, slow_mo=500)
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()

    _logger.info(f" Browser launched in {'headless' if is_headless else 'headed'} mode")

    yield page

    _logger.info("🧹 Closing browser and saving trace")
    context.tracing.stop(path="trace.zip")
    context.close()
    browser.close()
    playwright.stop()
