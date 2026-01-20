"""Authentication manager for user sign up and login."""

import json
import os
from pathlib import Path


class AuthManager:
    """Manages user authentication (sign up and login)."""

    def __init__(self, users_file: str = "users.json"):
        """Initialize the AuthManager.
        
        Args:
            users_file: Path to the JSON file storing user data.
        """
        self.users_file = users_file
        self._ensure_users_file_exists()

    def _ensure_users_file_exists(self) -> None:
        """Create the users.json file if it doesn't exist."""
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump([], f)

    def _load_users(self) -> list:
        """Load users from the JSON file.
        
        Returns:
            List of user dictionaries.
        """
        try:
            with open(self.users_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_users(self, users: list) -> None:
        """Save users to the JSON file.
        
        Args:
            users: List of user dictionaries to save.
        """
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=2)

    def _user_exists(self, username: str) -> bool:
        """Check if a username already exists.
        
        Args:
            username: Username to check.
            
        Returns:
            True if username exists, False otherwise.
        """
        users = self._load_users()
        return any(user["username"] == username for user in users)

    def _validate_input(self, username: str, password: str) -> bool:
        """Validate that username and password are not empty or whitespace only.
        
        Args:
            username: Username to validate.
            password: Password to validate.
            
        Returns:
            True if both inputs are valid, False otherwise.
        """
        return bool(username.strip() and password.strip())

    def sign_up(self) -> bool:
        """Handle user sign up process.
        
        Prompts user for username and password, validates input,
        checks if username exists, and saves the new user.
        
        Returns:
            True if sign up was successful, False otherwise.
        """
        while True:
            username = input("Enter username: ")
            password = input("Enter password: ")

            # Validate input (not empty or whitespace only)
            if not self._validate_input(username, password):
                print("Error: Username and password cannot be empty or contain only spaces.")
                continue

            # Check if username already exists
            if self._user_exists(username):
                print(f"Error: Username '{username}' already exists. Please choose a different username.")
                continue

            # Save the new user
            users = self._load_users()
            users.append({"username": username.strip(), "password": password.strip()})
            self._save_users(users)

            print(f"Sign up successful! Welcome, {username}!")
            return True

    def login(self) -> str | None:
        """Handle user login process.
        
        Prompts user for username and password, validates input,
        and checks credentials against stored users.
        
        Returns:
            Username if login successful, None otherwise.
        """
        while True:
            username = input("Enter username: ")
            password = input("Enter password: ")

            # Validate input (not empty or whitespace only)
            if not self._validate_input(username, password):
                print("Error: Username and password cannot be empty or contain only spaces.")
                continue

            # Check credentials
            users = self._load_users()
            for user in users:
                if (
                    user["username"] == username.strip()
                    and user["password"] == password.strip()
                ):
                    print(f"Login successful! Welcome, {username}!")
                    return username.strip()

            # If we reach here, credentials are invalid
            print("Error: Invalid username or password. Please try again.")
