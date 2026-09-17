# Project Overview — CS114 Scam Detection

## Tổng quan dự án

**Tên dự án:** Hệ thống Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam  
**Môn học:** CS114 — Máy học (Machine Learning) — UIT, ĐHQG-HCM  
**Nhóm:** 10 (3 thành viên: Đặng Chí Thanh - 25730067 [PM/Lead], Bùi Thị Mỷ Cẩm - 25730013, Hoàng Cao Sơn - 25730061)  
**Repository:** [`uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection`](https://github.com/uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection)  
**Deadline:** 23/09/2026 (Báo cáo sớm theo nguyện vọng nhóm | Hạn LMS gốc: 13/10/2026)

---

## Vấn đề cần giải quyết

Người cao tuổi (NCT) tại Việt Nam là đối tượng bị nhắm mục tiêu nhiều nhất bởi các chiêu trò lừa đảo qua tin nhắn SMS, Zalo, Telegram. Bài toán có 2 thách thức:

1. **Ngữ cảnh tiếng Việt đặc thù**: Teencode, từ viết tắt, không có word boundary rõ ràng, cần tokenizer riêng
2. **Dataset tự thu thập**: Không có benchmark dataset sẵn cho Vietnamese scam SMS → phải xây dựng từ đầu

## Mục tiêu

- Xây dựng pipeline NLP tiếng Việt: thu thập → tiền xử lý → feature extraction → modeling (Đã hoàn thành Phase 01–03)
- Thử nghiệm ≥3 models: Naive Bayes (✅ F1=0.8864), Random Forest (🚀 đang làm), XGBoost (✅ F1=0.9535), SVM (⏳ kế tiếp)
- Phân loại 4 nhóm bẫy tâm lý: `fear_authority`, `family_emergency`, `health_gift`, `public_service`
- Đánh giá: F1-Score ≥ 88%, Recall Scam ≥ 92% (Cả Naive Bayes [Recall 92.86%] và XGBoost [Recall 97.62%, F1 0.9535] đã đạt và vượt mục tiêu)
- Demo Streamlit với UX dành cho người cao tuổi (Sprint 2–3)

## Dataset

| Thuộc tính | Giá trị |
|-----------|---------|
| Nguồn | Đời thực: IEEE Access 2026, UIT IE403, Báo Dân Trí, VnExpress, Tuổi Trẻ, CS114 Evidence Vault |
| Số mẫu | **2.193 mẫu thực tế** (vượt mốc ≥1500) |
| Schema | `id, text, label, scam_category, source, source_url, collector_name, notes` |
| Tỷ lệ | 1.773 Bình thường (80.8%) / 420 Lừa đảo (19.2%) across 4 scam categories |
| Chính sách | **100% Zero Synthetic Text** (0% AI tự sinh, 0% PII leak, 0 duplicate, 100% provenance URLs) |

## Phạm vi đề tài

- ✅ Thu thập và gán nhãn dataset tiếng Việt
- ✅ Vietnamese text preprocessing (Unicode, tokenize, stopwords, TF-IDF)
- ✅ EDA và Feature Engineering
- ✅ ≥3 models (NB + RF/XGB + SVM)
- ✅ Evaluation: Confusion Matrix, Learning Curves, ROC, Precision-Recall
- ✅ XAI: Top-20 scam keywords, SHAP (optional)
- ✅ Báo cáo Word + PPT + Code + Demo Streamlit

## Ngoài phạm vi

- ❌ Deploy lên production server
- ❌ Real-time monitoring
- ❌ Mobile app
- ❌ PhoBERT fine-tuning (optional bonus nếu có thời gian)
