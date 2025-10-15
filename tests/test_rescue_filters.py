"""Tests for rescue_filters module."""

import unittest

import pandas as pd

from rescue_filters import (
    apply_rescue_filter,
    disaster_rescue_filter,
    mountain_rescue_filter,
    reset_filter,
    water_rescue_filter,
)


class TestWaterRescueFilter(unittest.TestCase):
    """Test cases for water_rescue_filter function."""

    def setUp(self):
        """Create test DataFrame with normalized data."""
        self.df = pd.DataFrame({
            'animal_id': ['A001', 'A002', 'A003', 'A004', 'A005'],
            'breed': [
                'Labrador Retriever Mix',
                'Chesapeake Bay Retriever',
                'German Shepherd',
                'Labrador Retriever',
                'Newfoundland'
            ],
            'sex': ['Female', 'Female', 'Female', 'Male', 'Female'],
            'intact_status': [
                'Intact',
                'Intact',
                'Intact',
                'Intact',
                'Spayed'
            ],
            'age_weeks': [52, 100, 52, 52, 52]
        })

    def test_filters_correct_breed(self):
        """Test that only water rescue breeds are included."""
        result = water_rescue_filter(self.df)
        # A001: Labrador Retriever Mix, Female, Intact, 52 weeks - MATCH
        # A002: Chesapeake Bay Retriever, Female, Intact, 100 weeks - MATCH
        # A003: German Shepherd - wrong breed
        # A004: Labrador Retriever, Male - wrong sex
        # A005: Newfoundland, Spayed - wrong intact status
        self.assertEqual(len(result), 2)
        self.assertIn('A001', result['animal_id'].values)
        self.assertIn('A002', result['animal_id'].values)

    def test_filters_correct_sex(self):
        """Test that only intact females are included."""
        result = water_rescue_filter(self.df)
        self.assertTrue((result['sex'] == 'Female').all())
        self.assertTrue((result['intact_status'] == 'Intact').all())

    def test_filters_correct_age_range(self):
        """Test that only animals in age range 26-156 weeks are included."""
        df_age_test = pd.DataFrame({
            'animal_id': ['A001', 'A002', 'A003', 'A004'],
            'breed': ['Labrador Retriever Mix'] * 4,
            'sex': ['Female'] * 4,
            'intact_status': ['Intact'] * 4,
            'age_weeks': [25, 26, 156, 157]  # Below, min, max, above
        })
        result = water_rescue_filter(df_age_test)
        # Only A002 (26 weeks) and A003 (156 weeks) should match
        self.assertEqual(len(result), 2)
        self.assertIn('A002', result['animal_id'].values)
        self.assertIn('A003', result['animal_id'].values)

    def test_empty_result_when_no_matches(self):
        """Test that empty DataFrame is returned when no matches."""
        df_no_match = pd.DataFrame({
            'animal_id': ['A001'],
            'breed': ['Poodle'],
            'sex': ['Female'],
            'intact_status': ['Intact'],
            'age_weeks': [52]
        })
        result = water_rescue_filter(df_no_match)
        self.assertEqual(len(result), 0)


