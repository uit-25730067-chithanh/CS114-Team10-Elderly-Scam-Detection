# Hệ Thống Phát Hiện Tin Nhắn & Kịch Bản Thao Túng Tâm Lý Lừa Đảo Nhắm Vào Người Cao Tuổi Tại Việt Nam

<p align="center">
  <img src="./docs/cover.png" alt="Ảnh bìa đồ án CS114" width="100%" style="border-radius: 8px;" />
</p>

<p align="center">
  <a href="https://www.uit.edu.vn/"><img src="https://img.shields.io/badge/Trường-ĐH%20Công%20nghệ%20Thông%20tin%20(UIT)-0052cc.svg" alt="UIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python 3.10+"></a>
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Ứng%20dụng-Streamlit%20Cloud-FF4B4B.svg" alt="Streamlit"></a>
  <a href="https://scikit-learn.org/"><img src="https://img.shields.io/badge/Thư%20viện-scikit--learn%20%7C%20XGBoost-orange.svg" alt="Scikit-Learn"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/Giấy%20phép-MIT-green.svg" alt="Giấy phép MIT"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/Language-English-blue.svg" alt="English"></a>
</p>

---

## 📌 Tổng Quan Đề Tài

Kho lưu trữ này công khai kết quả nghiên cứu và mã nguồn thực nghiệm của **Đồ án cuối kỳ môn Máy học (CS114.F31.CN2.TTNT)** tại **Trường Đại học Công nghệ Thông tin - ĐHQG-HCM (UIT)**.

Đề tài giải quyết vấn nạn thao túng tâm lý và lừa đảo qua mạng viễn thông nhắm vào đối tượng dễ bị tổn thương nhất trong xã hội hiện nay: **Người cao tuổi tại Việt Nam**. Hệ thống kết hợp kỹ thuật tiền xử lý ngôn ngữ tự nhiên (NLP) tiếng Việt đặc thù, trích xuất đặc trưng hai không gian (TF-IDF từ ngữ và 15 đặc trưng nhận thức/tâm lý), thực nghiệm đối chứng 4 họ mô hình máy học giám sát, giải thích quyết định dự đoán bằng XAI (SHAP), và cung cấp giao diện web trực quan tối ưu khả năng tiếp cận cho người lớn tuổi.

### Điểm Nhấn Nghiên Cứu
* **Chính Sách Không Dữ Liệu Nhân Tạo (Zero Synthetic Text):** Toàn bộ tập dữ liệu gồm **2.193 tin nhắn tiếng Việt thực tế** (1.773 mẫu bình thường và 420 mẫu lừa đảo có truy vết chứng cứ) thu thập từ cổng tin tức, cơ quan công an, trang cảnh báo lừa đảo và tin nhắn thực tế của người dân.
* **Không Gian Đặc Trưng Kép (Dual-Space Representation):** Hợp nhất ma trận TF-IDF 5.000 chiều và 15 đặc trưng bổ trợ phản ánh độ khẩn cấp, mạo danh cơ quan công quyền, bẫy trúng thưởng/tài chính, tỷ lệ chữ hoa và dấu hiệu liên lạc bất thường.
* **Hiệu Năng Vượt Trội:** Trong 4 họ mô hình được thử nghiệm, **XGBoost** đạt hiệu năng cao nhất với **F1-Score: 95.35%**, **Recall bắt lừa đảo: 97.62%**, và **PR-AUC: 0.9969**.
* **Giao Diện Hướng Người Cao Tuổi:** Web demo Streamlit hỗ trợ phóng to kích thước chữ, đồng hồ đo mức độ nguy cơ độ tương phản cao, bôi đỏ cụm từ thao túng tâm lý và đưa ra lời khuyên an toàn dễ hiểu.

---

## 🏛️ Kiến Trúc Hệ Thống

```text
Tin nhắn đầu vào (SMS / Chat)
    │
    ▼
[Tiền Xử Lý & Chuẩn Hóa Văn Bản]
    ├── Chuẩn hóa Unicode NFC
    ├── Thay thế 160+ từ điển Teencode & tiếng lóng tiếng Việt
    ├── Ẩn thông tin định danh PII ([PHONE], [URL], [OTP], [MONEY])
    └── Tách từ tiếng Việt (pyvi / underthesea)
    │
    ├───────────────────────────────────────────────┐
    ▼                                               ▼
[Không Gian Từ Vựng (TF-IDF)]          [Đặc Trưng Bổ Trợ (15 Biến Tâm Lý)]
├── Unigrams + Bigrams (Tối đa 5.000)   ├── Điểm số áp lực thời gian & cấp bách
└── Sublinear Term Frequency Scaling    ├── Mức độ mạo danh công quyền / công an
                                        ├── Mật độ bẫy quà tặng / tài chính / trúng thưởng
                                        └── Dấu hiệu cú pháp (Chữ hoa, dấu chấm than)
    │                                               │
    └───────────────────────┬───────────────────────┘
                            ▼
                [Hợp Nhất Đặc Trưng (Fusion)]
                (Không gian đặc trưng: 5.015 chiều)
                            │
                            ▼
                [Bộ Phân Loại Máy Học]
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   Naive Bayes        Random Forest          XGBoost (Champion)
  (Baseline)         (F1: 94.25%)           (F1: 95.35%)
                            │
                            ▼
             [Động Cơ Suy Luận & Giải Thích (XAI)]
            ├── Xác suất cảnh báo nguy cơ
            ├── Phân loại nhóm bẫy (Áp lực công quyền, Khẩn cấp gia đình, Quà tặng, Dịch vụ công)
            └── Trích xuất Top-20 đặc trưng chi phối dự đoán qua SHAP
                            │
                            ▼
          [Giao Diện Web Trực Quan Hóa (Streamlit)]
```

