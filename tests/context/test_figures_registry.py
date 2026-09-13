from academic_supervisor.context.figures_registry import build_figure_table_registry


def test_registry_marks_caption_with_matching_reference():
    captions = [{"type": "figure", "number": 1, "caption": "A chart", "page": 1}]
    paragraphs = ["See Figure 1 for details."]

    registry = build_figure_table_registry(paragraphs, captions)

    assert registry == [
        {
            "type": "figure",
            "number": 1,
            "caption": "A chart",
            "page": 1,
            "has_caption": True,
            "referenced_in_paragraphs": [0],
        }
    ]


def test_registry_marks_caption_with_no_reference():
    captions = [{"type": "table", "number": 2, "caption": "Summary", "page": 3}]
    paragraphs = ["No mention of it here."]

    registry = build_figure_table_registry(paragraphs, captions)

    assert registry == [
        {
            "type": "table",
            "number": 2,
            "caption": "Summary",
            "page": 3,
            "has_caption": True,
            "referenced_in_paragraphs": [],
        }
    ]


def test_registry_marks_reference_with_no_matching_caption():
    paragraphs = ["As shown in Figure 3, the trend is clear."]

    registry = build_figure_table_registry(paragraphs, [])

    assert registry == [
        {
            "type": "figure",
            "number": 3,
            "caption": None,
            "page": None,
            "has_caption": False,
            "referenced_in_paragraphs": [0],
        }
    ]
