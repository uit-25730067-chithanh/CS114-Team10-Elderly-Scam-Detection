---
title: "Phát hiện Tin nhắn và Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam"
subtitle: "Báo cáo Đồ án Cuối kỳ — CS114 Máy học"
course: "CS114.F31.CN2.TTNT"
instructor: "ThS. Cáp Phạm Đình Thăng"
group: "Nhóm 10"
members:
  - name: "Đặng Chí Thanh"
    mssv: "25730067"
    role: "Trưởng nhóm / PM"
    email: "25730067@ms.uit.edu.vn"
  - name: "Bùi Thị Mỷ Cẩm"
    mssv: "25730013"
    role: "ML Modeling"
    email: "25730013@ms.uit.edu.vn"
  - name: "Hoàng Cao Sơn"
    mssv: "25730061"
    role: "Data Collection & Demo UI"
    email: "25730061@ms.uit.edu.vn"
date: "23/09/2026"
university: "Trường Đại học Công nghệ Thông tin — ĐHQG-HCM"
academic_integrity: true
---

<!-- ═══════════════════════════════════════════════════════════════════
     TEMPLATE MẪU — Phase 09 Report
     Branch: feat/phase-09-report-template
     Bàn giao: Hoàng Cao Sơn (25730061) tạo PR và sửa tiếp
     Reviewer: Đặng Chí Thanh (25730067)
     ═══════════════════════════════════════════════════════════════════ -->

# Cam kết Liêm chính Học thuật

> Chúng tôi — Đặng Chí Thanh (25730067), Bùi Thị Mỷ Cẩm (25730013), Hoàng Cao Sơn (25730061) — cam kết rằng báo cáo này là công trình nghiên cứu độc lập của nhóm, không vi phạm liêm chính học thuật. Mọi nguồn tài liệu đều được trích dẫn đầy đủ.

---

# Mục lục

1. Đặt vấn đề
2. Các phương pháp tiếp cận
3. Phương pháp nhóm chọn
4. Thực nghiệm
5. Kết luận
- Tài liệu tham khảo

---

# Chương 1 — Đặt vấn đề

## 1.1. Bối cảnh và tính cấp thiết

<!-- TODO Sơn: Viết 2-3 đoạn về tình trạng lừa đảo NCT tại VN 2026.
     Gợi ý: số liệu thực tế từ Bộ CA, VnExpress, Tuổi Trẻ 2025-2026 -->

Hiện nay, người cao tuổi tại Việt Nam đang là đối tượng bị nhắm mục tiêu hàng đầu trong các chiến dịch lừa đảo qua tin nhắn điện thoại. Theo thống kê [TODO: chèn nguồn], hàng chục nghìn vụ lừa đảo liên quan đến người trên 60 tuổi được ghi nhận mỗi năm.

Đặc điểm chung của các cuộc tấn công: kẻ lừa đảo khai thác tâm lý sợ hãi, lòng tin vào quyền lực nhà nước, tình cảm gia đình và sự ham muốn trúng thưởng. Bốn nhóm bẫy tâm lý chính được nhóm phát hiện và phân loại trong quá trình thu thập dữ liệu:

- **Đe dọa quyền lực (fear_authority)**: giả mạo cảnh sát, tòa án, Bộ Công an
- **Khẩn cấp gia đình (family_emergency)**: con cháu tai nạn, cần tiền gấp
- **Dụ dỗ quà tặng (health_gift)**: trúng thưởng, ưu đãi bảo hiểm, thuốc miễn phí
- **Giả mạo dịch vụ công (public_service)**: BHXH, điện lực, ngân hàng giả

## 1.2. Các khó khăn và thách thức

<!-- TODO Sơn: Trình bày 3-4 thách thức kỹ thuật khi xử lý văn bản tiếng Việt -->

Việc phát hiện tự động tin nhắn lừa đảo tiếng Việt gặp nhiều thách thức đặc thù:

