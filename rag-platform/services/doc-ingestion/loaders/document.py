from dataclasses import dataclass
from typing import Dict


@dataclass
class Document:
    text: str
    metadata: Dict