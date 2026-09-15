# Research Report: Exploratory Data Analysis & Zero-Leakage Feature Engineering Pipeline

- **Course:** CS114 — Machine Learning (Máy học), UIT ĐHQG-HCM
- **Project:** Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam
- **Author:** Đặng Chí Thanh (MSSV: 25730067 — Trưởng nhóm / Phụ trách Tiền xử lý dữ liệu & Kỹ thuật đặc trưng)
- **Date:** 15/09/2026
- **Scope:** Báo cáo kiểm toán kỹ thuật Phase 03: Thiết kế quy trình phân tích khám phá dữ liệu (EDA), phát hiện và triệt tiêu lỗi rò rỉ dữ liệu (data leakage), xây dựng pipeline trích xuất 5.015 đặc trưng chuẩn hóa và bàn giao ma trận huấn luyện cho Sprint 2 Modeling.

---

## Executive Summary

Trong giai đoạn thẩm định kỹ thuật Phase 03, nhóm nghiên cứu đã tiến hành rà soát toàn diện mã nguồn nháp và thiết kế lại quy trình kỹ thuật đặc trưng nhằm giải quyết triệt để rủi ro học thuật lớn nhất trong Machine Learning: **Rò rỉ dữ liệu từ tập kiểm thử sang tập huấn luyện (Data Leakage)**.

Bản nháp ban đầu chứa lỗi nghiêm trọng khi áp dụng `TfidfVectorizer.fit_transform()` trên toàn bộ 2.193 dòng dữ liệu trước khi thực hiện chia tập Train/Test. Điều này khiến từ vựng và tần số nghịch đảo (IDF) của tập Test bị rò rỉ vào không gian huấn luyện, dẫn đến chỉ số F1-Score ảo và mô hình mất khả năng khái quát hóa trong đời thực.

Quy trình chuẩn mực mới đã được thiết lập với nguyên tắc: **Stratified Split 80/20 ĐẦU TIÊN → fit Vectorizer & Scaler CHỈ trên tập Train → transform sang tập Test**. 

Kết quả đầu ra của Phase 03 bao gồm:
1. **Bộ ma trận đặc trưng chuẩn hóa**:
   - `X_train.pkl`: Kích thước (1.754 × 5.015), định dạng sparse CSR, dung lượng 1.25 MB.
   - `X_test.pkl`: Kích thước (439 × 5.015), định dạng sparse CSR, dung lượng 302 KB.
   - `y_train.pkl` & `y_test.pkl`: Nhãn nhị phân tương ứng (tỷ lệ lừa đảo được bảo toàn nghiêm ngặt ở mức 19.15%).
2. **Hệ thống 7 biểu đồ phân tích khám phá dữ liệu chất lượng xuất bản (300 DPI)** lưu tại `reports/figures/`.
3. **Bộ kiểm thử tự động 34/34 tests PASSED** đảm bảo tính tái lập 100% (`RANDOM_STATE = 42`).

---

## 1. Rủi Ro Rò Rỉ Dữ Liệu & Giao Thức Khắc Phục Zero-Leakage

### 1.1. Lỗ hổng rò rỉ trong thiết kế cũ
Khi tính toán chỉ số TF-IDF:
```text
IDF(t) = ln((1 + n) / (1 + df(t))) + 1
```
Nếu tính trên toàn bộ tập dữ liệu:
- Tổng số văn bản `n` và tần số xuất hiện `df(t)` chứa cả thông tin phân bố của tập Test.
- Các từ vựng hiếm chỉ xuất hiện trong tập Test vẫn lọt vào danh mục 5.000 từ khóa đặc trưng (Vocabulary).
- Tương tự, nếu `StandardScaler` tính `mean` và `std` của 15 đặc trưng phụ trên toàn bộ 2.193 dòng, các giá trị ngoại lai (outliers) của tập Test sẽ làm dịch chuyển trọng tâm phân phối của tập Train.

