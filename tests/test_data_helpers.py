"""Tests for data_helpers module."""

import unittest

from data_helpers import (
    breed_matches_rescue_type,
    bucket_categories,
    normalize_sex_intact,
    parse_age_to_weeks,
    validate_coordinates,
)


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


class TestNormalizeSexIntact(unittest.TestCase):
    """Test cases for normalize_sex_intact function."""

    def test_neutered_male(self):
        """Test parsing 'Neutered Male'."""
        sex, intact = normalize_sex_intact("Neutered Male")
        self.assertEqual(sex, 'Male')
        self.assertEqual(intact, 'Neutered')

    def test_intact_female(self):
        """Test parsing 'Intact Female'."""
        sex, intact = normalize_sex_intact("Intact Female")
        self.assertEqual(sex, 'Female')
        self.assertEqual(intact, 'Intact')

    def test_spayed_female(self):
        """Test parsing 'Spayed Female'."""
        sex, intact = normalize_sex_intact("Spayed Female")
        self.assertEqual(sex, 'Female')
        self.assertEqual(intact, 'Spayed')

    def test_intact_male(self):
        """Test parsing 'Intact Male'."""
        sex, intact = normalize_sex_intact("Intact Male")
        self.assertEqual(sex, 'Male')
        self.assertEqual(intact, 'Intact')

    def test_case_insensitive(self):
        """Test case-insensitive parsing."""
        sex1, intact1 = normalize_sex_intact("NEUTERED MALE")
        sex2, intact2 = normalize_sex_intact("neutered male")
        sex3, intact3 = normalize_sex_intact("Neutered Male")

        self.assertEqual(sex1, sex2)
        self.assertEqual(sex2, sex3)
        self.assertEqual(intact1, intact2)
        self.assertEqual(intact2, intact3)

    def test_whitespace_handling(self):
        """Test handling of whitespace."""
        sex1, intact1 = normalize_sex_intact("  Neutered Male  ")
        sex2, intact2 = normalize_sex_intact("Neutered Male")

        self.assertEqual(sex1, sex2)
        self.assertEqual(intact1, intact2)

    def test_none_input(self):
        """Test None input returns Unknown."""
        sex, intact = normalize_sex_intact(None)
        self.assertEqual(sex, 'Unknown')
        self.assertEqual(intact, 'Unknown')

    def test_empty_string(self):
        """Test empty string returns Unknown."""
        sex, intact = normalize_sex_intact("")
        self.assertEqual(sex, 'Unknown')
        self.assertEqual(intact, 'Unknown')

        sex, intact = normalize_sex_intact("   ")
        self.assertEqual(sex, 'Unknown')
        self.assertEqual(intact, 'Unknown')

    def test_unknown_value(self):
        """Test 'Unknown' input returns Unknown."""
        sex, intact = normalize_sex_intact("Unknown")
        self.assertEqual(sex, 'Unknown')
        self.assertEqual(intact, 'Unknown')

    def test_invalid_format(self):
        """Test invalid format returns Unknown for missing parts."""
        sex, intact = normalize_sex_intact("Male")
        self.assertEqual(sex, 'Male')
        self.assertEqual(intact, 'Unknown')

        sex, intact = normalize_sex_intact("Neutered")
        self.assertEqual(sex, 'Unknown')
        self.assertEqual(intact, 'Neutered')

    def test_non_string_input(self):
        """Test non-string input returns Unknown."""
        sex, intact = normalize_sex_intact(123)
        self.assertEqual(sex, 'Unknown')
        self.assertEqual(intact, 'Unknown')

        sex, intact = normalize_sex_intact([])
        self.assertEqual(sex, 'Unknown')
        self.assertEqual(intact, 'Unknown')


