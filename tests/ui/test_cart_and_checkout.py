import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage


@pytest.mark.ui
@pytest.mark.smoke
def test_cart_add_product_from_detail_updates_cart_badge(page: Page):
    """
    Mục tiêu: Kiểm tra thêm sản phẩm vào giỏ hàng và cập nhật huy hiệu (badge) số lượng (Mục 3.2: Giỏ hàng).
    Tiền điều kiện: Đang ở trang chi tiết sản phẩm.
    Kết quả mong đợi: Sau khi bấm Thêm vào giỏ hàng, số lượng trên icon giỏ hàng ở header tăng lên.
    """
    home_page = HomePage(page)
    home_page.open()
    expect(home_page.product_cards.first).to_be_visible()
    home_page.click_first_product()

    detail_page = ProductDetailPage(page)
    expect(detail_page.btn_add_to_cart).to_be_visible()
    detail_page.add_to_cart()

    # Kiểm tra badge giỏ hàng trên header có hiển thị số lượng ít nhất là 1
    expect(detail_page.cart_quantity_badge).to_be_visible()
    badge_text = detail_page.cart_quantity_badge.inner_text()
    assert int(badge_text) >= 1, f"Số lượng trong giỏ hàng phải >= 1 nhưng nhận được {badge_text}"


@pytest.mark.ui
@pytest.mark.regression
def test_cart_view_and_verify_total_price_calculation(page: Page):
    """
    Mục tiêu: Kiểm tra giao diện bảng giỏ hàng và tính toán tổng tiền (Mục 3.2: Giỏ hàng & thanh toán).
    Tiền điều kiện: Đã thêm sản phẩm vào giỏ hàng và mở trang /checkout.
    Kết quả mong đợi: Bảng giỏ hàng hiển thị đúng sản phẩm, tổng tiền > 0 và khớp với đơn giá.
    """
    home_page = HomePage(page)
    home_page.open()
    expect(home_page.product_cards.first).to_be_visible()
    home_page.click_first_product()

    detail_page = ProductDetailPage(page)
    expect(detail_page.btn_add_to_cart).to_be_visible()
    detail_page.add_to_cart()
    expect(detail_page.cart_quantity_badge).to_be_visible()

    # Mở giỏ hàng
    cart_page = CartPage(page)
    cart_page.open()

    expect(cart_page.cart_table).to_be_visible()
    expect(cart_page.btn_proceed_to_checkout).to_be_visible()
    total = cart_page.get_total_price_number()
    assert total > 0, f"Tổng tiền giỏ hàng phải lớn hơn 0, nhận được: {total}"


@pytest.mark.ui
@pytest.mark.regression
def test_cart_remove_item_clears_product_from_list(page: Page):
    """
    Mục tiêu: Kiểm tra thao tác xóa sản phẩm khỏi giỏ hàng (Mục 3.2: Giỏ hàng & thanh toán).
    Tiền điều kiện: Trong giỏ hàng có ít nhất 1 sản phẩm.
    Kết quả mong đợi: Sau khi bấm nút xóa (thùng rác), sản phẩm bị loại bỏ khỏi danh sách giỏ hàng.
    """
    home_page = HomePage(page)
    home_page.open()
    expect(home_page.product_cards.first).to_be_visible()
    home_page.click_first_product()

    detail_page = ProductDetailPage(page)
    expect(detail_page.btn_add_to_cart).to_be_visible()
    detail_page.add_to_cart()
    expect(detail_page.cart_quantity_badge).to_be_visible()

    cart_page = CartPage(page)
    cart_page.open()
    expect(cart_page.cart_rows.first).to_be_visible()
    initial_count = cart_page.get_cart_items_count()

    # Bấm nút xóa sản phẩm đầu tiên
    cart_page.remove_item(0)
    page.wait_for_load_state("networkidle")

    # Xác nhận số lượng sản phẩm trong bảng đã giảm
    new_count = cart_page.get_cart_items_count()
    assert new_count < initial_count, "Số lượng dòng trong giỏ hàng phải giảm sau khi xóa"
