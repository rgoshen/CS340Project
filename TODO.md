# Project One: Grazioso Rescue Finder - Development Tracking

## CRUD Operations Implementation
- [x] Create Method - COMPLETED in Module Four
- [x] Read Method - COMPLETED in Module Four
- [x] Update Method - COMPLETED on feature/update-operation
- [x] Delete Method - COMPLETED on feature/delete-operation

## Testing Implementation
- [x] Create test cell - COMPLETED in Module Four
- [x] Read test cell - COMPLETED in Module Four
- [x] Update test cells - COMPLETED (Tests 10-14)
- [x] Delete test cells - COMPLETED (Tests 15-18)

## Documentation
- [x] README: Update to include all four CRUD operations - COMPLETED
- [x] README: PyMongo driver explanation - COMPLETED
- [x] Update method docstring - COMPLETED
- [x] Delete method docstring - COMPLETED
- [x] Code comments for update method - COMPLETED
- [x] Code comments for delete method - COMPLETED

## Development Progress
- [x] Create feature/update-operation branch
- [x] Implement update() method with modified_count return
- [x] Add comprehensive error handling to update()
- [x] Test update() method in Jupyter notebook
- [x] Merge update operation to main
- [x] Create feature/delete-operation branch
- [x] Implement delete() method with deleted_count return
- [x] Add comprehensive error handling to delete()
- [x] Test delete() method in Jupyter notebook
- [x] Merge delete operation to main
- [x] Verify PEP 8 compliance for all new code - COMPLETED
- [x] Update README with complete documentation - COMPLETED

## Project One Status: ✅ COMPLETE

All CRUD operations implemented, tested, and documented according to requirements.

---

# Project Two: Interactive Dashboard - Development Tracking

## Phase 0: Foundation - Testing & CI/CD Infrastructure

### Test Conversion (ProjectOneTestScript.ipynb → unittest)
- [x] Create tests/ directory structure
  - [x] Create tests/__init__.py
  - [x] Create tests/test_crud.py (all CRUD operations)
  - [x] Create tests/test_authentication.py
  - [x] Create tests/test_error_handling.py
  - [x] Create tests/fixtures/ directory
  - [x] Create tests/fixtures/__init__.py
  - [x] Create tests/fixtures/test_data.py
- [x] Create test_crud.py with all CRUD operation tests
  - [x] Create TestCreate class with setUp/tearDown
    - [x] Test create with valid data
    - [x] Test create with None data
    - [x] Test create with duplicate animal_id
    - [x] Test create with empty animal_id
    - [x] Test create with empty object
  - [x] Create TestRead class with setUp/tearDown
    - [x] Test read with valid query
    - [x] Test read with non-matching query
    - [x] Test read with None query
  - [x] Create TestUpdate class with setUp/tearDown
    - [x] Test update with explicit $set operator
    - [x] Test update without operator (auto-wrap)
    - [x] Test update with None query
    - [x] Test update with None update_data
    - [x] Test update with non-matching query
  - [x] Create TestDelete class with setUp/tearDown
    - [x] Test delete with valid query
    - [x] Test delete with None query
    - [x] Test delete with non-matching query
    - [x] Test delete multiple documents
- [x] Create test_authentication.py
  - [x] Create TestAuthentication class
  - [x] Test valid authentication with correct credentials
  - [x] Test invalid authentication with wrong credentials
  - [x] Test database and collection access
  - [x] Test MongoDB connection timeout handling
- [x] Create test_error_handling.py
  - [x] Create TestErrorHandling class
  - [x] Test create with invalid data types (string, int, list, bool)
  - [x] Test read with invalid data types (string, int, list, bool)
  - [x] Test create with malformed documents (nested structures, special chars, unicode)
  - [x] Test update with invalid data types
  - [x] Test delete with invalid data types
  - [x] Test special characters in queries
  - [x] Test very large query results
- [x] Create test fixtures (tests/fixtures/test_data.py)
  - [x] Create sample_animal_data dictionary
  - [x] Create invalid_data_samples list
  - [x] Create query_samples dictionary
  - [x] Create BaseTestCase class with shared setUp/tearDown
  - [x] Add helper methods for test data creation and cleanup
- [x] Add mock data for offline testing
  - [x] Install unittest.mock for MongoDB mocking
  - [x] Create MockMongoClient in fixtures
  - [x] Create MockDatabase in fixtures
  - [x] Create MockCollection in fixtures
  - [x] Ensure tests can run without live database connection
  - [x] Add environment variable to toggle mock vs real DB
