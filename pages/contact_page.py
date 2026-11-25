from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class ContactPage(BasePage):
    """
    Page Object cho Trang Liên hệ (/contact).
    Đặc thù Mục 3.2: Có testcase kiểm tra tải tệp lên (Toolshop chỉ nhận tệp rỗng 0 byte).
    """

    def __init__(self, page: Page, base_url: str = None, route_prefix: str = None):
        super().__init__(page, base_url, route_prefix)

        # --- Locators Form liên hệ ---
        self.first_name_input = self.page.get_by_test_id("first-name")
        self.last_name_input = self.page.get_by_test_id("last-name")
        self.email_input = self.page.get_by_test_id("email")
        self.subject_select = self.page.get_by_test_id("subject")
        self.message_textarea = self.page.get_by_test_id("message")
        self.attachment_input = self.page.get_by_test_id("attachment")
        self.submit_button = self.page.get_by_test_id("contact-submit")
        self.success_alert = self.page.locator(".alert-success, div[role='alert']")
        self.error_alert = self.page.locator(".alert-danger, .invalid-feedback")

    def open(self) -> None:
        """Mở trang liên hệ."""
        self.navigate("/contact")

    def fill_contact_form(self, first_name: str, last_name: str, email: str, subject: str, message: str) -> None:
        """Điền thông tin form liên hệ."""
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        self.subject_select.select_option(subject)
        self.message_textarea.fill(message)

    def upload_file(self, file_path: str) -> None:
        """Tải tệp đính kèm lên (Mục 3.2: Toolshop chỉ nhận tệp rỗng 0 byte)."""
        self.attachment_input.set_input_files(file_path)

    def submit(self) -> None:
        """Bấm nút gửi form liên hệ."""
        self.submit_button.click()
