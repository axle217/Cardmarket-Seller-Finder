import argparse
import csv
from collections import defaultdict


def read_csv(filename, column):
    """
    Read a CSV and return:
        {
            column_value: [row, row, ...]
        }
    """
    results = defaultdict(list)

    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError(f"{filename}: CSV has no header")

        if column not in reader.fieldnames:
            raise ValueError(
                f"{filename}: column '{column}' not found. "
                f"Available columns: {', '.join(reader.fieldnames)}"
            )

        for row in reader:
            value = row[column].strip()

            if value:
                results[value].append(row)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Find values occurring in multiple CSV files."
    )

    parser.add_argument(
        "column",
        help="Column to search for"
    )

    parser.add_argument(
        "files",
        nargs="+",
        help="CSV files to search"
    )

    args = parser.parse_args()

    # value -> filename -> rows
    matches = defaultdict(lambda: defaultdict(list))

    for filename in args.files:
        data = read_csv(filename, args.column)

        for value, rows in data.items():
            for row in rows:
                matches[value][filename].append(row)

    # Only keep values appearing in multiple files
    common = {
        value: files
        for value, files in matches.items()
        if len(files) >= 2
    }

    if not common:
        print("No values found in multiple files.")
        return

    print(f"Found {len(common)} values occurring in multiple files.\n")

    for value in sorted(common):
        print("=" * 80)
        print(f"{args.column}: {value}")

        files = common[value]

        for filename in args.files:
            if filename not in files:
                continue

            print(f"\n  [{filename}]")

            for row in files[filename]:
                print(f"    {row}")


if __name__ == "__main__":
    main()
