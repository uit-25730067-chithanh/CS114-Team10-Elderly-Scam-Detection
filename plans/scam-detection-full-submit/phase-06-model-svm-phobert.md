# Phase 06 — Modeling — SVM (Optional: PhoBERT)

**Parent plan:** [plan.md](./plan.md)  
**Previous phase:** [Phase 05 — Modeling — Random Forest & XGBoost](./phase-05-model-rf-xgboost.md)  
**Next phase:** [Phase 07 — Evaluation & XAI](./phase-07-evaluation-xai.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Cẩm** |
| Priority | P1 |
| Status | `passed` ✅ |
| Review | ⬜ Not reviewed |
| Estimated effort | 3–5h |
| Sprint | Sprint 2 Fast-Track (17/09 – 18/09/2026) |

## Context

SVM (Support Vector Machine) là mô hình thứ 3 bắt buộc theo yêu cầu thầy Thăng. Linear SVM rất hiệu quả cho text classification với TF-IDF features. Optional: Fine-tune PhoBERT nếu nhóm có thời gian.

## Implementation Steps

### Step 0 — Nạp Feature Matrices Từ Phase 03 (KHÔNG tự split lại)

> ⚠️ **BẮT BUỘC:** Load `X_train.pkl` / `X_test.pkl` đã có từ Phase 03. TUYỆT ĐỐI KHÔNG fit lại TF-IDF hay split lại dataset — sẽ tạo split khác, phá vỡ consistency với Phase 04 và Phase 07.

```python
import joblib
from pathlib import Path
from src.utils import RANDOM_STATE

DATA_DIR = Path("data/processed")

X_train = joblib.load(DATA_DIR / "X_train.pkl")   # (1754, 5015) sparse CSR
X_test  = joblib.load(DATA_DIR / "X_test.pkl")    # (439, 5015)  sparse CSR
y_train = joblib.load(DATA_DIR / "y_train.pkl")   # 336 scam / 1418 normal
y_test  = joblib.load(DATA_DIR / "y_test.pkl")    # 84 scam / 355 normal
```

### Step 1 — SVM Linear

```python
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from src.utils import RANDOM_STATE

# LinearSVC + CalibratedClassifierCV để có predict_proba
svm_base = LinearSVC(
    C=1.0,
    class_weight='balanced',
    random_state=RANDOM_STATE,
    max_iter=5000,
)
svm_model = CalibratedClassifierCV(svm_base, cv=5)
svm_model.fit(X_train, y_train)
```

### Step 2 — SVM RBF Kernel (Alternative)

```python
from sklearn.svm import SVC

svm_rbf = SVC(
    kernel='rbf',
    C=1.0,
    gamma='scale',
    class_weight='balanced',
    random_state=RANDOM_STATE,
    probability=True,
)
# ⚠️ RBF SVM chậm trên sparse matrix lớn — cân nhắc subsample hoặc PCA
```

### Step 3 — Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'estimator__C': [0.01, 0.1, 1.0, 10.0],
}
grid_svm = GridSearchCV(
    CalibratedClassifierCV(LinearSVC(class_weight='balanced', random_state=RANDOM_STATE)),
    param_grid, cv=5, scoring='f1', n_jobs=-1,
)
grid_svm.fit(X_train, y_train)
```

### Step 4 — (Optional) PhoBERT Fine-tuning

> ⚠️ Chỉ thực hiện nếu có đủ thời gian và GPU resources.

```python
# PhoBERT approach (sketch):
# 1. pip install transformers torch
# 2. Load vinai/phobert-base
# 3. Tokenize với PhoBERTTokenizer
# 4. Fine-tune classification head
# 5. Train 3-5 epochs
```

### Step 5 — Save Model

```python
import joblib
joblib.dump(svm_model, "models/svm_linear.pkl")
```


## 🔌 Interface Contract — Model Output (Phase 06 → Phase 08)

> [!IMPORTANT]
> Phase 08 (Demo UI) **phụ thuộc** vào output format chính xác từ Phase 06. Đây là hợp đồng cứng giữa Cẩm (train model) và Sơn (build app). Phải thống nhất trước khi bắt đầu code Phase 08.

| Field | Spec bắt buộc |
|---|---|
| **Format lưu model** | `joblib` — `joblib.dump(bundle, 'models/best_model_bundle.pkl')` |
| **Bundle structure** | `{'model': calibrated_svc, 'vectorizer': tfidf_vectorizer, 'aux_scaler': auxiliary_scaler, 'feature_names': feature_names, 'model_name': 'SVM Linear', 'threshold': 0.5}` |
| **Path chuẩn** | `models/best_model_bundle.pkl` (relative to repo root) |
| **sklearn version** | Phải khớp với `requirements.txt` — kiểm tra bằng `sklearn.__version__` trước khi lưu |
| **Không gian đặc trưng** | 5.015 chiều kết hợp: 5.000 TF-IDF N-grams + 15 đặc trưng phụ đã chuẩn hóa (`aux_scaler`) |
| **Input format** | Raw text string → clean & tokenize → TF-IDF & aux features → hstack → model.predict_proba |
| **Output format** | Hàm `predict_raw_text()` (xem `05_model_svm.ipynb` mục 11) trả về `{'label': int, 'risk_score': float}`. `highlight_keywords` **chưa** được đóng gói ở Phase 06 — sẽ do Phase 07 (XAI/SHAP — Thanh) hoặc Phase 08 bổ sung ở tầng UI. |

```python
# Mẫu sử dụng chuẩn trong Streamlit (Phase 08 — hỗ trợ 5.015 chiều)
import joblib
import pandas as pd
from scipy.sparse import csr_matrix, hstack
from src.feature_engineering_config import AUX_FEATURE_COLS
from src.preprocessing.pipeline import preprocess_pipeline

