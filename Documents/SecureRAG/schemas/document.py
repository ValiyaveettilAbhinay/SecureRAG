from pydantic import BaseModel

class DocumentChunk(BaseModel):
    chunk_index: int
    text: str
    character_count: int

class DocumentIngestionResponse(BaseModel):
    filename: str
    file_type: str
    character_count: int
    text: str
    total_chunks: int
    chunks: list[DocumentChunk]
