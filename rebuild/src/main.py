from pprint import pprint
from typing import List, TypedDict
from data_access_layer.published_works_collectors import OgPondocPublishedWorksCollector
from data_access_layer.researchers_collectors import ScrapperResearchersCollector
from data_access_layer.scientific_serial_publisher_collectors import CsvScientificSerialPublisherCollector
from data_access_layer.students_collectors import CsvStudentsCollector
from entities import ResearcherEntity
from entities import StudentEntity


YEARS = [2022]

# Data extractors
students, year_students_dict = CsvStudentsCollector().collect(YEARS)
year_students_dict = {k: [students[x] for x in v] for k,v in year_students_dict.items()}
# pprint(students)

issn_ssp_dict = CsvScientificSerialPublisherCollector().collect(YEARS)
# pprint(issn_ssp_dict)

researchers, year_researchers_dict = ScrapperResearchersCollector().collect(YEARS)
year_researchers_dict = {k: [researchers[x] for x in v] for k,v in year_researchers_dict.items()}
# pprint((researchers, {k: len(v) for k,v in year_researchers_dict.items()}))
# pprint(researchers['5882024148867913'].authorship_regex.match('D. N. BRANDAO'))
# pprint(researchers['5882024148867913'].authorship_regex.match('DIEGO. BRANDAO'))


year_published_works_dict = OgPondocPublishedWorksCollector().collect(YEARS)
# pprint(year_published_works_dict)

class Record(TypedDict):
    Ano: str
    Numero: int
    Artigo: str
    Fórum: str
    Qualis: str
    Discente: List[StudentEntity]
    Docentes: List[ResearcherEntity]

year_to_records_dict = {}
for year in YEARS:
    sub_result = []
    students = year_students_dict[year]
    researchers = year_researchers_dict[year]

    for publication in year_published_works_dict[year]:
        numero = len(sub_result) + 1
        artigo = publication.title
        forum = ''
        qualis = ''
        authors = set(publication.authors)
        discentes = []
        docentes = []

        if issn_ssp_dict.get(str(publication.publisher_issn)):
            ssp = issn_ssp_dict.get(str(publication.publisher_issn)).name
            forum = issn_ssp_dict.get(str(publication.publisher_issn)).name
            qualis = issn_ssp_dict.get(str(publication.publisher_issn)).qualis.value

        for student in students:
            if any([student.authorship_regex.match(x) for x in authors]):
                discentes.append(student)

        for researcher in researchers:
            if any([researcher.authorship_regex.match(x) for x in authors]):
                docentes.append(researcher)

        if forum == '' or len(docentes) == 0:
            continue

        sub_result.append(Record(
            Ano=year,
            Numero=numero,
            Artigo=artigo,
            Fórum=forum,
            Qualis=qualis,
            Discente=[x.full_name for x in discentes],
            Docentes=[x.full_name for x in docentes]))

    year_to_records_dict[year] = sub_result

pprint(year_to_records_dict[YEARS[0]])
