# 📄 Report Outline — CS114 Final: Vietnamese Elderly Scam Detection

> **Template mẫu Phase 09 — Bàn giao Hoàng Cao Sơn (25730061) tạo PR và hoàn thiện**
>
> Skill: `uit:academic-report` | Branch: `feat/phase-09-report-template`
> Reviewer: Đặng Chí Thanh (25730067)

---

## 🎯 Thông số đầu vào (Đã xác định)

| Thông số | Giá trị |
|----------|---------|
| **Loại tài liệu** | Báo cáo kỹ thuật — `report` (không phải essay) |
| **Ngôn ngữ** | Tiếng Việt (văn phong học thuật trang trọng) |
| **Font / cỡ chữ** | Times New Roman 13pt |
| **Line spacing** | 1.3 |
| **Lề** | Trái 3cm · Phải 2cm · Trên 2cm · Dưới 2cm |
| **Mục tiêu trang** | ≥ 15 trang (yêu cầu GV) |
| **Trang bìa** | Chuẩn UIT hoa văn OpenXML |
| **Mục lục** | Dot-leader TOC tự động |
| **Output** | `report.docx` → xuất PDF thủ công từ Word |

---

## 📐 Cấu trúc báo cáo (Dàn ý chi tiết)

### Trang bìa (UIT standard cover)
- Logo UIT + Tên trường
- Tên môn học: CS114 — Máy học
- Tên đề tài: Phát hiện Tin nhắn Lừa đảo nhắm vào Người cao tuổi
- Thông tin nhóm: Nhóm 10 + 3 thành viên + MSSV
- Giảng viên: ThS. Cáp Phạm Đình Thăng
- Ngày: 23/09/2026

### Cam kết Liêm chính Học thuật (bắt buộc)
- 3 MSSV ký cam kết

### Mục lục tự động (dot-leader TOC)

---

### Chương 1 — Đặt vấn đề (~2-3 trang)

#### 1.1. Bối cảnh và tính cấp thiết
- **Nội dung cần hoàn thiện (Sơn)**:
  - Số liệu thực tế từ Bộ Công an / báo chí 2025-2026 về lừa đảo NCT
  - Dẫn chứng cụ thể 1-2 vụ điển hình (từ Tuổi Trẻ, VnExpress)
  - Lý do NCT dễ bị nhắm mục tiêu (ít am hiểu công nghệ, tin tưởng quyền lực)
- **Figures**: Không cần figure — chỉ văn bản + số liệu thống kê

#### 1.2. Các khó khăn và thách thức
- **Nội dung cần hoàn thiện (Sơn)**:
  - 4 thách thức kỹ thuật (xem template)
  - Thêm số liệu cụ thể nếu có
- **Từ ngữ**: Câu văn học thuật, không viết "chúng tôi thấy rằng"

#### 1.3. Ý nghĩa thực tiễn
- Ứng dụng xã hội của hệ thống
- Tác động đến cộng đồng NCT Việt Nam

---

### Chương 2 — Các phương pháp tiếp cận (~2-3 trang)

#### 2.1. Khảo sát công trình liên quan (Related Works)
- **Nội dung cần hoàn thiện (Sơn)**:
  - Đọc 3-5 bài báo liên quan (từ `research-cam-phase04-05-modeling-audit.md`)
  - Điền vào bảng Related Works: Paper | Method | Dataset | Result
  - Viết 1 đoạn so sánh nhóm với các công trình liên quan

#### 2.2. So sánh các hướng tiếp cận
- Bảng so sánh Rule-based vs ML vs Deep Learning đã có trong template
- **Thêm (Sơn)**: 1-2 câu nhận xét lý do loại bỏ Rule-based và DL

#### 2.3. Lý do chọn hướng ML + NLP tiếng Việt
- Đã có trong template, cần review và bổ sung nếu thiếu

---

### Chương 3 — Phương pháp nhóm chọn (~3-4 trang)

#### 3.1. Pipeline Tiền xử lý
- **Nội dung cần hoàn thiện (Sơn)**:
  - Điền đầy đủ 15 auxiliary features (xem `src/feature_engineering.py`)
  - Thêm code snippet minh họa nếu cần

#### 3.2. Feature Engineering
- Đã hoàn chỉnh trong template

#### 3.3. Mô tả 4 Mô hình
- Template đã có cấu trúc, Sơn thêm 1-2 câu mô tả kỹ thuật cho mỗi model
- Tham khảo: `phase-04`, `phase-05`, `phase-06` plan files

