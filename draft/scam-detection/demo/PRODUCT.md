# PRODUCT.md — Đặc tả Trải nghiệm & Sản phẩm: Hệ thống Phát hiện Tin nhắn Lừa đảo Người cao tuổi

> **Tài liệu Nguồn Sự Thật Duy Nhất (Single Source of Truth)** chuẩn hóa theo kỹ năng `uit:ux-research`.  
> Phục vụ thiết kế giao diện demo và kiểm định tương tác trước khi làm visual styling.

---

## 1. Purpose (Mục đích Sản phẩm)

- **Trải nghiệm mới:** Cung cấp một giao diện web trực quan, chuyên biệt hóa cho người cao tuổi và gia đình tại Việt Nam, giúp kiểm tra và bóc trần các kịch bản lừa đảo thao túng tâm lý qua tin nhắn SMS, Zalo, Telegram.
- **Vấn đề giải quyết:** Người cao tuổi tại Việt Nam đang là mục tiêu hàng đầu của các mạng lưới lừa đảo công nghệ cao. Khi bị tấn công bởi các bẫy tâm lý sợ hãi quyền lực (*công an điều tra rửa tiền*), lo lắng gia đình (*con cháu tai nạn cấp cứu*), hoặc bẫy quà tặng sức khỏe (*tri ân người già, thuốc tiên phong tê thấp*), các cụ thường hoảng loạn, không phân biệt được thật giả và vội vã chuyển tiền tiết kiệm cả đời.
- **Vị trí trong dự án:** Là sản phẩm đầu ra ứng dụng thực tế (Phase 08) của đồ án môn học Máy học CS114, đưa mô hình học máy (XGBoost / Random Forest) từ các notebook nghiên cứu đến gần với người dân.

---

## 2. Existing Product Context (Bối cảnh Sản phẩm Hiện tại)

- **Hạ tầng ML sẵn có:**
  - Tập dữ liệu 2.193 mẫu thực tế tiếng Việt, cam kết 100% Zero Synthetic Text (1.773 tin bình thường, 420 tin lừa đảo).
  - Không gian 5.015 đặc trưng (5.000 từ vựng TF-IDF n-gram + 15 đặc trưng hành vi tâm lý phụ).
  - Mô hình máy học XGBoost đạt F1-Score = 0.9535, Random Forest đạt Recall Lừa đảo = 97.62%.
- **Ràng buộc công nghệ:** Triển khai bằng Python + Streamlit trên môi trường local/web để hội đồng chấm đồ án dễ dàng trải nghiệm trực tiếp.

---

## 3. Target User Experience (Trải nghiệm Người dùng Mục tiêu)

- **Độ rõ ràng (Clarity):** Nhìn vào hiểu ngay tin nhắn có nguy hiểm hay không chỉ trong vòng **3 giây** thông qua màu sắc và biểu tượng lớn.
- **Sự tự tin & Trấn an (Confidence & Reassurance):** Không dùng ngôn ngữ công nghệ gây thêm hoang mang (như *"Xác suất lừa đảo 98.42%"* hay *"Vector TF-IDF"*). Dùng ngôn ngữ bình dân, lời khuyên kiên quyết và trấn an: *"Bác hãy bình tĩnh, đây là chiêu trò lừa đảo mạo danh!"*.
- **Công sức (Effort):** Hỗ trợ tính năng "Thử tin mẫu" 1-chạm (One-click preset) để người cao tuổi không phải gõ bàn phím dài dòng.
- **Đường thoát khẩn cấp (Emergency Exit):** Cung cấp ngay nút bấm khẩn cấp để gọi điện cho con cháu hoặc đường dây nóng phòng chống lừa đảo Bộ Công an (A05).

---

## 4. User Journey (Hành trình Người dùng Chi tiết)

```text
[BƯỚC 1: ĐIỂM VÀO]
Người cao tuổi nhận được tin nhắn lạ trên điện thoại (SMS/Zalo/Telegram)
  ↓
[BƯỚC 2: NHẬP LIỆU]
Mở Web App → Chọn "Cỡ chữ lớn cho người cao tuổi" → Dán nội dung hoặc chọn Tin mẫu
  ↓
[BƯỚC 3: PHÂN TÍCH TỨC THỜI]
Bấm nút lớn "🔍 KIỂM TRA NGAY" (Model XGBoost xử lý 5.015 đặc trưng trong < 200ms)
  ↓
[BƯỚC 4: KẾT QUẢ TRỰC QUAN]
Thanh đo rủi ro trực quan (Xanh: An toàn / Vàng: Nghi vấn / Đỏ: Nguy hiểm lừa đảo)
  ↓
[BƯỚC 5: GIẢI THÍCH BẪY TÂM LÝ]
Đoạn tin nhắn được bôi màu từ khóa nguy hiểm + Nêu rõ chiêu trò (Dọa dẫm / Thúc ép / Tiền bạc)
  ↓
[BƯỚC 6: HÀNH ĐỘNG AN TOÀN]
Hiển thị danh sách 4 điều cần làm ngay: KHÔNG CHUYỂN TIỀN - KHÔNG BẤM LINK - KHÔNG ĐỌC OTP - GỌI NGƯỜI THÂN
```

