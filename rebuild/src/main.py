from pprint import pprint
from data_access_layer.published_works_collectors import OgPondocPublishedWorksCollector
from data_access_layer.researchers_collectors import ScrapperResearchersCollector
from data_access_layer.scientific_serial_publisher_collectors import CsvScientificSerialPublisherCollector
from data_access_layer.students_collectors import CsvStudentsCollector


YEAR = 2022

# Data extractors
students, year_students_dict = CsvStudentsCollector().collect([YEAR])
pprint((students))

issn_ssp_dict = CsvScientificSerialPublisherCollector().collect([YEAR])
# pprint(issn_ssp_dict)

researchers, year_researchers_dict = ScrapperResearchersCollector().collect([YEAR])
pprint((researchers, {k: len(v) for k,v in year_researchers_dict.items()}))
# pprint(researchers['5882024148867913'])

# year_published_works_dict = OgPondocPublishedWorksCollector().collect([YEAR])
# pprint(year_published_works_dict)
