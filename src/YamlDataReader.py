import yaml

from .DataReader import DataReader
from .Types import DataType


class YamlDataReader(DataReader):
    def read(self, path: str) -> DataType:
        with open(path, encoding="utf-8-sig") as file:
            try:
                entries = yaml.safe_load(file)
            except yaml.YAMLError as error:
                raise ValueError("Invalid YAML syntax") from error

        if entries is None:
            return {}

        if not isinstance(entries, list):
            raise ValueError("Expected a list of student records")

        data: DataType = {}

        for entry in entries:
            if not isinstance(entry, dict) or len(entry) != 1:
                raise ValueError("Each record must contain one student")

            student, subjects = next(iter(entry.items()))

            if not isinstance(student, str) or not student.strip():
                raise ValueError("Student name must be a non-empty string")

            student = student.strip()
            if student in data:
                raise ValueError(f"Duplicate student: {student}")

            if not isinstance(subjects, dict) or not subjects:
                raise ValueError("Student must have a subject mapping")

            grades: list[tuple[str, int]] = []
            for subject, score in subjects.items():
                if not isinstance(subject, str) or not subject.strip():
                    raise ValueError("Subject must be a non-empty string")

                if type(score) is not int:
                    raise ValueError("Score must be an integer")

                grades.append((subject.strip(), score))

            data[student] = grades

        return data