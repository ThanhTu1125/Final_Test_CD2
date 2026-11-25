# QUY TRÌNH PHỐI HỢP GIT & REVIEW PULL REQUEST (GIT WORKFLOW GUIDELINES)

Tài liệu này quy định chuẩn hóa quy trình làm việc trên Git, quản trị nhánh, kiểm thử cộng tác và văn hóa review code giữa các thành viên trong nhóm, phục vụ yêu cầu **Mục 3.8 (Git / GitHub)** của đồ án cuối kỳ môn Kiểm thử tự động.

---

## 1. Mục tiêu và Ý nghĩa Kỹ thuật
* **Bảo vệ mã nguồn chính (`main`):** Ngăn chặn việc đẩy code trực tiếp làm gãy luồng kiểm thử hoặc đưa vào các vi phạm bị trừ điểm (như commit `.venv`, `report.html`, hard-code URL).
* **Minh bạch đóng góp cá nhân:** Đảm bảo mọi thành viên đều có commit và Pull Request đứng tên mình, phục vụ phần đánh giá cá nhân (2.0 điểm).
* **Đảm bảo tính hồi quy:** Code chỉ được tích hợp vào `main` sau khi đã vượt qua quá trình kiểm tra cục bộ và nhận được phê duyệt từ thành viên khác trong nhóm.

---

## 2. Quy trình Cấp quyền Cộng tác viên (Collaborators)
1. **Chủ Repository (Repo Owner):**
   * Truy cập GitHub Repository $\to$ **Settings** $\to$ **Collaborators**.
   * Nhấn **Add people**, nhập username/email GitHub của 2 thành viên còn lại.
2. **Thành viên nhận lời mời:**
   * Kiểm tra email hoặc truy cập thông báo GitHub để nhấn **Accept invitation**.
   * Chỉ sau khi chấp nhận lời mời, thành viên mới có quyền đẩy nhánh lên repository.

---

## 3. Chiến lược Phân nhánh (Branching Strategy)

> ⛔ **Nguyên tắc bất di bất dịch:** Không commit hoặc push trực tiếp lên nhánh `main`. Mọi công việc đều thực hiện trên nhánh tính năng (feature branch).

### Quy ước đặt tên nhánh:
* Nhánh tính năng kiểm thử mới: `feat/<tên-chức-năng>` (vd: `feat/route-mocking`, `feat/data-driven-tests`, `feat/bdd-checkout-flow`)
* Nhánh sửa lỗi / điều chỉnh locator: `fix/<tên-lỗi>` (vd: `fix/contact-form-message`, `fix/auth-storage-state`)
* Nhánh tài liệu: `docs/<tên-tài-liệu>` (vd: `docs/bug-report-buggy`, `docs/readme-matrix`)
* Nhánh cấu hình CI/CD: `ci/<nội-dung>` (vd: `ci/github-actions-docker-matrix`)

### Chu trình lệnh thao tác trên máy cá nhân:
```bash
# 1. Chuyển về nhánh main và cập nhật mã nguồn mới nhất
git checkout main
git pull origin main

# 2. Khởi tạo và chuyển sang nhánh làm việc mới
git checkout -b feat/<ten-tinh-nang>

# 3. Thực hiện lập trình và kiểm thử nội bộ trên máy cá nhân
pytest tests/<duong-dan-test> -v

# 4. Gom nhóm thay đổi và commit theo chuẩn Semantic Commit Messages
git add <cac-file-thay-doi>
git commit -m "loại(phạm-vi): mô tả ngắn gọn bằng thể mệnh lệnh"
# Ví dụ: git commit -m "feat(mocking): implement route abort and mock response tests"

# 5. Đẩy nhánh lên GitHub
git push -u origin feat/<ten-tinh-nang>
```

---

## 4. Chuẩn hóa Tạo Pull Request (PR)

Khi nhánh được đẩy lên GitHub, tác giả nhánh tiến hành mở Pull Request vào nhánh `main`.

