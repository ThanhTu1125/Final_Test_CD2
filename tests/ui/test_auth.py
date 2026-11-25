import pytest
from typing import Dict
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.smoke
def test_auth_login_with_invalid_credentials_shows_error(page: Page):
    """
    Mục tiêu: Kiểm tra xử lý lỗi khi nhập sai tài khoản đăng nhập (Mục 3.2: Xác thực).
    Tiền điều kiện: Đang ở trang Đăng nhập (/auth/login).
    Quy tắc an toàn: Dùng email ngẫu nhiên không tồn tại, KHÔNG dùng tài khoản mẫu để tránh bị khóa sau 3 lần sai.
    Kết quả mong đợi: Hiển thị thông báo lỗi 'Invalid email or password'.
    """
    login_page = LoginPage(page)
    login_page.open()

    login_page.login(
        email="non_existent_random_user_99999@test.com",
        password="WrongPassword999!"
    )

    expect(login_page.error_message).to_be_visible()
    error_text = login_page.get_error_text()
    assert "Invalid email or password" in error_text, f"Thông báo lỗi không đúng: {error_text}"


@pytest.mark.ui
@pytest.mark.regression
def test_auth_login_with_valid_credentials_redirects_to_account(page: Page, registered_user: Dict[str, str]):
    """
    Mục tiêu: Kiểm tra đăng nhập thành công với tài khoản hợp lệ của nhóm (Mục 3.2: Xác thực).
    Tiền điều kiện: Tài khoản đã được đăng ký thành công qua API fixture.
    Kết quả mong đợi: Chuyển hướng thành công và hiển thị menu người dùng trên thanh điều hướng.
    """
    login_page = LoginPage(page)
    login_page.open()

    login_page.login(
        email=registered_user["email"],
        password=registered_user["password"]
    )

    # Sau khi đăng nhập thành công, menu tài khoản xuất hiện trên header
    expect(login_page.nav_user_menu).to_be_visible()
