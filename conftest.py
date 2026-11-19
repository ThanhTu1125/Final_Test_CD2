import os
import pytest
from typing import Generator
from playwright.sync_api import Playwright, Browser, BrowserContext, Page, APIRequestContext
from dotenv import load_dotenv

# Nạp các biến môi trường từ file .env (BASE_URL, API_URL, ROUTE_PREFIX)
load_dotenv()

STORAGE_STATE_PATH = "storage_state.json"


@pytest.fixture(scope="session", autouse=True)
def configure_playwright_test_id(playwright: Playwright):
    """
    Yêu cầu 3.1: Đặt data-test làm thuộc tính test id mặc định cho Playwright.
    Scope: session, autouse=True.
    """
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def base_url() -> str:
    """Lấy BASE_URL từ biến môi trường, tuyệt đối không hard-code."""
    return os.getenv("BASE_URL", "https://practicesoftwaretesting.com")


@pytest.fixture(scope="session")
def api_url() -> str:
    """Lấy API_URL từ biến môi trường, tuyệt đối không hard-code."""
    return os.getenv("API_URL", "https://api.practicesoftwaretesting.com")


@pytest.fixture(scope="session")
def route_prefix() -> str:
    """Lấy ROUTE_PREFIX từ biến môi trường (Ví dụ: '/#' trên môi trường BUGGY)."""
    return os.getenv("ROUTE_PREFIX", "")


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright, api_url: str) -> Generator[APIRequestContext, None, None]:
    """
    Fixture khởi tạo APIRequestContext cho các test case API (Mục 3.5).
    Scope: session.
    """
    request_context = playwright.request.new_context(
        base_url=api_url,
        extra_http_headers={"Accept": "application/json"}
    )
    yield request_context
    request_context.dispose()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Fixture tạo mới một BrowserContext cho mỗi test case (Mục 3.4).
    Scope: function (đảm bảo tính độc lập giữa các test).
    """
    new_context = browser.new_context()
    yield new_context
    new_context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Fixture cung cấp một Page (tab trình duyệt) mới cho mỗi test case UI.
    Scope: function.
    """
    new_page = context.new_page()
    yield new_page
    new_page.close()
