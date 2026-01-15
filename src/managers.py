"""Manager classes for authentication and todo operations."""

import json
import os
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from models import TodoItem, Priority, Status


class AuthManager:
    """Manages user authentication and storage."""

    def __init__(self, users_file: str = "users.json"):
        """Initialize the AuthManager.
        
        Args:
            users_file: Path to the users JSON file.
        """
        self.users_file = users_file
        self._ensure_users_file()

    def _ensure_users_file(self) -> None:
        """Ensure the users JSON file exists."""
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump({}, f)

    def _load_users(self) -> dict:
        """Load users from JSON file."""
        try:
            with open(self.users_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_users(self, users: dict) -> None:
        """Save users to JSON file."""
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=2)

    def sign_up(self, username: str, password: str) -> bool:
        """Register a new user.
        
        Args:
            username: The username for the new account.
            password: The password for the new account.
            
        Returns:
            True if sign-up was successful, False if user already exists.
        """
        if not username or not password:
            return False

        users = self._load_users()

        if username in users:
            print(f"Error: Username '{username}' already exists.")
            return False

        users[username] = password
        self._save_users(users)
        print(f"Success: User '{username}' registered successfully!")
        return True

    def login(self, username: str, password: str) -> bool:
        """Authenticate a user.
        
        Args:
            username: The username to log in.
            password: The password for authentication.
            
        Returns:
            True if login was successful, False otherwise.
        """
        if not username or not password:
            return False

        users = self._load_users()

        if username not in users:
            print(f"Error: Username '{username}' not found.")
            return False

        if users[username] != password:
            print("Error: Invalid password.")
            return False

        print(f"Success: Logged in as '{username}'!")
        return True

    def user_exists(self, username: str) -> bool:
        """Check if a user exists.
        
        Args:
            username: The username to check.
            
        Returns:
            True if user exists, False otherwise.
        """
        users = self._load_users()
        return username in users


class TodoManager:
    """Manages todo items and persistence."""

    def __init__(self, todos_file: str = "todos.json"):
        """Initialize the TodoManager.
        
        Args:
            todos_file: Path to the todos JSON file.
        """
        self.todos_file = todos_file
        self._ensure_todos_file()

    def _ensure_todos_file(self) -> None:
        """Ensure the todos JSON file exists."""
        if not os.path.exists(self.todos_file):
            with open(self.todos_file, "w") as f:
                json.dump([], f)

    def _load_todos(self) -> List[dict]:
        """Load todos from JSON file."""
        try:
            with open(self.todos_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_todos(self, todos: List[dict]) -> None:
        """Save todos to JSON file."""
        with open(self.todos_file, "w") as f:
            json.dump(todos, f, indent=2)

    def create_todo(self, title: str, details: str, priority: str, owner: str) -> Optional[TodoItem]:
        """Create a new todo item.
        
        Args:
            title: The todo title.
            details: The todo details.
            priority: Priority level (HIGH, MID, LOW).
            owner: Username of the todo owner.
            
        Returns:
            The created TodoItem, or None if validation fails.
        """
        if not title or not owner:
            print("Error: Title and owner are required.")
            return None

        try:
            priority_enum = Priority[priority.upper()]
        except KeyError:
            print(f"Error: Invalid priority. Use HIGH, MID, or LOW.")
            return None

        todo_item = TodoItem(
            title=title,
            details=details,
            priority=priority_enum,
            owner=owner
        )

        todos = self._load_todos()
        todos.append(todo_item.to_dict())
        self._save_todos(todos)
        print(f"Success: Todo '{title}' created!")
        return todo_item

    def get_all_todos(self, owner: Optional[str] = None) -> List[TodoItem]:
        """Get all todo items, optionally filtered by owner.
        
        Args:
            owner: Optional username to filter todos by owner.
            
        Returns:
            List of TodoItem objects.
        """
        todos_data = self._load_todos()
        todos = [TodoItem.from_dict(data) for data in todos_data]

        if owner:
            todos = [todo for todo in todos if todo.owner == owner]

        return todos

    def get_todo_by_id(self, todo_id: str) -> Optional[TodoItem]:
        """Get a specific todo by ID.
        
        Args:
            todo_id: The todo ID.
            
        Returns:
            The TodoItem if found, None otherwise.
        """
        todos_data = self._load_todos()
        for data in todos_data:
            if data["id"] == todo_id:
                return TodoItem.from_dict(data)
        return None

    def update_todo(self, todo_id: str, **kwargs) -> bool:
        """Update a todo item.
        
        Args:
            todo_id: The todo ID to update.
            **kwargs: Fields to update (title, details, priority, status).
            
        Returns:
            True if update was successful, False otherwise.
        """
        todos_data = self._load_todos()
        updated = False

        for data in todos_data:
            if data["id"] == todo_id:
                if "title" in kwargs:
                    data["title"] = kwargs["title"]
                if "details" in kwargs:
                    data["details"] = kwargs["details"]
                if "priority" in kwargs:
                    try:
                        data["priority"] = Priority[kwargs["priority"].upper()].value
                    except KeyError:
                        print("Error: Invalid priority.")
                        return False
                if "status" in kwargs:
                    try:
                        data["status"] = Status[kwargs["status"].upper()].value
                    except KeyError:
                        print("Error: Invalid status.")
                        return False
                data["updated_at"] = datetime.now().isoformat()
                updated = True
                break

        if updated:
            self._save_todos(todos_data)
            print("Success: Todo updated!")
            return True

        print("Error: Todo not found.")
        return False

    def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo item.
        
        Args:
            todo_id: The todo ID to delete.
            
        Returns:
            True if deletion was successful, False otherwise.
        """
        todos_data = self._load_todos()
        initial_length = len(todos_data)
        todos_data = [todo for todo in todos_data if todo["id"] != todo_id]

        if len(todos_data) < initial_length:
            self._save_todos(todos_data)
            print("Success: Todo deleted!")
            return True

        print("Error: Todo not found.")
        return False

    def mark_completed(self, todo_id: str) -> bool:
        """Mark a todo as completed.
        
        Args:
            todo_id: The todo ID to mark as completed.
            
        Returns:
            True if successful, False otherwise.
        """
        return self.update_todo(todo_id, status="COMPLETED")
