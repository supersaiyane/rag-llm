from typing import List


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> List[str]:

    """
    Splits a document into overlapping chunks.
    """

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size
        chunk = words[start:end]

        chunks.append(" ".join(chunk))

        start += chunk_size - chunk_overlap

    return chunks