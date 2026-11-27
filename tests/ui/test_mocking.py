import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_route_abort_image_resources_speeds_up_page_load(page: Page):
    """
    Mục tiêu: Kiểm tra kỹ thuật chặn tài nguyên mạng (Mục 3.6: page.route() chặn ảnh).
    Tiền điều kiện: Chặn tất cả request có kiểu tài nguyên là 'image'.
    Kết quả mong đợi:
    - Các yêu cầu tải ảnh bị chặn thành công qua route.abort().
    - Trang chủ vẫn tải thành công mà không bị crash hay gián đoạn.
    - Nội dung chữ (tên sản phẩm, giá) vẫn hiển thị đầy đủ.
    """
    aborted_image_urls = []

    def abort_images(route):
        if route.request.resource_type == "image":
            aborted_image_urls.append(route.request.url)
            route.abort()
        else:
            route.continue_()

    # 1. Thiết lập chặn toàn bộ request tài nguyên ảnh
    page.route("**/*", abort_images)

    home_page = HomePage(page)
    home_page.open()

    # 2. Xác thực nội dung văn bản cốt lõi vẫn hiển thị bình thường
    expect(home_page.product_cards.first).to_be_visible()
    expect(home_page.product_names.first).to_be_visible()

    # 3. Kiểm chứng có ít nhất một request ảnh đã bị chặn thành công
    assert len(aborted_image_urls) > 0, "Phải có ít nhất 1 yêu cầu hình ảnh bị chặn bởi page.route()"


@pytest.mark.ui
@pytest.mark.regression
def test_route_mock_empty_product_list_displays_no_results(page: Page):
    """
    Mục tiêu: Giả lập phản hồi mạng trả về danh sách sản phẩm rỗng (Mục 3.6: Mocking response).
    Tiền điều kiện: Intercept API GET /products và trả về payload rỗng (data: []).
    Kết quả mong đợi:
    - Giao diện trang chủ nhận diện không có sản phẩm nào.
    - Không hiển thị bất kỳ thẻ sản phẩm nào.
    - Hiển thị thông báo hoặc vùng trống tương ứng.
    """
    # 1. Mock API trả về danh sách sản phẩm rỗng
    def handle_empty_products(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            json={
                "current_page": 1,
                "data": [],
                "from": None,
                "last_page": 1,
                "per_page": 9,
                "to": None,
                "total": 0
            }
        )

    page.route("**/products**", handle_empty_products)

    home_page = HomePage(page)
    home_page.open()
    page.wait_for_load_state("networkidle")

    # 2. Kiểm chứng không có sản phẩm nào được render trên giao diện
    assert home_page.product_cards.count() == 0, "Không được hiển thị thẻ sản phẩm khi API trả về danh sách rỗng"


@pytest.mark.ui
@pytest.mark.regression
def test_route_mock_server_error_500_handles_gracefully(page: Page):
    """
    Mục tiêu: Giả lập phản hồi mạng khi backend gặp sự cố HTTP 500 (Mục 3.6: Mocking response lỗi 500).
    Tiền điều kiện: Intercept API GET /products và trả về mã lỗi 500 Internal Server Error.
    Kết quả mong đợi:
    - Ứng dụng xử lý an toàn, không làm crash toàn bộ trình duyệt.
    - Thanh điều hướng (Header, Navigation) vẫn hiển thị hoạt động bình thường.
    """
    # 1. Mock API trả về lỗi 500
    page.route(
        "**/products**",
        lambda route: route.fulfill(
            status=500,
            content_type="application/json",
            json={"message": "Internal Server Error, please try again later."}
        )
    )

    home_page = HomePage(page)
    home_page.open()
    page.wait_for_load_state("networkidle")

    # 2. Xác thực trang không bị sập, các thành phần chính như Navigation vẫn truy cập được
    expect(home_page.nav_home).to_be_visible()
    expect(home_page.nav_categories).to_be_visible()
    expect(home_page.nav_contact).to_be_visible()
    # Không có thẻ sản phẩm nào tải thành công
    assert home_page.product_cards.count() == 0, "Khi server lỗi 500, danh sách sản phẩm không được hiển thị"
