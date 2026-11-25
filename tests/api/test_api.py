import pytest
from typing import Dict
from playwright.sync_api import APIRequestContext, expect
from conftest import generate_random_user


@pytest.mark.api
@pytest.mark.smoke
def test_status_check_system_health_returns_200(api_request_context: APIRequestContext):
    """
    Mục tiêu: Kiểm tra trạng thái hoạt động của hệ thống backend Toolshop.
    Tiền điều kiện: Hệ thống backend đang chạy.
    Kết quả mong đợi: Endpoint /status trả về HTTP 200 OK và chứa trạng thái hệ thống.
    """
    response = api_request_context.get("/status")
    expect(response).to_be_ok()
    data = response.json()
    assert "version" in data or "app_name" in data or "status" in data or "timestamp" in data


@pytest.mark.api
@pytest.mark.regression
def test_products_get_list_verifies_json_structure_and_types(api_request_context: APIRequestContext):
    """
    Mục tiêu: Kiểm tra cấu trúc và kiểu dữ liệu JSON của danh sách sản phẩm.
    Tiền điều kiện: Hệ thống có dữ liệu sản phẩm.
    Kết quả mong đợi:
    - HTTP 200 OK
    - Trường 'data' là một danh sách (list)
    - Mỗi sản phẩm có 'name' (str), 'price' (int hoặc float)
    - Không assert số lượng hay id cố định để tương thích cả PROD và BUGGY.
    """
    response = api_request_context.get("/products")
    expect(response).to_be_ok()
    body = response.json()

    assert isinstance(body, dict), "Response body phải là một JSON object"
    assert "data" in body, "Response body phải có key 'data'"
    products = body["data"]
    assert isinstance(products, list), "Trường 'data' phải là một list"
    assert len(products) > 0, "Danh sách sản phẩm không được rỗng"

    first_product = products[0]
    assert isinstance(first_product.get("name"), str), "Tên sản phẩm phải là string"
    assert isinstance(first_product.get("price"), (int, float)), "Giá sản phẩm phải là int hoặc float"


@pytest.mark.api
@pytest.mark.regression
def test_products_get_non_existent_id_returns_404_not_found(api_request_context: APIRequestContext):
    """
    Mục tiêu: Kiểm tra xử lý lỗi khi yêu cầu sản phẩm không tồn tại (Mục 3.5: Test mã lỗi 4xx).
    Tiền điều kiện: ID sản phẩm không tồn tại trong hệ thống.
    Kết quả mong đợi: HTTP 404 Not Found hoặc lỗi 4xx tương ứng.
    """
    response = api_request_context.get("/products/non-existent-product-id-999999")
    assert response.status == 404, f"Mong đợi HTTP 404 nhưng nhận được {response.status}"


@pytest.mark.api
@pytest.mark.smoke
def test_auth_login_with_invalid_credentials_returns_401_unauthorized(api_request_context: APIRequestContext):
    """
    Mục tiêu: Kiểm tra cơ chế từ chối khi thông tin đăng nhập sai (Mục 3.5: Test mã lỗi 4xx).
    Tiền điều kiện: Sử dụng email ngẫu nhiên không tồn tại (tránh dùng tài khoản mẫu để không bị khóa).
    Kết quả mong đợi: HTTP 401 Unauthorized.
    """
    fake_payload = {
        "email": "non_existent_user_99999@test.com",
        "password": "WrongPassword123!"
    }
    response = api_request_context.post("/users/login", data=fake_payload)
    assert response.status == 401, f"Mong đợi HTTP 401 nhưng nhận được {response.status}"


@pytest.mark.api
@pytest.mark.smoke
def test_users_me_authenticated_with_bearer_token_returns_profile(
    api_request_context: APIRequestContext,
    registered_user: Dict[str, str]
):
    """
    Mục tiêu: Kiểm tra endpoint yêu cầu xác thực bằng Token (Mục 3.5: Test có xác thực token).
    Tiền điều kiện: Đã có tài khoản đăng ký hợp lệ và lấy được access_token.
    Kết quả mong đợi: HTTP 200 OK và trả về đúng email của tài khoản đang đăng nhập.
    """
    # 1. Đăng nhập lấy access_token
    login_response = api_request_context.post(
        "/users/login",
        data={
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
    )
    expect(login_response).to_be_ok()
    token_data = login_response.json()
    access_token = token_data.get("access_token")
    assert access_token, "Không nhận được access_token từ API login"

    # 2. Gọi endpoint /users/me kèm Bearer Token
    profile_response = api_request_context.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    expect(profile_response).to_be_ok()
    profile_data = profile_response.json()
    assert profile_data.get("email") == registered_user["email"], "Email trả về không khớp với tài khoản đăng nhập"


@pytest.mark.api
@pytest.mark.regression
def test_contact_send_inquiry_message_returns_success(api_request_context: APIRequestContext):
    """
    Mục tiêu: Kiểm tra gửi thông điệp liên hệ qua API POST /messages (Mục 3.5: >= 2 phương thức HTTP).
    Tiền điều kiện: Thông tin liên hệ đầy đủ và hợp lệ.
    Kết quả mong đợi: HTTP 200 hoặc 201 Created.
    """
    message_payload = {
        "name": "Nguyen Van A",
        "email": "nguyenvana@example.com",
        "subject": "customer-service",
        "message": "Toi can ho tro ve don hang so #12345."
    }
    response = api_request_context.post("/messages", data=message_payload)
    assert response.status in [200, 201], f"Mong đợi HTTP 200/201 nhưng nhận được {response.status}"
