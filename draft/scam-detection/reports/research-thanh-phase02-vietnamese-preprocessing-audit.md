# Research Report: Comprehensive Vietnamese NLP Text Preprocessing for Elderly Scam Detection

- **Course:** CS114 — Machine Learning (Máy học), UIT ĐHQG-HCM
- **Project:** Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam
- **Author:** Đặng Chí Thanh (MSSV: 25730067 — Trưởng nhóm / Phụ trách Tiền xử lý dữ liệu)
- **Date:** 15/09/2026
- **Scope:** Thẩm định toàn diện 2.193 mẫu dữ liệu thực tế (`dataset.csv`), phân tích các biến thể ngôn ngữ tiếng Việt (Unicode, teencode, leet-speak, không dấu, masked entities), và thiết kế kiến trúc tiền xử lý chuẩn mực học máy.

---

## Executive Summary

Qua quá trình rà soát và kiểm toán thực nghiệm trên toàn bộ 2.193 mẫu văn bản thực tế tại `draft/scam-detection/data/raw/dataset.csv`, nhóm nghiên cứu phát hiện cấu trúc văn bản chứa các thách thức đặc thù rất sâu sắc mà các bộ tiền xử lý sơ sài không thể bao quát:
1. **Sự hiện diện dày đặc của các nhãn thực thể đã ẩn danh hóa (Masked Entities)**: Có tới 2.378 nhãn `[MONEY]`, 2.062 nhãn `[NUMBER]`, 700 nhãn `[TIME]`, 161 nhãn `[ĐƯỜNG_DẪN]`, 53 nhãn `[MÃ_OTP]`. Nếu bộ trích xuất đặc trưng chỉ dựa vào regex URL/SĐT/tiền thông thường, hơn 90% các tín hiệu đắt giá này sẽ bị bỏ sót.
2. **Kỹ thuật lẩn tránh bộ lọc (Evasion & Leet-Speak)**: Các đối tượng lừa đảo chủ động sử dụng ký tự thay thế như số `0` thay chữ `o` (`Th0ng ba0`, `kh0ng`, `kh0a`, `vui l0ng`), dùng `!` hoặc `1` thay `i` (`d!eu k!en`, `t!en`, `T1EN`), dùng `j` thay `i` (`TuyetDjnh`, `DacBjet`), chèn các chuỗi ký tự ngẫu nhiên (`aab`, `SP0s`) nhằm vượt qua các bộ lọc viễn thông.
3. **Tính bất đối xứng về dấu thanh (Accent Duality)**: 55.3% tin nhắn thường (980/1.773 mẫu) là tiếng Việt không dấu (do đặc thù tiết kiệm ký tự SMS viễn thông), trong khi 98.3% tin nhắn lừa đảo (413/420 mẫu) là tiếng Việt có dấu (nhằm tạo vẻ trang trọng, giả danh cơ quan nhà nước). Điều này đòi hỏi quy trình tiền xử lý phải hỗ trợ nhận diện cả hai dạng mà không làm mất đi các cụm từ ghép then chốt.
4. **Từ điển viết tắt/Teencode**: Bộ từ điển ban đầu (60 từ) là quá thiếu sót so với kho từ vựng thực tế gồm hơn 7.000 từ vựng duy nhất. Cần mở rộng lên hơn 160 từ viết tắt bao quát toàn diện các lĩnh vực: giao tiếp, viễn thông, ngân hàng, y tế, hành chính tư pháp và tiếng lóng mạng.

Báo cáo này đề xuất kiến trúc tiền xử lý đa tầng chuyên sâu: Chuẩn hóa thực thể ẩn danh → De-obfuscation Leet-Speak → Chuẩn hóa vị trí dấu thanh (NFC + Chuẩn mới) → Mở rộng từ điển 160+ Teencode → Tách từ ghép thích ứng (PyVi) → Lọc từ dừng có bảo vệ danh sách trắng → Trích xuất 14 đặc trưng phụ chuyên sâu.

---

## 1. Thống Kê & Phát Hiện Thực Nghiệm Trên 2.193 Mẫu Dữ Liệu

