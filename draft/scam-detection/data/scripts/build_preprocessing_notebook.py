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
## Phase 02: Tiền Xử Lý Dữ Liệu Văn Bản Tiếng Việt & Trích Xuất Đặc Trưng Phụ (Phiên Bản Nâng Cao Nghiên Cứu)

- **Đề tài:** Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam
- **Nhóm thực hiện:** Nhóm 10
  - Đặng Chí Thanh — MSSV: 25730067 (Trưởng nhóm / Phụ trách Tiền xử lý dữ liệu)
  - Bùi Thị Mỷ Cẩm — MSSV: 25730013 (Thành viên)
  - Hoàng Cao Sơn — MSSV: 25730061 (Thành viên)
- **Giảng viên hướng dẫn:** ThS. Cáp Phạm Đình Thăng
- **Các phát hiện thực nghiệm & Mục tiêu nâng cấp của Phase 02:**
  1. **Khắc phục hiện tượng ẩn danh hóa (Masked Tokens)**: Xử lý hơn 2.400 nhãn `[MONEY]`, 2.060 nhãn `[NUMBER]`, 160 nhãn `[ĐƯỜNG_DẪN]`, 53 nhãn `[MÃ_OTP]`.
  2. **De-obfuscation thủ thuật Leet-speak**: Hóa giải các ký tự lẩn tránh bộ lọc tin nhắn rác của kẻ lừa đảo (`th0ng ba0`, `kh0ng`, `kh0a`, `d!eu k!en`, `t!en`, `h0 tro`, `BHTN`).
  3. **Xử lý tính bất đối xứng dấu thanh**: 55.3% tin nhắn thường là tiếng Việt không dấu (do viễn thông tiết kiệm ký tự), trong khi 98.3% tin nhắn lừa đảo là tiếng Việt có dấu. Tích hợp cơ chế nối từ ghép không dấu (`tai_khoan`, `chuyen_khoan`, `cong_an`).
  4. **Chuẩn hóa dấu thanh chuẩn mới**: Tích hợp `underthesea.text_normalize` kết hợp `unicodedata` NFC để đưa vị trí đặt dấu về chuẩn ngữ âm học thống nhất (`hòa`, `khỏe`, `thủy`).
  5. **Mở rộng từ điển Teencode/Viết tắt**: Nâng cấp lên trên 160 mục từ vựng bao quát 6 lĩnh vực chính (giao tiếp, viễn thông, ngân hàng, công quyền, y tế, tiếng lóng).
  6. **Trích xuất 15 đặc trưng phụ chuyên sâu**: Bổ sung các cờ phát hiện leet-speak, không dấu, cấp cứu gia đình, bẫy quà tặng, và yêu cầu OTP."""))

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
    deobfuscate_leetspeak,
    normalize_tone_marks,
    segment_vietnamese,
    remove_stopwords,
    extract_auxiliary_features,
    preprocess_pipeline,
    TextPreprocessor,
    TEENCODE_DICT,
    LEET_SPEAK_PATTERNS,
    UNACCENTED_COMPOUNDS,
    EFFECTIVE_STOPWORDS,
    DOMAIN_PROTECTED_WORDS,
)

# Set random seeds for deterministic reproducibility
set_seeds(RANDOM_STATE)
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial"]
print(f"Project root resolved: {PROJECT_ROOT}")
print(f"Random state initialized: {RANDOM_STATE}")
print(f"Teencode dictionary active entries: {len(TEENCODE_DICT)}")"""))

    # Cell 3: Markdown — Section 1: Data Ingestion & Masked Entity Audit
    cells.append(nbf.v4.new_markdown_cell("""---
## 1. Khảo Sát Tập Dữ Liệu Gốc & Thực Thể Ẩn Danh (Masked Entity Audit)

Tập dữ liệu `data/raw/dataset.csv` gồm 2.193 mẫu thực tế, trong đó có một lượng lớn thực thể được ẩn danh hóa ở Phase 01 nhằm bảo vệ quyền riêng tư (Zero PII Leakage)."""))

    # Cell 4: Code — Load raw dataset and inspect masked placeholders
    cells.append(nbf.v4.new_code_cell("""# Load raw dataset and analyze masked entities distribution
raw_data_path = PROJECT_ROOT / "data" / "raw" / "dataset.csv"
df_raw = pd.read_csv(raw_data_path)

print(f"Total raw samples: {len(df_raw)}")
print(f"Columns: {df_raw.columns.tolist()}")

# Count masked placeholders
import re
from collections import Counter

placeholders = Counter()
for text in df_raw["text"]:
    matches = re.findall(r"\\[(.*?)\\]", text)
    placeholders.update(matches)

df_placeholders = pd.DataFrame(placeholders.most_common(12), columns=["Nhãn Ẩn Danh", "Số Lượng"])
display(df_placeholders)

# Visualize label distribution
fig, ax = plt.subplots(figsize=(6, 3.5))
label_counts = df_raw["label"].value_counts().rename({0: "Normal (Bình thường)", 1: "Scam (Lừa đảo)"})
sns.barplot(x=label_counts.index, y=label_counts.values, ax=ax, palette=["#2ecc71", "#e74c3c"])
ax.set_title("Phân Bố Nhãn Dữ Liệu CS114 Final (2.193 Mẫu Thực Tế)", fontsize=11, fontweight="bold")
for i, v in enumerate(label_counts.values):
    ax.text(i, v + 25, f"{v} ({v/len(df_raw)*100:.1f}%)", ha="center", fontweight="bold")
plt.tight_layout()
plt.show()"""))

    # Cell 5: Markdown — Section 2: De-obfuscation & Step-by-Step Demonstration
    cells.append(nbf.v4.new_markdown_cell("""---
## 2. Hóa Giải Kỹ Thuật Lẩn Tránh (De-obfuscation) & Minh Họa Từng Bước

Thủ đoạn của đối tượng lừa đảo qua tin nhắn thường xuyên dùng số thay chữ cái (`th0ng ba0`, `kh0ng`, `kh0a`, `d!eu k!en`, `t!en`) và dính các thẻ đường dẫn để tránh bị chặn bởi AI/Telco filter."""))

    # Cell 6: Code — Step-by-step pipeline test
    cells.append(nbf.v4.new_code_cell("""# Test pipeline on 4 representative samples including obfuscated leet-speak
demo_samples = [
    # 1. Leet-speak obfuscated scam (Evading filter)
    ("LEET_SPEAK_SCAM", "Th0ng ba0: [THƯƠNG_HIỆU] nang cap he thong. Vui l0ng dang nhap [ĐƯỜNG_DẪN]va nang cap. Neu kh0ng tai khoa se bi kh0a. aab"),
    # 2. Insurance trap with punctuation substitution
    ("BHTN_OBFUSCATED", "Ong/(Ba) da du d!eu'k!en NHAN'TIEN ho tro tu quy-BHTN. Bam'vao [ĐƯỜNG_DẪN]de_'lay. QUA-HAN' SE KH0ng duoc nhan nua nhe!"),
    # 3. Tone normalization test (Old vs New style)
    ("TONE_NORMALIZATION", "hoà bình và khoẻ mạnh, thuỷ điện toàn quốc"),
    # 4. Unaccented Normal SMS
    ("UNACCENTED_NORMAL", "Quy khach da dang ky thanh cong goi data 4G, cuoc phi [MONEY] tru vao tai khoan."),
]

demo_results = []
for tag, text in demo_samples:
    aux = extract_auxiliary_features(text)
    clean = clean_text(text)
    seg = segment_vietnamese(clean)
    final = remove_stopwords(seg)
    demo_results.append({
        "Mẫu": tag,
        "Văn bản gốc": text[:60] + "...",
        "Sau Clean & De-obfuscate": clean[:60] + "...",
        "Sau Tách từ PyVi": seg[:60] + "...",
        "Kết quả cuối cùng": final,
        "Chỉ báo đặc trưng": f"URL:{aux['num_urls']}, Tiền:{aux['num_money_mentions']}, Leet:{aux['has_leet_speak']}, Không dấu:{aux['is_unaccented']}"
    })

demo_df = pd.DataFrame(demo_results)
display(demo_df[["Mẫu", "Sau Clean & De-obfuscate", "Sau Tách từ PyVi", "Kết quả cuối cùng", "Chỉ báo đặc trưng"]])"""))

    # Cell 7: Markdown — Section 3: Teencode Dictionary Inspection
    cells.append(nbf.v4.new_markdown_cell("""---
## 3. Khảo Sát Từ Điển Teencode & Viết Tắt Mở Rộng (160+ Từ Vựng)

Bộ từ điển `TEENCODE_DICT` được nâng cấp lên trên 160 mục từ vựng, bao quát toàn diện các lĩnh vực: giao tiếp, viễn thông, ngân hàng, cơ quan công quyền, y tế và tiếng lóng mạng xã hội."""))

    # Cell 8: Code — Teencode inspection
    cells.append(nbf.v4.new_code_cell("""# Display sample categories of the expanded teencode dictionary
print(f"Total entries in TEENCODE_DICT: {len(TEENCODE_DICT)}")

# Display 20 representative mappings across different domains
sample_items = list(TEENCODE_DICT.items())[:20]
teencode_df = pd.DataFrame(sample_items, columns=["Từ Viết Tắt / Teencode", "Dạng Chuẩn Tiếng Việt"])
display(teencode_df.T)

# Test expansion on a dense SMS sentence
slang_sentence = "ko dc ck vao stk nay nhe, ca se vao cuoc va vks se khoi to bca"
print(f"Câu gốc: {slang_sentence}")
print(f"Sau chuẩn hóa: {clean_text(slang_sentence)}")"""))

    # Cell 9: Markdown — Section 4: Auxiliary Features Analysis
    cells.append(nbf.v4.new_markdown_cell("""---
## 4. Phân Tích Thống Kê 15 Đặc Trưng Phụ Chuyên Sâu (Auxiliary Features EDA)

Thống kê so sánh 15 chỉ số giữa hai lớp Lừa đảo (Scam) và Bình thường (Normal). Các đặc trưng này mang tính phân tách cực kỳ mạnh mẽ."""))

    # Cell 10: Code — Auxiliary features statistical comparison
    cells.append(nbf.v4.new_code_cell("""# Extract auxiliary features across all 2,193 samples
print("Trích xuất 15 đặc trưng phụ trên toàn bộ 2.193 mẫu dữ liệu...")
features_list = [extract_auxiliary_features(t) for t in df_raw["text"]]
features_df = pd.DataFrame(features_list)
features_df["label"] = df_raw["label"]

# Group by label to compute means
comparison_table = features_df.groupby("label").mean().rename(index={0: "Normal (0)", 1: "Scam (1)"})
display(comparison_table.T)

# Plot key auxiliary feature distributions
key_features = [
    ("has_urgent_words", "Áp Lực Khẩn Cấp"),
    ("has_emergency_words", "Tai Nạn Cấp Cứu"),
    ("num_authority_words", "Cơ Quan Quyền Lực"),
    ("has_leet_speak", "Thủ Đoạn Leet-Speak"),
    ("is_unaccented", "Tiếng Việt Không Dấu"),
]

fig, axes = plt.subplots(1, len(key_features), figsize=(16, 3.5))
for idx, (col, title) in enumerate(key_features):
    means = features_df.groupby("label")[col].mean()
    sns.barplot(x=["Normal", "Scam"], y=[means[0], means[1]], ax=axes[idx], palette=["#2ecc71", "#e74c3c"])
    axes[idx].set_title(title, fontsize=10, fontweight="bold")
    axes[idx].set_ylabel("Tỷ lệ xuất hiện")
    axes[idx].set_ylim(0, max(means) * 1.35 if max(means) > 0 else 1.0)
    for i, m in enumerate([means[0], means[1]]):
        axes[idx].text(i, m + 0.01, f"{m:.3f}", ha="center", fontweight="bold", fontsize=9)

plt.tight_layout()
plt.show()"""))

    # Cell 11: Markdown — Section 5: Batch Processing & Validation
    cells.append(nbf.v4.new_markdown_cell("""---
## 5. Thực Thi Tiền Xử Lý Hàng Loạt & Kiểm Định Tính Toàn Vẹn (Batch Preprocessing)

Áp dụng lớp `TextPreprocessor` lên toàn bộ 2.193 dòng dữ liệu:
- Bảo toàn tuyệt đối số lượng mẫu (2.193 dòng).
- Đảm bảo 0 giá trị Null trong `text_cleaned`.
- Đảm bảo 0 chuỗi rỗng sau tiền xử lý.
- Xuất dữ liệu ra `data/processed/dataset_preprocessed.csv`."""))

    # Cell 12: Code — Batch processing and integrity checks
    cells.append(nbf.v4.new_code_cell("""# Batch process entire dataset using TextPreprocessor
preprocessor = TextPreprocessor()
df_preprocessed = preprocessor.process_dataframe(df_raw, text_column="text")

print(f"Kích thước sau tiền xử lý: {df_preprocessed.shape}")
print(f"Tổng số cột: {len(df_preprocessed.columns)}")

# Integrity assertions
assert len(df_preprocessed) == len(df_raw), f"Lỗi mất mát dữ liệu: {len(df_preprocessed)} vs {len(df_raw)}"
assert df_preprocessed["text_cleaned"].notna().all(), "Phát hiện giá trị Null trong text_cleaned!"
empty_count = (df_preprocessed["text_cleaned"].str.strip() == "").sum()
assert empty_count == 0, f"Phát hiện {empty_count} chuỗi rỗng trong text_cleaned!"

print("[THÀNH CÔNG] Toàn bộ 2.193 mẫu đã được tiền xử lý hoàn chỉnh (0 nulls, 0 empty strings).")

# Save preprocessed dataset to disk
out_csv = PROJECT_ROOT / "data" / "processed" / "dataset_preprocessed.csv"
df_preprocessed.to_csv(out_csv, index=False)
print(f"[ĐÃ LƯU] Tệp dữ liệu tiền xử lý: {out_csv.relative_to(PROJECT_ROOT)} ({out_csv.stat().st_size / 1024:.1f} KB)")"""))

    # Cell 13: Markdown — Section 6: Vocabulary Frequency Analysis
    cells.append(nbf.v4.new_markdown_cell("""---
## 6. Phân Tích Phân Bố Từ Khóa Sau Tiền Xử Lý (Vocabulary Analysis)

Khảo sát Top 15 từ ghép đặc trưng nhất của tin nhắn Lừa đảo (Scam) so với tin nhắn Bình thường (Normal)."""))

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
axes[0].set_title("Top 15 Từ Khóa Đặc Trưng Nhất Của Tin Nhắn Lừa Đảo", fontsize=11, fontweight="bold")
axes[0].set_xlabel("Số lần xuất hiện")
axes[0].invert_yaxis()