class TestMountainRescueFilter(unittest.TestCase):
    """Test cases for mountain_rescue_filter function."""

    def setUp(self):
        """Create test DataFrame with normalized data."""
        self.df = pd.DataFrame({
            'animal_id': ['A001', 'A002', 'A003', 'A004', 'A005'],
            'breed': [
                'German Shepherd',
                'Alaskan Malamute',
                'Labrador Retriever',
                'German Shepherd',
                'Rottweiler'
            ],
            'sex': ['Male', 'Male', 'Male', 'Female', 'Male'],
            'intact_status': [
                'Intact',
                'Intact',
                'Intact',
                'Intact',
                'Neutered'
            ],
            'age_weeks': [52, 100, 52, 52, 52]
        })

    def test_filters_correct_breed(self):
        """Test that only mountain rescue breeds are included."""
        result = mountain_rescue_filter(self.df)
        # A001: German Shepherd, Male, Intact, 52 weeks - MATCH
        # A002: Alaskan Malamute, Male, Intact, 100 weeks - MATCH
        # A003: Labrador Retriever - wrong breed
        # A004: German Shepherd, Female - wrong sex
        # A005: Rottweiler, Neutered - wrong intact status
        self.assertEqual(len(result), 2)
        self.assertIn('A001', result['animal_id'].values)
        self.assertIn('A002', result['animal_id'].values)

    def test_filters_correct_sex(self):
        """Test that only intact males are included."""
        result = mountain_rescue_filter(self.df)
        self.assertTrue((result['sex'] == 'Male').all())
        self.assertTrue((result['intact_status'] == 'Intact').all())

    def test_filters_correct_age_range(self):
        """Test that only animals in age range 26-156 weeks are included."""
        df_age_test = pd.DataFrame({
            'animal_id': ['A001', 'A002', 'A003', 'A004'],
            'breed': ['German Shepherd'] * 4,
            'sex': ['Male'] * 4,
            'intact_status': ['Intact'] * 4,
            'age_weeks': [25, 26, 156, 157]
        })
        result = mountain_rescue_filter(df_age_test)
        self.assertEqual(len(result), 2)
        self.assertIn('A002', result['animal_id'].values)
        self.assertIn('A003', result['animal_id'].values)


class TestDisasterRescueFilter(unittest.TestCase):
    """Test cases for disaster_rescue_filter function."""

    def setUp(self):
        """Create test DataFrame with normalized data."""
        self.df = pd.DataFrame({
            'animal_id': ['A001', 'A002', 'A003', 'A004', 'A005'],
            'breed': [
                'Doberman Pinscher',
                'German Shepherd',
                'Golden Retriever',
                'German Shepherd',
                'Bloodhound'
            ],
            'sex': ['Male', 'Male', 'Male', 'Female', 'Male'],
            'intact_status': [
                'Intact',
                'Intact',
                'Intact',
                'Intact',
                'Neutered'
            ],
            'age_weeks': [52, 100, 200, 52, 52]
        })

    def test_filters_correct_breed(self):
        """Test that only disaster rescue breeds are included."""
        result = disaster_rescue_filter(self.df)
        # A001: Doberman Pinscher, Male, Intact, 52 weeks - MATCH
        # A002: German Shepherd, Male, Intact, 100 weeks - MATCH
        # A003: Golden Retriever, Male, Intact, 200 weeks - MATCH
        # A004: German Shepherd, Female - wrong sex
        # A005: Bloodhound, Neutered - wrong intact status
        self.assertEqual(len(result), 3)
        self.assertIn('A001', result['animal_id'].values)
        self.assertIn('A002', result['animal_id'].values)
        self.assertIn('A003', result['animal_id'].values)

    def test_filters_correct_sex(self):
        """Test that only intact males are included."""
        result = disaster_rescue_filter(self.df)
        self.assertTrue((result['sex'] == 'Male').all())
        self.assertTrue((result['intact_status'] == 'Intact').all())

    def test_filters_correct_age_range(self):
        """Test that only animals in age range 20-300 weeks are included."""
        df_age_test = pd.DataFrame({
            'animal_id': ['A001', 'A002', 'A003', 'A004'],
            'breed': ['German Shepherd'] * 4,
            'sex': ['Male'] * 4,
            'intact_status': ['Intact'] * 4,
            'age_weeks': [19, 20, 300, 301]  # Below, min, max, above
        })
        result = disaster_rescue_filter(df_age_test)
        self.assertEqual(len(result), 2)
        self.assertIn('A002', result['animal_id'].values)
        self.assertIn('A003', result['animal_id'].values)


class TestResetFilter(unittest.TestCase):
    """Test cases for reset_filter function."""

    def test_returns_unchanged_dataframe(self):
        """Test that reset_filter returns the entire DataFrame unchanged."""
        df = pd.DataFrame({
            'animal_id': ['A001', 'A002', 'A003'],
            'breed': ['Labrador', 'Poodle', 'German Shepherd'],
            'sex': ['Male', 'Female', 'Male'],
            'age_weeks': [52, 100, 200]
        })
        result = reset_filter(df)
        self.assertEqual(len(result), len(df))
        pd.testing.assert_frame_equal(result, df)

    def test_preserves_all_rows(self):
        """Test that all rows are preserved."""
        df = pd.DataFrame({
            'animal_id': ['A001', 'A002', 'A003', 'A004', 'A005']
        })
        result = reset_filter(df)
        self.assertEqual(len(result), 5)


