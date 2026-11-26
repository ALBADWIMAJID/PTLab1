import pytest

from src.TextDataReader import TextDataReader


def test_read_utf8_data(tmp_path):
    path = tmp_path / "grades.txt"
    path.write_text(
        "Иванов Иван\n    математика:80\n    литература:76\n"
        "Петров Петр\n    химия:61\n",
        encoding="utf-8",
    )

    assert TextDataReader().read(str(path)) == {
        "Иванов Иван": [("математика", 80), ("литература", 76)],
        "Петров Петр": [("химия", 61)],
    }


def test_read_ignores_blank_lines(tmp_path):
    path = tmp_path / "grades.txt"
    path.write_text(
        "\n    \nИванов Иван\n\n    математика:80\n\t\n    литература:76\n\n",
        encoding="utf-8",
    )

    assert TextDataReader().read(str(path)) == {
        "Иванов Иван": [("математика", 80), ("литература", 76)],
    }


def test_repeated_reads_use_fresh_data(tmp_path):
    first_path = tmp_path / "first.txt"
    first_path.write_text("Иванов Иван\n    математика:80\n", encoding="utf-8")
    second_path = tmp_path / "second.txt"
    second_path.write_text("Петров Петр\n    химия:61\n", encoding="utf-8")

    reader = TextDataReader()
    first_data = reader.read(str(first_path))
    second_data = reader.read(str(second_path))

    assert first_data == {"Иванов Иван": [("математика", 80)]}
    assert second_data == {"Петров Петр": [("химия", 61)]}


@pytest.mark.parametrize(
    "content",
    [
        "Иванов Иван\n    математика 80\n",
        "Иванов Иван\n    :80\n",
        "Иванов Иван\n    математика:\n",
        "Иванов Иван\n    математика:80:90\n",
        "Иванов Иван\n    математика:80.5\n",
        "    математика:80\n",
    ],
    ids=[
        "missing-colon",
        "missing-subject",
        "missing-score",
        "extra-colon",
        "non-integer-score",
        "subject-before-student",
    ],
)
def test_read_rejects_malformed_data(tmp_path, content):
    path = tmp_path / "invalid.txt"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError):
        TextDataReader().read(str(path))


def test_read_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        TextDataReader().read(str(tmp_path / "missing.txt"))
