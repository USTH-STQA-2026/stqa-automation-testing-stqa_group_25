"""
Logout & Language Tests (*Kiểm thử Đăng xuất & Chuyển ngôn ngữ*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 2 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 2 test case trong file này.*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR,
)


def test_logout(page, test_config):
    """TC-11: Logout success (*Đăng xuất thành công*)

    Description (*Mô tả*):
        Log in → click Logout → verify page returns to login screen.
    """
    # 1. Đăng nhập và bật semantics
    login(page, test_config)
    enable_flutter_semantics(page)

    # 2. Tìm nút Đăng xuất trên thanh AppBar và click
    logout_btn = page.locator('flt-semantics[role="button"]:has-text("Đăng xuất")').first
    assert logout_btn.count() > 0, "Không tìm thấy nút Đăng xuất."
    logout_btn.click()

    # 3. Chờ hệ thống xử lý session và điều hướng về trang Login
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)

    # 4. Chụp ảnh minh chứng
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "logout_success.png"))

    # 5. Kiểm tra xem đã quay về màn hình Đăng nhập chưa (kiểm tra có chữ Đăng nhập hoặc trường Email)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đăng nhập" in sem_text or "Email" in sem_text, \
        "Logout failed: Không tìm thấy giao diện Đăng nhập sau khi ấn đăng xuất."


def test_switch_language_to_english(page, test_config):
    """TC-12: Switch language to English (*Chuyển ngôn ngữ sang tiếng Anh*)

    Description (*Mô tả*):
        Log in → click "EN" button → verify UI switches to English.
    """
    # 1. Đăng nhập và bật semantics
    login(page, test_config)
    enable_flutter_semantics(page)

    # 2. Tìm nút "EN" trên giao diện và click để đổi ngôn ngữ
    en_btn = page.locator('flt-semantics[role="button"]:has-text("EN")').first
    assert en_btn.count() > 0, "Không tìm thấy nút chuyển ngôn ngữ EN."
    en_btn.click()

    # 3. Đợi giao diện re-render lại toàn bộ text sang tiếng Anh
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    # 4. Chụp ảnh minh chứng
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "switch_language_en.png"))

    # 5. Đọc text trên cây Semantics và kiểm tra các từ khóa tiếng Anh đặc trưng
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Logout" in sem_text or "Borrow" in sem_text or "Library" in sem_text or "Search" in sem_text, \
        "Language switch failed: Giao diện chưa được chuyển đổi thành công sang tiếng Anh."
