# Raw Data Registry & Provenance Guide

Thư mục này lưu trữ bộ dữ liệu thô tích hợp chính thức (`dataset.csv`) và các tệp dữ liệu phân đoạn (staging) thu thập độc lập bởi 3 thành viên Nhóm 10.

---

## 🛡️ Tuyên Bố Liêm Chính Học Thuật (Zero Synthetic Text)

Bộ dữ liệu đồ án gồm **2.193 mẫu thực tế 100%**, tuân thủ tuyệt đối các cam kết:
1. **0% Dữ liệu AI tự sinh (Zero Synthetic Text):** Kiên quyết loại bỏ mọi mẫu do LLM tự bịa.
2. **0% Rò rỉ thông tin định danh cá nhân (PII Protection):** 100% số điện thoại, số tài khoản, mã OTP, số CCCD đời thực đã được ẩn danh hóa sang các token an toàn (`[MONEY]`, `[NUMBER]`, `[ĐƯỜNG_DẪN]`, `[MÃ_OTP]`).
3. **100% Minh chứng nguồn gốc (Provenance Links):** Mọi dòng dữ liệu đều có liên kết kiểm chứng 1-1 trên GitHub Raw hoặc bài báo chính thống.

---

## 📂 Danh Mục Tệp Dữ Liệu Thô

| Tên Tệp | Số lượng mẫu | Thành viên phụ trách | Nhóm bẫy / Tính chất |
|---------|--------------|----------------------|----------------------|
| `dataset.csv` | **2.193 dòng** | **Cả nhóm** | Bộ dữ liệu tích hợp chính thức sau khi vượt qua `data_validation.py` |
| `staging_thanh_normal.csv` | 1.773 dòng | **Đặng Chí Thanh** | Tin nhắn thường đời thực (Bộ dữ liệu Vietnamese SMS Dataset trên GitHub & CS114 Evidence Vault) |
| `staging_son_scam.csv` | 215 dòng | **Hoàng Cao Sơn** | Tin lừa đảo: Đe dọa quyền lực (`fear_authority`) & Thúc ép gia đình (`family_emergency`) |
| `staging_cam_scam.csv` | 205 dòng | **Bùi Thị Mỷ Cẩm** | Tin lừa đảo: Quà tặng sức khỏe (`health_gift`) & Giả mạo dịch vụ công (`public_service`) |
| `dataset_template.csv` | 6 dòng | **Đặng Chí Thanh** | Tệp mẫu UTF-8-sig quy định header chuẩn |
| `backup_synthetic_*.csv` | — | **Lưu trữ kiểm toán** | Bản lưu vết dữ liệu tổng hợp cũ (đã loại bỏ hoàn toàn khỏi master dataset) |

---

## 📋 Cấu Trúc Header Chuẩn 8 Cột

```csv
id,text,label,scam_category,source,source_url,collector_name,notes
```
