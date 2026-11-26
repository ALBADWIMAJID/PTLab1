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


@pytest.mark.parametrize("extension", [".yaml", ".yml"])
@pytest.mark.parametrize("quartile_only", [False, True])
def test_cli_reads_yaml(tmp_path, extension, quartile_only):
    path = tmp_path / f"students{extension}"
    path.write_text(
        "- A: {math: 50}\n"
        "- B: {math: 60}\n"
        "- C: {math: 70}\n"
        "- D: {math: 80}\n",
        encoding="utf-8",
    )
    project_root = Path(__file__).resolve().parents[1]
    command = [sys.executable, "-m", "src.main", "-p", str(path)]
    if quartile_only:
        command.append("--second-quartile")

    result = subprocess.run(
        command,
        cwd=project_root,
        check=True,
        capture_output=True,
        encoding="utf-8",
    )

    expected = ["A: 50.0", "B: 60.0", "C: 70.0", "D: 80.0"]
    if quartile_only:
        expected = ["B: 60.0"]

    assert result.stdout.splitlines() == expected


def test_cli_reports_empty_second_quartile(tmp_path):
    path = tmp_path / "equal.yaml"
    path.write_text(
        "- A: {math: 80}\n- B: {math: 80}\n",
        encoding="utf-8",
    )
    project_root = Path(__file__).resolve().parents[1]

    result = subprocess.run(
        [
            sys.executable, "-m", "src.main",
            "-p", str(path), "--second-quartile",
        ],
        cwd=project_root,
        check=True,
        capture_output=True,
        encoding="utf-8",
    )

    assert result.stdout.strip() == "No students in the second quartile."