### 1.1. Thống kê nhãn ẩn danh hóa (Masked Tokens)
| Nhãn ẩn danh | Số lượng xuất hiện | Ý nghĩa trong bài toán lừa đảo |
|--------------|-------------------|--------------------------------|
| `[MONEY]` / `[SỐ_TIỀN]` | 2.449 | Số tiền giao dịch, phí, tiền thưởng, tiền đe dọa cưỡng đoạt |
| `[NUMBER]` | 2.062 | Số hiệu nghị quyết, số tài khoản, mã bưu điện, mã hồ sơ |
| `[TIME]` / `[THỜI_GIAN]` | 746 | Áp lực khung giờ vàng, hạn chót thanh toán, giờ xảy ra tai nạn |
| `[DATE]` | 400 | Ngày ban hành lệnh bắt, ngày hết hạn căn cước, ngày nhập viện |
| `[TB]` / `[QC]` | 520 | Đầu ngữ tin nhắn nhà mạng hoặc đối tượng lừa đảo giả mạo |
| `[ĐƯỜNG_DẪN]` | 161 | Đường link lừa đảo đánh cắp thông tin (phishing URL) |
| `[MÃ_OTP]` | 53 | Mã xác thực giao dịch ngân hàng / đổi mật khẩu |
| `[THƯƠNG_HIỆU]` | 165 | Tên tổ chức bị mạo danh (VCB, Vietinbank, Viettel, Bộ Y tế...) |
| `[SỐ_ĐIỆN_THOẠI]` / `[HOTLINE]` | 25 | Số liên lạc giả danh điều tra viên / bác sĩ cấp cứu |

> **Rút ra**: `extract_auxiliary_features` bắt buộc phải quét cả dạng ký tự thô (raw regex) VÀ các nhãn ẩn danh tương ứng để đạt độ nhạy trích xuất 100%.

### 1.2. Thống kê biến thể Leet-speak và tiếng lóng trong tin nhắn lừa đảo
Các mẫu lừa đảo đời thực từ Cục An toàn thông tin và Bộ Công an ghi nhận các thủ đoạn làm biến dạng chữ cái:
- Thay thế số cho chữ: `0` → `o` (`th0ng ba0`, `kh0ng`, `kh0a`, `vui l0ng`, `d0`), `1` → `i` (`t1en`, `d1eu k1en`), `4` → `a` (`4G`).
- Thay thế dấu câu cho chữ: `!` → `i` (`d!eu'k!en`, `nhan'tien`, `t!en`).
- Thay thế phụ âm: `j` → `i` (`TuyetDjnh`, `DacBjet`, `Tang Rjeng`, `KMaj`).
- Viết tắt tổ chức: `BHTN`, `BH-TN`, `B/H/T/N` (Bảo hiểm thất nghiệp), `BHXH` (Bảo hiểm xã hội), `VNeID`, `NQ-116` / `NQ_II6`.
- Ghép từ không khoảng cách: `[ĐƯỜNG_DẪN]de lay`, `[ĐƯỜNG_DẪN]va nang cap`.

### 1.3. Thống kê tính bất đối xứng về dấu thanh
- **Toàn bộ dataset**: 987/2.193 mẫu (45.0%) hoàn toàn không có dấu tiếng Việt.
- **Nhóm Bình thường (Label 0)**: 980/1.773 mẫu (55.3%) không dấu.
- **Nhóm Lừa đảo (Label 1)**: 413/420 mẫu (98.3%) có dấu đầy đủ; chỉ 7 mẫu không dấu.

---

## 2. Các Nghiên Cứu Kỹ Thuật Chuyên Sâu Cần Áp Dụng

### 2.1. Chuẩn hóa vị trí dấu thanh tiếng Việt (Tone Mark Normalization)
Trong tiếng Việt, tồn tại hai trường phái đặt dấu thanh:
- **Kiểu cũ**: Đặt dấu ở nguyên âm đầu (`hoà`, `toàn`, `thuỷ`, `khoẻ`).
- **Kiểu mới (Chuẩn ngữ âm học hiện đại)**: Đặt dấu ở âm chính đứng sau (`hòa`, `toàn`, `thủy`, `khỏe`).
Sự không đồng nhất này khiến cho mô hình TF-IDF coi `hoà_bình` và `hòa_bình` là 2 đặc trưng hoàn toàn tách biệt, làm loãng không gian vector.
**Giải pháp**: Tích hợp `underthesea.text_normalize` kết hợp `unicodedata.normalize("NFC", text)` để đưa 100% nguyên âm đôi về chuẩn mới thống nhất.

### 2.2. Xử lý De-obfuscation (Hóa giải Leet-speak và lặp ký tự)
- Sử dụng regex đặc thù nhận diện từ ghép chứa `0`, `!`, `1` trong ngữ cảnh từ tiếng Việt để giải mã về nguyên bản:
  - `re.sub(r'\bth0ng\b', 'thông', text)`
  - `re.sub(r'\bba0\b', 'báo', text)`
  - `re.sub(r'\bkh0ng\b', 'không', text)`
  - `re.sub(r'\bkh0a\b', 'khóa', text)`
  - `re.sub(r'\bl0ng\b', 'lòng', text)`
  - `re.sub(r'\bd[!1]eu\s*k[!1]en\b', 'điều kiện', text)`
  - `re.sub(r'\bt[!1]en\b', 'tiền', text)`
