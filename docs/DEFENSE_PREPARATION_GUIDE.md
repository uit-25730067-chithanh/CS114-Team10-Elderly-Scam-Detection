# 🎓 CẨM NANG BẢO VỆ ĐỒ ÁN CS114 (DEFENSE PREPARATION GUIDE)
## Thuyết Trình Báo Cáo Sớm: Ngày 23/09/2026 — Nhóm 10

**Môn học:** CS114 — Máy học (Machine Learning) — UIT, ĐHQG-HCM  
**Giảng viên chấm:** ThS. Cáp Phạm Đình Thăng  
**Thời lượng quy định:** **15 phút / nhóm** (Khuyến nghị: 11–12 phút thuyết trình + 3–4 phút Q&A phản biện)  
**Đề tài:** *Nghiên cứu và Xây dựng Hệ thống Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam*  
**Thành viên bảo vệ:**
1. **Đặng Chí Thanh** (MSSV: `25730067`) — Lead / Data & NLP Pipeline
2. **Bùi Thị Mỷ Cẩm** (MSSV: `25730013`) — Machine Learning Modeling & Benchmarking
3. **Hoàng Cao Sơn** (MSSV: `25730061`) — Data Collection & Web App Demo UI

---

## I. MA TRẬN PHÂN CHIA THỜI LƯỢNG THUYẾT TRÌNH (12 PHÚT)

| Mốc thời gian | Thời lượng | Nội dung chính | Slide | Người trình bày |
|:---:|:---:|---|:---:|:---:|
| **00:00 – 01:30** | 1.5 phút | Giới thiệu thành viên, Lý do chọn đề tài, Nỗi đau người cao tuổi tại VN 2026, Ý nghĩa xã hội | Slide 1 – 2 | **Đặng Chí Thanh** |
| **01:30 – 04:30** | 3.0 phút | Quy trình thu thập dataset (1.500+ mẫu, chống rò rỉ, 4 nhóm bẫy tâm lý), Pipeline tiền xử lý tiếng Việt & TF-IDF | Slide 3 – 5 | **Đặng Chí Thanh** |
| **04:30 – 08:30** | 4.0 phút | So sánh thực nghiệm 3+ mô hình (NB baseline, RF/XGBoost, SVM), Phân tích Overfitting (Train vs Val Learning Curves), Confusion Matrix & Recall | Slide 6 – 9 | **Bùi Thị Mỷ Cẩm** |
| **08:30 – 11:30** | 3.0 phút | Explainable AI (Top 20 từ khóa kích hoạt tâm lý), Demo trực tiếp Web App Streamlit (live input), Kết luận & Hướng mở rộng | Slide 10 – 13 | **Hoàng Cao Sơn** |
| **11:30 – 15:00** | 3.5 phút | **Hỏi đáp & Phản biện trực tiếp với ThS. Cáp Phạm Đình Thăng (Q&A)** | Slide 14 (Q&A) | **Cả nhóm** |

---

## II. BỐ CỤC SLIDE THUYẾT TRÌNH (14–16 SLIDES)

*Thiết kế tuân thủ bộ nhận diện UIT (Gam màu chủ đạo: Xanh Navy `#003366`, Xanh Dương `#0066CC`, Điểm nhấn Cảnh báo `#D9381E` / `#E65100`). Phông chữ hiện đại (Inter / Roboto / Outfit).*

- **Slide 1: Trang bìa (Title Slide)**
  - Tên đề tài (Tiếng Việt & Tiếng Anh).
  - Tên môn học: CS114 — Máy học | GVHD: ThS. Cáp Phạm Đình Thăng.
  - Thông tin 3 thành viên: Họ tên, MSSV, Email UIT.
- **Slide 2: Tính cấp bách & Ý nghĩa thực tiễn (Problem Statement)**
  - Thống kê tội phạm công nghệ cao nhắm vào người cao tuổi tại VN năm 2026.
  - 4 thủ đoạn thao túng tâm lý: Dọa nạt quyền lực (`fear_authority`), Cấp cứu con cháu (`family_emergency`), Thuốc tiên / Quà tặng (`health_gift`), Cập nhật dịch vụ công giả mạo (`public_service`).
