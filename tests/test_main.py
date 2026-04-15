import unittest

from main import AffiliatePerformance


class TestAffiliatePerformance(unittest.TestCase):
    def test_valid_record_casts_numeric_fields(self):
        record = AffiliatePerformance(
            date="2026-04-15",
            code="AFF123",
            registration="10",
            ftds="3",
            state="CA",
        )

        self.assertEqual(record.date, "2026-04-15")
        self.assertEqual(record.code, "AFF123")
        self.assertEqual(record.registration, 10)
        self.assertEqual(record.ftds, 3)
        self.assertEqual(record.state, "CA")

    def test_rejects_code_without_aff_prefix(self):
        with self.assertRaises(ValueError):
            AffiliatePerformance(
                date="2026-04-15",
                code="BAD123",
                registration=10,
                ftds=3,
                state="CA",
            )

    def test_rejects_invalid_state(self):
        with self.assertRaises(ValueError):
            AffiliatePerformance(
                date="2026-04-15",
                code="AFF123",
                registration=10,
                ftds=3,
                state="ZZ",
            )

    def test_rejects_negative_numeric_fields(self):
        with self.assertRaises(ValueError):
            AffiliatePerformance(
                date="2026-04-15",
                code="AFF123",
                registration=-1,
                ftds=3,
                state="CA",
            )


if __name__ == "__main__":
    unittest.main()
