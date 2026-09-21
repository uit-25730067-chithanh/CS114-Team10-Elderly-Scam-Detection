# Research & Audit Report: CS114 Final Phase 09 Defense Presentation Deck (20 Slides)
## Formal Academic & Technical Hard Review for Bùi Thị Mỷ Cẩm (PPT Lead)

- **Course:** CS114 — Machine Learning (Máy học) — UIT ĐHQG-HCM
- **Instructor:** ThS. Cáp Phạm Đình Thăng
- **Project:** Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam (Elderly Scam Detection)
- **Reviewer:** Đặng Chí Thanh (MSSV: 25730067 — Project Manager / Reviewer)
- **Author of Artifact:** Bùi Thị Mỷ Cẩm (MSSV: 25730013 — PPT Template & Modeling Lead)
- **Date:** 21/09/2026
- **Branch:** `feat/phase-09-ppt-template` (HEAD: `d54df44`)
- **Scope:** Thẩm định chất lượng slide thuyết trình 15 phút, tính chân thực của số liệu, bố cục trực quan, speaker notes, giải quyết 4 vấn đề bàn giao, chuẩn bị 10 câu hỏi Q&A phản biện học thuật trước ThS. Cáp Phạm Đình Thăng.

---

## 1. Kết Quả Thẩm Định & Điểm Số (Audit Scorecard)

- **Điểm tổng kết:** **88/100 (Hạng A-)**
- **Đánh giá nỗ lực:** Cẩm đã hoàn thành một khối lượng công việc xuất sắc khi tự động hóa 100% quá trình dựng slide bằng script `generate_slides.js` (PptxGenJS), khắc phục thành công lỗi hiển thị font dấu tiếng Việt (chuyển sang Cambria/Calibri), tuân thủ nguyên tắc không hard-code số liệu mà đọc từ `models/*_metrics.json`, giữ đúng tỷ lệ hình ảnh 300 DPI, và bổ sung speaker notes cho toàn bộ 20 slide.
- **Yêu cầu nâng cấp lên 98/100 (A+):** Cần dứt điểm 4 vấn đề bàn giao (chuẩn hóa RF ROC-AUC thành 99.77%, fix bug Naive Bayes alpha=0.01, gỡ bỏ citation giả [4]), thêm nhận diện UIT ở Cover slide, và siết chặt kịch bản thời gian để không cháy giáo án 15 phút.

---

## 2. Giải Quyết Dứt Điểm 4 Vấn Đề Bàn Giao

| # | Vấn đề bàn giao | Hiện trạng kiểm toán | Quyết định dứt điểm của PM |
|:---:|---|---|---|
| **1** | **ROC-AUC của Random Forest** (99.76% vs 99.77%) | Đánh giá lại model artifact `random_forest.pkl` trên test set thực tế cho kết quả chính xác `0.99765258...` → làm tròn 4 chữ số là **0.9977 (99.77%)**. Biểu đồ ROC curve và `model_comparison.csv` đều ghi 99.77%. | **Chốt 99.77%**. Cập nhật `random_forest_metrics.json` test_metrics roc_auc thành `0.9976525821596244`. Slide 9 sẽ tự động hiển thị 99.77%, khớp 100% với Slide 10. |
| **2** | **Naive Bayes alpha=0.5 vs 0.01 & Tác giả Phase 04** | `metrics_calculator.py` dòng 44–45 gõ cứng sai `alpha=0.5` và `Phase 04 — Thanh`. Giá trị tối ưu thực tế từ GridSearchCV là `alpha=0.01`, do Cẩm thực hiện ở Phase 04. | **Sửa ngay 4 nơi:** `metrics_calculator.py`, `model_comparison.csv`, `README.md`, và `demo/app.py` thành `alpha=0.01` và ghi nhận công trạng `(Phase 04 — Cẩm)`. |
| **3** | **Tài liệu [4] "IEEE Access 2026 (doi pending)"** | Không tồn tại bài báo này; đây là placeholder. Vi phạm nghiêm trọng liêm chính học thuật nếu để vào slide bảo vệ trước Thầy Thăng. | **Xóa bỏ trích dẫn giả**. Thay bằng trích dẫn dataset thực tế của đồ án kèm repo GitHub hoặc Báo cáo tình hình lừa đảo mạng của Cục ATTT. |
| **4** | **Hiệu ứng chuyển slide (Transitions)** | Script XML injection gây nguy cơ corrupt file trên một số phiên bản PowerPoint. | **Giữ slide nguyên bản**, không hack XML. Khi trình chiếu qua MS Teams chỉ cần bật hiệu ứng Fade nhẹ 0.3s trên PowerPoint native. |

---

## 3. Chiến Thuật Phân Bổ Thời Gian 15 Phút & Kịch Bản Phân Vai

- **Giới hạn thời gian:** Nghiêm ngặt **15 phút** cho cả nhóm 3 người.
- **Kịch bản điều phối:**
  - **Khối 1 (Slide 1–7): Đặng Chí Thanh** — 4 phút 30 giây.
    *Tập trung:* Câu hỏi mở đầu, 3 số liệu ấn tượng (2.193 mẫu, 4 nhóm bẫy, 0% AI text), 68% bẫy quyền lực/dịch vụ công, quy tắc Zero-Leakage. Không đọc lan man chi tiết kỹ thuật từng dòng code.
  - **Khối 2 (Slide 8–11): Bùi Thị Mỷ Cẩm** — 5 phút 00 giây.
    *Tập trung:* Bảng so sánh 4 mô hình (XGBoost F1=95.35%, Recall=97.62%, chỉ bỏ sót 2/84 tin lừa đảo), phân tích Precision-Recall curves do dữ liệu mất cân bằng 4.2:1, và giải thích SHAP Beeswarm minh bạch.
  - **Khối 3 (Slide 12–16): Hoàng Cao Sơn** — 4 phút 30 giây.
    *Tập trung:* 60 giây live demo / screenshot Web app Streamlit, các tính năng trợ năng cho người già (font 150%, hotline 156/113), hướng phát triển PhoBERT/Voice scam, cảm ơn và mở màn Q&A.
  - **Phụ lục (Slide 17–20): Cả nhóm phối hợp** — Dành cho phần hỏi đáp phản biện với ThS. Cáp Phạm Đình Thăng.

