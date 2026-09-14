# BÁO CÁO KHẢO SÁT & KIỂM TOÁN DỮ LIỆU SMS TRÊN KAGGLE
**Đồ án:** Nhận diện tin nhắn / Kịch bản lừa đảo nhắm vào người cao tuổi (CS114 - Nhóm 10)  
**Người thực hiện khảo sát:** Hoàng Cao Sơn  
**Thời gian thực hiện:** 14/09/2026  
**Chế độ quét:** `--hard --deep` (Tải trực tiếp toàn bộ dữ liệu thô, giải nén và rà soát chi tiết từng dòng)

---

## 1. TỔNG QUAN CÁC BỘ DỮ LIỆU TÌM THẤY TRÊN KAGGLE

Hệ thống đã kết nối trực tiếp đến Kaggle API, tải về toàn bộ 4 bộ dữ liệu liên quan đến từ khóa *Vietnamese SMS / Scam / Phishing / Fraud*, giải nén và phân tích cấu trúc dữ liệu thô:

| STT | Dataset Identifier trên Kaggle | Tác giả | Quy mô & Cấu trúc file | Đặc điểm nội dung chính |
| :---: | :--- | :--- | :---: | :--- |
| **1** | `pak3k8/scamshield-vn-vietnamese-scam-and-phishing-detection` | PAK Phan | **16.673 dòng**<br>(`scamshield_vn_public.csv`) | 15.648 URLs lừa đảo, 1.000 tên miền, 25 tin nhắn cảnh báo OTP an toàn. **0 mẫu tin nhắn lừa đảo dạng text.** |
| **2** | `trnminhmn/vietnamese-sms-spam-detection-dataset` | Trần Minh Mẫn (ĐH Nam Cần Thơ) | **5.819 dòng**<br>(`vi_dataset.csv`) | Gồm 4.823 `ham`, 746 `spam`, 250 nhãn `1`. Là bản dịch máy từ bộ UCI tiếng Anh + spam vay tiền template. |
| **3** | `phcohng/vietnamese-sms-spam-dataset` | Phước Đào Hồng | **10.961 dòng**<br>(`vi_dataset.csv`) | Gồm 8.555 `ham`, 2.406 `spam`. Toàn bộ là tin rác quảng cáo trúng thưởng tiếng Anh dịch tự động. |
| **4** | `tuan251209/vietnamese-sms-dataset` | Thái Tuấn (`tranguyenthaituan`) | **2.991 dòng**<br>(`full_dataset.csv`) | Gồm 2.193 `ham`, 798 `spam`. Chuyên phishing mạo danh ngân hàng và cờ bạc. **(Đã được Nhóm trưởng Đặng Chí Thanh sử dụng)**. |

---

## 2. KẾT QUẢ RÀ SOÁT TỪNG DÒNG THEO 2 CHỦ ĐỀ CỦA ANH SƠN

Nhóm từ khóa kiểm tra thực nghiệm (Regex Match):
* **Nhóm `fear_authority`:** `công an`, `viện kiểm sát`, `tòa án`, `lệnh bắt`, `phong tỏa tài sản`, `điều tra`, `rửa tiền`, `ma túy`, `phạt nguội`, `csgt`, `cục thuế`, `chi cục thuế`, `bộ công an`...
* **Nhóm `family_emergency`:** `cấp cứu`, `tai nạn`, `bệnh viện`, `viện phí`, `nguy kịch`, `mổ cấp cứu`, `chấn thương sọ não`...

### Chi tiết kiểm toán từng bộ:

### A. Bộ `pak3k8/scamshield-vn-vietnamese-scam-and-phishing-detection` (16.673 dòng)
* **Mục tiêu ban đầu kỳ vọng:** Là dự án *ScamShield VN*, hy vọng có các kịch bản lừa đảo tiếng Việt.
* **Kết quả thực tế sau giải nén:**
  * File chứa **15.648 dòng URL phishing** từ các feed kỹ thuật (*PhishTank, OpenPhish, URLhaus*).
  * 1.000 dòng benign domain.
  * Chỉ có đúng **25 dòng** có chứa văn bản (`text_sanitized`), nhưng toàn bộ 25 dòng này đều là `benign_message` (mẫu tin nhắn cảnh báo OTP thông thường của ngân hàng như: *"Mã OTP của bạn là 456789. Tuyệt đối không cung cấp mã..."*).
* **Kết luận:** **0 mẫu văn bản lừa đảo**. Không dùng được cho bài toán NLP phân loại văn bản SMS lừa đảo.

---

### B. Bộ `trnminhmn/vietnamese-sms-spam-detection-dataset` (5.819 dòng)
* **Kết quả bóc tách nhãn `spam` (746 dòng):**
  * Dữ liệu dịch máy tự động từ bộ dữ liệu tiếng Anh cổ điển (UCI SMS Spam Collection).
  * *Mẫu thực tế dòng 0:* `"Nhập miễn phí trong 2 WKLY Comp để giành chiến thắng FA Cup Final TKTS ngày 21 tháng 5 năm 2005. Văn bản FA đến 87121 để nhận câu hỏi nhập cảnh..."`
  * *Mẫu khớp duy nhất từ khóa 'tai nạn':* `"FreemSG: Hồ sơ của chúng tôi cho thấy bạn có thể được hưởng 3750 pound cho vụ tai nạn bạn gặp phải."` (Dịch từ mẫu đòi bồi thường bảo hiểm ở Anh tính bằng bảng Anh `pound`).
