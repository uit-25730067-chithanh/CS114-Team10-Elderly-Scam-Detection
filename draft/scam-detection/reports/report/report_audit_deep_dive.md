# BÁO CÁO KIỂM ĐỊNH CHUYÊN SÂU BÁO CÁO ĐỒ ÁN FINAL CS114
## Đề tài: Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam
**Môn học:** CS114 — Máy học | **GVHD:** ThS. Cáp Phạm Đình Thăng  
**Tập thể thực hiện:** Nhóm 10 (Đặng Chí Thanh - 25730067, Bùi Thị Mỷ Cẩm - 25730013, Hoàng Cao Sơn - 25730061)  
**Tệp kiểm tra:**
- `report-source.md` (`draft/scam-detection/reports/report/report-source.md`)
- `report.docx` (`draft/scam-detection/reports/report/report.docx`)
- `report.pdf` (`draft/scam-detection/reports/report/report.pdf`)
- `generate_academic_report.py` (`draft/scam-detection/reports/report/generate_academic_report.py`)
- Thư mục hình ảnh: `draft/scam-detection/reports/figures/` (35 tệp ảnh @ 300 DPI)

---

## Executive Summary (Tóm tắt cốt lõi)

Báo cáo hiện tại (`report.docx` / `report.pdf` 32 trang và `report-source.md` 610 dòng) đã có nền tảng học thuật rất tốt: bao phủ đầy đủ 2 thực nghiệm đối chứng (Ablation Studies), phân tích ca biên ngoại vi theo chỉ đạo Buổi 8 của ThS. Cáp Phạm Đình Thăng, và đạt 100% tiêu chí OpenXML theo `audit_docx_xml.py`.

Tuy nhiên, **BẢN BÁO CÁO HIỆN TẠI CHƯA ĐỦ ĐIỀU KIỆN ĐỂ NỘP** do tồn tại **8 lỗi kỹ thuật & phương pháp luận nghiêm trọng**:
1. **Lệch pha số trang Mục lục (TOC Desynchronization):** Toàn bộ số trang trong Mục lục từ Chương 3 đến Tài liệu tham khảo bị lệch từ 1 đến 2 trang so với vị trí thực tế trong file Word/PDF (Mục lục ghi Trang 14 là Chương 4, thực tế Trang 14 là Mục 3.5; Tài liệu tham khảo ghi Trang 30, thực tế là Trang 32).
2. **Sai thông tin đơn vị quản lý trên Trang bìa:** Ghi *"KHOA HỆ THỐNG THÔNG TIN — BỘ MÔN TRÍ TUỆ NHÂN TẠO"* trong khi CS114 và Bộ môn TTNT thuộc **Khoa Khoa học Máy tính**.
3. **Mất đồng bộ kép (Dual Desynchronization) giữa Markdown và Script sinh Word:** `generate_academic_report.py` không đọc `report-source.md` mà hardcode văn bản độc lập, dẫn đến việc Bảng 3.1 trong Word bị cắt xén mất số liệu thống kê (Mean Scam vs Normal), thiếu công thức hàm mất mát Cost-Sensitive và thiếu công thức TF-IDF.
4. **Tỷ lệ sử dụng hình ảnh quá thấp (Chỉ 12/35 hình được đưa vào báo cáo — 34%):** Kho 35 hình ảnh 300 DPI rất công phu bị bỏ sót 23 hình, trong đó bỏ sót 4 biểu đồ EDA cốt lõi (dù văn bản tuyên bố thực hiện 7 biểu đồ EDA), bỏ sót hình ảnh minh chứng trợ năng người già của Web Demo, và không có biểu đồ Feature Importance của từng mô hình.
5. **Thiếu Bảng phân công nhiệm vụ & Tỷ lệ đóng góp nhóm:** Bắt buộc phải có để giảng viên chấm điểm cá nhân cho 3 thành viên theo quy chế môn học UIT.
6. **Cấu trúc Chương 4 chưa khớp 100% đề cương của Thầy Thăng:** Mục *"Phương pháp đánh giá là gì"* bị hạ cấp thành tiểu mục 4.2.0 thay vì là mục lớn 4.2 độc lập.
7. **Lỗi dàn trang, ngắt bảng biểu và khoảng trắng mồ côi:** Bảng 4.3 (Top 20 SHAP) bị gãy đôi qua trang, một số trang có mật độ chữ dưới 950 ký tự do lạm dụng ngắt trang cứng.
8. **Thiếu lý giải toán học cho mô hình Linear SVM trong Ablation 2:** Chưa giải thích tại sao khi thêm 15 đặc trưng phụ, F1 của SVM giảm nhẹ từ 0.9697 xuống 0.9474 trong khi XGBoost tăng.

