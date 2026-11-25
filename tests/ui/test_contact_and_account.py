import os
import pytest
from typing import Dict
from playwright.sync_api import Page, expect
from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.account_page import AccountPage


@pytest.mark.ui
@pytest.mark.smoke
def test_contact_form_with_empty_attachment_submits_successfully(page: Page):
    """
    Mục tiêu: Kiểm tra gửi form liên hệ kèm tệp rỗng 0 byte (Mục 3.2: Bắt buộc >= 1 testcase tải tệp lên form Contact).
    Tiền điều kiện: Đang ở trang Liên hệ (/contact), có sẵn file rỗng 0 byte tại data/empty_file_0byte.txt.
    Kết quả mong đợi: Hệ thống chấp nhận tệp 0 byte và hiển thị thông báo gửi thành công.
    """
    contact_page = ContactPage(page)
    contact_page.open()

    # Chuẩn bị đường dẫn tuyệt đối tới tệp rỗng 0 byte
    file_path = os.path.abspath("data/empty_file_0byte.txt")
    assert os.path.exists(file_path), "File rỗng 0 byte không tồn tại"
    assert os.path.getsize(file_path) == 0, "File đính kèm phải có dung lượng đúng 0 byte theo quy định Toolshop"

    contact_page.fill_contact_form(
        first_name="Nguyen",
        last_name="An",
        email="nguyenan@example.com",
        subject="Customer service",
        message="Toi can ho tro ve tai khoan cua minh, vui long lien he lai som nhat co the de giai quyet giup toi."
    )
    contact_page.upload_file(file_path)
    contact_page.submit()

    # Chờ thông báo thành công
    expect(contact_page.success_alert).to_be_visible()
    alert_text = contact_page.success_alert.inner_text()
    assert "Thanks for your message" in alert_text, f"Thông báo gửi liên hệ không đúng: {alert_text}"


@pytest.mark.ui
@pytest.mark.regression
def test_footer_github_link_opens_in_new_tab(page: Page):
    """
    Mục tiêu: Kiểm tra liên kết mở tab mới (Mục 3.2: Bắt buộc >= 1 testcase tab mới link GitHub ở chân trang).
    Tiền điều kiện: Đang ở trang chủ Toolshop.
    Kết quả mong đợi: Click vào link GitHub ở footer mở ra một tab/page mới trỏ tới github.com.
    """
    home_page = HomePage(page)
    home_page.open()

    expect(home_page.footer).to_be_visible()
    expect(home_page.footer_github_link).to_be_visible()

    # Bắt sự kiện mở tab mới khi click link
    with page.context.expect_page() as new_page_info:
        home_page.footer_github_link.click()

    new_tab = new_page_info.value
    new_tab.wait_for_load_state("domcontentloaded")
    new_url = new_tab.url

    assert "github.com" in new_url, f"Tab mới mở không dẫn tới GitHub: {new_url}"
    new_tab.close()


@pytest.mark.ui
@pytest.mark.regression
def test_account_profile_view_displays_registered_information(
    authenticated_page: Page,
    registered_user: Dict[str, str]
):
    """
    Mục tiêu: Kiểm tra xem trang cá nhân hiển thị thông tin tài khoản (Mục 3.2: Tài khoản).
    Tiền điều kiện: Đã đăng nhập thông qua authenticated_page fixture (sử dụng storage_state).
    Kết quả mong đợi: Trang Profile hiển thị đúng tên hoặc email của tài khoản đăng nhập.
    """
    account_page = AccountPage(authenticated_page)
    account_page.open()

    expect(account_page.nav_profile).to_be_visible()
    account_page.go_to_profile()

    # Kiểm tra trường first name hoặc email hiển thị đúng thông tin của tài khoản
    expect(account_page.first_name_input).to_have_value(registered_user["first_name"])
