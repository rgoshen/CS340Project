"""Dashboard authentication module for Grazioso Salvare Rescue Finder.

This module provides simple authentication functionality for the dashboard
login gate. It is designed for coursework purposes and is NOT intended for
production use.

For production systems, use proper authentication services like OAuth2,
JWT tokens, or enterprise SSO solutions.
"""


def validate_credentials(username: str, password: str) -> bool:
    """Validate dashboard login credentials.

    This is a simple authentication check for coursework requirements.
    In production, this would connect to a proper authentication service.

    Args:
        username (str): The username to validate
        password (str): The password to validate

    Returns:
        bool: True if credentials are valid, False otherwise

    Examples:
        >>> validate_credentials("admin", "password123")
        True
        >>> validate_credentials("wrong", "invalid")
        False
        >>> validate_credentials("", "")
        False
    """
    # Input validation
    if username is None or password is None:
        return False

    if not isinstance(username, str) or not isinstance(password, str):
        return False

    # Strip whitespace for comparison
    username = username.strip()
    password = password.strip()

    # Reject empty credentials
    if not username or not password:
        return False

    # Simple credential check for coursework
    # For production: use secure authentication service
    valid_username = "admin"
    valid_password = "grazioso2024"

    return username == valid_username and password == valid_password


def get_auth_error_message(username: str, password: str) -> str:
    """Generate appropriate error message for failed authentication.

    Args:
        username (str): The attempted username
        password (str): The attempted password

    Returns:
        str: User-friendly error message

    Examples:
        >>> get_auth_error_message("", "")
        'Username and password are required.'
        >>> get_auth_error_message("admin", "wrong")
        'Invalid username or password.'
    """
    # Handle None inputs
    if username is None or password is None:
        return "Username and password are required."

    # Handle non-string inputs
    if not isinstance(username, str) or not isinstance(password, str):
        return "Username and password must be text."

    # Strip whitespace
    username = username.strip()
    password = password.strip()

    # Check for empty credentials
    if not username and not password:
        return "Username and password are required."

    if not username:
        return "Username is required."

    if not password:
        return "Password is required."

    # Generic error for wrong credentials (security best practice)
    return "Invalid username or password."


def is_authenticated(auth_state: dict) -> bool:
    """Check if the current session is authenticated.

    Args:
        auth_state (dict): Authentication state dictionary from dcc.Store

    Returns:
        bool: True if authenticated, False otherwise

    Examples:
        >>> is_authenticated({"authenticated": True})
        True
        >>> is_authenticated({"authenticated": False})
        False
        >>> is_authenticated({})
        False
        >>> is_authenticated(None)
        False
    """
    if auth_state is None:
        return False

    if not isinstance(auth_state, dict):
        return False

    return auth_state.get("authenticated", False) is True