class TestValidateCoordinates(unittest.TestCase):
    """Test cases for validate_coordinates function."""

    def test_valid_coordinates_float(self):
        """Test valid coordinates as floats."""
        self.assertTrue(validate_coordinates(30.2672, -97.7431))
        self.assertTrue(validate_coordinates(0.0, 0.0))
        self.assertTrue(validate_coordinates(-90, -180))
        self.assertTrue(validate_coordinates(90, 180))

    def test_valid_coordinates_string(self):
        """Test valid coordinates as strings."""
        self.assertTrue(validate_coordinates("30.2672", "-97.7431"))
        self.assertTrue(validate_coordinates("0", "0"))

    def test_latitude_out_of_range(self):
        """Test latitude out of valid range."""
        self.assertFalse(validate_coordinates(91, -97.7431))
        self.assertFalse(validate_coordinates(-91, -97.7431))
        self.assertFalse(validate_coordinates(100, 0))

    def test_longitude_out_of_range(self):
        """Test longitude out of valid range."""
        self.assertFalse(validate_coordinates(30.2672, 181))
        self.assertFalse(validate_coordinates(30.2672, -181))
        self.assertFalse(validate_coordinates(0, 200))

    def test_none_values(self):
        """Test None values return False."""
        self.assertFalse(validate_coordinates(None, -97.7431))
        self.assertFalse(validate_coordinates(30.2672, None))
        self.assertFalse(validate_coordinates(None, None))

    def test_invalid_string_values(self):
        """Test invalid string values return False."""
        self.assertFalse(validate_coordinates("invalid", -97.7431))
        self.assertFalse(validate_coordinates(30.2672, "invalid"))
        self.assertFalse(validate_coordinates("abc", "xyz"))

    def test_non_numeric_types(self):
        """Test non-numeric types return False."""
        self.assertFalse(validate_coordinates([], -97.7431))
        self.assertFalse(validate_coordinates(30.2672, {}))
        self.assertFalse(validate_coordinates({}, []))

    def test_nan_values(self):
        """Test NaN values return False."""
        self.assertFalse(validate_coordinates(float('nan'), -97.7431))
        self.assertFalse(validate_coordinates(30.2672, float('nan')))

    def test_boundary_values(self):
        """Test boundary values are valid."""
        self.assertTrue(validate_coordinates(90, 180))
        self.assertTrue(validate_coordinates(-90, -180))
        self.assertTrue(validate_coordinates(90, -180))
        self.assertTrue(validate_coordinates(-90, 180))


class TestBreedMatchesRescueType(unittest.TestCase):
    """Test cases for breed_matches_rescue_type function."""

    def test_water_rescue_exact_match(self):
        """Test water rescue with exact breed matches."""
        self.assertTrue(
            breed_matches_rescue_type("Labrador Retriever", "water")
        )
        self.assertTrue(
            breed_matches_rescue_type("Chesapeake Bay Retriever", "water")
        )
        self.assertTrue(breed_matches_rescue_type("Newfoundland", "water"))

    def test_water_rescue_mix(self):
        """Test water rescue with mixed breeds."""
        self.assertTrue(
            breed_matches_rescue_type("Labrador Retriever Mix", "water")
        )
        self.assertTrue(
            breed_matches_rescue_type("Labrador Retriever/Pit Bull", "water")
        )

    def test_mountain_rescue_breeds(self):
        """Test mountain rescue breed matches."""
        self.assertTrue(
            breed_matches_rescue_type("German Shepherd", "mountain")
        )
        self.assertTrue(
            breed_matches_rescue_type("Alaskan Malamute", "mountain")
        )
        self.assertTrue(
            breed_matches_rescue_type("Old English Sheepdog", "mountain")
        )
        self.assertTrue(
            breed_matches_rescue_type("Siberian Husky", "mountain")
        )
        self.assertTrue(
            breed_matches_rescue_type("Rottweiler", "mountain")
        )

    def test_disaster_rescue_breeds(self):
        """Test disaster rescue breed matches."""
        self.assertTrue(
            breed_matches_rescue_type("Doberman Pinscher", "disaster")
        )
        self.assertTrue(
            breed_matches_rescue_type("German Shepherd", "disaster")
        )
        self.assertTrue(
            breed_matches_rescue_type("Golden Retriever", "disaster")
        )
        self.assertTrue(
            breed_matches_rescue_type("Bloodhound", "disaster")
        )
        self.assertTrue(
            breed_matches_rescue_type("Rottweiler", "disaster")
        )

    def test_tracking_same_as_disaster(self):
        """Test tracking uses same breeds as disaster."""
        self.assertTrue(
            breed_matches_rescue_type("Bloodhound", "tracking")
        )
        self.assertTrue(
            breed_matches_rescue_type("German Shepherd", "tracking")
        )

    def test_case_insensitive(self):
        """Test case-insensitive breed matching."""
        self.assertTrue(
            breed_matches_rescue_type("LABRADOR RETRIEVER", "water")
        )
        self.assertTrue(
            breed_matches_rescue_type("labrador retriever", "water")
        )
        self.assertTrue(
            breed_matches_rescue_type("Labrador Retriever", "WATER")
        )

    def test_multi_breed_with_separators(self):
        """Test multi-breed strings with various separators."""
        self.assertTrue(
            breed_matches_rescue_type("Labrador Retriever/Pit Bull", "water")
        )
        self.assertTrue(
            breed_matches_rescue_type("German Shepherd Mix", "mountain")
        )

    def test_non_matching_breed(self):
        """Test breeds that don't match rescue type."""
        self.assertFalse(breed_matches_rescue_type("Poodle", "water"))
        self.assertFalse(breed_matches_rescue_type("Chihuahua", "mountain"))
        self.assertFalse(breed_matches_rescue_type("Beagle", "disaster"))

    def test_none_breed(self):
        """Test None breed returns False."""
        self.assertFalse(breed_matches_rescue_type(None, "water"))

    def test_empty_breed(self):
        """Test empty breed returns False."""
        self.assertFalse(breed_matches_rescue_type("", "water"))
        self.assertFalse(breed_matches_rescue_type("   ", "water"))

    def test_invalid_rescue_type(self):
        """Test invalid rescue type returns False."""
        self.assertFalse(
            breed_matches_rescue_type("Labrador Retriever", "invalid")
        )
        self.assertFalse(
            breed_matches_rescue_type("German Shepherd", "unknown")
        )

    def test_non_string_breed(self):
        """Test non-string breed returns False."""
        self.assertFalse(breed_matches_rescue_type(123, "water"))
        self.assertFalse(breed_matches_rescue_type([], "water"))


class TestBucketCategories(unittest.TestCase):
    """Test cases for bucket_categories function."""

    def test_basic_bucketing(self):
        """Test basic bucketing with clear top categories."""
        values = ["A", "A", "A", "B", "B", "C"]
        result = bucket_categories(values, top_n=2)
        self.assertEqual(result["A"], "A")
        self.assertEqual(result["B"], "B")
        self.assertEqual(result["C"], "Other")

    def test_deterministic_tie_breaking(self):
        """Test alphabetical tie-breaking when counts are equal."""
        values = ["Dog", "Cat", "Bird"]  # All have count 1
        result = bucket_categories(values, top_n=2)
        # Bird and Cat should be top 2 (alphabetically first)
        self.assertEqual(result["Bird"], "Bird")
        self.assertEqual(result["Cat"], "Cat")
        self.assertEqual(result["Dog"], "Other")

    def test_all_categories_fit(self):
        """Test when top_n >= number of unique categories."""
        values = ["A", "B", "C"]
        result = bucket_categories(values, top_n=10)
        self.assertEqual(result["A"], "A")
        self.assertEqual(result["B"], "B")
        self.assertEqual(result["C"], "C")

    def test_top_n_one(self):
        """Test with top_n=1."""
        values = ["A", "A", "B", "C"]
        result = bucket_categories(values, top_n=1)
        self.assertEqual(result["A"], "A")
        self.assertEqual(result["B"], "Other")
        self.assertEqual(result["C"], "Other")

    def test_empty_list(self):
        """Test empty list returns empty dict."""
        result = bucket_categories([], top_n=5)
        self.assertEqual(result, {})

    def test_zero_top_n(self):
        """Test top_n=0 returns empty dict."""
        values = ["A", "B", "C"]
        result = bucket_categories(values, top_n=0)
        self.assertEqual(result, {})

    def test_negative_top_n(self):
        """Test negative top_n returns empty dict."""
        values = ["A", "B", "C"]
        result = bucket_categories(values, top_n=-1)
        self.assertEqual(result, {})

    def test_duplicate_values_in_list(self):
        """Test that duplicate values in input are handled correctly."""
        values = ["A", "A", "A", "B", "B", "C", "D"]
        result = bucket_categories(values, top_n=2)
        # A appears 3 times, B appears 2 times - these are top 2
        self.assertEqual(result["A"], "A")
        self.assertEqual(result["B"], "B")
        self.assertEqual(result["C"], "Other")
        self.assertEqual(result["D"], "Other")

    def test_mapping_includes_all_unique_values(self):
        """Test that mapping includes all unique values from input."""
        values = ["A", "A", "B", "C", "D"]
        result = bucket_categories(values, top_n=2)
        self.assertIn("A", result)
        self.assertIn("B", result)
        self.assertIn("C", result)
        self.assertIn("D", result)


if __name__ == '__main__':
    unittest.main()
