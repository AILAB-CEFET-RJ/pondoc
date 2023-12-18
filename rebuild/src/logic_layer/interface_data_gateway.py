from abc import ABC, abstractmethod
from typing import Dict, List, TypedDict

from entities import PublishedWorkEntity
from entities import ResearcherEntity
from entities import StudentEntity
from entities.types import Issn
from entities.enums import QualisEnum


class YearResume(TypedDict):
    published_works: List[PublishedWorkEntity]
    qualis: Dict[Issn, QualisEnum]
    researchers: Dict[str, ResearcherEntity]
    students: Dict[str, StudentEntity]

class IDataGateway(ABC):
    """Interface which the logic layer queries data."""

    @abstractmethod
    def get_year_works_dict(self, years: List[int]) -> Dict[int, YearResume]:
        """Returns a dictionary which maps a year (YYYY) to their published works, qualis, 
        reaseachers and students."""
        raise NotImplementedError