class TestApplyRescueFilter(unittest.TestCase):
    """Test cases for apply_rescue_filter dispatcher function."""

    def setUp(self):
        """Create test DataFrame with normalized data."""
        self.df = pd.DataFrame({
            'animal_id': ['A001', 'A002', 'A003'],
            'breed': [
                'Labrador Retriever',
                'German Shepherd',
                'Doberman Pinscher'
            ],
            'sex': ['Female', 'Male', 'Male'],
            'intact_status': ['Intact', 'Intact', 'Intact'],
            'age_weeks': [52, 52, 52]
        })

    def test_dispatches_to_water_filter(self):
        """Test that 'water' dispatches to water_rescue_filter."""
        result = apply_rescue_filter(self.df, 'water')
        # Only A001 (Labrador, Female, Intact) should match
        self.assertEqual(len(result), 1)
        self.assertEqual(result['animal_id'].iloc[0], 'A001')

    def test_dispatches_to_mountain_filter(self):
        """Test that 'mountain' dispatches to mountain_rescue_filter."""
        result = apply_rescue_filter(self.df, 'mountain')
        # Only A002 (German Shepherd, Male, Intact) should match
        self.assertEqual(len(result), 1)
        self.assertEqual(result['animal_id'].iloc[0], 'A002')

    def test_dispatches_to_disaster_filter(self):
        """Test that 'disaster' dispatches to disaster_rescue_filter."""
        result = apply_rescue_filter(self.df, 'disaster')
        # A002 (German Shepherd) and A003 (Doberman) should match
        self.assertEqual(len(result), 2)

    def test_tracking_same_as_disaster(self):
        """Test that 'tracking' uses disaster_rescue_filter."""
        disaster_result = apply_rescue_filter(self.df, 'disaster')
        tracking_result = apply_rescue_filter(self.df, 'tracking')
        pd.testing.assert_frame_equal(disaster_result, tracking_result)

    def test_wilderness_same_as_mountain(self):
        """Test that 'wilderness' uses mountain_rescue_filter."""
        mountain_result = apply_rescue_filter(self.df, 'mountain')
        wilderness_result = apply_rescue_filter(self.df, 'wilderness')
        pd.testing.assert_frame_equal(mountain_result, wilderness_result)

    def test_dispatches_to_reset_filter(self):
        """Test that 'reset' dispatches to reset_filter."""
        result = apply_rescue_filter(self.df, 'reset')
        self.assertEqual(len(result), len(self.df))

    def test_empty_string_same_as_reset(self):
        """Test that empty string uses reset_filter."""
        result = apply_rescue_filter(self.df, '')
        self.assertEqual(len(result), len(self.df))

    def test_case_insensitive(self):
        """Test that filter type is case-insensitive."""
        result_lower = apply_rescue_filter(self.df, 'water')
        result_upper = apply_rescue_filter(self.df, 'WATER')
        result_mixed = apply_rescue_filter(self.df, 'WaTeR')
        pd.testing.assert_frame_equal(result_lower, result_upper)
        pd.testing.assert_frame_equal(result_lower, result_mixed)

    def test_whitespace_handling(self):
        """Test that filter type handles whitespace."""
        result_no_space = apply_rescue_filter(self.df, 'water')
        result_with_space = apply_rescue_filter(self.df, '  water  ')
        pd.testing.assert_frame_equal(result_no_space, result_with_space)

    def test_invalid_filter_type_raises_error(self):
        """Test that invalid filter type raises ValueError."""
        with self.assertRaises(ValueError) as context:
            apply_rescue_filter(self.df, 'invalid')

        self.assertIn('invalid', str(context.exception).lower())
        self.assertIn('water', str(context.exception))
        self.assertIn('mountain', str(context.exception))


if __name__ == '__main__':
    unittest.main()
