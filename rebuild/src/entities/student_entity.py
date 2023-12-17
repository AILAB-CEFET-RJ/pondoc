from dataclasses import dataclass
import re
from typing import Optional
from helpers import create_authorship_regex


@dataclass
class StudentEntity:
    """Represent PPCIC students."""

    registration: str
    full_name: str
    authorship_regex: Optional[re.Pattern] = None

    def __post_init__(self):
        self.authorship_regex = create_authorship_regex(self.full_name)
