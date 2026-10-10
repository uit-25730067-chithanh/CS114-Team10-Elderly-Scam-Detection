# 📑 Phân Tích Chuyên Sâu: Toàn Bộ Góp Ý & Phương Pháp Luận Của ThS. Cáp Phạm Đình Thăng (Buổi 8 — 23/09/2026)

> **Mục đích:** Cung cấp bức tranh toàn cảnh, minh chứng trích xuất từ 911 dòng transcript Buổi 8 để cả nhóm (Thanh, Cẩm, Sơn) hiểu rõ **lý do tại sao có nhánh `feat/phase-09-defense-feedback-enhancements`** và những yêu cầu phương pháp luận bắt buộc phải đưa vào Báo cáo Final.

---

## 1. Bối Cảnh Buổi Báo Cáo Sớm (23/09/2026)

Tối ngày 23/09/2026, Nhóm 10 đã bảo vệ sớm đồ án trước ThS. Cáp Phạm Đình Thăng. Nhóm đã hoàn thành trọn vẹn phần trình bày luân phiên (Thanh: Bối cảnh & Tiền xử lý; Cẩm: Mô hình & SHAP XAI; Sơn: Demo Web App & Kết luận) tại mốc `[01:08:13]` đến `[01:29:03]`.

Thầy Thăng đánh giá rất cao sự chuẩn bị công phu, tính chân thực của bộ dữ liệu 2.193 mẫu thực tế và sự mượt mà của Web Demo. Tuy nhiên, về mặt **phương pháp luận nghiên cứu khoa học (Empirical Methodology)**, thầy đã chỉ đạo nhóm cần bổ sung các thực nghiệm đối chứng mang tính sống còn vào báo cáo Word để đạt điểm A+ tuyệt đối.

---

## 2. Các Góp Ý Trực Tiếp Cho Nhóm 10 Trong Q&A (`[01:29:03]` – `[01:32:15]`)

### 🔹 Góp ý 1: Xử lý Mất cân bằng dữ liệu (Imbalanced Data)
* **Câu hỏi của thầy (`[01:29:05]` – `[01:29:29]`)**:
  > *"Như vậy thì ở đây mình nhìn thấy của dữ liệu nó cũng mất cân bằng nè. Các bạn có xử lý cái việc mất cân bằng này không? Dữ liệu của mình là khoảng 2000 mấy mẫu đúng không? Trong đó có 400 mẫu là lừa đảo, còn lại khoảng 1700 mẫu không phải lừa đảo (tỷ lệ 4.2 : 1). Dữ liệu này mất cân bằng. Các bạn có xử lý không?"*
* **Phản hồi của nhóm (`[01:29:44]`)**: Nhóm giải thích không can thiệp cơ học vào dữ liệu (không dùng SMOTE vì dễ sinh vector lai tạp vô nghĩa trong văn bản tiếng Việt) mà dùng Cost-sensitive Learning (phạt nặng lỗi bỏ sót tin lừa đảo qua `scale_pos_weight = 4.22` trên XGBoost) và phân tầng Stratified 80/20. Thầy gật đầu đồng ý ("Ok").
* **Yêu cầu Báo cáo**: Phải trình bày công thức toán học của hàm mất mát có trọng số và lý giải khoa học tại sao từ chối SMOTE.

### 🔹 Góp ý 2: Thực nghiệm đối chứng vai trò của Tiền xử lý (Ablation on Preprocessing)
* **Nguyên văn chỉ đạo của thầy (`[01:30:09]` – `[01:30:42]`)**:
  > *"Ở đây mình có trình bày là mình có làm tiền xử lý... Nhưng mình chưa có thực nghiệm là ví dụ nếu mình chưa tiền xử lý và nếu mình tiền xử lý thì kết quả như thế nào? Nó phải tăng thì mình mới làm tiền xử lý đúng không, còn nếu kết quả giảm thì mình làm tiền xử lý làm gì... Nên làm một cái này nè... Tổng hợp lại thành cái bảng, ha."*
