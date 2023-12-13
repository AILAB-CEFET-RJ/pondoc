from dataclasses import dataclass


@dataclass
class ResearcherEntity:
    """Represents the professors and research of EIC."""

    lattes_id: str
    full_name: str
