# Kế hoạch Hoàn thiện Báo cáo Đồ án Final CS114 (report-source.md → report.docx)

> **Mã kế hoạch:** `20261011-final-report-refinement`  
> **Đề tài:** Nghiên cứu và Xây dựng Hệ thống Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam  
> **Môn học:** CS114 — Máy học | **GVHD:** ThS. Cáp Phạm Đình Thăng  
> **Tập thể thực hiện:** Nhóm 10 (Đặng Chí Thanh - 25730067, Bùi Thị Mỷ Cẩm - 25730013, Hoàng Cao Sơn - 25730061)  
> **Ngày khởi tạo:** 11/10/2026  
> **Luồng thực thi bắt buộc:** `report-source.md` (Single Source of Truth) → `report.docx` (Word chuẩn UIT). *(Tệp .pdf người dùng sẽ tự xuất thủ công trong Microsoft Word).*  
> **Cơ chế nghiệm thu nghiêm ngặt:** Mỗi Phase BẮT BUỘC phải điền đầy đủ mục `## Evidence` với bằng chứng thực tế (lệnh chạy, diff, số dòng, kết quả test), đạt 100% tiêu chí validation và được **Kongming Advisory Gate** đánh giá là `PASSED` thì mới được xem là hoàn thành.

---

## 1. Bối cảnh & Mục tiêu

Sau buổi báo cáo sớm ngày 23/09/2026 và đợt kiểm định chuyên sâu ngày 11/10/2026, nhóm đã phát hiện 8 điểm lệch pha, lỗi dàn trang và thiếu sót hình ảnh nghiêm trọng trong bản báo cáo hiện tại:
1. Số trang trong bảng Mục lục bị lệch 1 đến 2 trang so với nội dung thực tế.
2. Trang bìa ghi sai Khoa quản lý (*Khoa Hệ thống Thông tin* thay vì *Khoa Khoa học Máy tính*).
3. Đứt gãy đồng bộ giữa Markdown (`report-source.md`) và script sinh Word (`generate_academic_report.py`), làm mất số liệu thống kê Bảng 3.1 và thiếu các công thức toán quan trọng.
4. Kho 35 hình ảnh 300 DPI chỉ dùng 12 hình (34%), bỏ sót 4 biểu đồ EDA và hình ảnh minh chứng trợ năng thị giác người già.
5. Thiếu Bảng phân công nhiệm vụ và tỷ lệ hoàn thành của 3 thành viên.
6. Cấu trúc Chương 4 chưa chuẩn theo đề cương bắt buộc của Thầy Thăng trong `NopDoAnMonHoc.png`.
7. Lỗi dàn trang ngắt đôi Bảng 4.3 (Top 20 SHAP) qua trang và nhiều trang có mật độ chữ quá thấp do ngắt trang cứng.
8. Thiếu lý giải toán học về sự dịch chuyển siêu phẳng của Linear SVM trong Ablation 2.

**Mục tiêu của kế hoạch:** Giải quyết triệt để 100% các vấn đề trên, đảm bảo tính nhất quán tuyệt đối giữa `report-source.md` và `report.docx`, đưa báo cáo đạt chuẩn A+ trước khi nộp chính thức lên LMS.

---

## 2. Quy tắc Nghiệm thu & Giám sát Kongming (Quality Gate Invariants)

1. **Zero-Assumption Gate:** Không đánh dấu hoàn thành chỉ bằng checklist `[x]`. Mọi phase phải có mục `## Evidence` ghi lại kết quả thực tế (terminal output, diff kiểm chứng, đường dẫn tệp cụ thể).
2. **Kongming Checkpoint Gate:** Sau khi hoàn thành triển khai của từng phase, agent phải kích hoạt kiểm tra phản biện Kongming (Advisory Supervision):
   - Đánh giá go/no-go.
   - Nhận diện rủi ro hoặc lỗ hổng sót lại.
   - Chỉ khi Kongming xác nhận `Verdict: PASSED`, phase đó mới được xem là kết thúc và chuyển tiếp sang phase tiếp theo.

---

## 3. Lộ trình Thực thi Phân đoạn (Phased Roadmap)

| Phase | Tên giai đoạn | Trọng tâm công việc | Tệp tác động chính | Trạng thái |
|:---:|---|---|---|:---:|
| **01** | **Chuẩn hóa Toàn diện Markdown Source** | Sửa trang bìa, bổ sung Bảng phân công 3 thành viên, tái cấu trúc Chương 4 theo chuẩn Thầy Thăng, chèn 4 ảnh EDA + 1 ảnh Demo + 1 ảnh barplot XAI, đồng bộ Bảng 3.1 (6 cột có Mean), bổ sung công thức toán `L(θ)`, SVM, TF-IDF và lý giải SVM trong Ablation 2. | `draft/scam-detection/reports/report/report-source.md` | `done` |
| **02** | **Đồng bộ Kịch bản Sinh Word & OMML Math** | Cập nhật `generate_academic_report.py` đồng bộ 100% với Markdown, chuyển đổi công thức toán sang Word Equation OMML native, định cấu hình bảng 6 cột, nhúng đủ hình ảnh mới, tinh chỉnh khoảng cách chống ngắt đôi bảng. | `draft/scam-detection/reports/report/generate_academic_report.py` | `done` |
| **03** | **Biên dịch Word, Đồng bộ Mục lục & Hyperlinks** | Biên dịch `report.docx`, cập nhật số trang bảng Mục lục chính xác 100%, chạy script gắn bookmarks và hyperlinks tương tác, kiểm định OpenXML bằng `audit_docx_xml.py`. | `draft/scam-detection/reports/report/report.docx`<br>`apply_toc_links.py`<br>`apply_reference_links.py` | `done` |
| **04** | **Kiểm định Nghiệm thu & Pre-submit Audit** | Chạy `verify_final.py` và `validate_assignment.py --id Final`, đối soát Semantic Parity, kiểm tra dung lượng Git (< 50MB), bàn giao tệp Word hoàn hảo cho người dùng tự xuất PDF. | `verify_final.py`<br>`submit/README.md` | `done` |

---

## 4. Bản đồ Tệp Phân hệ Chi tiết

- [Phase 01: Chuẩn hóa Toàn diện Markdown Source](./phase-01-markdown-content-enrichment.md)
- [Phase 02: Đồng bộ Kịch bản Sinh Word & OMML Math](./phase-02-docx-generator-sync-and-math.md)
- [Phase 03: Biên dịch Word, Đồng bộ Mục lục & Hyperlinks](./phase-03-docx-compilation-and-toc-sync.md)
- [Phase 04: Kiểm định Nghiệm thu & Pre-submit Audit](./phase-04-verification-and-pre-submit-audit.md)
