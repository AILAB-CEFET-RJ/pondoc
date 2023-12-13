from pprint import pprint
from data_access_layer.published_works_collectors import OgPondocPublishedWorksCollector
from data_access_layer.researchers_collectors import ScrapperResearchersCollector
from data_access_layer.scientific_serial_publisher_collectors import CsvScientificSerialPublisherCollector
from data_access_layer.students_collectors import CsvStudentsCollector
from report_parameters import ReportParameters


settings = {'startDate': '2017-02-15', 'endDate': '2018-02-15', 'score_weights': []}
ReportParameters.validate_parameters(settings)
report_parameters = ReportParameters(settings['startDate'], settings['endDate'], settings['score_weights'])

# # Data extractors
students, year = CsvStudentsCollector().collect([2022])
# pprint((students))

scientific_serial_publishers = CsvScientificSerialPublisherCollector().collect([2022])
# pprint(scientific_serial_publishers)

researchers, year_researchers_dict = ScrapperResearchersCollector().collect([2022])
# pprint((researchers, {k: len(v) for k,v in year_researchers_dict.items()}))

published_works_dict = OgPondocPublishedWorksCollector().collect([2022])
pprint(published_works_dict)

# papers = ScopusPublishedWorksCollector().collect(year_researchers_dict)

# reserchers = get_researchers()
# published_works = get_published_works(reserchers)
# paper_qualis_dict = get_qualis(published_works)
# # save(students, ...)

# # load(students, ...)
# intermediate_report_representation = calculate_score(settings)
# # save(intermediate_report_representation)

# # load(intermediate_report_representation)
# json_report = export_json_report(intermediate_report_representation)