---

## PHẦN I: GIẢI MÃ NGUYÊN NHÂN TẠI SAO `figures/` CÓ NHIỀU HÌNH NHƯNG DÙNG QUÁ ÍT

Trong thư mục `draft/scam-detection/reports/figures/` có tổng cộng **35 tệp hình ảnh PNG độ phân giải cao (300 DPI)**. Tuy nhiên trong `report.docx` và `report-source.md` chỉ xuất hiện **12 hình ảnh** (tỷ lệ sử dụng chỉ đạt **34.3%**). Dưới đây là bảng kiểm kê chi tiết 35 hình ảnh và nguyên nhân chưa được đưa vào:

| Nhóm | Tệp hình ảnh trong `figures/` | Trạng thái trong Báo cáo | Phân tích nguyên nhân & Đánh giá mức độ thiếu sót |
|---|---|:---:|---|
| **Kiến trúc** | `system_io_flowchart.png` | ✅ Dùng (Hình 3.1) | Sơ đồ luồng I/O hệ thống (bị co nhỏ xuống 2.2 inch trên Word làm chữ hơi bé). |
| **EDA (7 hình)** | `label_distribution.png` | ✅ Dùng (Hình 4.1) | Phân bố nhãn và tỷ lệ mất cân bằng 4.22 : 1. |
| | `scam_category_distribution.png` | ✅ Dùng (Hình 4.2) | Cơ cấu 4 nhóm bẫy tâm lý lừa đảo. |
| | `auxiliary_correlation_heatmap.png` | ✅ Dùng (Hình 4.3) | Ma trận tương quan Pearson 15 đặc trưng phụ. |
| | `text_length_comparison.png` | ❌ **BỎ SÓT** | **Thiếu sót nặng:** So sánh độ dài ký tự và số từ giữa lừa đảo (140.8 ký tự) vs bình thường (232.9 ký tự). Văn bản ghi "thực hiện 7 biểu đồ EDA" nhưng không đưa hình này vào! |
| | `wordcloud_scam_vs_normal.png` | ❌ **BỎ SÓT** | **Thiếu sót nặng:** Đám mây từ vựng trực quan hóa đối kháng từ vựng lừa đảo (*công an, viện kiểm sát, chuyển khoản*) vs tin thường. Hình ảnh này cực kỳ trực quan và giá trị cho bài báo cáo học thuật. |
| | `top_ngrams_scam_vs_normal.png` | ❌ **BỎ SÓT** | **Thiếu sót nặng:** Top-20 N-grams có độ phân tách mạnh nhất; là bằng chứng thực nghiệm giải thích tại sao TF-IDF phải dùng N-gram (1, 2) để bắt `bộ_công_an`, `viện_kiểm_sát`. |
| | `source_distribution.png` | ❌ **BỎ SÓT** | Biểu đồ nguồn dữ liệu thực tế (IEEE Access, Báo chí, Vault). |
| **Đơn mô hình NB (3 hình)** | `nb_confusion_matrix.png`<br>`nb_roc_curve.png`<br>`nb_learning_curve.png` | ⚠️ Thay thế | Đã được gom vào 4 biểu đồ lưới 2×2 ở Mục 4.2. Hợp lý để tránh loãng báo cáo, nhưng có thể đưa vào Phụ lục. |
| **Đơn mô hình RF (4 hình)** | `rf_confusion_matrix.png`<br>`rf_roc_curve.png`<br>`rf_learning_curve.png`<br>`rf_feature_importance.png` | ⚠️ Thay thế / ❌ Bỏ sót | 3 hình đầu đã gom vào lưới 2×2. Riêng `rf_feature_importance.png` (Gini Importance của Random Forest) bị **bỏ sót hoàn toàn**, không được so sánh với SHAP của XGBoost! |
| **Đơn mô hình XGB (4 hình)** | `xgb_confusion_matrix.png`<br>`xgb_roc_curve.png`<br>`xgb_learning_curve.png`<br>`xgb_feature_importance.png` | ⚠️ Thay thế / ❌ Bỏ sót | 3 hình đầu gom vào lưới 2×2. Riêng `xgb_feature_importance.png` (Trọng số phân nhánh cây) bị bỏ sót, chỉ dùng SHAP beeswarm. |
| **Đơn mô hình SVM (4 hình)** | `svm_confusion_matrix.png`<br>`svm_roc_curve.png`<br>`svm_learning_curve.png`<br>`svm_feature_importance.png` | ⚠️ Thay thế / ❌ Bỏ sót | 3 hình đầu gom vào lưới 2×2. Riêng `svm_feature_importance.png` (Hệ số siêu phẳng `coef_` của Linear SVM) bị bỏ sót. |
| **Đa mô hình (4 hình)** | `confusion_matrices_all.png` | ✅ Dùng (Hình 4.6) | Lưới 2×2 ma trận nhầm lẫn 4 mô hình. |
| | `roc_curves_comparison.png` | ✅ Dùng (Hình 4.4) | 4 đường cong ROC lồng ghép (AUC 0.9911 → 0.9986). |
| | `precision_recall_curves.png` | ✅ Dùng (Hình 4.5) | 4 đường Precision-Recall trên dữ liệu mất cân bằng. |
| | `learning_curves_summary.png` | ✅ Dùng (Hình 4.7) | Lưới 2×2 đường cong học tập kiểm tra Overfitting. |
| **XAI (2 hình)** | `shap_summary.png` | ✅ Dùng (Hình 4.8) | Biểu đồ SHAP Beeswarm của XGBoost. |
| | `top20_keywords_barplot.png` | ❌ **BỎ SÓT** | Biểu đồ cột ngang Top-20 từ khóa cảnh báo có trọng số đồng thuận cao nhất. Trong báo cáo chỉ dùng Bảng 4.3 (text) mà bỏ quên biểu đồ trực quan này. |
| **Ablation (2 hình)** | `ablation_preprocessing_comparison.png` | ✅ Dùng (Hình 4.10) | Biểu đồ đối chứng Raw vs Preprocessed Text. |
| | `ablation_featurespace_comparison.png` | ✅ Dùng (Hình 4.11) | Biểu đồ đối chứng 3 không gian đặc trưng. |
| **Demo UI (4 hình)** | `demo_03_scam_detection_verdict.png` | ✅ Dùng (Hình 4.9) | Màn hình kết quả phân tích tin nhắn lừa đảo. |
| | `demo_01_initial_layout.png` | ❌ **BỎ SÓT** | Giao diện tổng quan ban đầu Split-View. |
| | `demo_02_font_scaling_elderly.png` | ❌ **BỎ SÓT CỰC KỲ ĐÁNG TIẾC** | Minh chứng trực quan cho tuyên bố **Trợ năng người cao tuổi: Phóng đại phông chữ 100% → 125% → 150%**. Không có hình này thì lời khẳng định trợ năng bị thiếu minh chứng thị giác! |
| | `demo_04_mobile_responsive.png` | ❌ **BỎ SÓT** | Giao diện trên điện thoại di động thông minh. |

