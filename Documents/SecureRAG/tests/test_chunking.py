import pytest

from SecureRAG.services.chunking_service import chunk_text


def test_chunk_text_returns_chunks():
    text = (
        "Eligibility requirements are important.\n\n"
        "Students must have a minimum CGPA of 7.5.\n\n"
        "Students must not have active backlogs."
    )

    chunks = chunk_text(
        text,
        chunk_size=60,
        chunk_overlap=10,
    )

    assert len(chunks) >= 1
    assert all(isinstance(chunk, str) for chunk in chunks)
    assert all(chunk.strip() for chunk in chunks)


def test_chunk_text_preserves_content():
    text = (
        "Minimum CGPA is 7.5.\n\n"
        "Active backlogs are not allowed."
    )

    chunks = chunk_text(
        text,
        chunk_size=100,
        chunk_overlap=10,
    )

    combined_text = " ".join(chunks)

    assert "Minimum CGPA is 7.5." in combined_text
    assert "Active backlogs are not allowed." in combined_text


def test_chunk_text_rejects_blank_input():
    with pytest.raises(ValueError):
        chunk_text("   ")


def test_chunk_text_rejects_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_text(
            "Some document text.",
            chunk_size=100,
            chunk_overlap=100,
        )


def test_chunk_text_rejects_zero_chunk_size():
    with pytest.raises(ValueError):
        chunk_text(
            "Some document text.",
            chunk_size=0,
            chunk_overlap=0,
        )

