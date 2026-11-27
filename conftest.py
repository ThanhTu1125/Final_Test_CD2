import os
import json
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
    - Độ dài >= 16 ký tự
    - Tránh các mật khẩu lộ dữ liệu như welcome01, Welcome01!
    """
    token = secrets.token_hex(5)
    return f"A!9z#{token}T$8mQ"


def generate_random_user() -> Dict[str, Any]:
    """Sinh dữ liệu người dùng ngẫu nhiên để đăng ký tài khoản."""
    unique_id = uuid.uuid4().hex[:8]
    unique_letters = "".join(secrets.choice(string.ascii_lowercase) for _ in range(6))
    return {
        "first_name": "AutoTester",
        "last_name": f"Tester{unique_letters}",
        "dob": "1995-05-20",
        "address": "456 Automation Road",
        "city": "Da Nang",
        "state": "Da Nang",
        "country": "US",
        "postcode": "55000",
        "phone": f"09{secrets.randbelow(89999999) + 10000000}",
        "email": f"group_test_{unique_id}@testmail.com",
        "password": generate_strong_password(),
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Lưu kết quả thực thi của từng pha (setup/call/teardown) vào node để chụp ảnh và lưu trace khi lỗi."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def _finalize_context_with_artifacts(ctx: BrowserContext, request: pytest.FixtureRequest) -> None:
    """Chụp ảnh màn hình và xuất file trace.zip vào test-results/ nếu test case bị lỗi (Mục 3.10 & 3.13)."""
    rep_call = getattr(request.node, "rep_call", None)
    rep_setup = getattr(request.node, "rep_setup", None)
    failed = (rep_call and rep_call.failed) or (rep_setup and rep_setup.failed)

    if failed:
        safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "-" for c in request.node.nodeid).strip("-")
        artifact_dir = os.path.join("test-results", safe_name)
        os.makedirs(artifact_dir, exist_ok=True)
        try:
            if ctx.pages:
                ctx.pages[-1].screenshot(
                    path=os.path.join(artifact_dir, "test-failed-1.png"),
                    full_page=True
                )
        except Exception:
            pass
        try:
            ctx.tracing.stop(path=os.path.join(artifact_dir, "trace.zip"))
        except Exception:
            pass
    else:
        try:
            ctx.tracing.stop()
        except Exception:
            pass
    ctx.close()


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
def registered_user(api_request_context: APIRequestContext, api_url: str) -> Dict[str, Any]:
    """
    Đăng ký một tài khoản riêng của nhóm qua API đăng ký (Mục 2).
    Xử lý tương thích môi trường (Mục 1 & 2):
    - PROD: address là object {'street', 'city', 'state', 'country', 'postal_code'}.
    - BUGGY: address là chuỗi, city, state, country, postcode tách riêng.
    Scope: session.
    """
    user_data = generate_random_user()
    is_buggy = "with-bugs" in api_url or os.getenv("ROUTE_PREFIX", "") != ""

    if is_buggy:
        payload = {
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
    else:
        payload = {
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "dob": user_data["dob"],
            "address": {
                "street": user_data["address"],
                "city": user_data["city"],
                "state": user_data["state"],
                "country": user_data["country"],
                "postal_code": user_data["postcode"],
            },
            "phone": user_data["phone"],
            "email": user_data["email"],
            "password": user_data["password"],
        }

    response = api_request_context.post("/users/register", data=payload)
    if response.status in [200, 201]:
        resp_data = response.json()
        user_data["id"] = resp_data.get("id")
        return user_data
    else:
        print(f"[Warning] Register API failed with status {response.status}: {response.text()}")

    return user_data


@pytest.fixture(scope="session")
def storage_state_file(browser: Browser, base_url: str, route_prefix: str, registered_user: Dict[str, str]) -> str:
    """
    Yêu cầu 3.4: Đăng nhập 1 lần, lưu storage_state (scope session) và tái sử dụng cho các test.
    """
    context = browser.new_context()
    # Đóng ngay kết nối SSE /sales-stream để không làm treo wait_for_load_state("networkidle")
    context.route("**/sales-stream**", lambda route: route.fulfill(status=204, body=""))
    page = context.new_page()
    login_url = f"{base_url.rstrip('/')}{route_prefix}/auth/login"

    try:
        page.goto(login_url, wait_until="domcontentloaded", timeout=20000)
        # Điền email & password của tài khoản nhóm
        page.get_by_test_id("email").fill(registered_user["email"])
        page.get_by_test_id("password").fill(registered_user["password"])
        page.get_by_test_id("login-submit").click()
        page.get_by_test_id("nav-profile").or_(page.get_by_test_id("page-title")).or_(
            page.get_by_test_id("nav-menu")
        ).first.wait_for(state="visible", timeout=15000)
        # Đồng bộ sessionStorage sang localStorage để storage_state.json lưu được token trên cả PROD và BUGGY
        page.evaluate(
            """() => {
                for (let i = 0; i < window.sessionStorage.length; i++) {
                    const key = window.sessionStorage.key(i);
                    const val = window.sessionStorage.getItem(key);
                    if (key && val && !window.localStorage.getItem(key)) {
                        window.localStorage.setItem(key, val);
                    }
                }
            }"""
        )
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
def context(browser: Browser, request: pytest.FixtureRequest) -> Generator[BrowserContext, None, None]:
    """
    Fixture tạo mới một BrowserContext sạch cho mỗi test case (Mục 3.4).
    Tích hợp lưu trace và chụp ảnh màn hình khi test thất bại (Mục 3.10).
    Scope: function.
    """
    new_context = browser.new_context()
    # Đóng ngay kết nối SSE /sales-stream để không làm treo wait_for_load_state("networkidle")
    new_context.route("**/sales-stream**", lambda route: route.fulfill(status=204, body=""))
    new_context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield new_context
    _finalize_context_with_artifacts(new_context, request)


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Fixture cung cấp một Page mới sạch cho mỗi test case.
    Scope: function.
    """
    new_page = context.new_page()
    yield new_page


