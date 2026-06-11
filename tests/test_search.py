"""
Search & Filter Tests (*Kiểm thử Tìm kiếm & Lọc sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

📖 Textbook concepts in this file:
    - Input Domain Modeling (Ch.6)
    - Automated UI Testing with Playwright & Python
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR,
)


def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name – results found (*Tìm kiếm sách theo tên — tìm thấy kết quả*)

    Description (*Mô tả*):
        Log in → search keyword "Flutter" → verify Flutter books appear in results.
        (*Đăng nhập → tìm kiếm từ khóa "Flutter" → kiểm tra có sách Flutter trong kết quả.*)
    """
    # 1. Thực hiện đăng nhập thông qua hàm helper có sẵn
    login(page, test_config)
    
    # Đảm bảo bật semantics để tương tác với các thành phần Flutter Web Canvas
    enable_flutter_semantics(page)

    # 2. Nhập từ khóa cần tìm kiếm vào ô Input tương ứng
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
    
    # Chờ một khoảng thời gian ngắn để hệ thống cập nhật kết quả tìm kiếm trên UI
    page.wait_for_timeout(2000)

    # 3. Chụp ảnh minh chứng kết quả tìm kiếm thành công
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_book_by_name_success.png"))

    # 4. Kiểm tra xem có phần tử nào chứa từ khóa "Flutter" xuất hiện hay không
    book_count = page.locator('flt-semantics[aria-label*="Flutter"]').count()
    assert book_count > 0, "Search failed: No books found containing keyword 'Flutter'."


def test_search_book_no_result(page, test_config):
    """TC-05: Search book – no results (*Tìm kiếm sách — không có kết quả*)

    Description (*Mô tả*):
        Log in → search a non-existent keyword (e.g. "xyz_khong_ton_tai_12345")
        → verify no books are displayed.
        (*Đăng nhập → tìm kiếm từ khóa không tồn tại → kiểm tra không có sách nào hiển thị.*)
    """
    # 1. Thực hiện đăng nhập
    login(page, test_config)
    enable_flutter_semantics(page)

    # 2. Nhập từ khóa ngẫu nhiên không có trong cơ sở dữ liệu
    invalid_keyword = "xyz_khong_ton_tai_12345"
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", invalid_keyword)
    
    page.wait_for_timeout(2000)

    # 3. Chụp ảnh minh chứng danh sách trống
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_book_no_result.png"))

    # 4. Xác thực không có thẻ sách nào (role="group" với Mã: BOOK) hiển thị trên màn hình
    displayed_books = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').count()
    assert displayed_books == 0, f"Search failed: System still displays books for non-existent keyword '{invalid_keyword}'."


def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ' (*Lọc sách theo thể loại 'Công nghệ'*)

    Description (*Mô tả*):
        Log in → enter "Công nghệ" in the category filter → verify all displayed books
        belong to the "Công nghệ" category.
        (*Đăng nhập → nhập "Công nghệ" vào ô lọc thể loại → kiểm tra tất cả sách
        hiển thị đều thuộc thể loại Công nghệ.*)
    """
    # 1. Thực hiện đăng nhập
    login(page, test_config)
    enable_flutter_semantics(page)

    # 2. Điền giá trị vào bộ lọc thể loại sách
    target_category = "Công nghệ"
    flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", target_category)
    
    page.wait_for_timeout(2000)

    # 3. Chụp ảnh giao diện sau khi áp dụng bộ lọc thể loại
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "filter_by_category_technology.png"))

    # 4. Lấy danh sách toàn bộ các thẻ sách đang hiển thị
    book_locators = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    total_books = book_locators.count()
    
    # Kiểm tra điều kiện tiên quyết là phải có ít nhất 1 cuốn sách thuộc thể loại này hiển thị
    assert total_books > 0, f"Filter failed: No books found for category '{target_category}'."

    # 5. Vòng lặp quét qua từng thẻ sách để kiểm tra tính nhất quán của dữ liệu
    for i in range(total_books):
        aria_label_content = book_locators.nth(i).get_attribute("aria-label")
        assert target_category in aria_label_content, \
            f"Filter anomaly detected: Book at index {i} ('{aria_label_content}') does not belong to '{target_category}'."


def test_search_by_author(page, test_config):
    """TC-07: Search book by author name (*Tìm kiếm sách theo tên tác giả*)

    Description (*Mô tả*):
        Log in → search author name (e.g. "Nguyễn Minh Đức") → verify results found.
        (*Đăng nhập → tìm kiếm tên tác giả → kiểm tra có kết quả.*)
    """
    # 1. Thực hiện đăng nhập
    login(page, test_config)
    enable_flutter_semantics(page)

    # 2. Nhập tên tác giả cụ thể cần tìm kiếm vào thanh công cụ tra cứu
    author_name = "Nguyễn Minh Đức"
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", author_name)
    
    page.wait_for_timeout(2000)

    # 3. Chụp ảnh giao diện kết quả tìm kiếm theo tác giả
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_by_author_success.png"))

    # 4. Xác thực kết quả tìm kiếm trả về đúng bản ghi của tác giả được yêu cầu
    author_match_count = page.locator(f'flt-semantics[aria-label*="{author_name}"]').count()
    assert author_match_count > 0, f"Search failed: No results found for author '{author_name}'."