### 1.2. Giao thức Zero-Leakage chuẩn mực UIT
Nhóm đã triển khai lớp `DataSplitter`, `TextFeatureExtractor`, và `AuxiliaryFeatureScaler` theo luồng tuần tự nghiêm ngặt:
1. **Bước 1**: Nhận `dataset_preprocessed.csv` (2.193 dòng × 24 cột).
2. **Bước 2**: Thực hiện phân tầng nhãn `StratifiedShuffleSplit` tỷ lệ 80/20 với `random_state=42`. Tách thành `X_train_df` (1.754 dòng) và `X_test_df` (439 dòng). Tỷ lệ lừa đảo đạt 19.16% (Train: 336/1.754) và 19.13% (Test: 84/439).
3. **Bước 3**: `TextFeatureExtractor.fit_transform(X_train_df["text_cleaned"])` → Chỉ học từ vựng và IDF trên 1.754 dòng train. Sau đó gọi `transform(X_test_df["text_cleaned"])`.
4. **Bước 4**: `AuxiliaryFeatureScaler.fit_transform(X_train_df[aux_cols])` → Chỉ học `mean` và `variance` trên tập train. Sau đó gọi `transform(X_test_df[aux_cols])`.
5. **Bước 5**: Ghép nối ma trận thưa bằng `scipy.sparse.hstack` tạo thành không gian thống nhất 5.015 chiều.

---

## 2. Thống Kê Không Gian Đặc Trưng (5.015 Chiều)

Không gian biểu diễn dữ liệu của hệ thống kết hợp sức mạnh ngữ nghĩa của N-grams và tri thức miền an ninh mạng của các cờ phụ:

| Nhóm đặc trưng | Chiều | Cấu hình & Vai trò |
|----------------|-------|--------------------|
| **TF-IDF N-grams** | 5.000 | `ngram_range=(1, 2)`, `sublinear_tf=True`, `min_df=2`, `max_df=0.95`. Bắt trọn các từ ghép và cụm từ ngữ cảnh then chốt (`công_an`, `viện_kiểm_sát`, `chuyển_khoản`, `tai_nạn`, `trúng_thưởng`, `bảo_hiểm_thất_nghiệp`). |
| **Độ dài & Định dạng** | 3 | `text_length`, `num_exclamation`, `uppercase_ratio`. Đo lường tính chất gây hoang mang, thúc ép bằng trực giác hình thức. |
| **Liên hệ & Số liệu** | 4 | `num_phone_numbers`, `num_urls`, `num_money_mentions`, `num_digits`. Đo lường mức độ xuất hiện các yếu tố phục vụ chiếm đoạt tài sản. |
| **Nhãn ẩn danh hóa** | 3 | `has_masked_money`, `has_masked_otp`, `has_masked_url`. Nhận diện các vị trí đã được che giấu thông tin nhạy cảm. |
| **Thủ thuật lẩn tránh** | 2 | `has_unaccented_keywords`, `has_leetspeak`. Bắt các kỹ thuật cố tình viết sai chính tả, thay số đổi chữ nhằm vượt tường lửa viễn thông. |
| **Bẫy tâm lý chuyên biệt** | 3 | `has_urgent_words`, `has_emergency_keywords`, `has_gift_keywords`. Định vị trực tiếp các chiêu trò thao túng nhắm vào người già. |
| **TỔNG CỘNG** | **5.015** | Ma trận kết hợp hoàn chỉnh dạng `scipy.sparse.csr_matrix` |

---

## 3. Phân Tích Thực Nghiệm Khám Phá Dữ Liệu (7 Biểu Đồ 300 DPI)

Toàn bộ 7 biểu đồ phân tích chuyên sâu đã được sinh tự động tại `reports/figures/`:

1. **`label_distribution.png`**:
   - Tỷ lệ nhãn: 80.8% Tin nhắn thường (1.773 mẫu) vs 19.2% Tin nhắn lừa đảo (420 mẫu).
   - Tỷ lệ mất cân bằng mẫu: **4.22 : 1**. Tỷ lệ này phản ánh đúng thực tế đời sống (tin rác/thường nhiều hơn tin lừa đảo có tổ chức). Nhóm quyết định sử dụng tham số `class_weight='balanced'` trong mô hình và đánh giá bằng F1/PR-AUC thay vì Accuracy thuần túy.
2. **`scam_category_distribution.png`**:
   - Phân bố 4 bẫy tâm lý trong 420 mẫu lừa đảo:
     - Giả mạo dịch vụ công (`public_service`): 159 mẫu (37.9%).
     - Đe dọa quyền lực / Viện kiểm sát (`fear_authority`): 127 mẫu (30.2%).
     - Thúc ép tai nạn gia đình (`family_emergency`): 88 mẫu (21.0%).
     - Dụ dỗ quà tặng sức khỏe (`health_gift`): 46 mẫu (11.0%).
