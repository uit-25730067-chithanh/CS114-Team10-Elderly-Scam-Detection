# CS114 Final Project — Submission Packaging Guide

Thư mục này chứa cấu trúc tệp và bản nộp bài chính thức của Nhóm 10 theo đúng quy định nộp đồ án môn học **CS114.F31.CN2.TTNT — Máy học (Machine Learning)** tại UIT.

---

## 👥 Danh sách Sinh viên & Mã số Nộp bài

- **Đặng Chí Thanh** — MSSV: `25730067` (Trưởng nhóm / PM)
- **Bùi Thị Mỷ Cẩm** — MSSV: `25730013` (Thành viên)
- **Hoàng Cao Sơn** — MSSV: `25730061` (Thành viên)

**Tên tệp nén chính thức:** `25730067-25730013-25730061.zip`  
**Thư mục gốc bên trong:** `25730067-25730013-25730061/`

---

## 📂 Cấu trúc Lưu trữ Bản Nộp Hoàn Chỉnh

```
25730067-25730013-25730061/
├── DOCS/
│   ├── DoAnMonHoc.docx        # Báo cáo đồ án đầy đủ (≥15 trang)
│   └── DoAnMonHoc.pdf         # Bản xuất PDF chính thức
├── SLIDES/
│   └── Presentation_CS114.pptx # Slide thuyết trình tối ưu 15 phút (14–16 slides)
├── SOURCE/
│   ├── data/                  # dataset.csv (2.193 mẫu thực tế) & feature matrices
│   ├── models/                # best_model_bundle.pkl & model weights
│   ├── src/                   # Mã nguồn Python hoàn chỉnh
│   ├── notebooks/             # Jupyter notebooks (01–06)
│   ├── demo/                  # Web App Streamlit demo
│   ├── app.py                 # Entry point khởi chạy nhanh demo
│   ├── requirements.txt       # Danh mục thư viện phụ thuộc
│   └── reports/               # Bảng so sánh chỉ số & 14 biểu đồ 300 DPI (7 EDA + 7 Model Evaluation)
└── README.md                  # Hướng dẫn chạy mã nguồn và tái lập thực nghiệm
```

---

## 🛠️ Quy trình Đóng gói Tự động

Trước khi nộp bài trên hệ thống Moodle LMS của trường, Trưởng nhóm thực hiện lệnh kiểm định và đóng gói:

```bash
# 1. Chạy kiểm tra định dạng và tính toàn vẹn
python3 verify_final.py

# 2. Xem trước nội dung đóng gói (Dry Run)
python3 .agents/skills/project-audit/scripts/package_submission.py --project . --course CS114 --group 10 --dry-run

# 3. Tạo gói nộp bài ZIP chính thức kèm mã băm SHA256
python3 .agents/skills/project-audit/scripts/package_submission.py --project . --course CS114 --group 10 --output submit/
```