1. **Sự đa dạng ngôn ngữ tiếng Việt**: ngôn ngữ tonal với 6 thanh điệu, teencode, viết tắt không chuẩn
2. **Mất cân bằng nhãn (class imbalance)**: tỷ lệ lừa đảo thực tế rất thấp (~20% trong dataset)
3. **Thiếu dữ liệu chuẩn (benchmark)**: chưa có dataset tiếng Việt chuẩn công khai cho bài toán này
4. **Yêu cầu Recall cao**: bỏ lọt lừa đảo (FN) nguy hiểm hơn báo sai (FP) — cần tối ưu Recall

## 1.3. Ý nghĩa thực tiễn

<!-- TODO Sơn: 1-2 đoạn về tác động xã hội -->

Hệ thống phát hiện tự động có thể được tích hợp vào ứng dụng nhắn tin, nền tảng ngân hàng, hoặc phần mềm bảo vệ cho người cao tuổi. Mô hình XAI giúp giải thích từng cảnh báo, tăng cường niềm tin của người dùng.

---

# Chương 2 — Các phương pháp tiếp cận

## 2.1. Khảo sát công trình liên quan (Related Works)

<!-- TODO Sơn: Tóm tắt 3-5 bài báo liên quan -->

| Công trình | Phương pháp | Dataset | Kết quả |
|-----------|-------------|---------|---------|
| [TODO: Paper 1] | [TODO] | [TODO] | [TODO] |
| [TODO: Paper 2] | [TODO] | [TODO] | [TODO] |
| [TODO: Paper 3] | [TODO] | [TODO] | [TODO] |

*Ghi chú: Tham khảo `reports/research-cam-phase04-05-modeling-audit.md` và `research-thanh-phase03-eda-feature-engineering-audit.md` để tìm các bài báo đã review trong quá trình nghiên cứu.*

## 2.2. So sánh các hướng tiếp cận

| Hướng | Ưu điểm | Nhược điểm | Phù hợp? |
|-------|---------|-----------|----------|
| Rule-based | Đơn giản, giải thích được | Không tổng quát, cần cập nhật thủ công | ❌ |
| Machine Learning cổ điển | Nhanh, giải thích được, ít tài nguyên | Cần feature engineering tốt | ✅ Chọn |
| Deep Learning (BERT) | Hiểu ngữ cảnh sâu | Cần nhiều data, chậm hơn | 🔭 Hướng tương lai |

## 2.3. Lý do chọn hướng ML + NLP tiếng Việt

<!-- TODO Sơn: 1 đoạn giải thích lý do lựa chọn -->

Nhóm chọn hướng Machine Learning cổ điển vì:
- Phù hợp quy mô dataset (2.193 mẫu)
- Tốc độ inference nhanh (<1 giây/sample)
- Giải thích được qua SHAP (phù hợp yêu cầu học thuật)
- Không cần GPU, có thể deploy trên server bình thường

---

# Chương 3 — Phương pháp nhóm chọn

## 3.1. Pipeline Tiền xử lý Tiếng Việt

Tin nhắn thô được xử lý theo hai nhánh song song (xem Hình 3.1). Điểm cần lưu ý về thứ tự: **15 đặc trưng phụ được trích từ văn bản gốc trước khi làm sạch**, vì các bước làm sạch xóa mất URL, số điện thoại, chữ in hoa và dấu câu, đúng là những tín hiệu mà các đặc trưng này cần đếm. Nhánh văn bản gồm năm bước theo thứ tự dưới đây.

```
Văn bản thô ─┬─► [Nhánh A] 15 đặc trưng phụ (regex trên văn bản gốc) ─► StandardScaler ─┐
             │                                                                          ├─► X ∈ R^5015
             └─► [Nhánh B] Bước 1 → 2 → 3 → 4 → 5 ─► TF-IDF 5.000 chiều ──────────────┘
```

### Bước 1: Gỡ ký tự thay thế (leet-speak) và tách thẻ ẩn danh
Kẻ lừa đảo thường thay chữ bằng số hoặc ký tự lạ để né bộ lọc (ví dụ "th0ng bao", "kh0a the"). Nhóm dùng 22 mẫu regex để khôi phục về chữ gốc. Các thẻ ẩn danh dính liền chữ (ví dụ `[ĐƯỜNG_DẪN]de`) được tách bằng khoảng trắng.

