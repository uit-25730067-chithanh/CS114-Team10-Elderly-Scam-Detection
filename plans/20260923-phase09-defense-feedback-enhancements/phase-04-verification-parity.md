# Phase 04 — Verification & Parity (Kiểm Định & Đồng Bộ Dự Án)

> **Kế hoạch cha:** [plan.md](./plan.md)  
> **Người phụ trách:** Đặng Chí Thanh (25730067)  
> **Trạng thái:** `ready`

---

## 🎯 Mục Tiêu Kiểm Định

Sau khi hoàn thành Báo cáo Word và có kết quả thực nghiệm đầy đủ:
1. **Kiểm tra tự động toàn diện**:
   - Chạy script kiểm định đồ án:
     ```bash
     python3 assignments/Final/verify_final.py
     ```
   - Chạy kiểm tra định dạng bài làm môn học:
     ```bash
     python3 scripts/validate_assignment.py --id Final
     ```
   - Đảm bảo 100% các tiêu chí từ Phase 00 đến Phase 09 đều đạt trạng thái `PASSED`.

2. **Đồng bộ hóa tài liệu (Cross-Document Parity)**:
   - Cập nhật tiến độ trong `assignments/Final/README.md` và `assignments/Final/AGENTS.md`.
   - Cập nhật file kế hoạch gốc: `assignments/Final/plans/scam-detection-full-submit/phase-09-report-ppt.md` (chuyển trạng thái sang hoàn tất `passed` ✅).
   - Đảm bảo tính nhất quán tuyệt đối về số liệu số mẫu (2.193 mẫu, 1.754 train, 439 test, 420 lừa đảo), metrics (F1 0.9535, Recall 97.62%) trên toàn bộ tài liệu.

3. **Tạo Pull Request chuẩn UIT**:
   - Commit các thay đổi với thông điệp rõ ràng theo Conventional Commits:
     ```bash
     git add draft/scam-detection/reports/report/ plans/20260923-phase09-defense-feedback-enhancements/
     git commit -m "feat(phase-09): enrich academic report with ablation studies and defense feedback"
     ```
   - Tạo PR trên repository `CS114-Team10-Elderly-Scam-Detection` từ nhánh `feat/phase-09-defense-feedback-enhancements` vào `main`.
   - Tiêu đề PR: `Enrich Academic Report With Ablation Studies and Defense Feedback (#31)` (Title Case, Imperative).
   - Nội dung PR theo chuẩn tiếng Việt, liệt kê chi tiết các bổ sung theo lời ThS. Cáp Phạm Đình Thăng.