### 🔍 Lý giải nguyên nhân sâu xa từ quy trình phát triển:
1. **Áp lực khống chế số trang cố định:** Tác giả kịch bản sinh Word (`generate_academic_report.py`) đặt mục tiêu cố định mỗi mục vừa khít 1 trang (để đạt đúng 32 trang). Do đó, tác giả đã chủ động cắt bớt hình ảnh để tránh tràn trang.
2. **Thiếu thiết kế dạng lưới ghép (Sub-figures / Grid layout):** Thay vì ghép 4 biểu đồ EDA còn lại thành một lưới 2×2 (ví dụ Hình 4.4a–d) hoặc ghép 2 ảnh Demo UI thành một hình đôi so sánh (Desktop vs Font phóng to cho người già), kịch bản lại chọn cách lược bỏ hoàn toàn.
3. **Mâu thuẫn văn bản chưa được rà soát:** Dòng 298 `report-source.md` vẫn giữ nguyên câu văn cũ: *"Nhóm thực hiện 7 biểu đồ EDA tại 300 DPI:"*, tạo cảm giác nhóm làm thiếu hoặc bỏ quên bài làm.

---

## PHẦN II: 8 LỖI SAI VÀ ĐIỂM CHƯA ỔN NGHIÊM TRỌNG TRƯỚC KHI NỘP

