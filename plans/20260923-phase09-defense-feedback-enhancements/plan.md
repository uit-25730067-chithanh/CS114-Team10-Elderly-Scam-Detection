---
title: "Kế Hoạch Hoàn Thiện Báo Cáo Final Dựa Trên Góp Ý Buổi 8 (ThS. Cáp Phạm Đình Thăng)"
description: "Kế hoạch nâng cấp và hoàn thiện Báo cáo Word Đồ án CS114 (Phase 09) bằng cách tích hợp 2 bài thực nghiệm đối chứng (Ablation Studies), chuẩn hóa bài toán và hàm mất mát, và biên dịch DOCX chuẩn UIT."
status: in-progress
priority: P1
effort: ~8-10h (Cả nhóm 10)
branch: feat/phase-09-defense-feedback-enhancements
tags: [cs114, phase09, academic-report, ablation-studies, feedback-defense, docx, uit]
created: 2026-09-23
updated: 2026-09-23
---

# Kế Hoạch Hoàn Thiện Báo Cáo Đồ Án Cuối Kỳ Dựa Trên Góp Ý Buổi 8

> **Mã kế hoạch:** `20260923-phase09-defense-feedback-enhancements`  
> **Repository:** `CS114-Team10-Elderly-Scam-Detection` (Submodule: `assignments/Final`)  
> **Nhánh làm việc:** `feat/phase-09-defense-feedback-enhancements` (tạo trực tiếp từ `main`)  
> **Tài liệu nghiên cứu cơ sở:** [research-buoi-08-lecture-feedback.md](./research-buoi-08-lecture-feedback.md)  
> **Kế hoạch mẹ:** [plans/scam-detection-full-submit/phase-09-report-ppt.md](../scam-detection-full-submit/phase-09-report-ppt.md)

---

## 🎯 Bối Cảnh: Vì Sao Lại Có Branch Và PR Này?

Tối ngày 23/09/2026, Nhóm 10 đã bảo vệ sớm thành công đồ án CS114 trước ThS. Cáp Phạm Đình Thăng. Nhóm đã đạt được kết quả rất tốt ở khối Slide PPT 22 trang và Web App Demo. 

Tuy nhiên, trong phần Q&A và nhận xét tổng kết buổi học, Thầy Thăng đã chỉ rõ **những khoảng trống phương pháp luận bắt buộc phải bổ sung trong Báo cáo Word** để đạt điểm tối đa (A+):

1. **Thực nghiệm đối chứng Tiền xử lý (Ablation on Preprocessing)**: Thầy chỉ đạo: *"Ở đây mình có tiền xử lý. Nhưng mình chưa có thực nghiệm là ví dụ nếu mình chưa tiền xử lý và nếu mình tiền xử lý thì kết quả như thế nào?... Nó phải tăng thì mình mới làm tiền xử lý đúng không?... Tổng hợp lại thành cái bảng, ha."* → Cần bảng đo lường thực tế giữa Raw Text vs Preprocessed Text.
2. **Thực nghiệm đối chứng Không gian đặc trưng (Ablation on Feature Space)**: Thầy chỉ đạo: *"5000 TF-IDF và mười mấy đặc trưng phụ đúng không?... Nếu chỉ dùng TF-IDF thôi, bỏ 15 cái phụ đi thì kết quả như thế nào? Sau đó kết hợp cả hai thì kết quả như thế nào? Để giải thích lý do tại sao mình lại chọn thêm 15 đặc trưng phụ này. Tổng hợp lại thành bảng."* → Cần bảng so sánh 3 cấu hình: Chỉ TF-IDF vs Chỉ 15 Features vs Kết hợp 5.015.
3. **Phân định rõ ranh giới bài toán**: Nêu bật sự khác biệt bản chất giữa tin nhắn lừa đảo thao túng tâm lý (Social Engineering) vs tin giả báo chí (Fake News).
4. **Công thức toán học tường minh**: Trình bày công thức hàm mất mát có trọng số (Cost-sensitive Loss `scale_pos_weight = 4.22`), lý do từ chối SMOTE trên text tiếng Việt, và công thức toán của các metric đánh giá (Accuracy, Precision, Recall, F1, ROC-AUC).
5. **Phân tích ca biên đe dọa trực diện & Định hướng giải pháp theo Thầy Thăng**: Thầy dặn dò ca test cuối buổi *"Cướp đây, đưa hết tiền đây!"* (báo an toàn 4.1% do domain gap và hạn chế unigram). Định hướng giải pháp theo lời Thầy Thăng gồm:
   - Mở rộng N-gram range lên `(1, 2)` và `(1, 3)` để bắt trọn cụm từ nối tiếp như `"cướp đây"`, `"đưa hết tiền"`.
   - Bổ sung nhóm đặc trưng từ khóa cưỡng bức trực diện (`imperative_threat`).
   - Ứng dụng mô hình ngữ cảnh Transformer (PhoBERT) với cơ chế Self-Attention để bắt trọn ngữ nghĩa câu ngắn.

