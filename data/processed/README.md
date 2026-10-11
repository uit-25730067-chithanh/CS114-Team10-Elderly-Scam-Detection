# Processed Data Registry & Feature Dictionary

Thư mục này lưu trữ các tệp dữ liệu đã qua tiền xử lý, ma trận đặc trưng phân chia Train/Test theo giao thức **Zero-Leakage**, và các đối tượng vectorizer/scaler đã huấn luyện.

---

## 📂 Danh Mục Tệp Xử Lý

| Tên Tệp | Định dạng | Kích thước / Chiều | Mô tả |
|---------|-----------|---------------------|-------|
| `dataset_preprocessed.csv` | CSV (UTF-8-sig) | 2.193 dòng × 24 cột | Tập dữ liệu hoàn chỉnh sau chuẩn hóa Unicode NFC, 160 teencode, Leet-speak, tách từ pyvi và 15 đặc trưng phụ |
| `X_train.pkl` | Sparse CSR Matrix | (1.754 × 5.015) — 1.25 MB | Ma trận đặc trưng tập Huấn luyện (5.000 TF-IDF + 15 aux features) |
| `X_test.pkl` | Sparse CSR Matrix | (439 × 5.015) — 302 KB | Ma trận đặc trưng tập Kiểm thử độc lập (transform ONLY từ train vectorizer/scaler) |
| `y_train.pkl` | NumPy Array (int) | (1.754,) — 56 KB | Nhãn nhị phân tập Train: 1.418 Normal (0) / 336 Scam (1) — Tỷ lệ lừa đảo: 19.16% |
| `y_test.pkl` | NumPy Array (int) | (439,) — 15 KB | Nhãn nhị phân tập Test: 355 Normal (0) / 84 Scam (1) — Tỷ lệ lừa đảo: 19.13% |
| `tfidf_vectorizer.pkl` | Scikit-Learn Estimator | 198 KB | Đối tượng `TfidfVectorizer` (N-gram 1-2, sublinear_tf=True, min_df=2, max_df=0.95, fit duy nhất trên Train) |
| `aux_scaler.pkl` | Scikit-Learn Estimator | 0.9 KB | Đối tượng `StandardScaler` (fit duy nhất trên 15 đặc trưng phụ của Train) |
| `feature_names.json` | JSON List | 80 KB (5.015 tên) | Danh sách tên gọi 5.015 đặc trưng phục vụ phân tích độ quan trọng và giải thích mô hình (XAI SHAP) |
| `real_world_test_thanh.csv` | CSV (UTF-8-sig) | 50 dòng | Tập kiểm thử độc lập từ ảnh chụp màn hình đời thực trong `CS114_Evidence_Vault` |

---

## 🔒 Bản Thừa Kế 24 Cột trong `dataset_preprocessed.csv`

1. `id`: Định danh mẫu tin (1 – 2193)
2. `text`: Văn bản tin nhắn gốc
3. `label`: Nhãn nhị phân (0: Normal, 1: Scam)
4. `scam_category`: Nhóm bẫy tâm lý (`fear_authority`, `family_emergency`, `health_gift`, `public_service`, `none`)
5. `source`: Nguồn thu thập đời thực
6. `source_url`: Permalink kiểm chứng 1-1
7. `collector_name`: Người thu thập (Thanh: 1.773, Sơn: 215, Cẩm: 205)
8. `notes`: Ghi chú kiểm toán
9. `text_cleaned`: Văn bản sau chuẩn hóa Unicode NFC, khử Leet-speak, giải mã 160 teencode, xóa URL/SĐT và tách từ ghép pyvi
10–24. **15 Đặc trưng phụ:**
- `num_phone_numbers`: Số lượng số điện thoại
- `num_urls`: Số lượng liên kết URL
- `num_money_mentions`: Số lần nhắc cụm từ tiền tệ
- `num_digits`: Tổng số chữ số xuất hiện
- `text_length`: Độ dài ký tự văn bản gốc
- `num_exclamation`: Số lượng dấu chấm than (!)
- `uppercase_ratio`: Tỷ lệ chữ IN HOA trên tổng số chữ cái
- `has_masked_money`: Cờ (0/1) xuất hiện nhãn `[MONEY]`
- `has_masked_otp`: Cờ (0/1) xuất hiện nhãn `[MÃ_OTP]`
- `has_masked_url`: Cờ (0/1) xuất hiện nhãn `[ĐƯỜNG_DẪN]`
- `has_unaccented_keywords`: Cờ (0/1) chứa từ khóa bất đối xứng không dấu
- `has_leetspeak`: Cờ (0/1) chứa thủ thuật lẩn tránh leet-speak
- `has_urgent_words`: Cờ (0/1) chứa từ ngữ thúc ép khẩn cấp
- `has_emergency_keywords`: Cờ (0/1) chứa kịch bản tai nạn / cấp cứu
- `has_gift_keywords`: Cờ (0/1) chứa kịch bản tri ân / quà tặng