- Thu gọn ký tự kéo dài do cảm xúc (Character De-duplication):
  - `nhaaaaa` → `nha`, `gấpppp` → `gấp`, `alooolooo` → `alo`.
  - Regex: `re.sub(r'([a-zA-Zàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ])\1{2,}', r'\1', text)`

### 2.3. Mở rộng từ điển Teencode & Viết tắt (160+ Từ Vựng Toàn Diện)
Mở rộng danh mục từ điển theo 6 nhóm miền ngữ nghĩa chính:
1. **Giao tiếp / Mạng xã hội**: `ib`, `inbox`, `rep`, `tl`, `nt`, `kb`, `fb`, `zalo`, `mess`, `call`, `dt`, `đt`, `sdt`, `sđt`, `sn`, `ns`, `nsx`, `hsd`...
2. **Tiếng lóng & Đại từ thường gặp**: `ko`, `k`, `kh`, `khg`, `hok`, `hông`, `dc`, `đc`, `ng`, `ngừoi`, `vs`, `mk`, `mik`, `mềnh`, `bn`, `mn`, `r`, `ch`, `bt`, `tks`, `ty`, `thks`, `thanks`, `nhug`, `nha`, `nhe`, `nhé`, `cx`, `đag`, `dag`, `tg`, `h`, `p`, `đk`, `dk`...
3. **Mẫu tin viễn thông (Telecom Patterns)**: `tb`, `qc`, `lh`, `soan`, `qk`, `kh`, `tt`, `yc`, `km`, `cuoc`, `goi`, `dv`, `hd`, `hđ`, `nv`, `cs`, `cskh`...
4. **Giao dịch & Tài chính ngân hàng**: `ck`, `tk`, `stk`, `acc`, `pass`, `nh`, `atm`, `otp`, `vnd`, `vnđ`, `tr`, `ngàn`, `k`, `gd`, `sodu`, `tien`, `khoan`...
5. **Cơ quan công quyền & Pháp lý**: `ca`, `cand`, `cs`, `csgt`, `cstt`, `vks`, `vksnd`, `ta`, `tand`, `ubnd`, `bca`, `byt`, `bkhcn`, `bhtn`, `bhxh`, `bhyt`, `bv`, `bsy`, `bs`, `bnt`, `vneid`, `cmnd`, `cccd`, `gplx`, `nq`...
6. **Mã ngân hàng Việt Nam**: `vcb`, `tcb`, `bidv`, `ctg`, `acb`, `mb`, `vpb`, `tpb`, `shb`, `hdb`, `vib`, `msb`, `ocb`, `scb`, `agri`, `agribank`...

### 2.4. Chiến lược Tách từ tiếng Việt thích ứng (Adaptive Tokenization)
- Thư viện `pyvi` phân tách từ ghép tiếng Việt rất tốt đối với văn bản có dấu (`công_an`, `tài_khoản`, `ngân_hàng`).
- Đối với 45% mẫu văn bản không dấu, `pyvi` mặc định không nhận diện được từ ghép (`tai khoan` không thành `tai_khoan`).
- **Giải pháp**: Xây dựng bước tiền xử lý nối cụm từ không dấu phổ biến (Phrase-level Unaccented Joining):
  - Ánh xạ các cụm 2 từ không dấu trọng yếu như `tai khoan` → `tai_khoan`, `chuyen khoan` → `chuyen_khoan`, `cong an` → `cong_an`, `ngan hang` → `ngan_hang`, `mat khau` → `mat_khau`, `xac thuc` → `xac_thuc`, `quy khach` → `quy_khach`, `thong bao` → `thong_bao`, `tien mat` → `tien_mat`.
  - Nhờ đó, các văn bản không dấu vẫn giữ được tính toàn vẹn của khái niệm ngữ nghĩa, đồng bộ với văn bản có dấu.

