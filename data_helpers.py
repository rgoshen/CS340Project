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
