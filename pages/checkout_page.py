from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """
    Page Object cho Luồng Thanh toán từng bước (Checkout steps).
    Step 1: Xem giỏ hàng (proceed-1)
    Step 2: Đăng nhập nếu chưa đăng nhập (proceed-2)
    Step 3: Địa chỉ thanh toán & hóa đơn (proceed-3)
    Step 4: Phương thức thanh toán & Hoàn tất (finish)
    """

    def __init__(self, page: Page, base_url: str = None, route_prefix: str = None):
        super().__init__(page, base_url, route_prefix)

        # Nút chuyển bước
        self.btn_proceed_step_1 = self.page.get_by_test_id("proceed-1")
        self.btn_proceed_step_2 = self.page.get_by_test_id("proceed-2")
        self.btn_proceed_step_3 = self.page.get_by_test_id("proceed-3")
        self.btn_finish_order = self.page.get_by_test_id("finish")

        # Step 3: Địa chỉ
        self.input_state = self.page.get_by_test_id("state")
        self.input_postal_code = self.page.get_by_test_id("postal_code")

        # Step 4: Phương thức thanh toán
        self.select_payment_method = self.page.get_by_test_id("payment-method")
        self.input_account_name = self.page.get_by_test_id("account-name")
        self.input_account_number = self.page.get_by_test_id("account-number")

        # Thông báo xác nhận đơn hàng thành công
        self.order_confirmation_message = self.page.locator(".help-block, .alert-success, #order-confirmation")

    def proceed_to_login_or_billing(self) -> None:
        """Chuyển từ bước 1 sang bước 2."""
        self.btn_proceed_step_1.click()

    def proceed_to_address(self) -> None:
        """Chuyển sang bước 3 (Địa chỉ)."""
        self.btn_proceed_step_2.click()

    def proceed_to_payment(self) -> None:
        """Chuyển sang bước 4 (Thanh toán)."""
        self.btn_proceed_step_3.click()

    def fill_payment_info(self, method: str = "Bank Transfer", account_name: str = "Test Account", account_number: str = "123456789") -> None:
        """Điền thông tin thanh toán."""
        self.select_payment_method.select_option(label=method)
        if self.input_account_name.is_visible():
            self.input_account_name.fill(account_name)
        if self.input_account_number.is_visible():
            self.input_account_number.fill(account_number)

    def confirm_and_finish_order(self) -> None:
        """Bấm nút xác nhận thanh toán cuối cùng."""
        self.btn_finish_order.click()
