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
- [ ] Create tests/ directory structure
  - [ ] Create tests/__init__.py
  - [ ] Create tests/test_crud.py (all CRUD operations)
  - [ ] Create tests/test_authentication.py
  - [ ] Create tests/test_error_handling.py
  - [ ] Create tests/fixtures/ directory
  - [ ] Create tests/fixtures/__init__.py
  - [ ] Create tests/fixtures/test_data.py
- [ ] Create test_crud.py with all CRUD operation tests
  - [ ] Create TestCreate class with setUp/tearDown
    - [ ] Test create with valid data
    - [ ] Test create with None data
    - [ ] Test create with duplicate animal_id
    - [ ] Test create with empty animal_id
    - [ ] Test create with empty object
  - [ ] Create TestRead class with setUp/tearDown
    - [ ] Test read with valid query
    - [ ] Test read with non-matching query
    - [ ] Test read with None query
  - [ ] Create TestUpdate class with setUp/tearDown
    - [ ] Test update with explicit $set operator
    - [ ] Test update without operator (auto-wrap)
    - [ ] Test update with None query
    - [ ] Test update with None update_data
    - [ ] Test update with non-matching query
  - [ ] Create TestDelete class with setUp/tearDown
    - [ ] Test delete with valid query
    - [ ] Test delete with None query
    - [ ] Test delete with non-matching query
    - [ ] Test delete multiple documents
- [ ] Create test_authentication.py
  - [ ] Create TestAuthentication class
  - [ ] Test valid authentication with correct credentials
  - [ ] Test invalid authentication with wrong credentials
  - [ ] Test connection without authentication
  - [ ] Test MongoDB connection timeout handling
- [ ] Create test_error_handling.py
  - [ ] Create TestErrorHandling class
  - [ ] Test create with invalid data types (string, int, list, bool)
  - [ ] Test read with invalid data types (string, int, list, bool)
  - [ ] Test create with malformed documents (nested structures, special chars, unicode)
  - [ ] Test database connection failures
  - [ ] Test cursor iteration edge cases
- [ ] Create test fixtures (tests/fixtures/test_data.py)
  - [ ] Create sample_animal_data dictionary
  - [ ] Create invalid_data_samples list
  - [ ] Create query_samples dictionary
  - [ ] Create BaseTestCase class with shared setUp/tearDown
  - [ ] Add helper methods for test data creation and cleanup
- [ ] Add mock data for offline testing
  - [ ] Install unittest.mock for MongoDB mocking
  - [ ] Create MockMongoClient in fixtures
  - [ ] Create MockDatabase in fixtures
  - [ ] Create MockCollection in fixtures
  - [ ] Ensure tests can run without live database connection
  - [ ] Add environment variable to toggle mock vs real DB
- [ ] Verify test discovery and execution
  - [ ] Run: python -m unittest discover -s tests -p "test_*.py"
  - [ ] Verify all tests pass with live database
  - [ ] Verify all tests pass with mocked database
  - [ ] Check test coverage with coverage.py (optional)
  - [ ] Document test execution in README

### CI/CD Setup (GitHub Actions)
- [ ] Create .github/workflows/ directory
- [ ] Implement push workflow (linting + unit tests only)
  - [ ] Create .github/workflows/on-push.yml
  - [ ] Configure Python 3.13 environment
  - [ ] Add pip cache configuration
  - [ ] Add ruff linter step (fail on errors)
  - [ ] Add unit test execution step
  - [ ] Ensure no network/DB calls in unit tests
  - [ ] Configure to run on push to any branch
- [ ] Implement pull_request workflow (linting + unit + integration)
  - [ ] Create .github/workflows/on-pr.yml
  - [ ] Configure Python 3.13 environment
  - [ ] Add pip cache configuration
  - [ ] Add ruff linter step (fail on errors)
  - [ ] Add unit test execution step
  - [ ] Add integration test execution step (mocked DB)
  - [ ] Configure to run on PR to main branch
- [ ] Add ruff configuration
  - [ ] Create ruff.toml or pyproject.toml
  - [ ] Configure line length (79 for PEP 8)
  - [ ] Configure target Python version (3.13)
  - [ ] Select linting rules
- [ ] Test CI/CD workflows locally
  - [ ] Install ruff: pip install ruff
  - [ ] Run ruff check on CRUD_Python_Module.py
  - [ ] Verify unit tests pass in isolation
  - [ ] Fix any linting issues
- [ ] Document CI/CD in README
  - [ ] Add CI badge to README
  - [ ] Document how to run tests locally
  - [ ] Explain CI workflow differences (push vs PR)

### Phase 0 Branch Strategy
- [ ] Create feature/phase0-testing-infrastructure branch
- [ ] Commit test conversion changes incrementally
- [ ] Create feature/phase0-ci-setup branch
- [ ] Commit CI/CD configuration changes
- [ ] Merge Phase 0 branches to main before starting Phase 1
- [ ] Ensure CI is green before proceeding to dashboard work

## Phase 1: Data Normalization & Helper Functions
- [ ] Implement parse_age_to_weeks() function
  - [ ] Handle "X weeks" format
  - [ ] Handle "X months" format (multiply by 4.345)
  - [ ] Handle "X years" format (multiply by 52.143)
  - [ ] Handle "X days" format (divide by 7)
  - [ ] Handle edge cases: malformed strings, nulls, negative values, zero
  - [ ] Add comprehensive docstring with examples
- [ ] Implement normalize_sex_intact() function
  - [ ] Parse sex_upon_outcome into separate sex and intact_status fields
  - [ ] Handle case-insensitive variations
  - [ ] Handle whitespace variations
  - [ ] Handle null/empty values
  - [ ] Return standardized values (Neutered/Spayed/Intact/Unknown)
- [ ] Implement breed_matches_rescue_type() function
  - [ ] Implement case-insensitive matching
  - [ ] Handle multi-breed strings with "Mix"
  - [ ] Handle multi-breed strings with "/" separator
  - [ ] Handle multi-breed strings with "," separator
  - [ ] Make non-ASCII safe
  - [ ] Add docstring with rescue type breed lists
- [ ] Implement validate_coordinates() function
  - [ ] Coerce location_lat and location_long to floats
  - [ ] Validate latitude range [-90, 90]
  - [ ] Validate longitude range [-180, 180]
  - [ ] Return valid_coords boolean flag
  - [ ] Handle NaN and non-numeric values
- [ ] Implement bucket_categories() function
  - [ ] Create Top N categories (default N=10)
  - [ ] Group remaining as "Other"
  - [ ] Implement deterministic tie-breaking (alphabetical)
  - [ ] Make N configurable parameter
- [ ] Create normalize_dataframe() function to apply all normalizations
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
