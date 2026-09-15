# Project Roadmap — CS114 Scam Detection (Fast-Track 23/09 Mode)

## Hành trình dự án

**Bắt đầu:** 06/09/2026 | **Báo cáo sớm:** 23/09/2026 (Hạn LMS gốc: 13/10/2026) | **Daily Sync:** 21:00 hàng ngày

> ⚡ **Chiến lược Thực thi Song song (`--parallels`):**
> Do nhóm xin thầy báo cáo sớm vào ngày **23/09/2026**, toàn bộ lộ trình được tối ưu thành **3-Sprint Fast-Track** (13 ngày). Dữ liệu khóa vào 12/09, kích hoạt 4 luồng kỹ thuật song song từ 13/09, hoàn tất Báo cáo Word & Slide PPT ngày 20/09, dành 2 ngày (21–22/09) diễn tập bấm giờ và đóng gói ZIP.

---

## 🗺️ Lộ trình tổng thể (Biểu đồ Gantt Fast-Track)

```mermaid
gantt
    title CS114 Scam Detection — Tiến độ Fast-Track (06/09 - 23/09)
    dateFormat  YYYY-MM-DD
    axisFormat  %d/%m
    tickInterval 2d

    section Sprint 1: Hạ tầng & Khóa Data (06/09 – 14/09)
    Setup repo, venv & verify_final (Thanh)        :done, s1_1, 2026-09-06, 2026-09-09
    Thu thập 1.773 mẫu bình thường (Thanh)         :done, s1_2, 2026-09-06, 2026-09-10
    Thu thập 420 mẫu lừa đảo (Sơn & Cẩm)           :done, s1_3, 2026-09-09, 2026-09-14
    Khóa dataset.csv 2.193 mẫu & chia 80/20 (Thanh):done, s1_4, 2026-09-14, 2026-09-15

    section Sprint 2: Song song NLP & ML (15/09 – 18/09)
    Tiền xử lý NLP tiếng Việt (Thanh)              :active, s2_1, 2026-09-15, 2026-09-16
    EDA & Trích xuất TF-IDF (Thanh)                :s2_2, 2026-09-16, 2026-09-17
    Naive Bayes Baseline (Cẩm)                     :s2_3, 2026-09-15, 2026-09-16
    Random Forest & Hypertuning (Sơn)              :s2_4, 2026-09-16, 2026-09-17
    XGBoost & SVM Linear/RBF (Cẩm)                 :s2_5, 2026-09-16, 2026-09-17
    Demo UI Streamlit shell (Sơn)                  :s2_6, 2026-09-16, 2026-09-18
    Báo cáo Word Chương 1, 2, 3 (Cả nhóm)          :s2_7, 2026-09-15, 2026-09-18

    section Sprint 3: Đánh giá, PPT & Diễn tập (19/09 – 22/09)
    Đánh giá tổng hợp & XAI SHAP (Thanh & Cẩm)     :s3_1, 2026-09-18, 2026-09-19
    Tích hợp Best Model vào Demo UI (Sơn & Thanh)  :s3_2, 2026-09-19, 2026-09-20
    Báo cáo Word Chương 4–5 + Refs (Cả nhóm)       :s3_3, 2026-09-20, 2026-09-21
    Slide PPT 15 phút (14–16 slides) (Cả nhóm)     :s3_4, 2026-09-20, 2026-09-21
    Diễn tập thuyết trình bấm giờ ≤15p (Cả nhóm)   :crit, s3_5, 2026-09-21, 2026-09-22
    Đóng gói ZIP 25730067-... (Thanh)              :s3_6, 2026-09-22, 2026-09-22

    section D-Day: Thuyết trình MS Teams (18h30 23/09)
    BÁO CÁO TRỰC TUYẾN MS TEAMS (18h30)            :milestone, s3_7, 2026-09-23, 0d
```

---

## 🏃 Sprint 1 — 06/09 → 14/09 (Khóa Hạ tầng & Dữ liệu)

> **Mục tiêu:** Setup môi trường, hoàn tất thu thập ≥1.500 mẫu tiếng Việt, chạy `data_validation.py` PASSED và đóng băng `dataset.csv` 2.193 mẫu thực tế.

### Thanh (PM & Data Lead)
| Task | Trạng thái |
|------|:---:|
| Setup repo, venv, requirements.txt, verify_final.py | ✅ Done (Phase 00) |
| `src/utils/helpers.py`: constants, set_seeds(), random_state=42 | ✅ Done (Phase 00) |
| Thu thập 1.773 mẫu bình thường, ẩn danh PII 100%, 50 mẫu Holdout Test | ✅ Done (Phase 01) |
| Hỗ trợ review schema và đối soát dữ liệu cho Sơn & Cẩm | ✅ Done |
| Hợp nhất dữ liệu (2.193 mẫu), chạy kiểm định và khóa `dataset.csv` | ✅ Done |

