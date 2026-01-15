"""Unit tests for AuthManager class (Task 3)."""

import json
import tempfile
import pytest
from pathlib import Path
from src.auth import AuthManager


class TestAuthManagerSignup:
    """Test cases for the signup functionality."""

    @pytest.fixture
    def temp_users_file(self):
        """Create a temporary users file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        yield temp_path
        # Cleanup
        Path(temp_path).unlink(missing_ok=True)

    @pytest.fixture
    def auth_manager(self, temp_users_file):
        """Create an AuthManager instance with temp file."""
        return AuthManager(temp_users_file)

    def test_signup_success(self, auth_manager):
        """Test successful user signup."""
        success, message = auth_manager.signup("testuser", "password123")
        
        assert success is True
        assert "successfully" in message.lower()
        assert "testuser" in message

    def test_signup_duplicate_username(self, auth_manager):
        """Test signup with an already existing username."""
        auth_manager.signup("testuser", "password123")
        success, message = auth_manager.signup("testuser", "newpassword")
        
        assert success is False
        assert "already exists" in message.lower()

    def test_signup_empty_username(self, auth_manager):
        """Test signup with empty username."""
        success, message = auth_manager.signup("", "password123")
        
        assert success is False
        assert "cannot be empty" in message.lower()

    def test_signup_empty_password(self, auth_manager):
        """Test signup with empty password."""
        success, message = auth_manager.signup("testuser", "")
        
        assert success is False
        assert "cannot be empty" in message.lower()

    def test_signup_username_too_short(self, auth_manager):
        """Test signup with username less than 3 characters."""
        success, message = auth_manager.signup("ab", "password123")
        
        assert success is False
        assert "3 characters" in message.lower()

    def test_signup_password_too_short(self, auth_manager):
        """Test signup with password less than 6 characters."""
        success, message = auth_manager.signup("testuser", "pass1")
        
        assert success is False
        assert "6 characters" in message.lower()

    def test_signup_min_valid_credentials(self, auth_manager):
        """Test signup with minimum valid credentials."""
        success, message = auth_manager.signup("abc", "123456")
        
        assert success is True
        assert "successfully" in message.lower()

    def test_signup_stores_hashed_password(self, auth_manager, temp_users_file):
        """Test that password is stored as hash, not plaintext."""
        auth_manager.signup("testuser", "mypassword")
        
        users = auth_manager._load_users()
        assert len(users) == 1
        assert users[0]["username"] == "testuser"
        # Verify password is hashed (SHA-256 hash should be 64 characters)
        assert len(users[0]["password"]) == 64
        assert users[0]["password"] != "mypassword"

    def test_signup_multiple_users(self, auth_manager):
        """Test signing up multiple different users."""
        success1, _ = auth_manager.signup("user1", "password1")
        success2, _ = auth_manager.signup("user2", "password2")
        success3, _ = auth_manager.signup("user3", "password3")
        
        assert success1 is True
        assert success2 is True
        assert success3 is True
        
        users = auth_manager._load_users()
        assert len(users) == 3

    def test_signup_special_characters_in_username(self, auth_manager):
        """Test signup with special characters in username."""
        success, message = auth_manager.signup("test_user-123", "password123")
        
        assert success is True

    def test_signup_unicode_username(self, auth_manager):
        """Test signup with unicode characters in username."""
        success, message = auth_manager.signup("用户123", "password123")
        
        assert success is True


class TestAuthManagerLogin:
    """Test cases for the login functionality."""

    @pytest.fixture
    def temp_users_file(self):
        """Create a temporary users file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        yield temp_path
        # Cleanup
        Path(temp_path).unlink(missing_ok=True)

    @pytest.fixture
    def auth_manager(self, temp_users_file):
        """Create an AuthManager instance with temp file."""
        return AuthManager(temp_users_file)

    def test_login_success(self, auth_manager):
        """Test successful login with correct credentials."""
        auth_manager.signup("testuser", "password123")
        success, message = auth_manager.login("testuser", "password123")
        
        assert success is True
        assert "welcome" in message.lower()
        assert "testuser" in message

    def test_login_invalid_password(self, auth_manager):
        """Test login with incorrect password."""
        auth_manager.signup("testuser", "password123")
        success, message = auth_manager.login("testuser", "wrongpassword")
        
        assert success is False
        assert "invalid password" in message.lower()

    def test_login_nonexistent_user(self, auth_manager):
        """Test login with non-existent username."""
        success, message = auth_manager.login("nonexistent", "password123")
        
        assert success is False
        assert "not found" in message.lower()

    def test_login_empty_username(self, auth_manager):
        """Test login with empty username."""
        success, message = auth_manager.login("", "password123")
        
        assert success is False
        assert "cannot be empty" in message.lower()

    def test_login_empty_password(self, auth_manager):
        """Test login with empty password."""
        success, message = auth_manager.login("testuser", "")
        
        assert success is False
        assert "cannot be empty" in message.lower()

    def test_login_case_sensitive_username(self, auth_manager):
        """Test that login username is case-sensitive."""
        auth_manager.signup("testuser", "password123")
        success, message = auth_manager.login("TestUser", "password123")
        
        assert success is False
        assert "not found" in message.lower()

    def test_login_after_multiple_signups(self, auth_manager):
        """Test login works correctly with multiple users."""
        auth_manager.signup("user1", "password1")
        auth_manager.signup("user2", "password2")
        auth_manager.signup("user3", "password3")
        
        # Verify each user can log in
        success1, _ = auth_manager.login("user1", "password1")
        success2, _ = auth_manager.login("user2", "password2")
        success3, _ = auth_manager.login("user3", "password3")
        
        assert success1 is True
        assert success2 is True
        assert success3 is True

    def test_login_wrong_user_password_pair(self, auth_manager):
        """Test login with wrong password for existing user."""
        auth_manager.signup("user1", "password1")
        auth_manager.signup("user2", "password2")
        
        # Try to login with user1's username but user2's password
        success, message = auth_manager.login("user1", "password2")
        
        assert success is False
        assert "invalid password" in message.lower()

    def test_login_with_special_characters_password(self, auth_manager):
        """Test login with special characters in password."""
        special_password = "p@ssw0rd!#$%"
        auth_manager.signup("testuser", special_password)
        success, message = auth_manager.login("testuser", special_password)
        
        assert success is True