- [x] Verify test discovery and execution
  - [x] Run: python -m unittest discover -s tests -p "test_*.py"
  - [x] Verify all tests pass with live database (29/29 passing)
  - [x] Verify all tests pass with mocked database (optional - deferred to CI)
  - [x] Check test coverage with coverage.py - 77% coverage achieved
  - [x] Document test execution in README

### CI/CD Setup (GitHub Actions)
- [x] Create .github/workflows/ directory
- [x] Implement push workflow (linting + unit tests only)
  - [x] Create .github/workflows/on-push.yml
  - [x] Configure Python 3.13 environment
  - [x] Add pip cache configuration
  - [x] Add ruff linter step (fail on errors)
  - [x] Add unit test execution step
  - [x] Configure to run on push to any branch
- [x] Implement pull_request workflow (linting + unit + coverage)
  - [x] Create .github/workflows/on-pr.yml
  - [x] Configure Python 3.13 environment
  - [x] Add pip cache configuration
  - [x] Add ruff linter step (fail on errors)
  - [x] Add unit test execution step
  - [x] Add coverage reporting step
  - [x] Configure to run on PR to main branch
- [x] Add ruff configuration
  - [x] Create ruff.toml
  - [x] Configure line length (79 for PEP 8)
  - [x] Configure target Python version (3.13)
  - [x] Select linting rules (pycodestyle, pyflakes, isort, etc.)
- [x] Test CI/CD workflows locally
  - [x] Install ruff: pip install ruff
  - [x] Run ruff check on CRUD_Python_Module.py and tests
  - [x] Verify unit tests pass in isolation (29/29 passing)
  - [x] Fix all linting issues
- [x] Document CI/CD in README
  - [x] Document CI workflows (push vs PR)
  - [x] Explain CI environment and configuration
  - [x] Document how to view CI results
  - [x] Document GitHub Secrets requirement for MongoDB credentials
  - [ ] Add CI badge to README (after first successful run)
- [x] Configure MongoDB service in CI workflows with GitHub Secrets
  - [x] Add MongoDB 8.0 service container to workflows
  - [x] Create user creation step using secrets
  - [x] Update workflows to use MONGODB_USER and MONGODB_PASSWORD secrets
  - [x] Document security rationale in SUMMARY.md

