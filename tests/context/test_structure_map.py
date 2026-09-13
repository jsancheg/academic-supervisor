from academic_supervisor.context.structure_map import build_section_structure_map


def test_build_section_structure_map_preserves_order_and_counts():
    sections = [
        {"title": "1. Introduction", "paragraphs": ["a", "b"]},
        {"title": "2. Methodology", "paragraphs": ["c"]},
        {"title": None, "paragraphs": []},
    ]

    structure_map = build_section_structure_map(sections)

    assert structure_map == [
        {"title": "1. Introduction", "paragraph_count": 2},
        {"title": "2. Methodology", "paragraph_count": 1},
        {"title": None, "paragraph_count": 0},
    ]
