from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class AccountPage(BasePage):
    """
    Page Object cho Trang Tài khoản người dùng (/account).
    """

    def __init__(self, page: Page, base_url: str = None, route_prefix: str = None):
        super().__init__(page, base_url, route_prefix)

        # --- Locators các mục trong tài khoản ---
        self.nav_profile = self.page.get_by_test_id("nav-profile")
        self.nav_favorites = self.page.get_by_test_id("nav-favorites")
        self.nav_invoices = self.page.get_by_test_id("nav-invoices")
        self.page_title = self.page.get_by_test_id("page-title")

        # Profile fields
        self.first_name_input = self.page.get_by_test_id("first-name")
        self.last_name_input = self.page.get_by_test_id("last-name")
        self.email_input = self.page.get_by_test_id("email")
        self.btn_update_profile = self.page.get_by_test_id("btn-update-profile")

    def open(self) -> None:
        """Mở trang tài khoản."""
        self.navigate("/account")

    def go_to_profile(self) -> None:
        """Mở mục thông tin cá nhân."""
        self.nav_profile.click()

    def go_to_favorites(self) -> None:
        """Mở mục danh sách yêu thích."""
        self.nav_favorites.click()

    def go_to_invoices(self) -> None:
        """Mở mục danh sách hóa đơn/đơn hàng."""
        self.nav_invoices.click()
