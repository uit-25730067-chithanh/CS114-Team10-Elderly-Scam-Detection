"""Unit tests for Vietnamese text preprocessing, tokenizer, stopwords, and auxiliary features."""

from __future__ import annotations

import unicodedata
import pandas as pd
import pytest

from src.preprocessing.pipeline import (
    TextPreprocessor,
    extract_auxiliary_features,
    preprocess_pipeline,
)
from src.preprocessing.stopwords import (
    DOMAIN_PROTECTED_WORDS,
    EFFECTIVE_STOPWORDS,
    VIETNAMESE_STOPWORDS,
    remove_stopwords,
)
from src.preprocessing.text_cleaner import (
    TEENCODE_DICT,
    clean_text,
    normalize_unicode,
    teencode_normalize,
)
from src.preprocessing.tokenizer import (
    ViTextTokenizer,
    segment_vietnamese,
    tokenize_words,
)


class TestUnicodeAndCleaning:
    """Test suite for Unicode NFC and regex text cleaning."""

    def test_unicode_normalization_nfc(self) -> None:
        """Verify decomposed Unicode (NFD) is normalized to NFC."""
        # 'e' + combining acute accent (\u0301) vs precomposed 'é' (\u00e9)
        nfd_text = "tiê\u0301ng Viê\u0323t"
        nfc_text = normalize_unicode(nfd_text)
        assert unicodedata.is_normalized("NFC", nfc_text)
        assert nfc_text == "tiếng Việt"

    def test_teencode_normalization(self) -> None:
        """Verify common teencode words and abbreviations expand correctly."""
        raw = "ko dc ck vao stk cua mk nhe"
        expected = "không được chuyển khoản vao số tài khoản cua mình nhe"
        assert teencode_normalize(raw) == expected

    def test_teencode_dict_size(self) -> None:
        """Verify teencode dictionary contains >= 30 entries as requested in plan."""
        assert len(TEENCODE_DICT) >= 30

    def test_clean_text_removes_urls_phones_emails(self) -> None:
        """Verify cleaning removes URLs, phone numbers, emails, and punctuation."""
        raw = "Bấm http://scam.vn hoặc liên hệ 0987123456 qua email support@gov.vn ngay!!!"
        cleaned = clean_text(raw)
        assert "http" not in cleaned
        assert "scam.vn" not in cleaned
        assert "0987123456" not in cleaned
        assert "support@gov.vn" not in cleaned
        assert "!" not in cleaned
        assert cleaned.strip() != ""


class TestTokenizerAndStopwords:
    """Test suite for Vietnamese word segmentation and stopword removal."""

    def test_segment_vietnamese_compounds(self) -> None:
        """Verify pyvi joins Vietnamese compound words with underscores."""
        raw = "công an yêu cầu chuyển khoản tài khoản ngân hàng"
        segmented = segment_vietnamese(raw)
        assert "công_an" in segmented
        assert "chuyển_khoản" in segmented
        assert "tài_khoản" in segmented
        assert "ngân_hàng" in segmented

    def test_tokenizer_class_and_word_list(self) -> None:
        """Verify ViTextTokenizer callable class and token listing."""
        tokenizer = ViTextTokenizer()
        segmented = tokenizer("Bộ Công an Việt Nam")
        words = tokenize_words("Bộ Công an Việt Nam")
        assert "công_an" in segmented.lower()
        assert len(words) >= 3

    def test_stopwords_list_size(self) -> None:
        """Verify Vietnamese stopwords list contains >= 50 entries."""
        assert len(VIETNAMESE_STOPWORDS) >= 50
        assert len(EFFECTIVE_STOPWORDS) >= 50

    def test_scam_domain_keywords_preserved(self) -> None:
        """Verify domain-specific scam indicators are never filtered as stopwords."""
        scam_tokens = "công_an phong_tỏa tiền triệu tài_khoản khẩn_cấp cấp_cứu"
        filtered = remove_stopwords(scam_tokens)
        for token in scam_tokens.split():
            assert token in filtered

    def test_grammatical_stopwords_removed(self) -> None:
        """Verify purely grammatical conjunctions and prepositions are filtered."""
        text = "và là của được cho với trong này công_an"
        filtered = remove_stopwords(text)
        assert "công_an" in filtered
        assert "và" not in filtered
        assert "của" not in filtered


class TestAuxiliaryFeaturesAndPipeline:
    """Test suite for auxiliary feature extraction and full preprocessing pipeline."""

    def test_extract_auxiliary_features(self) -> None:
        """Verify accurate feature extraction before text cleaning."""
        sample = "CẢNH BÁO KHẨN: Công an phạt 20 triệu đồng! Xem www.vn.com hoặc gọi 0912345678?"
        feats = extract_auxiliary_features(sample)
        assert feats["num_phone_numbers"] == 1
        assert feats["num_urls"] == 1
        assert feats["num_money_mentions"] == 1
        assert feats["has_urgent_words"] == 1
        assert feats["num_authority_words"] == 1
        assert feats["num_exclamation"] == 1
        assert feats["num_question"] == 1
        assert feats["num_uppercase_words"] >= 3

    def test_preprocess_pipeline_end_to_end(self) -> None:
        """Verify end-to-end pipeline returns tuple of cleaned text and features dict."""
        sample = "KHẨN CẤP: Bị phong tỏa stk 12345 tại vcb. Nộp 10 triệu đồng ngay!"
        cleaned, feats = preprocess_pipeline(sample)
        assert isinstance(cleaned, str)
        assert isinstance(feats, dict)
        assert len(cleaned) > 0
        assert feats["has_urgent_words"] == 1
        assert feats["num_money_mentions"] == 1

    def test_edge_cases_empty_or_punct_only(self) -> None:
        """Verify fallback behavior on blank, whitespace, and punctuation-only strings."""
        assert preprocess_pipeline("")[0] == ""
        assert preprocess_pipeline("   ")[0] == ""
        # Punctuation-only string should not crash
        res, feats = preprocess_pipeline("!@#$%^&*()")
        assert isinstance(res, str)
        assert isinstance(feats, dict)

    def test_dataframe_batch_preprocessing(self) -> None:
        """Verify TextPreprocessor batches DataFrame and appends feature columns."""
        df = pd.DataFrame({
            "text": [
                "Công an gửi giấy triệu tập khẩn cấp",
                "Chào bạn ngày mới tốt lành",
            ],
            "label": [1, 0],
        })
        processor = TextPreprocessor()
        augmented_df = processor.process_dataframe(df, text_column="text")
        assert "text_cleaned" in augmented_df.columns
        assert "num_phone_numbers" in augmented_df.columns
        assert "has_urgent_words" in augmented_df.columns
        assert augmented_df["text_cleaned"].iloc[0] != ""
        assert augmented_df["text_cleaned"].iloc[1] != ""
