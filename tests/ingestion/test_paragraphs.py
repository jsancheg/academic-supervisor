import io

from academic_supervisor.ingestion.paragraphs import split_paragraphs
from academic_supervisor.ingestion.pdf import read_pdf
from academic_supervisor.ingestion.text import read_text


def test_split_paragraphs_drops_blank_entries():
    text = "First paragraph.\n\n\n\nSecond paragraph.\n\n"
    assert split_paragraphs(text) == ["First paragraph.", "Second paragraph."]


def test_split_paragraphs_on_plain_text_ingestion(tmp_path):
    file_path = tmp_path / "doc.txt"
    file_path.write_text("Para one.\n\nPara two.", encoding="utf-8")

    text = read_text(file_path)

    assert split_paragraphs(text) == ["Para one.", "Para two."]


def test_split_paragraphs_on_pdf_ingestion(make_pdf):
    pdf_bytes = make_pdf([["First page paragraph"], ["Second page paragraph"]])

    text = read_pdf(io.BytesIO(pdf_bytes))

    paragraphs = split_paragraphs(text)
    assert paragraphs == ["First page paragraph", "Second page paragraph"]
