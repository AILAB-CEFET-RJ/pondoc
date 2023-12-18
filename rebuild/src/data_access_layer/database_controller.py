from typing import Dict, List
from logic_layer import IDataGateway, YearResume


class DatabaseController(IDataGateway):
    """Implements the data access of the logic layer."""

    def get_year_works_dict(self, years: List[int]) -> Dict[int, YearResume]:
        # Check if the database has the data
        # If it has, query them
        # Else, use a data collector for each missing data, save it in the database and return
        return {}