bundle = joblib.load('models/best_model_bundle.pkl')
# 1. Tiền xử lý văn bản & trích xuất đặc trưng phụ (chuẩn train: clean, segment, remove_stopwords)
cleaned_text, aux_dict = preprocess_pipeline(user_input)

# 2. Chuẩn hóa 15 đặc trưng phụ theo đúng thứ tự cột AUX_FEATURE_COLS
aux_df = pd.DataFrame([aux_dict])[AUX_FEATURE_COLS]
aux_scaled = bundle['aux_scaler'].transform(aux_df.values)  # .values: tránh UserWarning "fitted without feature names"

# 3. Biến đổi TF-IDF 5.000 chiều
tfidf_vec = bundle['vectorizer'].transform([cleaned_text])

# 4. Hợp nhất 5.015 chiều & dự đoán
full_vec = hstack([tfidf_vec, csr_matrix(aux_scaled)])
proba = float(bundle['model'].predict_proba(full_vec)[0][1])
label = 1 if proba >= bundle.get('threshold', 0.5) else 0
```

## Checklist

- [x] SVM Linear trained với best C (`C=10.0`, GridSearchCV 5-fold, CV-F1=0.9567)
- [x] Classification report recorded (xem Evidence Section)
- [x] Confusion Matrix plotted (`reports/figures/svm_confusion_matrix.png`)
- [x] Learning Curve plotted (`reports/figures/svm_learning_curve.png`)
- [x] Model saved `models/svm_linear.pkl`
- [ ] (Optional) PhoBERT fine-tuned — bỏ qua (giới hạn thời gian/GPU trước hạn bảo vệ 23/09)
- [x] Notebook `05_model_svm.ipynb` chạy end-to-end
- [x] SVM RBF Kernel đối chứng (Step 2) — F1=0.8598 (val, `CalibratedClassifierCV(SVC(), ensemble=False)`), kém hơn Linear → giữ Linear
- [x] `models/best_model_bundle.pkl` đóng gói theo Interface Contract, kiểm thử end-to-end raw text → prediction thành công

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| SVM F1-Score | F1 competitive with RF/XGB |
| 3+ models compared | NB, RF, XGB, SVM all trained |
| Recall Scam | ≥ 90% |

## Evidence Section

```
--- SVM Linear (LinearSVC + CalibratedClassifierCV, C=10.0) — TEST SET (439 mẫu) ---
Accuracy:  0.9795
Precision: 0.9310
Recall:    0.9643   (81/84 mẫu lừa đảo được nhận diện đúng)
F1-Score:  0.9474
ROC-AUC:   0.9986

                 precision    recall  f1-score   support
Bình thường (0)     0.9915    0.9831    0.9873       355
    Lừa đảo (1)     0.9310    0.9643    0.9474        84
       accuracy                         0.9795       439

GridSearchCV (5-fold CV trên X_train, 4 giá trị C): best_params = {'estimator__C': 10.0}, CV-F1 = 0.9567

--- SVM RBF Kernel (đối chứng, chưa tune, X_tr/X_val) ---
F1 = 0.8598, Recall = 0.9020, Precision = 0.8214, ROC-AUC = 0.9768 (đã sửa dùng `CalibratedClassifierCV(SVC(),
ensemble=False)` thay `SVC(probability=True)` — tham số này bị deprecate ở sklearn 1.9, sẽ xóa ở 1.11)
→ Kém hơn Linear rõ rệt trên không gian TF-IDF thưa 5.015 chiều — giữ Linear làm lựa chọn chính thức.