### Sơn (Data Collection Lead)
| Task | Trạng thái |
|------|:---:|
| Lập quy chuẩn phân loại 4 nhóm bẫy tâm lý theo chuẩn kiểm toán | ✅ Done |
| Thu thập 215 mẫu lừa đảo (`fear_authority` và `family_emergency`) | ✅ Done (PR #10 merged) |
| Export dữ liệu và vượt qua 7 tầng kiểm toán `audit_son_rigorous.py` | ✅ Done |

### Cẩm (Modeling Engineer)
| Task | Trạng thái |
|------|:---:|
| Setup venv cá nhân, cài đặt thư viện ML | ✅ Done |
| Thu thập 205 mẫu lừa đảo (`health_gift` và `public_service`) | ✅ Done (PR #9 merged) |
| Export dữ liệu và vượt qua 10 vòng kiểm toán `audit_cam_rigorous.py` | ✅ Done |

---

## 🏃 Sprint 2 — 15/09 → 18/09 (Song song NLP & Huấn luyện Mô hình)

> **Mục tiêu:** Pipeline tiền xử lý hoàn tất, trích xuất TF-IDF sẵn sàng, huấn luyện đồng thời 4 mô hình (NB, RF, XGBoost, SVM), dựng khung Demo UI Streamlit, viết xong Báo cáo Word Chương 1–3.

### Thanh (Data & NLP Lead)
| Task | Trạng thái |
|------|:---:|
| `src/preprocessing/text_cleaner.py`: Unicode NFC, teencode mapper, xóa rác | 🚀 Đang làm (15/09) |
| `src/preprocessing/tokenizer.py` (pyvi) + stopwords | ⏳ (15/09) |
| `src/preprocessing/pipeline.py` + trích xuất đặc trưng phụ (URL, SĐT, cấp cứu) | ⏳ (15/09 – 16/09) |
| `notebooks/01_preprocessing.ipynb`: Thực nghiệm pipeline và xuất CSV sạch | ⏳ (16/09) |
| `notebooks/02_eda.ipynb`: Phân phối nhãn, n-grams, word cloud, độ dài | ⏳ (16/09) |
| Lưu trữ `models/vectorizer.pkl` và các ma trận đặc trưng `data/processed/` | ⏳ (16/09 – 17/09) |

### Cẩm (Modeling Engineer — NB, XGBoost, SVM)
| Task | Trạng thái |
|------|:---:|
| `notebooks/03_model_naive_bayes.ipynb`: GridSearch alpha, Learning Curve, Confusion Matrix | ⏳ (15/09 – 16/09) |
| `models/naive_bayes.pkl`: Lưu trọng số baseline | ⏳ (16/09) |
| `notebooks/04_model_xgboost.ipynb`: Tinh chỉnh n_estimators, max_depth, learning_rate | ⏳ (16/09 – 17/09) |
| `notebooks/05_model_svm.ipynb`: LinearSVC Calibrated / RBF kernel, so sánh đa tham số | ⏳ (16/09 – 17/09) |
| Lưu `models/xgboost.pkl` và `models/svm.pkl` | ⏳ (17/09) |

### Sơn (Modeling & UI Lead — Random Forest & Demo UI)
| Task | Trạng thái |
|------|:---:|
| `notebooks/04_model_random_forest.ipynb`: RandomizedSearch n_estimators, max_depth | ⏳ (16/09 – 17/09) |
| `models/random_forest.pkl`: Lưu trọng số Random Forest | ⏳ (17/09) |
| `demo/app.py`: Khung Streamlit 2 cột (Nhập liệu / Kết quả cảnh báo) | ⏳ (16/09 – 17/09) |
| `demo/components/`: risk_meter.py, keyword_highlighter.py, safety_advisor.py | ⏳ (17/09 – 18/09) |

### Cả nhóm (Academic Documentation)
| Task | Trạng thái |
|------|:---:|
| Báo cáo Word: Chương 1 — Đặt vấn đề, bối cảnh lừa đảo NCT 2026, ý nghĩa xã hội | ⏳ (15/09 – 16/09) |
| Báo cáo Word: Chương 2 — Khảo sát các công trình nghiên cứu & hướng tiếp cận | ⏳ (16/09 – 17/09) |
| Báo cáo Word: Chương 3 — Phương pháp nhóm chọn: Tiền xử lý, TF-IDF, kiến trúc 3+ models | ⏳ (17/09 – 18/09) |
| Lên khung cấu trúc Slide PowerPoint 15 phút (14–16 slides) | ⏳ (18/09) |


---

## 🏃 Sprint 3 — 19/09 → 22/09 (Đánh giá, Demo, PPT & Diễn tập Bảo vệ)

> **Mục tiêu:** Đánh giá tổng hợp 4 mô hình, trích xuất XAI SHAP, tích hợp model vào Demo Streamlit, hoàn thiện Báo cáo Word (≥15 trang) và Slide PPT, diễn tập bảo vệ ≤15 phút, đóng gói ZIP `25730067-25730013-25730061.zip`.

### Thanh (Evaluation & Packaging Lead)
| Task | Trạng thái |
|------|:---:|
| `notebooks/06_evaluation_xai.ipynb`: Bảng so sánh 4 models (Accuracy, Precision, Recall, F1, ROC-AUC) | 🔲 (18/09 – 19/09) |
| Trực quan hóa: Confusion Matrix so sánh, ROC Curves, Precision-Recall Curves | 🔲 (19/09) |
| Phân tích Overfitting: Learning Curves (Train vs Validation K-Fold) | 🔲 (19/09) |
| XAI: Trích xuất Top-20 từ khóa cảnh báo kích hoạt bẫy tâm lý (SHAP / Feature Weights) | 🔲 (19/09) |
| `reports/model_comparison.csv` và xuất toàn bộ figures | 🔲 (19/09) |
| Pre-flight check toàn diện bằng `verify_final.py` | 🔲 (22/09) |
| Đóng gói ZIP `25730067-25730013-25730061.zip` theo chuẩn nộp bài UIT | 🔲 (22/09) |

### Sơn (Demo Integration & Screenshots)
| Task | Trạng thái |
|------|:---:|
| Tích hợp Best Model (.pkl) và Vectorizer vào `demo/app.py` | 🔲 (19/09 – 20/09) |
| Hoàn thiện tính năng bôi đỏ từ khóa bẫy tâm lý và khuyến cáo an toàn cho NCT | 🔲 (20/09) |
| Chụp ≥3 ảnh màn hình Demo chất lượng cao chèn vào Báo cáo Word và Slide PPT | 🔲 (20/09) |

### Cả nhóm (Báo cáo, Slide PPT & Diễn tập Thuyết trình)
| Task | Trạng thái |
|------|:---:|
| Báo cáo Word: Chương 4 — Thực nghiệm (Dataset, Metrics, Bảng so sánh, Confusion Matrix, Overfitting) | 🔲 (20/09) |
| Báo cáo Word: Chương 5 — Kết luận, Hạn chế và Định hướng phát triển (PhoBERT, Mobile) | 🔲 (20/09) |
| Hoàn thiện Tài liệu tham khảo (≥10 trích dẫn chuẩn IEEE/APA) | 🔲 (20/09) |
| Xuất bản file `DOCS/DoAnMonHoc.docx` và `DOCS/DoAnMonHoc.pdf` (≥15 trang) | 🔲 (21/09) |
| Hoàn thiện file Slide `SLIDES/Presentation_CS114.pptx` (14–16 slides) | 🔲 (20/09 – 21/09) |
| Diễn tập thuyết trình lần 1: Bấm giờ từng phần (Thanh 5p, Cẩm 4p, Sơn 3p) | 🔲 (21/09) |
| Diễn tập thuyết trình lần 2: Giả lập phản biện Q&A từ ThS. Cáp Phạm Đình Thăng (3p) | 🔲 (22/09) |

---

## 🎯 D-Day — 18:30 Ngày 23/09/2026: Thuyết Trình Bảo Vệ Đồ Án (MS Teams)

> 📌 **Hình thức:** Trực tuyến qua Microsoft Teams (khe giờ môn SS007 cũ, thầy Thăng tạo điều kiện báo cáo sớm).  
> 📌 **Quy cách:** Bắt buộc thuyết trình luân phiên cả 3 thành viên; Trưởng nhóm Đặng Chí Thanh điều phối Master Share Screen.

| Thời gian | Nội dung | Phụ trách & Thao tác kỹ thuật |
|-----------|----------|------------------------------|
| 00:00 – 01:30 | Chào thầy, giới thiệu Nhóm 10, bối cảnh lừa đảo NCT tại VN & ý nghĩa thực tiễn | **Đặng Chí Thanh** (Bật mic/cam, Share Screen Slide 1–2) |
| 01:30 – 04:30 | Quy trình thu thập dataset (≥1.500 mẫu, PII Masking), Pipeline NLP tiếng Việt & TF-IDF | **Đặng Chí Thanh** (Slide 3–5, chuyển quyền nói cho Cẩm) |
| 04:30 – 08:30 | Thực nghiệm 3+ mô hình (NB, RF/XGB, SVM), Đánh giá Overfitting (Learning Curves), Confusion Matrix | **Bùi Thị Mỷ Cẩm** (Bật mic/cam, Slide 6–9, chuyển quyền nói cho Sơn) |
| 08:30 – 11:30 | Giải thích bẫy tâm lý XAI SHAP, Demo trực tiếp Web App Streamlit, Kết luận & Hướng mở rộng | **Hoàng Cao Sơn** (Bật mic/cam, thuyết minh trên tab Demo do Thanh share, Slide 10–13) |
| 11:30 – 15:00 | Trả lời câu hỏi phản biện của ThS. Cáp Phạm Đình Thăng (Q&A) | **Cả nhóm** (Thanh điều phối mở đầu và cùng Cẩm, Sơn phản biện) |
