"""Managers for handling application logic and data persistence."""

import json
import os
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from models import TodoItem, Priority, Status


class TodoManager:
    """Manages todo items and their persistence to JSON."""

    def __init__(self, data_dir: str = "data"):
        """Initialize TodoManager with a data directory."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.todos_file = self.data_dir / "todos.json"

    def create_todo(
        self,
        title: str,
        details: str,
        priority: Priority,
        owner: str,
    ) -> TodoItem:
        """Create a new todo item and save it."""
        # Assign a sequential numeric ID (stored as string) starting from 1.
        todo_id = self._get_next_id()

        todo = TodoItem(
            id=todo_id,
            title=title,
            details=details,
            priority=priority,
            status=Status.PENDING,
            owner=owner,
        )
        self._save_todo(todo)
        return todo

    def _get_next_id(self) -> str:
        """Return the next numeric ID as a string.

        This scans existing todos for numeric IDs and returns max+1.
        Non-numeric IDs are ignored.
        """
        todos = self._load_all_todos()
        max_id = 0
        for todo in todos:
            try:
                val = int(todo.id)
            except Exception:
                continue
            if val > max_id:
                max_id = val
        return str(max_id + 1)

    def get_todos_by_owner(self, owner: str) -> List[TodoItem]:
        """Retrieve all todos for a specific owner."""
        todos = self._load_all_todos()
        return [todo for todo in todos if todo.owner == owner]

    def get_all_todos(self) -> List[TodoItem]:
        """Return all todos stored in the system."""
        return self._load_all_todos()

    def get_todo_by_id(self, todo_id: str) -> Optional[TodoItem]:
        """Retrieve a specific todo by ID."""
        todos = self._load_all_todos()
        for todo in todos:
            if todo.id == todo_id:
                return todo
        return None

    def update_todo(self, todo: TodoItem) -> None:
        """Update an existing todo item."""
        todo.updated_at = datetime.now().isoformat()
        todos = self._load_all_todos()
        # Replace the todo with the same ID
        updated_todos = [t for t in todos if t.id != todo.id]
        updated_todos.append(todo)
        self._save_all_todos(updated_todos)

    def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo item by ID."""
        todos = self._load_all_todos()
        original_len = len(todos)
        todos = [todo for todo in todos if todo.id != todo_id]
        if len(todos) < original_len:
            self._save_all_todos(todos)
            return True
        return False

    def mark_as_completed(self, todo_id: str, owner: str) -> bool:
        """Mark a todo as completed if it exists and belongs to the owner.

        Returns True if updated, False otherwise.
        """
        todos = self._load_all_todos()
        for todo in todos:
            if todo.id == todo_id:
                if todo.owner != owner:
                    return False
                todo.status = Status.COMPLETED
                todo.updated_at = datetime.now().isoformat()
                self._save_all_todos(todos)
                return True
        return False

    def _load_all_todos(self) -> List[TodoItem]:
        """Load all todos from the JSON file."""
        if not self.todos_file.exists():
            return []
        with open(self.todos_file, "r") as f:
            data = json.load(f)
        return [TodoItem.from_dict(item) for item in data]

    def _save_todo(self, todo: TodoItem) -> None:
        """Save a todo item to the JSON file."""
        todos = self._load_all_todos()
        todos.append(todo)
        self._save_all_todos(todos)

    def _save_all_todos(self, todos: List[TodoItem]) -> None:
        """Save all todos to the JSON file."""
        with open(self.todos_file, "w") as f:
            json.dump([todo.to_dict() for todo in todos], f, indent=2)


class AuthManager:
    """Manages user authentication and persistence."""

    def __init__(self, data_dir: str = "data"):
        """Initialize AuthManager with a data directory."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.users_file = self.data_dir / "users.json"

    def sign_up(self, username: str, password: str) -> bool:
        """Register a new user."""
        if not username or not password:
            return False
        if self.user_exists(username):
            return False
        users = self._load_users()
        users[username] = password
        self._save_users(users)
        return True

    def login(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        users = self._load_users()
        return users.get(username) == password

    def user_exists(self, username: str) -> bool:
        """Check if a user exists."""
        users = self._load_users()
        return username in users

    def _load_users(self) -> dict:
        """Load all users from the JSON file."""
        if not self.users_file.exists():
            return {}
        with open(self.users_file, "r") as f:
            return json.load(f)

    def _save_users(self, users: dict) -> None:
        """Save all users to the JSON file."""
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=2)
