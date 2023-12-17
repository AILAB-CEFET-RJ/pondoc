from abc import ABC, abstractmethod
from typing import Dict, List, Set, Tuple

from entities.researcher_entity import ResearcherEntity


class IReserchersCollector(ABC):
    """Public interface for reserchers collectors."""

    @abstractmethod
    def collect(self, years: List[int]) -> Tuple[Dict[str, ResearcherEntity], Dict[int, Set[str]]]:
        """Returns a dictionary that maps a researcher primary key to a resercher and another dictionary
        that maps year to a set of researcher primary keys."""
        raise NotImplementedError