- **Slide 3: Thiết kế & Thu thập Dataset (Dataset Architecture)**
  - Tổng số mẫu: ≥1.500 mẫu tiếng Việt (Thanh: 1.773 mẫu bình thường có permalink; Sơn & Cẩm: 1.000 mẫu lừa đảo từ Bộ Công an, Cục ATTT, báo Dân Trí/VnExpress).
  - Quy trình khử định danh thông tin cá nhân (PII Masking) 100%.
  - Phân chia Stratified Train/Test 80/20 + Tập Holdout Test độc lập 42 mẫu.
- **Slide 4: Pipeline Tiền xử lý Văn bản Tiếng Việt (NLP Preprocessing Pipeline)**
  - Chuẩn hóa Unicode tiếng Việt dựng sẵn (NFC).
  - Xử lý teencode, viết tắt, làm sạch ký tự rác.
  - Tách từ tiếng Việt (`pyvi` / `underthesea`).
- **Slide 5: Trích xuất Đặc trưng (Feature Engineering)**
  - TF-IDF N-grams (1-2) bắt cặp ngữ nghĩa.
  - Trích xuất đặc trưng phụ thủ công (Auxiliary features): đếm số điện thoại lạ, URL, từ khóa đe dọa/cấp bách.
- **Slide 6: Kiến trúc Huấn luyện 3+ Mô hình Machine Learning**
  - Mô hình 1: Multinomial Naive Bayes (Baseline).
  - Mô hình 2: Ensemble Learning — Random Forest & XGBoost.
  - Mô hình 3: Support Vector Machine (LinearSVC Calibrated & RBF Kernel).
- **Slide 7: Bảng Tổng hợp Kết quả Thực nghiệm (Benchmark Table)**
  - So sánh chi tiết: Accuracy, Precision, Recall, F1-Score trên Test Set.
  - Nhấn mạnh chỉ số **Recall lớp Lừa đảo** (đạt mục tiêu $\ge 92\%$).
- **Slide 8: Phân tích Nguy cơ Overfitting qua Learning Curves**
  - Đồ thị đường cong học tập Train vs Validation (5-Fold Cross Validation).
  - Minh chứng mô hình không bị học vẹt, khoảng cách giữa Train và Val tiệm cận hẹp.
- **Slide 9: Phân tích Nhầm lẫn qua Confusion Matrix**
  - Ma trận nhầm lẫn của từng mô hình.
  - Phân tích chi phí thực tế: False Negative (bỏ lọt lừa đảo → người già mất tiền) nguy hiểm hơn nhiều so với False Positive (báo nhầm tin nhắn người nhà).
- **Slide 10: Trí tuệ Nhân tạo Có Thể Giải Thích (Explainable AI - XAI)**
  - Bảng biểu đồ Top 20 từ khóa có trọng số cảnh báo cao nhất (SHAP Values / Feature Weights): *bắt tạm giam, viện kiểm sát, chuyển tiền gấp, tai nạn, nợ cước...*
  - Giúp giải thích tường minh vì sao mô hình đưa ra phán đoán.
- **Slide 11: Ứng dụng Web Demo (Streamlit Application)**
  - Kiến trúc ứng dụng: Chạy trực quan trên trình duyệt.
  - Thiết kế UX thân thiện với người cao tuổi: Nút bấm lớn, độ tương phản cao, thanh đo nguy cơ trực quan (Xanh / Vàng / Đỏ).
- **Slide 12: Kịch bản Kiểm thử Thực tế trên Demo (Case Studies)**
  - Test case 1: Tin nhắn giả danh Viện kiểm sát dọa bắt giam → Cảnh báo ĐỎ, bôi đỏ từ khóa quyền lực, gợi ý gọi 113.
  - Test case 2: Tin nhắn giả mạo VNeID cấp 2 → Cảnh báo ĐỎ, phát hiện link lạ.
  - Test case 3: Tin nhắn hỏi thăm sinh hoạt gia đình bình thường → Cảnh báo XANH an toàn.
- **Slide 13: Kết luận & Định hướng Tương lai (Conclusion & Future Work)**
  - Tóm tắt đóng góp chính của đồ án.
  - Hạn chế của mô hình thống kê truyền thống với ngữ cảnh dài.
  - Định hướng phát triển: Tích hợp mô hình ngôn ngữ lớn (PhoBERT fine-tuning), phát triển tiện ích chặn trên điện thoại (Android App).
