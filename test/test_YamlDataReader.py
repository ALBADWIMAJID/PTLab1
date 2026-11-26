import pytest

from src.DataReader import DataReader
from src.YamlDataReader import YamlDataReader


def test_read_yaml(tmp_path):
    path = tmp_path / "students.yaml"
    path.write_text(
        "- Иванов Иван:\n"
        "    математика: 80\n"
        "    физика: 90\n"
        "- Петров Петр:\n"
        "    химия: 61\n",
        encoding="utf-8",
    )

    reader = YamlDataReader()

    assert isinstance(reader, DataReader)
    assert reader.read(str(path)) == {
        "Иванов Иван": [("математика", 80), ("физика", 90)],
        "Петров Петр": [("химия", 61)],
    }


@pytest.mark.parametrize("content", ["", "[]"])
def test_empty_yaml(tmp_path, content):
    path = tmp_path / "empty.yaml"
    path.write_text(content, encoding="utf-8")

    assert YamlDataReader().read(str(path)) == {}


@pytest.mark.parametrize(
    "content",
    [
        "Student: {math: 80}",
        "- Student",
        "- {}",
        "- A: {math: 80}\n  B: {math: 90}",
        "- '': {math: 80}",
        "- 123: {math: 80}",
        "- A: {}",
        "- A: [80, 90]",
        "- A: {'': 80}",
        "- A: {123: 80}",
        "- A: {math: 'bad'}",
        "- A: {math: 80.5}",
        "- A: {math: true}",
        "- A: {math: 80}\n- A: {math: 90}",
        "- A: [",
    ],
)
def test_invalid_yaml(tmp_path, content):
    path = tmp_path / "invalid.yaml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError):
        YamlDataReader().read(str(path))


def test_missing_yaml_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        YamlDataReader().read(str(tmp_path / "missing.yaml"))


def test_repeated_reads_use_fresh_data(tmp_path):
    path = tmp_path / "students.yaml"
    reader = YamlDataReader()

    path.write_text("- A: {math: 80}", encoding="utf-8")
    assert reader.read(str(path)) == {"A": [("math", 80)]}

    path.write_text("- B: {physics: 90}", encoding="utf-8")
    assert reader.read(str(path)) == {"B": [("physics", 90)]}
