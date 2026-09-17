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
aux_scaled = bundle['aux_scaler'].transform(aux_df)

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
- [x] SVM RBF Kernel đối chứng (Step 2) — F1=0.8276 (val), kém hơn Linear → giữ Linear
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
F1 = 0.8276, Recall = 0.9412, Precision = 0.7385, ROC-AUC = 0.9768
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

⚠️ PHÁT HIỆN CẦN LƯU Ý CHO PHASE 07 (XAI):
Khi thử nghiệm thủ công với câu bình thường dạng "Con chào bố mẹ, con đến trường an toàn rồi, chiều con
về sớm phụ bố mẹ đón em" (có dấu đầy đủ), CẢ 2 mô hình đều lệch về phía "Lừa đảo":
  - SVM Linear:  scam-proba = 0.6447 (label=1, SAI — false positive, vượt ngưỡng 0.5)
  - XGBoost:     scam-proba = 0.9852 (label=1, SAI — false positive rất tự tin)
Nghi vấn: mẫu câu "con ... bố mẹ" trùng lặp bề mặt với các đặc trưng của category `family_emergency`
(kịch bản lừa đảo "con bị tai nạn cần tiền gấp") trong tập train (chỉ 336 mẫu lừa đảo — dễ overfit theo
n-gram bề mặt thay vì ngữ cảnh khẩn cấp/tiền bạc thực sự). Vì đây chỉ là 1 mẫu thử thủ công (không nằm
trong 439 mẫu test chính thức) nên KHÔNG dùng để đảo ngược kết luận F1 ở trên, nhưng đáng để Phase 07
(Thanh) đào sâu bằng SHAP — nếu xác nhận là lỗi hệ thống, có thể cần bổ sung dữ liệu train đối chứng
(câu bình thường có chữ "con", "bố mẹ") hoặc hiệu chỉnh lại 15 đặc trưng phụ liên quan `family_emergency`.

🔎 BẰNG CHỨNG BỔ SUNG — Top-20 |hệ số| SVM Linear (trích từ models/svm_linear.pkl, đã re-audit sau khi train):
  1. thương_hiệu   2.18   6. đang    1.45   11. sử_dụng  0.97   16. trẻ_em      0.85
  2. number        1.97   7. sẽ      1.32   12. thuế     0.95   17. bạn_number  0.84
  3. đường_dẫn     1.93   8. mã      1.18   13. shop     0.91   18. anh         0.84
  4. số_tiền       1.61   9. money   1.02   14. tao      0.88   19. dieu tra    0.84
  5. số_định_danh  1.48  10. mày     0.98   15. họ_và_tên 0.87   20. hoặc        0.83
Phần lớn hợp lý (số_tiền, mã, họ_và_tên, thuế, đường_dẫn — đúng vocab lừa đảo). Nhưng 4/20 từ là TỪ CHỨC
NĂNG PHỔ THÔNG không mang nghĩa lừa đảo: "đang", "sẽ", "hoặc", "anh" — nằm trong top-7 với trọng số khá
cao (1.3–1.45). Đây là bằng chứng cụ thể CỦNG CỐ nghi vấn false positive "con...bố mẹ" ở trên: model có
thể đang học một phần theo văn phong/cách xưng hô thay vì thuần nội dung lừa đảo, do tập scam chỉ có 336
mẫu. → Ưu tiên đưa danh sách này cho Phase 07 làm input đối chiếu SHAP thay vì suy đoán lại từ đầu.