### Cấu trúc nội dung PR chuẩn:
* **Tiêu đề (Title):** Ghi rõ loại thay đổi và phạm vi (vd: `feat(ui): bổ sung bộ test Route / Mocking theo Mục 3.6`).
* **Nội dung mô tả (Body):** Bắt buộc tuân thủ mẫu:

```markdown
### 🎯 Mục tiêu công việc
- Xây dựng 2 test case cho kỹ thuật Route / Mocking bằng `page.route()` thỏa mãn Mục 3.6.

### 📋 Danh sách thay đổi chi tiết
- [x] Tạo file `tests/ui/test_mocking.py`.
- [x] Test case 1: Chặn tài nguyên hình ảnh (`route.abort()`) để kiểm tra fallback UI và tối ưu tải trang.
- [x] Test case 2: Giả lập phản hồi HTTP 500 / danh sách rỗng (`route.fulfill()`) để kiểm chứng thông báo lỗi trên UI.

### 🧪 Bằng chứng kiểm thử (Local Execution)
- Lệnh chạy: `pytest tests/ui/test_mocking.py -v`
- Kết quả: 2 passed in 3.45s.
- Báo cáo đính kèm: Đã kiểm tra không có vi phạm hard-code URL và không có `time.sleep()`.

### 👤 Phân công
- Author: @<username_tac_gia>
- Assignee: @<username_tac_gia>
- Reviewer: @<username_nguoi_review>
```

---

## 5. Quy trình Kiểm thử Đánh giá Chéo (Peer Code Review)

Thành viên được chỉ định làm Reviewer có trách nhiệm kiểm tra toàn diện trước khi bấm phê duyệt (Approve).

### Bảng kiểm duyệt kỹ thuật (Review Checklist):
| STT | Tiêu chí kỹ thuật | Yêu cầu kiểm tra | Trạng thái |
| :---: | :--- | :--- | :---: |
| 1 | **Page Object Model** | Không có câu lệnh `expect()` hay assertion bên trong các class `pages/`. | ☐ |
| 2 | **Cơ chế chờ (Wait)** | Tuyệt đối **không** có lệnh `time.sleep()`. Sử dụng auto-wait của Playwright hoặc `expect()`. | ☐ |
| 3 | **Biến môi trường** | Mọi URL đều thông qua `BASE_URL`, `API_URL`, `ROUTE_PREFIX`, không viết cứng chuỗi URL. | ☐ |
| 4 | **Tính độc lập** | Test case chạy độc lập, có thể thực thi đơn lẻ mà không phụ thuộc thứ tự chạy của test khác. | ☐ |
| 5 | **Không commit file cấm**| Không có sự xuất hiện của `report.html`, `.venv/`, `test-results/`, `storage_state.json`. | ☐ |

### Thao tác phê duyệt trên GitHub:
1. Vào tab **Files changed** của PR.
2. Kiểm tra các dòng mã nguồn thay đổi.
3. Bấm **Review changes** ở góc phải:
   * Nếu có điểm chưa đạt: Chọn **Request changes** và ghi rõ lý do kỹ thuật cần chỉnh sửa.
   * Nếu đạt yêu cầu: Chọn **Approve** và để lại lời nhận xét kỹ thuật:
     > *"Code tuân thủ chặt chẽ mô hình POM, các bộ định vị ưu tiên đúng test-id/role, không phát hiện vi phạm time.sleep hay hard-code URL. Test đã được xác thực cục bộ. Phê duyệt gộp code (LGTM)!"*
4. Nhấn **Submit review**.

---

## 6. Gộp mã nguồn (Merging) & Đồng bộ Cục bộ (Local Sync)
1. Sau khi nhận đủ phê duyệt (ít nhất 1 Approval) và các kiểm tra trạng thái CI hoàn thành:
   * Nhấn **Merge pull request** $\to$ **Confirm merge**.
   * Nhấn **Delete branch** để dọn dẹp nhánh tính năng trên remote.
2. Tất cả thành viên trong nhóm lập tức đồng bộ mã nguồn mới nhất về máy cá nhân:
   ```bash
   git checkout main
   git pull origin main
   ```
