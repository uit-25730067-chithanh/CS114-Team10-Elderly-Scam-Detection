# Research Report: Elderly Scam Detection Web Application, Accessibility UX Design & Multi-Model Inference Engine (Phase 08)

- **Course:** CS114 — Machine Learning (Máy học), UIT ĐHQG-HCM
- **Project:** Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam
- **Author:** Hoàng Cao Sơn (MSSV: 25730061 — Lead Data Collection & Demo UI) & Đặng Chí Thanh (MSSV: 25730067 — Trưởng nhóm / PM)
- **Date:** 20/09/2026
- **Scope:** Báo cáo kiểm toán kỹ thuật và nghiệm thu thực nghiệm Phase 08 (Demo UI); Thẩm định kiến trúc Split-View Workbench; Đánh giá trợ năng người cao tuổi (Elderly Accessibility Standards); Chuẩn hóa bộ điều phối đa mô hình (Model Catalog); Phân tích 15 đặc trưng tâm lý thời gian thực; Nghiệm thu bộ kiểm thử tự động Playwright E2E trên trình duyệt Google Chrome.

---

## Executive Summary

Trong khuôn khổ Sprint 2–3 của đồ án cuối kỳ môn CS114, thành viên Hoàng Cao Sơn (với sự hỗ trợ kiểm định của Đặng Chí Thanh) đã hoàn thành toàn diện **Phase 08 — Demo UI (Streamlit Web Application)**:
1. **Kiến trúc Split-View Workbench:** Phân tách rõ ràng hai luồng tương tác (Cột trái: Nhập liệu tin nhắn, kịch bản mẫu một-chạm, dán tự động qua Web Clipboard API; Cột phải: Kết quả chẩn đoán AI, thanh đo nguy cơ trực quan, bôi đỏ từ khóa nhạy cảm, khuyến cáo an toàn "3 KHÔNG & 1 GỌI", và bảng 15 đặc trưng kỹ thuật thời gian thực).
2. **Trợ năng chuyên biệt cho Người cao tuổi (Elderly UX):** Tích hợp bộ phóng đại cỡ chữ (100% – 125% – 150%) với tương phản cao (contrast ratio ≥ 4.5:1), hỗ trợ hotline khẩn cấp một-chạm (`tel:156`, `tel:113`), cơ chế tự động cuộn trang (auto-scroll) đến khối kết quả sau phân tích, và tối ưu hiển thị Mobile Responsive (360px – 450px).
3. **Bộ điều phối Đa mô hình (Model Catalog):** Cho phép chuyển đổi linh hoạt giữa 4 mô hình học máy đã huấn luyện: **XGBoost (Mặc định — F1=0.9535, Recall=97.62%)**, **Linear SVM (F1=0.9474, ROC-AUC=0.9986)**, **Random Forest (F1=0.9425)**, và **Naive Bayes (F1=0.8864)**.
4. **Kiểm thử tự động toàn diện:** Đạt 100% PASS trên bộ kiểm thử tự động E2E qua Playwright (`run_full_web_test_suite.py` với 16 ca kiểm thử giao diện & chức năng) và 70/70 unit tests `pytest` trong 11.37s.

---

## 1. Bối cảnh Bài toán & Nguyên tắc Thiết kế Trợ năng cho Người cao tuổi

Người cao tuổi tại Việt Nam khi tiếp cận điện thoại thông minh thường đối mặt với các rào cản nhận thức và sinh lý:
- **Thị lực suy giảm:** Khó đọc các font chữ nhỏ (< 16px), dễ nhầm lẫn các sắc thái màu sắc tương tự nhau.
- **Thao tác vận động chậm:** Vùng chạm (tap target) nhỏ trên màn hình cảm ứng dễ gây bấm nhầm.
- **Tâm lý lo âu khi bị đe dọa:** Khi nhận tin nhắn giả danh Công an hoặc cấp cứu, người cao tuổi dễ hoảng loạn và vội vã chuyển tiền.

Dựa trên các nghiên cứu về Human-Computer Interaction (HCI) và Tiêu chuẩn Trợ năng Web (WCAG 2.1 AA), ứng dụng được thiết kế theo 4 nguyên lý:

| Tiêu chuẩn trợ năng | Hiện thực hóa trong Demo UI | Ý nghĩa thực tế |
|---|---|---|
| **Dynamic Font Scaling** | Bộ chọn 3 mức: 100% (Mặc định), 125% (Rõ ràng), 150% (Rất lớn) | Cho phép người cao tuổi tự do phóng to chữ mà không làm vỡ bố cục giao diện |
| **Color Contrast & Luminance** | Nền trắng `#ffffff`, chữ đen xám `#1e293b`, thẻ cảnh báo đỏ tươi `#dc2626` | Đạt tỷ lệ tương phản vượt chuẩn 4.5:1, phân biệt rõ xanh lá (an toàn) và đỏ (lừa đảo) |
| **Large Touch Targets** | Nút bấm có padding tối thiểu 12px, font-size 18px, hotline dạng thẻ bấm | Giảm thiểu tối đa lỗi trượt tay trên màn hình cảm ứng điện thoại |
| **Instant Actionable Advice** | Hộp thoại "3 KHÔNG & 1 GỌI" hiển thị ngay trên cùng kết quả | Hướng dẫn hành vi tức thời trước khi người cao tuổi đọc chi tiết kỹ thuật |

---

## 2. Kiến trúc Hệ thống Split-View Workbench & Luồng Dữ liệu

Ứng dụng được xây dựng tại `draft/scam-detection/demo/` với cấu trúc module hóa cao:

```
draft/scam-detection/demo/
├── app.py                         ← Module chính điều phối giao diện Streamlit
├── Chay_Demo.bat                  ← Script khởi chạy một-chạm trên Windows
├── assets/
│   └── elderly_check_sms.jpg      ← Hình ảnh minh họa thân thiện (815 KB)
└── components/
    ├── __init__.py
    ├── risk_meter.py              ← Thanh đo mức độ nguy cơ 3 cấp độ (Xanh/Vàng/Đỏ)
    ├── keyword_highlighter.py     ← Bôi đỏ/vàng từ khóa cảnh báo bằng regex biên dịch trước
    └── safety_advisor.py          ← Chẩn đoán 4 bẫy tâm lý, hotline 1-chạm & quy tắc an toàn
```

### Luồng xử lý dữ liệu đầu cuối (End-to-End Inference Pipeline):

1. **Thu nhận đầu vào:** Người dùng dán tin nhắn qua Web Clipboard API hoặc nhập thủ công / chọn 5 presets mẫu.
2. **Chuẩn hóa & Tiền xử lý (Phase 02):** Gọi `clean_text()` (Unicode NFC, hạ âm, gỡ teencode/leet-speak) và `segment_vietnamese()` (`pyvi`).
3. **Trích xuất 15 đặc trưng phụ:** Đếm số điện thoại, URL, từ ngữ khẩn cấp, từ khóa quyền lực, tỷ lệ viết hoa... và chuẩn hóa qua `aux_scaler`.
4. **Vector hóa TF-IDF:** Transform văn bản qua `tfidf_vectorizer` (5.000 đặc trưng N-gram 1-2).
5. **Hợp nhất không gian 5.015 chiều:** Kết hợp ma trận thưa CSR (`scipy.sparse.hstack`).
6. **Dự đoán xác suất:** Gọi `predict_proba()` từ mô hình được chọn trong Model Catalog.
7. **Hiển thị đa chiều:** Cập nhật Risk Meter, bôi màu từ khóa, kích hoạt lời khuyên an toàn, lưu trạng thái vào URL query params (`?text=...`).

---

## 3. Bộ Điều Phối Đa Mô Hình (Model Catalog)

Nhằm phục vụ tốt nhất cho buổi bảo vệ đồ án trước Giảng viên, ứng dụng không chỉ đóng gói một mô hình đơn lẻ mà tích hợp cả 4 kiến trúc đã nghiên cứu:

| Thứ tự Catalog | Mô hình | Kỹ thuật & Hyperparameters | F1-Score | Recall (Scam) | ROC-AUC | Vai trò trong Demo |
|:---:|---|---|:---:|:---:|:---:|---|
| **1 (Default)** | **XGBoost** | `depth=5, lr=0.05, subsample=0.7, scale_pos_weight=4.22` | **0.9535** | **97.62%** | **0.9984** | **Mô hình khuyến nghị cao nhất**, sai số cực thấp (FN=2) |
| 2 | **Linear SVM** | `C=10.0`, CalibratedClassifierCV 5-fold | 0.9474 | 96.43% | **0.9986** | Mô hình phân tách tuyến tính tối ưu, AUC cao nhất |
| 3 | **Random Forest** | `n_est=200, depth=50, leaf=2, max_feat=0.2` | 0.9425 | 97.62% | 0.9976 | Cây quyết định bagging của Hoàng Cao Sơn |
| 4 | **Naive Bayes** | `MultinomialNB(alpha=0.01)`, 5.000 TF-IDF dims | 0.8864 | 92.86% | 0.9911 | Mô hình baseline đối chứng |

