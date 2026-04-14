import csv
import tempfile
import unittest
from pathlib import Path

from clean_fake_news_dataset import clean_dataset, clean_fake_news_title


class CleanFakeNewsDatasetTests(unittest.TestCase):
    def test_removes_old_photo_marker(self):
        original = "গত ১৫ আগস্টে যুবলীগের দোয়া মাহফিলের দৃশ্য দাবিতে পুরোনো ছবি প্রচার"
        expected = "গত ১৫ আগস্টে যুবলীগের দোয়া মাহফিলের দৃশ্য দাবিতে ছবি প্রচার"
        self.assertEqual(clean_fake_news_title(original), expected)

    def test_fixes_trailing_shonakter(self):
        original = "এভারকেয়ার হাসপাতালে এমপক্স (মাঙ্কিপক্স) শনাক্তের"
        expected = "এভারকেয়ার হাসপাতালে এমপক্স (মাঙ্কিপক্স) শনাক্ত"
        self.assertEqual(clean_fake_news_title(original), expected)

    def test_clean_dataset_preserves_source_and_label_columns(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "input.csv"
            output_path = Path(tmp_dir) / "output.csv"

            with input_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["id", "title", "source", "label"])
                writer.writeheader()
                writer.writerow(
                    {
                        "id": "1",
                        "title": "নেতাকর্মীদের গোপালগঞ্জে আসার দাবিতে সাদ্দামকে উদ্ধৃত করে ঢাকা ট্রিবিউনের নামে ফটোকার্ড প্রচার",
                        "source": "bangla_fakenews",
                        "label": "1",
                    }
                )

            clean_dataset(input_path, output_path)

            with output_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                self.assertEqual(reader.fieldnames, ["id", "title", "source", "label"])
                row = next(reader)

            self.assertEqual(row["source"], "bangla_fakenews")
            self.assertEqual(row["label"], "1")
            self.assertEqual(
                row["title"],
                "নেতাকর্মীদের গোপালগঞ্জে আসার দাবিতে সাদ্দামকে উদ্ধৃত করে ঢাকা ট্রিবিউনের নামে ফটোকার্ড প্রচার",
            )


if __name__ == "__main__":
    unittest.main()
