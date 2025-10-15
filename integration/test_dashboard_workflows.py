"""Integration tests for dashboard workflows.

Tests the complete data pipeline from database to filters to visualizations.
Uses mock data to avoid database dependencies in CI.
"""

import unittest

import pandas as pd

from dashboard_auth import is_authenticated, validate_credentials
from data_helpers import bucket_categories, normalize_dataframe
from rescue_filters import apply_rescue_filter


class TestPrimaryWorkflow(unittest.TestCase):
    """Test the primary workflow: Reset → Water → Mountain → Disaster."""

    def setUp(self):
        """Create mock dataset matching AAC schema."""
        self.mock_data = pd.DataFrame({
            'animal_id': ['A001', 'A002', 'A003', 'A004', 'A005', 'A006'],
            'animal_type': ['Dog', 'Dog', 'Dog', 'Dog', 'Dog', 'Cat'],
            'breed': [
                'Labrador Retriever Mix',
                'German Shepherd',
                'Doberman Pinscher',
                'Chesapeake Bay Retriever',
                'Alaskan Malamute',
                'Domestic Shorthair'
            ],
            'name': ['Buddy', 'Max', 'Rex', 'Charlie', 'Duke', 'Mittens'],
            'age_upon_outcome': [
                '2 years', '150 weeks', '4 years',
                '1 year', '2 years', '5 years'
            ],
            'sex_upon_outcome': [
                'Intact Female',
                'Intact Male',
                'Intact Male',
                'Intact Female',
                'Intact Male',
                'Spayed Female'
            ],
            'outcome_type': [
                'Adoption', 'Transfer', 'Adoption',
                'Adoption', 'Transfer', 'Adoption'
            ],
            'location_lat': [
                30.267, 30.268, 30.269, 30.270, 30.271, 30.272
            ],
            'location_long': [
                -97.743, -97.744, -97.745, -97.746, -97.747, -97.748
            ]
        })

    def test_reset_to_water_to_mountain_to_disaster_workflow(self):
        """Test primary workflow sequence shows expected row counts."""
        # Normalize the data
        df = normalize_dataframe(self.mock_data)

        # Step 1: Reset - should show all animals
        reset_result = apply_rescue_filter(df, 'reset')
        self.assertEqual(
            len(reset_result), 6, "Reset should show all 6 animals"
        )

        # Step 2: Water rescue - should show only water rescue candidates
        water_result = apply_rescue_filter(df, 'water')
        self.assertGreater(len(reset_result), len(water_result),
                          "Water filter should reduce dataset")
        # A001: Labrador Female Intact 104 weeks - MATCH
        # A004: Chesapeake Female Intact 52 weeks - MATCH
        self.assertEqual(
            len(water_result), 2, "Should find 2 water rescue candidates"
        )
        self.assertIn('A001', water_result['animal_id'].values)
        self.assertIn('A004', water_result['animal_id'].values)

        # Step 3: Mountain rescue - should show only mountain rescue candidates
        mountain_result = apply_rescue_filter(df, 'mountain')
        self.assertGreater(len(reset_result), len(mountain_result),
                          "Mountain filter should reduce dataset")
        # A002: German Shepherd Male Intact 150 weeks - MATCH
        # A005: Alaskan Malamute Male Intact 104 weeks - MATCH
        self.assertEqual(
            len(mountain_result), 2,
            "Should find 2 mountain rescue candidates"
        )
        self.assertIn('A002', mountain_result['animal_id'].values)
        self.assertIn('A005', mountain_result['animal_id'].values)

        # Step 4: Disaster rescue - should show only disaster rescue candidates
        disaster_result = apply_rescue_filter(df, 'disaster')
        self.assertGreater(len(reset_result), len(disaster_result),
                          "Disaster filter should reduce dataset")
        # A002: German Shepherd Male Intact 156 weeks - MATCH
        # A003: Doberman Male Intact 208 weeks - MATCH
        self.assertEqual(
            len(disaster_result), 2,
            "Should find 2 disaster rescue candidates"
        )
        self.assertIn('A002', disaster_result['animal_id'].values)
        self.assertIn('A003', disaster_result['animal_id'].values)

    def test_filter_results_have_correct_composition(self):
        """Test that filtered results contain only matching animals."""
        df = normalize_dataframe(self.mock_data)

        # Water rescue: Only intact females with water breeds
        water_result = apply_rescue_filter(df, 'water')
        self.assertTrue((water_result['sex'] == 'Female').all())
        self.assertTrue((water_result['intact_status'] == 'Intact').all())

        # Mountain rescue: Only intact males with mountain breeds
        mountain_result = apply_rescue_filter(df, 'mountain')
        self.assertTrue((mountain_result['sex'] == 'Male').all())
        self.assertTrue((mountain_result['intact_status'] == 'Intact').all())

        # Disaster rescue: Only intact males with disaster breeds
        disaster_result = apply_rescue_filter(df, 'disaster')
        self.assertTrue((disaster_result['sex'] == 'Male').all())
        self.assertTrue((disaster_result['intact_status'] == 'Intact').all())


