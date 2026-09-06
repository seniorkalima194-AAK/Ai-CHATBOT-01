from app.documents.cleaner import clean_text, repair_text_encoding


def test_repair_text_encoding_fixes_legacy_pdf_mojibake():
    assert repair_text_encoding("The â€œcellâ€ is important.") == "The “cell” is important."


def test_repair_text_encoding_replaces_private_bullet_glyph():
    assert repair_text_encoding("ïƒ˜ Nutrition") == "• Nutrition"


def test_clean_text_applies_encoding_repair_before_normalising_whitespace():
    assert clean_text("â€œLiving thingsâ€\nneed water.") == "“Living things” need water."
