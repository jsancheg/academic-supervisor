import io

from academic_supervisor.ingestion.text import normalize_whitespace, read_text


def test_normalize_whitespace_converts_crlf_and_cr():
    assert normalize_whitespace("a\r\nb\rc") == "a\nb\nc"


def test_normalize_whitespace_collapses_excess_blank_lines():
    text = "para one\n\n\n\n\npara two"
    assert normalize_whitespace(text) == "para one\n\npara two"


def test_normalize_whitespace_strips_trailing_line_whitespace():
    text = "line one   \nline two\t\t"
    assert normalize_whitespace(text) == "line one\nline two"


def test_read_text_from_path(tmp_path):
    file_path = tmp_path / "doc.txt"
    file_path.write_text("hello\r\nworld", encoding="utf-8")

    assert read_text(file_path) == "hello\nworld"


def test_read_text_falls_back_to_latin1_on_bad_utf8():
    raw = "café".encode("latin-1")
    assert read_text(io.BytesIO(raw)) == "café"