### Bước 2: Chuẩn hóa Unicode NFC và vị trí dấu thanh
Chuyển văn bản về dạng Unicode NFC, chuẩn hóa vị trí dấu thanh theo quy tắc đặt dấu hiện hành (thư viện `underthesea`), sau đó đưa về chữ thường. Bước này bảo đảm cùng một từ không bị tính thành nhiều dạng khác nhau chỉ vì cách gõ dấu hay bảng mã.

### Bước 3: Chuẩn hóa thực thể, teencode và ký tự nhiễu
- Xóa URL, số điện thoại và địa chỉ email còn nguyên dạng trong văn bản.
- Chuyển các thẻ ẩn danh của bộ dữ liệu sang token ngữ nghĩa: `[ĐƯỜNG_DẪN]` thành `link_truy_cap`, `[SỐ_ĐIỆN_THOẠI]` thành `so_dien_thoai`, `[MONEY]` hoặc `[SỐ_TIỀN]` thành `so_tien`, `[MÃ_OTP]` thành `ma_otp`, `[THƯƠNG_HIỆU]` thành `thuong_hieu`.
- Mở rộng 160 từ viết tắt và teencode do nhóm tự xây dựng (ví dụ "kq" thành "kết quả", "đc" thành "được").
- Loại ký tự đặc biệt nhưng giữ nguyên chữ cái có dấu tiếng Việt, rồi gộp khoảng trắng.

### Bước 4: Tách từ bằng PyVi
Tiếng Việt viết có khoảng trắng giữa các âm tiết, nên một từ ghép như "tài khoản" sẽ bị tách thành hai đơn vị nếu không tách từ. Nhóm dùng PyVi để ghép thành `tài_khoản`. Với tin nhắn viết không dấu (chiếm khoảng 55% tin bình thường trong bộ dữ liệu), một danh sách các cụm không dấu thường gặp được ghép trước khi chạy PyVi.

### Bước 5: Lọc từ dừng có bảo vệ từ khóa miền
Loại 83 từ dừng ngữ pháp (liên từ, giới từ, từ nối). Danh sách 44 từ khóa miền (ví dụ `công_an`, `khẩn`, `chuyển_khoản`, `otp`, `viện_phí`) được bảo vệ, không bao giờ bị loại. Nếu kết quả rỗng, hệ thống giữ lại văn bản đã làm sạch ở bước 3 để không tạo ra dòng trống.

### Vector hóa TF-IDF
- Cấu hình: `max_features=5000`, `ngram_range=(1,2)` (đơn từ và cụm hai từ), `min_df=2`, `max_df=0.95`, `sublinear_tf=True`.
- **Quan trọng**: `fit()` chỉ chạy trên tập huấn luyện, sau đó `transform` tập kiểm thử (Zero-Leakage).

### 15 đặc trưng phụ (Auxiliary Features)
Các đặc trưng này được trích bằng regex trên văn bản gốc, rồi chuẩn hóa bằng `StandardScaler` (fit chỉ trên tập huấn luyện). Cột trung bình tính trên toàn bộ 2.193 mẫu của bộ dữ liệu, chỉ để mô tả.

