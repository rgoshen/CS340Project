# Manual Testing Plan - Grazioso Salvare Dashboard

## Overview
This document provides a comprehensive checklist for manually testing the Grazioso Salvare Animal Rescue Dashboard. Complete each section in order, checking off items as you verify functionality.

## Prerequisites

- [ ] MongoDB is running on localhost:27017
- [ ] Database `aac` has the `animals` collection populated with AAC data
- [ ] Virtual environment is activated (`.venv`)
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Jupyter Notebook is running (`jupyter notebook`)

## Test Environment Setup

### 1. Start Jupyter Notebook

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.\.venv\Scripts\Activate.ps1  # Windows PowerShell

# Start Jupyter
jupyter notebook
```

### 2. Open Dashboard Notebook

- [ ] Open `ProjectTwoDashboard.ipynb`
- [ ] Verify all code is in a single cell (MVC architecture)
- [ ] Note: Keep this checklist open in a separate window for reference

---

## Phase 1: Authentication Gate Testing

### Test 1.1: Failed Login - Empty Credentials

**Steps:**
1. [ ] Run the dashboard cell
2. [ ] Leave both username and password fields empty
3. [ ] Click "Login" button

**Expected Results:**
- [ ] Error message displays: "Username and password are required"
- [ ] Error message is red/prominent
- [ ] Dashboard does NOT appear
- [ ] Login form remains visible

### Test 1.2: Failed Login - Wrong Username

**Steps:**
1. [ ] Refresh/re-run the cell if needed
2. [ ] Enter username: `wronguser`
3. [ ] Enter password: `grazioso2024`
4. [ ] Click "Login" button

**Expected Results:**
- [ ] Error message displays: "Invalid username or password"
- [ ] Dashboard does NOT appear
- [ ] Login form remains visible
- [ ] Can retry login

### Test 1.3: Failed Login - Wrong Password

**Steps:**
1. [ ] Enter username: `admin`
2. [ ] Enter password: `wrongpassword`
3. [ ] Click "Login" button

**Expected Results:**
- [ ] Error message displays: "Invalid username or password"
- [ ] Dashboard does NOT appear
- [ ] Login form remains visible

### Test 1.4: Successful Login

**Steps:**
1. [ ] Enter username: `admin`
2. [ ] Enter password: `grazioso2024`
3. [ ] Click "Login" button

**Expected Results:**
- [ ] Login form disappears
- [ ] Dashboard appears with all components visible:
  - [ ] Grazioso Salvare logo (top left)
  - [ ] Dashboard title and creator info
  - [ ] Filter radio buttons (4 options + Reset)
  - [ ] Data table with animal records
  - [ ] Pie chart showing outcome types
  - [ ] Map with animal locations

---

## Phase 2: Dashboard Layout & Branding

### Test 2.1: Branding Header

- [ ] Logo is visible and properly sized
- [ ] Logo has alt text: "Grazioso Salvare Logo"
- [ ] Logo is clickable and links to SNHU website
- [ ] Dashboard title: "Grazioso Salvare Animal Rescue Dashboard"
- [ ] Creator credit: "Dashboard by Rick Goshen"
- [ ] Course info: "CS 340 - Client/Server Development"
- [ ] Header has horizontal rule separator

### Test 2.2: Layout Organization

- [ ] Components are arranged vertically in logical order
- [ ] Filters appear before data table
- [ ] Data table appears before visualizations
- [ ] Chart and map are visible without excessive scrolling
- [ ] No overlapping components
- [ ] Professional, clean appearance

---

## Phase 3: Filter Functionality Testing

### Test 3.1: Reset Filter (Default State)

**Steps:**
1. [ ] Ensure "Reset" radio button is selected by default

**Expected Results:**
- [ ] Data table shows ALL animals from database
- [ ] Note the total row count: __________ animals
- [ ] Table includes mix of dogs, cats, other animals
- [ ] Pie chart shows all outcome types
- [ ] Map shows all valid coordinate locations

### Test 3.2: Water Rescue Filter

**Steps:**
1. [ ] Click "Water Rescue" radio button
2. [ ] Wait for table to update

**Expected Results:**
- [ ] Row count DECREASES from reset count
- [ ] Note water rescue count: __________ animals
- [ ] ALL visible animals meet criteria:
  - [ ] Breed: Labrador Retriever Mix, Chesapeake Bay Retriever, or Newfoundland
  - [ ] Sex: Female
  - [ ] Intact Status: Intact
  - [ ] Age: Between 26-156 weeks (0.5-3 years)
- [ ] Verify at least 3 random rows meet all criteria
- [ ] Pie chart updates to show only water rescue outcome types
- [ ] Map updates to show only water rescue locations

### Test 3.3: Mountain/Wilderness Rescue Filter

**Steps:**
1. [ ] Click "Mountain/Wilderness Rescue" radio button
2. [ ] Wait for table to update

**Expected Results:**
- [ ] Row count changes from water rescue count
- [ ] Note mountain rescue count: __________ animals
- [ ] ALL visible animals meet criteria:
  - [ ] Breed: German Shepherd, Alaskan Malamute, Old English Sheepdog, Siberian Husky, or Rottweiler
  - [ ] Sex: Male
  - [ ] Intact Status: Intact
  - [ ] Age: Between 26-156 weeks (0.5-3 years)
- [ ] Verify at least 3 random rows meet all criteria
- [ ] Pie chart updates
- [ ] Map updates

### Test 3.4: Disaster/Tracking Rescue Filter

**Steps:**
1. [ ] Click "Disaster/Tracking" radio button
2. [ ] Wait for table to update

**Expected Results:**
- [ ] Row count changes from mountain rescue count
- [ ] Note disaster rescue count: __________ animals
- [ ] ALL visible animals meet criteria:
  - [ ] Breed: Doberman Pinscher, German Shepherd, Golden Retriever, Bloodhound, or Rottweiler
  - [ ] Sex: Male
  - [ ] Intact Status: Intact
  - [ ] Age: Between 20-300 weeks (~5 months - ~6 years)
- [ ] Verify at least 3 random rows meet all criteria
- [ ] Pie chart updates
- [ ] Map updates

### Test 3.5: Filter Transition - Reset Again

**Steps:**
1. [ ] Click "Reset" radio button
2. [ ] Wait for table to update

**Expected Results:**
- [ ] Row count returns to original "all animals" count
- [ ] Table shows same data as Test 3.1
- [ ] Pie chart shows all outcome types again
- [ ] Map shows all locations again

---

## Phase 4: Data Table Interaction Testing

### Test 4.1: Table Sorting

**Steps:**
1. [ ] Ensure "Reset" filter is selected (all animals visible)
2. [ ] Click on "breed" column header
3. [ ] Click again to reverse sort

**Expected Results:**
- [ ] First click: Breeds sorted alphabetically A→Z
- [ ] Second click: Breeds sorted reverse Z→A
- [ ] Sort indicator appears (arrow/icon)
- [ ] Filter remains active during sorting

**Repeat for other columns:**
- [ ] Sort by "name"
- [ ] Sort by "age_upon_outcome"
- [ ] Sort by "outcome_type"

### Test 4.2: Table Pagination

**Steps:**
1. [ ] Ensure "Reset" filter is selected
2. [ ] Check default page size (should show 10 rows per page)
3. [ ] Click "Next" page button

**Expected Results:**
- [ ] Page advances to show next 10 records
- [ ] Page indicator updates (e.g., "Page 2 of X")
- [ ] Can navigate forward and backward
- [ ] "Previous" button works
- [ ] Last page shows remaining records (may be < 10)

### Test 4.3: Table Row Selection

**Steps:**
1. [ ] Ensure "Reset" filter is selected
2. [ ] Note: First row should be selected by default
3. [ ] Click on a different row (e.g., row 3)

**Expected Results:**
- [ ] Selected row is highlighted (different background color)
- [ ] Only ONE row selected at a time (single selection mode)
- [ ] Previous selection is deselected
- [ ] Map updates to focus on selected animal (see Phase 5)

### Test 4.4: Table Tooltips

**Steps:**
1. [ ] Hover mouse over cells with long text (name, breed, etc.)
2. [ ] Wait ~1 second

**Expected Results:**
- [ ] Tooltip appears showing full cell content
- [ ] Tooltip is readable and properly positioned
- [ ] Works for all columns

---

## Phase 5: Map Interaction Testing

### Test 5.1: Map Display - Reset Filter

**Steps:**
1. [ ] Ensure "Reset" filter is selected
2. [ ] Examine the map component

**Expected Results:**
- [ ] Map displays with Austin, TX area visible
- [ ] Multiple markers visible (one per animal with valid coordinates)
- [ ] Markers are clustered appropriately if many animals
- [ ] Map controls visible (zoom in/out, pan)

### Test 5.2: Map Marker Tooltips

**Steps:**
1. [ ] Hover over a map marker

**Expected Results:**
- [ ] Tooltip appears showing animal info:
  - [ ] Animal name
  - [ ] Breed
  - [ ] Location coordinates (lat/long)
- [ ] Tooltip is readable

### Test 5.3: Map Marker Popups

**Steps:**
1. [ ] Click on a map marker

**Expected Results:**
- [ ] Popup appears with detailed animal information
- [ ] Popup includes: name, breed, sex, age, outcome type
- [ ] Popup has close button (X)
- [ ] Can close popup and open another

### Test 5.4: Map Updates with Row Selection

**Steps:**
1. [ ] Ensure "Reset" filter is selected
2. [ ] In data table, click on row 1
3. [ ] Note the animal's name and location
4. [ ] Look at the map

**Expected Results:**
- [ ] Map centers on the selected animal's location (if coordinates valid)
- [ ] Selected animal's marker may be highlighted or popup opens
- [ ] Map zoom level is appropriate to see marker clearly

**Repeat:**
5. [ ] Click on a different row (e.g., row 5)
6. [ ] Verify map updates to new selection

### Test 5.5: Map Updates with Filters

**Steps:**
1. [ ] Select "Water Rescue" filter
2. [ ] Note number of markers on map

**Expected Results:**
- [ ] Map shows ONLY water rescue animal locations
- [ ] Marker count matches filtered row count (minus any invalid coordinates)
- [ ] Map may re-center to show all visible markers

**Repeat for each filter:**
- [ ] "Mountain/Wilderness Rescue" - verify markers update
- [ ] "Disaster/Tracking" - verify markers update
- [ ] "Reset" - verify all markers return

---

## Phase 6: Pie Chart Testing

### Test 6.1: Pie Chart Display - Reset Filter

**Steps:**
1. [ ] Ensure "Reset" filter is selected
2. [ ] Examine the pie chart

**Expected Results:**
- [ ] Chart title: "Outcome Type Distribution" (or similar)
- [ ] Chart shows pie slices for different outcome types
- [ ] Each slice has a label showing outcome type name
- [ ] Percentages or counts displayed
- [ ] Legend visible with color mapping
- [ ] Top 10 outcome types shown individually
- [ ] Remaining types grouped as "Other" (if > 10 types total)

### Test 6.2: Pie Chart Interactivity

**Steps:**
1. [ ] Hover over a pie slice

**Expected Results:**
- [ ] Tooltip appears showing:
  - [ ] Outcome type name
  - [ ] Count of animals with this outcome
  - [ ] Percentage of total
- [ ] Slice may highlight on hover

### Test 6.3: Pie Chart Updates with Filters

**Steps:**
1. [ ] Select "Water Rescue" filter
2. [ ] Note which outcome types appear in chart

**Expected Results:**
- [ ] Chart updates to show ONLY water rescue outcome types
- [ ] Slice sizes change to reflect filtered data
- [ ] Percentages recalculate for filtered subset
- [ ] Chart remains readable (no overlapping labels)

**Repeat for each filter:**
- [ ] "Mountain/Wilderness Rescue" - verify chart updates
- [ ] "Disaster/Tracking" - verify chart updates
- [ ] "Reset" - verify chart returns to all data

---

## Phase 7: Data Quality Testing with Real Data

### Test 7.1: Age Parsing Validation

**Steps:**
1. [ ] Select "Reset" filter
2. [ ] Sort table by "age_upon_outcome" column
3. [ ] Examine various age formats in the data

**Check for these formats:**
- [ ] Ages in years (e.g., "2 years", "5 year")
- [ ] Ages in months (e.g., "6 months", "18 month")
- [ ] Ages in weeks (e.g., "12 weeks", "8 week")
- [ ] Ages in days (e.g., "21 days")
- [ ] Mixed formats in same dataset

**Expected Results:**
- [ ] All age formats display correctly in table
- [ ] No "None" or "NaN" values in normalized age_weeks column (if visible)
- [ ] Filters correctly handle all age formats
- [ ] Animals with malformed ages (if any) don't crash dashboard

### Test 7.2: Breed Matching Validation

**Steps:**
1. [ ] Select "Water Rescue" filter
2. [ ] Examine breed column for all visible rows

**Check for these breed string patterns:**
- [ ] Simple breeds: "Labrador Retriever Mix"
- [ ] Multi-breed with slash: "Labrador/Retriever Mix"
- [ ] Multi-breed with comma: "Labrador, Retriever Mix"
- [ ] Breeds with "Mix" suffix
- [ ] Different capitalizations

**Expected Results:**
- [ ] All visible breeds match water rescue criteria
- [ ] Multi-breed strings are recognized (not filtered out)
- [ ] Case variations are handled (e.g., "labrador" vs "Labrador")
- [ ] No incorrect breeds visible in filtered results

**Repeat for:**
- [ ] "Mountain/Wilderness Rescue" filter
- [ ] "Disaster/Tracking" filter

### Test 7.3: Coordinate Validation

**Steps:**
1. [ ] Select "Reset" filter
2. [ ] Count total rows in table: __________
3. [ ] Count markers on map: __________
4. [ ] Sort by location_lat column
5. [ ] Look for null, invalid, or out-of-range coordinates

**Expected Results:**
- [ ] Map marker count ≤ table row count (some animals may have invalid coords)
- [ ] Animals with null coordinates still appear in table
- [ ] Animals with invalid coordinates (e.g., 999, 0, etc.) still appear in table
- [ ] Map gracefully handles invalid coordinates (doesn't crash)
- [ ] Only animals with valid coordinates appear on map

### Test 7.4: Null/Missing Values Handling

**Steps:**
1. [ ] Select "Reset" filter
2. [ ] Scroll through table looking for null/empty values

**Check these columns:**
- [ ] name (some animals may be unnamed)
- [ ] breed (should have value)
- [ ] sex_upon_outcome (may have missing data)
- [ ] outcome_type (should have value)
- [ ] age_upon_outcome (may have missing data)

**Expected Results:**
- [ ] Dashboard doesn't crash with null values
- [ ] Null values display as empty cells or "N/A" (not "None" or error)
- [ ] Filters handle nulls gracefully (exclude or include based on logic)
- [ ] Charts/maps exclude animals with required null fields

### Test 7.5: Category Bucketing Validation

**Steps:**
1. [ ] Select "Reset" filter
2. [ ] Examine pie chart outcome types
3. [ ] Count unique outcome types in chart: __________

**Expected Results:**
- [ ] If > 10 outcome types exist, chart shows top 10 + "Other"
- [ ] If ≤ 10 outcome types exist, chart shows all individually
- [ ] "Other" category combines low-frequency outcomes
- [ ] "Other" slice shows combined count/percentage
- [ ] No duplicate categories in chart

---

## Phase 8: Cross-Component Integration Testing

### Test 8.1: Filter → Table → Map → Chart Flow

**Steps:**
1. [ ] Select "Water Rescue" filter
2. [ ] Note table row count: __________
3. [ ] Click on row 3 in table
4. [ ] Check pie chart

**Expected Results:**
- [ ] All four components update together:
  - [ ] Table shows filtered animals
  - [ ] Map shows filtered locations
  - [ ] Pie chart shows filtered outcome types
  - [ ] Row selection updates map focus
- [ ] All counts are consistent across components

### Test 8.2: Sorting with Filtering

**Steps:**
1. [ ] Select "Mountain/Wilderness Rescue" filter
2. [ ] Sort table by "breed" column
3. [ ] Select "Disaster/Tracking" filter
4. [ ] Verify sorting persists

**Expected Results:**
- [ ] Sorting order maintained when switching filters
- [ ] Filtered results are properly sorted
- [ ] No sorting errors or crashes

### Test 8.3: Pagination with Filtering

**Steps:**
1. [ ] Select "Reset" filter
2. [ ] Navigate to page 3 (or any page > 1)
3. [ ] Select "Water Rescue" filter

**Expected Results:**
- [ ] Pagination resets to page 1 when filter changes
- [ ] Correct number of pages for filtered data
- [ ] Can paginate through filtered results

---

## Phase 9: Performance & Usability Testing

### Test 9.1: Dashboard Load Time

**Steps:**
1. [ ] Close and restart Jupyter kernel
2. [ ] Re-run dashboard cell
3. [ ] Time how long until dashboard is interactive

**Expected Results:**
- [ ] Dashboard loads in < 10 seconds
- [ ] No visible errors during load
- [ ] All components render properly

### Test 9.2: Filter Response Time

**Steps:**
1. [ ] Select each filter and note response time:
   - [ ] Reset: __________ seconds
   - [ ] Water Rescue: __________ seconds
   - [ ] Mountain/Wilderness: __________ seconds
   - [ ] Disaster/Tracking: __________ seconds

**Expected Results:**
- [ ] Each filter updates in < 2 seconds
- [ ] No lag or freezing
- [ ] Smooth transitions

### Test 9.3: Large Dataset Handling

**Steps:**
1. [ ] Select "Reset" filter (largest dataset)
2. [ ] Scroll through many pages
3. [ ] Select multiple rows
4. [ ] Zoom/pan map

**Expected Results:**
- [ ] No performance degradation with full dataset
- [ ] Table pagination remains responsive
- [ ] Map handles many markers without lag
- [ ] Chart renders quickly

---

## Phase 10: Error Handling & Edge Cases

### Test 10.1: Database Connection Loss (Optional)

**Steps:**
1. [ ] (Advanced) Stop MongoDB service
2. [ ] Re-run dashboard cell

**Expected Results:**
- [ ] Dashboard shows user-friendly error message
- [ ] No Python stack trace visible to user
- [ ] Instructions to check database connection

### Test 10.2: Empty Filter Results

**Steps:**
1. [ ] If possible, select a filter that returns 0 results
   (This may not be possible with real AAC data)

**Expected Results:**
- [ ] Table shows "No data available" message
- [ ] Pie chart shows empty state or message
- [ ] Map shows no markers (or shows message)
- [ ] No errors or crashes

### Test 10.3: Browser Compatibility (Optional)

**Repeat all tests in different browsers:**
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (macOS)
- [ ] Edge (Windows)

---

## Test Summary

### Overall Results

**Total Tests Executed:** __________
**Tests Passed:** __________
**Tests Failed:** __________

### Issues Found

| Issue # | Description | Severity | Component |
|---------|-------------|----------|-----------|
| 1       |             |          |           |
| 2       |             |          |           |
| 3       |             |          |           |

### Notes & Observations

(Add any additional observations, unexpected behavior, or suggestions)

---

## Sign-off

**Tester Name:** ________________________________
**Date Completed:** ________________________________
**Overall Status:** [ ] PASS  [ ] FAIL  [ ] PASS WITH ISSUES

---

## Appendix: Quick Reference

### Test Credentials
- Username: `admin`
- Password: `grazioso2024`

### Filter Criteria Reference

**Water Rescue:**
- Breeds: Labrador Retriever Mix, Chesapeake Bay Retriever, Newfoundland
- Sex: Female, Intact
- Age: 26-156 weeks (6 months - 3 years)

**Mountain/Wilderness Rescue:**
- Breeds: German Shepherd, Alaskan Malamute, Old English Sheepdog, Siberian Husky, Rottweiler
- Sex: Male, Intact
- Age: 26-156 weeks (6 months - 3 years)

**Disaster/Tracking Rescue:**
- Breeds: Doberman Pinscher, German Shepherd, Golden Retriever, Bloodhound, Rottweiler
- Sex: Male, Intact
- Age: 20-300 weeks (5 months - 6 years)

### Expected Component Behavior

| Component | Filter Change | Row Selection | Sort | Pagination |
|-----------|---------------|---------------|------|------------|
| Table     | Updates       | Highlights    | Yes  | Yes        |
| Map       | Updates       | Re-centers    | No   | No         |
| Chart     | Updates       | No change     | No   | No         |

---

**End of Manual Testing Plan**