### 1. Lệch pha số trang Mục lục (TOC Desynchronization)
- **Hiện trạng kiểm chứng thực tế:** Trong tệp `report.pdf` (32 trang) xuất bản từ `report.docx`, bảng Mục lục ở Trang 3 chứa dữ liệu số trang được hardcode cứng trong `generate_academic_report.py` (`default_toc_data`), không khớp với vị trí thực tế:
  - `CHƯƠNG 3`: Mục lục ghi `Trang 09` → Thực tế bắt đầu ở `Trang 10` (lệch 1 trang).
  - `Mục 3.3`: Mục lục ghi `Trang 11` → Thực tế ở `Trang 12` (lệch 1 trang).
  - `Mục 3.4`: Mục lục ghi `Trang 12` → Thực tế ở `Trang 13` (lệch 1 trang).
  - `Mục 3.5`: Mục lục ghi `Trang 13` → Thực tế ở `Trang 14` (lệch 1 trang).
  - `CHƯƠNG 4`: Mục lục ghi `Trang 14` → Thực tế bắt đầu ở `Trang 15` (lệch 1 trang).
  - `Mục 4.2`: Mục lục ghi `Trang 17` → Thực tế ở `Trang 18` (lệch 1 trang).
  - `Mục 4.3`: Mục lục ghi `Trang 22` → Thực tế ở `Trang 23` (lệch 1 trang).
  - `Mục 4.4`: Mục lục ghi `Trang 24` → Thực tế ở `Trang 25` (lệch 1 trang).
  - `Mục 4.5`: Mục lục ghi `Trang 25` → Thực tế ở `Trang 26–27` (lệch 2 trang).
  - `Mục 4.6`: Mục lục ghi `Trang 27` → Thực tế ở `Trang 29` (lệch 2 trang).
  - `CHƯƠNG 5`: Mục lục ghi `Trang 28` → Thực tế bắt đầu ở `Trang 30` (lệch 2 trang).
  - `Mục 5.3`: Mục lục ghi `Trang 29` → Thực tế ở `Trang 31` (lệch 2 trang).
  - `TÀI LIỆU THAM KHẢO`: Mục lục ghi `Trang 30` → Thực tế ở `Trang 32` (lệch 2 trang).
- **Hậu quả:** Giảng viên chấm thi lật Mục lục tìm Chương 4 (ghi Trang 14) nhưng mở ra lại thấy Mục 3.5; tìm Tài liệu tham khảo (ghi Trang 30) mở ra lại thấy Chương 5. Đây là lỗi cấm kỵ trong báo cáo học thuật tốt nghiệp/đồ án.

### 2. Sai tên Khoa quản lý trên Trang bìa chính
- **Hiện trạng:** Dòng 459 trong `generate_academic_report.py`:
  ```python
  p2.add_run("KHOA HỆ THỐNG THÔNG TIN — BỘ MÔN TRÍ TUỆ NHÂN TẠO")
  ```
- **Thực tế học thuật:**
  - Môn học là `CS114` (Computer Science — Khoa học Máy tính).
  - Lớp học là `CS114.F31.CN2.TTNT` (Chuyên ngành Trí tuệ Nhân tạo).
  - Tại Trường ĐH Công nghệ Thông tin (UIT), **Bộ môn Trí tuệ Nhân tạo trực thuộc Khoa Khoa học Máy tính**, không thuộc Khoa Hệ thống Thông tin.
- **Hậu quả:** Sai lệch cơ cấu tổ chức học thuật của trường, thể hiện sự thiếu chỉn chu ngay trên trang đầu tiên của đồ án.

### 3. Đứt gãy kiến trúc Single Source of Truth (SSOT) giữa Markdown và Word
- **Hiện trạng:**
  - `report-source.md` (Markdown) và `generate_academic_report.py` (Script sinh Word) là hai nguồn văn bản độc lập hoàn toàn.
  - Khi thành viên trong nhóm sửa `report-source.md`, file `report.docx` không tự cập nhật; ngược lại khi chỉnh sửa `generate_academic_report.py`, `report-source.md` bị bỏ lại phía sau.
