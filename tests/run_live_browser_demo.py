"""
Script Trình Diễn & Kiểm Tra Trực Quan Live (Headful Chrome - Headless=False)
Mở cửa sổ Google Chrome thật trên macOS, tự động thao tác chậm rãi (slow_mo=800ms)
để người dùng theo dõi trực quan từng tương tác giao diện trên cổng 8505.
"""
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
APP_URL = "http://localhost:8505"


def ensure_sidebar_open(page):
    sidebar = page.locator('section[data-testid="stSidebar"]')
    if not sidebar.is_visible():
        btn = page.locator('button[data-testid="stExpandSidebarButton"], [data-testid="collapsedControl"]').first
        if btn.is_visible():
            btn.click()
            time.sleep(1.2)


def ensure_sidebar_closed(page):
    sidebar = page.locator('section[data-testid="stSidebar"]')
    if sidebar.is_visible():
        btn = page.locator('button[data-testid="stSidebarCollapseButton"]').first
        if btn.is_visible():
            btn.click()
            time.sleep(1.2)


def ensure_presets_open(page):
    exp = page.locator("summary:has-text('thử nhanh các kịch bản lừa đảo')").first
    if exp.is_visible():
        is_open = page.locator("details:has(summary:has-text('thử nhanh các kịch bản lừa đảo'))").first.get_attribute("open")
        if is_open is None:
            exp.click()
            time.sleep(0.6)


def scroll_top(page):
    page.evaluate("() => { const el = document.querySelector('section.stMain'); if (el) el.scrollTop = 0; }")
    time.sleep(0.6)


def scroll_to(page, y):
    page.evaluate(f"() => {{ const el = document.querySelector('section.stMain'); if (el) el.scrollTop = {y}; }}")
    time.sleep(0.6)


def main():
    print("=" * 75)
    print("🖥️  KHỞI CHẠY GOOGLE CHROME TRỰC QUAN TRÊN MÀN HÌNH (HEADFUL MODE)")
    print("=" * 75)

    with sync_playwright() as p:
        # Khởi chạy Chrome thật có giao diện với độ trễ thao tác slow_mo=700ms
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=False,
            slow_mo=700,
            args=["--start-maximized", "--window-size=1440,960"],
        )
        context = browser.new_context(viewport={"width": 1440, "height": 960})
        page = context.new_page()

        print("\n[BƯỚC 1] Truy cập ứng dụng tại:", APP_URL)
        page.goto(APP_URL, wait_until="networkidle")
        time.sleep(2)

        print("[BƯỚC 2] Kiểm tra trạng thái mặc định:")
        print("  - Sidebar mặc định: Thu gọn (Collapsed)")
        print("  - Nút Hotline đầu trang: 'Gọi 156' (Đỏ) & 'Gọi 113' (Cam) chữ trắng sắc nét")
        print("  - Cột phải: Hiển thị Ảnh bìa chính thức docs/cover.png của đồ án CS114")
        print("  - Cột trái: Nút động '📋 Nạp tin mẫu' khi chưa có nội dung")
        time.sleep(2)

        print("\n[BƯỚC 3] Bấm nút '📋 Nạp tin mẫu'...")
        btn_sample = page.get_by_role("button", name="📋 Nạp tin mẫu")
        if btn_sample.is_visible():
            btn_sample.click()
            time.sleep(1.5)

        print("[BƯỚC 4] Bấm '🔍 KIỂM TRA TIN NHẮN NGAY'...")
        btn_check = page.get_by_role("button", name="🔍 KIỂM TRA TIN NHẮN NGAY")
        btn_check.click()
        time.sleep(2.5)

        print("[BƯỚC 5] Cuộn xem Thước đo rủi ro và Phân tích bẫy tâm lý...")
        scroll_to(page, 350)
        time.sleep(2)

        print("\n[BƯỚC 6] Kiểm tra nút động: Bấm '🗑️ Xóa tin' để làm sạch ô nhập...")
        scroll_top(page)
        btn_clear = page.get_by_role("button", name="🗑️ Xóa tin")
        if btn_clear.is_visible():
            btn_clear.click()
            time.sleep(1.5)

        print("\n[BƯỚC 7] Thử nghiệm Kịch bản 1-chạm: '🚨 Báo người thân tai nạn cấp cứu'...")
        ensure_presets_open(page)
        btn_emg = page.get_by_role("button", name="🚨 Báo người thân tai nạn cấp cứu")
        if btn_emg.is_visible():
            btn_emg.click()
            time.sleep(1.5)
            btn_check.click()
            time.sleep(2.5)

        print("\n[BƯỚC 8] Mở Sidebar (bấm nút '>>' góc trên bên trái)...")
        ensure_sidebar_open(page)
        time.sleep(1.5)

        print("[BƯỚC 9] Kiểm tra Bộ chỉnh cỡ chữ trực quan:")
        print("  - Bấm 'Chữ Rất To (150%)'...")
        font_150 = page.locator("label:has-text('Chữ Rất To (150%)')")
        if font_150.is_visible():
            font_150.click()
            time.sleep(2)

        print("  - Bấm 'Chữ Vừa (100%)'...")
        font_100 = page.locator("label:has-text('Chữ Vừa (100%)')")
        if font_100.is_visible():
            font_100.click()
            time.sleep(1.5)

        print("  - Trả về 'Chữ To (125%)'...")
        font_125 = page.locator("label:has-text('Chữ To (125%)')")
        if font_125.is_visible():
            font_125.click()
            time.sleep(1.5)

        print("\n[BƯỚC 10] Bật '🎓 Chế độ Giảng viên CS114' để đối chứng 4 mô hình học máy...")
        toggle_academic = page.locator("label:has-text('Chế độ Giảng viên')").first
        if toggle_academic.is_visible():
            toggle_academic.click()
            time.sleep(2)

        print("\n[BƯỚC 11] Đóng Sidebar lại để quan sát giao diện tổng thể...")
        ensure_sidebar_closed(page)
        scroll_top(page)
        time.sleep(3)

        print("\n" + "=" * 75)
        print("✅ TRÌNH DIỄN VÀ KIỂM TRA TRỰC QUAN HOÀN TẤT THÀNH CÔNG!")
        print("=" * 75)
        time.sleep(2)
        browser.close()


if __name__ == "__main__":
    main()
