from typing import Dict
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class RegisterPage(BasePage):
    """
    Page Object cho Trang Đăng ký tài khoản (/auth/register).
    """

    def __init__(self, page: Page, base_url: str = None, route_prefix: str = None):
        super().__init__(page, base_url, route_prefix)

        # --- Locators Form đăng ký ---
        self.first_name_input = self.page.get_by_test_id("first-name")
        self.last_name_input = self.page.get_by_test_id("last-name")
        self.dob_input = self.page.get_by_test_id("dob")
        self.address_input = self.page.get_by_test_id("address")
        self.postcode_input = self.page.get_by_test_id("postcode")
        self.city_input = self.page.get_by_test_id("city")
        self.state_input = self.page.get_by_test_id("state")
        self.country_select = self.page.get_by_test_id("country")
        self.phone_input = self.page.get_by_test_id("phone")
        self.email_input = self.page.get_by_test_id("email")
        self.password_input = self.page.get_by_test_id("password")
        self.register_button = self.page.get_by_test_id("register-submit")
        self.success_alert = self.page.locator(".alert-success, div[role='alert']")

    def open(self) -> None:
        """Mở trang đăng ký."""
        self.navigate("/auth/register")

    def fill_registration_form(self, user_info: Dict[str, str]) -> None:
        """Điền đầy đủ thông tin vào form đăng ký."""
        self.first_name_input.fill(user_info.get("first_name", "Test"))
        self.last_name_input.fill(user_info.get("last_name", "User"))
        self.dob_input.fill(user_info.get("dob", "1990-01-01"))
        self.address_input.fill(user_info.get("address", "123 Main St"))
        self.postcode_input.fill(user_info.get("postcode", "10000"))
        self.city_input.fill(user_info.get("city", "City"))
        self.state_input.fill(user_info.get("state", "State"))
        if "country" in user_info:
            self.country_select.select_option(user_info["country"])
        self.phone_input.fill(user_info.get("phone", "0123456789"))
        self.email_input.fill(user_info["email"])
        self.password_input.fill(user_info["password"])

    def submit(self) -> None:
        """Bấm nút Đăng ký."""
        self.register_button.click()
