"""Data normalization and helper functions for Grazioso Rescue Finder.

This module provides utility functions to clean, normalize, and transform
animal shelter data for use in the dashboard and rescue type filtering.
"""

import re
from collections import Counter

import pandas as pd


def parse_age_to_weeks(age_str: str | None) -> float | None:
    """Parse age string to numeric weeks.

    Converts age strings like "2 years", "6 months", "3 weeks", "14 days"
    into a numeric value in weeks for consistent age comparisons.

    Args:
        age_str: Age string from shelter data (e.g., "2 years", "6 months")

    Returns:
        Age in weeks as float, or None if input is invalid/None

    Examples:
        >>> parse_age_to_weeks("2 years")
        104.286
        >>> parse_age_to_weeks("6 months")
        26.07
        >>> parse_age_to_weeks("3 weeks")
        3.0
        >>> parse_age_to_weeks("14 days")
        2.0
        >>> parse_age_to_weeks(None)
        None
        >>> parse_age_to_weeks("invalid")
        None
    """
    if age_str is None or not isinstance(age_str, str):
        return None

    age_str = age_str.strip().lower()

    if not age_str:
        return None

    # Extract number and unit using regex
    match = re.match(r'(\d+(?:\.\d+)?)\s*(year|month|week|day)s?', age_str)

    if not match:
        return None

    value = float(match.group(1))
    unit = match.group(2)

    # Handle negative or zero values
    if value <= 0:
        return None

    # Convert to weeks based on unit
    match unit:
        case 'year':
            return value * 52.143  # Average weeks per year
        case 'month':
            return value * 4.345  # Average weeks per month
        case 'week':
            return value
        case 'day':
            return value / 7.0
        case _:
            return None


def normalize_sex_intact(
    sex_upon_outcome: str | None
) -> tuple[str, str]:
    """Parse sex_upon_outcome into separate sex and intact status.

    Extracts sex (Male/Female) and intact status (Intact/Neutered/Spayed)
    from combined shelter data strings like "Neutered Male", "Intact Female".

    Args:
        sex_upon_outcome: Combined sex and status (e.g., "Neutered Male")

    Returns:
        Tuple of (sex, intact_status):
        - sex: "Male", "Female", or "Unknown"
        - intact_status: "Intact", "Neutered", "Spayed", or "Unknown"

    Examples:
        >>> normalize_sex_intact("Neutered Male")
        ('Male', 'Neutered')
        >>> normalize_sex_intact("Intact Female")
        ('Female', 'Intact')
        >>> normalize_sex_intact("Spayed Female")
        ('Female', 'Spayed')
        >>> normalize_sex_intact(None)
        ('Unknown', 'Unknown')
        >>> normalize_sex_intact("Unknown")
        ('Unknown', 'Unknown')
    """
    if sex_upon_outcome is None or not isinstance(sex_upon_outcome, str):
        return ('Unknown', 'Unknown')

    sex_upon_outcome = sex_upon_outcome.strip().lower()

    if not sex_upon_outcome or sex_upon_outcome == 'unknown':
        return ('Unknown', 'Unknown')

    # Initialize defaults
    sex = 'Unknown'
    intact_status = 'Unknown'

    # Determine sex
    if 'male' in sex_upon_outcome and 'female' not in sex_upon_outcome:
        sex = 'Male'
    elif 'female' in sex_upon_outcome:
        sex = 'Female'

    # Determine intact status
    if 'neutered' in sex_upon_outcome:
        intact_status = 'Neutered'
    elif 'spayed' in sex_upon_outcome:
        intact_status = 'Spayed'
    elif 'intact' in sex_upon_outcome:
        intact_status = 'Intact'

    return (sex, intact_status)


def validate_coordinates(
    location_lat: float | str | None,
    location_long: float | str | None
) -> bool:
    """Validate geographic coordinates.

    Checks if latitude and longitude values are within valid ranges
    and can be coerced to floats.

    Args:
        location_lat: Latitude value (-90 to 90)
        location_long: Longitude value (-180 to 180)

    Returns:
        True if both coordinates are valid, False otherwise

    Examples:
        >>> validate_coordinates(30.2672, -97.7431)
        True
        >>> validate_coordinates("30.2672", "-97.7431")
        True
        >>> validate_coordinates(91, -97.7431)
        False
        >>> validate_coordinates(30.2672, -181)
        False
        >>> validate_coordinates(None, -97.7431)
        False
        >>> validate_coordinates("invalid", -97.7431)
        False
    """
    try:
        lat = float(location_lat)
        lon = float(location_long)

        # Check for NaN
        if lat != lat or lon != lon:  # NaN check
            return False

        # Validate ranges
        if lat < -90 or lat > 90:
            return False

        return not (lon < -180 or lon > 180)

    except (TypeError, ValueError):
        return False


