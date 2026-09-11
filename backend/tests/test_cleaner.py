from app.documents.cleaner import clean_text, repair_text_encoding


def test_repair_text_encoding_replaces_private_bullet_glyph():
    assert repair_text_encoding("\uf0d8 Nutrition") == "\u2022 Nutrition"


def test_repair_text_encoding_fixes_mojibake_bullet():
    assert repair_text_encoding("\u00e2\u20ac\u00a2 Nutrition") == "\u2022 Nutrition"


def test_clean_text_normalises_wrapped_lines_and_whitespace():
    assert clean_text("Living things\nneed water.\n\n  They grow.  ") == (
        "Living things need water.\n\nThey grow."
    )
