import subprocess
import sys
from pathlib import Path

import pytest

from src.main import get_path_from_arguments


@pytest.mark.parametrize("flag", ["-p", "--path"])
def test_get_path_from_arguments(flag):
    path = "data/student grades.txt"
    assert get_path_from_arguments([flag, path]) == path


def test_get_path_from_arguments_requires_path():
    with pytest.raises(SystemExit) as error:
        get_path_from_arguments([])

    assert error.value.code == 2


def test_cli_prints_sample_ratings():
    project_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "src.main", "-p", "data/data.txt"],
        cwd=project_root,
        check=True,
        capture_output=True,
        encoding="utf-8",
    )

    assert result.stdout.splitlines() == [
        "Иванов Иван Иванович: 82.0",
        "Петров Петр Петрович: 83.66666666666667",
    ]
