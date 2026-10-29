from fastapi import APIRouter, File, HTTPException, UploadFile

from SecureRAG.schemas.document import (
    DocumentIngestionResponse,
    DocumentChunk
)
from SecureRAG.services.ingestion_service import (
    DocumentIngestionError,
    extract_text,
)
from SecureRAG.services.chunking_service import chunk_text

router = APIRouter(prefix="/api/documents", tags=["Documents"])

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("/ingest", response_model=DocumentIngestionResponse)
async def ingest_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File exceeds the 5 MB size limit.",
        )

    try:
        text = extract_text(file.filename, content)

        chunks = chunk_text(
            text,
            chunk_size=1000,
            chunk_overlap=150,
        )

    except DocumentIngestionError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return DocumentIngestionResponse(
        filename=file.filename,
        file_type="." + file.filename.rsplit(".", 1)[-1].lower(),
        character_count=len(text),
        text=text,
        total_chunks=len(chunks),
        chunks=[
            DocumentChunk(
                chunk_index=index,
                text=chunk,
                character_count=len(chunk),
            )
            for index, chunk in enumerate(chunks)
        ],
    )
