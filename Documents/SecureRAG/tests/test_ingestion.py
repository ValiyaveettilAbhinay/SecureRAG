import pytest

from SecureRAG.services.ingestion_service import (
    DocumentIngestionError,
    extract_text,
)


def test_extract_text_from_txt():
    content = b"SecureRAG document ingestion test."

    result = extract_text("sample.txt", content)

    assert result == "SecureRAG document ingestion test."


def test_reject_unsupported_file():
    with pytest.raises(DocumentIngestionError):
        extract_text("sample.exe", b"some content")


def test_reject_empty_file():
    with pytest.raises(DocumentIngestionError):
        extract_text("empty.txt", b"")


def test_reject_txt_without_readable_text():
    with pytest.raises(DocumentIngestionError):
        extract_text("blank.txt", b"   \n  ")


def test_reject_invalid_utf8():
    with pytest.raises(DocumentIngestionError):
        extract_text("invalid.txt", b"\xff\xfe\xfa")