### Phase 0 Branch Strategy
- [x] Create feature/phase0-testing-infrastructure branch
- [x] Commit test conversion changes incrementally
- [x] Merge testing infrastructure to main (PR #12)
- [x] Create feature/phase0-ci-setup branch
- [x] Commit CI/CD configuration changes incrementally
- [x] Configure GitHub Secrets in repository settings
  - [x] Add MONGODB_USER secret (e.g., aacuser)
  - [x] Add MONGODB_PASSWORD secret (e.g., SNHU1234)
- [x] Install mongosh in CI workflows
- [x] Verify CI passes after mongosh installation
- [x] Merge CI/CD setup to main (PR #13)
- [x] Ensure CI is green before proceeding to dashboard work

## Phase 1: Data Normalization & Helper Functions
- [x] Add CI and project badges to README
- [x] Implement parse_age_to_weeks() function
  - [x] Handle "X weeks" format
  - [x] Handle "X months" format (multiply by 4.345)
  - [x] Handle "X years" format (multiply by 52.143)
  - [x] Handle "X days" format (divide by 7)
  - [x] Handle edge cases: malformed strings, nulls, negative values, zero
  - [x] Add comprehensive docstring with examples
  - [x] Write 14 comprehensive unit tests (all passing)
  - [x] Refactor to use match/case instead of if/elif
- [x] Implement normalize_sex_intact() function
  - [x] Parse sex_upon_outcome into separate sex and intact_status fields
  - [x] Handle case-insensitive variations
  - [x] Handle whitespace variations
  - [x] Handle null/empty values
  - [x] Return standardized values (Neutered/Spayed/Intact/Unknown)
  - [x] Write 11 comprehensive unit tests (all passing)
- [x] Implement validate_coordinates() function
  - [x] Coerce location_lat and location_long to floats
  - [x] Validate latitude range [-90, 90]
  - [x] Validate longitude range [-180, 180]
  - [x] Return valid_coords boolean flag
  - [x] Handle NaN and non-numeric values
  - [x] Write 9 comprehensive unit tests (all passing)
- [x] Implement breed_matches_rescue_type() function
  - [x] Implement case-insensitive matching
  - [x] Handle multi-breed strings with "Mix"
  - [x] Handle multi-breed strings with "/" separator
  - [x] Handle substring matching for all separators
  - [x] Add docstring with rescue type breed lists
  - [x] Use match/case for rescue type selection
  - [x] Write 12 comprehensive unit tests (all passing)
- [x] Implement bucket_categories() function
  - [x] Create Top N categories (default N=10)
  - [x] Group remaining as "Other"
  - [x] Implement deterministic tie-breaking (alphabetical)
  - [x] Make N configurable parameter
  - [x] Write 9 comprehensive unit tests (all passing)
- [ ] Create normalize_dataframe() function (deferred to Phase 2)
  - [ ] Apply age parsing to create age_weeks column
  - [ ] Apply sex/intact normalization
  - [ ] Apply coordinate validation to create valid_coords flag
  - [ ] Cache normalized DataFrame at module level
  - [ ] Add error handling for missing columns

## Phase 2: Rescue Type Filter Logic
- [ ] Implement water_rescue_filter() function
  - [ ] Filter breeds: Labrador Retriever Mix, Chesapeake Bay Retriever, Newfoundland
  - [ ] Filter sex: Intact Female
  - [ ] Filter age: 26-156 weeks
  - [ ] Return filtered DataFrame
  - [ ] Add docstring with filter criteria
- [ ] Implement mountain_rescue_filter() function
  - [ ] Filter breeds: German Shepherd, Alaskan Malamute, Old English Sheepdog, Siberian Husky, Rottweiler
  - [ ] Filter sex: Intact Male
  - [ ] Filter age: 26-156 weeks
  - [ ] Return filtered DataFrame
  - [ ] Add docstring with filter criteria
- [ ] Implement disaster_rescue_filter() function
  - [ ] Filter breeds: Doberman Pinscher, German Shepherd, Golden Retriever, Bloodhound, Rottweiler
  - [ ] Filter sex: Intact Male
  - [ ] Filter age: 20-300 weeks
  - [ ] Return filtered DataFrame
  - [ ] Add docstring with filter criteria
- [ ] Implement reset_filter() function
  - [ ] Return full normalized DataFrame (no filtering)
  - [ ] Add docstring
- [ ] Create apply_filter() dispatcher function
  - [ ] Map filter type string to appropriate filter function
  - [ ] Handle invalid filter types gracefully
  - [ ] Return filtered DataFrame

## Phase 3: Authentication Gate
- [ ] Design authentication layout
  - [ ] Create username input field (dcc.Input)
  - [ ] Create password input field (dcc.Input, type='password')
  - [ ] Create submit button (html.Button)
  - [ ] Add error message placeholder (html.Div)
  - [ ] Style login form for centered, professional appearance
- [ ] Add authentication storage
  - [ ] Create dcc.Store component for authentication state
  - [ ] Initialize as not authenticated
- [ ] Implement authentication callback
  - [ ] Input: submit button clicks, username, password
  - [ ] Validate credentials (simple check for coursework)
  - [ ] Output: authentication state to dcc.Store
  - [ ] Output: error message if login fails
- [ ] Implement dashboard visibility callback
  - [ ] Input: authentication state from dcc.Store
  - [ ] Output: toggle login view vs dashboard view
  - [ ] Return login layout when not authenticated
  - [ ] Return full dashboard when authenticated

## Phase 4: Dashboard Layout (View)
- [ ] Implement branding header
  - [ ] Create html.A link wrapper for logo
  - [ ] Embed Grazioso-Salvare-Logo.png with base64 encoding
  - [ ] Add alt text: "Grazioso Salvare Logo"
  - [ ] Add creator identification: "Dashboard by Rick Goshen"
  - [ ] Add project context: "CS 340 - Client/Server Development"
  - [ ] Separate header with html.Hr()
  - [ ] Apply accessible styling (proper contrast, font sizes)
- [ ] Implement filter controls
  - [ ] Create dcc.RadioItems component with id='filter-type'
  - [ ] Add 4 options: Water Rescue, Mountain/Wilderness Rescue, Disaster/Tracking, Reset
  - [ ] Set default value to 'reset'
  - [ ] Add clear labels with rescue type descriptions
  - [ ] Add help text explaining each filter
  - [ ] Style for readability and spacing
- [ ] Enhance data table (keep existing features)
  - [ ] Verify sorting is enabled (sort_action='native')
  - [ ] Verify pagination is enabled (page_action='native')
  - [ ] Verify single-row selection (row_selectable='single')
  - [ ] Add tooltips for long text fields
  - [ ] Ensure consistent cell styling
  - [ ] Keep selected_rows=[0] default
- [ ] Update map component
  - [ ] Modify to use derived_virtual_data (filtered data)
  - [ ] Add coordinate validation before rendering markers
  - [ ] Add graceful error handling for no valid coordinates
  - [ ] Add empty state message when no data to display
  - [ ] Keep existing tooltip and popup functionality
  - [ ] Ensure map updates on filter changes
- [ ] Implement second chart component
  - [ ] Create new html.Div container for chart
  - [ ] Add clear title describing chart purpose
  - [ ] Choose chart type: pie or bar (outcome_type distribution)
  - [ ] Plan for category bucketing (Top 10 + Other)
  - [ ] Add clear legend and axis labels
  - [ ] Ensure chart reflects filtered data
  - [ ] Style for readability (proper sizing, colors)

## Phase 5: Controller (Callbacks)
- [ ] Implement filter callback (update_dashboard)
  - [ ] Input: filter-type radio button value
  - [ ] Get normalized DataFrame from cache
  - [ ] Apply appropriate filter function via dispatcher
  - [ ] Output: filtered data to datatable-id.data
  - [ ] Add error handling for filter failures
  - [ ] Add logging for debugging
- [ ] Implement chart callback (update_graphs)
  - [ ] Input: datatable-id.derived_virtual_data
  - [ ] Extract filtered/sorted data from input
  - [ ] Apply category bucketing for chart data
  - [ ] Create pie or bar chart with plotly.express
  - [ ] Add title indicating current filter state
  - [ ] Output: dcc.Graph component to graph-id.children
  - [ ] Handle empty data gracefully
- [ ] Refine map callback (update_map)
  - [ ] Keep existing inputs: derived_virtual_data, derived_virtual_selected_rows
  - [ ] Add coordinate validation before creating markers
  - [ ] Handle case where selected row has invalid coordinates
  - [ ] Add fallback message when no valid coordinates
  - [ ] Keep existing marker tooltip and popup
  - [ ] Ensure map centers on selected animal location
- [ ] Verify style callback (update_styles)
  - [ ] Confirm existing cell highlighting works with filtered data
  - [ ] No changes needed if working correctly

## Phase 6: Testing & Validation
- [ ] Manual testing workflow
  - [ ] Test authentication gate (successful and failed login)
  - [ ] Test Reset filter shows all animals
  - [ ] Test Water Rescue filter and verify row count
  - [ ] Test Mountain/Wilderness Rescue filter and verify row count
  - [ ] Test Disaster/Tracking filter and verify row count
  - [ ] Verify each filter shows correct breeds/sex/age ranges
  - [ ] Test table row selection updates map marker
  - [ ] Test table row selection updates map center
  - [ ] Verify chart updates with each filter change
  - [ ] Test pagination with filtered data
  - [ ] Test sorting with filtered data
- [ ] Data quality testing
  - [ ] Test age parsing with sample records from each format
  - [ ] Test breed matching with multi-breed strings
  - [ ] Test coordinate validation with edge cases
  - [ ] Test with null/missing values in all normalized fields
  - [ ] Verify category bucketing produces Top N + Other correctly
- [ ] UI/UX validation
  - [ ] Verify logo displays with proper alt text
  - [ ] Check all labels are clear and descriptive
  - [ ] Verify font sizes are legible
  - [ ] Check color contrast meets accessibility standards
  - [ ] Verify consistent spacing throughout dashboard
  - [ ] Test responsive layout (if applicable)
  - [ ] Verify all interactive elements provide feedback

## Phase 7: Documentation & Cleanup
- [ ] Code documentation
  - [ ] Add comprehensive module-level docstring to dashboard cell
  - [ ] Document all helper functions with docstrings
  - [ ] Add inline comments explaining filter criteria
  - [ ] Document callback interactions and data flow
  - [ ] Explain data normalization decisions in comments
- [ ] Update README.md
  - [ ] Add Project Two overview section
  - [ ] Document how to run the dashboard (jupyter notebook command)
  - [ ] Explain the four filter types and their criteria
  - [ ] Add screenshot placeholders for dashboard views
  - [ ] Document authentication credentials for coursework
- [ ] Update TODO.md
  - [ ] Mark all completed Phase 1-7 tasks as done
  - [ ] Document any known issues or limitations
  - [ ] Add future enhancement ideas (optional)
- [ ] Final code review
  - [ ] Verify all code is in single Jupyter cell
  - [ ] Confirm CRUD module is not modified (read-only)
  - [ ] Verify no original data fields are altered (non-destructive)
  - [ ] Check for any TODO or FIXME comments left in code
  - [ ] Verify app.run() uses jupyter_mode="tab" or "inline"
  - [ ] Remove any debug print statements
  - [ ] Verify PEP 8 compliance in new functions

## Project Two Status: 🚧 IN PROGRESS

Dashboard implementation following single-cell architecture with MVC pattern.
