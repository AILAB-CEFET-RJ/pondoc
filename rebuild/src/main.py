from pprint import pprint
from typing import List, TypedDict

from openpyxl import Workbook, load_workbook

from data_access_layer.published_works_collectors import OgPondocPublishedWorksCollector
from data_access_layer.researchers_collectors import ScrapperResearchersCollector
from data_access_layer.scientific_serial_publisher_collectors import CsvScientificSerialPublisherCollector
from data_access_layer.students_collectors import CsvStudentsCollector
from entities import ResearcherEntity
from entities import StudentEntity
from helpers import number_to_column_label


def main(_years: List[int]) -> Workbook:
    pass

    # Data extractors
    students, year_students_dict = CsvStudentsCollector().collect(_years)
    year_students_dict = {k: [students[x] for x in v] for k,v in year_students_dict.items()}
    # pprint(students)

    issn_ssp_dict = CsvScientificSerialPublisherCollector().collect(_years)
    # pprint(issn_ssp_dict)

    _researchers, year_researchers_dict = ScrapperResearchersCollector().collect(_years)
    year_researchers_dict = {k: [_researchers[x] for x in v] for k,v in year_researchers_dict.items()}
    # pprint((researchers, {k: len(v) for k,v in year_researchers_dict.items()}))
    # pprint(researchers['5882024148867913'].authorship_regex.match('D. N. BRANDAO'))
    # pprint(researchers['5882024148867913'].authorship_regex.match('DIEGO. BRANDAO'))


    year_published_works_dict = OgPondocPublishedWorksCollector().collect(_years)
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
    for year in _years:
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
                ssp = issn_ssp_dict.get(str(publication.publisher_issn))
                forum = ssp.name
                qualis = ssp.qualis.value

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
                Discente=discentes,
                Docentes=docentes))

        year_to_records_dict[year] = sub_result

    # Excel
    XL_FILE_NAME = './reports/base-copy.xlsx'
    workbook = load_workbook(XL_FILE_NAME)

    # Fill LConferencias
    sheet = workbook['LConferencias']
    i = 2
    for conf in issn_ssp_dict.values():
        sheet[f'A{i}'] = conf.name
        sheet[f'B{i}'] = conf.qualis.value
        sheet[f'C{i}'] = f'=IF(B{i}<>"NI",1,0)'
        sheet[f'D{i}'] = f'=VLOOKUP(B{i}, Tabelas!A:C,3,FALSE())'
        sheet[f'E{i}'] = f'=VLOOKUP(B{i}, Tabelas!A:C,2,FALSE())'
        i += 1

    # Fill Conferencias
    sheet = workbook['Conferencias']

    docentes = list(_researchers.values())
    docente_id_to_col_dict = {}
    sheet.insert_cols(11, len(docentes) - 1)

    i = 0
    for docente in docentes:
        col = f'{number_to_column_label(11 + i)}1'
        sheet[col] = docente.full_name
        docente_id_to_col_dict[docente.lattes_id] = number_to_column_label(11 + i)
        i += 1

    i = 2
    for year in _years:
        records = year_to_records_dict[year]

        for record in records:
            sheet[f'A{i}'] = record['Ano']
            sheet[f'B{i}'] = record['Numero']
            sheet[f'C{i}'] = record['Artigo']
            sheet[f'D{i}'] = record['Fórum']
            sheet[f'E{i}'] = ','.join([x.full_name for x in record['Discente']])
            sheet[f'F{i}'] = record['Qualis']
            sheet[f'G{i}'].value = f'=VLOOKUP(D{i}, LConferencias!A:C,3,FALSE())'
            sheet[f'H{i}'] = f'=VLOOKUP(D{i}, LConferencias!A:D,4,FALSE())'
            sheet[f'I{i}'] = f'=IF(E{i}<>"",1,0)'

            for pesquisador in record['Docentes']:
                sheet[docente_id_to_col_dict[pesquisador.lattes_id] + f'{i}'] = 1

            sheet[f'{number_to_column_label(10 + len(docentes) + 2)}{i}'] = f'=VLOOKUP(F{i}, Tabelas!A:C,2,FALSE())'
            sheet[f'{number_to_column_label(10 + len(docentes) + 3)}{i}'] = f'=SUM(K{i}:{number_to_column_label(10 + len(docentes))}{i})'
            sheet[f'{number_to_column_label(10 + len(docentes) + 4)}{i}'] = f'=IF({number_to_column_label(10 + len(docentes) + 3)}{i}<=2,1,1-LOG({number_to_column_label(10 + len(docentes) + 3)}{i}-1))'
            sheet[f'{number_to_column_label(10 + len(docentes) + 5)}{i}'] = f'=VLOOKUP(D{i}, LConferencias!A:E,5,FALSE())*IF(I{i}>0,1.1,1)*{number_to_column_label(10 + len(docentes) + 4)}{i}'

            i += 1

    # pprint(year_to_records_dict[YEARS[0]])
    return workbook

if __name__ == '__main__':
    main([2019,2020,2021,2022]).save('./reports/base-copy_1.xlsx')
