import nltk
from typing import List

# Ensure punkt tokenizer exists
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")


class SemanticChunker:

    def __init__(self, chunk_size: int = 500, overlap: int = 0):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        """
        Splits text by sentence boundaries while respecting chunk size.
        """

        sentences = nltk.sent_tokenize(text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:

            if len(current_chunk) + len(sentence) < self.chunk_size:
                current_chunk += " " + sentence

            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks