"""Tests for data_helpers module."""

import unittest

from data_helpers import parse_age_to_weeks


class TestParseAgeToWeeks(unittest.TestCase):
    """Test cases for parse_age_to_weeks function."""

    def test_parse_years(self):
        """Test parsing years to weeks."""
        result = parse_age_to_weeks("2 years")
        self.assertAlmostEqual(result, 104.286, places=2)

        result = parse_age_to_weeks("1 year")
        self.assertAlmostEqual(result, 52.143, places=2)

        result = parse_age_to_weeks("5 years")
        self.assertAlmostEqual(result, 260.715, places=2)

    def test_parse_months(self):
        """Test parsing months to weeks."""
        result = parse_age_to_weeks("6 months")
        self.assertAlmostEqual(result, 26.07, places=2)

        result = parse_age_to_weeks("1 month")
        self.assertAlmostEqual(result, 4.345, places=2)

        result = parse_age_to_weeks("12 months")
        self.assertAlmostEqual(result, 52.14, places=2)

    def test_parse_weeks(self):
        """Test parsing weeks to weeks."""
        result = parse_age_to_weeks("3 weeks")
        self.assertEqual(result, 3.0)

        result = parse_age_to_weeks("1 week")
        self.assertEqual(result, 1.0)

        result = parse_age_to_weeks("52 weeks")
        self.assertEqual(result, 52.0)

    def test_parse_days(self):
        """Test parsing days to weeks."""
        result = parse_age_to_weeks("14 days")
        self.assertEqual(result, 2.0)

        result = parse_age_to_weeks("7 days")
        self.assertEqual(result, 1.0)

        result = parse_age_to_weeks("1 day")
        self.assertAlmostEqual(result, 0.142857, places=5)

    def test_case_insensitive(self):
        """Test case-insensitive parsing."""
        result1 = parse_age_to_weeks("2 Years")
        result2 = parse_age_to_weeks("2 YEARS")
        result3 = parse_age_to_weeks("2 years")
        self.assertAlmostEqual(result1, result2, places=2)
        self.assertAlmostEqual(result2, result3, places=2)

    def test_whitespace_handling(self):
        """Test handling of whitespace."""
        result1 = parse_age_to_weeks("  2 years  ")
        result2 = parse_age_to_weeks("2 years")
        self.assertAlmostEqual(result1, result2, places=2)

    def test_singular_and_plural(self):
        """Test both singular and plural forms."""
        result_singular = parse_age_to_weeks("1 year")
        result_plural = parse_age_to_weeks("1 years")
        self.assertAlmostEqual(result_singular, result_plural, places=2)

    def test_decimal_values(self):
        """Test decimal age values."""
        result = parse_age_to_weeks("1.5 years")
        self.assertAlmostEqual(result, 78.2145, places=2)

        result = parse_age_to_weeks("2.5 months")
        self.assertAlmostEqual(result, 10.8625, places=2)

    def test_none_input(self):
        """Test None input returns None."""
        result = parse_age_to_weeks(None)
        self.assertIsNone(result)

    def test_empty_string(self):
        """Test empty string returns None."""
        result = parse_age_to_weeks("")
        self.assertIsNone(result)

        result = parse_age_to_weeks("   ")
        self.assertIsNone(result)

    def test_invalid_format(self):
        """Test invalid format returns None."""
        result = parse_age_to_weeks("invalid")
        self.assertIsNone(result)

        result = parse_age_to_weeks("abc years")
        self.assertIsNone(result)

        result = parse_age_to_weeks("2")
        self.assertIsNone(result)

    def test_negative_values(self):
        """Test negative values return None."""
        result = parse_age_to_weeks("-2 years")
        self.assertIsNone(result)

    def test_zero_value(self):
        """Test zero value returns None."""
        result = parse_age_to_weeks("0 years")
        self.assertIsNone(result)

    def test_non_string_input(self):
        """Test non-string input returns None."""
        result = parse_age_to_weeks(123)
        self.assertIsNone(result)

        result = parse_age_to_weeks([])
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