---

## 4. Kiểm Thử Tự Động & Thẩm Định Chất Lượng Mã Nguồn

### 4.1. Bộ kiểm thử E2E Playwright (`run_full_web_test_suite.py`)
Bộ kiểm thử tự động khởi chạy Google Chrome thực tế và kiểm tra toàn bộ 16 ca thực nghiệm:
- **CA 1–3:** Kiểm tra nạp giao diện, chuyển đổi cỡ chữ 100% → 150% → 100%.
- **CA 4–5:** Kiểm tra bắt lỗi nhập liệu (chuỗi rỗng, chuỗi quá ngắn < 5 ký tự).
- **CA 6–10:** Kiểm thử suy luận trên 5 kịch bản mẫu (Đe dọa quyền lực, Cấp cứu gia đình, Dịch vụ công VNeID, Tri ân trúng thưởng, và Tin nhắn ngân hàng an toàn).
- **CA 11–14:** Kiểm tra chuyển đổi mượt mà giữa cả 4 mô hình trong Catalog.
- **CA 15:** Kiểm tra nút xóa trắng (Clear input).
- **CA 16:** Kiểm tra giao diện co dãn trên màn hình điện thoại di động (Viewport: 390 × 844 px).

**Kết quả:** 16/16 ca kiểm thử đạt **PASS 100%**. 21 ảnh chụp nghiệm thu màn hình độ phân giải cao được ghi nhận.

### 4.2. Khắc phục phản hồi từ Gemini Code Review
- **HTML Injection / XSS Sanitization:** Đã bọc `html.escape()` cho chuỗi văn bản đầu vào trước khi thực hiện regex bôi màu trong `keyword_highlighter.py`.
- **Hiệu năng Render Regex:** Biên dịch trước toàn bộ `COMPILED_PATTERNS` giúp tốc độ bôi đỏ dưới 10ms.
- **Hotline tương thích di động:** Đã cấu hình các thẻ liên kết `tel:156` và `tel:113` với màu sắc tương phản cao, hỗ trợ bấm gọi ngay trên smartphone.
- **Bảo lưu trạng thái:** Bổ sung đồng bộ URL query params (`?text=...`) giúp người dùng không bị mất kết quả khi tải lại trang.

---

## 5. Bảng Đối Soát Tiêu Chí Nghiệm Thu (Acceptance Parity)

| Tiêu chí nghiệm thu | Yêu cầu gốc | Kết quả thực tế | Đánh giá |
|---|---|---|:---:|
| Khởi chạy ứng dụng | `streamlit run demo/app.py` không lỗi | Khởi chạy mượt mà trên localhost, có script `Chay_Demo.bat` | ✅ Đạt 100% |
| Tích hợp mô hình | Tích hợp Best Model | Tích hợp cả 4 mô hình, XGBoost mặc định | ✅ Vượt chỉ tiêu |
| Giao diện người cao tuổi | Cỡ chữ to, tương phản cao | Phóng đại 100%-125%-150%, hotline 1-chạm, 3 KHÔNG 1 GỌI | ✅ Đạt 100% |
| Ảnh chụp báo cáo | ≥3 ảnh chụp trong `reports/figures/` | Đã xuất 4 ảnh chuẩn 300 DPI (`demo_01` → `demo_04`) | ✅ Đạt 100% |
| Bộ test tự động | Test suite chạy pass | 70/70 pytest pass, 16/16 Playwright E2E pass | ✅ Đạt 100% |

---

## Kết Luận

Phase 08 — Demo UI do thành viên **Hoàng Cao Sơn** chủ trì đã hoàn thành xuất sắc, vượt mọi chỉ tiêu kỹ thuật và thẩm mỹ của đề tài CS114. Sản phẩm sẵn sàng 100% phục vụ cho việc trình chiếu trực tiếp trong buổi bảo vệ trực tuyến MS Teams vào ngày 23/09/2026.