- **Slide 14: Lời cảm ơn & Hỏi đáp (Q&A)**
  - Nhóm 10 chân thành cảm ơn ThS. Cáp Phạm Đình Thăng và các bạn sinh viên.
  - Mời Thầy và Hội đồng đặt câu hỏi.

---

## III. BỘ CÂU HỎI PHẢN BIỆN DỰ KIẾN TỪ THẦY THĂNG & CÁCH TRẢ LỜI

### Câu 1: *"Tại sao nhóm lại ưu tiên tối ưu chỉ số Recall của lớp Lừa đảo hơn là Accuracy hay Precision?"*
- **Người trả lời chính:** Bùi Thị Mỷ Cẩm (hoặc Đặng Chí Thanh).
- **Ý chính trả lời:**
  > *"Thưa Thầy, trong bài toán phát hiện gian lận và lừa đảo nhắm vào người cao tuổi, chi phí rủi ro giữa hai loại sai lầm là bất đối xứng nghiêm trọng:*
  > 1. *Nếu **False Positive (Dương tính giả)** xảy ra: Hệ thống cảnh báo nhầm một tin nhắn thông thường là lừa đảo. Hậu quả chỉ là người già tốn thêm 1-2 phút gọi điện hỏi lại người thân để kiểm chứng.*
  > 2. *Nhưng nếu **False Negative (Âm tính giả)** xảy ra: Hệ thống bỏ lọt một tin nhắn lừa đảo tinh vi, người già tin tưởng đây là tin thật và chuyển toàn bộ tiền tiết kiệm dưỡng già cho tội phạm. Hậu quả là không thể cứu vãn.*
  > *Chính vì vậy, trong mục tiêu tối ưu, nhóm chấp nhận đánh đổi một phần Precision để kéo **Recall của lớp Lừa đảo lên trên 92%**."*

---

### Câu 2: *"Nhóm làm cách nào để chứng minh mô hình không bị Overfitting?"*
- **Người trả lời chính:** Bùi Thị Mỷ Cẩm.
- **Ý chính trả lời:**
  > *"Thưa Thầy, nhóm đã kiểm soát và đánh giá Overfitting qua 3 tầng bảo vệ:*
  > 1. *Tầng 1 (K-Fold Cross Validation): Sử dụng 5-Fold Stratified CV trong suốt quá trình tinh chỉnh siêu tham số (GridSearchCV/RandomizedSearchCV), đảm bảo tỷ lệ lớp cân đối.*
  > 2. *Tầng 2 (Learning Curves): Nhóm đã vẽ đường cong học tập giữa Train Score và Validation Score theo số lượng mẫu tăng dần. Đồ thị cho thấy khi số lượng mẫu tăng, Validation Score tiệm cận gần sát Train Score và khoảng cách không vượt quá 3-5%, chứng minh mô hình có khả năng tổng quát hóa tốt.*
  > 3. *Tầng 3 (Independent Holdout Test Set): Nhóm giữ lại một tập 42 mẫu Holdout hoàn toàn tách biệt, chưa từng xuất hiện trong quá trình train hay validation để kiểm tra lần cuối."*

---

### Câu 3: *"Bộ dữ liệu tự thu thập có bị hiện tượng Data Leakage (Rò rỉ dữ liệu) giữa tập Train và Test không?"*
- **Người trả lời chính:** Đặng Chí Thanh.
- **Ý chính trả lời:**
  > *"Thưa Thầy, nhóm kiểm soát rò rỉ dữ liệu bằng quy trình nghiêm ngặt:*
  > 1. *Nhóm thực hiện phân chia Stratified Train/Test (80/20) **ngay sau bước làm sạch cơ bản**, trước khi thực hiện trích xuất TF-IDF.*
  > 2. *`TfidfVectorizer` chỉ được `fit` trên tập Train (`fit_transform(X_train)`), sau đó chỉ dùng `transform(X_test)` trên tập Test. Tuyệt đối không fit trên toàn bộ dữ liệu.*
  > 3. *Đối với các mẫu tăng cường dữ liệu (Data Augmentation), việc sinh mẫu mới chỉ được thực hiện bên trong tập Train, tuyệt đối không tăng cường tập Test.*
  > 4. *Mọi thông tin PII (tên riêng, số điện thoại người thật) đều được mask chuẩn hóa thành token `<PHONE>`, `<NAME>` để tránh mô hình học thuộc lòng danh tính cục bộ."*

