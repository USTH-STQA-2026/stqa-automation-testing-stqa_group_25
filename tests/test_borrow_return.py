"""
Borrow & Return Tests (*Kiểm thử Mượn & Trả sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 3 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 3 test case trong file này.*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR,
)


def test_borrow_book(page, test_config):
    """TC-08: Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)

    Description (*Mô tả*):
        Log in → find an "Available" book → click "Mượn sách này" → confirm dialog
        → verify book status changes to "Borrowed" or success message appears.
    """
    # 1. Đăng nhập và kích hoạt Semantics Tree
    login(page, test_config)
    enable_flutter_semantics(page)

    # 2. Tìm cuốn sách đầu tiên đang ở trạng thái "Có sẵn"
    available_book = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
    assert available_book.count() > 0, "Không tìm thấy sách nào đang 'Có sẵn' để mượn."

    # 3. Bấm vào nút "Mượn sách này" của cuốn sách đó
    available_book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")').first.click()

    # 4. Đợi hộp thoại xác nhận (Dialog) bật lên và kích hoạt lại Semantics
    # LƯU Ý QUAN TRỌNG: Flutter vẽ lại UI khi có Dialog, phải bật lại semantics
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)

    # 5. Bấm nút "Mượn" trong Dialog để xác nhận
    page.locator('flt-semantics[role="button"]:has-text("Mượn")').first.click()

    # 6. Đợi hệ thống xử lý API và vẽ lại UI, sau đó kiểm tra kết quả
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    
    # Chụp ảnh minh chứng
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_book_success.png"))

    # Đọc toàn bộ text trên màn hình để kiểm tra thông báo thành công hoặc trạng thái Đang mượn
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Thành công" in sem_text or "Đang mượn" in sem_text, \
        "Borrow failed: Không thấy thông báo thành công hoặc trạng thái sách chưa chuyển sang Đang mượn."


def test_view_borrowed_books(page, test_config):
    """TC-09: View borrowed books list (*Xem danh sách sách đang mượn — tab Mượn / Trả*)

    Description (*Mô tả*):
        Log in → switch to "Mượn / Trả" tab → verify borrowed books are shown.
    """
    # 1. Đăng nhập
    login(page, test_config)
    enable_flutter_semantics(page)

    # 2. Chuyển sang tab "Mượn / Trả"
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').click()
    
    # Đợi load danh sách phiếu mượn và bật lại Semantics
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    # 3. Chụp ảnh minh chứng
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "view_borrowed_books.png"))

    # 4. Kiểm tra xem có sách "Đang mượn" hoặc có xuất hiện nút "Trả sách" không
    borrowed_books_count = page.locator('flt-semantics[role="group"][aria-label*="Đang mượn"]').count()
    return_buttons_count = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').count()
    
    assert borrowed_books_count > 0 or return_buttons_count > 0, \
        "View failed: Không tìm thấy cuốn sách nào đang mượn trong tab Mượn/Trả."


def test_return_book(page, test_config):
    """TC-10: Return a borrowed book (*Trả sách đang mượn*)

    Description (*Mô tả*):
        Log in → go to "Mượn / Trả" tab → click "Trả sách" → verify book is returned.
    """
    # 1. Đăng nhập
    login(page, test_config)
    enable_flutter_semantics(page)

    # 2. Chuyển sang tab "Mượn / Trả"
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').click()
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    # 3. Tìm nút "Trả sách" đầu tiên và bấm vào đó
    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    assert return_btn.count() > 0, "Return failed: Không tìm thấy nút 'Trả sách' nào, có thể tài khoản chưa mượn sách."
    return_btn.click()

    # 4. Đợi hệ thống xử lý giao dịch trả sách và cập nhật UI
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    
    # Chụp ảnh minh chứng
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "return_book_success.png"))

    # 5. Kiểm tra thông báo hoặc sự thay đổi trên màn hình
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Thành công" in sem_text or "Có sẵn" in sem_text or "Đã trả" in sem_text, \
        "Return failed: Không thấy thông báo trả sách thành công."
