"""Rescue type filtering for Grazioso Salvare animal candidates.

This module provides filtering functions for identifying animals suitable
for specific rescue operations (water, mountain, disaster/tracking) based
on breed, sex, age, and other characteristics.
"""

import pandas as pd

from data_helpers import breed_matches_rescue_type


def water_rescue_filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter animals suitable for water rescue operations.

    Applies breed, sex, and age criteria specific to water rescue training.

    Filter Criteria:
        - Breeds: Labrador Retriever, Chesapeake Bay Retriever, Newfoundland
        - Sex: Intact Female
        - Age: 26-156 weeks (6 months to 3 years)

    Args:
        df: Normalized DataFrame with age_weeks, sex, intact_status columns

    Returns:
        Filtered DataFrame containing only water rescue candidates

    Examples:
        >>> from data_helpers import normalize_dataframe
        >>> df = normalize_dataframe(raw_df)
        >>> water_candidates = water_rescue_filter(df)
        >>> len(water_candidates)  # Number of water rescue candidates
    """
    filtered = df[
        df['breed'].apply(
            lambda b: breed_matches_rescue_type(b, 'water')
        ) &
        (df['sex'] == 'Female') &
        (df['intact_status'] == 'Intact') &
        (df['age_weeks'] >= 26) &
        (df['age_weeks'] <= 156)
    ]
    return filtered


def mountain_rescue_filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter animals suitable for mountain/wilderness rescue operations.

    Applies breed, sex, and age criteria specific to mountain rescue
    training.

    Filter Criteria:
        - Breeds: German Shepherd, Alaskan Malamute, Old English Sheepdog,
                 Siberian Husky, Rottweiler
        - Sex: Intact Male
        - Age: 26-156 weeks (6 months to 3 years)

    Args:
        df: Normalized DataFrame with age_weeks, sex, intact_status columns

    Returns:
        Filtered DataFrame containing only mountain rescue candidates

    Examples:
        >>> from data_helpers import normalize_dataframe
        >>> df = normalize_dataframe(raw_df)
        >>> mountain_candidates = mountain_rescue_filter(df)
        >>> len(mountain_candidates)  # Number of mountain rescue candidates
    """
    filtered = df[
        df['breed'].apply(
            lambda b: breed_matches_rescue_type(b, 'mountain')
        ) &
        (df['sex'] == 'Male') &
        (df['intact_status'] == 'Intact') &
        (df['age_weeks'] >= 26) &
        (df['age_weeks'] <= 156)
    ]
    return filtered


def disaster_rescue_filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter animals suitable for disaster rescue or tracking operations.

    Applies breed, sex, and age criteria specific to disaster rescue
    and individual tracking training.

    Filter Criteria:
        - Breeds: Doberman Pinscher, German Shepherd, Golden Retriever,
                 Bloodhound, Rottweiler
        - Sex: Intact Male
        - Age: 20-300 weeks (5 months to ~6 years)

    Args:
        df: Normalized DataFrame with age_weeks, sex, intact_status columns

    Returns:
        Filtered DataFrame containing only disaster/tracking rescue
        candidates

    Examples:
        >>> from data_helpers import normalize_dataframe
        >>> df = normalize_dataframe(raw_df)
        >>> disaster_candidates = disaster_rescue_filter(df)
        >>> len(disaster_candidates)  # Number of disaster rescue candidates
    """
    filtered = df[
        df['breed'].apply(
            lambda b: breed_matches_rescue_type(b, 'disaster')
        ) &
        (df['sex'] == 'Male') &
        (df['intact_status'] == 'Intact') &
        (df['age_weeks'] >= 20) &
        (df['age_weeks'] <= 300)
    ]
    return filtered


def reset_filter(df: pd.DataFrame) -> pd.DataFrame:
    """Return unfiltered DataFrame (reset to show all animals).

    This function returns the DataFrame unchanged, effectively resetting
    any active filters to show all available animals.

    Args:
        df: Normalized DataFrame

    Returns:
        The same DataFrame unchanged (no filtering applied)

    Examples:
        >>> from data_helpers import normalize_dataframe
        >>> df = normalize_dataframe(raw_df)
        >>> all_animals = reset_filter(df)
        >>> len(all_animals) == len(df)
        True
    """
    return df


def apply_rescue_filter(
    df: pd.DataFrame,
    filter_type: str
) -> pd.DataFrame:
    """Apply rescue type filter based on filter type string.

    Dispatcher function that routes to appropriate rescue filter based
    on the filter_type parameter. This is the main entry point for
    applying rescue filters in the dashboard.

    Args:
        df: Normalized DataFrame with required columns
        filter_type: Type of rescue filter to apply
                    ('water', 'mountain', 'disaster', 'tracking', 'reset')

    Returns:
        Filtered DataFrame based on rescue type criteria

    Raises:
        ValueError: If filter_type is not recognized

    Examples:
        >>> from data_helpers import normalize_dataframe
        >>> df = normalize_dataframe(raw_df)
        >>> water_df = apply_rescue_filter(df, 'water')
        >>> mountain_df = apply_rescue_filter(df, 'mountain')
        >>> all_df = apply_rescue_filter(df, 'reset')
    """
    filter_type = filter_type.strip().lower()

    match filter_type:
        case 'water':
            return water_rescue_filter(df)
        case 'mountain' | 'wilderness':
            return mountain_rescue_filter(df)
        case 'disaster' | 'tracking':
            return disaster_rescue_filter(df)
        case 'reset' | '':
            return reset_filter(df)
        case _:
            raise ValueError(
                f"Invalid filter type: '{filter_type}'. "
                f"Valid options: water, mountain, disaster, tracking, reset"
            )