- **Các điểm lệch pha nội dung cụ thể:**
  - **Bảng 3.1 (15 đặc trưng phụ):** Trong `report-source.md` (dòng 163–181) là bảng 6 cột chi tiết với số liệu trung bình thực tế (`TB lừa đảo`, `TB bình thường`) và đoạn phân tích sâu sắc về việc thẻ `[MONEY]` xuất hiện ở tin thường nhiều hơn (1.221 / 1.236 mẫu). Trong `report.docx`, bảng này bị cắt xén chỉ còn 3 cột và mất sạch số liệu trung bình!
  - **Công thức hàm mất mát Cost-Sensitive:** Trong `report-source.md` (dòng 240) có công thức toán học hoàn chỉnh:
    `L(θ) = − Σᵢ [ w · yᵢ · log(pᵢ) + (1 − yᵢ) · log(1 − pᵢ) ]`
    và công thức SVM Hinge Loss có trọng số (dòng 252). Trong `report.docx`, toàn bộ các công thức trọng tâm này không được đưa vào!
  - **Công thức TF-IDF:** Trong `report-source.md` (dòng 340–344) có đầy đủ 3 công thức: `tf(t, d)`, `idf(t)` và `tfidf(t, d)`. Trong `report.docx`, chỉ có 1 công thức con nội dòng `tf_log = 1 + log(tf)`!
  - **Mục lục của `report-source.md`:** Chỉ có 6 dòng tiêu đề cấp 1 sơ sài, không có cấu trúc phân cấp chi tiết.

### 4. Thiếu Bảng Phân công Nhiệm vụ & Tỷ lệ Đóng góp của Thành viên
- **Hiện trạng:** Cả `report-source.md` và `report.docx` chỉ liệt kê danh sách 3 sinh viên và vai trò chung chung trên bìa (Thanh: PM, Cẩm: ML, Sơn: Data & UI).
- **Yêu cầu giảng viên:** Trong đề cương và quy chế chấm đồ án nhóm 3 người (`NopDoAnMonHoc.png`), báo cáo phải có một bảng ma trận phân công chi tiết:
  - Sinh viên phụ trách từng phân hệ cụ thể (Data collection & Provenance, Preprocessing Pipeline, Feature Engineering, Huấn luyện 4 mô hình, XAI SHAP, Streamlit Web App, Soạn thảo Báo cáo Word & Slide).
  - Tỷ lệ hoàn thành nhiệm vụ (100%).
  - Tỷ lệ đóng góp vào đề tài (33.3% hoặc đánh giá theo thang điểm đóng góp).

### 5. Cấu trúc Chương 4 chưa bám sát Đề cương bắt buộc của Thầy Thăng
- **Yêu cầu trong `NopDoAnMonHoc.png`:**
  - 4. Thực nghiệm
    - 4.1. Dataset là gì
    - 4.2. Phương pháp đánh giá là gì
    - 4.3. Kết quả đạt được
- **Hiện trạng trong báo cáo:**
  - Báo cáo đặt 4.1 là *Đặc tả tập dữ liệu và EDA*.
  - Đặt 4.2 là *Kết quả thực nghiệm đối sánh 4 mô hình*, sau đó lại chèn một tiểu mục con đánh số bất thường `4.2.0. Định nghĩa các thước đo đánh giá và ví dụ tính tay`, rồi tiếp tục `4.2.1. Bảng đối sánh tổng hợp...`.
  - Mục *"Phương pháp đánh giá là gì"* (gồm Chiến lược chia Train/Test 80/20, Kiểm định chéo 5-Fold Stratified CV, Định nghĩa các thước đo Accuracy/Precision/Recall/F1/ROC-AUC và ví dụ tính tay) là một trụ cột phương pháp luận lớn, cần được tách thành một mục cấp hai độc lập `4.2` đúng như đề cương của thầy.

### 6. Lỗi dàn trang, ngắt bảng biểu và mật độ chữ không đều trong Word/PDF
- **Hiện trạng kiểm tra trực quan từng trang của `report.pdf`:**
  - **Bảng 4.3 (Top 20 từ khóa SHAP):** Bảng có 21 hàng bị ngắt đôi qua trang (nửa đầu nằm ở cuối Trang 24, nửa sau tràn sang Trang 25).
  - **Mục 4.4 (Web Demo):** Do Bảng 4.3 tràn sang Trang 25 chiếm một phần nhỏ, nội dung Web Demo bị đẩy hẳn sang Trang 26, để lại Trang 25 rất trống trải.
  - **Trang 17, 27, 28 có mật độ chữ dưới 950 ký tự:** Do kịch bản đặt lệnh `doc.add_page_break()` cưỡng bức ở đầu mỗi mục con ngắn (như Ablation 1 và Ablation 2), khiến nửa dưới các trang này để trống hoàn toàn.