#### 3.4. Kiến trúc tổng thể
- **Thêm figure (Sơn)**: Render diagram từ `diagrams.json` hoặc vẽ bằng Mermaid
  - Tool: `ak-mermaidjs-v11` hoặc `ak-excalidraw`
  - Save vào `reports/figures/architecture_diagram.png`

---

### Chương 4 — Thực nghiệm (~5-6 trang)

#### 4.1. Dataset & EDA
- **Template đã có** cấu trúc và figure references
- **Sơn cần thêm**:
  - Nhận xét sau mỗi figure (2-3 câu)
  - Bổ sung Figure 4.4-4.9 nhận xét

#### 4.2. Kết quả
- Bảng so sánh đã điền đầy đủ metrics thực tế
- **Sơn cần thêm**:
  - Phân tích sau bảng: tại sao XGBoost tốt nhất? (scale_pos_weight)
  - Nhận xét từng figure (4.4-4.7)

#### 4.3. SHAP XAI
- **Sơn cần hoàn thiện**:
  - Điền 20 từ khóa SHAP từ output Phase 07
  - Mô tả 2-3 đoạn về phân tích tâm lý học từ khóa

#### 4.4. Demo
- Đã hoàn chỉnh với figures từ Phase 08

---

### Chương 5 — Kết luận (~1-2 trang)
- **Template đã có** cấu trúc, Sơn review và bổ sung

---

### Tài liệu tham khảo
- **Sơn cần thêm**: Citation cho Vietnamese SMS Dataset IEEE Access 2026
- Kiểm tra format IEEE: `[N] Tác giả, "Tiêu đề," Nơi xuất bản, Năm.`

---

## ❓ Câu hỏi mở cho Sơn xác nhận khi tạo PR

1. **Figure architecture**: Muốn dùng Mermaid hay Graphviz cho sơ đồ hệ thống Chương 3.4?
2. **Related Works**: Dùng bài báo trong `research-cam-phase04-05-modeling-audit.md` hay tìm mới?
3. **SHAP keywords**: Lấy từ output Phase 07 `reports/` hay từ notebook?
4. **Trang bìa**: Logo UIT ở `docs/assets/` hay cần tải mới từ UIT website?
5. **Auxiliary features**: Lấy tên đầy đủ 15 features từ `src/feature_engineering.py`?

---

## 🛠️ Workflow Sơn thực hiện

```bash
# 1. Checkout branch này
git checkout feat/phase-09-report-template

# 2. Đọc template
cat scam-detection/reports/report/report-source.md

# 3. Điền nội dung còn thiếu (các TODO Sơn) vào report-source.md

# 4. Compile sang Word
python3 ../../.agents/skills/academic-report/scripts/report_builder.py \
  --input scam-detection/reports/report/report-source.md \
  --output scam-detection/reports/report/report.docx \
  --meta scam-detection/reports/report/report-meta.yaml

# 5. Kiểm tra format
python3 ../../.agents/skills/academic-report/scripts/audit_docx_xml.py \
  scam-detection/reports/report/report.docx \
  --output scam-detection/reports/report/audit_result.md

# 6. Xuất PDF từ Microsoft Word thủ công

# 7. Tạo PR → tag @25730067
```

---

## 📋 PR Checklist (Sơn điền khi tạo PR)

- [ ] Tất cả TODO Sơn đã được điền trong report-source.md
- [ ] Chương 1: Số liệu thực tế + 2 vụ điển hình cụ thể
- [ ] Chương 2: Related Works table điền đầy đủ 3-5 bài báo
- [ ] Chương 3.1: 15 auxiliary features liệt kê đầy đủ
- [ ] Chương 3.4: Architecture figure đã render và embed
- [ ] Chương 4: Nhận xét sau mỗi figure (2-3 câu)
- [ ] Chương 4.3: 20 từ khóa SHAP điền đầy đủ
- [ ] Tài liệu tham khảo: IEEE Access 2026 citation
- [ ] report_builder.py compile thành công (không lỗi)
- [ ] audit_docx_xml.py: margins, font, borders đúng chuẩn UIT
- [ ] Tổng trang >= 15 (yêu cầu GV)
- [ ] Cam kết liêm chính học thuật có mặt
- [ ] PR title: feat(phase-09): Write CS114 Final Academic Report Template
- [ ] PR body: tiếng Việt nested bullets
- [ ] Reviewer: @25730067 (Thanh - PM)
