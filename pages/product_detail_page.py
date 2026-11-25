from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    """
    Page Object cho Trang Chi tiết sản phẩm.
    """

    def __init__(self, page: Page, base_url: str = None, route_prefix: str = None):
        super().__init__(page, base_url, route_prefix)

        # --- Locators thông tin sản phẩm ---
        self.product_title = self.page.get_by_test_id("product-name")
        self.unit_price = self.page.get_by_test_id("unit-price")
        self.product_description = self.page.get_by_test_id("product-description")

        # --- Locators tương tác ---
        self.quantity_input = self.page.get_by_test_id("quantity")
        self.btn_increase_quantity = self.page.get_by_test_id("btn-increase-quantity")
        self.btn_decrease_quantity = self.page.get_by_test_id("btn-decrease-quantity")
        self.btn_add_to_cart = self.page.get_by_test_id("btn-add-to-cart")
        self.btn_add_to_favorites = self.page.get_by_test_id("btn-add-to-favorites")

        # Thông báo Toast / Alert sau khi thao tác
        self.toast_alert = self.page.locator("div[role='alert'], .toast-message, .alert")

    def open(self, product_id: str) -> None:
        """Mở trực tiếp trang sản phẩm theo ID."""
        self.navigate(f"/product/{product_id}")

    def set_quantity(self, quantity: int) -> None:
        """Nhập trực tiếp số lượng mong muốn."""
        self.quantity_input.fill(str(quantity))

    def increase_quantity(self, times: int = 1) -> None:
        """Bấm nút tăng số lượng (+) theo số lần."""
        for _ in range(times):
            self.btn_increase_quantity.click()

    def decrease_quantity(self, times: int = 1) -> None:
        """Bấm nút giảm số lượng (-) theo số lần."""
        for _ in range(times):
            self.btn_decrease_quantity.click()

    def add_to_cart(self) -> None:
        """Click nút Thêm vào giỏ hàng."""
        self.btn_add_to_cart.click()

    def add_to_favorites(self) -> None:
        """Click nút Thêm vào danh sách yêu thích."""
        self.btn_add_to_favorites.click()

    def get_unit_price_number(self) -> float:
        """Lấy giá trị số của đơn giá."""
        text = self.unit_price.inner_text()
        return float(text.replace("$", "").strip())
