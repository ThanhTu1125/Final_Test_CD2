from typing import List
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class HomePage(BasePage):
    """
    Page Object cho Trang chủ Toolshop (practicesoftwaretesting.com).
    Bao gồm:
    - Tìm kiếm sản phẩm
    - Bộ lọc danh mục, thương hiệu
    - Bộ lọc giá bằng thanh trượt (slider)
    - Sắp xếp sản phẩm
    - Danh sách thẻ sản phẩm
    """

    def __init__(self, page: Page, base_url: str = None, route_prefix: str = None):
        super().__init__(page, base_url, route_prefix)

        # --- Locators Tìm kiếm ---
        self.search_input = self.page.get_by_test_id("search-query")
        self.search_button = self.page.get_by_test_id("search-submit")
        self.search_reset_button = self.page.get_by_test_id("search-reset")

        # --- Locators Bộ lọc & Sắp xếp ---
        self.sort_select = self.page.get_by_test_id("sort")
        # Thanh trượt lọc giá (ngx-slider) - Yêu cầu Mục 3.2
        self.price_slider_container = self.page.locator(".ngx-slider")
        self.price_slider_min_pointer = self.page.locator(".ngx-slider-pointer-min")
        self.price_slider_max_pointer = self.page.locator(".ngx-slider-pointer-max")
        self.price_slider_ceil_label = self.page.locator(".ngx-slider-ceil")
        self.price_slider_floor_label = self.page.locator(".ngx-slider-floor")

        # --- Locators Danh sách sản phẩm ---
        self.product_cards = self.page.locator("a.card")
        self.product_names = self.page.get_by_test_id("product-name")
        self.product_prices = self.page.get_by_test_id("product-price")
        self.no_results_message = self.page.get_by_test_id("no-results")

    def open(self) -> None:
        """Mở trang chủ."""
        self.navigate("/")

    def search_product(self, keyword: str) -> None:
        """Thực hiện tìm kiếm sản phẩm theo từ khóa."""
        self.search_input.fill(keyword)
        self.search_button.click()
        self.page.wait_for_load_state("networkidle")

    def reset_search(self) -> None:
        """Reset ô tìm kiếm."""
        self.search_reset_button.click()

    def select_sort_option(self, option_value_or_text: str) -> None:
        """
        Sắp xếp sản phẩm (vd: 'name,asc', 'name,desc', 'price,asc', 'price,desc').
        """
        self.sort_select.select_option(option_value_or_text)

    def filter_by_brand(self, brand_name: str) -> None:
        """Chọn checkbox thương hiệu theo tên."""
        checkbox = self.page.get_by_label(brand_name)
        if not checkbox.is_checked():
            checkbox.check()

    def filter_by_category(self, category_name: str) -> None:
        """Chọn checkbox danh mục theo tên."""
        checkbox = self.page.get_by_label(category_name)
        if not checkbox.is_checked():
            checkbox.check()

    def adjust_price_slider_max(self, offset_x: int = -50) -> None:
        """
        Kéo thanh trượt giá tối đa (ngx-slider-pointer-max) sang trái để lọc giá.
        Yêu cầu Mục 3.2: có testcase thao tác với thanh trượt.
        """
        box = self.price_slider_max_pointer.bounding_box()
        if box:
            self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            self.page.mouse.down()
            self.page.mouse.move(box["x"] + box["width"] / 2 + offset_x, box["y"] + box["height"] / 2)
            self.page.mouse.up()

    def get_all_product_names(self) -> List[str]:
        """Lấy danh sách tất cả tên sản phẩm đang hiển thị."""
        return self.product_names.all_text_contents()

    def get_all_product_prices(self) -> List[float]:
        """Lấy danh sách giá sản phẩm (đã bóc tách ký tự $ và convert sang float)."""
        texts = self.product_prices.all_text_contents()
        prices = []
        for text in texts:
            cleaned = text.replace("$", "").strip()
            try:
                prices.append(float(cleaned))
            except ValueError:
                pass
        return prices

    def click_first_product(self) -> None:
        """Click vào thẻ sản phẩm đầu tiên."""
        self.product_cards.first.click()

    def click_product_by_name(self, product_name: str) -> None:
        """Click vào sản phẩm có tên cụ thể."""
        self.product_names.filter(has_text=product_name).first.click()