def breed_matches_rescue_type(
    breed: str | None,
    rescue_type: str
) -> bool:
    """Check if breed matches rescue type requirements.

    Determines if an animal's breed is suitable for a specific rescue type
    (water, mountain, disaster, tracking) based on breed requirements.

    Args:
        breed: Animal breed string (may include multiple breeds)
        rescue_type: Type of rescue (water/mountain/disaster/tracking)

    Returns:
        True if breed matches rescue type requirements, False otherwise

    Rescue Type Breed Requirements:
        - water: Labrador Retriever Mix, Chesapeake Bay Retriever, Newfoundland
        - mountain: German Shepherd, Alaskan Malamute, Old English Sheepdog,
                   Siberian Husky, Rottweiler
        - disaster: Doberman Pinscher, German Shepherd, Golden Retriever,
                    Bloodhound, Rottweiler
        - tracking: (same as disaster)

    Examples:
        >>> breed_matches_rescue_type("Labrador Retriever Mix", "water")
        True
        >>> breed_matches_rescue_type("German Shepherd", "mountain")
        True
        >>> breed_matches_rescue_type("Poodle", "water")
        False
        >>> breed_matches_rescue_type(None, "water")
        False
    """
    if breed is None or not isinstance(breed, str):
        return False

    breed = breed.strip().lower()

    if not breed:
        return False

    rescue_type = rescue_type.strip().lower()

    # Define breed requirements for each rescue type
    water_breeds = {
        'labrador retriever',
        'chesapeake bay retriever',
        'newfoundland'
    }

    mountain_breeds = {
        'german shepherd',
        'alaskan malamute',
        'old english sheepdog',
        'siberian husky',
        'rottweiler'
    }

    disaster_breeds = {
        'doberman pinscher',
        'german shepherd',
        'golden retriever',
        'bloodhound',
        'rottweiler'
    }

    # Select appropriate breed set based on rescue type
    match rescue_type:
        case 'water':
            target_breeds = water_breeds
        case 'mountain':
            target_breeds = mountain_breeds
        case 'disaster' | 'tracking':
            target_breeds = disaster_breeds
        case _:
            return False

    # Check if any target breed is in the animal's breed string
    return any(target_breed in breed for target_breed in target_breeds)


def bucket_categories(
    values: list[str],
    top_n: int = 10
) -> dict[str, str]:
    """Group low-frequency categories into 'Other' bucket.

    Creates top N categories and groups remaining values as "Other"
    for cleaner dashboard visualizations. Uses deterministic alphabetical
    tie-breaking when categories have equal counts.

    Args:
        values: List of category values (e.g., breeds, colors)
        top_n: Number of top categories to keep (default: 10)

    Returns:
        Dictionary mapping original values to bucketed values
        (either original value or "Other")

    Examples:
        >>> values = ["Dog", "Dog", "Cat", "Cat", "Bird", "Fish"]
        >>> bucket_categories(values, top_n=2)
        {'Dog': 'Dog', 'Cat': 'Cat', 'Bird': 'Other', 'Fish': 'Other'}
    """
    if not values or top_n <= 0:
        return {}

    # Count occurrences
    counts = Counter(values)

    # Get top N categories with deterministic tie-breaking
    # Sort by count (descending), then alphabetically for ties
    top_categories = sorted(
        counts.items(),
        key=lambda x: (-x[1], x[0])
    )[:top_n]

    # Create set of top category names
    top_names = {cat[0] for cat in top_categories}

    # Create mapping: top categories map to themselves, others to "Other"
    mapping = {}
    for value in values:
        if value in top_names:
            mapping[value] = value
        else:
            mapping[value] = 'Other'

    return mapping


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize animal shelter DataFrame with derived fields.

    Applies all normalization helpers to create cleaned, enriched data:
    - Parses age strings into numeric weeks (age_weeks column)
    - Extracts sex and intact status (sex, intact_status columns)
    - Validates coordinates (valid_coords boolean column)

    This is a non-destructive transformation - original columns are preserved
    and new normalized columns are added alongside them.

    Args:
        df: Raw animal shelter DataFrame with AAC schema columns

    Returns:
        Normalized DataFrame with additional columns:
        - age_weeks: float, age in weeks (None if unparseable)
        - sex: str, standardized sex (Male/Female/Unknown)
        - intact_status: str, standardized status
                        (Intact/Neutered/Spayed/Unknown)
        - valid_coords: bool, True if coordinates are valid for mapping

    Raises:
        ValueError: If required columns are missing from DataFrame

    Examples:
        >>> df = pd.DataFrame({
        ...     'animal_id': ['A001'],
        ...     'age_upon_outcome': ['2 years'],
        ...     'sex_upon_outcome': ['Neutered Male'],
        ...     'location_lat': [30.2672],
        ...     'location_long': [-97.7431]
        ... })
        >>> normalized = normalize_dataframe(df)
        >>> normalized['age_weeks'][0]
        104.286
        >>> normalized['sex'][0]
        'Male'
        >>> normalized['intact_status'][0]
        'Neutered'
        >>> normalized['valid_coords'][0]
        True
    """
    # Validate required columns exist
    required_columns = [
        'age_upon_outcome',
        'sex_upon_outcome',
        'location_lat',
        'location_long'
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    # Create a copy to avoid modifying original DataFrame
    normalized_df = df.copy()

    # Apply age parsing to create age_weeks column
    normalized_df['age_weeks'] = normalized_df['age_upon_outcome'].apply(
        parse_age_to_weeks
    )

    # Apply sex/intact normalization to create sex and intact_status columns
    sex_intact_tuples = normalized_df['sex_upon_outcome'].apply(
        normalize_sex_intact
    )
    normalized_df['sex'] = sex_intact_tuples.apply(lambda x: x[0])
    normalized_df['intact_status'] = sex_intact_tuples.apply(lambda x: x[1])

    # Apply coordinate validation to create valid_coords flag
    normalized_df['valid_coords'] = normalized_df.apply(
        lambda row: validate_coordinates(
            row['location_lat'],
            row['location_long']
        ),
        axis=1
    )

    return normalized_df
