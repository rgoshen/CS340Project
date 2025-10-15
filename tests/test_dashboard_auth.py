"""Unit tests for dashboard authentication module."""

import unittest

from dashboard_auth import (
    get_auth_error_message,
    is_authenticated,
    validate_credentials,
)


class TestValidateCredentials(unittest.TestCase):
    """Test cases for validate_credentials function."""

    def test_valid_credentials(self):
        """Test that valid credentials return True."""
        result = validate_credentials("admin", "grazioso2024")
        self.assertTrue(result)

    def test_invalid_username(self):
        """Test that invalid username returns False."""
        result = validate_credentials("wrong", "grazioso2024")
        self.assertFalse(result)

    def test_invalid_password(self):
        """Test that invalid password returns False."""
        result = validate_credentials("admin", "wrongpass")
        self.assertFalse(result)

    def test_both_invalid(self):
        """Test that both invalid credentials return False."""
        result = validate_credentials("wrong", "wrongpass")
        self.assertFalse(result)

    def test_empty_username(self):
        """Test that empty username returns False."""
        result = validate_credentials("", "grazioso2024")
        self.assertFalse(result)

    def test_empty_password(self):
        """Test that empty password returns False."""
        result = validate_credentials("admin", "")
        self.assertFalse(result)

    def test_both_empty(self):
        """Test that both empty credentials return False."""
        result = validate_credentials("", "")
        self.assertFalse(result)

    def test_none_username(self):
        """Test that None username returns False."""
        result = validate_credentials(None, "grazioso2024")
        self.assertFalse(result)

    def test_none_password(self):
        """Test that None password returns False."""
        result = validate_credentials("admin", None)
        self.assertFalse(result)

    def test_both_none(self):
        """Test that both None credentials return False."""
        result = validate_credentials(None, None)
        self.assertFalse(result)

    def test_whitespace_only_username(self):
        """Test that whitespace-only username returns False."""
        result = validate_credentials("   ", "grazioso2024")
        self.assertFalse(result)

    def test_whitespace_only_password(self):
        """Test that whitespace-only password returns False."""
        result = validate_credentials("admin", "   ")
        self.assertFalse(result)

    def test_valid_credentials_with_whitespace(self):
        """Test that valid credentials with whitespace are trimmed."""
        result = validate_credentials("  admin  ", "  grazioso2024  ")
        self.assertTrue(result)

    def test_case_sensitive_username(self):
        """Test that username is case-sensitive."""
        result = validate_credentials("ADMIN", "grazioso2024")
        self.assertFalse(result)

    def test_case_sensitive_password(self):
        """Test that password is case-sensitive."""
        result = validate_credentials("admin", "GRAZIOSO2024")
        self.assertFalse(result)

    def test_non_string_username(self):
        """Test that non-string username returns False."""
        result = validate_credentials(12345, "grazioso2024")
        self.assertFalse(result)

    def test_non_string_password(self):
        """Test that non-string password returns False."""
        result = validate_credentials("admin", 12345)
        self.assertFalse(result)

    def test_username_with_special_characters(self):
        """Test that username with special chars fails if not exact."""
        result = validate_credentials("admin@", "grazioso2024")
        self.assertFalse(result)

    def test_password_with_special_characters(self):
        """Test that password with special chars fails if not exact."""
        result = validate_credentials("admin", "grazioso2024!")
        self.assertFalse(result)


class TestGetAuthErrorMessage(unittest.TestCase):
    """Test cases for get_auth_error_message function."""

    def test_both_empty(self):
        """Test error message for both empty credentials."""
        result = get_auth_error_message("", "")
        self.assertEqual(result, "Username and password are required.")

    def test_empty_username(self):
        """Test error message for empty username."""
        result = get_auth_error_message("", "somepass")
        self.assertEqual(result, "Username is required.")

    def test_empty_password(self):
        """Test error message for empty password."""
        result = get_auth_error_message("someuser", "")
        self.assertEqual(result, "Password is required.")

    def test_invalid_credentials(self):
        """Test error message for invalid credentials."""
        result = get_auth_error_message("wrong", "wrongpass")
        self.assertEqual(result, "Invalid username or password.")

    def test_none_username(self):
        """Test error message for None username."""
        result = get_auth_error_message(None, "somepass")
        self.assertEqual(result, "Username and password are required.")

    def test_none_password(self):
        """Test error message for None password."""
        result = get_auth_error_message("someuser", None)
        self.assertEqual(result, "Username and password are required.")

    def test_both_none(self):
        """Test error message for both None credentials."""
        result = get_auth_error_message(None, None)
        self.assertEqual(result, "Username and password are required.")

    def test_whitespace_only_username(self):
        """Test error message for whitespace-only username."""
        result = get_auth_error_message("   ", "somepass")
        self.assertEqual(result, "Username is required.")

    def test_whitespace_only_password(self):
        """Test error message for whitespace-only password."""
        result = get_auth_error_message("someuser", "   ")
        self.assertEqual(result, "Password is required.")

    def test_both_whitespace_only(self):
        """Test error message for both whitespace-only credentials."""
        result = get_auth_error_message("   ", "   ")
        self.assertEqual(result, "Username and password are required.")

    def test_non_string_username(self):
        """Test error message for non-string username."""
        result = get_auth_error_message(12345, "somepass")
        self.assertEqual(result, "Username and password must be text.")

    def test_non_string_password(self):
        """Test error message for non-string password."""
        result = get_auth_error_message("someuser", 12345)
        self.assertEqual(result, "Username and password must be text.")

    def test_both_non_string(self):
        """Test error message for both non-string credentials."""
        result = get_auth_error_message(12345, 67890)
        self.assertEqual(result, "Username and password must be text.")


class TestIsAuthenticated(unittest.TestCase):
    """Test cases for is_authenticated function."""

    def test_authenticated_true(self):
        """Test that authenticated state returns True."""
        result = is_authenticated({"authenticated": True})
        self.assertTrue(result)

    def test_authenticated_false(self):
        """Test that non-authenticated state returns False."""
        result = is_authenticated({"authenticated": False})
        self.assertFalse(result)

    def test_empty_dict(self):
        """Test that empty dict returns False."""
        result = is_authenticated({})
        self.assertFalse(result)

    def test_none_state(self):
        """Test that None state returns False."""
        result = is_authenticated(None)
        self.assertFalse(result)

    def test_missing_authenticated_key(self):
        """Test that dict without 'authenticated' key returns False."""
        result = is_authenticated({"user": "admin"})
        self.assertFalse(result)

    def test_authenticated_non_boolean(self):
        """Test that non-boolean authenticated value returns False."""
        result = is_authenticated({"authenticated": "yes"})
        self.assertFalse(result)

    def test_authenticated_truthy_value(self):
        """Test that truthy non-True value returns False."""
        result = is_authenticated({"authenticated": 1})
        self.assertFalse(result)

    def test_authenticated_with_extra_keys(self):
        """Test that extra keys don't affect authentication check."""
        result = is_authenticated({
            "authenticated": True,
            "username": "admin",
            "timestamp": "2024-01-01"
        })
        self.assertTrue(result)

    def test_non_dict_state(self):
        """Test that non-dict state returns False."""
        result = is_authenticated("authenticated")
        self.assertFalse(result)

    def test_list_state(self):
        """Test that list state returns False."""
        result = is_authenticated([True])
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
