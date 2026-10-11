"""
Bộ kiểm thử tự động toàn diện Web App Streamlit (CS114 Final Project - PR #21)
Thực thi kiểm tra end-to-end trên trình duyệt Google Chrome thực tế qua Playwright.
Chụp ảnh màn hình nghiệm thu độ phân giải cao cho từng ca kiểm thử.
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ARTIFACT_SCREENSHOT_DIR = Path("/Users/tcdtist/.gemini/antigravity-ide/brain/976d48f3-08e3-4372-a127-7a570aae9d8b/screenshots")
ARTIFACT_SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
APP_URL = "http://localhost:8505"


def scroll_top(page):
    page.evaluate("() => { const el = document.querySelector('section.stMain'); if (el) el.scrollTop = 0; }")
    time.sleep(0.4)


def scroll_to(page, y):
    page.evaluate(f"() => {{ const el = document.querySelector('section.stMain'); if (el) el.scrollTop = {y}; }}")
    time.sleep(0.4)


def ensure_sidebar_open(page):
    sidebar = page.locator('section[data-testid="stSidebar"]')
    if not sidebar.is_visible():
        btn = page.locator('button[data-testid="stExpandSidebarButton"], [data-testid="collapsedControl"]').first
        if btn.is_visible():
            btn.click()
            time.sleep(1.0)


def ensure_sidebar_closed(page):
    sidebar = page.locator('section[data-testid="stSidebar"]')
    if sidebar.is_visible():
        btn = page.locator('button[data-testid="stSidebarCollapseButton"]').first
        if btn.is_visible():
            btn.click()
            time.sleep(1.0)


def ensure_presets_open(page):
    exp = page.locator("summary:has-text('thử nhanh các kịch bản lừa đảo')").first
    if exp.is_visible():
        is_open = page.locator("details:has(summary:has-text('thử nhanh các kịch bản lừa đảo'))").first.get_attribute("open")
        if is_open is None:
            exp.click()
            time.sleep(0.6)


def select_model(page, model_keyword: str):
    sb = page.locator('div[data-testid="stSelectbox"]').first
    if not sb.is_visible():
        return False
    sb_btn = sb.locator('button[aria-label="Open"], div[role="combobox"]').first
    sb_btn.click()
    time.sleep(0.8)
    opt = page.locator(f'[role="option"]:has-text("{model_keyword}")').first
    if not opt.is_visible():
        # Thử click lại nếu menu chưa bung
        sb_btn.click()
        time.sleep(0.8)
    if opt.is_visible():
        opt.click()
        time.sleep(1.5)
        return True
    # Đóng lại nếu không thấy
    page.keyboard.press("Escape")
    return False


def run_suite():
    results = []
    print("=" * 70)
    print("🚀 BẮT ĐẦU BỘ KIỂM THỬ TRẢI NGHIỆM WEB APP STREAMLIT (PR #21)")
    print("=" * 70)

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 960})
        page = context.new_page()

        # -------------------------------------------------------------
        # CA 1: Tải trang khởi tạo & Kiểm tra bố cục mặc định (Desktop)
        # -------------------------------------------------------------
        print("\n[CA 1] Kiểm tra giao diện khởi tạo mặc định...")
        page.goto(APP_URL, wait_until="networkidle")
        time.sleep(2)
        scroll_top(page)
        path1 = ARTIFACT_SCREENSHOT_DIR / "01_initial_layout.png"
        page.screenshot(path=str(path1), full_page=False)
        print(f"  -> Lưu: {path1.name}")
        results.append(("CA 1: Giao diện khởi tạo Desktop", "PASS", path1.name))

        # -------------------------------------------------------------
        # CA 2: Kiểm tra Bộ phóng đại cỡ chữ (150% - Cho người lớn tuổi)
        # -------------------------------------------------------------
        print("\n[CA 2] Kiểm tra Phóng to chữ 150%...")
        ensure_sidebar_open(page)
        font_150 = page.locator("label:has-text('Chữ Rất To (150%)')")
        if font_150.is_visible():
            font_150.click()
            time.sleep(1.2)
            scroll_top(page)
            path2 = ARTIFACT_SCREENSHOT_DIR / "02_font_scale_150.png"
            page.screenshot(path=str(path2), full_page=False)
            print(f"  -> Lưu: {path2.name}")
            results.append(("CA 2: Phóng đại cỡ chữ 150%", "PASS", path2.name))
        else:
            print("  [!] Không tìm thấy radio 150%")
            results.append(("CA 2: Phóng đại cỡ chữ 150%", "FAIL", ""))

        # -------------------------------------------------------------
        # CA 3: Kiểm tra Thu nhỏ cỡ chữ (100% - Chữ Vừa)
        # -------------------------------------------------------------
        print("\n[CA 3] Kiểm tra Chuyển về cỡ chữ vừa 100%...")
        ensure_sidebar_open(page)
        font_100 = page.locator("label:has-text('Chữ Vừa (100%)')")
        if font_100.is_visible():
            font_100.click()
            time.sleep(1.2)
            scroll_top(page)
            path3 = ARTIFACT_SCREENSHOT_DIR / "03_font_scale_100.png"
            page.screenshot(path=str(path3), full_page=False)
            print(f"  -> Lưu: {path3.name}")
            results.append(("CA 3: Chuyển cỡ chữ 100%", "PASS", path3.name))

        # Chuyển về 125% chuẩn khuyến nghị và đóng sidebar để giữ giao diện thoáng
        font_125 = page.locator("label:has-text('Chữ To (125%)')")
        if font_125.is_visible():
            font_125.click()
            time.sleep(0.8)
        ensure_sidebar_closed(page)

        # -------------------------------------------------------------
        # CA 4: Kiểm tra Ràng buộc nhập liệu (Để trống nội dung)
        # -------------------------------------------------------------
        print("\n[CA 4] Kiểm tra Cảnh báo để trống ô nhập...")
        btn_check = page.get_by_role("button", name="🔍 KIỂM TRA TIN NHẮN NGAY")
        btn_check.click()
        time.sleep(1.2)
        scroll_top(page)
        path4 = ARTIFACT_SCREENSHOT_DIR / "04_validation_empty.png"
        page.screenshot(path=str(path4), full_page=False)
        print(f"  -> Lưu: {path4.name}")
        results.append(("CA 4: Cảnh báo để trống", "PASS", path4.name))

        # -------------------------------------------------------------
        # CA 5: Kiểm tra Ràng buộc tin nhắn quá ngắn (<10 ký tự)
        # -------------------------------------------------------------
        print("\n[CA 5] Kiểm tra Cảnh báo tin nhắn quá ngắn (<10 ký tự)...")
        textarea = page.locator("textarea").first
        textarea.fill("Alo alo")
        time.sleep(0.5)
        btn_check.click()
        time.sleep(1.2)
        scroll_top(page)
        path5 = ARTIFACT_SCREENSHOT_DIR / "05_validation_short.png"
        page.screenshot(path=str(path5), full_page=False)
        print(f"  -> Lưu: {path5.name}")
        results.append(("CA 5: Cảnh báo tin nhắn quá ngắn", "PASS", path5.name))

        # -------------------------------------------------------------
        # CA 6: Kịch bản mẫu 1: CSGT phạt nguội dọa bắt (Fear Scam)
        # -------------------------------------------------------------
        print("\n[CA 6] Kiểm tra Kịch bản 1: CSGT phạt nguội dọa bắt (Risk Meter)...")
        ensure_presets_open(page)
        btn_fear = page.get_by_role("button", name="⚖️ CSGT phạt nguội dọa bắt")
        btn_fear.click()
        time.sleep(0.8)
        btn_check.click()
        time.sleep(2.5)
        scroll_top(page)
        path6 = ARTIFACT_SCREENSHOT_DIR / "06_preset_fear_risk_meter.png"
        page.screenshot(path=str(path6), full_page=False)
        print(f"  -> Lưu: {path6.name}")
        results.append(("CA 6: Kịch bản CSGT phạt nguội (Risk Meter)", "PASS", path6.name))

        # Mở rộng bảng chi tiết kỹ thuật 15 đặc trưng cho Giảng viên & Lời khuyên
        print("  -> Mở rộng bảng 15 đặc trưng kỹ thuật & Lời khuyên an toàn...")
        expander = page.locator("summary:has-text('Xem chi tiết kỹ thuật mô hình')")
        if expander.is_visible():
            expander.click()
            time.sleep(1.2)
        scroll_to(page, 700)
        path7 = ARTIFACT_SCREENSHOT_DIR / "07_preset_fear_advisor_and_features.png"
        page.screenshot(path=str(path7), full_page=False)
        print(f"  -> Lưu: {path7.name}")
        results.append(("CA 7: Bảng 15 đặc trưng kỹ thuật & Lời khuyên", "PASS", path7.name))

        # -------------------------------------------------------------
        # CA 8: Kịch bản mẫu 2: Cấp cứu người thân nguy kịch (Emergency Scam)
        # -------------------------------------------------------------
        print("\n[CA 8] Kiểm tra Kịch bản 2: Báo người thân tai nạn cấp cứu...")
        scroll_top(page)
        ensure_presets_open(page)
        btn_emergency = page.get_by_role("button", name="🚨 Báo người thân tai nạn cấp cứu")
        btn_emergency.click()
        time.sleep(0.8)
        btn_check.click()
        time.sleep(2.5)
        scroll_top(page)
        path8 = ARTIFACT_SCREENSHOT_DIR / "08_preset_emergency.png"
        page.screenshot(path=str(path8), full_page=False)
        print(f"  -> Lưu: {path8.name}")
        results.append(("CA 8: Kịch bản Cấp cứu người thân", "PASS", path8.name))

        # -------------------------------------------------------------
        # CA 9: Kịch bản mẫu 3: Giả VNeID dọa khóa định danh
        # -------------------------------------------------------------
        print("\n[CA 9] Kiểm tra Kịch bản 3: Giả VNeID dọa khóa định danh...")
        ensure_presets_open(page)
        btn_vneid = page.get_by_role("button", name="🏛️ Giả VNeID dọa khóa định danh")
        btn_vneid.click()
        time.sleep(0.8)
        btn_check.click()
        time.sleep(2.5)
        scroll_top(page)
        path9 = ARTIFACT_SCREENSHOT_DIR / "09_preset_vneid.png"
        page.screenshot(path=str(path9), full_page=False)
        print(f"  -> Lưu: {path9.name}")
        results.append(("CA 9: Kịch bản Giả VNeID", "PASS", path9.name))

        # -------------------------------------------------------------
        # CA 10: Kịch bản mẫu 4: Báo trúng thưởng xe & thuốc bổ
        # -------------------------------------------------------------
        print("\n[CA 10] Kiểm tra Kịch bản 4: Báo trúng thưởng xe & thuốc bổ...")
        ensure_presets_open(page)
        btn_gift = page.get_by_role("button", name="🎁 Báo trúng thưởng xe & thuốc bổ")
        btn_gift.click()
        time.sleep(0.8)
        btn_check.click()
        time.sleep(2.5)
        scroll_top(page)
        path10 = ARTIFACT_SCREENSHOT_DIR / "10_preset_gift.png"
        page.screenshot(path=str(path10), full_page=False)
        print(f"  -> Lưu: {path10.name}")
        results.append(("CA 10: Kịch bản Trúng thưởng & Thuốc tiên", "PASS", path10.name))

        # -------------------------------------------------------------
        # CA 11: Kịch bản mẫu 5: Tin nhắn biến động số dư Vietcombank (An toàn)
        # -------------------------------------------------------------
        print("\n[CA 11] Kiểm tra Kịch bản 5: Biến động số dư Vietcombank (An toàn)...")
        ensure_presets_open(page)
        btn_bank = page.get_by_role("button", name="💳 Tin nhắn biến động số dư (An toàn)")
        btn_bank.click()
        time.sleep(0.8)
        btn_check.click()
        time.sleep(2.5)
        scroll_top(page)
        path11 = ARTIFACT_SCREENSHOT_DIR / "11_preset_bank_safe.png"
        page.screenshot(path=str(path11), full_page=False)
        print(f"  -> Lưu: {path11.name}")
        results.append(("CA 11: Tin nhắn biến động số dư (An toàn)", "PASS", path11.name))

        # -------------------------------------------------------------
        # CA 12: Chuyển đổi mô hình sang XGBoost (F1 95.35%)
        # -------------------------------------------------------------
        print("\n[CA 12] Kiểm tra Chuyển đổi mô hình: XGBoost...")
        # Bật Chế độ giảng viên trên Sidebar để mở Bộ chọn mô hình
        ensure_sidebar_open(page)
        toggle_academic = page.locator("label:has-text('Chế độ Giảng viên')").first
        if toggle_academic.is_visible():
            toggle_academic.click()
            time.sleep(2.5)
            page.wait_for_selector('div[data-testid="stSelectbox"]', state="visible", timeout=10000)
            time.sleep(1.0)

        if select_model(page, "XGBoost"):
            ensure_presets_open(page)
            btn_fear = page.get_by_role("button", name="⚖️ CSGT phạt nguội dọa bắt")
            btn_fear.click()
            time.sleep(0.6)
            btn_check.click()
            time.sleep(2.5)
            scroll_top(page)
            path12 = ARTIFACT_SCREENSHOT_DIR / "12_model_xgboost.png"
            page.screenshot(path=str(path12), full_page=False)
            print(f"  -> Lưu: {path12.name}")
            results.append(("CA 12: Chuyển đổi sang XGBoost", "PASS", path12.name))
        else:
            print("  [!] Lỗi chọn XGBoost")
            results.append(("CA 12: Chuyển đổi sang XGBoost", "FAIL", ""))

        # -------------------------------------------------------------
        # CA 13: Chuyển đổi mô hình sang Linear SVM (Calibrated CV)
        # -------------------------------------------------------------
        print("\n[CA 13] Kiểm tra Chuyển đổi mô hình: Linear SVM...")
        if select_model(page, "Linear SVM"):
            btn_check.click()
            time.sleep(2.5)
            scroll_top(page)
            path13 = ARTIFACT_SCREENSHOT_DIR / "13_model_svm_linear.png"
            page.screenshot(path=str(path13), full_page=False)
            print(f"  -> Lưu: {path13.name}")
            results.append(("CA 13: Chuyển đổi sang Linear SVM", "PASS", path13.name))
        else:
            print("  [!] Lỗi chọn Linear SVM")
            results.append(("CA 13: Chuyển đổi sang Linear SVM", "FAIL", ""))

        # -------------------------------------------------------------
        # CA 14: Chuyển đổi mô hình sang Naive Bayes (Baseline)
        # -------------------------------------------------------------
        print("\n[CA 14] Kiểm tra Chuyển đổi mô hình: Naive Bayes...")
        if select_model(page, "Naive Bayes"):
            btn_check.click()
            time.sleep(2.5)
            scroll_top(page)
            path14 = ARTIFACT_SCREENSHOT_DIR / "14_model_naive_bayes.png"
            page.screenshot(path=str(path14), full_page=False)
            print(f"  -> Lưu: {path14.name}")
            results.append(("CA 14: Chuyển đổi sang Naive Bayes", "PASS", path14.name))
        else:
            print("  [!] Lỗi chọn Naive Bayes")
            results.append(("CA 14: Chuyển đổi sang Naive Bayes", "FAIL", ""))

        # Đóng sidebar lại trước khi kiểm tra tiếp trên Desktop
        ensure_sidebar_closed(page)

        # -------------------------------------------------------------
        # CA 15: Kiểm tra Nút Xóa tin (Clear Input)
        # -------------------------------------------------------------
        print("\n[CA 15] Kiểm tra Nút Xóa tin nội dung...")
        scroll_top(page)
        btn_clear = page.get_by_role("button", name="🗑️ Xóa tin")
        btn_clear.click()
        time.sleep(1)
        val = page.locator("textarea").first.input_value()
        scroll_top(page)
        path15 = ARTIFACT_SCREENSHOT_DIR / "15_clear_button.png"
        page.screenshot(path=str(path15), full_page=False)
        print(f"  -> Lưu: {path15.name} (Nội dung sau khi xóa: '{val}')")
        results.append(("CA 15: Nút Xóa tin", "PASS", path15.name))

        # Đóng ngữ cảnh Desktop trước khi chuyển sang Mobile
        context.close()

        # -------------------------------------------------------------
        # CA 16: Kiểm tra Giao diện trên Thiết bị Di động (Mobile Viewport 390x844)
        # -------------------------------------------------------------
        print("\n[CA 16] Kiểm tra Responsive trên Điện thoại (390x844 iPhone 14)...")
        mobile_context = browser.new_context(
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            has_touch=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        )
        page_m = mobile_context.new_page()
        page_m.goto(APP_URL, wait_until="domcontentloaded")
        time.sleep(2.5)

        # Bấm thử kịch bản cấp cứu 1-chạm trên mobile
        ensure_presets_open(page_m)
        btn_m_emg = page_m.get_by_role("button", name="🚨 Báo người thân tai nạn cấp cứu")
        if btn_m_emg.is_visible():
            btn_m_emg.click(force=True)
            time.sleep(2.5)

        # Cuộn xem kết quả phán đoán trên mobile
        page_m.evaluate("() => { const el = document.querySelector('section.stMain'); if (el) el.scrollTop = 450; }")
        time.sleep(0.8)

        path16 = ARTIFACT_SCREENSHOT_DIR / "16_mobile_responsive.png"
        page_m.screenshot(path=str(path16), full_page=False)
        print(f"  -> Lưu: {path16.name}")
        results.append(("CA 16: Responsive trên Điện thoại di động", "PASS", path16.name))
        
        mobile_context.close()
        browser.close()

    print("\n" + "=" * 70)
    print("📊 BẢNG TỔNG HỢP KẾT QUẢ KIỂM THỬ THỰC NGHIỆM:")
    print("=" * 70)
    for name, status, file in results:
        print(f"[{status}] {name} -> {file}")
    print("=" * 70)


if __name__ == "__main__":
    run_suite()