3. **`text_length_comparison.png`**:
   - Tin nhắn lừa đảo có độ dài trung bình (142 ký tự, 28 từ) cao hơn đáng kể so with tin nhắn thường (68 ký tự, 13 từ).
   - Lý do: Kẻ lừa đảo cần xây dựng kịch bản dàn dựng phức tạp, xưng danh cơ quan chức năng, liệt kê điều luật và hướng dẫn thao tác chuyển khoản.
4. **`wordcloud_scam_vs_normal.png`**:
   - Tin lừa đảo tập trung cao độ vào các từ vựng cưỡng chế: *công an, lệnh bắt, viện kiểm sát, hồ sơ, chuyển khoản, tài khoản, vneid, trợ cấp, cấp cứu, bệnh viện*.
   - Tin thường tập trung vào từ ngữ sinh hoạt và viễn thông thường nhật: *cảm ơn, mai, gói cước, data, chúc mừng, gọi lại, hẹn*.
5. **`top_ngrams_scam_vs_normal.png`**:
   - Top-20 N-grams phân tách mạnh nhất: `bộ_công_an`, `viện_kiểm_sát`, `tạm_giam`, `chuyển_khoản_ngay`, `nâng_cấp_sim`, `vneid_mức_2`, `thông_báo_xử_phạt`.
6. **`auxiliary_correlation_heatmap.png`**:
   - Các đặc trưng có hệ số tương quan dương cao nhất với nhãn lừa đảo:
     - `has_masked_otp` (+0.38)
     - `has_urgent_words` (+0.35)
     - `num_exclamation` (+0.32)
     - `uppercase_ratio` (+0.29)
     - `has_masked_url` (+0.27)
7. **`source_distribution.png`**:
   - Thể hiện sự đa dạng nguồn thu thập minh bạch: IEEE Access 2026, UIT IE403, La Chắn Cuộc Gọi, Báo Dân Trí, VnExpress, Tuổi Trẻ và kho ảnh chứng thực điện thoại `CS114_Evidence_Vault`.

---

## 4. Kiểm Thử Hệ Thống & Tái Lập Thực Nghiệm

Toàn bộ kiểm thử đơn vị cho module tiền xử lý và kỹ thuật đặc trưng đã được tự động hóa qua `pytest`:

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.3, pytest-9.0.2
rootdir: /Users/tcdtist/dev/uit/cs114/assignments/Final/draft/scam-detection

tests/test_feature_engineering.py ............. [ 38%] (13/13 passed)
tests/test_preprocessing.py ..................... [100%] (21/21 passed)

============================== 34 passed in 2.35s ==============================
```

Các bài kiểm tra xác nhận:
- Tập Train và Test không có bất kỳ điểm dữ liệu nào trùng lặp (No Data Overlap).
- Kích thước ma trận chính xác 5.015 cột trên cả Train và Test.
- `y_train` và từ vựng TF-IDF hoàn toàn đồng nhất giữa 2 lần chạy liên tiếp với cùng seed `42`.
- Không xuất hiện bất kỳ giá trị `NaN` hoặc `Inf` nào trong ma trận thưa.

---

## 5. Hướng Dẫn Bàn Giao Cho Sprint 2 (Phase 04, 05, 06)

Các thành viên phụ trách mô hình nạp dữ liệu trực tiếp từ các file đã đóng gói:

```python
import joblib
from pathlib import Path

DATA_DIR = Path("data/processed")

X_train = joblib.load(DATA_DIR / "X_train.pkl")   # (1754, 5015)
X_test  = joblib.load(DATA_DIR / "X_test.pkl")    # (439, 5015)
y_train = joblib.load(DATA_DIR / "y_train.pkl")   # 336 scam / 1418 normal
y_test  = joblib.load(DATA_DIR / "y_test.pkl")    # 84 scam / 355 normal
```

- **Bùi Thị Mỷ Cẩm**: Nạp dữ liệu vào `03_model_naive_bayes.ipynb` (Phase 04) và `04_model_xgboost.ipynb` (Phase 05).
- **Hoàng Cao Sơn**: Nạp dữ liệu vào `04_model_random_forest.ipynb` (Phase 05).
- **Đặng Chí Thanh**: Chuẩn bị module tính toán chỉ số so sánh tổng hợp và giải thích mô hình XAI (Phase 07).