---

## 5. Flow Specification (Đặc tả Các Luồng Chính)

### Luồng 1: Kiểm tra Tin nhắn Mới (Primary Inspection Flow)
- **Kích hoạt:** Người dùng dán nội dung vào khung văn bản và bấm "🔍 KIỂM TRA NGAY".
- **Các bước:**
  1. Kiểm tra văn bản có rỗng không (nếu rỗng, hiển thị lời nhắc dịu dàng).
  2. Kích hoạt module tiền xử lý tiếng Việt (`clean_text`, `segment_vietnamese`, trích xuất 15 đặc trưng phụ).
  3. Dự đoán qua mô hình ML và trả về điểm rủi ro (Risk Score: 0.0 → 1.0).
  4. Hiển thị kết quả chia cột trực quan: Bên trái là tin nhắn có bôi màu từ khóa, bên phải là thước đo rủi ro và khuyến cáo.
- **Xử lý thất bại:** Nếu mô hình chưa được tải, tự động chuyển sang chế độ phân tích quy tắc dự phòng (Rule-based Fallback) để không làm gián đoạn người dùng.

### Luồng 2: Thử Tin mẫu Nhanh (Preset Sample Flow)
- **Kích hoạt:** Người dùng bấm vào 1 trong các thẻ kịch bản mẫu:
  - *Mẫu 1: Dọa bắt giam từ Viện Kiểm Sát / Công An (Fear/Authority).*
  - *Mẫu 2: Con cháu tai nạn cấp cứu tại Chợ Rẫy (Family Emergency).*
  - *Mẫu 3: Nhận quà tri ân thuốc bổ miễn phí (Health/Gift).*
  - *Mẫu 4: Tin nhắn con cái hỏi thăm bình thường (Normal Message).*
- **Kết quả:** Tự động điền văn bản và hiển thị ngay kết quả phân tích để hội đồng hoặc người già trải nghiệm ngay lập tức.

### Luồng 3: Chuyển đổi Chế độ Trợ năng Người cao tuổi (Elderly Accessibility Toggle)
- **Kích hoạt:** Bật công tắc "Chế độ Cỡ chữ Người cao tuổi (Elderly Mode)".
- **Tác động:** Toàn bộ font chữ của giao diện phóng to từ 14px lên 20px–24px, độ tương phản tăng cao, viền thẻ đậm rõ, chiều cao nút bấm tăng tối thiểu 56px.

---

## 6. Screen & State Inventory (Danh mục Màn hình & Trạng thái)

### Màn hình Chính: Dashboard Kiểm tra Tin nhắn
- **Header:** Logo khiên bảo vệ `🛡️`, tiêu đề to rõ ràng, nút chuyển đổi Cỡ chữ Người cao tuổi.
- **Khu vực Nhập liệu (Cột Trái):** Khung nhập tin nhắn rộng, nút "Thử tin mẫu nhanh", nút bấm chính "KIỂM TRA NGAY" to nổi bật.
- **Khu vực Kết quả (Cột Phải):**
  - *Trạng thái Chưa kiểm tra (Empty State):* Lời chào ấm áp, hướng dẫn 2 bước đơn giản để bắt đầu.
  - *Trạng thái An toàn (Safe State - Màu Xanh):* Biểu tượng dấu tích xanh, thông báo *"Tin nhắn có vẻ an toàn"*, nhắc nhở nhẹ nhàng vẫn cần thận trọng.
  - *Trạng thái Nghi vấn (Suspicious State - Màu Vàng):* Biểu tượng cảnh giác, cảnh báo *"Có dấu hiệu bất thường"*, liệt kê các điểm nghi ngờ.
  - *Trạng thái Lừa đảo Nguy hiểm (Scam Alert - Màu Đỏ):* Biểu tượng còi báo động đỏ rực, cảnh báo lớn *"CẢNH BÁO: ĐÂY LÀ KỊCH BẢN LỪA ĐẢO!"*, nêu đích danh chiêu trò thao túng tâm lý.
  - *Hộp Khuyến cáo An toàn (Safety Card):* 4 gạch đầu dòng chữ to in đậm những việc cần làm ngay.