⚠️ RỦI RO HẠ TẦNG — sklearn version không khớp giữa các artifact:
`data/processed/tfidf_vectorizer.pkl` và `aux_scaler.pkl` được pickle từ Phase 03 bằng sklearn 1.8.0,
trong khi môi trường Phase 04–06 hiện tại chạy sklearn 1.9.0 (`requirements.txt` chỉ ghi `>=1.5.0`, không
pin cứng) → mỗi lần load đều phát `InconsistentVersionWarning`. `best_model_bundle.pkl` hiện mang cả
object cũ (1.8.0) lẫn model mới train (1.9.0) trong cùng 1 file. Nếu máy của Sơn (Phase 08) cài sklearn
version khác nữa, cảnh báo sẽ lặp lại hoặc tệ hơn có thể predict_proba lệch kết quả giữa các máy. Khuyến
nghị: pin cứng `scikit-learn==1.9.0` (hoặc version cả nhóm thống nhất) trong `requirements.txt` trước khi
Phase 08 build demo, và re-serialize `tfidf_vectorizer.pkl`/`aux_scaler.pkl` cùng version để dứt điểm.
```

## Phase Summary

> ✅ **PASSED.** SVM Linear (LinearSVC + CalibratedClassifierCV, `C=10.0` từ GridSearchCV 5-fold) đạt **F1=0.9474, Recall=96.43%, ROC-AUC=0.9986** trên test set 439 mẫu — vượt Success Criteria (F1 cạnh tranh RF/XGB, Recall ≥ 90%) và target chung của đề tài (F1 ≥ 0.88). Đối chứng SVM RBF (F1=0.8276) xác nhận Linear là lựa chọn đúng cho không gian TF-IDF thưa. Đã đóng gói `models/best_model_bundle.pkl` đúng Interface Contract (bổ sung `metrics` + `metadata` theo `models/README.md`) và kiểm thử thành công luồng suy luận end-to-end raw text → prediction — sẵn sàng bàn giao cho Phase 08 (Sơn).
>
> ⚠️ **Lưu ý cho Phase 07 (Thanh) — 3 điểm cần quyết định trước khi Phase 08 chốt bản demo:**
> 1. **Chọn model cuối cùng:** F1 của SVM (0.9474) thấp hơn XGBoost (0.9535) nhưng cao hơn Random Forest (0.9425). `best_model_bundle.pkl` hiện đóng gói **SVM** theo đúng `model_name` mẫu trong Interface Contract gốc của Phase 06 — trong khi `models/README.md` định nghĩa file này là "Model tốt nhất (F1 cao nhất)" tức về lý thuyết nên là XGBoost. Đã chuẩn bị sẵn `notebooks/build_best_model_bundle.py` để re-bundle bằng model bất kỳ (tự động chọn F1 cao nhất trong số các `.pkl` có sẵn) — Phase 07 chỉ cần chạy lại script này sau khi quyết định, xem mục 2 trước khi chốt.
> 2. **Điều tra false positive "con...bố mẹ":** xem cảnh báo trong Evidence Section — cả SVM và XGBoost đều gắn nhãn sai một câu nhắn tin gia đình bình thường thành lừa đảo. Bằng chứng bổ sung: top-20 hệ số SVM có 4 từ chức năng phổ thông ("đang", "sẽ", "hoặc", "anh") với trọng số cao bất thường — gợi ý model học theo văn phong thay vì nội dung. Nên xác minh bằng SHAP (Phase 07) trước khi chốt model cuối, vì đây là loại lỗi rủi ro cao khi demo trực tiếp trước thầy Thăng (báo động giả với tin nhắn con cháu hỏi thăm — đúng nhóm đối tượng người cao tuổi mà đề tài hướng tới).
> 3. **Pin sklearn version:** `tfidf_vectorizer.pkl`/`aux_scaler.pkl` (Phase 03, sklearn 1.8.0) và các model Phase 04–06 (sklearn 1.9.0 trên máy Cẩm) không cùng version, `requirements.txt` chưa pin cứng — nên thống nhất 1 version cho cả nhóm trước khi Phase 08 deploy, tránh predict_proba lệch giữa các máy.
>
> PhoBERT fine-tuning (optional) không thực hiện do giới hạn thời gian/GPU trước hạn bảo vệ 23/09/2026.

## Commit

```bash
git add notebooks/05_model_svm.ipynb notebooks/generate_svm_notebook.py \
        models/svm_metrics.json reports/figures/svm_*.png \
        plans/scam-detection-full-submit/phase-06-model-svm-phobert.md
# models/svm_linear.pkl và models/best_model_bundle.pkl bị .gitignore (**/models/*.pkl) — quản lý ngoài Git theo quy ước dự án
git commit -m "feat(phase06): SVM trained (F1=0.9474), best_model_bundle.pkl packaged for Phase 08"
```
