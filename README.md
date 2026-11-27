# ĐỒ ÁN CUỐI KỲ: CHUYÊN ĐỀ KIỂM THỬ TỰ ĐỘNG (AUTOMATION TESTING)

[![CI Playwright Tests](https://github.com/ThanhTu1125/Final_Test_CD2/actions/workflows/ci.yml/badge.svg)](https://github.com/ThanhTu1125/Final_Test_CD2/actions)
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-1.42+-green.svg)
![Pytest](https://img.shields.io/badge/Pytest-8.0+-orange.svg)

Dự án xây dựng bộ kiểm thử tự động toàn diện cho hệ thống website thương mại điện tử **Toolshop**, ứng dụng công nghệ **Playwright + Pytest (Python)**, tổ chức theo mô hình **Page Object Model (POM)** và tích hợp luồng **CI/CD trên GitHub Actions**.

---

## 1. Phân Công Công Việc Nhóm (3 Sinh viên)

| Thành viên | Vai trò | Trách nhiệm chính theo phân công | Tỉ lệ đóng góp |
| :--- | :--- | :--- | :---: |
| **Thành viên 1** (Chủ Repo) | **Tech Lead & Core UI** | Khởi tạo repo, BasePage, POM, bộ test UI 6 nhóm chức năng, thanh trượt giá, upload file 0 byte, tab mới GitHub, **Route/Mocking (chặn ảnh, mock 500/rỗng)**, **test Tải tệp xuống (Điểm cộng)**. | 100% |
| **Thành viên 2** | **API & Data-driven** | Fixture auth session `storage_state`, bộ test REST API (APIRequestContext, 4xx, token), bộ test Hướng dữ liệu (Data-driven) với file JSON/CSV. | 100% |
| **Thành viên 3** | **BDD, CI/CD & BUGGY** | Kịch bản BDD Gherkin (`pytest-bdd`), GitHub Actions CI ma trận 3 trình duyệt + Docker runner, đối soát hồi quy trên BUGGY và lập [docs/BUG_REPORT.md](docs/BUG_REPORT.md). | 100% |

*Chi tiết phân công nhiệm vụ và ma trận trách nhiệm xem tại:* [docs/TASK_ASSIGNMENT.md](docs/TASK_ASSIGNMENT.md)  
*Quy chuẩn phân nhánh và review Pull Request xem tại:* [docs/GIT_WORKFLOW_GUIDELINES.md](docs/GIT_WORKFLOW_GUIDELINES.md)

---

## 2. Hướng Dẫn Cài Đặt & Thực Thi Bộ Test

### 2.1. Yêu cầu môi trường
* Python 3.10 trở lên (khuyên dùng Python 3.12).
* Hệ điều hành: Windows, macOS hoặc Linux.
* Git đã được cấu hình trên máy.

### 2.2. Khởi tạo môi trường ảo và cài đặt thư viện
```bash
# 1. Clone repository về máy
git clone https://github.com/ThanhTu1125/Final_Test_CD2.git
cd Final_Test_CD2

# 2. Khởi tạo môi trường ảo Python
python -m venv .venv

# 3. Kích hoạt môi trường ảo
# Trên Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Trên macOS / Linux:
source .venv/bin/activate

# 4. Cài đặt các gói phụ thuộc
pip install -r requirements.txt

# 5. Cài đặt trình duyệt Playwright
playwright install chromium
```

### 2.3. Cấu hình biến môi trường
Tạo file `.env` từ file mẫu `.env.example`:
```env
# Chạy trên môi trường chuẩn PROD:
BASE_URL=https://practicesoftwaretesting.com
API_URL=https://api.practicesoftwaretesting.com
ROUTE_PREFIX=

# Chạy trên môi trường kiểm chứng BUGGY:
# BASE_URL=https://with-bugs.practicesoftwaretesting.com
# API_URL=https://api-with-bugs.practicesoftwaretesting.com
# ROUTE_PREFIX=/#
```

### 2.4. Các lệnh thực thi kiểm thử thông dụng
```bash
# Chạy toàn bộ các test cases (chế độ ẩn headless)
pytest

# Chạy có mở cửa sổ trình duyệt (headed mode)
pytest --headed

# Chạy theo nhóm Marker:
pytest -m smoke          # Chạy các test case cốt lõi quan trọng
pytest -m api            # Chỉ chạy các test case kiểm thử REST API
pytest -m ui             # Chỉ chạy các test case kiểm thử giao diện UI

# Chạy song song nhiều tiến trình bằng pytest-xdist
pytest -n auto

# Xem báo cáo HTML tự đóng gói sau khi chạy
# Mở file report.html trực tiếp bằng trình duyệt
```

---

## 3. Bảng Ma Trận Test Cases (Đã triển khai)

| Test Case ID | Module / Chức năng | Mô tả kịch bản kiểm thử | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) |
| :--- | :--- | :--- | :--- | :--- |
| **API-001** | API Health | Kiểm tra endpoint trạng thái hệ thống | `GET /status` | HTTP 200 OK, phản hồi chứa version / app_name. |
| **API-002** | API Products | Kiểm tra cấu trúc & kiểu dữ liệu JSON | `GET /products` | HTTP 200, `data` là list, `name: str`, `price: number`. |
| **API-003** | API Error | Kiểm tra mã lỗi khi ID không tồn tại | `GET /products/invalid-id-999999` | HTTP 404 Not Found. |
| **API-004** | API Auth | Kiểm tra từ chối đăng nhập sai | Email không tồn tại | HTTP 401 Unauthorized. |
| **API-005** | API Profile | Kiểm tra xác thực qua Bearer Token | `Authorization: Bearer <token>` | HTTP 200 OK, trả về đúng profile người dùng. |
| **API-006** | API Contact | Gửi thông điệp liên hệ qua API | `POST /messages` | HTTP 200/201 Created. |
| **UI-001** | Tìm kiếm | Tìm kiếm sản phẩm theo từ khóa | Keyword: `pliers` | Danh sách kết quả hiển thị đều chứa chữ pliers. |
| **UI-002** | Bộ lọc | Thao tác thanh trượt giá (Slider) | Kéo slider max sang trái | Danh sách sản phẩm cập nhật phù hợp với giá trần mới. |
| **UI-003** | Sắp xếp | Sắp xếp giá từ thấp đến cao | Select: `price,asc` | Danh sách giá hiển thị theo thứ tự tăng dần. |
| **UI-004** | Chi tiết SP | Xem đầy đủ thông tin sản phẩm | Click sản phẩm đầu tiên | Hiển thị tên, đơn giá > 0, mô tả, nút thêm vào giỏ. |
| **UI-005** | Chi tiết SP | Tăng số lượng sản phẩm | Bấm nút tăng (+) 2 lần | Ô số lượng hiển thị giá trị là 3. |
| **UI-006** | Giỏ hàng | Thêm sản phẩm vào giỏ từ chi tiết | Bấm nút Add to Cart | Badge giỏ hàng trên header cập nhật số lượng $\ge 1$. |
| **UI-007** | Giỏ hàng | Kiểm tra bảng giỏ hàng & tính tiền | Mở trang `/checkout` | Tổng tiền giỏ hàng hiển thị chính xác > 0. |
| **UI-008** | Giỏ hàng | Xóa sản phẩm khỏi giỏ hàng | Bấm icon xóa (thùng rác) | Dòng sản phẩm bị xóa khỏi bảng giỏ hàng. |
| **UI-009** | Xác thực | Đăng nhập sai tài khoản | Email không tồn tại | Hiển thị thông báo lỗi `Invalid email or password`. |
| **UI-010** | Xác thực | Đăng nhập tài khoản hợp lệ | Tài khoản fixture nhóm | Chuyển hướng thành công, menu user hiển thị. |
| **UI-011** | Liên hệ | Upload tệp rỗng 0 byte (Bắt buộc) | Tệp `data/empty_file_0byte.txt` | Form chấp nhận tệp và gửi thành công. |
| **UI-012** | Footer | Link GitHub mở tab mới (Bắt buộc) | Click footer GitHub link | Bắt sự kiện expect_page(), tab mới dẫn tới github.com. |
| **UI-013** | Tài khoản | Xem trang profile tài khoản | Dùng `authenticated_page` | Trang profile hiển thị đúng tên/email tài khoản nhóm. |
| **MCK-001** | Route/Mocking | Chặn tài nguyên hình ảnh (Mục 3.6) | Chặn `**/*.{png,jpg,jpeg...}` | Trang tải nhanh, text hiển thị, ảnh bị chặn. |
| **MCK-002** | Route/Mocking | Mock API trả về danh sách rỗng | Mock `**/products**` payload `[]` | Giao diện hiển thị vùng trống/no-results. |
| **MCK-003** | Route/Mocking | Mock API trả về mã lỗi 500 | Mock `**/products**` status 500 | Trang xử lý an toàn không sập trình duyệt. |
| **DLD-001** | Tải tệp xuống | Tải file PDF hóa đơn (ĐIỂM CỘNG) | Bắt sự kiện expect_download | File lưu thành công, đuôi .pdf, dung lượng > 0 byte. |
| **DDT-001** | Data-driven UI | Tìm kiếm sản phẩm đa từ khóa từ JSON (Mục 3.3) | `data/search_keywords.json` | Kết quả hiển thị đúng sản phẩm chứa từ khóa tương ứng. |
| **DDT-002** | Data-driven UI | Gửi form liên hệ đa bộ dữ liệu từ CSV (Mục 3.3) | `data/contact_messages.csv` | Form gửi thành công và hiển thị thông báo alert success. |

---

## 4. Minh Bạch Sử Dụng Trợ Lý AI (Mục 6)

Theo đúng quy định tại **Mục 6 (Sử dụng AI)** của đề tài, nhóm công khai minh bạch các phạm vi có sự hỗ trợ của AI:
* **Công cụ sử dụng:** Antigravity AI Assistant, Playwright CLI code generator.
* **Các phần có AI hỗ trợ:**
  * Hỗ trợ gợi ý khung cú pháp khởi tạo Page Object Model và mẫu docstring chuẩn.
  * Hỗ trợ tìm kiếm cấu trúc dữ liệu payload API đăng ký của Toolshop trên PROD (đối tượng `address`).
* **Cam kết cá nhân:** Mọi thành viên trong nhóm đều hiểu tường tận từng dòng mã nguồn, sẵn sàng trả lời chất vấn và giải thích lý do lựa chọn từng bộ định vị (locator) trong buổi thi vấn đáp.
