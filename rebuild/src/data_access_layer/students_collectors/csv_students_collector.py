from uuid import uuid4
import pandas
from typing import Dict, List, Set, Tuple

from entities.student_entity import StudentEntity
from .interface_students_collector import IStudentsCollector


class CsvStudentsCollector(IStudentsCollector):
    """Gets students data from a CSV file."""

    def collect(self, years: List[int]) -> Tuple[Dict[str, StudentEntity], Dict[int, Set[str]]]:
        students_dict = {}
        year_students_dict = {year: set() for year in years}

        for year in years:
            students_df = pandas.read_csv(f'./static_data/students/students-2022.csv')
            # students_df = pandas.read_csv(f'./static_data/students/students-{year}.csv')
            students_df = self._upper_case_student_names(students_df)

            for student_dict in students_df.to_dict('records'):
                student = self._create_student_from_dict(student_dict)
                year_students_dict[year].add(student.full_name)

                if student.full_name not in student_dict:
                    students_dict[student.full_name] = student

        return students_dict, year_students_dict

    @staticmethod
    def _upper_case_student_names(students_df: pandas.DataFrame) -> pandas.DataFrame:
        copy_df = students_df.copy()
        copy_df['nome'] = students_df['nome'].str.upper()
        return copy_df

    @staticmethod
    def _create_student_from_dict(student_dict: Dict) -> StudentEntity:
        return StudentEntity(registration=uuid4().hex, full_name=student_dict['nome'])
