from io import BytesIO
from pathlib import Path

from pypdf import PdfReader
from SecureRAG.services.chunking_service import chunk_text


ALLOWED_EXTENSIONS = {".pdf", ".txt"}


class DocumentIngestionError(Exception):
    """Raised when a document cannot be ingested."""


def validate_file(filename: str) -> str:
    """Validate the filename and return its extension."""

    if not filename or not filename.strip():
        raise DocumentIngestionError("Filename is required.")

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise DocumentIngestionError(
            "Unsupported file type. Upload a PDF or TXT file."
        )

    return extension


def extract_text(filename: str, content: bytes) -> str:
    """Extract text from PDF or TXT document bytes."""

    extension = validate_file(filename)

    if not content:
        raise DocumentIngestionError("Uploaded file is empty.")

    try:
        if extension == ".txt":
            text = content.decode("utf-8-sig")

        elif extension == ".pdf":
            reader = PdfReader(BytesIO(content))

            if reader.is_encrypted:
                raise DocumentIngestionError(
                    "Encrypted PDFs are not supported."
                )

            extracted_pages = []

            for page in reader.pages:
                extracted_pages.append(page.extract_text() or "")

            text = "\n".join(extracted_pages)

    except DocumentIngestionError:
        raise

    except Exception as exc:
        raise DocumentIngestionError(
            "Unable to read the uploaded document."
        ) from exc

    if not text.strip():
        raise DocumentIngestionError(
            "No readable text found in the document."
        )

    return text.strip()

def ingest_document(filename: str, content: bytes) -> dict:
    text = extract_text(filename, content)

    chunks = chunk_text(
        text,
        chunk_size=1000,
        chunk_overlap=150,
    )

    return {
        "filename": filename,
        "total_characters": len(text),
        "total_chunks": len(chunks),
        "chunks": [
            {
                "chunk_index": index,
                "text": chunk,
            }
            for index, chunk in enumerate(chunks)
        ],
    }

