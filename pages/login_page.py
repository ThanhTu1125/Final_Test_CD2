from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object cho Trang Đăng nhập (/auth/login).
    """

    def __init__(self, page: Page, base_url: str = None, route_prefix: str = None):
        super().__init__(page, base_url, route_prefix)

        # --- Locators Form đăng nhập ---
        self.email_input = self.page.get_by_test_id("email")
        self.password_input = self.page.get_by_test_id("password")
        self.login_button = self.page.get_by_test_id("login-submit")
        self.error_message = self.page.get_by_test_id("login-error")
        self.register_link = self.page.get_by_test_id("register-link")

    def open(self) -> None:
        """Mở trang đăng nhập."""
        self.navigate("/auth/login")

    def login(self, email: str, password: str) -> None:
        """Nhập thông tin và click đăng nhập."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_text(self) -> str:
        """Lấy thông báo lỗi khi đăng nhập sai."""
        return self.error_message.inner_text()

    def click_register(self) -> None:
        """Bấm link chuyển sang trang Đăng ký."""
        self.register_link.click()
