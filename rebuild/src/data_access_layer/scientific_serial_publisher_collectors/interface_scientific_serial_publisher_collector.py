from abc import ABC, abstractmethod
from typing import Dict, List

from entities import ScientificSerialPublisherEntity
from entities.types import Issn


class IScientificSerialPublisherCollector(ABC):
    """Public interface for qualis collectors."""

    @abstractmethod
    def collect(self, years: List[int]) -> Dict[Issn, ScientificSerialPublisherEntity]:
        """Returns a dictionary that maps ISSN to ScientificSerialPublisher."""
        raise NotImplementedError