---

## 📊 Bảng Kết Quả Thực Nghiệm Đối Sánh

Toàn bộ các mô hình được đánh giá trên tập kiểm thử độc lập (Holdout Test 20%) với kiểm định chéo Stratified 5-Fold. Quá trình tiền xử lý tuân thủ nghiêm ngặt nguyên tắc chống rò rỉ dữ liệu (Zero Data Leakage).

| Mô hình | Xử lý mất cân bằng | Accuracy | Precision | Recall (Scam) | F1-Score | ROC-AUC | Thời gian huấn luyện |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Multinomial Naive Bayes** | Class Weights | 95.90% | 85.00% | 92.54% | **88.64%** | 0.9782 | < 1s |
| **Random Forest** | Balanced Subsample | 97.95% | 91.11% | **97.62%** | **94.25%** | 0.9972 | 14.8s |
| **XGBoost (Vô địch)** | `scale_pos_weight` | **98.41%** | **93.33%** | **97.62%** | **95.35%** | **0.9986** | 8.2s |
| **Linear SVM** | Calibrated Sigmoid | 98.18% | 92.22% | 96.43% | **94.74%** | **0.9986** | 3.5s |

*Chi tiết biểu đồ ROC, PR Curves, ma trận nhầm lẫn và kết quả Ablation Study xem tại thư mục [`reports/figures/`](reports/figures/) và [`reports/model_comparison.csv`](reports/model_comparison.csv).*

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Thử

### Yêu cầu môi trường
* Python 3.10 trở lên
* Git

### 1. Tải mã nguồn
```bash
git clone https://github.com/uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection.git
cd CS114-Team10-Elderly-Scam-Detection
```

### 2. Thiết lập môi trường ảo
```bash
python3 -m venv .venv
source .venv/bin/activate  # Trên Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Khởi chạy ứng dụng Web Demo
```bash
streamlit run demo/app.py
```
Truy cập trình duyệt tại địa chỉ `http://localhost:8501`.

### 4. Chạy kiểm thử tự động
```bash
python3 -m unittest discover tests/
```

---

## 📂 Cấu Trúc Thư Mục Repository

```text
.
├── data/                                # Dữ liệu nghiên cứu
│   ├── processed/                       # Ma trận đặc trưng và bộ vectorizer
│   │   ├── tfidf_vectorizer.pkl         # Bộ TF-IDF vectorizer (5.000 từ vựng)
│   │   ├── aux_scaler.pkl               # Bộ chuẩn hóa đặc trưng bổ trợ
│   │   └── real_world_test_thanh.csv    # Tập đánh giá thực tế độc lập
│   └── raw/
│       └── dataset.csv                  # 2.193 mẫu SMS thực tế (Zero Synthetic Text)
├── demo/                                # Ứng dụng Web Demo Streamlit
│   ├── app.py                           # Điểm khởi chạy ứng dụng chính
│   └── components/                      # Các thành phần giao diện (Thanh đo rủi ro, cố vấn)
├── docs/                                # Tài liệu kỹ thuật kiến trúc
│   ├── cover.png                        # Ảnh bìa học thuật đồ án
│   ├── code-standards.md                # Quy chuẩn lập trình Python
│   └── system-architecture.md           # Đặc tả luồng xử lý hệ thống
├── models/                              # Trọng số mô hình đã huấn luyện (< 5MB)
│   ├── best_model_bundle.pkl            # Gói mô hình vô địch XGBoost tích hợp
│   ├── naive_bayes.pkl                  # Mô hình cơ sở Naive Bayes
│   ├── random_forest.pkl                # Mô hình Random Forest đã tinh chỉnh
│   ├── svm_linear.pkl                   # Mô hình Linear SVM hiệu chuẩn xác suất
│   └── xgboost.pkl                      # Mô hình XGBoost đã tinh chỉnh
├── notebooks/                           # Sổ tay nghiên cứu thực nghiệm Jupyter
│   ├── 01_data_preprocessing.ipynb     # Tiền xử lý dữ liệu và làm sạch teencode
│   ├── 02_eda_feature_engineering.ipynb # Khám phá phân phối và tạo đặc trưng bổ trợ
│   ├── 03_baseline_naive_bayes.ipynb    # Huấn luyện mô hình cơ sở Naive Bayes
│   ├── 04_random_forest.ipynb           # Tinh chỉnh siêu tham số Random Forest
│   ├── 05_xgboost.ipynb                 # Huấn luyện và tối ưu mô hình XGBoost
│   ├── 06_svm.ipynb                     # Phân loại và hiệu chuẩn xác suất SVM
│   └── 07_evaluation_xai.ipynb          # Đánh giá đa mô hình và phân tích XAI SHAP
├── reports/                             # Minh chứng học thuật và biểu đồ thực nghiệm
│   ├── figures/                         # 32 biểu đồ trực quan hóa độ phân giải cao 300 DPI
│   ├── ablation_studies.json            # Dữ liệu thực nghiệm bóc tách đặc trưng
│   └── model_comparison.csv             # Bảng đối sánh số liệu định lượng giữa các mô hình
├── slide/                               # Slide thuyết trình báo cáo đồ án
│   ├── [Nhom10]_Slide_ScamDetection.pdf # Slide báo cáo hoàn chỉnh (PDF 22 trang)
│   └── script.md                        # Kịch bản thuyết trình bảo vệ 15 phút
├── src/                                 # Gói mã nguồn Python dùng chung
│   ├── preprocessing/                   # Bộ làm sạch, tách từ và từ điển teencode
│   ├── evaluation/                      # Tính toán độ đo, XAI giải thích và ablation
│   ├── feature_engineering.py           # Bộ trích xuất 15 đặc trưng tâm lý
│   └── utils/                           # Hàm tiện ích nạp dữ liệu
├── tests/                               # Bộ kiểm thử đơn vị và tích hợp
├── requirements.txt                     # Danh sách thư viện phụ thuộc
└── LICENSE                              # Giấy phép phần mềm MIT
```

