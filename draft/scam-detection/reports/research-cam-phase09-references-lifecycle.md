# Research: Tài liệu tham khảo 2 cột theo vòng đời dự án (Phase 09 — chỉ đạo số 4 của anh Thanh)

- **Tác giả:** Bùi Thị Mỷ Cẩm (25730013) · **Ngày:** 21/09/2026 · **Trạng thái:** đã được Cẩm duyệt (15 mục lên slide, đổi Platt sang bản xuất bản 2000) và áp dụng vào slide 17 ngày 21/09/2026
- **Yêu cầu của anh Thanh:** xếp Slide "Tài liệu tham khảo" thành 2 cột theo vòng đời: *Nguồn cào data → Tiền xử lý NLP → Thuật toán Học máy → XAI → Trợ năng Web → PhoBERT*.
- **Quy tắc của nhóm:** chỉ đưa nguồn thật, mỗi nguồn phải kiểm chứng; không đưa "Báo cáo Cục ATTT" vì chưa có tên báo cáo và đường dẫn để kiểm chứng.

## 1. Phương pháp kiểm chứng
Mọi nguồn được tra bằng cơ sở dữ liệu hoặc trang gốc, không dựa vào trí nhớ: **Crossref** (nguồn có DOI: tên bài, tác giả, tập, số, trang, năm), **trang gốc của tạp chí/hội nghị** (JMLR, NeurIPS Proceedings, AAAI), **arXiv**, **W3C**, **Unicode.org**, **PyPI** và **GitHub API** (phần mềm). Chỉ dùng thư viện mà dự án thật sự import (`pyvi 0.1.1`, `underthesea 9.5.0`, `shap 0.49.1`, `streamlit 1.63.0`, `scikit-learn`, `xgboost`). Truy cập ngày 21/09/2026.

## 2. Kết quả kiểm chứng từng nguồn
| # | Giai đoạn | Nguồn | Bằng chứng kiểm chứng | Trạng thái |
|:-:|---|---|---|---|
| 1 | Dữ liệu | Tran et al., *Vietnamese SMS Dataset with Quality Assurance*, IEEE Access, 2026 | README chính thức của repo `trannguyenthaituan251209/vietnamese_sms_dataset` yêu cầu trích dẫn đúng bài này (5 tác giả); README không ghi tập/DOI | Trích dẫn của tác giả xác nhận; **chưa xác nhận đã xuất bản** |
| 2 | Dữ liệu | Các repo GitHub và báo chí trong `dataset.csv` (249 mẫu lừa đảo) | 4 repo còn tồn tại (`gh api`), mọi dòng có `source_url` | Đã kiểm chứng |
| 3 | NLP | Unicode Consortium, *UAX #15: Unicode Normalization Forms* | Trang unicode.org: Unicode 18.0.0, ngày 2026-08-12, biên tập Ken Whistler | Đã kiểm chứng (dùng cho bước NFC) |
| 4 | NLP | V.-T. Tran, *PyVi* v0.1.1 (phần mềm) | PyPI: tác giả Viet-Trung Tran, giấy phép MIT; GitHub `trungtv/pyvi`; khớp phiên bản dự án | Đã kiểm chứng (phần mềm, không có bài báo) |
| 5 | NLP | Underthesea NLP, *underthesea* v9.5.0 (phần mềm) | PyPI Apache-2.0; GitHub `undertheseanlp/underthesea`; khớp phiên bản dự án; PyPI không ghi tên tác giả cá nhân | Đã kiểm chứng (trích theo tổ chức) |
| 6 | NLP/ML | Salton & Buckley, *Term-weighting approaches in automatic text retrieval*, IPM 24(5):513–523, 1988 | Crossref, DOI 10.1016/0306-4573(88)90021-0 | Đã kiểm chứng (TF-IDF) |
| 7 | ML | Chen & Guestrin, *XGBoost*, KDD 2016, pp. 785–794 | Crossref, DOI 10.1145/2939672.2939785 | Đã kiểm chứng (hiện thiếu số trang) |
| 8 | ML | Breiman, *Random Forests*, Machine Learning 45(1):5–32, 2001 | Crossref, DOI 10.1023/A:1010933404324 | Đã kiểm chứng |
| 9 | ML | Cortes & Vapnik, *Support-vector networks*, Machine Learning 20(3):273–297, 1995 | Crossref, DOI 10.1007/BF00994018 | Đã kiểm chứng |
| 10 | ML | Fan et al., *LIBLINEAR*, JMLR 9:1871–1874, 2008 | Trang jmlr.org; docstring `LinearSVC` của scikit-learn nêu rõ dùng `liblinear` | Đã kiểm chứng |
| 11 | ML | Platt, *Probabilities for SV Machines*, trong *Advances in Large-Margin Classifiers*, MIT Press, 2000, pp. 61–74 | Crossref, DOI 10.7551/mitpress/1113.003.0008 (sách: Smola, Bartlett, Schölkopf, Schuurmans) | Đã kiểm chứng — **khác với trích dẫn hiện có (xem mục 3)** |
| 12 | ML | McCallum & Nigam, *A Comparison of Event Models for Naive Bayes Text Classification*, AAAI-98 Workshop, Tech. Rep. WS-98-05, 1998 | PDF gốc trên aaai.org (đọc trang 1: đúng tên bài và tác giả, 8 trang) | Đã kiểm chứng; không ghi số trang vì trang gốc không hiển thị |
| 13 | ML | Pedregosa et al., *Scikit-learn*, JMLR 12:2825–2830, 2011 | Trang jmlr.org | Đã kiểm chứng |
| 14 | XAI | Lundberg & Lee, *A Unified Approach to Interpreting Model Predictions*, NeurIPS 30, 2017 | proceedings.neurips.cc và arXiv:1705.07874 | Đã kiểm chứng; không ghi số trang (chưa xác nhận được từ nguồn) |
| 15 | XAI | Lundberg et al., *From local explanations to global understanding with explainable AI for trees*, Nature Machine Intelligence 2(1):56–67, 2020 | Crossref, DOI 10.1038/s42256-019-0138-9; `xai_explainer.py` dùng `shap.TreeExplainer` | Đã kiểm chứng (đúng phương pháp nhóm dùng) |
| 16 | Trợ năng | W3C, *WCAG 2.1*, W3C Recommendation 5/6/2018 (bản cập nhật 6/5/2025) | Trang w3.org: tiêu chí 1.4.3 "Contrast (Minimum)" (mức AA) yêu cầu tỉ lệ tương phản ≥ 4.5:1; màu chữ của demo `#1e293b` trên `#ffffff` đo được **14,6:1** | Đã kiểm chứng tiêu chí 1.4.3 |
| 17 | Trợ năng | Streamlit v1.63.0 (phần mềm) | PyPI Apache-2.0; https://streamlit.io | Đã kiểm chứng |
| 18 | Tương lai | Nguyen & Nguyen, *PhoBERT*, Findings of EMNLP 2020, pp. 1037–1042 | Crossref, DOI 10.18653/v1/2020.findings-emnlp.92 | Đã kiểm chứng (hiện thiếu số trang) |

