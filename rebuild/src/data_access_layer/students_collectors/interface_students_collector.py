from abc import ABC, abstractmethod
from typing import Dict, List, Set, Tuple

from entities.student_entity import StudentEntity


class IStudentsCollector(ABC):
    """Public interface for students collectors."""

    @abstractmethod
    def collect(self, years: List[int]) -> Tuple[Dict[str, StudentEntity], Dict[int, Set[str]]]:
        """Returns a dictionary that maps a student primary key to a student and another dictionary
        that maps year to a set of student primary key."""
        raise NotImplementedError
