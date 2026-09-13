import io

from academic_supervisor.ingestion.pdf import extract_pages_text, read_pdf


def test_extract_pages_text_returns_one_entry_per_page(make_pdf):
    pdf_bytes = make_pdf([["Page one line"], ["Page two line"]])

    pages = extract_pages_text(io.BytesIO(pdf_bytes))

    assert len(pages) == 2
    assert "Page one line" in pages[0]
    assert "Page two line" in pages[1]


def test_read_pdf_joins_pages_with_paragraph_break(make_pdf):
    pdf_bytes = make_pdf([["First page text"], ["Second page text"]])

    text = read_pdf(pdf_bytes)

    assert "First page text" in text
    assert "Second page text" in text
    assert "\n\n" in text
