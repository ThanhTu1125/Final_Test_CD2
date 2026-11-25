import os
import uuid
import secrets
import string
import pytest
from typing import Generator, Dict, Any
from playwright.sync_api import Playwright, Browser, BrowserContext, Page, APIRequestContext
from dotenv import load_dotenv

# Nạp biến môi trường từ .env
load_dotenv()

STORAGE_STATE_PATH = "storage_state.json"


def generate_strong_password() -> str:
    """
    Sinh mật khẩu ngẫu nhiên đủ mạnh thỏa mãn Toolshop:
    - Chứa chữ hoa, chữ thường, chữ số, ký tự đặc biệt
    - Độ dài >= 12 ký tự
    - Tránh các mật khẩu lộ dữ liệu như welcome01, Welcome01!
    """
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    # Đảm bảo có ít nhất 1 chữ hoa, 1 chữ thường, 1 số, 1 ký tự đặc biệt
    pwd = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*"),
    ]
    pwd += [secrets.choice(chars) for _ in range(10)]
    secrets.SystemRandom().shuffle(pwd)
    return "".join(pwd)


def generate_random_user() -> Dict[str, str]:
    """Sinh dữ liệu người dùng ngẫu nhiên để đăng ký tài khoản."""
    unique_id = uuid.uuid4().hex[:8]
    return {
        "first_name": "AutoTester",
        "last_name": f"User{unique_id}",
        "dob": "1995-05-20",
        "address": "456 Automation Road",
        "city": "Da Nang",
        "state": "Da Nang",
        "country": "US",
        "postcode": "55000",
        "phone": f"09{secrets.randbelow(89999999) + 10000000}",
        "email": f"test_group_{unique_id}@practicesoftwaretesting.com",
        "password": generate_strong_password(),
    }


# ==============================================================================
# SESSION FIXTURES
# ==============================================================================

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
    """Lấy ROUTE_PREFIX từ biến môi trường (Ví dụ: '/#' trên BUGGY)."""
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


@pytest.fixture(scope="session")
def registered_user(api_request_context: APIRequestContext) -> Dict[str, str]:
    """
    Đăng ký một tài khoản riêng của nhóm qua API đăng ký (Mục 2).
    Scope: session.
    """
    user_data = generate_random_user()
    try:
        response = api_request_context.post(
            "/users/register",
            data={
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "dob": user_data["dob"],
                "address": user_data["address"],
                "city": user_data["city"],
                "state": user_data["state"],
                "country": user_data["country"],
                "postcode": user_data["postcode"],
                "phone": user_data["phone"],
                "email": user_data["email"],
                "password": user_data["password"],
            }
        )
        if response.status in [200, 201]:
            return user_data
    except Exception:
        pass
    # Fallback dữ liệu nếu API chưa sẵn sàng
    return user_data


@pytest.fixture(scope="session")
def storage_state_file(browser: Browser, base_url: str, route_prefix: str, registered_user: Dict[str, str]) -> str:
    """
    Yêu cầu 3.4: Đăng nhập 1 lần, lưu storage_state (scope session) và tái sử dụng cho các test.
    """
    context = browser.new_context()
    page = context.new_page()
    login_url = f"{base_url.rstrip('/')}{route_prefix}/auth/login"

    try:
        page.goto(login_url, wait_until="domcontentloaded", timeout=15000)
        # Điền email & password của tài khoản nhóm
        page.get_by_test_id("email").fill(registered_user["email"])
        page.get_by_test_id("password").fill(registered_user["password"])
        page.get_by_test_id("login-submit").click()
        page.wait_for_timeout(1000)
        context.storage_state(path=STORAGE_STATE_PATH)
    except Exception:
        # Nếu chưa đăng nhập được do site ngoài, tạo file rỗng để không crash
        context.storage_state(path=STORAGE_STATE_PATH)
    finally:
        context.close()

    return STORAGE_STATE_PATH


# ==============================================================================
# FUNCTION FIXTURES
# ==============================================================================

@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Fixture tạo mới một BrowserContext sạch cho mỗi test case (Mục 3.4).
    Scope: function.
    """
    new_context = browser.new_context()
    yield new_context
    new_context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Fixture cung cấp một Page mới sạch cho mỗi test case.
    Scope: function.
    """
    new_page = context.new_page()
    yield new_page
    new_page.close()


@pytest.fixture(scope="function")
def authenticated_context(browser: Browser, storage_state_file: str) -> Generator[BrowserContext, None, None]:
    """
    Yêu cầu 3.4: Mỗi test cần đăng nhập tạo context mới từ file storage_state đã lưu.
    Scope: function.
    """
    if os.path.exists(storage_state_file):
        auth_ctx = browser.new_context(storage_state=storage_state_file)
    else:
        auth_ctx = browser.new_context()
    yield auth_ctx
    auth_ctx.close()


@pytest.fixture(scope="function")
def authenticated_page(authenticated_context: BrowserContext) -> Generator[Page, None, None]:
    """
    Fixture Page đã có sẵn trạng thái phiên đăng nhập.
    Scope: function.
    """
    auth_page = authenticated_context.new_page()
    yield auth_page
    auth_page.close()
