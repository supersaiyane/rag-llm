import os
import glob
from pathlib import Path
from typing import List

from .document import Document


class MarkdownLoader:

    def __init__(self, docs_path: str):
        self.docs_path = docs_path

    def load(self) -> List[Document]:

        documents = []

        md_files = glob.glob(
            os.path.join(self.docs_path, "**/*.md"),
            recursive=True
        )

        for file_path in md_files:

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            metadata = self._extract_metadata(file_path)

            documents.append(
                Document(
                    text=content,
                    metadata=metadata
                )
            )

        print(f"Loaded {len(documents)} markdown documents")

        return documents


    def _extract_metadata(self, file_path: str):

        filename = Path(file_path).name.lower()

        service = "general"
        doc_type = "documentation"

        if "redis" in filename:
            service = "redis"

        if "kafka" in filename:
            service = "kafka"

        if "runbook" in filename:
            doc_type = "runbook"

        return {
            "source": file_path,
            "service": service,
            "type": doc_type
        }