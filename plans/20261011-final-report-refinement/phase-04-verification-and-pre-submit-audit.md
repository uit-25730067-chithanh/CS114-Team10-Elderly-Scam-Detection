# Phase 04 — Kiểm định Nghiệm thu & Pre-submit Audit

> **Parent plan:** [plan.md](./plan.md)  
> **Previous phase:** [Phase 03 — Biên dịch Word, Đồng bộ Mục lục & Hyperlinks](./phase-03-docx-compilation-and-toc-sync.md)  
> **Tệp tác động:**
> - `verify_final.py`
> - `scripts/validate_assignment.py`
> - `assignments/Final/submit/README.md`  
> **Trạng thái:** `done`  

---

## 1. Mục tiêu
Thực hiện kiểm định toàn diện chất lượng đồ án Final trước khi nộp bài: chạy toàn bộ các kịch bản kiểm tra tự động của môn học, đối soát Semantic Parity giữa các tài liệu quản lý và sản phẩm nộp, đảm bảo quy tắc an toàn Git (< 50MB) và bàn giao rõ ràng cho người dùng.

---

## 2. Chi tiết các nhiệm vụ thực thi

### 2.1. Chạy Scripts Kiểm tra Tự động của Học phần
- Chạy script kiểm định đồ án Final:
  ```bash
  python3 assignments/Final/verify_final.py
  ```
  Yêu cầu: 100% các kiểm tra về cấu trúc thư mục, tệp bắt buộc, 11 phase plans và tính toàn vẹn của dataset template đạt trạng thái `[SUCCESS]`.
- Chạy script kiểm tra định dạng nộp bài toàn môn học:
  ```bash
  python3 scripts/validate_assignment.py --id Final
  ```
  Yêu cầu: Kết quả kiểm tra đạt `[PASS]`.

### 2.2. Kiểm định Tính Nhất quán Ngữ nghĩa (Semantic Parity Gate)
- Đối soát số liệu định lượng xuyên suốt:
  - Dataset: 2.193 mẫu thực tế (1.773 bình thường, 420 lừa đảo).
  - Tỷ lệ mất cân bằng: 4.22 : 1 (`scale_pos_weight = 4.22`).
  - Train (1.754 mẫu) / Test (439 mẫu).
  - F1-Score: XGBoost = 0.9535, Linear SVM = 0.9474, Random Forest = 0.9425, Naive Bayes = 0.8864.
  - Recall lớp lừa đảo: XGBoost = 97.62%, Random Forest = 97.62%, Linear SVM = 96.43%, Naive Bayes = 92.86%.
  - ROC-AUC: Linear SVM = 0.9986, XGBoost = 0.9984, Random Forest = 0.9977, Naive Bayes = 0.9911.
- Đảm bảo 100% các số liệu trong `report-source.md`, `report.docx`, `AGENTS.md`, `README.md` và `phase-09-report-ppt.md` trùng khớp từng chữ số thập phân.

### 2.3. Rà soát An toàn Git & Kiểm tra Kích thước Tệp
- Kiểm tra trạng thái Git trong `cs114` và submodule `assignments/Final`:
  - Working tree sạch sẽ, không có tệp thừa ngoài phạm vi báo cáo.
  - Tệp `report.docx` có kích thước 9.1MB (< 50MB), hoàn toàn an toàn và tuân thủ quy định dung lượng tệp tin.
- Đã dọn dẹp các tệp tạm backup (`report_backup_before_links.docx`).

### 2.4. Bàn giao Hướng dẫn Xuất PDF Thủ công cho Người dùng
- Cung cấp hướng dẫn chi tiết cách mở `report.docx` trên Microsoft Word để xuất ra file `report.pdf` sắc nét nhất (giữ trọn vẹn bookmarks, links và căn lề) mà không cần dùng công cụ tự động can thiệp file PDF.

---

## 3. Checklist Nghiệm thu Phase 04
- [x] `verify_final.py` đạt 100% SUCCESS.
- [x] `validate_assignment.py --id Final` đạt PASS.
- [x] Không có bất kỳ mâu thuẫn số liệu nào giữa các tài liệu (Semantic Parity Gate PASSED).
- [x] Không có tệp vượt quá 50MB trong git (tệp `report.docx` ~9.1MB).
- [x] Tệp `report.docx` hoàn thiện 100%, sẵn sàng để người dùng xuất PDF thủ công và nộp LMS.

---

## 4. Evidence (Bằng chứng Thực tế Nghiệm thu)

- **Trạng thái:** `Hoàn thành (Passed)`
- **Kết quả `verify_final.py`:**
  ```
  === Running Verification for CS114 Final Project ===
  [*] Checking essential directory structure... -> All directories exist [SUCCESS]
  [*] Checking required files... -> All required files verified [SUCCESS]
  [*] Checking 11 phase plan specifications... -> Phase 00-10 verified [SUCCESS]
  [*] Verifying dataset_template.csv schema... -> Header matches [SUCCESS]
  [*] Testing Python utils module import... -> helpers.py imported successfully [SUCCESS]
  [*] Checking Team Roster (3 members) & Student IDs... -> 3 MSSV verified in README & AGENTS [SUCCESS]
  [*] Checking Documentation Semantic Parity & 11-File Matrix... -> All verified [SUCCESS]
  --------------------------------------------------
  [SUCCESS] All Final project checks PASSED! Ready for Sprint execution.
  ```
- **Kết quả `validate_assignment.py --id Final`:**
  ```
  === Running Validation for Final ===
  [*] Found custom verify script: .../assignments/Final/verify_final.py. Executing...
  [SUCCESS] Custom verify script passed.
  [COMPLETE] Validation for Final completed successfully!
  ```
- **Kết quả đối soát số liệu (Semantic Parity):**
  - Trùng khớp 100% giữa `report-source.md`, `report.docx`, `README.md`, `AGENTS.md` về: Tổng số mẫu (2.193), Tỷ lệ Imbalance (4.22 : 1), Kích thước Train/Test (1.754 / 439), Metrics 4 mô hình (XGBoost F1 0.9535, Recall 97.62%, AUC 0.9984), Bảng thống kê 6 đặc trưng domain Bảng 3.1, và kết quả Ablation Study.
- **Kích thước các tệp nhị phân Git:**
  - `report.docx`: 9.1MB (< 50MB, chuẩn OpenXML UIT, không có tệp nào vi phạm).

---

## 5. Kongming Advisory Gate (Passed Criteria)
- [x] 100% kiểm tra học phần đạt `SUCCESS` / `PASS`.
- [x] Số liệu nhất quán tuyệt đối giữa `report-source.md`, `report.docx`, `README.md` và `AGENTS.md`.
- [x] Tuyệt đối không can thiệp tệp PDF theo đúng cam kết với người dùng.
- [x] Kongming xác nhận đánh giá: `PASSED`.

---

## 6. Verdict
- **Đánh giá cuối cùng:** `PASSED`

