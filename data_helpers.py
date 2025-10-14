"""Data normalization and helper functions for Grazioso Rescue Finder.

This module provides utility functions to clean, normalize, and transform
animal shelter data for use in the dashboard and rescue type filtering.
"""

import re
from typing import Optional


def parse_age_to_weeks(age_str: Optional[str]) -> Optional[float]:
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
    sex_upon_outcome: Optional[str]
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
    location_lat: Optional[float | str],
    location_long: Optional[float | str]
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

        if lon < -180 or lon > 180:
            return False

        return True

    except (TypeError, ValueError):
        return False


def breed_matches_rescue_type(
    breed: Optional[str],
    rescue_type: str
) -> bool:
    """Check if breed matches rescue type requirements.

    Determines if an animal's breed is suitable for a specific rescue type
    (water, mountain, disaster, tracking) based on breed requirements.

    Args:
        breed: Animal breed string (may include multiple breeds)
        rescue_type: Type of rescue ("water", "mountain", "disaster", "tracking")

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
    for target_breed in target_breeds:
        if target_breed in breed:
            return True

    return False
