# Grazioso Rescue Finder

![CI Status](https://github.com/rgoshen/CS340Project/actions/workflows/on-push.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)
![MongoDB Version](https://img.shields.io/badge/mongodb-8.0-green.svg)
![PyMongo Version](https://img.shields.io/badge/pymongo-4.10.1-blue.svg)
![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

- [Grazioso Rescue Finder](#grazioso-rescue-finder)
  - [About the Project](#about-the-project)
  - [Motivation](#motivation)
  - [System Architecture](#system-architecture)
  - [CRUD Operations](#crud-operations)
    - [Create Operation](#create-operation)
    - [Read Operation](#read-operation)
    - [Update Operation](#update-operation)
    - [Delete Operation](#delete-operation)
  - [Why PyMongo?](#why-pymongo)
  - [Getting Started](#getting-started)
  - [Quick Start](#quick-start)
  - [Installation](#installation)
    - [Required Tools](#required-tools)
    - [Installation Commands](#installation-commands)
  - [Usage](#usage)
    - [CRUD Module Code Example](#crud-module-code-example)
    - [Dashboard Usage](#dashboard-usage)
    - [Tests](#tests)
    - [Screenshots](#screenshots)
      - [Module Setup and Import](#module-setup-and-import)
      - [Test Data Setup](#test-data-setup)
      - [Creation Operation – Valid data and None Data](#creation-operation--valid-data-and-none-data)
      - [Creation Operation – Duplicate Entry Handling and Empty Animal ID](#creation-operation--duplicate-entry-handling-and-empty-animal-id)
      - [Creation Operation – Handling Empty Object](#creation-operation--handling-empty-object)
      - [Read Operation – Find Record](#read-operation--find-record)
      - [Read Operation – Empty Result](#read-operation--empty-result)
      - [Read Operation – Error Handling](#read-operation--error-handling)
      - [Update Operation with Valid Query and Update Data (Explicit $set)](#update-operation-with-valid-query-and-update-data-explicit-set)
      - [Update Operation without Operator (Auto-wrap in $set)](#update-operation-without-operator-auto-wrap-in-set)
      - [Update Operation with None Query (Error Handling Test)](#update-operation-with-none-query-error-handling-test)
      - [Update Operation with None Update Data (Error Handling Test)](#update-operation-with-none-update-data-error-handling-test)
      - [Update Operation with Non-Matching Query (No Documents Modified)](#update-operation-with-non-matching-query-no-documents-modified)
      - [Delete Operation with Valid Query](#delete-operation-with-valid-query)
      - [Delete Operation with None Query (Error Handling Test)](#delete-operation-with-none-query-error-handling-test)
      - [Delete Operation with Non-Matching Query (No Documents Deleted)](#delete-operation-with-non-matching-query-no-documents-deleted)
      - [Delete Multiple Documents](#delete-multiple-documents)
      - [Test Teardown - Cleanup Test Data](#test-teardown---cleanup-test-data)
  - [Features](#features)
  - [Contact](#contact)

## About the Project

This full-stack application streamlines the identification of rescue dog candidates for Grazioso Salvare through a Python/MongoDB backend and interactive Dash/Plotly web dashboard. Using Austin Animal Center shelter data, the system provides CRUD operations for data management and real-time filtering by rescue specialization (water, mountain, disaster, tracking) based on breed, sex, age, and intact status. The dashboard features authentication, interactive data tables, geolocation maps, and outcome distribution visualizations.

## Motivation

Grazioso Salvare needs an efficient way to identify dogs with the right characteristics for search-and-rescue training from thousands of shelter animals across the Austin area. Manual review of shelter records is time-consuming and inconsistent. This system automates the candidate identification process, enabling trainers to quickly locate dogs that match specific rescue profiles—ultimately getting more qualified animals into life-saving training programs faster while giving shelter dogs a second chance at purposeful work.

## System Architecture

This project follows a Model-View-Controller (MVC) architecture:

**Model (Data Layer):**
- MongoDB database (aac.animals collection)
- AnimalShelter CRUD module (CRUD_Python_Module.py)
- Data normalization functions (data_helpers.py)
- Rescue filter logic (rescue_filters.py)

**View (Presentation Layer):**
- Interactive Dash/Plotly web dashboard (ProjectTwoDashboard.ipynb)
- Authentication gate with login form
- Filtered data table with sorting and pagination
- Geolocation map showing animal locations
- Pie chart showing outcome type distribution

**Controller (Business Logic):**
- Dash callbacks coordinating user interactions
- Filter dispatchers applying rescue criteria
- Authentication validation (dashboard_auth.py)

## CRUD Operations

The CRUD Python module provides four essential database operations for managing animal shelter data:

### Create Operation

- **Purpose**: Insert new animal records into the MongoDB database
- **Method**: `create(data: dict) -> bool`
- **Returns**: `True` on successful insertion, `False` on failure
- **Features**:
  - Validates required `animal_id` field
  - Prevents duplicate entries
  - Comprehensive error handling

### Read Operation

- **Purpose**: Query and retrieve animal records from the database
- **Method**: `read(query: dict) -> list`
- **Returns**: List of matching documents, empty list if none found
- **Features**:
  - Flexible query filtering
  - Returns all matching documents
  - Proper cursor handling for efficient memory usage

### Update Operation

- **Purpose**: Modify existing animal records in the database
- **Method**: `update(query: dict, update_data: dict) -> int`
- **Returns**: Number of modified documents (modified_count)
- **Features**:
  - Auto-wraps update data in `$set` if no operator provided
  - Supports all MongoDB update operators ($set, $inc, $push, etc.)
  - Returns 0 on error or if no documents modified

### Delete Operation

- **Purpose**: Remove animal records from the database
- **Method**: `delete(query: dict) -> int`
- **Returns**: Number of deleted documents (deleted_count)
- **Features**:
  - Removes all documents matching query criteria
  - Returns 0 on error or if no documents deleted
  - Safe deletion with query validation

## Why PyMongo?

PyMongo was selected as the database driver for this project for the following reasons:

1. **Official MongoDB Support**: PyMongo is the official MongoDB driver for Python, ensuring reliable compatibility and long-term support.

2. **Comprehensive Feature Set**: Provides complete access to MongoDB's CRUD operations, aggregation framework, and advanced query capabilities.

3. **Pythonic API**: Offers intuitive, Python-native interface that follows familiar dictionary and list patterns for working with documents.

4. **Performance**: Implements connection pooling and efficient cursor management for optimal database performance.

5. **Active Development**: Regular updates and maintenance from MongoDB Inc. ensure compatibility with latest MongoDB versions and Python releases.

6. **Industry Standard**: Widely adopted in production environments with extensive documentation and community support.

## Getting Started

To get a local copy of this CRUD module up and running, follow these simple steps:

1. Prerequisites
    Before you begin, ensure you have completed the following setup requirements:

    1. MongoDB Installation: MongoDB Community Edition installed and running on localhost:27017
    2. Python Environment: Python 3.13+ with pip package manager
    3. Database Setup: AAC database imported with proper authentication

2. Database Setup

    1. Import the AAC Dataset:

        ```bash
        cd ./datasets
        mongoimport --type=csv --headerline --db aac --collection animals --drop ./aac_shelter_outcomes.csv
        ```

    2. Create Database User:

        ```bash
        mongosh
        use admin
        db.createUser({
            user: "aacuser",
            pwd: passwordPrompt(),
            roles: [{role: "readWrite", db: "aac"}]
            });
        ```

    3. Verify Connection:

        ```bash
        db.runCommand({connectionStatus:1});
        ```

## Quick Start

1. Download all project files to your local development environment
2. Install required dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

3. Start Jupyter Notebook:

    ```bash
    jupyter notebook
    ```

**To run the CRUD module tests:**

- Open `ProjectOneTestScript.ipynb` and run all cells

**To run the interactive dashboard:**

- Open `ProjectTwoDashboard.ipynb` and run the cell
- Login with credentials: `admin` / `grazioso2024`
- Use rescue type filters to identify candidate animals
- Click table rows to view animal locations on the map

That's it! You now have a working full-stack application for identifying rescue dog candidates.

## Installation

The following tools and libraries are required to use this CRUD Python module:

### Required Tools

- Python 3 (Version 3.13 or higher)
  - Rationale: Core programming language providing object-oriented programming capabilities and extensive library support
  - Installation: Download from python.org or use system package manager

- PyMongo (Latest stable version)
  - Rationale: Official MongoDB driver for Python, providing comprehensive database operation support and connection management
  - Installation: pip3 install pymongo

- MongoDB (Version 8 or higher)
  - Rationale: Document-oriented database system ideal for flexible data storage and retrieval of animal shelter records
  - Installation: Download MongoDB Community Edition from mongodb.com

- Jupyter Notebook (Latest version)
  - Rationale: Interactive development environment enabling iterative testing and documentation of CRUD operations
  - Installation: pip3 install jupyter

### Installation Commands

```bash
# Create a virtual environment
python3 -m venv  .venv            # macos or linux
python -m venv .venv.             # windows

# Activate the virtual environment
source .venv/bin/activate.        # macos or linux
.\.venv\Scripts\Activate.ps1.     # windows (PowerShell)
.venv\Script\activate.bat.        # windows (cmd.exe)

# Install project requirements
pip3 install -r requirements.txt

# Verify MongoDB is running
mongosh --eval "db.runCommand('ismaster')"
```

## Usage

This section demonstrates how the CRUD Python module works and provides examples of its functionality.

### CRUD Module Code Example

```python
# Import the CRUD module
from CRUD_Python_Module import AnimalShelter

# Instantiate the AnimalShelter class
shelter = AnimalShelter()

# Example: Create a new animal record
new_animal = {
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

# Insert the new record
create_result = shelter.create(new_animal)
print(f"Create operation successful: {create_result}")

# Example: Read animal records
# Query for all dogs
query_dogs = {"animal_type": "Dog"}
dog_results = shelter.read(query_dogs)
print(f"Found {len(dog_results)} dog records")

# Query for a specific animal by animal_id
query_id = {"animal_id": "TestID001"}
id_results = shelter.read(query_id)
print(f"Found {len(id_results)} matching record(s)")

# Example: Update animal records
# Update a single field
update_count = shelter.update(
    {"animal_id": "TestID001"},
    {"outcome_type": "Adoption"}
)
print(f"Updated {update_count} record(s)")

# Update with explicit $set operator
update_count = shelter.update(
    {"animal_id": "TestID001"},
    {"$set": {"location_lat": 30.2672}}
)
print(f"Updated {update_count} record(s)")

# Example: Delete animal records
# Delete a single record by animal_id
delete_count = shelter.delete({"animal_id": "TestID001"})
print(f"Deleted {delete_count} record(s)")

# Delete multiple records by criteria
delete_count = shelter.delete({"outcome_type": "Transfer"})
print(f"Deleted {delete_count} transfer record(s)")
```

### Dashboard Usage

The interactive dashboard provides a web-based interface for identifying rescue candidates:

**Starting the Dashboard:**

```python
# Open ProjectTwoDashboard.ipynb in Jupyter Notebook
# Run the cell - dashboard opens in new browser tab
```

**Authentication:**

- Username: `admin`
- Password: `grazioso2024`

**Using Rescue Filters:**

1. **Water Rescue** - Filters for Labrador, Chesapeake Bay Retriever, Newfoundland (Intact Female, 26-156 weeks)
2. **Mountain/Wilderness** - Filters for German Shepherd, Alaskan Malamute, Old English Sheepdog, Siberian Husky, Rottweiler (Intact Male, 26-156 weeks)
3. **Disaster/Tracking** - Filters for Doberman Pinscher, German Shepherd, Golden Retriever, Bloodhound, Rottweiler (Intact Male, 20-300 weeks)
4. **Reset** - Shows all animals

**Dashboard Features:**

- **Interactive Table**: Sort, paginate, and select animals
- **Geolocation Map**: View selected animal's location with breed tooltip and name popup
- **Outcome Chart**: Pie chart showing distribution of outcome types for filtered data
- **Row Highlighting**: Selected row highlighted in pale green for easy identification

### Tests

Testing for this CRUD module is performed using both:
1. **Unit Tests** - Python unittest suite in `tests/` directory (recommended for development)
2. **Interactive Tests** - ProjectOneTestScript.ipynb Jupyter Notebook (for demonstration)

#### Running Unit Tests

The project includes a comprehensive unittest suite with 29 tests covering all CRUD operations:

**With Live MongoDB Database (default):**
```bash
# Requires MongoDB running on localhost:27017 with aacuser credentials

# Run all tests
python -m unittest discover -s tests -p "test_*.py"

# Run with verbose output
python -m unittest discover -s tests -p "test_*.py" -v

# Run specific test file
python -m unittest tests.test_crud

# Run specific test class
python -m unittest tests.test_crud.TestCreate

# Run specific test method
python -m unittest tests.test_crud.TestCreate.test_create_with_valid_data
```

**With Mock Database (for CI/offline testing):**
```bash
# No MongoDB connection required - uses mocked database

# Run all tests with mock
USE_MOCK_DB=true python -m unittest discover -s tests -p "test_*.py"

# Run with verbose output
USE_MOCK_DB=true python -m unittest discover -s tests -p "test_*.py" -v
```
*Note: Mock database testing is currently in development. All 29 tests pass with live MongoDB.*

**Test Structure:**
- `tests/test_crud.py` - All CRUD operation tests (17 tests: Create, Read, Update, Delete)
- `tests/test_authentication.py` - Authentication and connection tests (4 tests)
- `tests/test_error_handling.py` - Error handling and edge case tests (8 tests)
- `tests/fixtures/test_data.py` - Shared test data and base test classes

**Total: 29 tests, all passing**

**Test Coverage:**
```bash
# Run tests with coverage analysis
pip install coverage
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report -m CRUD_Python_Module.py

# Generate HTML coverage report
coverage html
# Open htmlcov/index.html in browser
```

**Current Coverage: 77%** of CRUD_Python_Module.py

#### Running Integration Tests

The project includes 7 integration tests for dashboard workflows that validate the complete data pipeline from database to filters to visualizations.

**Running integration tests:**
```bash
# Run all integration tests
python -m unittest discover -s integration -p "test_*.py"

# Run with verbose output
python -m unittest discover -s integration -p "test_*.py" -v

# Run specific test file
python -m unittest integration.test_dashboard_workflows

# Run specific test class
python -m unittest integration.test_dashboard_workflows.TestPrimaryWorkflow
```

**Test Structure:**
- `integration/test_dashboard_workflows.py` - Complete workflow integration tests (7 tests)
  - Primary workflow: Reset → Water → Mountain → Disaster (2 tests)
  - Authentication flow with state transitions (2 tests)
  - Data normalization pipeline from raw to filtered (1 test)
  - Category bucketing for chart visualization (1 test)
  - Coordinate validation for map rendering (1 test)

**Total: 7 integration tests, all passing**

**What Integration Tests Cover:**
- ✅ Complete data pipeline workflows (Database → Normalization → Filtering)
- ✅ Primary filter sequence: Reset → Water → Mountain → Disaster
- ✅ Filter results composition (correct sex, breed, age criteria)
- ✅ Authentication flow and session state management
- ✅ Data normalization end-to-end (raw AAC data → normalized fields)
- ✅ Category bucketing for charts (top-N + "Other")
- ✅ Coordinate validation for map rendering
- ✅ Mock data used (no database dependencies in CI)

**What Is NOT Tested (and Why):**

Integration tests focus on **data pipeline correctness**, not UI rendering. The following are intentionally excluded due to complexity vs. value trade-offs:

- **Dash Callback I/O Simulation**: Requires complex mocking of Dash context, callback_context, and State/Input/Output decorators. Manual testing provides better coverage for UI interactions.
- **Dashboard Layout Rendering**: Component composition is declarative and static; visual testing is more appropriate than programmatic assertions.
- **Map Marker Positioning**: Leaflet map behavior is tested by the library itself; we validate coordinate data correctness instead.
- **Chart Visual Appearance**: Plotly chart rendering is validated by the library; we test data transformation correctness.

**Testing Strategy:**
- **Unit Tests (129 tests)**: Test individual functions in isolation (filters, normalization, bucketing, auth)
- **Integration Tests (7 tests)**: Test complete workflows end-to-end with mock data
- **Manual Testing**: Validate UI rendering, interactivity, and user experience in Jupyter

For detailed rationale on integration test scope, see the **Phase 6: Testing & Validation** section in [SUMMARY.md](SUMMARY.md).

### Code Quality & Linting

This project uses **ruff** for fast Python linting and code quality checks.

**Running the linter:**
```bash
# Check all Python files for issues
ruff check .

# Check specific files
ruff check CRUD_Python_Module.py tests/

# Auto-fix issues where possible
ruff check --fix .

# Show detailed output
ruff check --output-format=full .
```

**Linting Configuration:**
- Configuration file: `ruff.toml`
- Target: Python 3.13
- Line length: 79 characters (PEP 8)
- Enabled rules: pycodestyle, pyflakes, isort, pep8-naming, pyupgrade, flake8-bugbear

**Pre-commit checks:**
```bash
# Run linter before committing
ruff check .

# Run tests before committing
python -m unittest discover -s tests -p "test_*.py"
```

### Continuous Integration (CI/CD)

This project uses GitHub Actions for automated testing and code quality checks.

**CI Workflows:**

1. **On Push** (`.github/workflows/on-push.yml`)
   - Runs on every push to any branch
   - Fast feedback loop for development
   - Steps:
     - Lint code with ruff
     - Run all unit tests

2. **On Pull Request** (`.github/workflows/on-pr.yml`)
   - Runs on PR to main branch
   - Comprehensive validation before merge
   - Steps:
     - Lint code with ruff
     - Run all unit tests
     - Generate coverage report
     - Upload coverage to Codecov

**CI Environment:**
- Python 3.13
- Ubuntu latest
- MongoDB 8.0 service container
- Pip caching enabled for faster builds
- All tests run with live MongoDB connection

**Required GitHub Secrets:**

The CI/CD workflows require two secrets to be configured in the repository:

1. Navigate to: **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:
   - `MONGODB_USER` - MongoDB username for testing (e.g., `aacuser`)
   - `MONGODB_PASSWORD` - MongoDB password for testing

**Why Secrets?**
- Passwords never appear in code or workflow files
- Easy to rotate credentials without code changes
- Follows security best practices
- Secrets are encrypted at rest in GitHub

**Note:** Workflows will fail with authentication errors if secrets are not configured.

**Viewing CI Results:**
- Check the "Actions" tab in GitHub repository
- PR checks must pass before merging to main
- Coverage reports available in PR comments

#### Interactive Test Script Example

```python
# Import the CRUD module
from CRUD_Python_Module import AnimalShelter

# Instantiate an instance of the class
shelter = AnimalShelter()

# Test Create functionality - insert a new record
test_animal = {
    "animal_id": "TEST001",
    "name": "Test Animal",
    "animal_type": "Dog", 
    "breed": "Test Breed",
    "age_upon_outcome": "2 years"
}

create_result = shelter.create(test_animal)
print(f"Create test result: {create_result}")

# Test Read functionality - query records
read_results = shelter.read({"animal_type": "Dog"})
print(f"Read test found {len(read_results)} dog records")

# Test Update functionality - modify a record
update_count = shelter.update(
    {"animal_id": "TEST001"},
    {"outcome_type": "Adoption"}
)
print(f"Update test modified {update_count} record(s)")

# Test Delete functionality - remove a record
delete_count = shelter.delete({"animal_id": "TEST001"})
print(f"Delete test removed {delete_count} record(s)")
```

### Screenshots

#### Module Setup and Import

![Module Setup and Import](./screenshots/module_setup.jpg)

#### Test Data Setup

![Test Data Setup](./screenshots/test_data_setup.jpg)

#### Creation Operation – Valid data and None Data

![Creation Operation – Valid data and None Data](./screenshots/creation_operation_1.jpg)

#### Creation Operation – Duplicate Entry Handling and Empty Animal ID

![Creation Operation – Duplicate Entry Handling and Empty Animal ID](./screenshots/creation_operation_2.jpg)

#### Creation Operation – Handling Empty Object

![Creation Operation – Handling Empty Object](./screenshots/creation_operation_3.jpg)

#### Read Operation – Find Record

![Read Operation – Find Record](./screenshots/read_operation_1.jpg)

#### Read Operation – Empty Result

![Read Operation – Empty Result](./screenshots/read_operation_2.jpg)

#### Read Operation – Error Handling

![Read Operation – Error Handling](./screenshots/read_operation_3.jpg)

#### Update Operation with Valid Query and Update Data (Explicit $set)

![Update Operation with Valid Query and Update Data (Explicit $set)](./screenshots/update_operation_1.jpg)

#### Update Operation without Operator (Auto-wrap in $set)

![Update Operation without Operator (Auto-wrap in $set)](./screenshots/update_operation_2.jpg)

#### Update Operation with None Query (Error Handling Test)

![Update Operation with None Query (Error Handling Test)](./screenshots/update_operation_3.jpg)

#### Update Operation with None Update Data (Error Handling Test)

![Update Operation with None Update Data (Error Handling Test)](./screenshots/update_operation_4.jpg)

#### Update Operation with Non-Matching Query (No Documents Modified)

![Update Operation with Non-Matching Query (No Documents Modified)](./screenshots/update_operation_5.jpg)

#### Delete Operation with Valid Query

![Delete Operation with Valid Query](./screenshots/delete_operation_1.jpg)

#### Delete Operation with None Query (Error Handling Test)

![Delete Operation with None Query (Error Handling Test)](./screenshots/delete_operation_2.jpg)

#### Delete Operation with Non-Matching Query (No Documents Deleted)

![Delete Operation with Non-Matching Query (No Documents Deleted)](./screenshots/delete_operation_3.jpg)

#### Delete Multiple Documents

![Delete Multiple Documents](./screenshots/delete_operation_4.jpg)

#### Test Teardown - Cleanup Test Data

![Test Teardown - Cleanup Test Data](./screenshots/test_teardown.jpg)

## Features

**Backend (CRUD Module):**

- ✅ Create, Read, Update, Delete operations for MongoDB
- ✅ Comprehensive error handling and validation
- ✅ 77% test coverage with 158 unit tests

**Dashboard (Interactive Web UI):**

- ✅ Authentication gate with username/password
- ✅ Four rescue type filters (Water, Mountain, Disaster, Reset)
- ✅ Interactive data table with sorting and pagination
- ✅ Geolocation map with animal location markers
- ✅ Outcome type distribution pie chart
- ✅ Row highlighting for selected animals
- ✅ Responsive empty states

**Data Processing:**

- ✅ Age normalization (parse to weeks from years/months/days)
- ✅ Sex and intact status parsing
- ✅ Coordinate validation for mapping
- ✅ Breed matching with multi-breed support
- ✅ Category bucketing for chart readability

**Testing & CI/CD:**

- ✅ 158 unit tests (77% coverage)
- ✅ 7 integration tests (workflow validation)
- ✅ GitHub Actions CI/CD with automated testing
- ✅ Ruff linting with PEP 8 compliance

## Contact

Your name: Rick Goshen
Email: [richard.goshen@snhu.edu](mailto: richard.goshen@snhu.edu)