* **Kết quả bóc tách nhãn `1` (250 dòng):**
  * Toàn bộ là spam quảng cáo sinh tự động bằng template (khuyến mãi, thẻ cào, vay online, đáo hạn, AirPods, iPhone, Shopee):
    * *Dòng 5569:* `"Liên hệ Facebook để giảm giá 20% AirPods, đáo hạn, duyệt trong 5 phút, lấy mã ngay"`
    * *Dòng 5570:* `"Liên hệ Messenger để quà tặng 50% thẻ cào, mở thẻ tín dụng, không chứng minh thu nhập, nhận ngay"`
* **Kết luận:** **0 mẫu lừa đảo đe dọa quyền lực / cấp cứu**. Toàn bộ là spam thương mại hoặc dịch máy.

---

### C. Bộ `phcohng/vietnamese-sms-spam-dataset` (10.961 dòng)
* **Kết quả bóc tách nhãn `spam` (2.406 dòng):**
  * Toàn bộ là spam quảng cáo kiểu Mỹ dịch thô bằng Google Translate:
    * *Dòng 0:* `"Chúc mừng! Bạn đã được chọn tham gia chuyến du lịch nghỉ dưỡng sang trọng. Hãy nhận giải thưởng ngay!"`
    * *Dòng 20:* `"Chúc mừng! Bạn đã được chọn để nhận thẻ quà tặng trị giá 1000 đô la. Nhận ngay!"`
    * *Dòng 25:* `"Hồ sơ của chúng tôi cho thấy bạn đủ điều kiện tham gia chương trình xóa nợ vay sinh viên. Hãy đăng ký ngay!"` (Chính sách xóa nợ sinh viên của Mỹ).
    * Có cả các đoạn tin tức chiến sự Trung Đông của hãng CNN bị dán nhầm vào.
* **Kết luận:** **0 mẫu lừa đảo đời thực tiếng Việt**. Không phù hợp với ngữ cảnh Việt Nam.

---

### D. Bộ `tuan251209/vietnamese-sms-dataset` (2.991 dòng)
* **Tác giả:** Trần Nguyễn Thái Tuấn.
* **Đối soát với Nhóm 10:** Đây là bộ dữ liệu mà **Đặng Chí Thanh (Nhóm trưởng)** đã lấy phần tin nhắn bình thường (Normal).
* **Kết quả bóc tách nhãn `label = 1` (798 dòng):**
  * Tập trung vào: Mạo danh Brandname ngân hàng (Vietcombank, Techcombank, ACB...) gắn link phishing, tin nhắn mời đánh bạc trực tuyến, tin nhắn Pháp Luân Công.
  * **Số mẫu khớp `fear_authority` và `family_emergency`:** **0 mẫu**.
* **Kết luận:** Vừa không có 2 chủ đề của anh Sơn, vừa **trùng nguồn với Nhóm trưởng Thanh** nên tuyệt đối không được đưa vào.

---

## 3. KẾT LUẬN & ĐÁNH GIÁ CHUYÊN MÔN (MACHINE LEARNING)

1. **Thực tế dữ liệu trên Kaggle:**
   * Các tập dữ liệu trên Kaggle gắn nhãn "SMS tiếng Việt" hiện nay chỉ giải quyết bài toán phát hiện **tin nhắn rác thương mại (Spam/Ham)** hoặc **phishing link ngân hàng**.
   * Dạng thức lừa đảo nhắm vào người già (`fear_authority` - dọa bắt giam/rửa tiền/ma túy và `family_emergency` - con cấp cứu) là **tội phạm lừa đảo công nghệ cao có kịch bản thao túng tâm lý sâu**. Kẻ gian không gửi spam hàng loạt bằng máy móc mà sử dụng kịch bản đe dọa trực tiếp (qua SMS, Zalo, gọi điện). Vì vậy, các bộ lọc spam thông thường không thu thập được dạng dữ liệu này.

2. **Khẳng định giá trị của Bộ 215 mẫu đời thực hiện tại (Ground Truth) (`staging_son_scam.csv`):**
   * Tập dữ liệu 215 mẫu đời thực mà anh Sơn đang nắm giữ (được bóc tách từ các chuyên án điều tra của *Dân Trí, Tuổi Trẻ, VnExpress, VietNamNet, Thanh Niên, Báo Công An...* và các mẫu SMS chuẩn học thuật) là **nguồn dữ liệu chân thực, hiếm có và đạt chuẩn cao nhất cho bài toán người cao tuổi**.
   * Dữ liệu hoàn toàn độc lập (0% trùng với Cẩm, 0% trùng với Thanh), đạt 100% về PII Masking và loại bỏ sạch sẽ các khuyến cáo của cơ quan chức năng để tránh mô hình học sai lệch đặc trưng.
