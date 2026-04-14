import argparse
import csv
import re
from pathlib import Path

_DEBUNKING_PATTERNS = [
    (r"(?<!\S)(পুরোনো|পুরনো)(?=\s+(ছবি|ভিডিও|ফটোকার্ড|ফুটেজ|অডিও|ঘটনা|তথ্য))", ""),
    (r"(?<!\S)সম্পাদিত(?=\s+(ছবি|ভিডিও|ফটোকার্ড|ফুটেজ|তথ্য))", ""),
    (r"(?<!\S)এডিটেড(?=\s+(ছবি|ভিডিও|ফটোকার্ড|ফুটেজ|তথ্য))", ""),
    (r"(?<!\S)বিকৃত(?=\s+(ছবি|ভিডিও|ফটোকার্ড|ফুটেজ|তথ্য))", ""),
    (r"(?<!\S)ভিন্ন\s+ঘটনার(?!\S)", ""),
    (r"(?<!\S)অসম্পর্কিত(?=\s+(ছবি|ভিডিও|ফটোকার্ড|ফুটেজ|তথ্য))", ""),
    (r"(?<!\S)নকল(?=\s+ফটোকার্ড)", ""),
    (r"(?<!\S)ফটোকার্ড\s+নকল(?!\S)", "ফটোকার্ড"),
    (r"(?<!\S)(প্রচারিত\s+)?তথ্যটি$", ""),
    (r"(?<!\S)শনাক্তের$", "শনাক্ত"),
]


def clean_fake_news_title(title: str) -> str:
    """Remove common debunking markers while preserving the core fake claim."""
    cleaned = (title or "").strip()

    for pattern, replacement in _DEBUNKING_PATTERNS:
        cleaned = re.sub(pattern, replacement, cleaned)

    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"\s+([,;:])", r"\1", cleaned)
    return cleaned.strip(" ,")


def clean_dataset(input_csv: Path, output_csv: Path) -> None:
    """Read a CSV and write a cleaned version preserving all original columns."""
    with input_csv.open("r", encoding="utf-8", newline="") as source_file:
        reader = csv.DictReader(source_file)
        if not reader.fieldnames or "title" not in reader.fieldnames:
            raise ValueError("Input CSV must contain a 'title' column")

        rows = []
        for row in reader:
            row = dict(row)
            row["title"] = clean_fake_news_title(row.get("title", ""))
            rows.append(row)

    with output_csv.open("w", encoding="utf-8", newline="") as target_file:
        writer = csv.DictWriter(target_file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean Bangla fake news titles by removing debunking markers."
    )
    parser.add_argument(
        "--input",
        default="/home/runner/work/BFakeN/BFakeN/fake_news_title_only_version.csv",
        help="Absolute path of input CSV file",
    )
    parser.add_argument(
        "--output",
        default="/home/runner/work/BFakeN/BFakeN/fake_news_title_only_version_cleaned.csv",
        help="Absolute path of output CSV file",
    )
    args = parser.parse_args()

    clean_dataset(Path(args.input), Path(args.output))


if __name__ == "__main__":
    main()
