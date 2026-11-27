import csv
import json
import os
import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.contact_page import ContactPage


def load_search_keywords():
    """Đọc danh sách từ khóa tìm kiếm từ file JSON."""
    file_path = os.path.abspath("data/search_keywords.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_contact_messages():
    """Đọc dữ liệu kiểm thử form liên hệ từ file CSV."""
    file_path = os.path.abspath("data/contact_messages.csv")
    rows = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("data", load_search_keywords())
def test_search_with_json_dataset_displays_matching_products(page: Page, data: dict):
    """
    Mục tiêu: Kiểm thử Hướng dữ liệu (Data-driven) chức năng tìm kiếm sản phẩm từ file JSON (Mục 3.3).
    Tiền điều kiện: Đang ở trang chủ Toolshop.
    Kết quả mong đợi:
    - Danh sách kết quả hiển thị ít nhất một sản phẩm.
    - Tất cả tên sản phẩm hiển thị đều chứa từ khóa tìm kiếm (assert theo hành vi, không assert số lượng cố định).
    """
    home_page = HomePage(page)
    home_page.open()

    keyword = data["keyword"]
    home_page.search_product(keyword)

    # Chờ kết quả hiển thị và sản phẩm đầu tiên chứa keyword
    expect(home_page.product_names.first).to_contain_text(keyword, ignore_case=True)

    product_names = home_page.get_all_product_names()
    assert len(product_names) > 0, f"Không tìm thấy sản phẩm nào với từ khóa '{keyword}'"
    for name in product_names:
        assert keyword.lower() in name.lower(), f"Tên sản phẩm '{name}' không chứa từ khóa '{keyword}'"


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("data", load_contact_messages())
def test_contact_form_with_csv_dataset_submits_successfully(page: Page, data: dict):
    """
    Mục tiêu: Kiểm thử Hướng dữ liệu (Data-driven) chức năng gửi form liên hệ từ file CSV (Mục 3.3).
    Tiền điều kiện: Đang ở trang Liên hệ (/contact).
    Kết quả mong đợi:
    - Điền đầy đủ thông tin từ file CSV và gửi form thành công.
    - Hiển thị thông báo thành công chứa nội dung 'Thanks for your message'.
    """
    contact_page = ContactPage(page)
    contact_page.open()

    contact_page.fill_contact_form(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        subject=data["subject"],
        message=data["message"]
    )
    contact_page.submit()

    # Chờ thông báo thành công xuất hiện
    expect(contact_page.success_alert).to_be_visible()
    alert_text = contact_page.success_alert.inner_text()
    assert "Thanks for your message" in alert_text, f"Thông báo gửi liên hệ không đúng: {alert_text}"
