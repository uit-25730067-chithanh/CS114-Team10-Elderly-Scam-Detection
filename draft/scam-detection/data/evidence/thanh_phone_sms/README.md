# Kho Ảnh Minh Chứng Tin Nhắn Điện Thoại Thực Tế (Đặng Chí Thanh)

Thư mục này dùng để lưu trữ các ảnh chụp màn hình tin nhắn SMS đời thực từ điện thoại cá nhân của Đặng Chí Thanh.

## Danh mục minh chứng:
- **Số lượng ảnh thực tế:** 20 ảnh (`thanh_sms_01.jpg` đến `thanh_sms_20.jpg`).
- **Thư mục lưu trữ Google Drive:** [**`Dang_Chi_Thanh_Normal_SMS`**](https://drive.google.com/drive/folders/1YIRd0PTYcCP_igYtY4YyZ-QCMKYBkJFg) (Folder ID: `1YIRd0PTYcCP_igYtY4YyZ-QCMKYBkJFg`).
- **Số lượng tin nhắn bóc tách:** 42 tin nhắn SMS đời thực (Viettel Tammi, Viettel++, Nạp thẻ, VoLTE, Bộ Công An, FPT Play OTP, Dịch Vụ Công, Sở KH&CN TP.HCM, Mắt Kính Tâm Đức, TikTok OTP, Karofi OTP, Mặt Trận Tổ Quốc Việt Nam, ePass, Pharmacity, Báo trúng tuyển UIT ngành AI, Bộ VHTTDL, MoMo EVNFinance).
- **Tệp dữ liệu kiểm định độc lập:** `draft/scam-detection/data/processed/real_world_test_thanh.csv`.

## Hướng dẫn tái tạo / bóc tách:
```bash
python3 draft/scam-detection/data/scripts/create_real_world_test.py
```
Script sẽ tự động đọc `drive_links.json`, áp dụng ẩn danh hóa PII (tên, OTP, SĐT, voucher) và lập bảng kiểm định 8 cột với `source_url` liên kết trực tiếp 1-1 tới từng ảnh Drive.
