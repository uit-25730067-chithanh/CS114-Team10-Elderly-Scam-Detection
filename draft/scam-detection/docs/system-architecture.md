# System Architecture — CS114 Scam Detection

## Tổng quan kiến trúc

```
┌─────────────────────────────────────────────────────────┐
│                      DATA LAYER                          │
│  Thu thập thủ công → data/raw/dataset.csv               │
│  (Nguồn: báo DanTri, VnExpress, FB groups, SMS)        │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              PREPROCESSING & FEATURE PIPELINE            │
│  1. Unicode NFC & tone normalization (underthesea)      │
│  2. Extract 15 auxiliary features (phone, money, flags)  │
│  3. Clean: lowercase, deobfuscate leetspeak, teencode    │
│  4. Vietnamese word segmentation (pyvi ViTokenizer)     │
│  5. Domain-guarded stopword removal                     │
│  6. Stratified 80/20 Train/Test split FIRST             │
│  7. TF-IDF vectorization (fit on Train only, 5000 feats) │
│  8. StandardScaler (fit on Train aux features only)     │
│  9. Combine sparse matrix: X_train (1754×5015), X_test  │
└─────────────────────┬───────────────────────────────────┘
                      │
         ┌────────────┼──────────────┐
         ▼            ▼              ▼
┌──────────────┐ ┌─────────┐ ┌─────────────┐
│ Naive Bayes  │ │ Random  │ │     SVM     │
│(MultinomialNB)│ │ Forest  │ │ (LinearSVC) │
└──────┬───────┘ └────┬────┘ └──────┬──────┘
       │              │              │
       │         ┌────┴────┐         │
       │         │ XGBoost │         │
       │         └────┬────┘         │
       └──────────────▼──────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                  EVALUATION MODULE                       │
│  - Confusion Matrix (4 models)                          │
│  - Precision, Recall, F1-Score                          │
│  - ROC-AUC Curve comparison                             │
│  - Precision-Recall Curve comparison                    │
│  - Learning Curves (Train vs Val — overfitting check)   │
│  - XAI: Top-20 scam keywords (feature weights / SHAP)  │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                   DEMO LAYER                             │
│  Streamlit Web App                                       │
│  - Input: text area (SMS/Zalo/Telegram)                 │
│  - Output: Risk meter + Keyword highlight + Category    │
│  - Lời khuyên an toàn per scam category                │
└─────────────────────────────────────────────────────────┘
```

---

## Chi tiết các thành phần

### 1. Data Layer

| File | Mô tả |
|------|-------|
| `data/raw/staging_thanh_normal.csv` | 1.773 mẫu SMS bình thường (IEEE Access 2026, 100% PII masked) |
| `data/raw/staging_cam_scam.csv` | 205 mẫu lừa đảo dịch vụ công & sức khỏe (7 tầng kiểm toán) |
| `data/raw/staging_son_scam.csv` | 215 mẫu lừa đảo quyền lực & cấp cứu (7 tầng kiểm toán) |
| `data/raw/dataset.csv` | Dataset tích hợp chính thức 2.193 mẫu thực tế (100% Zero Synthetic Text) |
| `data/raw/dataset_template.csv` | Template CSV với header chuẩn 8 cột |
| `data/processed/real_world_test_thanh.csv` | 50 mẫu kiểm định thực tế độc lập từ ảnh Drive (0% data leakage) |
| `data/processed/dataset_preprocessed.csv` | Sau clean + tokenize + auxiliary features |
| `data/processed/tfidf_vectorizer.pkl` | Fitted TF-IDF (fit trên train set only, max_features=5000) |
| `data/processed/aux_scaler.pkl` | Fitted StandardScaler (fit trên 15 đặc trưng phụ của train set) |
| `data/processed/X_train.pkl` | Combined sparse CSR matrix tập Train (1.754 × 5.015) |
| `data/processed/X_test.pkl` | Combined sparse CSR matrix tập Test (439 × 5.015) |
| `data/processed/y_train.pkl` | Nhãn nhị phân tập Train (1.418 normal / 336 scam) |
| `data/processed/y_test.pkl` | Nhãn nhị phân tập Test (355 normal / 84 scam) |
| `data/processed/feature_names.json` | 5.015 tên đặc trưng hoàn chỉnh (5.000 TF-IDF + 15 aux) |
| `models/naive_bayes.pkl` | Trained MultinomialNB baseline (Phase 04 — F1=0.8864, Recall=92.86%) |
| `models/naive_bayes_metrics.json` | Bộ tham số tối ưu (alpha=0.01) & metrics thực nghiệm Naive Bayes |
| `models/xgboost.pkl` | Trained XGBoost classifier (Phase 05 — F1=0.9535, Recall=97.62%) |
| `models/xgboost_metrics.json` | Bộ tham số tối ưu (best_params) & metrics thực nghiệm XGBoost |
| `models/random_forest.pkl` | Trained Random Forest (Phase 05 — đang thực hiện) |
| `models/svm_linear.pkl` | Trained SVM Linear (Phase 06 — kế hoạch Sprint 3) |

### 2. Preprocessing Pipeline (`src/preprocessing/`)