class TestAuthenticationFlow(unittest.TestCase):
    """Test complete authentication workflow."""

    def test_login_failure_to_success_workflow(self):
        """Test failed login followed by successful login."""
        # Step 1: Failed login with wrong credentials
        self.assertFalse(validate_credentials('wrong', 'invalid'))

        # Step 2: Failed login with empty credentials
        self.assertFalse(validate_credentials('', ''))

        # Step 3: Successful login with correct credentials
        self.assertTrue(validate_credentials('admin', 'grazioso2024'))

    def test_session_state_workflow(self):
        """Test authentication session state transitions."""
        # Step 1: Initial state - not authenticated
        initial_state = {'authenticated': False}
        self.assertFalse(is_authenticated(initial_state))

        # Step 2: After successful login - authenticated
        authenticated_state = {'authenticated': True}
        self.assertTrue(is_authenticated(authenticated_state))

        # Step 3: Invalid state - not authenticated
        invalid_state = None
        self.assertFalse(is_authenticated(invalid_state))


class TestDataNormalizationPipeline(unittest.TestCase):
    """Test complete data normalization pipeline."""

    def test_raw_to_normalized_to_filtered_pipeline(self):
        """Test data flows correctly through normalization and filtering."""
        # Step 1: Raw data from database
        raw_data = pd.DataFrame({
            'animal_id': ['A001', 'A002'],
            'animal_type': ['Dog', 'Dog'],
            'breed': ['Labrador Retriever Mix', 'German Shepherd'],
            'age_upon_outcome': ['1 year', '2 years'],
            'sex_upon_outcome': ['Intact Female', 'Intact Male'],
            'outcome_type': ['Adoption', 'Transfer'],
            'location_lat': [30.267, 30.268],
            'location_long': [-97.743, -97.744]
        })

        # Step 2: Normalize data
        normalized = normalize_dataframe(raw_data)

        # Verify normalized columns exist
        self.assertIn('age_weeks', normalized.columns)
        self.assertIn('sex', normalized.columns)
        self.assertIn('intact_status', normalized.columns)

        # Verify age conversion
        self.assertEqual(normalized.loc[0, 'age_weeks'], 52.143)  # 1 year
        self.assertEqual(normalized.loc[1, 'age_weeks'], 104.286)  # 2 years

        # Verify sex/intact parsing
        self.assertEqual(normalized.loc[0, 'sex'], 'Female')
        self.assertEqual(normalized.loc[0, 'intact_status'], 'Intact')
        self.assertEqual(normalized.loc[1, 'sex'], 'Male')
        self.assertEqual(normalized.loc[1, 'intact_status'], 'Intact')

        # Step 3: Filter normalized data
        water_result = apply_rescue_filter(normalized, 'water')
        self.assertEqual(len(water_result), 1)  # Only A001 matches
        self.assertEqual(water_result['animal_id'].iloc[0], 'A001')

        mountain_result = apply_rescue_filter(normalized, 'mountain')
        self.assertEqual(len(mountain_result), 1)  # Only A002 matches
        self.assertEqual(mountain_result['animal_id'].iloc[0], 'A002')


