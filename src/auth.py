"""Authentication manager for user login and signup."""

import json
import hashlib
from pathlib import Path
from typing import Optional


class AuthManager:
    """Manages user authentication including signup and login."""

    def __init__(self, users_file: str = "users.json"):
        """Initialize the AuthManager.
        
        Args:
            users_file: Path to the JSON file storing user data.
        """
        self.users_file = Path(users_file)
        self._ensure_users_file()

    def _ensure_users_file(self) -> None:
        """Create users.json file if it doesn't exist."""
        if not self.users_file.exists():
            self.users_file.write_text(json.dumps([]))

    def _load_users(self) -> list[dict]:
        """Load users from JSON file.
        
        Returns:
            List of user dictionaries.
        """
        try:
            content = self.users_file.read_text()
            return json.loads(content) if content else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_users(self, users: list[dict]) -> None:
        """Save users to JSON file.
        
        Args:
            users: List of user dictionaries to save.
        """
        self.users_file.write_text(json.dumps(users, indent=2))

    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256.
        
        Args:
            password: Plain text password.
            
        Returns:
            Hashed password.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def _user_exists(self, username: str) -> bool:
        """Check if a user already exists.
        
        Args:
            username: Username to check.
            
        Returns:
            True if user exists, False otherwise.
        """
        users = self._load_users()
        return any(user["username"] == username for user in users)

    def signup(self, username: str, password: str) -> tuple[bool, str]:
        """Register a new user.
        
        Args:
            username: Username for the new account.
            password: Password for the new account.
            
        Returns:
            Tuple of (success: bool, message: str).
        """
        # Strip whitespace
        username = username.strip()
        password = password.strip()
        
        # Validation
        if not username or not password:
            return False, "Username and password cannot be empty."
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long."
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        
        if self._user_exists(username):
            return False, f"Username '{username}' already exists."
        
        # Add new user
        users = self._load_users()
        users.append({
            "username": username,
            "password": self._hash_password(password)
        })
        self._save_users(users)
        
        return True, f"Account created successfully for '{username}'!"

    def login(self, username: str, password: str) -> tuple[bool, str]:
        """Authenticate a user.
        
        Args:
            username: Username to login.
            password: Password to verify.
            
        Returns:
            Tuple of (success: bool, message: str).
        """
        # Strip whitespace
        username = username.strip()
        password = password.strip()
        
        if not username or not password:
            return False, "Username and password cannot be empty."
        
        users = self._load_users()
        for user in users:
            if user["username"] == username:
                if user["password"] == self._hash_password(password):
                    return True, f"Welcome back, {username}!"
                else:
                    return False, "Invalid password."
        
        return False, f"User '{username}' not found."
