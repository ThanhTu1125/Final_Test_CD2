import os
from playwright.sync_api import Page, Locator


class BasePage:
    """
    Lớp cơ sở (BasePage) cho tất cả các trang theo mô hình Page Object Model (POM).
    Yêu cầu:
    - Locator là thuộc tính lớp.
    - Không đặt assertion (expect) trong Page Object.
    - Ưu tiên thứ tự: get_by_test_id -> get_by_role -> get_by_label/placeholder -> CSS.
    - Hỗ trợ ROUTE_PREFIX (ví dụ /#/ trên BUGGY).
    """

    def __init__(self, page: Page, base_url: str = None, route_prefix: str = None):
        self.page = page
        self.base_url = base_url or os.getenv("BASE_URL", "https://practicesoftwaretesting.com")
        self.route_prefix = route_prefix if route_prefix is not None else os.getenv("ROUTE_PREFIX", "")

        # --- Locators chung trên Header (Navigation Bar) ---
        self.nav_home = self.page.get_by_test_id("nav-home")
        self.nav_categories = self.page.get_by_test_id("nav-categories")
        self.nav_contact = self.page.get_by_test_id("nav-contact")
        self.nav_sign_in = self.page.get_by_test_id("nav-sign-in")
        self.nav_user_menu = self.page.get_by_test_id("nav-menu")
        self.nav_cart = self.page.get_by_test_id("nav-cart")
        self.cart_quantity_badge = self.page.get_by_test_id("cart-quantity")

        # --- Locators chung trên Footer ---
        self.footer = self.page.locator("footer")
        # Link GitHub ở footer (yêu cầu tab mới theo Mục 3.2)
        self.footer_github_link = self.page.locator("footer a[href*='github.com']")

    def navigate(self, path: str = "") -> None:
        """
        Điều hướng đến URL dựa trên path, tự động ghép tiền tố ROUTE_PREFIX.
        Ví dụ:
        - PROD: path='/auth/login' -> 'https://practicesoftwaretesting.com/auth/login'
        - BUGGY: path='/auth/login' -> 'https://with-bugs.practicesoftwaretesting.com/#/auth/login'
        """
        clean_path = path if path.startswith("/") else f"/{path}"
        full_url = f"{self.base_url.rstrip('/')}{self.route_prefix}{clean_path}"
        self.page.goto(full_url, wait_until="domcontentloaded")

    def get_current_url(self) -> str:
        """Trả về URL hiện tại của trang."""
        return self.page.url

    def get_page_title(self) -> str:
        """Trả về tiêu đề của trang."""
        return self.page.title()

    def go_to_cart(self) -> None:
        """Chuyển đến giỏ hàng thông qua nút Cart trên header."""
        self.nav_cart.click()

    def go_to_sign_in(self) -> None:
        """Chuyển đến trang Đăng nhập thông qua header."""
        self.nav_sign_in.click()

    def go_to_contact(self) -> None:
        """Chuyển đến trang Liên hệ thông qua header."""
        self.nav_contact.click()
