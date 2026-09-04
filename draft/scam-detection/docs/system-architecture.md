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
│              PREPROCESSING PIPELINE                      │
│  1. Unicode NFC normalization                           │
│  2. Extract auxiliary features (phone, url, money, ...)  │
│  3. Clean: lowercase, remove URL/phone, teencode norm   │
│  4. Vietnamese word segmentation (pyvi ViTokenizer)     │
│  5. Stopword removal                                    │
│  6. TF-IDF vectorization (max_features=5000, ngram 1-2) │
│  7. Combine: TF-IDF + auxiliary features matrix         │
│  8. Stratified Train/Val/Test split (60/20/20)          │
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
| `data/raw/dataset.csv` | Dataset tự thu thập (**không commit nếu > 10MB**) |
| `data/raw/dataset_template.csv` | Template CSV với header chuẩn |
| `data/processed/dataset_preprocessed.csv` | Sau clean + tokenize + auxiliary features |
| `data/processed/tfidf_vectorizer.pkl` | Fitted TF-IDF (fit trên train set only) |
| `data/processed/X_features.pkl` | TF-IDF + auxiliary features combined matrix |
| `data/processed/y_labels.pkl` | Labels array |
| `models/naive_bayes.pkl` | Trained Naive Bayes |
| `models/random_forest.pkl` | Trained Random Forest |
| `models/xgboost.pkl` | Trained XGBoost |
| `models/svm_linear.pkl` | Trained SVM Linear |

### 2. Preprocessing Pipeline (`src/preprocessing/`)

| Module | Chức năng |
|--------|-----------|
| `text_cleaner.py` | Unicode NFC, regex clean, teencode normalization |
| `tokenizer.py` | Vietnamese word segmentation (pyvi) |
| `stopwords.py` | Vietnamese stopword list & removal |
| `pipeline.py` | Full pipeline orchestrator: clean → tokenize → stopwords |

### 3. Feature Engineering (`src/feature_engineering.py`)

| Feature | Mô tả |
|---------|-------|
| TF-IDF matrix | max_features=5000, ngram=(1,2), sublinear_tf=True |
| `num_phone_numbers` | Đếm số điện thoại trong text |
| `num_urls` | Đếm URL trong text |
| `num_money_mentions` | Đếm cụm tiền tệ (triệu, tỷ, VND...) |
| `has_urgent_words` | 1 nếu có từ khẩn cấp |
| `text_length` | Độ dài text gốc |
| `num_exclamation` | Số dấu ! |

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