---

## 📄 Ấn Phẩm Học Thuật

* **Báo cáo toàn văn (PDF 32 trang):** Đã nộp chính thức trên hệ thống UIT Moodle LMS theo quy chế môn học. *(Nhóm bảo lưu quyền tác giả và phòng chống sao chép học thuật; vui lòng liên hệ nhóm nếu cần tham khảo phục vụ nghiên cứu).*
* **Slide thuyết trình (PDF 22 trang):** [`slide/[Nhom10]_Slide_ScamDetection.pdf`](slide/[Nhom10]_Slide_ScamDetection.pdf)
* **Website Demo trực tuyến:** [Streamlit Community Cloud](https://elderly-scam-detection.streamlit.app)

---

## 👥 Đội Ngũ Thực Hiện & Ghi Nhận

**Đơn vị:** Khoa Khoa học Máy tính, Trường Đại học Công nghệ Thông tin - ĐHQG-HCM (UIT)  
**Môn học:** Máy học (CS114.F31.CN2.TTNT)  
**Giảng viên hướng dẫn:** ThS. Cáp Phạm Đình Thăng (`thangcpd@uit.edu.vn`)  

### Thành viên Nhóm 10
* **Đặng Chí Thanh (Nhóm trưởng / Quản lý dự án)** — MSSV: `25730067`
  * *Phụ trách:* Kiến trúc dữ liệu, Pipeline tiền xử lý không rò rỉ, Kỹ thuật trích xuất đặc trưng, Khám phá dữ liệu EDA, Tích hợp hệ thống.
* **Bùi Thị Mỷ Cẩm** — MSSV: `25730013`
  * *Phụ trách:* Thu thập dữ liệu thực tế, Huấn luyện mô hình (Naive Bayes, XGBoost, SVM), Tinh chỉnh siêu tham số, Đánh giá độ đo.
* **Hoàng Cao Sơn** — MSSV: `25730061`
  * *Phụ trách:* Thu thập dữ liệu thực tế, Huấn luyện mô hình (Random Forest), Phát triển giao diện Web Demo Streamlit, Kiểm thử UX người cao tuổi.

---

## 📜 Trích Dẫn Học Thuật

Nếu công trình nghiên cứu, mã nguồn hoặc dữ liệu đối chứng của đồ án này hữu ích cho các nghiên cứu tiếp theo của bạn, vui lòng trích dẫn:

```bibtex
@misc{uit_cs114_elderly_scam_detection_2026,
  author       = {Đặng Chí Thanh and Bùi Thị Mỷ Cẩm and Hoàng Cao Sơn},
  title        = {Hệ Thống Phát Hiện Tin Nhắn và Kịch Bản Thao Túng Tâm Lý Lừa Đảo Nhắm Vào Người Cao Tuổi Tại Việt Nam},
  year         = {2026},
  publisher    = {GitHub},
  journal      = {Đồ án môn học Máy học, Trường Đại học Công nghệ Thông tin, ĐHQG-HCM},
  howpublished = {\url{https://github.com/uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection}}
}
```

---

## 📄 Giấy Phép

Dự án được phát hành theo giấy phép **[MIT License](LICENSE)**.
