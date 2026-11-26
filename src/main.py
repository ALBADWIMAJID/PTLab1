import argparse
import sys

from .CalcRating import CalcRating
from .TextDataReader import TextDataReader


def get_path_from_arguments(args: list[str] | None = None) -> str:
    parser = argparse.ArgumentParser(description="Calculate student ratings.")
    parser.add_argument("-p", "--path", required=True, help="Input TXT file")
    return parser.parse_args(args).path


def main() -> None:
    path = get_path_from_arguments()
    data = TextDataReader().read(path)
    ratings = CalcRating(data).calc()

    for student, rating in ratings.items():
        print(f"{student}: {rating}")


if __name__ == "__main__":
    # Keep Cyrillic names readable when output is redirected on Windows.
    sys.stdout.reconfigure(encoding="utf-8")
    main()
