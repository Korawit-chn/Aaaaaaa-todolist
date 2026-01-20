"""Unit tests for the AuthManager class."""

import json
import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from src.auth import AuthManager


class TestAuthManager:
    """Test suite for AuthManager."""

    @pytest.fixture
    def temp_users_file(self):
        """Create a temporary users.json file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
            json.dump([], f)
        yield temp_file
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)

    @pytest.fixture
    def auth_manager(self, temp_users_file):
        """Create an AuthManager instance with a temporary users file."""
        return AuthManager(temp_users_file)

    # ================== Tests for users.json File ==================

    def test_users_file_created_if_not_exists(self):
        """Test that users.json is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            users_file = os.path.join(temp_dir, 'users.json')
            assert not os.path.exists(users_file)
            
            auth = AuthManager(users_file)
            
            assert os.path.exists(users_file)
            with open(users_file, 'r') as f:
                data = json.load(f)
                assert data == []

    def test_users_file_not_overwritten_if_exists(self, temp_users_file):
        """Test that existing users.json is not overwritten."""
        test_data = [{"username": "existing_user", "password": "pass123"}]
        with open(temp_users_file, 'w') as f:
            json.dump(test_data, f)
        
        auth = AuthManager(temp_users_file)
        users = auth._load_users()
        
        assert len(users) == 1
        assert users[0]["username"] == "existing_user"

    # ================== Tests for Sign Up ==================

    @patch('builtins.input')
    def test_sign_up_successful(self, mock_input, auth_manager, temp_users_file):
        """Test successful user sign up."""
        mock_input.side_effect = ['newuser', 'password123']
        
        result = auth_manager.sign_up()
        
        assert result is True
        users = auth_manager._load_users()
        assert len(users) == 1
        assert users[0]['username'] == 'newuser'
        assert users[0]['password'] == 'password123'

    @patch('builtins.input')
    def test_sign_up_rejects_empty_username(self, mock_input, auth_manager, capsys):
        """Test that sign up rejects empty username."""
        mock_input.side_effect = ['', 'password123', 'validuser', 'password123']
        
        result = auth_manager.sign_up()
        
        assert result is True
        captured = capsys.readouterr()
        assert 'cannot be empty' in captured.out.lower()

    @patch('builtins.input')
    def test_sign_up_rejects_empty_password(self, mock_input, auth_manager, capsys):
        """Test that sign up rejects empty password."""
        mock_input.side_effect = ['username', '', 'username', 'password123']
        
        result = auth_manager.sign_up()
        
        assert result is True
        captured = capsys.readouterr()
        assert 'cannot be empty' in captured.out.lower()

    @patch('builtins.input')
    def test_sign_up_rejects_whitespace_only_username(self, mock_input, auth_manager, capsys):
        """Test that sign up rejects whitespace-only username."""
        mock_input.side_effect = ['   ', 'password123', 'validuser', 'password123']
        
        result = auth_manager.sign_up()
        
        assert result is True
        captured = capsys.readouterr()
        assert 'cannot be empty' in captured.out.lower()

    @patch('builtins.input')
    def test_sign_up_rejects_whitespace_only_password(self, mock_input, auth_manager, capsys):
        """Test that sign up rejects whitespace-only password."""
        mock_input.side_effect = ['username', '\t\n', 'username', 'password123']
        
        result = auth_manager.sign_up()
        
        assert result is True
        captured = capsys.readouterr()
        assert 'cannot be empty' in captured.out.lower()

    @patch('builtins.input')
    def test_sign_up_rejects_duplicate_username(self, mock_input, auth_manager, capsys):
        """Test that sign up rejects duplicate usernames."""
        # First sign up - create testuser
        mock_input.side_effect = ['testuser', 'password123']
        auth_manager.sign_up()
        
        # Try to sign up with duplicate username, then with a new one
        mock_input.side_effect = ['testuser', 'different_pass', 'newuser', 'password456']
        result = auth_manager.sign_up()
        
        assert result is True
        users = auth_manager._load_users()
        assert len(users) == 2
        assert users[0]['username'] == 'testuser'
        assert users[1]['username'] == 'newuser'
        
        captured = capsys.readouterr()
        assert 'already exists' in captured.out.lower()

    @patch('builtins.input')
    def test_sign_up_strips_whitespace(self, mock_input, auth_manager):
        """Test that sign up strips leading and trailing whitespace."""
        mock_input.side_effect = ['  newuser  ', '  password123  ']
        
        result = auth_manager.sign_up()
        
        assert result is True
        users = auth_manager._load_users()
        assert users[0]['username'] == 'newuser'
        assert users[0]['password'] == 'password123'

    @patch('builtins.input')
    def test_sign_up_multiple_users(self, mock_input, auth_manager):
        """Test signing up multiple users."""
        mock_input.side_effect = ['user1', 'pass1', 'user2', 'pass2']
        
        auth_manager.sign_up()
        
        users = auth_manager._load_users()
        assert len(users) == 1  # Only one successful sign up in this call
        
        # Reset and sign up another user
        mock_input.side_effect = ['user2', 'pass2']
        auth_manager.sign_up()
        
        users = auth_manager._load_users()
        assert len(users) == 2

    # ================== Tests for Login ==================

    @patch('builtins.input')
    def test_login_successful(self, mock_input, auth_manager):
        """Test successful login."""
        # First create a user
        mock_input.side_effect = ['testuser', 'password123', 'testuser', 'password123']
        auth_manager.sign_up()
        
        # Now login
        mock_input.side_effect = ['testuser', 'password123']
        username = auth_manager.login()
        
        assert username == 'testuser'

    @patch('builtins.input')
    def test_login_rejects_empty_username(self, mock_input, auth_manager, capsys):
        """Test that login rejects empty username."""
        # First create a user
        auth_manager._save_users([{"username": "validuser", "password": "password"}])
        
        # Try login with empty username, then valid credentials
        mock_input.side_effect = ['', 'password', 'validuser', 'password']
        username = auth_manager.login()
        
        assert username == 'validuser'
        captured = capsys.readouterr()
        assert 'cannot be empty' in captured.out.lower()

    @patch('builtins.input')
    def test_login_rejects_empty_password(self, mock_input, auth_manager, capsys):
        """Test that login rejects empty password."""
        # First create a user
        auth_manager._save_users([{"username": "validuser", "password": "password"}])
        
        # Try login with empty password, then valid credentials
        mock_input.side_effect = ['validuser', '', 'validuser', 'password']
        username = auth_manager.login()
        
        assert username == 'validuser'
        captured = capsys.readouterr()
        assert 'cannot be empty' in captured.out.lower()

    @patch('builtins.input')
    def test_login_rejects_whitespace_only_username(self, mock_input, auth_manager, capsys):
        """Test that login rejects whitespace-only username."""
        # First create a user
        auth_manager._save_users([{"username": "validuser", "password": "password"}])
        
        # Try login with whitespace-only username, then valid credentials
        mock_input.side_effect = ['   ', 'password', 'validuser', 'password']
        username = auth_manager.login()
        
        assert username == 'validuser'
        captured = capsys.readouterr()
        assert 'cannot be empty' in captured.out.lower()

    @patch('builtins.input')
    def test_login_rejects_whitespace_only_password(self, mock_input, auth_manager, capsys):
        """Test that login rejects whitespace-only password."""
        # First create a user
        auth_manager._save_users([{"username": "validuser", "password": "password"}])
        
        # Try login with whitespace-only password, then valid credentials
        mock_input.side_effect = ['validuser', '   ', 'validuser', 'password']
        username = auth_manager.login()
        
        assert username == 'validuser'
        captured = capsys.readouterr()
        assert 'cannot be empty' in captured.out.lower()

    @patch('builtins.input')
    def test_login_fails_with_wrong_password(self, mock_input, auth_manager, capsys):
        """Test that login fails with wrong password."""
        # Create user
        mock_input.side_effect = ['testuser', 'correct_pass', 'testuser', 'wrong_pass']
        auth_manager.sign_up()
        
        # Try to login with wrong password
        mock_input.side_effect = ['testuser', 'wrong_pass', 'testuser', 'correct_pass']
        username = auth_manager.login()
        
        assert username == 'testuser'
        captured = capsys.readouterr()
        assert 'invalid username or password' in captured.out.lower()

    @patch('builtins.input')
    def test_login_fails_with_nonexistent_user(self, mock_input, auth_manager, capsys):
        """Test that login fails with non-existent username."""
        # First create a user
        auth_manager._save_users([{"username": "testuser", "password": "password"}])
        
        # Try login with non-existent user, then with valid user
        mock_input.side_effect = ['nonexistent', 'password', 'testuser', 'password']
        username = auth_manager.login()
        
        assert username == 'testuser'
        captured = capsys.readouterr()
        assert 'invalid username or password' in captured.out.lower()

    @patch('builtins.input')
    def test_login_strips_whitespace(self, mock_input, auth_manager):
        """Test that login strips leading and trailing whitespace."""
        # Create user
        mock_input.side_effect = ['testuser', 'password123', '  testuser  ', '  password123  ']
        auth_manager.sign_up()
        
        # Login with whitespace
        mock_input.side_effect = ['  testuser  ', '  password123  ']
        username = auth_manager.login()
        
        assert username == 'testuser'

    # ================== Tests for Helper Methods ==================

    def test_user_exists_true(self, auth_manager):
        """Test _user_exists returns True for existing user."""
        auth_manager._save_users([{"username": "testuser", "password": "pass"}])
        
        assert auth_manager._user_exists("testuser") is True

    def test_user_exists_false(self, auth_manager):
        """Test _user_exists returns False for non-existent user."""
        auth_manager._save_users([{"username": "testuser", "password": "pass"}])
        
        assert auth_manager._user_exists("otheruser") is False

    def test_validate_input_valid(self, auth_manager):
        """Test _validate_input with valid input."""
        assert auth_manager._validate_input("testuser", "password") is True

    def test_validate_input_empty_username(self, auth_manager):
        """Test _validate_input with empty username."""
        assert auth_manager._validate_input("", "password") is False

    def test_validate_input_empty_password(self, auth_manager):
        """Test _validate_input with empty password."""
        assert auth_manager._validate_input("username", "") is False

    def test_validate_input_whitespace_username(self, auth_manager):
        """Test _validate_input with whitespace-only username."""
        assert auth_manager._validate_input("   ", "password") is False

    def test_validate_input_whitespace_password(self, auth_manager):
        """Test _validate_input with whitespace-only password."""
        assert auth_manager._validate_input("username", "   ") is False

    def test_load_and_save_users(self, auth_manager):
        """Test _load_users and _save_users methods."""
        test_users = [
            {"username": "user1", "password": "pass1"},
            {"username": "user2", "password": "pass2"},
        ]
        
        auth_manager._save_users(test_users)
        loaded_users = auth_manager._load_users()
        
        assert len(loaded_users) == 2
        assert loaded_users[0]["username"] == "user1"
        assert loaded_users[1]["username"] == "user2"

    def test_load_users_empty_file(self, auth_manager):
        """Test _load_users with empty file."""
        users = auth_manager._load_users()
        assert users == []

    def test_load_users_invalid_json(self, temp_users_file):
        """Test _load_users with invalid JSON file."""
        with open(temp_users_file, 'w') as f:
            f.write("invalid json {{{")
        
        auth = AuthManager(temp_users_file)
        users = auth._load_users()
        
        assert users == []