---

### Câu 4: *"Trong 3 mô hình đã thử nghiệm, mô hình nào hiệu quả nhất và giải thích tại sao?"*
- **Người trả lời chính:** Bùi Thị Mỷ Cẩm (bổ sung: Hoàng Cao Sơn).
- **Ý chính trả lời:**
  > *"Thưa Thầy, qua thực nghiệm trên tập Test Set:*
  > - *Naive Bayes đạt tốc độ huấn luyện nhanh nhất nhưng Recall lớp lừa đảo còn thấp (~85%) do giả định độc lập có điều kiện không đúng với văn bản tiếng Việt.*
  > - *Random Forest và XGBoost xử lý tốt các đặc trưng phi tuyến tính (kết hợp TF-IDF với số lượng SĐT, link URL) nhưng kích thước mô hình lưu trữ tương đối nặng.*
  > - *Support Vector Machine (LinearSVC Calibrated) cho kết quả cân bằng và xuất sắc nhất (F1 đạt ~90%, Recall Lừa đảo đạt ~93%). Lý do là không gian đặc trưng TF-IDF văn bản có số chiều rất lớn và thưa (High-dimensional Sparse Space) — đây là môi trường mà Linear SVM tìm siêu phẳng phân cách cực kỳ tối ưu, đồng thời thời gian inference dưới 50ms, rất phù hợp để tích hợp vào Web App Demo phục vụ người dùng."*

---

### Câu 5: *"Tại sao nhóm không đưa mô hình PhoBERT vào làm mô hình chính thức mà lại dùng SVM?"*
- **Người trả lời chính:** Đặng Chí Thanh.
- **Ý chính trả lời:**
  > *"Thưa Thầy, nhóm đã thử nghiệm và cân nhắc rất kỹ:*
  > 1. *PhoBERT là mô hình Transformer mạnh về ngữ cảnh tiếng Việt, nhưng đòi hỏi tài nguyên tính toán lớn (GPU) và độ trễ phản hồi (latency) cao khi người cao tuổi sử dụng trên thiết bị thông thường.*
  > 2. *Mục tiêu của môn CS114 là làm chủ các thuật toán Machine Learning cổ điển nền tảng. SVM kết hợp TF-IDF và đặc trưng phụ đã giải quyết bài toán với độ chính xác F1 ≥ 90% mà chỉ mất vài chục millisecond để suy luận trên CPU.*
  > 3. *Để đảm bảo tính ổn định, tin cậy tuyệt đối cho buổi báo cáo sớm và tính thực tế của ứng dụng demo, nhóm chọn Linear SVM làm mô hình cốt lõi phục vụ người dùng, và xếp PhoBERT vào phần hướng phát triển mở rộng."*

---

## IV. CHECKLIST CHUẨN BỊ KỸ THUẬT TRƯỚC GIỜ G (23/09/2026)

- [ ] **Máy tính trình chiếu:** Đã cài sẵn Python 3.10+, kiểm tra cổng xuất HDMI/Type-C với máy chiếu UIT.
- [ ] **Khởi động sẵn Web App Streamlit:** Mở sẵn `localhost:8501`, chuẩn bị sẵn 3 tab trình duyệt với 3 mẫu tin nhắn demo (1 tin dọa nạt, 1 tin dịch vụ công, 1 tin bình thường) để thao tác trong vòng 15 giây.
- [ ] **File Slide dự phòng:** Lưu 1 bản PPTX trên máy, 1 bản xuất PDF (phòng trường hợp lỗi font), 1 bản trên USB và 1 bản trên Google Drive.
- [ ] **Bút trình chiếu (Clicker):** Đã kiểm tra pin, kết nối ổn định.
- [ ] **Đồng hồ bấm giờ:** Phân công 1 thành viên theo dõi thời gian và ra hiệu ở các mốc 5 phút, 10 phút, 12 phút.
