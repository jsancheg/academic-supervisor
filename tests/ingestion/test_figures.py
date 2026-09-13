from academic_supervisor.ingestion.figures import detect_figures_tables


def test_detect_figures_tables_finds_figure_and_table(make_pdf):
    pdf_bytes = make_pdf(
        [
            ["Some intro text", "Figure 1: A chart showing results"],
            ["Table 2 - Summary of values"],
        ]
    )

    entries = detect_figures_tables(pdf_bytes)

    assert len(entries) == 2

    figure = next(e for e in entries if e["type"] == "figure")
    assert figure["number"] == 1
    assert figure["caption"] == "A chart showing results"
    assert figure["page"] == 1

    table = next(e for e in entries if e["type"] == "table")
    assert table["number"] == 2
    assert table["caption"] == "Summary of values"
    assert table["page"] == 2


def test_detect_figures_tables_returns_empty_when_none_present(make_pdf):
    pdf_bytes = make_pdf([["Just a plain paragraph with no captions."]])

    assert detect_figures_tables(pdf_bytes) == []
