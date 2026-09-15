# CS114 Final Project — Scam Detection Workspace

<p align="center">
  <b>Hệ thống Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam</b><br>
  <i>Môn học CS114 — Máy học (Machine Learning) | Lớp CS114.F31.CN2.TTNT | Nhóm 10</i><br>
  <a href="https://github.com/uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection"><code>uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection</code></a>
</p>

---

## 📌 Giới thiệu Workspace

Thư mục `draft/scam-detection` là không gian làm việc kỹ thuật chính của Nhóm 10. Nơi đây chứa toàn bộ mã nguồn Python (`src/`), dữ liệu (`data/`), sổ tay thực nghiệm (`notebooks/`), báo cáo biểu đồ (`reports/`), và ứng dụng web demo (`demo/`).

---

## 📂 Cấu trúc Thư mục

```
scam-detection/
├── data/
│   ├── raw/
│   │   ├── dataset_template.csv     ← Template định dạng chuẩn UTF-8-sig
│   │   ├── staging_thanh_normal.csv ← 1.773 mẫu SMS đời thực của Đặng Chí Thanh (100% PII masked)
│   │   ├── staging_cam_scam.csv     ← 205 mẫu lừa đảo đời thực của Bùi Thị Mỷ Cẩm (7 tầng kiểm toán)
│   │   ├── staging_son_scam.csv     ← 215 mẫu lừa đảo đời thực của Hoàng Cao Sơn (7 tầng kiểm toán)
│   │   └── dataset.csv              ← Bộ dữ liệu tích hợp chính thức (2.193 mẫu thực tế, 100% Zero Synthetic Text)
│   ├── processed/                   ← dataset_preprocessed.csv (2.193 dòng, 24 cột), real_world_test_thanh.csv, ma trận đặc trưng
│   ├── evidence/                    ← Ảnh chụp màn hình SMS minh chứng đời thực (Drive Vault) & JSON metadata
│   └── scripts/                     ← Bộ công cụ tự động hóa dữ liệu
│       ├── anonymize_sms.py         ← Ẩn danh hóa PII (che SĐT, STK, OTP, CCCD)
│       ├── drive_uploader.py        ← Đồng bộ ảnh minh chứng lên Google Drive Vault
│       ├── data_validation.py       ← Thẩm định chất lượng dữ liệu tự động
│       ├── split_data.py            ← Stratified 80/20 Train/Test split
│       └── collect_ieee_normal_dataset.py  ← Pipeline trích xuất dữ liệu chuẩn IEEE Access 2026
├── demo/
│   ├── app.py                       ← Web app Streamlit
│   └── components/                  ← Các module UI (Risk meter, Highlighting)
├── docs/                            ← Tài liệu kỹ thuật nội bộ
│   ├── code-standards.md            ← Quy chuẩn mã nguồn & phân công notebook
│   ├── project-overview-pdr.md      ← Tổng quan đề tài & chỉ số nghiệm thu
│   ├── project-roadmap.md           ← Lộ trình Sprint & biểu đồ Gantt
│   └── system-architecture.md       ← Kiến trúc hệ thống & pipeline NLP
├── models/                          ← Trọng số mô hình đã huấn luyện (.pkl)
├── notebooks/                       ← Jupyter Notebooks thực nghiệm
│   ├── 01_preprocessing.ipynb       ← [Thanh] Tiền xử lý văn bản
│   ├── 02_eda.ipynb                 ← [Thanh] Khám phá dữ liệu & Đặc trưng
│   ├── 03_model_naive_bayes.ipynb   ← [Cẩm] Huấn luyện Naive Bayes baseline
│   ├── 04_model_random_forest.ipynb ← [Sơn] Huấn luyện Random Forest
│   ├── 04_model_xgboost.ipynb       ← [Cẩm] Huấn luyện XGBoost
│   ├── 05_model_svm.ipynb           ← [Cẩm] Huấn luyện Support Vector Machine
│   └── 06_evaluation_xai.ipynb      ← [Thanh] So sánh mô hình & XAI
├── reports/
│   ├── figures/                     ← Biểu đồ ROC, Confusion Matrix, Learning Curves
│   └── model_comparison.csv         ← Bảng so sánh chỉ số tất cả mô hình
├── src/
│   ├── evaluation/                  ← Tính metrics, vẽ đồ thị, trích xuất XAI
│   ├── models/                      ← Định nghĩa wrapper các mô hình
│   ├── preprocessing/               ← Chuẩn hóa Unicode, tách từ pyvi, stopwords
│   └── utils/                       ← Helpers, constants, random seeds
├── requirements.txt                 ← Danh mục thư viện phụ thuộc
└── README.md                        ← Tài liệu hướng dẫn này
```

---

## ⚙️ Cài đặt Môi trường (Quickstart)

### 1. Khởi tạo môi trường ảo Python 3.10+
```bash
# Di chuyển vào workspace kỹ thuật
cd draft/scam-detection

# Khởi tạo venv
python3 -m venv .venv
source .venv/bin/activate

# Nâng cấp pip và cài đặt phụ thuộc
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Kiểm tra cài đặt và module dùng chung
```bash
python3 -c "from src.utils.helpers import RANDOM_STATE, set_seeds, SCAM_CATEGORIES; set_seeds(RANDOM_STATE); print('✅ Environment ready! Seed:', RANDOM_STATE); print('Categories:', SCAM_CATEGORIES)"
```

---

## 👥 Phân công Trách nhiệm & Notebooks

Nhằm tránh xung đột mã nguồn (merge conflicts), mỗi thành viên chịu trách nhiệm riêng trên từng notebook:

| Thành viên | MSSV | Trách nhiệm chính | Notebook phụ trách |
|------------|------|-------------------|-------------------|
| **Đặng Chí Thanh** *(PM & Lead)* | `25730067` | Data Preprocessing, Feature Engineering, Evaluation, XAI, Packaging | `01_preprocessing.ipynb`<br>`02_eda.ipynb`<br>`06_evaluation_xai.ipynb` |
| **Bùi Thị Mỷ Cẩm** | `25730013` | Baseline & Advanced Models (NB, XGBoost, SVM) | `03_model_naive_bayes.ipynb`<br>`04_model_xgboost.ipynb`<br>`05_model_svm.ipynb` |
| **Hoàng Cao Sơn** | `25730061` | Data Collection Lead, Random Forest, Streamlit Demo UI | `04_model_random_forest.ipynb`<br>`demo/app.py` |

---

## 🎯 Chỉ số Nghiệm thu Cốt lõi (Acceptance Criteria)

- **F1-Score tổng thể:** ≥ 88% trên tập kiểm thử.
- **Recall lớp Lừa đảo (Scam):** ≥ 92% (ưu tiên giảm thiểu tối đa bỏ sót tin nhắn nguy hiểm).
- **So sánh mô hình:** Tối thiểu 3 thuật toán khác biệt (MultinomialNB, Random Forest / XGBoost, LinearSVC).
- **Phân tích Overfitting:** Learning Curves (Train vs Validation) qua 5-Fold Cross Validation.
- **Explainable AI (XAI):** Trích xuất top 20 từ khóa kích hoạt tâm lý lừa đảo.
- **Demo Web:** Chạy ổn định trên localhost với tính năng phân loại + thanh đo nguy cơ + bôi đỏ từ khóa cảnh báo.
