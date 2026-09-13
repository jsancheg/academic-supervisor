import pymupdf
import pytest


@pytest.fixture
def make_pdf():
    def _make(pages: list[list[str]]) -> bytes:
        doc = pymupdf.open()
        for lines in pages:
            page = doc.new_page()
            y = 72
            for line in lines:
                page.insert_text((72, y), line, fontsize=11)
                y += 16
        pdf_bytes = doc.tobytes()
        doc.close()
        return pdf_bytes

    return _make
