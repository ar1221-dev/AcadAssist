from pathlib import Path
import pytest

from app.services.processors import (
    DOCXProcessor,
    DocumentProcessingError,
    PDFProcessor,
    PPTProcessor,
    TXTProcessor,
    get_processor_for_extension,
)

SAMPLE_DIR = Path("sample_data")


def test_pdf_extraction():
    processor = get_processor_for_extension("pdf")
    assert isinstance(processor, PDFProcessor)

    pdf_path = SAMPLE_DIR / "trees.pdf"
    assert pdf_path.is_file()

    result = processor.extract(pdf_path)
    assert result.page_count == 2
    assert result.total_chars > 50
    assert len(result.sections) == 2
    assert "Binary Search Trees" in result.sections[0]["content"]
    assert "BST Operations" in result.sections[1]["content"]


def test_pptx_extraction():
    processor = get_processor_for_extension("pptx")
    assert isinstance(processor, PPTProcessor)

    pptx_path = SAMPLE_DIR / "networks.pptx"
    assert pptx_path.is_file()

    result = processor.extract(pptx_path)
    assert result.slide_count == 2
    assert len(result.sections) == 2
    assert "OSI Model" in result.sections[0]["content"]
    assert "TCP" in result.sections[1]["content"]


def test_legacy_ppt_extraction():
    processor = get_processor_for_extension("ppt")
    assert isinstance(processor, PPTProcessor)

    ppt_path = SAMPLE_DIR / "os_scheduling.ppt"
    assert ppt_path.is_file()

    result = processor.extract(ppt_path)
    assert result.slide_count is not None
    assert "Operating Systems" in result.sections[0]["content"]


def test_docx_extraction():
    processor = get_processor_for_extension("docx")
    assert isinstance(processor, DOCXProcessor)

    docx_path = SAMPLE_DIR / "normalization.docx"
    assert docx_path.is_file()

    result = processor.extract(docx_path)
    assert len(result.sections) >= 2
    all_text = " ".join(s["content"] for s in result.sections)
    assert "Normalization" in all_text
    assert "1NF" in all_text
    assert "2NF" in all_text
    assert "Atomic attributes" in all_text  # Table content check


def test_legacy_doc_extraction():
    processor = get_processor_for_extension("doc")
    assert isinstance(processor, DOCXProcessor)

    doc_path = SAMPLE_DIR / "software_eng.doc"
    assert doc_path.is_file()

    result = processor.extract(doc_path)
    assert len(result.sections) >= 1
    assert "Agile Methodologies" in result.sections[0]["content"]


def test_txt_extraction():
    processor = get_processor_for_extension("txt")
    assert isinstance(processor, TXTProcessor)

    txt_path = SAMPLE_DIR / "linear_algebra.txt"
    assert txt_path.is_file()

    result = processor.extract(txt_path)
    assert len(result.sections) >= 2
    all_text = " ".join(s["content"] for s in result.sections)
    assert "Linear Algebra" in all_text
    assert "Vector Spaces" in all_text
    assert "Eigenvalues" in all_text


def test_corrupted_file_handling(tmp_path):
    corrupted_pdf = tmp_path / "broken.pdf"
    corrupted_pdf.write_bytes(b"This is not a real PDF file at all.")

    processor = get_processor_for_extension("pdf")
    with pytest.raises(DocumentProcessingError):
        processor.extract(corrupted_pdf)
