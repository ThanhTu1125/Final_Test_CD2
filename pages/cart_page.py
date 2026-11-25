from typing import List, Dict
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class CartPage(BasePage):
    """
    Page Object cho Trang Giỏ hàng (/checkout).
    """

    def __init__(self, page: Page, base_url: str = None, route_prefix: str = None):
        super().__init__(page, base_url, route_prefix)

        # --- Locators bảng giỏ hàng ---
        self.cart_table = self.page.locator("table")
        self.cart_rows = self.page.locator("tbody tr")
        self.item_titles = self.page.get_by_test_id("product-title")
        self.item_quantities = self.page.get_by_test_id("product-quantity")
        self.item_prices = self.page.get_by_test_id("product-price")
        self.item_line_prices = self.page.get_by_test_id("line-price")
        self.cart_total_price = self.page.get_by_test_id("cart-total")
        self.btn_proceed_to_checkout = self.page.get_by_test_id("proceed-1")
        self.delete_buttons = self.page.locator("a.btn-danger, button.btn-danger")

    def open(self) -> None:
        """Mở trang giỏ hàng."""
        self.navigate("/checkout")

    def get_cart_items_count(self) -> int:
        """Đếm số dòng sản phẩm trong giỏ hàng."""
        return self.cart_rows.count()

    def get_item_titles(self) -> List[str]:
        """Lấy danh sách tên các sản phẩm trong giỏ."""
        return self.item_titles.all_text_contents()

    def get_total_price_number(self) -> float:
        """Lấy tổng tiền giỏ hàng dạng số."""
        text = self.cart_total_price.inner_text()
        return float(text.replace("$", "").strip())

    def update_quantity(self, row_index: int, quantity: int) -> None:
        """Cập nhật số lượng của dòng sản phẩm thứ row_index."""
        input_elem = self.item_quantities.nth(row_index)
        input_elem.fill(str(quantity))
        # Nhấn Enter để lưu số lượng
        input_elem.press("Enter")

    def remove_item(self, row_index: int) -> None:
        """Xóa sản phẩm tại dòng row_index."""
        self.delete_buttons.nth(row_index).click()

    def proceed_to_checkout(self) -> None:
        """Bấm nút chuyển sang bước thanh toán (Proceed to checkout)."""
        self.btn_proceed_to_checkout.click()
