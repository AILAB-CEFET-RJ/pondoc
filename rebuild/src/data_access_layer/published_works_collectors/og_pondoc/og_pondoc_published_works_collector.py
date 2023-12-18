import re
import uuid
from typing import Dict, List

from unidecode import unidecode

from entities import PublishedWorkEntity
from entities.types import Issn
from ..interface_published_works_collector import IPublishedWorksCollector
from .reader import read_publications
from .analyser import parsePublication


class OgPondocPublishedWorksCollector(IPublishedWorksCollector):
    """Uses the original pondoc source to get published works from
    https://eic.cefet-rj.br/lattes/ppcic-{ano}/..."""

    def collect(self, years: List[int]) -> Dict[int, List[PublishedWorkEntity]]:
        years.sort()
        result = {year: [] for year in years}
        
        infosp, _, infosc = read_publications(years[0], years[-1])

        for year in years:
            for citation in infosp[year]:
                (
                    authors,
                    publication_title,
                    other_publication_details,
                ) = parsePublication(citation)
                paper = self._create_published_work_from_tuple(
                    publication_title, authors, year, other_publication_details
                )
                result[year].append(paper)

            for citation in infosc[year]:
                (
                    authors,
                    publication_title,
                    other_publication_details,
                ) = parsePublication(citation, False)
                paper = self._create_published_work_from_tuple(
                    publication_title, authors, year, other_publication_details
                )
                result[year].append(paper)

        return result

    @staticmethod
    def _create_published_work_from_tuple(
        title: str, authors: List[List[str]], year: int, other_details: List[str]
    ) -> PublishedWorkEntity:
        def get_issn(details: List[str]) -> Issn:
            result = None

            for detail in details:
                try:
                    result = Issn(detail)
                    break
                except ValueError:
                    pass

            return result

        def normalize_authors(author_refs: List[List[str]]) -> List[str]:
            result = []
            pattern = r"\.{2,}"
            for ref in author_refs:
                cleaned_strs = map(
                    lambda x: re.sub(pattern, ".", x.strip().upper()) + " ",
                    reversed(ref),
                )
                result.append(unidecode("".join(cleaned_strs).strip()))
            return result

        issn = get_issn(other_details)
        normalized_authors = normalize_authors(authors)
        return PublishedWorkEntity(
            id=uuid.uuid4(),
            title=title,
            year=year,
            publisher_issn=issn,
            authors=normalized_authors,
        )
