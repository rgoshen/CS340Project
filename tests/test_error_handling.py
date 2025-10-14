"""
Unit tests for error handling and edge cases in AnimalShelter class.

Tests invalid data types, malformed documents, and error scenarios.
"""

import unittest
from tests.fixtures.test_data import (
    BaseTestCase,
    INVALID_DATA_SAMPLES,
    MALFORMED_DOCUMENTS
)


class TestErrorHandling(BaseTestCase):
    """Test cases for error handling with invalid inputs."""

    def test_create_with_invalid_data_types(self):
        """Test create operation with various invalid data types."""
        # Test with string instead of dict
        result = self.shelter.create("string_instead_of_dict")
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

        # Test with integer
        result = self.shelter.create(123)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

        # Test with list
        result = self.shelter.create(["list", "instead", "of", "dict"])
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

        # Test with boolean
        result = self.shelter.create(True)
        self.assertIsInstance(result, bool)
        self.assertFalse(result)

    def test_read_with_invalid_data_types(self):
        """Test read operation with various invalid data types."""
        # Test with string instead of dict
        result = self.shelter.read("string_instead_of_dict")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        # Test with integer
        result = self.shelter.read(123)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        # Test with list
        result = self.shelter.read(["list", "instead", "of", "dict"])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

        # Test with boolean
        result = self.shelter.read(True)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_create_with_malformed_documents(self):
        """Test create operation with malformed but valid dict structures."""
        if not self.use_mock:
            for doc in MALFORMED_DOCUMENTS:
                # These should succeed (MongoDB accepts various structures)
                result = self.shelter.create(doc.copy())
                # Some may succeed, some may fail based on validation
                self.assertIsInstance(result, bool)

    def test_update_with_invalid_data_types(self):
        """Test update operation with invalid data types."""
        # Test with invalid query type
        result = self.shelter.update("string_query", {"field": "value"})
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

        # Test with invalid update_data type
        result = self.shelter.update({"animal_id": "test"}, "string_update")
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

        # Test with both invalid
        result = self.shelter.update("string", "string")
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

    def test_delete_with_invalid_data_types(self):
        """Test delete operation with invalid data types."""
        # Test with string instead of dict
        result = self.shelter.delete("string_instead_of_dict")
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

        # Test with integer
        result = self.shelter.delete(123)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

        # Test with list
        result = self.shelter.delete(["list"])
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

    def test_empty_query_variations(self):
        """Test various empty query scenarios."""
        # Empty dict should return all records (valid for read)
        result = self.shelter.read({})
        self.assertIsInstance(result, list)
        # Should return records if not mocked

        # Empty dict for update (should update 0 records without proper query)
        result = self.shelter.update({}, {"field": "value"})
        self.assertIsInstance(result, int)
        # Returns 0 or more depending on data

        # Empty dict for delete (dangerous but handled)
        # Don't actually test this as it could delete everything!
        # Just verify the method handles it gracefully

    def test_special_characters_in_queries(self):
        """Test queries with special characters."""
        if not self.use_mock:
            # Query with special characters should not crash
            result = self.shelter.read({"name": "Special!@#$%^&*()"})
            self.assertIsInstance(result, list)

            # Query with unicode
            result = self.shelter.read({"name": "Unicode™Ñáméś"})
            self.assertIsInstance(result, list)

    def test_very_large_query_results(self):
        """Test that large query results are handled properly."""
        if not self.use_mock:
            # Query for all dogs (potentially large result set)
            result = self.shelter.read({"animal_type": "Dog"})
            self.assertIsInstance(result, list)
            # Should complete without timeout or memory issues


if __name__ == '__main__':
    unittest.main()
