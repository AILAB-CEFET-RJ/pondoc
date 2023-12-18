from dataclasses import dataclass
from typing import List


@dataclass
class EicRelationshipEntity:
    """Represents which students and researches are related EIC in specific year."""

    year: int
    students: List[str]
    researchers: List[str]