| Module | Chức năng |
|--------|-----------|
| `text_cleaner.py` | Unicode NFC, regex clean, modern tone marks (underthesea), 160 teencode, leet-speak deobfuscation |
| `tokenizer.py` | Vietnamese word segmentation (pyvi) & unaccented compounds joining |
| `stopwords.py` | Vietnamese stopword list with domain guard protection for scam tokens |
| `pipeline.py` | Full pipeline orchestrator: clean → tokenize → stopwords → 15 auxiliary features |

### 3. Feature Engineering (`src/feature_engineering.py`)

| Nhóm đặc trưng | Tên đặc trưng | Mô tả chi tiết |
|----------------|---------------|----------------|
| **TF-IDF Matrix** | 5.000 n-grams | N-gram (1, 2), sublinear_tf=True, min_df=2, max_df=0.95 (fit on train only) |
| **Liên hệ & Số học** | `num_phone_numbers` | Số lượng số điện thoại trong văn bản |
| | `num_urls` | Số lượng liên kết URL |
| | `num_money_mentions` | Số lần nhắc đến đơn vị tiền tệ (triệu, tỷ, đ, VND...) |
| | `num_digits` | Tổng số lượng chữ số xuất hiện |
| **Độ dài & Định dạng** | `text_length` | Độ dài ký tự văn bản gốc |
| | `num_exclamation` | Số lượng dấu chấm than (!) tạo cảm giác thúc ép |
| | `uppercase_ratio` | Tỷ lệ ký tự IN HOA trên tổng số chữ cái |
| **Nhãn ẩn danh hóa** | `has_masked_money` | Cờ (0/1) xuất hiện token `[MONEY]` |
| | `has_masked_otp` | Cờ (0/1) xuất hiện token `[MÃ_OTP]` |
| | `has_masked_url` | Cờ (0/1) xuất hiện token `[ĐƯỜNG_DẪN]` |
| **Kỹ thuật lẩn tránh** | `has_unaccented_keywords` | Cờ (0/1) chứa từ khóa bất đối xứng không dấu (`cong_an`, `tai_khoan`) |
| | `has_leetspeak` | Cờ (0/1) chứa biến thể leet-speak (`th0ng ba0`, `kh0ng`) |
| **Bẫy tâm lý đặc thù** | `has_urgent_words` | Cờ (0/1) chứa từ khẩn cấp (gấp, khẩn, ngay lập tức) |
| | `has_emergency_keywords` | Cờ (0/1) chứa kịch bản cấp cứu, tai nạn, bệnh viện |
| | `has_gift_keywords` | Cờ (0/1) chứa kịch bản trúng thưởng, tri ấn, quà tặng |

### 4. Models (`src/models/`)

| Module | Thuật toán | Framework |
|--------|-----------|-----------|
| `naive_bayes_model.py` | MultinomialNB | scikit-learn |
| `random_forest_model.py` | RandomForestClassifier | scikit-learn |
| `xgboost_model.py` | XGBClassifier | xgboost |
| `svm_model.py` | LinearSVC + CalibratedClassifierCV | scikit-learn |

### 5. Evaluation (`src/evaluation/`)

| Module | Chức năng |
|--------|-----------|
| `metrics_calculator.py` | Accuracy, Precision, Recall, F1, AUC |
| `confusion_matrix_plot.py` | Confusion matrix heatmap (4 models) |
| `roc_curve_plot.py` | ROC curve comparison |
| `learning_curve_plot.py` | Learning curve (Train vs Val) |
| `model_comparator.py` | Bảng so sánh tổng hợp CSV |
| `xai_keywords.py` | Top-20 scam keywords extraction |
| `src/model_plots.py` | Helper trực quan hóa đánh giá mô hình: Confusion Matrix, Learning Curve, ROC Curve, Feature Importance (300 DPI) |

---

## Data Flow

```
data/raw/dataset.csv
    ↓ [pipeline.py] → clean + tokenize + stopwords removal
data/processed/dataset_preprocessed.csv (text_cleaned + aux features)
    ↓ [feature_engineering.py] → TF-IDF fit on train set
    ↓ Stratified split: 60% train | 20% val | 20% test
Train set (60%)                 Test set (20%)
    ↓ [models] fit               ↓ [models] predict only
NB / RF / XGB / SVM
    ↓ [evaluation]
Metrics on test set → reports/model_comparison.csv
    ↓ [xai_keywords.py]
Top-20 scam keywords → reports/figures/
```

---

## Quyết định thiết kế quan trọng

1. **TF-IDF fit chỉ trên train set** — tránh data leakage; test set dùng transform only
2. **Stratified split** — giữ tỷ lệ class ở cả train/val/test
3. **Auxiliary features** — bổ sung TF-IDF bằng handcrafted features (phone, url, urgency)
4. **Mỗi model 1 notebook riêng** — Cẩm và Sơn có notebook riêng tránh conflict
5. **CalibratedClassifierCV cho SVM** — để có `predict_proba()` phục vụ ROC và thanh nguy cơ demo
6. **`class_weight='balanced'`** — xử lý imbalance nhẹ, không cần SMOTE (text features ít bị ảnh hưởng)
