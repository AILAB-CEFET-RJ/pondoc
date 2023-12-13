from dataclasses import dataclass

from .enums import QualisEnum
from .types import Issn


@dataclass
class ScientificSerialPublisherEntity:
    """Represents a unique scientific publisher, such as journals, magazines, conferences etc."""

    issn: Issn
    name: str
    qualis: QualisEnum
