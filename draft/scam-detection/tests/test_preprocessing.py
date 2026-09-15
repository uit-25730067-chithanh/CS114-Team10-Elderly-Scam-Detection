"""Comprehensive unit tests for Vietnamese text preprocessing, tokenizer, stopwords, and 14 auxiliary features."""

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
from src.preprocessing.teencode_dictionary import (
    LEET_SPEAK_PATTERNS,
    TEENCODE_DICT,
    UNACCENTED_COMPOUNDS,
)
from src.preprocessing.text_cleaner import (
    clean_text,
    deobfuscate_leetspeak,
    normalize_tone_marks,
    normalize_unicode,
    teencode_normalize,
)
from src.preprocessing.tokenizer import (
    ViTextTokenizer,
    join_unaccented_compounds,
    segment_vietnamese,
    tokenize_words,
)


class TestUnicodeAndCleaning:
    """Test suite for Unicode NFC, tone normalization, and regex text cleaning."""

    def test_unicode_normalization_nfc(self) -> None:
        """Verify decomposed Unicode (NFD) is normalized to NFC."""
        nfd_text = "tiê\u0301ng Viê\u0323t"
        nfc_text = normalize_unicode(nfd_text)
        assert unicodedata.is_normalized("NFC", nfc_text)
        assert nfc_text == "tiếng Việt"

    def test_normalize_tone_marks_modern_rule(self) -> None:
        """Verify underthesea normalizes old tone placement to modern linguistic standard."""
        old_tone = "hoà bình và khoẻ mạnh"
        modern_tone = normalize_tone_marks(old_tone)
        assert "hòa" in modern_tone
        assert "khỏe" in modern_tone

    def test_teencode_dict_size(self) -> None:
        """Verify teencode dictionary contains >= 160 entries based on corpus audit."""
        assert len(TEENCODE_DICT) >= 160

    def test_teencode_normalization(self) -> None:
        """Verify abbreviations and slang expand to formal Vietnamese."""
        raw = "ko dc ck vao stk cua mk nhe, ca se vao cuoc"
        normalized = teencode_normalize(raw)
        assert "không" in normalized
        assert "được" in normalized
        assert "chuyển khoản" in normalized
        assert "số tài khoản" in normalized
        assert "mình" in normalized
        assert "công an" in normalized

    def test_deobfuscate_leetspeak_patterns(self) -> None:
        """Verify deliberate scam leet-speak obfuscation is de-obfuscated."""
        scam_leet = "Th0ng ba0 kh0ng hop le! Bam vao de lay t!en va d!eu k!en"
        deobfuscated = deobfuscate_leetspeak(scam_leet)
        assert "thông" in deobfuscated.lower()
        assert "báo" in deobfuscated.lower()
        assert "không" in deobfuscated.lower()
        assert "tiền" in deobfuscated.lower()
        assert "điều kiện" in deobfuscated.lower()

    def test_repeated_character_deduplication(self) -> None:
        """Verify repeated character elongation is collapsed to normal form."""
        elongated = "chuyển ngay nhaaaaa, gấp lắm rồi đấyyyyy"
        cleaned = clean_text(elongated)
        assert "nhaaaaa" not in cleaned
        assert "đấyyyyy" not in cleaned

    def test_clean_text_removes_urls_phones_emails(self) -> None:
        """Verify cleaning removes raw URLs, phone numbers, and emails."""
        raw = "Bấm http://scam.vn hoặc gọi 0987123456 qua email support@gov.vn ngay!"
        cleaned = clean_text(raw)
        assert "http" not in cleaned
        assert "0987123456" not in cleaned
        assert "support@gov.vn" not in cleaned
        assert cleaned.strip() != ""

    def test_glued_masked_tags_separated(self) -> None:
        """Verify bracketed tags glued to text are properly separated and handled."""
        glued = "[ĐƯỜNG_DẪN]de lay tien"
        cleaned = clean_text(glued)
        assert "đường_dẫn" in cleaned or "link_truy_cap" in cleaned
        assert "lay" in cleaned or "lấy" in cleaned

    def test_no_over_normalization_on_ambiguous_words(self) -> None:
        """Verify ambiguous unaccented words ('cuoc', 'the', 'vay', 'ty') are not naively distorted."""
        # Case 1: 'vao cuoc' should NOT become 'vao cước'
        text_police = "ca se vao cuoc dieu tra"
        cleaned_police = clean_text(text_police)
        assert "cước" not in cleaned_police
        assert "công an" in cleaned_police

        # Case 2: '62 ty dong' should NOT become '62 cảm ơn đồng'
        text_jackpot = "trung thuong hon 62 ty dong"
        cleaned_jackpot = clean_text(text_jackpot)
        assert "cảm ơn" not in cleaned_jackpot

        # Case 3: 'co the vay' should NOT become 'co thẻ khoản vay'
        text_loan = "ban co the vay den 50 trieu"
        cleaned_loan = clean_text(text_loan)
        assert "thẻ" not in cleaned_loan
        assert "khoản vay" not in cleaned_loan

        # Case 4: Standalone 'k' should become 'không', not 'nghìn'
        text_k = "toi k biet gi het"
        cleaned_k = clean_text(text_k)
        assert "không" in cleaned_k
        assert "nghìn" not in cleaned_k