| STT | Đặc trưng | Kiểu | Mô tả | TB lừa đảo | TB bình thường |
|:---:|-----------|:----:|-------|:---------:|:--------------:|
| 1 | `num_urls` | Đếm | Số URL hoặc thẻ `[ĐƯỜNG_DẪN]` | 0,40 | 0,46 |
| 2 | `num_phone_numbers` | Đếm | Số điện thoại hoặc thẻ `[SỐ_ĐIỆN_THOẠI]`, `[HOTLINE]` | 0,03 | 0,00 |
| 3 | `num_money_mentions` | Đếm | Số lần nhắc số tiền (triệu, tỷ, nghìn, đồng, `[MONEY]`...) | 0,24 | 1,40 |
| 4 | `has_urgent_words` | Cờ 0/1 | Có từ thúc ép (gấp, khẩn, phong tỏa, khóa tài khoản, hết hạn...) | 0,19 | 0,04 |
| 5 | `num_authority_words` | Đếm | Số từ chỉ cơ quan quyền lực (công an, viện kiểm sát, VNeID...) | 0,13 | 0,04 |
| 6 | `has_emergency_words` | Cờ 0/1 | Có từ tình huống khẩn cấp gia đình (cấp cứu, tai nạn, viện phí...) | 0,10 | 0,00 |
| 7 | `has_gift_words` | Cờ 0/1 | Có từ dụ quà tặng (trúng thưởng, tri ân, miễn phí, quay số...) | 0,09 | 0,11 |
| 8 | `has_otp_request` | Cờ 0/1 | Có cụm yêu cầu mã OTP, mật khẩu, mã xác thực | 0,01 | 0,04 |
| 9 | `has_leet_speak` | Cờ 0/1 | Có dấu hiệu thay chữ bằng số (th0ng, kh0a...) | 0,03 | 0,00 |
| 10 | `is_unaccented` | Cờ 0/1 | Toàn bộ tin nhắn không có dấu tiếng Việt | 0,02 | 0,55 |
| 11 | `text_length` | Số | Số ký tự của văn bản gốc | 140,8 | 232,9 |
| 12 | `num_words` | Số | Số từ (tách theo khoảng trắng) | 28,7 | 44,3 |
| 13 | `num_exclamation` | Đếm | Số dấu chấm than | 0,12 | 0,30 |
| 14 | `num_question` | Đếm | Số dấu chấm hỏi | 0,04 | 0,02 |
| 15 | `num_uppercase_words` | Đếm | Số từ viết hoa toàn bộ (từ hai ký tự trở lên) | 2,34 | 8,05 |

Nhận xét: các đặc trưng 2, 4, 5, 6, 9 và 14 có giá trị trung bình cao hơn ở tin lừa đảo như kỳ vọng, còn số lần nhắc tiền, số từ in hoa, độ dài và tính không dấu lại cao hơn ở tin bình thường. Riêng đặc trưng số lần nhắc tiền, nguyên nhân nằm ở bộ dữ liệu: thẻ `[MONEY]` xuất hiện trong 1.236 tin, trong đó 1.221 tin (khoảng 99%) thuộc lớp bình thường. Nhóm chưa phân tích nguyên nhân của các đặc trưng còn lại. Vì vậy, giá trị của 15 đặc trưng được đánh giá bằng thực nghiệm đối chứng ở Chương 4 chứ không dựa vào trực giác.

## 3.2. Feature Engineering tổng thể

Vector đặc trưng cuối cùng: **X ∈ R^{5015}**
- 5.000 đặc trưng TF-IDF
- 15 đặc trưng phụ (auxiliary)
- Zero-leakage: scaler và vectorizer không fit trên test set

## 3.3. Mô tả 4 Mô hình

### Mô hình 1: Naive Bayes (Baseline)
<!-- Phase 04 — Cẩm -->
- **Loại**: MultinomialNB với Laplace smoothing
- **Tham số tốt nhất**: `alpha=0.01` (GridSearchCV 5-fold)
- **Đặc trưng đầu vào**: chỉ 5.000 chiều TF-IDF (không âm)
- **Lý do chọn**: baseline nhanh, interpretable, phù hợp TF-IDF

### Mô hình 2: Random Forest
<!-- Phase 05 — Sơn -->
- **Loại**: sklearn RandomForestClassifier
- **Tham số**: `n_estimators=200, max_depth=50, min_samples_split=2, min_samples_leaf=2, max_features=0.2, class_weight="balanced"`
- **Lý do chọn**: ensemble robustness, ít overfit

### Mô hình 3: XGBoost
<!-- Phase 05 — Cẩm -->
- **Loại**: XGBClassifier
- **Tham số**: `n_estimators=300, max_depth=5, learning_rate=0.05, scale_pos_weight=4.22`
- **scale_pos_weight**: xử lý class imbalance 4.22:1 (Bình thường:Lừa đảo)

