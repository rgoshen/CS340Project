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
