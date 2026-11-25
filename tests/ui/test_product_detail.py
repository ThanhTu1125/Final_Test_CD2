import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage


@pytest.mark.ui
@pytest.mark.smoke
def test_product_detail_view_information_displays_correctly(page: Page):
    """
    Mục tiêu: Kiểm tra xem chi tiết sản phẩm hiển thị đầy đủ thông tin (Mục 3.2: Chi tiết sản phẩm).
    Tiền điều kiện: Đang ở trang chủ Toolshop.
    Kết quả mong đợi:
    - Chuyển hướng đến trang chi tiết sản phẩm.
    - Hiển thị tên sản phẩm, đơn giá, mô tả, nút thêm vào giỏ hàng.
    """
    home_page = HomePage(page)
    home_page.open()
    expect(home_page.product_cards.first).to_be_visible()

    # Click vào sản phẩm đầu tiên
    home_page.click_first_product()

    detail_page = ProductDetailPage(page)
    expect(detail_page.product_title).to_be_visible()
    expect(detail_page.unit_price).to_be_visible()
    expect(detail_page.btn_add_to_cart).to_be_visible()

    # Xác thực giá trị hợp lệ
    price = detail_page.get_unit_price_number()
    assert price > 0, f"Đơn giá sản phẩm phải lớn hơn 0, nhận được: {price}"


@pytest.mark.ui
@pytest.mark.regression
def test_product_detail_increase_quantity_updates_input_value(page: Page):
    """
    Mục tiêu: Kiểm tra nút bấm tăng số lượng sản phẩm (Mục 3.2: Chi tiết sản phẩm).
    Tiền điều kiện: Đang ở trang chi tiết sản phẩm.
    Kết quả mong đợi: Khi bấm nút tăng 2 lần, trường số lượng hiển thị giá trị là 3 (mặc định là 1).
    """
    home_page = HomePage(page)
    home_page.open()
    expect(home_page.product_cards.first).to_be_visible()
    home_page.click_first_product()

    detail_page = ProductDetailPage(page)
    expect(detail_page.quantity_input).to_be_visible()
    expect(detail_page.quantity_input).to_have_value("1")

    # Bấm tăng số lượng 2 lần
    detail_page.increase_quantity(times=2)
    expect(detail_page.quantity_input).to_have_value("3")
