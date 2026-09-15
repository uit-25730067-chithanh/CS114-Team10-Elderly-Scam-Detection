"""Build and execute draft/scam-detection/notebooks/01_preprocessing.ipynb with full cell outputs."""

from __future__ import annotations

from pathlib import Path
import nbformat as nbf
from nbclient import NotebookClient


def create_preprocessing_notebook() -> nbf.NotebookNode:
    """Generate structured notebook nodes for Vietnamese text preprocessing."""
    nb = nbf.v4.new_notebook()

    cells = []

    # Cell 1: Markdown Header & Metadata
    cells.append(nbf.v4.new_markdown_cell("""# CS114: Máy Học (Machine Learning) — Đồ Án Cuối Kỳ
## Phase 02: Tiền Xử Lý Dữ Liệu Văn Bản Tiếng Việt & Trích Xuất Đặc Trưng Phụ

- **Đề tài:** Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam
- **Nhóm thực hiện:** Nhóm 10
  - Đặng Chí Thanh — MSSV: 25730067 (Trưởng nhóm / Phụ trách Phase 02)
  - Bùi Thị Mỷ Cẩm — MSSV: 25730013 (Thành viên)
  - Hoàng Cao Sơn — MSSV: 25730061 (Thành viên)
- **Giảng viên hướng dẫn:** ThS. Cáp Phạm Đình Thăng
- **Mục tiêu Phase 02:**
  1. Chuẩn hóa mã hóa Unicode tiếng Việt theo tiêu chuẩn NFC (khắc phục lỗi tổ hợp).
  2. Trích xuất các đặc trưng phụ (auxiliary features) có tính chất báo động lừa đảo trước khi làm sạch văn bản (URL, SĐT, số tiền, từ khóa áp lực thời gian, từ khóa quyền lực cơ quan).
  3. Làm sạch văn bản: chuẩn hóa từ điển teencode/viết tắt, loại bỏ nhiễu và ký tự đặc biệt mà vẫn bảo toàn dấu thanh tiếng Việt.
  4. Tách từ tiếng Việt (Word Segmentation) bằng thư viện `pyvi` để tạo từ ghép có gạch dưới (`công_an`, `tài_khoản`, `chuyển_khoản`).
  5. Loại bỏ từ dừng (stopwords) ngữ pháp thông thường nhưng nghiêm ngặt bảo toàn các từ khóa trọng yếu của miền bài toán lừa đảo.
  6. Xuất tập dữ liệu tiền xử lý hoàn chỉnh `data/processed/dataset_preprocessed.csv` (2.193 dòng) sẵn sàng cho trích xuất đặc trưng TF-IDF ở Phase 03."""))

    # Cell 2: Code — Setup and Imports
    cells.append(nbf.v4.new_code_cell("""# Import standard libraries and project modules
import os
import sys
import unicodedata
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(os.getcwd()).resolve()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.helpers import RANDOM_STATE, set_seeds
from src.preprocessing import (
    clean_text,
    segment_vietnamese,
    remove_stopwords,
    extract_auxiliary_features,
    preprocess_pipeline,
    TextPreprocessor,
    TEENCODE_DICT,
    EFFECTIVE_STOPWORDS,
    DOMAIN_PROTECTED_WORDS,
)

# Set random seeds for deterministic reproducibility
set_seeds(RANDOM_STATE)
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial"]
print(f"Project root resolved: {PROJECT_ROOT}")
print(f"Random state initialized: {RANDOM_STATE}")"""))

    # Cell 3: Markdown — Section 1: Data Ingestion
    cells.append(nbf.v4.new_markdown_cell("""---
## 1. Khảo Sát Tập Dữ Liệu Gốc (Raw Dataset Overview)

Tập dữ liệu `data/raw/dataset.csv` đã được tổng hợp và kiểm toán qua 7 tầng ở Phase 01 với 2.193 mẫu thực tế, bao gồm:
- 1.773 mẫu tin nhắn bình thường (Label 0) thu thập từ ngân hàng, nhà mạng, tin nhắn cá nhân đời thực.
- 420 mẫu kịch bản lừa đảo (Label 1) phân bổ qua 4 nhóm bẫy thao túng tâm lý:
  - `public_service`: Giả mạo dịch vụ công, VNeID, thuế, cổng dịch vụ.
  - `fear_authority`: Đe dọa pháp lý, giả danh Công an, Viện kiểm sát, Tòa án.
  - `family_emergency`: Tin giả người thân tai nạn cấp cứu, viện phí khẩn cấp.
  - `health_gift`: Quà tri ân sức khỏe, tặng thuốc đông y miễn phí, trúng thưởng."""))

    # Cell 4: Code — Load raw dataset and display distribution
    cells.append(nbf.v4.new_code_cell("""# Load raw master dataset and display distribution
raw_data_path = PROJECT_ROOT / "data" / "raw" / "dataset.csv"
df_raw = pd.read_csv(raw_data_path)

print(f"Total raw samples: {len(df_raw)}")
print(f"Dataset columns: {df_raw.columns.tolist()}")

# Summary of labels and categories
label_dist = df_raw["label"].value_counts().rename({0: "Normal (0)", 1: "Scam (1)"})
category_dist = df_raw["scam_category"].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

# Plot label distribution
sns.barplot(x=label_dist.index, y=label_dist.values, ax=axes[0], palette=["#2ecc71", "#e74c3c"])
axes[0].set_title("Distribution of Labels (Normal vs Scam)", fontsize=12, fontweight="bold")
axes[0].set_ylabel("Count")
for i, v in enumerate(label_dist.values):
    axes[0].text(i, v + 20, f"{v} ({v/len(df_raw)*100:.1f}%)", ha="center", fontweight="bold")

# Plot scam category distribution
sns.barplot(x=category_dist.index, y=category_dist.values, ax=axes[1], palette="Blues_r")
axes[1].set_title("Distribution across Scam Categories", fontsize=12, fontweight="bold")
axes[1].set_ylabel("Count")
axes[1].tick_params(axis="x", rotation=25)
for i, v in enumerate(category_dist.values):
    axes[1].text(i, v + 20, f"{v}", ha="center", fontsize=9, fontweight="bold")

plt.tight_layout()
plt.show()"""))

    # Cell 5: Markdown — Section 2: Step-by-Step Pipeline Demonstration
    cells.append(nbf.v4.new_markdown_cell("""---
## 2. Minh Họa Quy Trình Xử Lý Từng Bước (Step-by-step Demonstration)

Để hiểu rõ sự biến đổi của văn bản qua từng bước, ta tiến hành kiểm thử trên 4 mẫu đại diện thuộc 4 nhóm ngữ cảnh khác nhau:
1. Giả danh Công an thao túng quyền lực (`fear_authority`).
2. Giả danh người thân tai nạn cấp cứu viện phí (`family_emergency`).
3. Giả mạo tri ân tặng quà sức khỏe (`health_gift`).
4. Tin nhắn biến động số dư ngân hàng hợp lệ (`normal`)."""))

    # Cell 6: Code — Step-by-step pipeline test
    cells.append(nbf.v4.new_code_cell("""# Select 4 representative samples for pipeline inspection
demo_samples = [
    # 1. Fear Authority
    ("FEAR_AUTHORITY", "CẢNH BÁO BỘ CÔNG AN: Lệnh bắt giam và phong tỏa tài khoản ngân hàng số 190333 tại VCB của ông/bà do liên quan đường dây ma túy! Bấm http://congan-vietnam.online hoặc gọi ngay 0912345678 để nộp 50 triệu đồng tiền bảo lãnh trước 17h hôm nay!"),
    # 2. Family Emergency
    ("FAMILY_EMERGENCY", "Bố ơi con là Nam đây! Con bị tai nạn giao thông đang cấp cứu nguy kịch ở BV Chợ Rẫy, bnt cần mổ gấp! Bố ck ngay 30 triệu vào stk 0988776655 bsy Nguyễn Văn A để đóng viện phí cho con với!"),
    # 3. Health Gift
    ("HEALTH_GIFT", "TRI ÂN KHÁCH HÀNG CAO TUỔI: Bệnh viện Đông y tặng miễn phí 01 liệu trình cao xương khớp trị giá 2 triệu đồng cho bác! Gọi ngay sdt 0909123456 để nhận quà ngay hôm nay."),
    # 4. Normal Bank SMS
    ("NORMAL_SMS", "[TB] VCB: Số dư TK 0071001234xxx thay đổi -150,000 VND lúc 14:20 15/09/2026. Ref: Chuyen tien hoc phi cho con. So du hien tai: 5,420,000 VND."),
]

demo_results = []
for tag, text in demo_samples:
    aux = extract_auxiliary_features(text)
    clean = clean_text(text)
    seg = segment_vietnamese(clean)
    final = remove_stopwords(seg)
    demo_results.append({
        "Loại": tag,
        "Nguyên bản (trích xuất)": text[:65] + "...",
        "Sau Clean": clean[:65] + "...",
        "Sau Segment (PyVi)": seg[:65] + "...",
        "Kết quả cuối (Stopwords)": final,
        "Đặc trưng phụ chính": f"URL:{aux['num_urls']}, SĐT:{aux['num_phone_numbers']}, Tiền:{aux['num_money_mentions']}, Khẩn:{aux['has_urgent_words']}, Quyền lực:{aux['num_authority_words']}"
    })

pd.set_option("display.max_colwidth", None)
demo_df = pd.DataFrame(demo_results)
display(demo_df[["Loại", "Sau Segment (PyVi)", "Kết quả cuối (Stopwords)", "Đặc trưng phụ chính"]])"""))

    # Cell 7: Markdown — Section 3: Teencode & Abbreviations
    cells.append(nbf.v4.new_markdown_cell("""---
## 3. Khảo Sát Từ Điển Teencode & Chuẩn Hóa Viết Tắt

Tin nhắn SMS và mạng xã hội tiếng Việt chứa nhiều từ viết tắt (`ko`, `dc`, `ck`, `stk`, `cccd`, `nh`, `vcb`). Bộ tiền xử lý tích hợp từ điển `TEENCODE_DICT` với trên 50 mục ánh xạ chuẩn xác sang từ nguyên bản có dấu."""))

    # Cell 8: Code — Teencode inspection
    cells.append(nbf.v4.new_code_cell("""# Inspect teencode coverage and expansion examples
print(f"Total entries in TEENCODE_DICT: {len(TEENCODE_DICT)}")

# Display sample mappings
sample_teencode = dict(list(TEENCODE_DICT.items())[:15])
teencode_sample_df = pd.DataFrame(list(sample_teencode.items()), columns=["Ký hiệu viết tắt", "Ánh xạ chuẩn tiếng Việt"])
display(teencode_sample_df)

# Test expansion on a condensed sentence
slang_sentence = "ko dc ck vao stk nay nhe, nh se khoa tk va otp"
print(f"Câu gốc: {slang_sentence}")
print(f"Sau chuẩn hóa teencode: {clean_text(slang_sentence)}")"""))

    # Cell 9: Markdown — Section 4: Auxiliary Features Analysis
    cells.append(nbf.v4.new_markdown_cell("""---
## 4. Phân Tích Thống Kê Đặc Trưng Phụ (Auxiliary Features EDA)

Các đối tượng lừa đảo thường tạo áp lực tâm lý thông qua:
- Kêu gọi gọi số điện thoại lạ hoặc bấm vào URL giả mạo.
- Nhắc đến các khoản tiền lớn (triệu, tỷ đồng).
- Dùng từ ngữ tạo sự hoảng loạn, gấp gáp (`khẩn cấp`, `bắt giam`, `phong tỏa`).
- Dùng tên cơ quan công quyền để thao túng người già (`Công an`, `Viện kiểm sát`).

Dưới đây là thống kê so sánh giữa nhóm Lừa đảo (Scam) và nhóm Bình thường (Normal)."""))

    # Cell 10: Code — Auxiliary features statistical comparison
    cells.append(nbf.v4.new_code_cell("""# Extract auxiliary features for entire raw dataset
print("Extracting auxiliary features across all samples...")
features_list = [extract_auxiliary_features(t) for t in df_raw["text"]]
features_df = pd.DataFrame(features_list)
features_df["label"] = df_raw["label"]

# Group by label to compare means
comparison_table = features_df.groupby("label").mean().rename(index={0: "Normal", 1: "Scam"})
display(comparison_table.T)

# Plot key auxiliary feature rates
feature_cols_to_plot = ["num_urls", "num_phone_numbers", "num_money_mentions", "has_urgent_words", "num_authority_words"]
fig, axes = plt.subplots(1, len(feature_cols_to_plot), figsize=(16, 3.5))

for idx, col in enumerate(feature_cols_to_plot):
    means = features_df.groupby("label")[col].mean()
    sns.barplot(x=["Normal (0)", "Scam (1)"], y=[means[0], means[1]], ax=axes[idx], palette=["#2ecc71", "#e74c3c"])
    axes[idx].set_title(col, fontsize=11, fontweight="bold")
    axes[idx].set_ylabel("Mean Frequency / Rate")
    axes[idx].set_ylim(0, max(means) * 1.25)
    for i, m in enumerate([means[0], means[1]]):
        axes[idx].text(i, m + 0.02, f"{m:.2f}", ha="center", fontweight="bold")

plt.tight_layout()
plt.show()"""))

    # Cell 11: Markdown — Section 5: Batch Processing & Validation
    cells.append(nbf.v4.new_markdown_cell("""---
## 5. Thực Thi Tiền Xử Lý Hàng Loạt & Kiểm Định Dữ Liệu (Batch Preprocessing & Validation)

Áp dụng lớp `TextPreprocessor` lên toàn bộ 2.193 dòng dữ liệu, kiểm tra:
1. Kích thước tập dữ liệu không đổi (không mất mát dòng).
2. Cột `text_cleaned` không chứa giá trị Null (`NaN`).
3. Cột `text_cleaned` không chứa chuỗi rỗng (`""`).
4. Lưu kết quả ra file `data/processed/dataset_preprocessed.csv`."""))

    # Cell 12: Code — Batch processing and integrity checks
    cells.append(nbf.v4.new_code_cell("""# Batch process entire dataset using TextPreprocessor
preprocessor = TextPreprocessor()
df_preprocessed = preprocessor.process_dataframe(df_raw, text_column="text")

print(f"Preprocessed shape: {df_preprocessed.shape}")
print(f"Columns: {df_preprocessed.columns.tolist()}")

# Integrity assertions
assert len(df_preprocessed) == len(df_raw), f"Data loss detected: {len(df_preprocessed)} vs {len(df_raw)}"
assert df_preprocessed["text_cleaned"].notna().all(), "Null values found in text_cleaned"
empty_strings_count = (df_preprocessed["text_cleaned"].str.strip() == "").sum()
assert empty_strings_count == 0, f"Found {empty_strings_count} empty strings in text_cleaned"

print("[SUCCESS] All integrity criteria satisfied: 2,193 rows preserved, 0 nulls, 0 empty strings.")

# Save preprocessed dataset to disk
out_csv = PROJECT_ROOT / "data" / "processed" / "dataset_preprocessed.csv"
df_preprocessed.to_csv(out_csv, index=False)
print(f"[SAVED] Exported preprocessed dataset to: {out_csv.relative_to(PROJECT_ROOT)} ({out_csv.stat().st_size / 1024:.1f} KB)")"""))

    # Cell 13: Markdown — Section 6: Vocabulary Frequency Analysis
    cells.append(nbf.v4.new_markdown_cell("""---
## 6. Phân Tích Phân Bố Từ Khóa Sau Tiền Xử Lý (Vocabulary Analysis)

Khảo sát 15 từ ghép xuất hiện nhiều nhất trong tập tin nhắn Lừa đảo (Scam) so với tập tin nhắn Bình thường (Normal) để kiểm tra tính phân tách của ngữ nghĩa."""))

    # Cell 14: Code — Vocabulary comparison
    cells.append(nbf.v4.new_code_cell("""# Calculate top word frequencies for scam vs normal
from collections import Counter

scam_texts = df_preprocessed[df_preprocessed["label"] == 1]["text_cleaned"]
normal_texts = df_preprocessed[df_preprocessed["label"] == 0]["text_cleaned"]

scam_words = [w for t in scam_texts for w in t.split()]
normal_words = [w for t in normal_texts for w in t.split()]

top_scam = Counter(scam_words).most_common(15)
top_normal = Counter(normal_words).most_common(15)

df_top_scam = pd.DataFrame(top_scam, columns=["Từ ghép", "Tần số"]).set_index("Từ ghép")
df_top_normal = pd.DataFrame(top_normal, columns=["Từ ghép", "Tần số"]).set_index("Từ ghép")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot top scam words
df_top_scam["Tần số"].plot(kind="barh", ax=axes[0], color="#e74c3c")
axes[0].set_title("Top 15 Từ Khóa Đặc Trưng Nhất Của Tin Nhắn Lừa Đảo", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Số lần xuất hiện")
axes[0].invert_yaxis()

# Plot top normal words
df_top_normal["Tần số"].plot(kind="barh", ax=axes[1], color="#2ecc71")
axes[1].set_title("Top 15 Từ Khóa Đặc Trưng Nhất Của Tin Nhắn Bình Thường", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Số lần xuất hiện")
axes[1].invert_yaxis()

plt.tight_layout()
plt.show()"""))

    # Cell 15: Markdown — Section 7: Conclusions and Next Steps
    cells.append(nbf.v4.new_markdown_cell("""---
## 7. Kết Luận & Chuyển Giao Cho Phase 03

### Kết quả đạt được trong Phase 02:
1. **Module hóa hoàn chỉnh**: Các thành phần tiền xử lý được tổ chức trong `src/preprocessing/` (`text_cleaner.py`, `tokenizer.py`, `stopwords.py`, `pipeline.py`) tuân thủ nghiêm ngặt chuẩn snake_case và quy định < 200 dòng/file.
2. **Bảo toàn ngữ nghĩa tiếng Việt**: Thư viện `pyvi` phân tách chính xác các từ ghép quan trọng (`công_an`, `tài_khoản`, `chuyển_khoản`, `khẩn_cấp`), khắc phục triệt để hiện tượng phân mảnh từ đơn lẻ.
3. **Bảo vệ từ khóa miền bài toán**: Bộ lọc từ dừng loại bỏ các hư từ ngữ pháp (`và`, `là`, `của`, `được`) nhưng giữ lại 100% các từ khóa mang tính chỉ báo thao túng tâm lý.
4. **Trích xuất 10 đặc trưng phụ đắt giá**: Tần suất xuất hiện URL, SĐT, số tiền, từ ngữ khẩn cấp và quyền lực ở nhóm Scam cao vượt trội so với Normal, đóng vai trò then chốt cho các mô hình Machine Learning ở các phase sau.
5. **Dữ liệu đầu ra**: File `data/processed/dataset_preprocessed.csv` gồm 2.193 dòng, 19 cột, hoàn toàn không có giá trị Null hay chuỗi rỗng.

### Bước tiếp theo (Phase 03):
- Khám phá dữ liệu EDA chuyên sâu và trích xuất ma trận TF-IDF (N-gram 1-2).
- Tiến hành phân chia tập dữ liệu Stratified Train/Test (80/20) đảm bảo tính cân bằng tỷ lệ nhãn."""))

    nb.cells = cells
    return nb


def main() -> None:
    nb = create_preprocessing_notebook()
    nb_path = Path("draft/scam-detection/notebooks/01_preprocessing.ipynb")
    nb_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Writing notebook structure to {nb_path}...")
    with open(nb_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print("Executing notebook via NotebookClient to populate outputs...")
    client = NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": "draft/scam-detection"}})
    client.execute()

    print(f"Writing executed notebook back to {nb_path}...")
    with open(nb_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"[SUCCESS] Notebook {nb_path} generated and executed successfully with cell outputs!")


if __name__ == "__main__":
    main()