class TestAuthManagerFileOperations:
    """Test cases for file operations in AuthManager."""

    @pytest.fixture
    def temp_users_file(self):
        """Create a temporary users file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        yield temp_path
        # Cleanup
        Path(temp_path).unlink(missing_ok=True)

    @pytest.fixture
    def auth_manager(self, temp_users_file):
        """Create an AuthManager instance with temp file."""
        return AuthManager(temp_users_file)

    def test_ensures_users_file_exists(self, temp_users_file):
        """Test that users.json is created if it doesn't exist."""
        Path(temp_users_file).unlink()  # Delete the file
        
        auth_manager = AuthManager(temp_users_file)
        
        assert Path(temp_users_file).exists()

    def test_users_file_contains_valid_json(self, auth_manager, temp_users_file):
        """Test that users.json contains valid JSON after signup."""
        auth_manager.signup("testuser", "password123")
        
        with open(temp_users_file, 'r') as f:
            data = json.load(f)
        
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["username"] == "testuser"

    def test_load_users_from_existing_file(self, temp_users_file):
        """Test loading users from an existing file."""
        # Write some data to the file
        test_data = [
            {"username": "user1", "password": "hash1"},
            {"username": "user2", "password": "hash2"}
        ]
        with open(temp_users_file, 'w') as f:
            json.dump(test_data, f)
        
        auth_manager = AuthManager(temp_users_file)
        users = auth_manager._load_users()
        
        assert len(users) == 2
        assert users[0]["username"] == "user1"
        assert users[1]["username"] == "user2"

    def test_persistence_across_instances(self, temp_users_file):
        """Test that data persists across different AuthManager instances."""
        # First instance: signup
        auth_manager1 = AuthManager(temp_users_file)
        auth_manager1.signup("testuser", "password123")
        
        # Second instance: verify user exists
        auth_manager2 = AuthManager(temp_users_file)
        success, message = auth_manager2.login("testuser", "password123")
        
        assert success is True

    def test_corrupt_json_file_handling(self, temp_users_file):
        """Test handling of corrupted JSON file."""
        # Write invalid JSON
        with open(temp_users_file, 'w') as f:
            f.write("{invalid json")
        
        auth_manager = AuthManager(temp_users_file)
        users = auth_manager._load_users()
        
        # Should return empty list instead of crashing
        assert isinstance(users, list)
        assert len(users) == 0