Nhánh `feat/phase-09-defense-feedback-enhancements` được tạo ra để **cô lập các cải tiến này, kế thừa bản nháp báo cáo từ Sơn, chạy đo đạc thực nghiệm số liệu thật, và xuất bản file Word hoàn chỉnh**.

---

## 📊 Phân Kỳ Thực Hiện (Phases)

| Phase | Tên giai đoạn | Trọng tâm | File chi tiết | Trạng thái |
|:---:|---|---|---|:---:|
| **01** | **Ablation Experiments** | Viết script đo lường thực tế 2 bảng đối chứng trên tập Test 439 mẫu | [phase-01-ablation-experiments.md](./phase-01-ablation-experiments.md) | `ready` |
| **02** | **Report Markdown Enrichment** | Bổ sung số liệu thực nghiệm, công thức toán và phân định bài toán vào `report-source.md` | [phase-02-report-markdown-enrichment.md](./phase-02-report-markdown-enrichment.md) | `ready` |
| **03** | **DOCX Compilation & Styling** | Biên dịch sang `report.docx` chuẩn UIT (Times New Roman 13pt, bìa hoa văn, TOC) | [phase-03-docx-compilation-formatting.md](./phase-03-docx-compilation-formatting.md) | `ready` |
| **04** | **Verification & Parity** | Chạy `verify_final.py`, kiểm toán PR, đồng bộ tài liệu chuẩn bị nộp bài (Phase 10) | [phase-04-verification-parity.md](./phase-04-verification-parity.md) | `ready` |

---

## 👥 Phân Công Trách Nhiệm

* **Đặng Chí Thanh (25730067 - Lead / PM)**:
  - Viết và chạy script `run_ablation_studies.py` để trích xuất số liệu thực tế cho 2 bảng Ablation.
  - Soạn thảo Mục 4.4 Thực nghiệm đối chứng và Mục 4.5 Phân tích sai số.
  - Chạy `verify_final.py` kiểm định toàn diện và review/merge PR.
* **Hoàng Cao Sơn (25730061)**:
  - Soạn thảo và trau chuốt văn phong Chương 1 (Đặt vấn đề) và Chương 2 (Khảo sát các phương pháp tiếp cận).
  - Quản lý chèn các hình ảnh biểu đồ EDA và Demo UI chuẩn 300 DPI vào văn bản.
* **Bùi Thị Mỷ Cẩm (25730013)**:
  - Soạn thảo Chương 3 (Phương pháp nhóm chọn): Trình bày công thức toán hàm mất mát có trọng số và pipeline trích xuất.
  - Rà soát tính chính xác của bảng so sánh 4 mô hình và kiểm tra định dạng ≥15 tài liệu tham khảo chuẩn IEEE.

---

## 🛡️ Nguyên Tắc Bất Di Bất Dịch (Non-Negotiables)

1. **Zero Data Leakage**: Tuyệt đối không fit lại TF-IDF hay Scaler trên tập Test. Toàn bộ thực nghiệm đối chứng phải tuân thủ nghiêm ngặt: fit duy nhất trên Train (1.754 mẫu), chỉ transform sang Test (439 mẫu).
2. **Số liệu thật 100% (Zero Faked Metrics)**: Toàn bộ con số trong 2 bảng Ablation Studies phải xuất từ kết quả chạy thực nghiệm thực tế của script, tuyệt đối không bịa số.
3. **Không làm xáo trộn Demo production**: Không sửa đổi file `best_model_bundle.pkl` hay code Streamlit demo đang chạy ổn định.
