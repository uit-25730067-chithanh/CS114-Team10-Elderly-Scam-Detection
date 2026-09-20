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

Nhóm xây dựng pipeline 5 bước:

```
Văn bản thô → Unicode NFC → 160 Teencode → PyVi Tokenizer
             → TF-IDF (5.000 từ) → 15 Auxiliary Features
             → Feature Vector X (5.015 chiều)
```

### Bước 1: Chuẩn hóa Unicode NFC
Đảm bảo đồng nhất encoding tiếng Việt, loại bỏ ký tự đặc biệt không hợp lệ.

### Bước 2: Chuẩn hóa Teencode (160 pattern)
Chuyển đổi 160 từ viết tắt phổ biến (vd: "kq" → "kết quả", "đc" → "được").

### Bước 3: Tách từ PyVi
Sử dụng thư viện PyVi cho word segmentation tiếng Việt.

### Bước 4: TF-IDF Vectorization
- `max_features=5000`, `max_df=0.85`, `min_df=2`
- `ngram_range=(1,2)`: đơn từ và cụm 2 từ
- **Quan trọng**: `fit()` chỉ trên X_train (Zero-Leakage)

### Bước 5: 15 Auxiliary Features
<!-- TODO Sơn: Liệt kê 15 auxiliary features từ feature_engineering.py -->

| Feature | Mô tả | Ý nghĩa |
|---------|-------|---------|
| urgency_score | Tổng hợp 8 tín hiệu khẩn cấp | Chỉ số mức độ thúc ép |
| exclamation_count | Số dấu "!" | Thường cao trong tin lừa đảo |
| caps_ratio | Tỷ lệ chữ hoa | Nhấn mạnh bất thường |
| [TODO: thêm 12 features còn lại] | | |

## 3.2. Feature Engineering tổng thể

Vector đặc trưng cuối cùng: **X ∈ R^{5015}**
- 5.000 đặc trưng TF-IDF
- 15 đặc trưng phụ (auxiliary)
- Zero-leakage: scaler và vectorizer không fit trên test set

## 3.3. Mô tả 4 Mô hình

### Mô hình 1: Naive Bayes (Baseline)
<!-- Phase 04 — Cẩm -->
- **Loại**: MultinomialNB với Laplace smoothing
- **Tham số tốt nhất**: `alpha=0.5`
- **Lý do chọn**: baseline nhanh, interpretable, phù hợp TF-IDF

### Mô hình 2: Random Forest
<!-- Phase 05 — Sơn -->
- **Loại**: sklearn RandomForestClassifier
- **Tham số**: `n_estimators=200, max_depth=50, min_samples_split=2`
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

```
[Input: Tin nhắn thô]
       ↓
[Text Preprocessing Pipeline]
  • Unicode NFC normalization
  • 160 Teencode expansion
  • PyVi word segmentation
       ↓
[Feature Engineering]
  • TF-IDF 5,000 features (fit on train only)
  • 15 Auxiliary features
  → X ∈ R^{5,015}
       ↓
[Model Ensemble]
  • Naive Bayes (baseline)
  • Random Forest
  • XGBoost ← Best Overall
  • SVM Linear
       ↓
[Prediction + Confidence Score]
       ↓
[XAI: SHAP Beeswarm]
  • Top-20 trigger keywords
  • Per-prediction explanation
       ↓
[Output: Cảnh báo + Mức độ nguy cơ]
```

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