--- So sánh 4 mô hình (Test Set 439 mẫu) ---
Naive Bayes    : F1 = 0.8864, Recall = 0.9286  (Phase 04 — 5.000 dims TF-IDF only)
Random Forest  : F1 = 0.9425, Recall = 0.9762  (Phase 05 — Sơn)
XGBoost        : F1 = 0.9535, Recall = 0.9762  (Phase 05 — Cẩm)
SVM Linear     : F1 = 0.9474, Recall = 0.9643  (Phase 06 — Cẩm)

Artifacts:
- models/svm_linear.pkl, models/svm_metrics.json
- models/best_model_bundle.pkl (model=SVM Linear + vectorizer + aux_scaler + feature_names + threshold=0.5 + metrics + metadata)
- reports/figures/svm_confusion_matrix.png, svm_roc_curve.png, svm_learning_curve.png, svm_feature_importance.png
- notebooks/05_model_svm.ipynb (12 sections, stripped outputs, sinh bởi notebooks/generate_svm_notebook.py)
- notebooks/build_best_model_bundle.py: tiện ích tái tạo best_model_bundle.pkl bằng model có F1 test cao nhất hiện có trong models/ (loại Naive Bayes vì khác không gian đặc trưng 5.000-dim)
- Self-test hợp đồng suy luận (raw text → predict_raw_text(), văn bản có dấu tiếng Việt chuẩn):
  mẫu SCAM ("...công an điều tra...chuyển khoản ngay 50 triệu...") → label=1, risk_score=0.9815
  mẫu NORMAL ("Ngân hàng thông báo số dư tài khoản...") → label=0, risk_score=0.1710

🛠️ ĐÍNH CHÍNH SAU CODE REVIEW (anh Thanh, 19/09) — đã tự kiểm chứng lại toàn bộ bằng code trước khi sửa:

1. **Lỗi phương pháp luận đã xác nhận:** bản gốc tính "độ quan trọng" bằng `np.abs(fold_coefs).mean(axis=0)`
   (lấy trị tuyệt đối TRƯỚC khi trung bình) → xóa mất dấu, nên không biết từ nào kéo về Lừa đảo, từ nào kéo
   về Bình thường. Đã sửa dùng `fold_coefs.mean(axis=0)` (trung bình CÓ DẤU) và tách 2 nhóm rõ ràng, vẽ lại
   `svm_feature_importance.png` dạng 2 cụm màu (đỏ=dương/Lừa đảo, xanh=âm/Bình thường):

   Top-10 kéo về LỪA ĐẢO (dương):        Top-10 kéo về BÌNH THƯỜNG (âm):
     thương_hiệu    +2.18                  number         −1.97
     đường_dẫn      +1.93                  mã             −1.18
     số_định_danh   +1.48                  money          −1.02
     số_tiền        +1.61                  sử_dụng        −0.97
     đang           +1.45                  shop           −0.91
     sẽ             +1.32                  trẻ_em         −0.85
     mày            +0.98                  hoặc           −0.83
     dieu tra       +0.84                  đón            −0.05 (nhỏ)
     họ_và_tên      +0.87                  đến            −0.45
     anh            +0.84                  sớm            −0.44

2. **2 nhận định trong bản gốc BỊ SAI (đã xác minh bằng code, không phải "chuyển từ tuyệt đối sang có dấu"
   đơn thuần):**
   - "mã" **KHÔNG** phải "vocab lừa đảo đúng" — hệ số thực là **−1.18 (kéo về Bình thường)**. Đây chính là
     nguyên nhân False Negative nguy hiểm: mẫu test thật `"Đơn hàng cần xác minh người nhận. Shipper sẽ
     gọi, bạn đọc giúp mã OTP vừa nhận để bên kho hoàn tất giao hàng."` (label=1, X_test vị trí 108) bị
     model dự đoán SAI thành Bình thường với risk_score chỉ **0.0688** — vì từ "mã" (xuất hiện 2 lần sau
     khi tách token "mã OTP"→"mã"+"xác_thực") kéo mạnh về phía Bình thường, lấn át các tín hiệu lừa đảo
     khác. Đây là lỗi thật, đã verify lại bằng cách chạy model trên đúng 439 mẫu test, không phải suy đoán.
   - "hoặc" **không nên** nằm trong nhóm "từ chức năng gây false positive" — hệ số là **−0.83 (kéo về Bình
     thường)**, tức nó không thể là nguyên nhân khiến 1 câu bị đẩy nhầm về Lừa đảo.