* **Ý nghĩa học thuật**: Nhóm làm 5 bước tiền xử lý công phu (Unicode NFC, 160 teencode, PyVi, regex lọc nhiễu). Thầy yêu cầu phải có **bảng số liệu đối chứng đo đạc thực tế trên Test set (439 mẫu)**:
  - Cấu hình 1: Raw Text (chưa tiền xử lý) qua TF-IDF.
  - Cấu hình 2: Preprocessed Text (tiền xử lý đầy đủ) qua TF-IDF.
  - Chứng minh F1 và Recall tăng rõ rệt nhờ chuẩn hóa từ vựng và giữ đúng từ ghép tiếng Việt.

### 🔹 Góp ý 3: Thực nghiệm đối chứng vai trò của 15 Đặc trưng tâm lý (Ablation on Feature Space)
* **Nguyên văn chỉ đạo của thầy (`[01:30:42]` – `[01:32:04]`)**:
  > *"Có trình bày một cái đặc trưng đó là 5000 TF-IDF và mười mấy đặc trưng phụ đúng không?... Khi em trình bày cái TF-IDF này á thì có một chỗ đó là mình có thể thực nghiệm: nếu chỉ dùng đặc trưng TF-IDF thôi, bỏ 15 cái phụ đi thì kết quả như thế nào? Sau đó kết hợp cả hai thì kết quả như thế nào? Để giải thích lý do tại sao mình lại chọn thêm 15 đặc trưng phụ này. Tổng hợp lại thành bảng."*
* **Ý nghĩa học thuật**: Khi phân chia không gian vector thành `5.000 TF-IDF + 15 Features = 5.015 chiều`, người phản biện sẽ hỏi lý do tại sao cần 15 đặc trưng đó. Cần có bảng số liệu so sánh 3 cấu hình:
  - Cấu hình A: Chỉ 5.000 TF-IDF.
  - Cấu hình B: Chỉ 15 Đặc trưng tâm lý.
  - Cấu hình C: Kết hợp 5.015 chiều (mô hình chính thức của nhóm).
  - Chứng minh 15 đặc trưng đóng vai trò chốt chặn an toàn, giữ vững Recall ≥ 97% khi kẻ gian đổi từ vựng.

---

### 🔹 Góp ý 4: Phân tích ca biên cuối buổi & Định hướng giải pháp N-gram (`[02:19:38]` – `[02:20:16]`)
* **Tình huống thực tế**: Cuối buổi học, có một ca test thử câu đe dọa trực diện: *"Cướp đây, đưa hết tiền đây!"* (mô hình trả về điểm rủi ro thấp ~4.1% - báo an toàn).
* **Nguyên văn lời dặn của Thầy Thăng**:
  > *"Bộ lọc phân loại chỉ có 40% hả? Không, nhiều khi tin nhắn này lại không... Tức là cái bài về tin nhắn á các bạn, thì các bạn nên kiểm tra thêm một số cái đặc trưng nữa, ví dụ đặc trưng N-gram nữa để phân tích cái chuỗi đó đó thì nó sẽ nâng cao cái độ chính xác với những tin nhắn như vầy nè. N-gram ha, kết hợp một từ, hai từ, ba từ, bốn từ nữa vân vân... Test thêm đặc trưng N-gram nữa cho cái 5000 TF-IDF á thì nó sẽ phát hiện đúng hơn những cái đó."*
* **Phân tích nguyên nhân kỹ thuật (Đưa vào Mục 4.5 Error Analysis của Báo cáo)**:
  1. **Lệch phân phối kịch bản (Domain Gap)**: Bộ dữ liệu của nhóm tập trung vào các kịch bản lừa đảo qua mạng / viễn thông tinh vi (mạo danh cơ quan công quyền VNeID, đe dọa pháp luật qua văn bản hành chính, dụ đầu tư/tặng quà). Câu *"Cướp đây, đưa hết tiền đây!"* là dạng **đe dọa cưỡng đoạt tài sản bạo lực trực diện ngoài đời thực (Physical Extortion / Robbery)**, rất hiếm gặp trong tin nhắn viễn thông lừa đảo thông thường nên phân phối từ này trong tập huấn luyện bị thiếu hụt.
  2. **Hạn chế của Unigram (Từ đơn lẻ)**: Nếu TF-IDF cấu hình unigram rời rạc, mô hình chỉ thấy các từ riêng lẻ: `cướp`, `đây`, `đưa`, `hết`, `tiền`. Trong dữ liệu thường ngày, từ `tiền`, `đưa`, `đây` xuất hiện nhiều trong tin giao dịch hợp lệ, khiến mô hình bị loãng trọng số rủi ro nếu thiếu mồi nhử URL hoặc số tài khoản.
