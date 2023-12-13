from abc import ABC, abstractmethod
from typing import Dict, List
from uuid import UUID

from entities import PublishedWorkEntity


class IPublishedWorksCollector(ABC):
    """Public interface for published works collectors."""

    @abstractmethod
    def collect(self, years: List[int]) -> Dict[UUID, PublishedWorkEntity]:
        """Extracts published works data from an external source."""
        raise NotImplementedError