### Mô hình 4: SVM Linear (Best Linear)
<!-- Phase 06 — Cẩm -->
- **Loại**: LinearSVC + CalibratedClassifierCV (5-fold)
- **Tham số**: `C=10.0`
- **Lý do chọn**: tốt với high-dimensional sparse features (TF-IDF)

## 3.4. Kiến trúc tổng thể hệ thống

Hình 3.1 mô tả luồng dữ liệu từ đầu vào đến đầu ra của hệ thống. Tin nhắn thô được tách thành hai nhánh song song:

- **Nhánh A (tín hiệu hành vi):** 15 đặc trưng phụ được trích bằng regex trực tiếp từ văn bản **gốc**, trước khi làm sạch, để không làm mất các dấu hiệu như URL, số điện thoại, chữ in hoa hay dấu chấm than. Sau đó chuẩn hóa bằng `StandardScaler`.
- **Nhánh B (nội dung văn bản):** làm sạch (gỡ leet-speak, chuẩn hóa Unicode NFC và vị trí dấu, đưa về chữ thường, chuyển thẻ ẩn danh thành token ngữ nghĩa, 160 quy tắc teencode, lọc ký tự), tách từ PyVi, lọc stopwords có bảo vệ từ khóa miền, rồi vector hóa TF-IDF 5.000 chiều (n-gram 1–2).

Hai nhánh được ghép thành vector X ∈ ℝ⁵⁰¹⁵ trước khi đưa vào bộ phân loại. Vectorizer và scaler chỉ được `fit` trên tập huấn luyện (Zero-Leakage). Naive Bayes là ngoại lệ: mô hình này chỉ dùng 5.000 chiều TF-IDF vì không nhận được giá trị âm của đặc trưng đã chuẩn hóa.

![Sơ đồ luồng Đầu vào – Đầu ra của hệ thống](../figures/system_io_flowchart.png)

*Hình 3.1. Sơ đồ luồng Đầu vào – Đầu ra của hệ thống phát hiện tin nhắn lừa đảo.*

Bốn mô hình (Naive Bayes, Random Forest, XGBoost, Linear SVM) được huấn luyện độc lập trên cùng một tập dữ liệu và là các **phương án thay thế** của nhau, không phải một hệ thống ensemble. Ứng dụng demo cho phép chọn một mô hình, mặc định là XGBoost, và trả về xác suất p = P(lừa đảo). Tin nhắn được gắn nhãn lừa đảo khi p ≥ 0,5. Kết quả hiển thị gồm thang mức độ nguy cơ, các từ khóa đáng ngờ được đánh dấu theo bộ từ khóa thao túng tâm lý, và khuyến nghị an toàn cho người cao tuổi. Phân tích SHAP (mục 4.3) là giải thích toàn cục thực hiện offline trên tập kiểm thử, không chạy theo từng tin nhắn trong ứng dụng.

---

# Chương 4 — Thực nghiệm

## 4.1. Dataset & Phân tích Khám phá (EDA)

### 4.1.1. Mô tả Bộ dữ liệu

Nhóm thu thập **2.193 mẫu thực tế** (100% Zero Synthetic Text):

| Loại | Số mẫu | Nguồn | Người thu thập |
|------|--------|-------|----------------|
| Bình thường (label=0) | 1.773 | IEEE Access 2026 Vietnamese SMS Dataset | Đặng Chí Thanh |
| Lừa đảo — Quyền lực | 127 | Báo Dân Trí, VnExpress, KLTN Smishing | Hoàng Cao Sơn |
| Lừa đảo — Gia đình | 88 | La Chắn Cuộc Gọi, SMS thực tế | Bùi Thị Mỷ Cẩm |
| Lừa đảo — Quà tặng | 46 | Bài báo chính thống | Bùi Thị Mỷ Cẩm |
| Lừa đảo — Dịch vụ công | 159 | Báo Tuổi Trẻ, UIT IE403 corpus | Hoàng Cao Sơn |
| **Tổng** | **2.193** | | **Cả nhóm** |

