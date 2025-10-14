"""
Unit tests for CRUD operations in AnimalShelter class.

Tests all Create, Read, Update, and Delete operations with valid data,
edge cases, and error conditions.
"""

import unittest

from tests.fixtures.test_data import (
    EMPTY_ID_DATA,
    EMPTY_OBJECT,
    QUERY_SAMPLES,
    SAMPLE_ANIMAL_DATA,
    UPDATE_SAMPLES,
    BaseTestCase,
)


class TestCreate(BaseTestCase):
    """Test cases for the create() method."""

    def test_create_with_valid_data(self):
        """Test create operation with valid animal data."""
        result = self.shelter.create(SAMPLE_ANIMAL_DATA.copy())

        self.assertIsInstance(result, bool)
        self.assertTrue(result)

        # Verify the animal was actually created
        if not self.use_mock:
            self.assertTrue(self.verify_animal_exists("TestID001"))

    def test_create_with_none_data(self):
        """Test create operation with None data."""
        result = self.shelter.create(None)

        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_create_with_duplicate_animal_id(self):
        """Test create operation with duplicate animal_id."""
        # Create first animal
        first_result = self.shelter.create(SAMPLE_ANIMAL_DATA.copy())
        self.assertTrue(first_result)

        # Attempt to create duplicate
        duplicate_result = self.shelter.create(SAMPLE_ANIMAL_DATA.copy())

        self.assertIsInstance(duplicate_result, bool)
        self.assertFalse(duplicate_result)

    def test_create_with_empty_animal_id(self):
        """Test create operation with empty animal_id."""
        result = self.shelter.create(EMPTY_ID_DATA.copy())

        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_create_with_empty_object(self):
        """Test create operation with empty object."""
        result = self.shelter.create(EMPTY_OBJECT.copy())

        self.assertIsInstance(result, bool)
        self.assertFalse(result)


class TestRead(BaseTestCase):
    """Test cases for the read() method."""

    def setUp(self):
        """Set up test fixtures and create test data."""
        super().setUp()
        # Create test animal for read operations
        if not self.use_mock:
            self.create_test_animal(SAMPLE_ANIMAL_DATA.copy())

    def test_read_with_valid_query(self):
        """Test read operation with valid query."""
        result = self.shelter.read(QUERY_SAMPLES["find_by_id"])

        self.assertIsInstance(result, list)
        if not self.use_mock:
            self.assertGreater(len(result), 0)
            self.assertEqual(result[0]["animal_id"], "TestID001")
            self.assertEqual(result[0]["name"], "TestDog")

    def test_read_with_non_matching_query(self):
        """Test read operation with query that matches no records."""
        result = self.shelter.read(QUERY_SAMPLES["find_none"])

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_read_with_none_query(self):
        """Test read operation with None query."""
        result = self.shelter.read(None)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)


class TestUpdate(BaseTestCase):
    """Test cases for the update() method."""

    def setUp(self):
        """Set up test fixtures and create test data."""
        super().setUp()
        # Create test animal for update operations
        if not self.use_mock:
            self.create_test_animal(SAMPLE_ANIMAL_DATA.copy())

    def test_update_with_explicit_set_operator(self):
        """Test update operation with explicit $set operator."""
        result = self.shelter.update(
            QUERY_SAMPLES["find_by_id"],
            UPDATE_SAMPLES["with_set"]
        )

        self.assertIsInstance(result, int)
        if not self.use_mock:
            self.assertGreaterEqual(result, 1)

            # Verify the update
            updated = self.shelter.read(QUERY_SAMPLES["find_by_id"])
            self.assertEqual(updated[0]["outcome_type"], "Transfer")

    def test_update_without_operator_auto_wrap(self):
        """Test update operation without operator (auto-wrap in $set)."""
        result = self.shelter.update(
            QUERY_SAMPLES["find_by_id"],
            {"name": "UpdatedTestDog"}
        )

        self.assertIsInstance(result, int)
        if not self.use_mock:
            self.assertGreaterEqual(result, 1)

            # Verify the update
            updated = self.shelter.read(QUERY_SAMPLES["find_by_id"])
            self.assertEqual(updated[0]["name"], "UpdatedTestDog")

    def test_update_with_none_query(self):
        """Test update operation with None query."""
        result = self.shelter.update(None, UPDATE_SAMPLES["simple_update"])

        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

    def test_update_with_none_update_data(self):
        """Test update operation with None update_data."""
        result = self.shelter.update(QUERY_SAMPLES["find_by_id"], None)

        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

    def test_update_with_non_matching_query(self):
        """Test update operation with query that matches no documents."""
        result = self.shelter.update(
            QUERY_SAMPLES["find_none"],
            UPDATE_SAMPLES["simple_update"]
        )

        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)


class TestDelete(BaseTestCase):
    """Test cases for the delete() method."""

    def setUp(self):
        """Set up test fixtures and create test data."""
        super().setUp()
        # Create test animal for delete operations
        if not self.use_mock:
            self.create_test_animal(SAMPLE_ANIMAL_DATA.copy())

    def test_delete_with_valid_query(self):
        """Test delete operation with valid query."""
        result = self.shelter.delete(QUERY_SAMPLES["find_by_id"])

        self.assertIsInstance(result, int)
        if not self.use_mock:
            self.assertGreaterEqual(result, 1)

            # Verify deletion
            remaining = self.shelter.read(QUERY_SAMPLES["find_by_id"])
            self.assertEqual(len(remaining), 0)

    def test_delete_with_none_query(self):
        """Test delete operation with None query."""
        result = self.shelter.delete(None)

        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

    def test_delete_with_non_matching_query(self):
        """Test delete operation with query that matches no documents."""
        result = self.shelter.delete(QUERY_SAMPLES["find_none"])

        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

    def test_delete_multiple_documents(self):
        """Test delete operation that removes multiple documents."""
        if not self.use_mock:
            # Create multiple test records
            test_data_1 = SAMPLE_ANIMAL_DATA.copy()
            test_data_1["animal_id"] = "TestDelete001"
            test_data_1["outcome_type"] = "Test_Delete"

            test_data_2 = SAMPLE_ANIMAL_DATA.copy()
            test_data_2["animal_id"] = "TestDelete002"
            test_data_2["outcome_type"] = "Test_Delete"

            test_data_3 = SAMPLE_ANIMAL_DATA.copy()
            test_data_3["animal_id"] = "TestDelete003"
            test_data_3["outcome_type"] = "Test_Delete"

            self.shelter.create(test_data_1)
            self.shelter.create(test_data_2)
            self.shelter.create(test_data_3)

        # Delete all with outcome_type="Test_Delete"
        result = self.shelter.delete({"outcome_type": "Test_Delete"})

        self.assertIsInstance(result, int)
        if not self.use_mock:
            self.assertEqual(result, 3)


if __name__ == '__main__':
    unittest.main()