# Plot top normal words
df_top_normal["Tần số"].plot(kind="barh", ax=axes[1], color="#2ecc71")
axes[1].set_title("Top 15 Từ Khóa Đặc Trưng Nhất Của Tin Nhắn Bình Thường", fontsize=11, fontweight="bold")
axes[1].set_xlabel("Số lần xuất hiện")
axes[1].invert_yaxis()

plt.tight_layout()
plt.show()"""))

    # Cell 15: Markdown — Section 7: Conclusions and Phase 03 Handoff
    cells.append(nbf.v4.new_markdown_cell("""---
## 7. Kết Luận & Chuyển Giao Cho Phase 03

### Kết quả đạt được trong Phase 02 (Phiên bản nâng cao):
1. **Kiến trúc mô-đun hóa cao cấp**: Phân tách rõ ràng giữa `teencode_dictionary.py`, `text_cleaner.py`, `tokenizer.py`, `stopwords.py`, và `pipeline.py`, mỗi file đều dưới 200 dòng theo đúng quy chuẩn CS114.
2. **De-obfuscation triệt để**: Giải mã toàn diện các biến thể leet-speak (`th0ng ba0`, `kh0ng`, `d!eu k!en`, `t!en`) và tách nhãn dính (`[ĐƯỜNG_DẪN]de lay`).
3. **Thích ứng tiếng Việt có dấu và không dấu**: Tích hợp `underthesea.text_normalize` cho văn bản có dấu và cơ chế nối từ ghép `join_unaccented_compounds` cho 45.0% mẫu văn bản không dấu.
4. **Bộ 15 đặc trưng phụ đắt giá**: Tần suất các chỉ báo khẩn cấp, tai nạn cấp cứu, quyền lực nhà nước, và leet-speak ở nhóm Scam cao gấp từ 3 đến 35 lần so với nhóm Normal.
5. **Dữ liệu hoàn chỉnh sẵn sàng**: Xuất tệp `data/processed/dataset_preprocessed.csv` gồm 2.193 dòng, 24 cột, không có giá trị Null hay chuỗi rỗng.

### Bước tiếp theo (Phase 03):
- EDA chuyên sâu và trích xuất ma trận TF-IDF (N-gram 1-2).
- Phân chia tập dữ liệu Stratified Train/Test 80/20 chuẩn bị cho huấn luyện mô hình Machine Learning."""))

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
