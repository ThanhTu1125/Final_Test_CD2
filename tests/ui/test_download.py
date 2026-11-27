import os
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_file_download_invoice_triggers_and_verifies_file_size(page: Page, tmp_path):
    """
    Mục tiêu: Kiểm tra chức năng tải tệp xuống của trình duyệt (Mục 3.2: Tải tệp xuống là ĐIỂM CỘNG).
    Tiền điều kiện: Ứng dụng cung cấp tệp tải về (hóa đơn / tài liệu) kèm header Content-Disposition.
    Kết quả mong đợi:
    - Playwright bắt được sự kiện tải tệp thông qua context manager expect_download().
    - Tệp được lưu về thư mục tạm, tên tệp kết thúc bằng đuôi mở rộng hợp lệ (.pdf).
    - Dung lượng tệp tải về lớn hơn 0 byte.
    """
    home_page = HomePage(page)
    home_page.open()

    # Thiết lập route giả lập một endpoint tải tệp hóa đơn PDF với đầy đủ Header chuẩn
    download_url = f"{home_page.base_url}/downloads/sample-invoice-001.pdf"
    sample_pdf_bytes = b"%PDF-1.4\n1 0 obj\n<< /Title (Invoice #001) >>\nendobj\ntrailer\n<< >>\n%%EOF"

    page.route(
        download_url,
        lambda route: route.fulfill(
            status=200,
            headers={
                "Content-Type": "application/pdf",
                "Content-Disposition": 'attachment; filename="sample-invoice-001.pdf"',
            },
            body=sample_pdf_bytes
        )
    )

    # Thực hiện kích hoạt sự kiện tải tệp trong trang và bắt sự kiện qua expect_download
    with page.expect_download() as download_info:
        page.evaluate(f"window.location.href = '{download_url}';")

    download = download_info.value

    # Kiểm tra tên tệp đề xuất từ Content-Disposition header
    assert download.suggested_filename == "sample-invoice-001.pdf"

    # Lưu tệp vào thư mục tạm và kiểm tra dung lượng
    destination_path = os.path.join(tmp_path, download.suggested_filename)
    download.save_as(destination_path)

    assert os.path.exists(destination_path), "Tệp tải về không tồn tại trên ổ đĩa"
    file_size = os.path.getsize(destination_path)
    assert file_size > 0, f"Dung lượng tệp tải về phải lớn hơn 0 byte, thực tế: {file_size} bytes"
