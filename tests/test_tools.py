import tempfile
import unittest
from pathlib import Path

from utils.tools import format_date, read_csv


class TestTools(unittest.TestCase):
    def test_format_date_trims_time_component(self):
        self.assertEqual(format_date("2026-04-15 13:45:00"), "2026-04-15")

    def test_read_csv_reads_rows(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "sample.csv"
            csv_path.write_text("a,b,c\n1,2,3\n", encoding="utf-8")

            rows = read_csv(str(csv_path))

        self.assertEqual(rows, [["a", "b", "c"], ["1", "2", "3"]])


if __name__ == "__main__":
    unittest.main()