@pytest.fixture(scope="function")
def authenticated_context(
    browser: Browser,
    storage_state_file: str,
    request: pytest.FixtureRequest
) -> Generator[BrowserContext, None, None]:
    """
    Yêu cầu 3.4: Mỗi test cần đăng nhập tạo context mới từ file storage_state đã lưu.
    Tích hợp lưu trace và chụp ảnh màn hình khi test thất bại (Mục 3.10).
    Scope: function.
    """
    if os.path.exists(storage_state_file):
        auth_ctx = browser.new_context(storage_state=storage_state_file)
        # Khôi phục trực tiếp token từ storage_state.json sang sessionStorage cho môi trường BUGGY
        try:
            with open(storage_state_file, "r", encoding="utf-8") as f:
                state_data = json.load(f)
            for origin in state_data.get("origins", []):
                for item in origin.get("localStorage", []):
                    k, v = item.get("name"), item.get("value")
                    if k and v:
                        auth_ctx.add_init_script(
                            f"window.sessionStorage.setItem({json.dumps(k)}, {json.dumps(v)}); "
                            f"window.localStorage.setItem({json.dumps(k)}, {json.dumps(v)});"
                        )
        except Exception:
            pass
    else:
        auth_ctx = browser.new_context()
    auth_ctx.route("**/sales-stream**", lambda route: route.fulfill(status=204, body=""))
    auth_ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield auth_ctx
    _finalize_context_with_artifacts(auth_ctx, request)


@pytest.fixture(scope="function")
def authenticated_page(authenticated_context: BrowserContext) -> Generator[Page, None, None]:
    """
    Fixture Page đã có sẵn trạng thái phiên đăng nhập.
    Scope: function.
    """
    auth_page = authenticated_context.new_page()
    yield auth_page
