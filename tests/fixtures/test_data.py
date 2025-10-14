"""
Test data fixtures for CRUD operation testing.

Provides sample animal data, invalid data samples, and query examples
used across the test suite.
"""

import os
import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any


# Sample valid animal data following AAC schema
SAMPLE_ANIMAL_DATA = {
    "rec_num": "99999",
    "age_upon_outcome": "2 years",
    "animal_id": "TestID001",
    "animal_type": "Dog",
    "breed": "Labrador Retriever Mix",
    "color": "Golden/White",
    "date_of_birth": "2021-06-15",
    "datetime": "2023-06-20 14:30:00",
    "monthyear": "2023-06-20T14:30:00",
    "name": "TestDog",
    "outcome_subtype": "",
    "outcome_type": "Adoption",
    "sex_upon_outcome": "Neutered Male",
    "location_lat": 30.2672,
    "location_long": -97.7431,
    "age_upon_outcome_in_weeks": 104.0
}

# Additional valid animal for multi-record tests
SAMPLE_ANIMAL_DATA_2 = {
    "rec_num": "99998",
    "age_upon_outcome": "1 year",
    "animal_id": "TestID002",
    "animal_type": "Cat",
    "breed": "Domestic Shorthair",
    "color": "Black/White",
    "date_of_birth": "2022-06-15",
    "datetime": "2023-06-20 15:30:00",
    "monthyear": "2023-06-20T15:30:00",
    "name": "TestCat",
    "outcome_subtype": "",
    "outcome_type": "Transfer",
    "sex_upon_outcome": "Spayed Female",
    "location_lat": 30.2700,
    "location_long": -97.7500,
    "age_upon_outcome_in_weeks": 52.0
}

# Animal with empty animal_id (invalid)
EMPTY_ID_DATA = {
    "animal_id": "",
    "name": "TestDog",
    "animal_type": "Dog"
}

# Empty object (invalid)
EMPTY_OBJECT = {}

# Invalid data types for testing error handling
INVALID_DATA_SAMPLES = [
    "string_instead_of_dict",
    123,
    ["list", "instead", "of", "dict"],
    True,
    None
]

# Malformed documents for edge case testing
MALFORMED_DOCUMENTS = [
    {
        "animal_id": "TEST_MALFORMED",
        "nested": {"invalid": {"deep": "structure"}}
    },
    {
        "animal_id": "TEST_SPECIAL_CHARS",
        "name": "Special!@#$%^&*()Characters"
    },
    {
        "animal_id": "TEST_UNICODE",
        "name": "Unicode™Ñáméś"
    }
]

# Sample queries for read operations
QUERY_SAMPLES = {
    "find_by_id": {"animal_id": "TestID001"},
    "find_by_type": {"animal_type": "Dog"},
    "find_by_outcome": {"outcome_type": "Adoption"},
    "find_none": {"animal_id": "NonExistentID"},
    "find_all": {}
}

# Sample update operations
UPDATE_SAMPLES = {
    "simple_update": {"outcome_type": "Return to Owner"},
    "with_set": {"$set": {"outcome_type": "Transfer"}},
    "with_inc": {"$inc": {"adoption_count": 1}}
}


class BaseTestCase(unittest.TestCase):
    """
    Base test case class with shared setUp and tearDown methods.

    Provides common functionality for all test classes including:
    - Database connection setup
    - Test data creation
    - Test data cleanup
    - Mock vs real database switching via environment variable
    """

    @classmethod
    def setUpClass(cls):
        """Set up class-level resources."""
        # Check if we should use mocked database
        cls.use_mock = os.environ.get('USE_MOCK_DB', 'false').lower() == 'true'

    def setUp(self):
        """Set up test fixtures before each test method."""
        if self.use_mock:
            self._setup_mock_db()
        else:
            self._setup_real_db()

    def tearDown(self):
        """Clean up test data after each test method."""
        if not self.use_mock and hasattr(self, 'shelter'):
            self._cleanup_test_data()
            # Close MongoDB connection to prevent resource warnings
            if hasattr(self.shelter, 'client'):
                self.shelter.client.close()

    def _setup_real_db(self):
        """Set up connection to real MongoDB instance."""
        from CRUD_Python_Module import AnimalShelter
        self.shelter = AnimalShelter()

    def _setup_mock_db(self):
        """Set up mocked MongoDB connection."""
        from CRUD_Python_Module import AnimalShelter

        # Create mock objects
        mock_client = MagicMock()
        mock_database = MagicMock()
        mock_collection = MagicMock()

        # Wire up the mocks
        mock_client.__getitem__.return_value = mock_database
        mock_database.__getitem__.return_value = mock_collection

        # Patch MongoClient and create shelter instance
        with patch('CRUD_Python_Module.MongoClient', return_value=mock_client):
            self.shelter = AnimalShelter()
            self.shelter.collection = mock_collection

    def _cleanup_test_data(self):
        """Remove all test data from database."""
        test_ids = [
            "TestID001", "TestID002", "TestID003",
            "TEST_MALFORMED", "TEST_SPECIAL_CHARS", "TEST_UNICODE",
            "TestDelete001", "TestDelete002", "TestDelete003"
        ]

        for test_id in test_ids:
            try:
                self.shelter.collection.delete_many({"animal_id": test_id})
            except Exception:
                pass  # Ignore cleanup errors

        # Also cleanup by outcome_type for multi-delete tests
        try:
            self.shelter.collection.delete_many({"outcome_type": "Test_Delete"})
        except Exception:
            pass

    def create_test_animal(self, animal_data: Dict[str, Any] = None) -> bool:
        """
        Helper method to create a test animal.

        Args:
            animal_data: Animal data dictionary (uses SAMPLE_ANIMAL_DATA if None)

        Returns:
            bool: True if creation successful, False otherwise
        """
        data = animal_data if animal_data else SAMPLE_ANIMAL_DATA.copy()
        return self.shelter.create(data)

    def verify_animal_exists(self, animal_id: str) -> bool:
        """
        Helper method to verify an animal exists in database.

        Args:
            animal_id: The animal_id to search for

        Returns:
            bool: True if animal exists, False otherwise
        """
        results = self.shelter.read({"animal_id": animal_id})
        return len(results) > 0