## 3. Sai lệch phát hiện trong danh sách tham khảo hiện tại của deck
1. **[2] Platt:** deck ghi *"Probabilistic Outputs for SVMs…", Advances in Large Margin Classifiers, 1999*. Bản **đã xuất bản** là chương *"Probabilities for SV Machines"*, MIT Press, **2000**, pp. 61–74 (Crossref). Tiêu đề dài và năm 1999 là của bản thảo lưu hành trước đó. Nên đổi sang bản xuất bản để tra được bằng DOI.
2. **[1], [3], [5]:** đúng nguồn nhưng thiếu số trang/DOI; bổ sung theo Crossref/JMLR.
3. **Chưa kiểm chứng, không đưa vào:** báo cáo của Cục ATTT (không có tên/đường dẫn); số trang bài SHAP NeurIPS 2017; số trang bài McCallum & Nigam; tiêu chí WCAG 1.4.4 (không tìm được đúng câu chữ trong lần kiểm tra, và demo chỉ phóng chữ tới 150% nên không nên khẳng định tuân thủ 1.4.4).
4. **Chưa xác nhận được:** bài IEEE Access 2026 của bộ dữ liệu đã xuất bản hay chưa (giữ nguyên ghi chú "chưa có tập/DOI").

## 4. Đề xuất nội dung theo vòng đời (mục để đưa lên slide 17)
Đủ 18 nguồn ở bảng trên sẽ quá dày cho một slide (2 cột, chữ ≥ 10pt tối đa chứa khoảng 14–15 mục kèm tiêu đề giai đoạn). Đề xuất **15 mục lên slide**, phần còn lại dành cho báo cáo Word (kế hoạch yêu cầu ≥ 10 tài liệu IEEE):

| Cột | Giai đoạn | Mục trên slide |
|---|---|---|
| Trái | Nguồn dữ liệu | Tran et al. 2026 (#1); các nguồn bổ sung (#2) |
| Trái | Tiền xử lý NLP | Unicode UAX #15 (#3); PyVi (#4); underthesea (#5); TF-IDF Salton & Buckley (#6) |
| Trái | Thuật toán ML | XGBoost (#7); Random Forest (#8) |
| Phải | Thuật toán ML (tiếp) | SVM Cortes & Vapnik (#9); Platt calibration (#11); scikit-learn (#13) |
| Phải | XAI | SHAP Lundberg & Lee (#14); TreeExplainer (#15) |
| Phải | Trợ năng Web | WCAG 2.1 (#16) |
| Phải | Hướng phát triển | PhoBERT (#18) |

Để dành cho báo cáo Word: LIBLINEAR (#10), McCallum & Nigam (#12), Streamlit (#17).

## 5. Kết quả áp dụng (21/09/2026)
- **Quyết định của Cẩm:** đồng ý 15 mục lên slide, phần còn lại (LIBLINEAR #10, McCallum & Nigam #12, Streamlit #17) để ở báo cáo Word; đổi Platt sang bản xuất bản năm 2000.
- **Slide 17:** 2 cột theo vòng đời, chữ 10pt, đủ 15 mục, không tràn khung (kiểm tra bố cục 0 lỗi).
- **Đánh số mới:** [1] bộ dữ liệu SMS chính, [2] nguồn bổ sung, [3] Unicode UAX #15, [4] PyVi, [5] underthesea, [6] TF-IDF, [7] XGBoost, [8] Random Forest, [9] SVM, [10] Platt, [11] scikit-learn, [12] SHAP, [13] TreeExplainer, [14] WCAG 2.1, [15] PhoBERT.
- **Trích dẫn trong slide:** slide 6 ([1], [2]); slide 8 ([3]–[6]); slide 10 ([7]–[11]); slide 12 ([12], [13]); slide 14 ([14], kèm tương phản chữ 14.6:1); slide 16 ([15]). Mỗi tài liệu trên slide 17 đều được trích dẫn ở ít nhất một slide.
- **Còn lại cho báo cáo Word (≥ 10 tài liệu IEEE theo kế hoạch):** dùng đủ 18 mục ở mục 2, thêm LIBLINEAR, McCallum & Nigam và Streamlit.
