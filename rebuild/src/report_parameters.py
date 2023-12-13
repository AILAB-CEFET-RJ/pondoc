import datetime
from typing import Dict, List, Optional


class ReportParameters:
    """Parameters used to build a report."""

    def __init__(self, start_date: str, end_date: str, score_weights: Optional[List[float]]) -> None:
        self.start_date = datetime.datetime.fromisoformat(start_date)
        self.end_date = datetime.datetime.fromisoformat(end_date)
        self.score_weights = score_weights

    @staticmethod
    def validate_parameters(params: Dict[str, str]) -> None:
        return None
