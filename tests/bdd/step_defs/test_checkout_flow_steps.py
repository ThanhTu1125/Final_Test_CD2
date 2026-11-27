import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import scenarios, given, when, then, parsers

from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage

# Liên kết toàn bộ kịch bản Gherkin trong file checkout_flow.feature (Mục 3.7)
scenarios("../features/checkout_flow.feature")


@given("the user opens the Toolshop home page")
def open_toolshop_home_page(page: Page) -> None:
    """
    Bước 1: Người dùng mở trang chủ Toolshop thông qua HomePage POM.
    """
    home_page = HomePage(page)
    home_page.open()
    expect(home_page.product_cards.first).to_be_visible()


@when(parsers.parse('the user searches for a product with keyword "{keyword}"'))
def search_product_by_keyword(page: Page, keyword: str) -> None:
    """
    Bước 2: Người dùng tìm kiếm sản phẩm theo từ khóa từ bảng Examples.
    """
    home_page = HomePage(page)
    home_page.search_product(keyword)
    expect(home_page.product_names.first).to_contain_text(keyword, ignore_case=True)


@when("the user selects the first matching product from the search results")
def select_first_matching_product(page: Page) -> None:
    """
    Bước 3: Người dùng chọn sản phẩm đầu tiên trong danh sách kết quả tìm kiếm.
    """
    home_page = HomePage(page)
    home_page.click_first_product()

    detail_page = ProductDetailPage(page)
    expect(detail_page.product_title).to_be_visible()
    expect(detail_page.btn_add_to_cart).to_be_visible()


@when(parsers.parse('the user sets the product quantity to "{quantity}" and adds it to the cart'))
def set_quantity_and_add_to_cart(page: Page, quantity: str) -> None:
    """
    Bước 4: Người dùng nhập số lượng sản phẩm và thêm vào giỏ hàng qua ProductDetailPage POM.
    """
    detail_page = ProductDetailPage(page)
    detail_page.set_quantity(int(quantity))
    detail_page.add_to_cart()
    expect(detail_page.cart_quantity_badge).to_be_visible()


@when("the user navigates to the shopping cart page")
def navigate_to_shopping_cart(page: Page) -> None:
    """
    Bước 5: Người dùng điều hướng đến trang giỏ hàng (/checkout) qua CartPage POM.
    """
    cart_page = CartPage(page)
    cart_page.open()
    expect(cart_page.cart_table).to_be_visible()


@then(parsers.parse('the shopping cart should contain a product matching "{keyword}" with total price greater than 0'))
def verify_cart_contains_product_and_valid_total(page: Page, keyword: str) -> None:
    """
    Bước 6: Xác nhận giỏ hàng hiển thị đúng sản phẩm vừa thêm và tổng tiền > 0.
    """
    cart_page = CartPage(page)
    expect(cart_page.cart_rows.first).to_be_visible()

    item_titles = cart_page.get_item_titles()
    assert len(item_titles) > 0, "Giỏ hàng không được rỗng sau khi thêm sản phẩm"
    assert any(
        keyword.lower() in title.lower() for title in item_titles
    ), f"Không tìm thấy sản phẩm chứa từ khóa '{keyword}' trong giỏ hàng: {item_titles}"

    total_price = cart_page.get_total_price_number()
    assert total_price > 0, f"Tổng tiền giỏ hàng phải lớn hơn 0, nhận được: {total_price}"


@then("the user proceeds to the checkout step and sees the authentication or billing prompt")
def proceed_to_checkout_step(page: Page) -> None:
    """
    Bước 7: Người dùng bấm nút Tiến hành thanh toán qua CheckoutPage POM và chuyển sang bước tiếp theo.
    """
    checkout_page = CheckoutPage(page)
    login_page = LoginPage(page)

    expect(checkout_page.btn_proceed_step_1).to_be_visible()
    checkout_page.proceed_to_login_or_billing()

    # Sau khi qua bước 1 (Giỏ hàng), hệ thống hiển thị bước 2 (Đăng nhập hoặc Xác nhận đã đăng nhập)
    expect(login_page.login_button.or_(checkout_page.btn_proceed_step_2)).to_be_visible()

