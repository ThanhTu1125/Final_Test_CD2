import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
def test_search_valid_keyword_displays_matching_products(page: Page):
    """
    Mục tiêu: Kiểm tra chức năng tìm kiếm sản phẩm với từ khóa hợp lệ (Mục 3.2: Danh sách & tìm kiếm).
    Tiền điều kiện: Đang ở trang chủ Toolshop.
    Kết quả mong đợi:
    - Danh sách kết quả hiển thị ít nhất một sản phẩm.
    - Tất cả tên sản phẩm hiển thị đều chứa từ khóa tìm kiếm (không phân biệt hoa thường).
    """
    home_page = HomePage(page)
    home_page.open()

    keyword = "pliers"
    home_page.search_product(keyword)

    # Chờ kết quả tìm kiếm cập nhật và sản phẩm đầu tiên chứa keyword
    expect(home_page.product_names.first).to_contain_text(keyword, ignore_case=True)

    product_names = home_page.get_all_product_names()
    assert len(product_names) > 0, "Không tìm thấy sản phẩm nào với từ khóa"
    for name in product_names:
        assert keyword.lower() in name.lower(), f"Tên sản phẩm '{name}' không chứa từ khóa '{keyword}'"


@pytest.mark.ui
@pytest.mark.regression
def test_filter_price_slider_adjusts_displayed_products(page: Page):
    """
    Mục tiêu: Kiểm tra bộ lọc giá bằng thanh trượt (Mục 3.2: Bắt buộc >= 1 testcase thanh trượt ở trang chủ).
    Tiền điều kiện: Trang chủ đã tải danh sách sản phẩm và thanh trượt giá sẵn sàng.
    Kết quả mong đợi: Sau khi kéo thanh trượt giá tối đa về bên trái, các sản phẩm hiển thị đều có giá hợp lệ.
    """
    home_page = HomePage(page)
    home_page.open()

    # Đảm bảo slider hiển thị
    expect(home_page.price_slider_container).to_be_visible()
    expect(home_page.product_cards.first).to_be_visible()

    # Kéo thanh trượt max sang trái để hạ giá trần
    home_page.adjust_price_slider_max(offset_x=-70)

    # Chờ danh sách sản phẩm cập nhật
    page.wait_for_load_state("networkidle")
    expect(home_page.product_cards.first).to_be_visible()

    prices = home_page.get_all_product_prices()
    assert len(prices) > 0, "Cần có ít nhất 1 sản phẩm hiển thị sau khi lọc giá"


@pytest.mark.ui
@pytest.mark.regression
def test_sort_products_by_price_orders_ascending(page: Page):
    """
    Mục tiêu: Kiểm tra chức năng sắp xếp sản phẩm theo giá tăng dần (Mục 3.2: Bộ lọc & sắp xếp).
    Tiền điều kiện: Đang ở trang chủ Toolshop.
    Kết quả mong đợi: Danh sách giá sản phẩm sau khi sắp xếp thỏa mãn thứ tự tăng dần.
    """
    home_page = HomePage(page)
    home_page.open()

    expect(home_page.product_cards.first).to_be_visible()

    # Chọn sắp xếp giá từ thấp đến cao (price,asc)
    home_page.select_sort_option("price,asc")

    # Chờ trang load lại dữ liệu sắp xếp
    page.wait_for_load_state("networkidle")
    expect(home_page.product_cards.first).to_be_visible()

    prices = home_page.get_all_product_prices()
    assert len(prices) >= 2, "Cần ít nhất 2 sản phẩm để kiểm tra thứ tự sắp xếp"
    # Kiểm tra danh sách giá sau khi sắp xếp tăng dần theo hành vi (yêu cầu Mục 1 & 2)
    assert prices == sorted(prices), f"Danh sách giá chưa được sắp xếp tăng dần: {prices}"