---

## 4. Danh Mục 10 Câu Hỏi Phản Biện Sát Sườn Của GV & Câu Trả Lời Mẫu

1. **Tại sao không dùng PhoBERT làm mô hình chính?** → *Latency <15ms so với >300ms; giải thích SHAP minh bạch; mô hình dạng cây kiểm soát quá khớp tốt hơn với 2.193 mẫu.*
2. **Tại sao dùng scale_pos_weight=4.22 thay vì SMOTE?** → *Giữ nguyên tắc Zero Synthetic Text 100% đời thực; SMOTE tạo vector giả vô nghĩa trong không gian thưa; scale_pos_weight phạt trực tiếp hàm mất mát.*
3. **Tại sao Naive Bayes không dùng 15 đặc trưng phụ?** → *MultinomialNB yêu cầu giá trị đầu vào không âm; 15 đặc trưng phụ qua StandardScaler có giá trị âm nên không tương thích.*
4. **CalibratedClassifierCV của SVM hoạt động ra sao?** → *LinearSVC chỉ có decision_function (khoảng cách), Platt Scaling hồi quy Logistic qua 5-fold CV chuyển thành xác suất [0, 1] chuẩn mực.*
5. **Có rò rỉ dữ liệu (data leakage) giữa TF-IDF và 15 đặc trưng không?** → *Không, chia Stratified 80/20 trước; fit() chỉ trên Train, transform() trên Train/Test.*
6. **Test set 84 mẫu lừa đảo có đủ tin cậy thống kê không?** → *Nhóm thừa nhận hạn chế mẫu; bù lại đã kiểm chứng qua 5-fold Cross-Validation trên 1.754 mẫu Train (CV F1 = 0.9603).*
7. **160 quy tắc teencode có bị bias không?** → *Tinh lọc từ benchmark NLP chuẩn và dữ liệu thực tế; kết hợp đặc trưng has_leet_speak cho ML tự học.*
8. **Từ 'money' trong SHAP Beeswarm là gì?** → *Là token chuẩn hóa regex cho mọi số tiền (ví dụ 50.000.000đ → money), không phải từ tiếng Anh.*
9. **Khoảng cách Train F1 (1.0) và Val F1 (0.95) có phải overfit không?** → *Overfit nhẹ đặc thù của cây trên 5.015 chiều; nhưng Val F1 vẫn liên tục dốc lên theo số mẫu và sát với Test F1 (0.9535).*
10. **Làm sao đảm bảo tính đạo đức và bảo mật dữ liệu (PII)?** → *Khử PII 100% (ẩn danh hóa số điện thoại, tài khoản); 100% tin lừa đảo lấy từ nguồn báo chí cảnh báo công khai có ảnh chụp bằng chứng.*

---

## 5. Chỉ Đạo Bổ Sung Của Trưởng Nhóm (Anh Thanh) Giao Cho Em Cẩm Hoàn Thiện

Sau khi xem xét toàn bộ các file và slide thực tế, Trưởng nhóm Đặng Chí Thanh đã đưa ra 5 chỉ đạo cốt lõi và 2 định hướng quan trọng để em Cẩm chủ động cập nhật vào `generate_slides.js`:

1. **Bổ sung Header, Footer & Đánh số trang (`X / N`):**
   - Header: `TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN — ĐHQG-HCM`
   - Footer: `CS114: Máy học — Nhóm 10 — Báo cáo Đồ án: Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam`
   - Page counter: `01 / 22`, `02 / 22`... ở góc dưới phải.
2. **Thống nhất 100% Tên đề tài chính thức:**
   - *"Nghiên cứu và Xây dựng Hệ thống Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam"* (chống tam sao thất bản).
3. **Thêm Slide Lộ trình báo cáo (Agenda — Slide 2):**
   - Bố trí 2 cột gồm 5 phần chính + Phụ lục Q&A; đánh số phân đoạn rõ ràng (`PHẦN 1` đến `PHẦN 5`).
4. **Sắp xếp Tài liệu tham khảo theo vòng đời dự án (Slide 17):**
   - Trật tự: Nguồn cào data thực tế → Tiền xử lý NLP → Thuật toán ML → XAI (SHAP) → Trợ năng Web (Streamlit/WCAG) → Deep Learning tương lai (PhoBERT).
5. **Chuẩn hóa Lời cảm ơn:**
   - `"CHÂN THÀNH CẢM ƠN THẦY VÀ CÁC BẠN ĐÃ LẮNG NGHE BÁO CÁO!"`
6. **Định hướng Kịch bản & Hiệu ứng Slide:**
   - *Transition:* Hoàn thiện sau cùng khi toàn bộ nội dung đã ổn định.
   - *Slide vs Script:* Slide là điểm tựa thị giác (visual anchor) bổ sung góc nhìn và số liệu cho kịch bản nói; không cần cắt gọt quá ngắn gọn gây thiếu hụt luận cứ khoa học.

---

*Báo cáo thẩm định chuyên môn nội bộ — CS114.F31.CN2.TTNT — Nhóm 10.*