class TestTokenizerAndStopwords:
    """Test suite for Vietnamese word segmentation and stopword removal."""

    def test_segment_vietnamese_compounds(self) -> None:
        """Verify pyvi joins accented Vietnamese compound words with underscores."""
        raw = "công an yêu cầu chuyển khoản tài khoản ngân hàng"
        segmented = segment_vietnamese(raw)
        assert "công_an" in segmented
        assert "chuyển_khoản" in segmented
        assert "tài_khoản" in segmented
        assert "ngân_hàng" in segmented

    def test_unaccented_compounds_joining(self) -> None:
        """Verify unaccented compound phrases are joined to preserve semantic entities."""
        unacc_raw = "tai khoan da bi khoa, vui long den ngan hang de xac thuc"
        joined = join_unaccented_compounds(unacc_raw)
        assert "tai_khoan" in joined
        assert "ngan_hang" in joined
        assert "xac_thuc" in joined

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
        """Verify domain-specific scam indicators are strictly guarded from stopword removal."""
        scam_tokens = "công_an phong_tỏa tiền triệu tài_khoản khẩn_cấp cấp_cứu bảo_hiểm ngay_lập_tức"
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
    """Test suite for 14 auxiliary feature extraction and full preprocessing pipeline."""

    def test_extract_auxiliary_features_comprehensive(self) -> None:
        """Verify extraction of all 14 auxiliary features including masked entities."""
        sample = "CẢNH BÁO BỘ CÔNG AN: Chuyển [MONEY] vào stk gấp qua [ĐƯỜNG_DẪN]! Mã OTP [MÃ_OTP] gọi 0912345678?"
        feats = extract_auxiliary_features(sample)
        assert feats["num_urls"] >= 1
        assert feats["num_phone_numbers"] >= 1
        assert feats["num_money_mentions"] >= 1
        assert feats["has_urgent_words"] == 1
        assert feats["num_authority_words"] >= 1
        assert feats["has_otp_request"] == 1
        assert feats["num_exclamation"] == 1
        assert feats["num_question"] == 1
        assert feats["num_uppercase_words"] >= 4

    def test_emergency_and_gift_feature_flags(self) -> None:
        """Verify detection of family emergency and gift/lottery indicators."""
        emergency_text = "Cháu bị tai nạn cấp cứu ở bệnh viện Chợ Rẫy, chuyển tiền viện phí ngay!"
        gift_text = "Chúc mừng bạn trúng thưởng gói quà tri ân miễn phí nhân dịp Tết!"
        assert extract_auxiliary_features(emergency_text)["has_emergency_words"] == 1
        assert extract_auxiliary_features(gift_text)["has_gift_words"] == 1

    def test_unaccented_and_leet_flags(self) -> None:
        """Verify detection of unaccented text and leet-speak obfuscation."""
        unacc_text = "Thue bao cua quy khach sap bi khoa do chua thanh toan cuoc"
        leet_text = "Th0ng ba0 tu Co quan Cong an: ban phai nop tien kh0ng se bi bat"
        assert extract_auxiliary_features(unacc_text)["is_unaccented"] == 1
        assert extract_auxiliary_features(leet_text)["has_leet_speak"] == 1

    def test_preprocess_pipeline_end_to_end(self) -> None:
        """Verify end-to-end pipeline returns tuple of cleaned text and features dict."""
        sample = "Th0ng ba0 KHẨN CẤP: Bị phong tỏa stk 12345 tại vcb. Nộp 10 triệu đồng ngay!"
        cleaned, feats = preprocess_pipeline(sample)
        assert isinstance(cleaned, str)
        assert isinstance(feats, dict)
        assert len(cleaned) > 0
        assert feats["has_urgent_words"] == 1
        assert feats["num_money_mentions"] == 1
        assert feats["has_leet_speak"] == 1

    def test_edge_cases_empty_or_punct_only(self) -> None:
        """Verify fallback behavior on blank, whitespace, and punctuation-only strings."""
        assert preprocess_pipeline("")[0] == ""
        assert preprocess_pipeline("   ")[0] == ""
        res, feats = preprocess_pipeline("!@#$%^&*()")
        assert isinstance(res, str)
        assert isinstance(feats, dict)

    def test_dataframe_batch_preprocessing(self) -> None:
        """Verify TextPreprocessor batches DataFrame and appends 14 feature columns."""
        df = pd.DataFrame({
            "text": [
                "Công an gửi giấy triệu tập khẩn cấp",
                "Chao ban ngay moi tot lanh",
            ],
            "label": [1, 0],
        })
        processor = TextPreprocessor()
        augmented_df = processor.process_dataframe(df, text_column="text")
        assert "text_cleaned" in augmented_df.columns
        assert "num_phone_numbers" in augmented_df.columns
        assert "has_urgent_words" in augmented_df.columns
        assert "has_leet_speak" in augmented_df.columns
        assert "is_unaccented" in augmented_df.columns
        assert len(augmented_df.columns) >= 16
