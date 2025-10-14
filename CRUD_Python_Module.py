"""
CRUD Python Module for Austin Animal Center Database.

This module provides MongoDB CRUD operations for animal shelter data
following PEP 8 and industry best practices.
"""

from typing import Any

from pymongo import MongoClient
from pymongo.errors import (
    ConfigurationError,
    ConnectionFailure,
    DuplicateKeyError,
    OperationFailure,
    PyMongoError,
    ServerSelectionTimeoutError,
    WriteError,
)


class AnimalShelter:
    """
    CRUD operations for Animal collection in MongoDB.

    Provides complete Create, Read, Update, and Delete functionality for
    Austin Animal Center database with comprehensive error handling and
    industry-standard best practices.

    Attributes:
        client: MongoDB client connection
        database: Reference to 'aac' database
        collection: Reference to 'animals' collection
    """

    # Class constants for database connection (DRY principle)
    _USER = 'aacuser'
    _PASS = 'SNHU1234'
    _HOST = 'localhost'
    _PORT = 27017
    _DB = 'aac'
    _COL = 'animals'

    def __init__(self, username: str = None, password: str = None) -> None:
        """
        Initialize MongoDB connection with authentication.

        Establishes connection to localhost MongoDB instance using class
        constants and connects to the 'aac' database 'animals' collection.

        Raises:
            ConnectionFailure: If unable to connect to MongoDB server
            ServerSelectionTimeoutError: If MongoDB server is unreachable
            ConfigurationError: If connection parameters are invalid
        """

        # Use provided credentials or fall back to class constants
        user = username if username else self._USER
        pwd = password if password else self._PASS

        try:
            # Build MongoDB connection string with credentials
            connection_string = (
                f'mongodb://{user}:{pwd}@'
                f'{self._HOST}:{self._PORT}'
            )

            # Create MongoDB client connection with timeout settings
            self.client = MongoClient(
                connection_string,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=5000           # 5 second connection timeout
            )

            # Test the connection by attempting to get server info
            # This forces an actual connection attempt
            self.client.server_info()

            # Access specific database instance from MongoDB server
            self.database = self.client[self._DB]

            # Access specific collection within database for CRUD operations
            self.collection = self.database[self._COL]

            print(f"✓ Successfully connected to MongoDB database '{self._DB}'")

        except ConnectionFailure as error:
            print(f"✗ Failed to connect to MongoDB: {error}")
            raise
        except ServerSelectionTimeoutError as error:
            print(
                f"✗ MongoDB server timeout - is MongoDB running on "
                f"{self._HOST}:{self._PORT}? {error}"
            )
            raise
        except ConfigurationError as error:
            print(f"✗ MongoDB configuration error: {error}")
            raise
        except Exception as error:
            print(f"✗ Unexpected error during MongoDB connection: {error}")
            raise

    def _validate_input(self, data: Any, input_type: str = "data") -> bool:
        """
        Common input validation for CRUD operations.

        Args:
            data: Input data to validate
            input_type (str): Type of input for error messaging

        Returns:
            bool: True if valid, False otherwise
        """
        return data is not None

    def _handle_database_error(
        self, operation: str, error: PyMongoError
    ) -> None:
        """
        Common error handling for database operations.

        Args:
            operation (str): The operation that failed
            error (PyMongoError): MongoDB-specific exception that occurred
        """
        print(f"{operation} operation failed: {error}")

    def create(self, data: dict[str, Any] | None) -> bool:
        """
        Insert a document into the animals collection.

        Validates required fields, checks for duplicates, and inserts
        animal data into MongoDB collection with comprehensive error
        handling.

        Args:
            data (dict): Key/value pairs for document insertion. Must contain
                        'animal_id' field. Example:
                        {
                            "animal_id": "A123456",
                            "name": "Buddy",
                            "animal_type": "Dog",
                            "breed": "Labrador Mix"
                        }

        Returns:
            bool: True if successful insert, False otherwise

        Example:
            >>> shelter = AnimalShelter()
            >>> animal_data = {
            ...     "animal_id": "A123",
            ...     "name": "Rex",
            ...     "animal_type": "Dog"
            ... }
            >>> result = shelter.create(animal_data)
            >>> print(result)  # True
        """
        # Use common input validation
        if not self._validate_input(data):
            return False

        try:
            # Extract animal_id from document for validation and
            # duplicate checking
            animal_id = data.get("animal_id")
            if not animal_id:
                print("animal_id is required and cannot be empty")
                return False

            # MongoDB find_one() - checks for existing document with
            # same animal_id. Returns None if not found, dict if found
            existing = self.collection.find_one({"animal_id": animal_id})
            if existing:
                print(f"Animal with ID {animal_id} already exists")
                return False

            # MongoDB insert_one() - adds new document to collection
            # Automatically generates ObjectId if not provided
            self.collection.insert_one(data)
            return True

        except DuplicateKeyError as error:
            print(f"Duplicate key error: {error}")
            return False
        except WriteError as error:
            print(f"MongoDB write error: {error}")
            return False
        except OperationFailure as error:
            print(f"MongoDB operation failed: {error}")
            return False
        except PyMongoError as error:
            self._handle_database_error("Insert", error)
            return False
        except Exception as error:
            print(f"Unexpected error during insert: {error}")
            return False

    def read(self, query: dict[str, Any] | None) -> list[dict[str, Any]]:
        """
        Query documents from the animals collection.

        Uses MongoDB find() method to retrieve documents matching query
        criteria and returns results as Python list with proper cursor
        handling.

        Args:
            query (dict): Key/value lookup pairs for MongoDB find() operation.
                         Use {} for all documents. Example:
                         {
                             "animal_type": "Dog",
                             "outcome_type": "Adoption"
                         }

        Returns:
            list: List of matching documents as dictionaries. Returns empty
                 list if no documents match or on error.

        Example:
            >>> shelter = AnimalShelter()
            >>> dogs = shelter.read({"animal_type": "Dog"})
            >>> print(len(dogs))  # Number of dogs found
            >>> specific_animal = shelter.read({"animal_id": "A123456"})
            >>> print(specific_animal[0]["name"])  # Animal name
        """
        # Use common input validation
        if not self._validate_input(query, "query"):
            return []

        try:
            # MongoDB find() - returns cursor object for query results
            # Cursor is iterable but not list - allows efficient memory
            # usage
            cursor = self.collection.find(query)

            # Convert MongoDB cursor to Python list for easier handling
            # This loads all results into memory - suitable for
            # moderate result sets
            results = list(cursor)
            return results

        except OperationFailure as error:
            print(f"MongoDB query operation failed: {error}")
            return []
        except PyMongoError as error:
            self._handle_database_error("Read", error)
            return []
        except Exception as error:
            print(f"Unexpected error during read: {error}")
            return []

    def update(
        self,
        query: dict[str, Any] | None,
        update_data: dict[str, Any] | None
    ) -> int:
        """
        Update documents in the animals collection.

        Modifies documents matching the query criteria with the provided update
        data. Automatically wraps update_data in $set operator if no MongoDB
        operator is provided.

        Args:
            query (dict): Key/value pairs to match documents for update.
                         Example: {"animal_type": "Dog", "breed": "Labrador"}
            update_data (dict): Update operations to apply. Can include MongoDB
                              operators ($set, $inc, $push, etc.) or plain
                              key/value pairs (auto-wrapped in $set).
                              Example: {"outcome_type": "Adoption"}
                              Example: {"$set": {"outcome_type": "Adoption"}}

        Returns:
            int: Number of documents modified (modified_count).
                 Returns 0 if no documents modified or on error.

        Example:
            >>> shelter = AnimalShelter()
            >>> # Update without operator (auto-wrapped in $set)
            >>> count = shelter.update(
            ...     {"animal_id": "A123"},
            ...     {"outcome_type": "Adoption"}
            ... )
            >>> print(count)  # 1
            >>>
            >>> # Update with explicit operator
            >>> count = shelter.update(
            ...     {"animal_type": "Dog"},
            ...     {"$set": {"location_lat": 30.2672}}
            ... )
            >>> print(count)  # Number of dogs updated
        """
        # Validate query parameter
        if not self._validate_input(query, "query"):
            return 0

        # Validate update_data parameter
        if not self._validate_input(update_data, "update_data"):
            return 0

        try:
            # Check if update_data contains MongoDB update operators
            # Operators start with $ (e.g., $set, $inc, $push, $pull)
            has_operator = any(
                key.startswith('$') for key in update_data
            )

            # If no operator provided, wrap in $set for safety
            # This prevents accidental document replacement
            if not has_operator:
                update_data = {"$set": update_data}

            # MongoDB update_many() - modifies all documents matching query
            # Returns UpdateResult object with modified_count attribute
            result = self.collection.update_many(query, update_data)

            # Return count of actually modified documents
            # Note: matched_count may differ from modified_count if values
            # are identical
            return result.modified_count

        except WriteError as error:
            print(f"MongoDB write error during update: {error}")
            return 0
        except OperationFailure as error:
            print(f"MongoDB update operation failed: {error}")
            return 0
        except PyMongoError as error:
            self._handle_database_error("Update", error)
            return 0
        except Exception as error:
            print(f"Unexpected error during update: {error}")
            return 0

    def delete(self, query: dict[str, Any] | None) -> int:
        """
        Delete documents from the animals collection.

        Removes documents matching the query criteria from the MongoDB
        collection and returns the count of deleted documents.

        Args:
            query (dict): Key/value pairs to match documents for
                         deletion. Example: {"animal_id": "A123456"}

        Returns:
            int: Number of documents deleted (deleted_count).
                 Returns 0 if no documents deleted or on error.

        Example:
            >>> shelter = AnimalShelter()
            >>> # Delete single document by animal_id
            >>> count = shelter.delete({"animal_id": "A123"})
            >>> print(count)  # 1
            >>>
            >>> # Delete multiple documents by criteria
            >>> count = shelter.delete({"outcome_type": "Transfer"})
            >>> print(count)  # Number of transfer records deleted
        """
        # Validate query parameter
        if not self._validate_input(query, "query"):
            return 0

        try:
            # MongoDB delete_many() - removes all documents matching query
            # Returns DeleteResult object with deleted_count attribute
            result = self.collection.delete_many(query)

            # Return count of deleted documents
            return result.deleted_count

        except WriteError as error:
            print(f"MongoDB write error during delete: {error}")
            return 0
        except OperationFailure as error:
            print(f"MongoDB delete operation failed: {error}")
            return 0
        except PyMongoError as error:
            self._handle_database_error("Delete", error)
            return 0
        except Exception as error:
            print(f"Unexpected error during delete: {error}")
            return 0