### 7. Thiếu phân tích sâu sắc cho trường hợp Linear SVM trong Ablation 2
- **Số liệu thực nghiệm trong Bảng Ablation 2:**
  - Cấu hình *TF-IDF Only (5.000 chiều)*: Linear SVM đạt F1 = **0.9697**, Precision = 98.77%, Recall = 95.24% (chỉ báo sai 1 ca FP).
  - Cấu hình *Combined (5.015 chiều)*: Linear SVM đạt F1 = **0.9474**, Precision = 93.10%, Recall = 96.43% (báo sai 6 ca FP).
- **Vấn đề trong nhận xét hiện tại:**
  - Báo cáo tập trung khen ngợi XGBoost (kết hợp giúp tăng F1 từ 0.9379 lên 0.9535 và giảm 40% FP), nhưng **hoàn toàn im lặng về việc tại sao F1 của Linear SVM lại giảm từ 0.9697 xuống 0.9474 khi thêm 15 đặc trưng phụ**!
  - Người phản biện có chuyên môn sẽ đặt câu hỏi ngay: *"Tại sao thêm đặc trưng mà mô hình SVM lại giảm hiệu năng?"*.
  - **Nguyên nhân khoa học cần bổ sung:** Không gian TF-IDF 5.000 chiều là không gian thưa (sparse) với các giá trị chuẩn hóa L2 phân bố từ 0 đến 1. Khi ghép thêm 15 đặc trưng phụ dạng liên tục được chuẩn hóa qua `StandardScaler` (chứa các giá trị âm và dương có biên độ lớn), góc của siêu phẳng lề tối ưu của bộ phân loại tuyến tính (Linear Classifier) bị dịch chuyển nhẹ, làm tăng số ca báo sai FP từ 1 lên 6 ca. Ngược lại, các mô hình phi tuyến dạng cây như XGBoost có khả năng phân ngưỡng độc lập từng đặc trưng nên hấp thụ hoàn hảo cả hai không gian.

### 8. Thông tin mã lớp và ngày tháng chưa đồng nhất
- Trên trang bìa: ghi `Nhóm 10 — Lớp CS114.F31.CN2` (thiếu mã phân ngành `.TTNT`).
- Ngày báo cáo: ghi `23/09/2026` (ngày báo cáo sớm), trong khi hạn nộp bài chính thức trên LMS là tháng 10/2026. Nên ghi rõ: *"Báo cáo bảo vệ sớm: 23/09/2026 | Nộp bài nghiệm thu chính thức: Tháng 10/2026"*.

---

## PHẦN III: DANH MỤC SKILL ĐỀ XUẤT CHO VIỆC SỬA ĐỔI (`uu:skill-advisor`)

Theo quy chuẩn của `uu:skill-advisor`, các skill tin cậy được kích hoạt để thực hiện xử lý bài toán này gồm:

1. **`uit:academic-report` (Trọng tâm số 1):**
   - **Lý do kích hoạt:** Đây là skill chuyên biệt của UIT để xử lý biên dịch tài liệu học thuật Markdown → Word (.docx) → PDF.
   - **Công cụ sử dụng:**
     - `sync_toc_pages.py`: Tự động trích xuất chính xác trang của từng heading từ file PDF qua PyMuPDF, sau đó nạp ngược lại vào bảng Mục lục Word để triệt tiêu 100% lỗi lệch trang.
     - `audit_docx_xml.py`: Kiểm định chuyên sâu định dạng OpenXML, lề 3-2-2-2 cm, chống gãy bảng qua trang (`<w:cantSplit/>`, `<w:tblHeader/>`).
2. **`ak-fable-thinking` (Trọng tâm số 2):**
   - **Lý do kích hoạt:** Đảm bảo kỷ luật phát ngôn học thuật (Claim Discipline: phân biệt rõ OBSERVED vs DERIVED facts), kiểm soát tính nhất quán số liệu toán học giữa các bảng benchmark và kết quả thực tế.
3. **`uit:project-audit` (Trọng tâm số 3):**
   - **Lý do kích hoạt:** Kiểm tra đối chiếu toàn diện các yêu cầu của ThS. Cáp Phạm Đình Thăng (`NopDoAnMonHoc.png`) và chuẩn bị hồ sơ đóng gói ZIP theo chuẩn UIT (Phase 10).