class TestCategoryBucketingWorkflow(unittest.TestCase):
    """Test category bucketing for chart visualization."""

    def test_outcome_type_bucketing_workflow(self):
        """Test outcome types are correctly bucketed for pie chart."""
        # Create dataset with various outcome types
        data = pd.DataFrame({
            'animal_id': ['A001', 'A002', 'A003', 'A004', 'A005',
                         'A006', 'A007', 'A008', 'A009', 'A010',
                         'A011', 'A012'],
            'outcome_type': [
                           'Adoption', 'Adoption', 'Adoption',
                           'Adoption', 'Adoption',
                           'Transfer', 'Transfer', 'Transfer',
                           'Return to Owner', 'Return to Owner',
                           'Euthanasia', 'Died']
        })

        # Get outcome counts as a dict
        # (bucket_categories expects dict, not Series)
        outcome_counts = data['outcome_type'].value_counts().to_dict()

        # Apply bucketing (top 3 + Other)
        category_mapping = bucket_categories(outcome_counts, top_n=3)

        # Verify top 3 are preserved
        self.assertEqual(category_mapping['Adoption'], 'Adoption')
        self.assertEqual(category_mapping['Transfer'], 'Transfer')
        self.assertEqual(
            category_mapping['Return to Owner'], 'Return to Owner'
        )

        # Verify others are bucketed
        self.assertEqual(category_mapping['Euthanasia'], 'Other')
        self.assertEqual(category_mapping['Died'], 'Other')

        # Apply mapping to dataframe
        data['outcome_bucketed'] = data['outcome_type'].map(category_mapping)
        bucketed_counts = data['outcome_bucketed'].value_counts()

        # Verify bucketing worked
        self.assertEqual(bucketed_counts['Adoption'], 5)
        self.assertEqual(bucketed_counts['Transfer'], 3)
        self.assertEqual(bucketed_counts['Return to Owner'], 2)
        self.assertEqual(bucketed_counts['Other'], 2)  # Euthanasia + Died


class TestCoordinateValidationWorkflow(unittest.TestCase):
    """Test coordinate validation for map rendering."""

    def test_valid_and_invalid_coordinates_workflow(self):
        """Test that invalid coordinates are handled gracefully."""
        # Create dataset with mix of valid and invalid coordinates
        data = pd.DataFrame({
            'animal_id': ['A001', 'A002', 'A003', 'A004'],
            'animal_type': ['Dog', 'Dog', 'Dog', 'Dog'],
            'breed': ['Labrador Retriever Mix'] * 4,
            'age_upon_outcome': ['2 years'] * 4,
            'sex_upon_outcome': ['Intact Female'] * 4,
            'outcome_type': ['Adoption'] * 4,
            # Valid, invalid, null, valid
            'location_lat': [30.267, 999.0, None, 30.269],
            # Valid, valid, valid, invalid
            'location_long': [-97.743, -97.744, -97.745, 999.0]
        })

        # Normalize data
        normalized = normalize_dataframe(data)

        # Filter for water rescue
        filtered = apply_rescue_filter(normalized, 'water')

        # Verify all 4 animals match filter criteria
        self.assertEqual(len(filtered), 4)

        # Only A001 should have valid coordinates for map display
        # (Map validation would happen in callback, not filter)
        valid_for_map = filtered[
            (filtered['location_lat'].notna()) &
            (filtered['location_long'].notna()) &
            (filtered['location_lat'] >= -90) &
            (filtered['location_lat'] <= 90) &
            (filtered['location_long'] >= -180) &
            (filtered['location_long'] <= 180)
        ]

        self.assertEqual(len(valid_for_map), 1)  # Only A001
        self.assertEqual(valid_for_map['animal_id'].iloc[0], 'A001')


if __name__ == '__main__':
    unittest.main()
