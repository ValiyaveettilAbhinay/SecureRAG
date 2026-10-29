
from SecureRAG.services.chunking_service import chunk_text

text = """
SecureRAG is an enterprise knowledge AI system.

It allows users to upload documents and retrieve relevant information.

Document chunking divides large documents into smaller pieces.

Embeddings convert text into numerical vectors for semantic search.

Access control ensures users can only retrieve documents they are authorized to access.
"""

chunks = chunk_text(
    text,
    chunk_size=100,
    chunk_overlap=20,
)

print(f"\nTotal chunks: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):
    print(f"\n{'=' * 15} CHUNK {index} {'=' * 15}")
    print(chunk)
    print(f"Characters: {len(chunk)}")