from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from .types import Issn


@dataclass
class PublishedWorkEntity:
    """Represents a published scientific work."""

    id: UUID
    title: str
    year: int
    publisher_issn: Optional[Issn]
    authors: List[str]
