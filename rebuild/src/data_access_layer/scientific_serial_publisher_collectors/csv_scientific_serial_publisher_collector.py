from typing import Dict, List
import pandas

from .interface_scientific_serial_publisher_collector import IScientificSerialPublisherCollector
from entities import ScientificSerialPublisherEntity
from entities.types import Issn
from entities.enums import QualisEnum


class CsvScientificSerialPublisherCollector(IScientificSerialPublisherCollector):
    """Gets ScientificSerialPublisher data from CSV files."""

    def collect(self, years: List[int]) -> Dict[Issn, ScientificSerialPublisherEntity]:
        ssp_dict = {}

        for year in years:
            qualis_df = pandas.read_csv(f'./static_data/qualis/qualis-2022.csv')
            # qualis_df = pandas.read_csv(f'./static_data/qualis/qualis-{year}.csv')

            for scientific_serial_publisher_dict in qualis_df.to_dict('records'):
                ssp = self._create_ssp_from_dict(scientific_serial_publisher_dict)
                ssp_dict[ssp.issn] = ssp


        return ssp_dict

    @staticmethod
    def _create_ssp_from_dict(scientific_serial_publisher_dict: Dict) -> ScientificSerialPublisherEntity:

        def _str_to_qualis_enum(qualis_str: str) -> QualisEnum:
            result = None
            try:
                result = QualisEnum(qualis_str.upper())
            except ValueError:
                result = QualisEnum.NOT_CLASSIFIED
            return result

        return ScientificSerialPublisherEntity(
            issn=scientific_serial_publisher_dict['ISSN'],
            name=scientific_serial_publisher_dict['Nome'],
            qualis=_str_to_qualis_enum(scientific_serial_publisher_dict['Qualis']))