3. **Nghi vấn "con...bố mẹ" ở bản gốc cũng SAI Ở TẦNG SÂU HƠN cả vấn đề dấu:** không có từ nào trong
   "đang/sẽ/hoặc/anh" xuất hiện trong câu ví dụ "Con chào bố mẹ, con đến trường an toàn rồi, chiều con về
   sớm phụ bố mẹ đón em" — nên toàn bộ lý do nêu ra ở bản gốc không liên quan đến câu này. Đã tính lại
   CONTRIBUTION THẬT của từng feature (giá trị vector × hệ số) cho đúng câu này (SVM, proba=0.5643):
   ```
   text_length          contrib=+0.9827   (câu NGẮN hơn trung bình → kéo về Lừa đảo, do coef âm × z-score âm)
   is_unaccented        contrib=+0.4756   (câu CÓ dấu → kéo về Lừa đảo, cùng lý do dấu*dấu)
   num_money_mentions   contrib=+0.2133
   con                  contrib=+0.1949   (từ "con" xuất hiện 2 lần, coef=+0.468 — từ TF-IDF ảnh hưởng nhất)
   chào                 contrib=+0.0734
   ...                  (bố_mẹ chỉ contrib=+0.0194 — hầu như không ảnh hưởng, ngược với suy đoán ban đầu)
   ```
   → Nguyên nhân thật: (a) từ "con" đứng riêng lẻ (không phải cụm "bố_mẹ") có hệ số dương thật, hợp lý vì
   scam "con bị tai nạn cần tiền gấp" cũng dùng từ "con"; (b) 2 đặc trưng phụ số (`text_length`,
   `is_unaccented`) tạo hiệu ứng phụ do tương tác dấu âm×âm — đây là điểm cần Phase 07 (SHAP) làm rõ, KHÔNG
   phải do "văn phong/từ chức năng" như suy đoán ban đầu.

4. **ConvergenceWarning + UserWarning đã xác nhận và sửa:** `LinearSVC(max_iter=5000)` ở `C=10.0` thực sự
   phát `ConvergenceWarning` (đã tự chạy lại kiểm chứng); tăng `max_iter=10000` hết cảnh báo — đã áp dụng
   cho baseline, GridSearchCV và learning curve. Đã gỡ `warnings.filterwarnings("ignore")` toàn cục, chỉ ẩn
   riêng `InconsistentVersionWarning` (vô hại). `aux_scaler.transform(aux_df)` (DataFrame) phát
   `UserWarning: X has feature names, but StandardScaler was fitted without feature names` — đã xác nhận
   và sửa thành `.transform(aux_df.values)` ở `generate_svm_notebook.py`, `build_best_model_bundle.py`, và
   code mẫu Interface Contract phía trên.

5. **`.gitignore` đã sửa:** thêm `!**/models/svm_linear.pkl` (đã verify file 204KB, dưới ngưỡng 50MB) —
   giờ `svm_linear.pkl` được Git theo dõi, `build_best_model_bundle.py` sẽ không còn `[skip] SVM Linear`
   khi clone mới mà chưa train lại.

6. **Không áp dụng — đã phản biện có căn cứ:** đề xuất chạy `jupyter nbconvert --execute --inplace` để lưu
   output vào `05_model_svm.ipynb`. Đã kiểm tra: cả 4/4 notebook hiện có (NB, RF, XGBoost, SVM) đều có
   **0/10-13 cell mang output** (100% stripped), đúng theo quy ước ghi rõ tại `notebooks/README.md` mục
   "Dọn sạch Output trước khi Commit" (tránh phình repo + xung đột merge nhị phân — kết quả chính thức lưu
   ở `reports/figures/*.png` và `models/*_metrics.json`). `jupyter`/`nbconvert` cũng không có trong
   `requirements.txt`. → Giữ nguyên stripped-outputs để nhất quán với NB/RF/XGBoost.

