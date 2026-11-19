# BÁO CÁO LỖI HỆ THỐNG BUGGY (BUG_REPORT.md)

Tài liệu ghi nhận các lỗi phát hiện được trên môi trường kiểm thử **BUGGY** (`with-bugs.practicesoftwaretesting.com` / `api-with-bugs.practicesoftwaretesting.com`) so với môi trường chuẩn **PROD** (`practicesoftwaretesting.com`).

---

## Danh sách lỗi phát hiện

### Mẫu báo cáo lỗi:

#### [BUG-001] Tên mô tả ngắn gọn về lỗi
* **Chức năng:** (Ví dụ: Giỏ hàng / Đăng nhập / Thanh toán...)
* **Test case phát hiện:** `tests/ui/test_cart.py::test_cart_add_item_success`
* **Các bước tái hiện (Steps to Reproduce):**
  1. Truy cập trang chi tiết sản phẩm...
  2. Bấm nút "Add to Cart"...
  3. Mở giỏ hàng...
* **Kết quả mong đợi (Expected Result):** Sản phẩm được thêm vào giỏ hàng với số lượng chính xác là 1 (xanh trên PROD).
* **Kết quả thực tế (Actual Result):** Giỏ hàng trống hoặc báo lỗi không tương thích (đỏ trên BUGGY).
* **Bằng chứng (Trace / Screenshot):**
  * Screenshot: `docs/screenshots/bug_001.png`
  * Trace file: `test-results/.../trace.zip`
* **Phân loại lỗi môi trường:** (Lỗi logic hệ thống / Khác biệt môi trường / ...)

---
