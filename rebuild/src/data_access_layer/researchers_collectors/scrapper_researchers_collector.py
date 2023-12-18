import re
from typing import Dict, List, Set, Tuple
from urllib.request import urlopen

import bs4
from unidecode import unidecode

from .interface_researchers_collector import IReserchersCollector
from entities import ResearcherEntity


class ScrapperResearchersCollector(IReserchersCollector):
    """Gets EIC reaserchers scrapping the eic web site.
    
    https://eic.cefet-rj.br/lattes/ppcic-YYYY/membros.html
    """

    def collect(self, years: List[int]) -> Tuple[Dict[str, ResearcherEntity], Dict[int, Set[str]]]:
        researchers_dict = {}
        year_researchers_dict = {year: set() for year in years}

        for year in years:
            url = f'https://eic.cefet-rj.br/lattes/ppcic-{year}/membros.html'
            raw_html = urlopen(url).read().decode('utf-8')
            soup = bs4.BeautifulSoup(raw_html, 'html.parser')
            raw_researchers = soup.find_all('a', href=re.compile('membro-\d+\.html'))
            researchers =  [self._normalize_researcher(rrr) for rrr in raw_researchers]

            for researcher in researchers:
                year_researchers_dict[year].add(researcher.lattes_id)
                
                if researcher.lattes_id not in researchers_dict:
                    researchers_dict[researcher.lattes_id] = researcher
            
        return researchers_dict, year_researchers_dict

    @staticmethod
    def _normalize_researcher(raw_researcher: bs4.element.Tag) -> ResearcherEntity:
        lattes_id = raw_researcher.attrs.get('href').removeprefix('membro-').removesuffix('.html')
        name = raw_researcher.text.strip().upper()
        return ResearcherEntity(lattes_id = lattes_id, full_name = unidecode(name))