---

## 7. Interaction Requirements (Yêu cầu Tương tác Thân thiện với Người già)

- **Target chạm tối thiểu:** Nút bấm chính và các thẻ chọn có chiều cao tối thiểu 56px, khoảng cách giữa các phần tử >= 12px để tránh chạm nhầm khi tay run.
- **Độ tương phản (Contrast):** Màu chữ trên nền đạt tối thiểu 7:1 (chuẩn WCAG AAA cho người thị lực kém). Chữ đỏ cảnh báo dùng mã màu sẫm rõ (`#B91C1C` trên nền trắng/vàng nhạt `#FEF2F2`).
- **Không tự động biến mất:** Các thông báo cảnh báo không được tự tắt (không dùng toast tự tắt sau vài giây) vì người cao tuổi cần nhiều thời gian để đọc và nghiền ngẫm.

---

## 8. UX Patterns & Research Findings (Minh chứng Nghiên cứu)

| Pattern Nghiên cứu | Ứng dụng Thực tế | Quyết định | Lý do & Minh chứng |
| :--- | :--- | :--- | :--- |
| **Scam Alert Banner** | UK National Cyber Security Centre (NCSC) & Gov.uk | `ADOPT` | Banner đỏ sẫm chiếm trọn tầm nhìn với hành động phủ định kiên quyết ("DO NOT SEND MONEY") giúp ngăn chặn ngay hành vi chuyển tiền bốc đồng. |
| **Three-Tier Risk Meter** | Google Play Protect / VirusTotal | `ADAPT` | Chuyển đổi xác suất toán học 0–100% thành 3 mức độ trực quan Xanh / Vàng / Đỏ, loại bỏ hoàn toàn các chỉ số thập phân gây bối rối. |
| **Psychological Tagging** | Báo cáo Cục An toàn Thông tin (A05) | `ADOPT` | Đặt tên đích danh kịch bản (Dọa công an, Cấp cứu bệnh viện, Tri ân quà tặng) giúp người già nhận diện ngay kịch bản mình vừa đọc. |
| **Technical Metrics Dashboard** | Confusion matrix, F1 curves | `REJECT` | Không đưa ma trận nhầm lẫn hay đồ thị kỹ thuật lên giao diện người dùng cuối; giữ giao diện thuần túy phục vụ dân sinh. |

---

## 9. Product Decisions (Các Quyết định Đã Khóa)

1. **Khóa quyết định không dùng điểm % đơn độc:** Bắt buộc luôn đi kèm nhãn văn bản tiếng Việt cực lớn: `🔴 NGUY CƠ LỪA ĐẢO RẤT CAO`, `🟡 TIN NHẮN NGHI VẤN`, `🟢 TIN NHẮN BÌNH THƯỜNG`.
2. **Khóa quyết định bôi màu trực tiếp trong văn bản:** Không chỉ đưa ra kết luận chung chung, hệ thống phải bôi màu chính xác cụm từ bẫy (ví dụ: *bắt tạm giam*, *chuyển tiền ngay*, *bệnh viện Chợ Rẫy*, *mã OTP*) để người dùng nhìn thấy bằng chứng tại chỗ.
3. **Khóa quyết định chế độ Accessibility mặc định tối ưu:** Ngay cả khi chưa bật Elderly Mode, cỡ chữ mặc định của ứng dụng vẫn phải là 16px (lớn hơn chuẩn 14px thông thường).

---

## 10. Assumptions & Open Questions

- **Đã xác nhận:** Bộ mô hình ML trong `models/` (XGBoost, Random Forest) và TF-IDF scaler trong `data/processed/` hoạt động tốt trên dữ liệu 5.015 chiều.
- **Giả định:** Người cao tuổi chủ yếu truy cập web app qua đường link do con cháu gửi qua Zalo, hoặc dùng trực tiếp trên máy tính bảng gia đình.
- **Câu hỏi mở:** Có nên bổ sung tính năng đọc giọng nói (Text-to-Speech) để đọc to cảnh báo cho các cụ mắt quá kém trong phiên bản tiếp theo không?

## 11. Non-goals (Ngoài Phạm vi)

- Không thu thập số điện thoại cá nhân của người dùng.
- Không tự động gửi tin nhắn báo cáo lên cơ quan công an (chỉ cung cấp số hotline để người dùng tự gọi).
- Không can thiệp hoặc chặn tin nhắn trực tiếp trên hệ điều hành điện thoại (ứng dụng hoạt động độc lập dạng Web).
