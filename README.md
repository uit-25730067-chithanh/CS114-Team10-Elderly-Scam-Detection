# Vietnamese Elderly Scam Detection: Machine Learning & NLP Defense System

<p align="center">
  <img src="./docs/cover.png" alt="Vietnamese Elderly Scam Detection Cover" width="100%" style="border-radius: 8px;" />
</p>

<p align="center">
  <a href="https://www.uit.edu.vn/"><img src="https://img.shields.io/badge/University-UIT--VNU--HCM-0052cc.svg" alt="UIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python 3.10+"></a>
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Demo-Streamlit%20Cloud-FF4B4B.svg" alt="Streamlit"></a>
  <a href="https://scikit-learn.org/"><img src="https://img.shields.io/badge/Library-scikit--learn%20%7C%20XGBoost-orange.svg" alt="Scikit-Learn"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License"></a>
  <a href="README-vi.md"><img src="https://img.shields.io/badge/Language-Tiếng%20Việt-red.svg" alt="Tiếng Việt"></a>
</p>

---

## 📌 Executive Overview

This repository hosts the official open-source showcase for the **CS114 Machine Learning Final Project** at the **University of Information Technology (UIT - VNU-HCM)**.

The system addresses the rising wave of social engineering cybercrime and telecommunication fraud targeting Vietnamese senior citizens. By integrating domain-driven NLP preprocessing, dual-space feature representation (TF-IDF and 15 auxiliary cognitive/urgency signals), and benchmarked supervised classifiers, the system provides real-time fraud probability scores, psychological manipulation trap explainability (XAI via SHAP), and an accessible web application tailored for elderly users.

### Key Highlights
* **Zero Synthetic Text Policy:** Trained on a curated ground-truth corpus of **2,193 authentic Vietnamese SMS messages** (1,773 normal messages and 420 real-world fraud cases) crawled from news portals, scam reporting vaults, and citizen submissions.
* **Dual-Feature Representation:** Combines a 5,000-dimensional TF-IDF word-level matrix with 15 engineered auxiliary features capturing urgency, authority impersonation, financial trigger keywords, uppercase ratios, and suspicious URLs/phone numbers.
* **Benchmark Superiority:** Evaluated across 4 model families; **XGBoost** achieved the best overall performance with **F1-Score: 95.35%**, **Recall: 97.62%**, and **PR-AUC: 0.9969**.
* **Elderly-Centric UI Design:** Streamlit Web Demo equipped with font size scaling, high-contrast risk gauges, keyword highlight triggers, and protective action recommendations.

---

## 🏛️ System Architecture

```text
Raw SMS Text
    │
    ▼
[Text Cleaning & Normalization]
    ├── Unicode NFC Normalization
    ├── 160+ Vietnamese Teencode & Slang Expansion
    ├── PII Masking ([PHONE], [URL], [OTP], [MONEY])
    └── Word Segmentation (pyvi / underthesea)
    │
    ├───────────────────────────────────────────────┐
    ▼                                               ▼
[Lexical Space (TF-IDF)]               [Cognitive Signals (15 Aux Features)]
├── Unigrams + Bigrams (Max 5,000)      ├── Psychological Urgency Score
└── Sublinear Term Frequency Scaling    ├── Authority Impersonation Lexicon
                                        ├── Financial / Gift Trap Density
                                        └── Syntactic Signals (Caps, Punctuation)
    │                                               │
    └───────────────────────┬───────────────────────┘
                            ▼
                [Feature Fusion Pipeline]
                (Concatenation: 5,015 Dimensions)
                            │
                            ▼
                [Machine Learning Engine]
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   Naive Bayes        Random Forest          XGBoost (Champion)
  (Baseline)         (F1: 94.25%)           (F1: 95.35%)
                            │
                            ▼
             [Explainability & Inference Engine]
            ├── Calibrated Scam Probability Score
            ├── Threat Category Taxonomy (Fear, Emergency, Gift, Public Service)
            └── SHAP Top-20 Cognitive Trigger Extraction
                            │
                            ▼
              [Elderly-Optimized Streamlit UI]
```

---

## 📊 Benchmark Results

All models were evaluated on an isolated 20% holdout test set with stratified 5-fold cross-validation during tuning. Zero test data was leaked into vocabulary extraction or scaler computation.

| Model | Class Imbalance Handling | Accuracy | Precision | Recall (Scam) | F1-Score | ROC-AUC | Training Time |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Multinomial Naive Bayes** | Class Weights | 95.90% | 85.00% | 92.54% | **88.64%** | 0.9782 | < 1s |
| **Random Forest** | Balanced Subsample | 97.95% | 91.11% | **97.62%** | **94.25%** | 0.9972 | 14.8s |
| **XGBoost (Champion)** | `scale_pos_weight` | **98.41%** | **93.33%** | **97.62%** | **95.35%** | **0.9986** | 8.2s |
| **Linear SVM** | Calibrated Sigmoid | 98.18% | 92.22% | 96.43% | **94.74%** | **0.9986** | 3.5s |

*For complete confusion matrices, ROC/PR curves, and ablation test records, inspect [`reports/figures/`](reports/figures/) and [`reports/model_comparison.csv`](reports/model_comparison.csv).*

---

## 🚀 Quickstart & Local Installation

### Prerequisites
* Python 3.10 or higher
* Git

### 1. Clone Repository
```bash
git clone https://github.com/uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection.git
cd CS114-Team10-Elderly-Scam-Detection
```