**Chiến lược phân chia Zero-Leakage (Stratified 80/20)**:
- Train: 1.754 mẫu | Test: 439 mẫu
- Holdout: 50 mẫu ảnh chụp điện thoại thực tế (CS114 Evidence Vault)

### 4.1.2. Phân tích Khám phá Dữ liệu (EDA)

Nhóm thực hiện 7 biểu đồ EDA tại 300 DPI:

![Phân bố nhãn](../figures/label_distribution.png)
*Hình 4.1: Phân bố nhãn — Bình thường (1.773) vs Lừa đảo (420), tỷ lệ mất cân bằng 4.2:1*

![Phân bố nhóm bẫy tâm lý](../figures/scam_category_distribution.png)
*Hình 4.2: Phân bố 4 nhóm bẫy tâm lý trong 420 mẫu lừa đảo*

<!-- TODO Sơn: Thêm nhận xét EDA cho Hình 4.1 và 4.2 -->

![Ma trận tương quan auxiliary features](../figures/auxiliary_correlation_heatmap.png)
*Hình 4.3: Ma trận tương quan 15 auxiliary features với nhãn lừa đảo. urgency_score có tương quan cao nhất.*

<!-- TODO Sơn: Nhận xét về 3 figures trên -->

## 4.2. Kết quả thực nghiệm

### 4.2.1. Bảng so sánh tổng thể 4 mô hình

| Mô hình | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---------|----------|-----------|--------|----------|---------|
| **XGBoost** ⭐ | **98.18%** | **93.18%** | **97.62%** | **95.35%** | 99.84% |
| SVM Linear | 97.95% | 93.10% | 96.43% | 94.74% | **99.86%** |
| Random Forest | 97.72% | 91.11% | 97.62% | 94.25% | 99.77% |
| Naive Bayes | 95.44% | 84.78% | 92.86% | 88.64% | 99.11% |

*Nguồn: `reports/model_comparison.csv` — tất cả mô hình vượt chỉ tiêu F1 ≥ 88%, Recall ≥ 92%*

### 4.2.2. ROC Curves & Precision-Recall Curves

![ROC Curves so sánh](../figures/roc_curves_comparison.png)
*Hình 4.4: ROC Curves — Tất cả 4 mô hình đạt AUC ≥ 99%, chứng tỏ chất lượng phân loại xuất sắc*

![Precision-Recall Curves](../figures/precision_recall_curves.png)
*Hình 4.5: Precision-Recall Curves — XGBoost và SVM duy trì Precision cao tại Recall cao*

<!-- TODO Sơn: Nhận xét 2-3 câu về mỗi biểu đồ -->

### 4.2.3. Confusion Matrices

![Confusion Matrices cả 4 mô hình](../figures/confusion_matrices_all.png)
*Hình 4.6: Confusion Matrices — XGBoost: TP=41, FN=1, FP=7, TN=390 (FN thấp nhất)*

<!-- TODO Sơn: Phân tích FP/FN từng model -->

### 4.2.4. Learning Curves — Kiểm tra Overfit

![Learning Curves tổng hợp](../figures/learning_curves_summary.png)
*Hình 4.7: Learning Curves — Train Score ≈ Val Score với tăng mẫu → không overfit*

## 4.3. Giải thích Mô hình (XAI — Explainable AI)

### 4.3.1. SHAP Beeswarm Analysis

![SHAP Summary Beeswarm](../figures/shap_summary.png)
*Hình 4.8: SHAP Beeswarm — Top-20 features ảnh hưởng đến quyết định XGBoost*

**Phân tích từ khóa kích hoạt cảnh báo**:

| Hạng | Từ khóa | Ảnh hưởng | Giải thích |
|------|---------|-----------|-----------|
| 1 | urgency_score | Cao | Feature tổng hợp mức độ thúc ép |
| 2 | chuyển khoản | Cao | Yêu cầu tài chính trực tiếp |
| 3 | khẩn cấp | Cao | Tạo áp lực thời gian |
| 4 | xác nhận | Trung bình | Giả vờ quy trình chính thức |
| 5 | phạt | Trung bình | Đe dọa pháp lý |
| [TODO Sơn: thêm 15 từ còn lại từ SHAP output] | | | |

