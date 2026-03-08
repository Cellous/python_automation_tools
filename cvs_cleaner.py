import csv
import argparse
import os
import sys


def clean_csv(input_file: str, output_file: str, delimiter: str = ",") -> None:
    """
    Cleans a CSV file by removing empty rows and standardizing delimiters.
    """

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file '{input_file}' does not exist.")
        sys.exit(1)

    try:
        with open(input_file, "r", newline="", encoding="utf-8") as infile, \
             open(output_file, "w", newline="", encoding="utf-8") as outfile:

            reader = csv.reader(infile, delimiter=delimiter)
            writer = csv.writer(outfile, delimiter=",")

            rows_written = 0

            for row in reader:
                if any(field.strip() for field in row):
                    writer.writerow(row)
                    rows_written += 1

        print(f"[SUCCESS] Cleaned CSV saved to '{output_file}'.")
        print(f"[INFO] Rows written: {rows_written}")

    except Exception as e:
        print(f"[ERROR] Failed to process file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Clean CSV files by removing empty rows and standardizing delimiters."
    )
    parser.add_argument("input", help="Path to input CSV file")
    parser.add_argument("output", help="Path to output CSV file")
    parser.add_argument(
        "--delimiter",
        default=",",
        help="Input file delimiter (default: ,)"
    )

    args = parser.parse_args()

    clean_csv(args.input, args.output, args.delimiter)


if __name__ == "__main__":
    main()