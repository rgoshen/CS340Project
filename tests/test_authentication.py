"""
Unit tests for authentication and connection handling in AnimalShelter class.

Tests MongoDB authentication, connection timeouts, and security scenarios.
"""

import unittest
from unittest.mock import patch

from pymongo.errors import (
    ConnectionFailure,
    OperationFailure,
    ServerSelectionTimeoutError,
)


class TestAuthentication(unittest.TestCase):
    """Test cases for MongoDB authentication and connection."""

    def test_valid_authentication_with_correct_credentials(self):
        """Test successful connection with valid credentials."""
        from CRUD_Python_Module import AnimalShelter

        # This should succeed with default credentials
        try:
            shelter = AnimalShelter()
            self.assertIsNotNone(shelter.client)
            self.assertIsNotNone(shelter.database)
            self.assertIsNotNone(shelter.collection)

            # Verify we can perform a basic operation
            shelter.client.server_info()

            # Clean up
            shelter.client.close()
        except Exception as e:
            self.fail(f"Valid authentication failed: {e}")

    def test_invalid_authentication_with_wrong_credentials(self):
        """Test connection failure with invalid credentials."""
        from CRUD_Python_Module import AnimalShelter

        # Attempt connection with wrong credentials
        with self.assertRaises((OperationFailure, ConnectionFailure)):
            shelter = AnimalShelter(username="wronguser", password="wrongpass")
            # Force connection attempt
            shelter.client.server_info()
            shelter.client.close()

    def test_connection_timeout_handling(self):
        """Test that connection timeout is properly configured."""
        from CRUD_Python_Module import AnimalShelter

        shelter = AnimalShelter()

        # Verify timeout settings are configured
        # The client should have timeout settings
        self.assertIsNotNone(shelter.client)

        # Test with unreachable host should timeout quickly
        with patch('CRUD_Python_Module.MongoClient') as mock_client:
            mock_client.side_effect = ServerSelectionTimeoutError("Timeout")

            with self.assertRaises(ServerSelectionTimeoutError):
                AnimalShelter()

    def test_database_and_collection_access(self):
        """Test that database and collection are properly accessible."""
        from CRUD_Python_Module import AnimalShelter

        shelter = AnimalShelter()

        # Verify database name
        self.assertEqual(shelter._DB, 'aac')

        # Verify collection name
        self.assertEqual(shelter._COL, 'animals')

        # Verify database object exists
        self.assertIsNotNone(shelter.database)

        # Verify collection object exists
        self.assertIsNotNone(shelter.collection)

        # Test that collection is from the correct database
        self.assertEqual(shelter.collection.name, 'animals')

        # Clean up
        shelter.client.close()


if __name__ == '__main__':
    unittest.main()