* **Định hướng giải pháp theo lời Thầy Thăng (Đưa vào Chương 5 Hướng phát triển)**:
  1. **Mở rộng N-gram range lên `(1, 2)` và `(1, 3)`**: Để bắt trọn các cụm từ nối tiếp mang tính đe dọa đặc thù như `"cướp đây"`, `"đưa hết tiền"`, `"chuyển tiền ngay"`, gán trọng số đặc trưng riêng biệt thay vì phân rã thành các từ đơn vô hại.
  2. **Bổ sung nhóm đặc trưng từ khóa cưỡng bức trực diện (`imperative_threat`)**: Nhận diện các cấu trúc mệnh lệnh thức cưỡng đoạt.
  3. **Ứng dụng mô hình ngữ cảnh Transformer (PhoBERT)**: Cơ chế Self-Attention sẽ nắm bắt trọn vẹn ngữ nghĩa câu đe dọa dù câu từ ngắn gọn.

---

## 3. Các Góp Ý Liên Đới Từ Nhóm 7 & Các Nhóm Khác

Quan sát cách thầy chấm Nhóm 7 (cùng làm về đề tài AI phát hiện tin giả và tin nhắn lừa đảo tiếng Việt) và các nhóm khác rút ra 3 chuẩn mực quan trọng:

### 🔹 Góp ý 4: Phân định rạch ròi Bài toán & Phạm vi nghiên cứu (Nhóm 7: `[01:03:16]` – `[01:05:02]`)
* Thầy chấn chỉnh Nhóm 7 khi gộp chung "tin giả" (fake news) và "tin nhắn lừa đảo" (phishing/scam).
* **Phân định của thầy**: Tin giả thì có nguồn uy tín bên ngoài để đối chiếu kiểm chứng (báo chí chính thống, cơ quan pháp luật); còn tin nhắn lừa đảo thì đánh vào hành vi, ngữ cảnh bất thường và tâm lý người nhận, không thể kiểm chứng từ nguồn bên ngoài.
* **Bài học cho Nhóm 10**: Trong Chương 1 & 2, nhóm phải định vị thật sắc nét: đề tài tập trung vào kỹ thuật thao túng xã hội (Social Engineering) nhắm vào người cao tuổi, hoàn toàn khác biệt với bài toán fact-checking tin tức báo chí.

### 🔹 Góp ý 5: Sơ đồ luồng Đầu vào – Đầu ra (Input/Output Flowchart) (Nhóm 7: `[01:05:02]`)
* Thầy yêu cầu: Phải vẽ hình trực quan hóa rõ ràng luồng đầu vào đầu ra của hệ thống, không trình bày lan man: Input raw text → Tiền xử lý → Trích xuất kép → Phân loại → Output nhãn rủi ro & XAI giải thích.

### 🔹 Góp ý 6: Công thức Toán học của Metrics phải tường minh (Nhóm 1: `[12:43]` – `[13:06]`)
* Thầy nhắc nhở sinh viên vì không giải thích được bản chất toán học của metric AUC và yêu cầu: trước khi trình bày bảng kết quả thực nghiệm, phải có mục trình bày công thức toán học của các thước đo (Accuracy, Precision, Recall, F1, ROC-AUC, TF-IDF).

---

## 4. Kết Luận: Tại Sao Cần Nhánh `feat/phase-09-defense-feedback-enhancements`?

1. **Cô lập và bảo vệ phiên bản chính thức**: Nhánh `main` hiện đang lưu giữ bản Slide 22 trang (PR #26) và Kịch bản thuyết trình (PR #27) đã bảo vệ thành công. Nhóm tuyệt đối không đụng vào code demo hay train lại mô hình production.
2. **Tập trung 100% vào Báo cáo Word**: Nhánh mới được tạo ra để:
   - Viết script chạy đo đạc thực nghiệm độc lập cho 2 bảng Ablation Studies.
   - Bổ sung số liệu thực tế, công thức toán và phân định bài toán vào bản thảo Báo cáo `report-source.md`.
   - Biên dịch ra bản Word `report.docx` hoàn chỉnh chuẩn UIT, sẵn sàng cho việc đóng gói nộp bài cuối kỳ (Phase 10).