⚠️ RỦI RO HẠ TẦNG — sklearn version không khớp giữa các artifact (đã fix 1 phần):
`data/processed/tfidf_vectorizer.pkl` và `aux_scaler.pkl` được pickle từ Phase 03 bằng sklearn 1.8.0,
trong khi môi trường Phase 04–06 chạy sklearn 1.9.0 → mỗi lần load phát `InconsistentVersionWarning`
(nay bị ẩn có chủ đích, xem mục 4). Đã **pin cứng `scikit-learn==1.9.0`** trong `requirements.txt` (trước
đây là `>=1.5.0`) để cả nhóm dùng cùng version từ giờ. Riêng con số "trượt 8% xác suất giữa bản 1.8.0 và
1.9.0 do `_SigmoidCalibration`" trong review gốc: **chưa verify được** (máy hiện tại không có sẵn sklearn
1.8.0 để đối chứng song song) — không bác bỏ, chỉ ghi nhận là chưa có bằng chứng trực tiếp. Khuyến nghị
còn lại (re-serialize `tfidf_vectorizer.pkl`/`aux_scaler.pkl` cùng version 1.9.0) nên để Thanh làm vì đây
là artifact gốc của Phase 03, không thuộc phạm vi Phase 06.
```

## Phase Summary

> ✅ **PASSED.** SVM Linear (LinearSVC + CalibratedClassifierCV, `C=10.0` từ GridSearchCV 5-fold) đạt **F1=0.9474, Recall=96.43%, ROC-AUC=0.9986** trên test set 439 mẫu — vượt Success Criteria (F1 cạnh tranh RF/XGB, Recall ≥ 90%) và target chung của đề tài (F1 ≥ 0.88). Đối chứng SVM RBF (F1=0.8598) xác nhận Linear là lựa chọn đúng cho không gian TF-IDF thưa. Đã đóng gói `models/best_model_bundle.pkl` đúng Interface Contract (bổ sung `metrics` + `metadata` theo `models/README.md`) và kiểm thử thành công luồng suy luận end-to-end raw text → prediction — sẵn sàng bàn giao cho Phase 08 (Sơn).
>
> ⚠️ **Lưu ý cho Phase 07 (Thanh) — 3 điểm cần quyết định trước khi Phase 08 chốt bản demo:**
> 1. **Chọn model cuối cùng:** F1 của SVM (0.9474) thấp hơn XGBoost (0.9535) nhưng cao hơn Random Forest (0.9425). `best_model_bundle.pkl` hiện đóng gói **SVM** theo đúng `model_name` mẫu trong Interface Contract gốc của Phase 06 — trong khi `models/README.md` định nghĩa file này là "Model tốt nhất (F1 cao nhất)" tức về lý thuyết nên là XGBoost. Đã chuẩn bị sẵn `notebooks/build_best_model_bundle.py` để re-bundle bằng model bất kỳ (tự động chọn F1 cao nhất trong số các `.pkl` có sẵn) — Phase 07 chỉ cần chạy lại script này sau khi quyết định, xem mục 2 trước khi chốt.
> 2. **False Negative "mã OTP" đã xác nhận thật (rủi ro cao hơn case "con...bố mẹ" ban đầu):** mẫu test `"...Shipper sẽ gọi, bạn đọc giúp mã OTP..."` (label=1, X_test vị trí 108) bị SVM dự đoán SAI thành Bình thường, risk_score=0.0688 — vì từ "mã" có hệ số −1.18 (kéo về Bình thường). Đây là 1/3 false negative thật trên tập test chính thức (439 mẫu), không phải suy đoán thủ công. Case "con...bố mẹ" ban đầu có sai ở khâu phân tích (xem Evidence Section mục 3) — nguyên nhân thật là từ "con" + tương tác 2 đặc trưng phụ số, không phải "đang/sẽ/hoặc/anh". Cả 2 case nên đưa vào Phase 07 SHAP để phân tích đúng.
> 3. **sklearn version đã pin `==1.9.0`** trong `requirements.txt` (fix một phần) — còn `tfidf_vectorizer.pkl`/`aux_scaler.pkl` (Phase 03) vẫn mang pickle-version 1.8.0, cần Thanh re-serialize lại cùng version vì đây là artifact gốc Phase 03.
>
> PhoBERT fine-tuning (optional) không thực hiện do giới hạn thời gian/GPU trước hạn bảo vệ 23/09/2026.

## Commit

```bash
git add notebooks/05_model_svm.ipynb notebooks/generate_svm_notebook.py notebooks/build_best_model_bundle.py \
        models/svm_metrics.json models/svm_linear.pkl models/best_model_bundle.pkl reports/figures/svm_*.png \
        .gitignore requirements.txt \
        plans/scam-detection-full-submit/phase-06-model-svm-phobert.md
# svm_linear.pkl (204KB) và best_model_bundle.pkl (490KB) đều có exception trong .gitignore — commit trực tiếp
git commit -m "feat(phase06): SVM trained (F1=0.9474), fix signed-coefficient bug, pin sklearn==1.9.0"
```
