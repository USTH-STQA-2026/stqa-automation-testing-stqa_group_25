"""
Login Tests (*Kiểm thử Đăng nhập*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

📖 Textbook concepts in this file:
   - RIPR Model (Ch.2): See [R], [I], [P], [R✓] comments in TC-01
   - Data-Driven Testing / @parametrize (Ch.3 §3.3.2): Applied in TC-02 & TC-03
"""
import os
import pytest
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter, SCREENSHOT_DIR


def test_login_success(page, test_config):
    """TC-01: Login success with valid credentials (*Đăng nhập thành công với thông tin hợp lệ*)

    ✅ COMPLETED — Use as a reference example.
    (*ĐÃ HOÀN THÀNH — Dùng làm ví dụ tham khảo.*)

    📖 RIPR Model (Textbook Ch.2 — Reachability → Infection → Propagation → Revealability):
        Mỗi dòng code trong test tương ứng với 1 bước trong chuỗi RIPR.
        Xem comment [R], [I], [P], [R✓] bên dưới.
    """
    # [R] Reachability: Truy cập trang đăng nhập — chạm tới UI cần test
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập dữ liệu hợp lệ — kích hoạt logic đăng nhập trong hệ thống
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ trạng thái lan truyền ra UI — nút "Đăng xuất" xuất hiện
    # (Smart Wait: thay vì time.sleep(5) — nhanh hơn và ổn định hơn)
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    # [R✓] Revealability: Kiểm tra kết quả — Test Oracle phát hiện lỗi nếu có
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, \
        f"Login failed: '{test_config['display_name']}' or Logout button not found " \
        f"(Đăng nhập không thành công: không tìm thấy tên hoặc nút Đăng xuất)"


# =====================================================================
# 💡 BONUS B2: DATA-DRIVEN TESTING (Gộp TC-02 và TC-03)
# =====================================================================
@pytest.mark.parametrize("email_input, password_input, expected_error, tc_id", [
    ("valid", "wrongpassword123", "Mật khẩu không đúng", "TC-02"),
    ("", "", "Vui lòng nhập email và mật khẩu", "TC-03")
])
def test_login_fail(page, test_config, email_input, password_input, expected_error, tc_id):
    """TC-02 & TC-03: Login fail (Sai mật khẩu & Bỏ trống) áp dụng Data-Driven Testing"""

    # [R] Reachability: Truy cập trang đăng nhập
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # Xử lý logic cấu hình data: Nếu truyền vào "valid" thì lấy email đúng từ file .env
    actual_email = test_config["email"] if email_input == "valid" else email_input

    # [I] Infection: Nhập dữ liệu (chỉ điền khi có dữ liệu, bỏ qua nếu để trống)
    if actual_email != "":
        flutter_fill(page, "Email", actual_email)
    if password_input != "":
        flutter_fill(page, "Mật khẩu", password_input)

    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ thông báo lỗi cụ thể xuất hiện trên màn hình
    wait_for_flutter(page, text=expected_error)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"login_fail_{tc_id.lower()}.png"))

    # [R✓] Revealability: Kiểm tra thông báo lỗi có thực sự tồn tại trong Semantics Tree không
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert expected_error in sem_text, \
        f"{tc_id} Failed: Expected error message '{expected_error}' not found " \
        f"(Không tìm thấy thông báo lỗi mong đợi)"
