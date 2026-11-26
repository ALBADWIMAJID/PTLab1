from .DataReader import DataReader
from .Types import DataType


class TextDataReader(DataReader):
    def read(self, path: str) -> DataType:
        data: DataType = {}
        student = None

        with open(path, encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()
                if not line:
                    continue

                if not raw_line[0].isspace():
                    student = line
                    data.setdefault(student, [])
                    continue

                if student is None:
                    raise ValueError(
                        f"Line {line_number}: subject before student"
                    )

                subject, separator, score_text = line.partition(":")
                subject = subject.strip()
                if not separator or not subject:
                    raise ValueError(
                        f"Line {line_number}: expected subject:score"
                    )

                try:
                    score = int(score_text)
                except ValueError as error:
                    raise ValueError(
                        f"Line {line_number}: score must be an integer"
                    ) from error

                data[student].append((subject, score))

        return data