### 2. Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run Streamlit Web Application
```bash
streamlit run demo/app.py
```
Open your browser at `http://localhost:8501`.

### 4. Execute Test Suite
```bash
python3 -m unittest discover tests/
```

---

## 📂 Repository Directory Layout

```text
.
├── data/
│   ├── processed/                       # Feature matrices & serialized transformers
│   │   ├── tfidf_vectorizer.pkl         # Trained TF-IDF vectorizer (5,000 features)
│   │   ├── aux_scaler.pkl               # Robust auxiliary feature scaler
│   │   └── real_world_test_thanh.csv    # Independent real-world evaluation set
│   └── raw/
│       └── dataset.csv                  # 2,193 ground-truth SMS corpus (Zero Synthetic Text)
├── demo/                                # Interactive Streamlit Web Application
│   ├── app.py                           # Main application entrypoint
│   └── components/                      # Modular UI widgets (Risk meter, advisors)
├── docs/                                # Technical specifications & system architecture
│   ├── cover.png                        # Academic project banner
│   ├── code-standards.md                # Python engineering conventions
│   └── system-architecture.md           # Pipeline specification
├── models/                              # Serialized model bundles (< 5MB)
│   ├── best_model_bundle.pkl            # Champion XGBoost pipeline package
│   ├── naive_bayes.pkl                  # Naive Bayes baseline
│   ├── random_forest.pkl                # Tuned Random Forest model
│   ├── svm_linear.pkl                   # Calibrated Linear SVM model
│   └── xgboost.pkl                      # Tuned XGBoost model
├── notebooks/                           # Step-by-step exploratory research notebooks
│   ├── 01_data_preprocessing.ipynb     # Text normalization & teencode cleaning
│   ├── 02_eda_feature_engineering.ipynb # Auxiliary features & data distributions
│   ├── 03_baseline_naive_bayes.ipynb    # Naive Bayes modeling
│   ├── 04_random_forest.ipynb           # Random Forest hyperparameter search
│   ├── 05_xgboost.ipynb                 # XGBoost training & metric optimization
│   ├── 06_svm.ipynb                     # SVM classification & calibration
│   └── 07_evaluation_xai.ipynb          # Multi-model evaluation & SHAP analysis
├── reports/                             # Benchmark evidence & visual artifacts
│   ├── figures/                         # 32 high-resolution experiment charts (@ 300 DPI)
│   ├── ablation_studies.json            # Feature contribution ablation records
│   └── model_comparison.csv             # Quantitative cross-model comparison matrix
├── slide/                               # Academic presentation slide
│   ├── [Nhom10]_Slide_ScamDetection.pdf # Presentation slide deck (22 pages PDF)
│   └── script.md                        # Defense presentation verbal script
├── src/                                 # Reusable core Python package
│   ├── preprocessing/                   # Text cleaner, tokenizer, teencode dictionary
│   ├── evaluation/                      # Metrics calculation, XAI explainers, ablation
│   ├── feature_engineering.py           # Auxiliary signals extractor
│   └── utils/                           # Data loading and helper utilities
├── tests/                               # Comprehensive unit & integration tests
├── requirements.txt                     # Pinned project dependencies
└── LICENSE                              # MIT License
```

---

## 📄 Academic Deliverables

* **Full Academic Report (PDF 32 pages):** Officially submitted to UIT Moodle LMS under course regulations. *(Retained to prevent academic plagiarism; please contact the team if you are an academic researcher requesting access).*
* **Presentation Slides (PDF 22 pages):** [`slide/[Nhom10]_Slide_ScamDetection.pdf`](slide/[Nhom10]_Slide_ScamDetection.pdf)
* **Live Demo Deployment:** [Streamlit Community Cloud](https://elderly-scam-detection.streamlit.app)

---

## 👥 Project Team & Contributors

**Institution:** University of Information Technology, VNU-HCM (UIT)  
**Course:** Machine Learning (CS114.F31.CN2.TTNT)  
**Faculty Advisor:** M.Sc. Cap Pham Dinh Thang (`thangcpd@uit.edu.vn`)  

### Team 10 Members
* **Dang Chi Thanh (Lead / Project Manager)** — Student ID: `25730067`
  * *Responsibilities:* Data architecture, Zero-Leakage Preprocessing, Feature Engineering, EDA, System Integration.
* **Bui Thi My Cam** — Student ID: `25730013`
  * *Responsibilities:* Data collection, Modeling (Naive Bayes, XGBoost, SVM), Hyperparameter Tuning, Metrics Evaluation.
* **Hoang Cao Son** — Student ID: `25730061`
  * *Responsibilities:* Data collection, Modeling (Random Forest), Streamlit Web Application Development, Elderly UX Testing.

---

## 📜 Citation

If this research, codebase, or dataset benchmark is helpful for your academic research, please cite:

```bibtex
@misc{uit_cs114_elderly_scam_detection_2026,
  author       = {Dang Chi Thanh and Bui Thi My Cam and Hoang Cao Son},
  title        = {Vietnamese Elderly Scam Detection: Machine Learning and NLP System for Psychological Manipulation Defense},
  year         = {2026},
  publisher    = {GitHub},
  journal      = {Course Project, CS114 Machine Learning, University of Information Technology, VNU-HCM},
  howpublished = {\url{https://github.com/uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection}}
}
```

---

## 📄 License

This project is released under the **[MIT License](LICENSE)**.