---

## PHẦN IV: KẾ HOẠCH HÀNH ĐỘNG CỤ THỂ ĐỂ ĐẠT ĐIỂM A+ TUYỆT ĐỐI

### Giai đoạn 1: Chuẩn hóa & Tái cấu trúc Nội dung
1. **Sửa trang bìa:** Đổi thành `KHOA KHOA HỌC MÁY TÍNH — BỘ MÔN TRÍ TUỆ NHÂN TẠO`, mã lớp `CS114.F31.CN2.TTNT`.
2. **Bổ sung Bảng Phân công & Đóng góp thành viên:** Đặt ngay sau trang Cam kết Liêm chính học thuật (Trang 2b hoặc lồng vào Trang 2).
3. **Tái cấu trúc Chương 4 theo chuẩn Thầy Thăng:**
   - `4.1. Bộ dữ liệu nghiên cứu và phân tích khám phá (EDA)` (Dataset là gì)
   - `4.2. Phương pháp đánh giá và kiểm soát rò rỉ dữ liệu` (Phương pháp đánh giá là gì — tách mục 4.2.0 cũ thành mục lớn độc lập)
   - `4.3. Kết quả thực nghiệm đối sánh 4 mô hình học máy` (Kết quả đạt được)
   - `4.4. Trí tuệ nhân tạo có thể giải thích (XAI) với SHAP và Top 20 từ khóa`
   - `4.5. Thực nghiệm đối chứng chuyên sâu (Ablation Studies)`
   - `4.6. Ứng dụng thực tế Web Demo Streamlit trợ năng người cao tuổi`
   - `4.7. Phân tích sai số và đánh giá ca biên ngoại vi`
4. **Bổ sung 4 hình ảnh EDA còn thiếu:** Ghép 4 hình ảnh EDA (`text_length_comparison.png`, `wordcloud_scam_vs_normal.png`, `top_ngrams_scam_vs_normal.png`, `source_distribution.png`) thành lưới hoặc chèn vào vị trí tương ứng kèm nhận xét học thuật đầy đủ.
5. **Bổ sung hình ảnh Web Demo Trợ năng người cao tuổi:** Chèn `demo_02_font_scaling_elderly.png` (Phóng đại cỡ chữ 125%–150%) vào Mục 4.6 để chứng minh tính năng trợ năng thị giác.
6. **Bổ sung đầy đủ công thức toán OMML:**
   - Hàm mất mát Cost-Sensitive Binary Cross-Entropy `L(θ)`.
   - Hàm Hinge Loss có trọng số của SVM.
   - 3 công thức TF-IDF (`tf`, `idf`, `tfidf`).
7. **Đồng bộ hóa Bảng 3.1 (15 đặc trưng):** Đưa bảng 6 cột có giá trị trung bình (`TB lừa đảo`, `TB bình thường`) và phân tích thẻ `[MONEY]` vào bản Word.
8. **Bổ sung nhận xét khoa học cho SVM trong Ablation 2:** Giải thích cơ chế không gian thưa TF-IDF kết hợp đặc trưng liên tục chuẩn hóa làm lệch nhẹ siêu phẳng phân cách.

### Giai đoạn 2: Tự động hóa & Căn chỉnh Bố cục Xuất bản
1. **Căn chỉnh chống gãy trang:** Tối ưu hóa kích thước hình ảnh và khoảng cách dòng để Bảng 4.3 nằm trọn trong 1 trang, không bị tràn 2 hàng sang trang sau.
2. **Đồng bộ Mục lục hai chiều (Two-Way PyMuPDF TOC Sync):**
   - Biên dịch Word → Xuất PDF → Chạy script quét số trang thực tế của từng Heading → Nạp lại vào bảng Mục lục Word → Xuất bản PDF cuối cùng đạt độ chính xác 100%.

---

## Unresolved Questions (Câu hỏi mở)
1. Bạn có muốn gộp 4 biểu đồ EDA còn thiếu (`text_length`, `wordcloud`, `top_ngrams`, `source_distribution`) vào phần Phụ lục (Appendix) hay đưa trực tiếp vào Mục 4.1 trong nội dung chính của báo cáo?
2. Bạn có muốn nhóm giữ nguyên số trang khoảng 32–34 trang hay cho phép mở rộng lên 36 trang để trình bày thoải mái toàn bộ các biểu đồ mà không bị chật chội?