<!-- TODO Sơn: Mô tả thêm nhận xét về SHAP feature importance -->

## 4.4. Demo Ứng dụng

![Demo Streamlit — Phát hiện tin nhắn lừa đảo](../figures/demo_03_scam_detection_verdict.png)
*Hình 4.9: Giao diện Streamlit Web App — Kết quả phân tích tin nhắn lừa đảo thời gian thực*

Ứng dụng Streamlit cung cấp:
- **Model Catalog**: 4 thuật toán có thể chuyển đổi
- **Trợ năng**: Font ≥16px, high contrast cho người cao tuổi
- **Giải thích AI**: SHAP explanation cho từng dự đoán
- **Kiểm tra**: 16/16 Playwright E2E tests PASSED, 70/70 pytest PASSED

---

# Chương 5 — Kết luận

## 5.1. Tổng kết kết quả

<!-- TODO Sơn: Viết 2-3 đoạn tổng kết -->

Qua quá trình thực nghiệm với bộ dữ liệu 2.193 mẫu thực tế (100% Zero Synthetic Text), nhóm đã đạt được các kết quả nổi bật:

- **XGBoost** là mô hình tốt nhất tổng thể: F1=**95.35%** (vượt mục tiêu ≥88%), Recall=**97.62%** (vượt mục tiêu ≥92%)
- **Tất cả 4 mô hình** đều vượt chỉ tiêu kỹ thuật đề ra
- **SHAP XAI** xác định thành công 20 từ khóa tâm lý học kích hoạt cảnh báo
- **Demo Streamlit** hoạt động đầy đủ với thiết kế trợ năng cho người cao tuổi

## 5.2. Đóng góp chính

1. **Dataset**: 2.193 mẫu thực tế tiếng Việt (đầu tiên về bẫy tâm lý NCT) với 4 phân loại nhóm bẫy mới
2. **Pipeline NLP tiếng Việt**: 160 teencode patterns + PyVi + Zero-Leakage TF-IDF + 15 auxiliary features
3. **So sánh toàn diện**: 4 mô hình chuẩn với đánh giá multi-metric (Accuracy, Precision, Recall, F1, ROC-AUC)
4. **XAI tích hợp**: SHAP Beeswarm giải thích cơ chế phát hiện cho từng dự đoán

## 5.3. Hướng phát triển

<!-- TODO Sơn: 4-5 bullet về hướng tương lai -->

- **Ngắn hạn**: Tích hợp PhoBERT (Pre-trained BERT tiếng Việt) — dự kiến F1 ≥ 97%
- **Trung hạn**: Mở rộng sang phát hiện voice scam (cuộc gọi thoại)
- **Dài hạn**: API tích hợp vào ứng dụng ngân hàng, nhà mạng, app bảo vệ NCT
- **Dataset**: Mở rộng lên 10.000+ mẫu với đa dạng nguồn và kịch bản mới

---

# Tài liệu tham khảo

[1] T. Chen và C. Guestrin, "XGBoost: A Scalable Tree Boosting System," trong *Proceedings KDD 2016*, San Francisco, CA, USA, 2016, tr. 785-794.

[2] J. Platt, "Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods," trong *Advances in Large Margin Classifiers*, MIT Press, 1999, tr. 61-74.

[3] D. Q. Nguyen và cộng sự, "PhoBERT: Pre-trained Language Models for Vietnamese," trong *Findings of EMNLP 2020*, Punta Cana, Dominican Republic, 2020.

[4] [TODO Sơn: Thêm citation cho Vietnamese SMS Dataset IEEE Access 2026]

[5] F. Pedregosa và cộng sự, "Scikit-learn: Machine Learning in Python," *Journal of Machine Learning Research*, tập 12, tr. 2825-2830, 2011.

[6] S. M. Lundberg và S.-I. Lee, "A Unified Approach to Interpreting Model Predictions," trong *Proceedings NeurIPS 2017*, Long Beach, CA, USA, 2017.

---

*Báo cáo được tạo theo template `uit:academic-report` | Branch: `feat/phase-09-report-template`*
