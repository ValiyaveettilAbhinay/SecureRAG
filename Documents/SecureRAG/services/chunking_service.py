
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[str]:
    """
    Split extracted document text into overlapping chunks.

    Args:
        text: Extracted document text.
        chunk_size: Maximum target size of each chunk, in characters.
        chunk_overlap: Number of characters to overlap between chunks.

    Returns:
        A list of non-empty text chunks.

    Raises:
        ValueError: If the text is blank or chunk settings are invalid.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if not text.strip():
        raise ValueError("Document text cannot be empty")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
        strip_whitespace=True,
    )

    return splitter.split_text(text)