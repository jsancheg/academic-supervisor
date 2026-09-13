from academic_supervisor.context.terminology import build_terminology_map


def test_build_terminology_map_flags_mixed_variant_usage():
    paragraphs = [
        "Please contact us by email.",
        "Send an e-mail to confirm.",
    ]

    terminology_map = build_terminology_map(paragraphs)

    assert terminology_map["email"] == {"email": [0], "e-mail": [1]}


def test_build_terminology_map_does_not_flag_consistent_usage():
    paragraphs = [
        "The dataset was cleaned first.",
        "We then split the dataset into train/test.",
    ]

    terminology_map = build_terminology_map(paragraphs)

    assert "dataset" not in terminology_map


def test_build_terminology_map_returns_empty_when_no_variants_present():
    paragraphs = ["This paragraph mentions nothing relevant."]

    assert build_terminology_map(paragraphs) == {}
