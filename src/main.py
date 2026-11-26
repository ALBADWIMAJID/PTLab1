import argparse
import sys
from pathlib import Path

from .CalcRating import CalcRating
from .SecondQuartile import SecondQuartile
from .TextDataReader import TextDataReader
from .YamlDataReader import YamlDataReader


def parse_arguments(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate student ratings.")
    parser.add_argument(
        "-p", "--path", required=True, help="Input TXT or YAML file"
    )
    parser.add_argument(
        "--second-quartile",
        action="store_true",
        help="Show only students with ratings in (Q1, Q2]",
    )
    return parser.parse_args(args)


def get_path_from_arguments(args: list[str] | None = None) -> str:
    return parse_arguments(args).path


def main() -> None:
    args = parse_arguments()
    extension = Path(args.path).suffix.lower()

    if extension in {".yaml", ".yml"}:
        reader = YamlDataReader()
    elif extension == ".txt":
        reader = TextDataReader()
    else:
        raise ValueError("Supported file extensions: .txt, .yaml, .yml")

    data = reader.read(args.path)
    ratings = CalcRating(data).calc()

    if args.second_quartile:
        ratings = SecondQuartile(ratings).calc()
        if not ratings:
            print("No students in the second quartile.")
            return

    for student, rating in ratings.items():
        print(f"{student}: {rating}")


if __name__ == "__main__":
    # Keep Cyrillic names readable when output is redirected on Windows.
    sys.stdout.reconfigure(encoding="utf-8")
    main()
