from enum import Enum


class QualisEnum(Enum):
    """Represents each qualis classification of Scientific Serial Publishers."""

    __order__ = 'A1 A2 A3 A4 A5 B1 B2 B3 B4 B5 C NOT_CLASSIFIED'

    A1 = 'A1'
    A2 = 'A2'
    A3 = 'A3'
    A4 = 'A4'
    A5 = 'A5'
    B1 = 'B1'
    B2 = 'B2'
    B3 = 'B3'
    B4 = 'B4'
    B5 = 'B5'
    C = 'C'
    NOT_CLASSIFIED = 'NC'