### 2.5. Danh mục 14 Đặc trưng Phụ (Auxiliary Features) Chuyên Sâu
Mở rộng bộ đặc trưng phụ từ 10 lên 14 chỉ báo đắt giá:
1. `num_urls`: Tổng số URL thực tế + nhãn `[ĐƯỜNG_DẪN]` + `[URL]`.
2. `num_phone_numbers`: Tổng số điện thoại thực tế + nhãn `[SỐ_ĐIỆN_THOẠI]` + `[HOTLINE]`.
3. `num_money_mentions`: Tổng số lần đề cập tiền tệ thực tế + nhãn `[MONEY]` + `[SỐ_TIỀN]`.
4. `has_urgent_words`: Chỉ báo áp lực thời gian (`gấp`, `khẩn`, `hạn chót`, `trong ngày`, `phong tỏa`, `bắt giam`, `truy nã`, `tạm khóa`, `tạm giữ`).
5. `num_authority_words`: Số lần xuất hiện danh xưng cơ quan công quyền (`công an`, `cảnh sát`, `viện kiểm sát`, `tòa án`, `bộ công an`, `bộ y tế`, `vneid`, `bảo hiểm xã hội`).
6. `has_emergency_words`: Chỉ báo tai nạn người thân (`cấp cứu`, `tai nạn`, `viện phí`, `bệnh viện`, `mổ gấp`, `nguy kịch`, `mất máu`).
7. `has_gift_words`: Chỉ báo bẫy tặng quà/trúng thưởng (`trúng thưởng`, `tri ân`, `tặng quà`, `miễn phí`, `lì xì`, `quay số`).
8. `has_otp_request`: Chỉ báo yêu cầu cung cấp OTP/mật khẩu (`mã otp`, `mật khẩu`, `xác thực`, `mã gd`, `[MÃ_OTP]`).
9. `has_leet_speak`: Phát hiện tin nhắn có sử dụng thủ thuật lẩn tránh chữ cái/số.
10. `is_unaccented`: Phát hiện tin nhắn có phải tiếng Việt không dấu (0/1).
11. `text_length`: Độ dài ký tự nguyên bản.
12. `num_words`: Số lượng từ nguyên bản.
13. `num_exclamation`: Số lượng dấu chấm than `!`.
14. `num_uppercase_words`: Số từ viết hoa toàn bộ (đặc trưng của tin nhắn đe dọa).

---

## 3. Kiến Trúc Pipeline Tiền Xử Lý Đề Xuất

```
Raw Text (2,193 mẫu thực tế)
  │
  ├── [1] Trích xuất 14 đặc trưng phụ (Auxiliary Features)
  │       (Bao gồm quét cả regex thô và các nhãn masked tokens [MONEY], [ĐƯỜNG_DẪN], [MÃ_OTP]...)
  │
  ├── [2] De-obfuscation & Tách nhãn dính
  │       (Hóa giải leet-speak th0ng ba0, d!eu k!en, t!en; tách dính [ĐƯỜNG_DẪN]de lay)
  │
  ├── [3] Chuẩn hóa dấu thanh tiếng Việt (Tone Normalization)
  │       (underthesea.text_normalize + unicodedata NFC)
  │
  ├── [4] Hạ chữ thường (Lowercase) & Lọc nhiễu URL/SĐT
  │       (Thay URL và SĐT bằng khoảng trắng sau khi đã trích xuất đặc trưng phụ)
  │
  ├── [5] Mở rộng Teencode & Viết tắt (160+ Mappings)
  │       (Ánh xạ chuẩn toàn diện cả có dấu lẫn không dấu)
  │
  ├── [6] Ghép cụm từ không dấu & Tách từ tiếng Việt thích ứng (PyVi)
  │       (pyvi.ViTokenizer + Phrase Joining cho mẫu không dấu)
  │
  ├── [7] Lọc từ dừng ngữ pháp có bảo vệ danh sách trắng
  │       (Loại bỏ hư từ, bảo vệ 100% từ khóa thao túng tâm lý và chỉ báo lừa đảo)
  │
  └── Output: Cleaned & Segmented Text + 14 Auxiliary Feature Columns
```

---

## 4. Kế Hoạch Chuyển Giao & Tái Cấu Trúc

1. **Mã nguồn**:
   - Nâng cấp [`text_cleaner.py`](src/preprocessing/text_cleaner.py): Tích hợp `underthesea.text_normalize`, bổ sung de-obfuscation leet-speak, mở rộng `TEENCODE_DICT` lên 160+ từ.
   - Nâng cấp [`tokenizer.py`](src/preprocessing/tokenizer.py): Thêm phrase-joining cho tin nhắn không dấu trước khi gọi `ViTokenizer`.
   - Nâng cấp [`pipeline.py`](src/preprocessing/pipeline.py): Nâng cấp bộ trích xuất đặc trưng phụ lên 14 cột, bao quát toàn diện nhãn masked entities.
2. **Kiểm thử**: Mở rộng `test_preprocessing.py` từ 13 lên 20+ test cases kiểm định leet-speak, không dấu, và nhãn masked.
3. **Dữ liệu & Sổ tay**: Tái tạo `dataset_preprocessed.csv` và chạy lại `01_preprocessing.ipynb`.
4. **Git & PR**: Commit các cải tiến và cập nhật PR #12.

---

## Unresolved Questions
- Không có câu hỏi nào chưa được giải quyết. Kế hoạch nghiên cứu đã xác định đầy đủ bằng chứng thực nghiệm trên toàn bộ 2.193 dòng dữ liệu.