class TestAuthManagerPasswordHashing:
    """Test cases for password hashing functionality."""

    @pytest.fixture
    def temp_users_file(self):
        """Create a temporary users file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        yield temp_path
        # Cleanup
        Path(temp_path).unlink(missing_ok=True)

    @pytest.fixture
    def auth_manager(self, temp_users_file):
        """Create an AuthManager instance with temp file."""
        return AuthManager(temp_users_file)

    def test_same_password_produces_same_hash(self, auth_manager):
        """Test that same password always produces the same hash."""
        password = "mypassword"
        hash1 = auth_manager._hash_password(password)
        hash2 = auth_manager._hash_password(password)
        
        assert hash1 == hash2

    def test_different_passwords_produce_different_hashes(self, auth_manager):
        """Test that different passwords produce different hashes."""
        hash1 = auth_manager._hash_password("password1")
        hash2 = auth_manager._hash_password("password2")
        
        assert hash1 != hash2

    def test_hash_is_sha256(self, auth_manager):
        """Test that password hash is SHA-256 (64 hex characters)."""
        password_hash = auth_manager._hash_password("testpassword")
        
        # SHA-256 hash produces 64 hex characters
        assert len(password_hash) == 64
        # All characters should be valid hex
        assert all(c in '0123456789abcdef' for c in password_hash)


class TestAuthManagerEdgeCases:
    """Test cases for edge cases and boundary conditions."""

    @pytest.fixture
    def temp_users_file(self):
        """Create a temporary users file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        yield temp_path
        # Cleanup
        Path(temp_path).unlink(missing_ok=True)

    @pytest.fixture
    def auth_manager(self, temp_users_file):
        """Create an AuthManager instance with temp file."""
        return AuthManager(temp_users_file)

    def test_username_with_spaces(self, auth_manager):
        """Test signup with spaces in username."""
        # Spaces are allowed in usernames
        success, message = auth_manager.signup("test user", "password123")
        
        assert success is True

    def test_username_exactly_3_chars(self, auth_manager):
        """Test signup with exactly 3 character username."""
        success, message = auth_manager.signup("abc", "password123")
        
        assert success is True

    def test_password_exactly_6_chars(self, auth_manager):
        """Test signup with exactly 6 character password."""
        success, message = auth_manager.signup("testuser", "123456")
        
        assert success is True

    def test_very_long_username(self, auth_manager):
        """Test signup with very long username."""
        long_username = "a" * 256
        success, message = auth_manager.signup(long_username, "password123")
        
        assert success is True

    def test_very_long_password(self, auth_manager):
        """Test signup with very long password."""
        long_password = "p" * 256
        success, message = auth_manager.signup("testuser", long_password)
        
        assert success is True

    def test_whitespace_only_username(self, auth_manager):
        """Test signup with whitespace-only username."""
        success, message = auth_manager.signup("   ", "password123")
        
        # Whitespace should be stripped, resulting in empty username
        assert success is False

    def test_whitespace_only_password(self, auth_manager):
        """Test signup with whitespace-only password."""
        success, message = auth_manager.signup("testuser", "   ")
        
        # Whitespace should be treated as empty
        assert success is False
