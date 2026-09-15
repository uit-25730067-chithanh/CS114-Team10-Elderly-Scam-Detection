# Kho Lưu Trữ Minh Chứng Nguồn Gốc Dữ Liệu (`data/evidence/`)

Thư mục này lưu các minh chứng xác thực nguồn gốc (provenance) cho toàn bộ dataset CS114 Final Project.
**Không chứa dữ liệu đã xử lý** — chỉ chứa bằng chứng thu thập thô để phục vụ kiểm định học thuật.

---

## Chính Sách Git

| Loại file | Trạng thái | Lý do |
|-----------|-----------|-------|
| `.json`, `.md` | ✅ Tracked trong git | Nhỏ, không PII, cần cho reproducibility |
| `.jpg`, `.jpeg`, `.png` | ⛔ `.gitignore` | Có thể chứa PII, ảnh SMS riêng tư; truy cập qua Google Drive |
| `.DS_Store` | ⛔ `.gitignore` | macOS metadata, không cần thiết |

> **Lý do ảnh không được commit:** `thanh_phone_sms/` chứa ảnh chụp màn hình SMS từ điện thoại cá nhân —
> có thể lộ tên người gửi, số điện thoại, nội dung riêng tư. Khi project được public hóa,
> git history không thể undo hoàn toàn. Dùng Google Drive cho phép thu hồi link truy cập.

---

## Cấu Trúc Thư Mục

```
data/evidence/
├── README.md                               ← file này
│
├── [Ảnh báo chí — xem qua Drive]
│   ├── thanhnien_phatnguoi_screenshot.jpeg  (gitignored)
│   ├── tuoitre_phatnguoi_screenshot.jpeg    (gitignored)
│   └── press_screenshots/                   (gitignored)
│       └── thanhnien_cho_ray_msg_*.jpg × 6
│
├── press_articles_cache.json               ← Nội dung bài báo thu thập được (Playwright)
├── press_provenance_audit.json             ← Audit trail permalink 1-1 cho mỗi mẫu báo chí
│
├── youtube_raw_transcripts_cache.json      ← Transcript thô từ VidCap API
├── youtube_transcript_manifest.json        ← Manifest liên kết video → dòng dữ liệu
│
├── backup_synthetic_manifest.json          ← Manifest bản nháp synthetic (Cẩm) — đã archived
├── backup_synthetic_son_manifest.json      ← Manifest bản nháp synthetic (Sơn) — đã archived
│
└── thanh_phone_sms/                        ← Minh chứng SMS thực tế
    ├── README.md                           ← Hướng dẫn truy cập & bóc tách
    ├── drive_links.json                    ← Link 1-1 ảnh Drive ↔ thanh_sms_XX.jpg
    ├── rename_mapping.json                 ← Bảng đổi tên gốc → anonymized
    └── thanh_sms_01–20.jpg × 20           ← (gitignored, xem qua Drive)
```

---

## Truy Cập Ảnh Minh Chứng (Cho Team)

| Bộ minh chứng | Google Drive | Nội dung |
|--------------|-------------|---------|
| **SMS cá nhân Thanh** | [Dang_Chi_Thanh_Normal_SMS](https://drive.google.com/drive/folders/1YIRd0PTYcCP_igYtY4YyZ-QCMKYBkJFg) | 20 ảnh SMS thực, 42 tin nhắn bình thường |
| **Ảnh báo chí** | Xem URL trong `press_provenance_audit.json` | Screenshots bài báo Thanh Niên, VnExpress |

---

## Tái Tạo Từ Drive (Reproducibility)

Để tải ảnh từ Drive về local và chạy lại pipeline bóc tách:

```bash
# Tải ảnh SMS từ Drive (cần google-auth)
python3 data/scripts/create_real_world_test.py

# Verify provenance JSON còn nguyên vẹn
python3 -c "import json; d = json.load(open('data/evidence/press_provenance_audit.json')); print(f'Provenance: {len(d)} entries')"
```

---

## Khi Public Hóa Repo

1. Thu hồi Drive sharing links (1 click trong Google Drive)
2. Git history không chứa ảnh PII → không cần `git filter-branch`
3. JSON manifests vẫn giữ nguyên làm audit trail (không có nội dung nhạy cảm)
