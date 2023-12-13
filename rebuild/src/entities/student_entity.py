from dataclasses import dataclass


@dataclass
class StudentEntity:
    """Represent PPCIC students."""

    registration: str
    full_name: str
