"""Unit tests for Task 4: Create and edit a to-do-list item.

This module tests the following functionalities:
- Create a new to-do item after login
- View your own to-do items
- Edit your existing to-do items
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models import TodoItem, Priority, Status
from managers import TodoManager


class TestTodoCreation:
    """Tests for creating new todo items."""

    def test_create_todo_with_valid_data(self, temp_data_dir):
        """Test creating a new todo item with valid data."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todo = manager.create_todo(
            title="Test Todo",
            details="This is a test todo",
            priority=Priority.HIGH,
            owner="testuser"
        )
        
        assert todo.title == "Test Todo"
        assert todo.details == "This is a test todo"
        assert todo.priority == Priority.HIGH
        assert todo.status == Status.PENDING
        assert todo.owner == "testuser"
        assert todo.id is not None
        assert todo.created_at is not None
        assert todo.updated_at is not None

    def test_create_todo_with_different_priorities(self, temp_data_dir):
        """Test creating todos with different priority levels."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        priorities = [Priority.HIGH, Priority.MID, Priority.LOW]
        
        for priority in priorities:
            todo = manager.create_todo(
                title=f"Todo with {priority.value} priority",
                details="Test details",
                priority=priority,
                owner="testuser"
            )
            assert todo.priority == priority

    def test_create_todo_with_empty_details(self, temp_data_dir):
        """Test creating a todo with empty details."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todo = manager.create_todo(
            title="Todo without details",
            details="",
            priority=Priority.MID,
            owner="testuser"
        )
        
        assert todo.title == "Todo without details"
        assert todo.details == ""

    def test_create_multiple_todos(self, temp_data_dir):
        """Test creating multiple todos."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todos = []
        for i in range(5):
            todo = manager.create_todo(
                title=f"Todo {i+1}",
                details=f"Details for todo {i+1}",
                priority=Priority.MID,
                owner="testuser"
            )
            todos.append(todo)
        
        assert len(todos) == 5
        # Verify all have unique IDs
        ids = [todo.id for todo in todos]
        assert len(set(ids)) == 5

    def test_create_todo_sets_default_status_to_pending(self, temp_data_dir):
        """Test that newly created todos have PENDING status."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todo = manager.create_todo(
            title="New Todo",
            details="Details",
            priority=Priority.LOW,
            owner="testuser"
        )
        
        assert todo.status == Status.PENDING

    def test_create_todo_persists_to_file(self, temp_data_dir):
        """Test that created todos are persisted to file."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todo = manager.create_todo(
            title="Persistent Todo",
            details="Should be saved",
            priority=Priority.HIGH,
            owner="testuser"
        )
        
        # Create a new manager instance to load from file
        new_manager = TodoManager(data_dir=temp_data_dir)
        todos = new_manager.get_todos_by_owner("testuser")
        
        assert len(todos) == 1
        assert todos[0].id == todo.id
        assert todos[0].title == "Persistent Todo"


class TestTodoViewing:
    """Tests for viewing todo items."""

    def test_get_todos_by_owner_single_user(self, temp_data_dir):
        """Test retrieving todos for a specific owner."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        # Create todos for testuser
        manager.create_todo("Todo 1", "Details 1", Priority.HIGH, "testuser")
        manager.create_todo("Todo 2", "Details 2", Priority.MID, "testuser")
        
        todos = manager.get_todos_by_owner("testuser")
        
        assert len(todos) == 2
        assert all(todo.owner == "testuser" for todo in todos)

    def test_get_todos_by_owner_multiple_users(self, temp_data_dir):
        """Test that todos are correctly filtered by owner."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        # Create todos for different users
        manager.create_todo("User1 Todo 1", "Details", Priority.HIGH, "user1")
        manager.create_todo("User1 Todo 2", "Details", Priority.MID, "user1")
        manager.create_todo("User2 Todo 1", "Details", Priority.LOW, "user2")
        
        user1_todos = manager.get_todos_by_owner("user1")
        user2_todos = manager.get_todos_by_owner("user2")
        
        assert len(user1_todos) == 2
        assert len(user2_todos) == 1
        assert all(todo.owner == "user1" for todo in user1_todos)
        assert all(todo.owner == "user2" for todo in user2_todos)

    def test_get_todos_by_owner_no_todos(self, temp_data_dir):
        """Test retrieving todos when user has none."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todos = manager.get_todos_by_owner("nonexistent")
        
        assert todos == []

    def test_get_todos_by_owner_returns_all_fields(self, temp_data_dir):
        """Test that retrieved todos contain all required fields."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        manager.create_todo(
            title="Complete Todo",
            details="All fields test",
            priority=Priority.HIGH,
            owner="testuser"
        )
        
        todos = manager.get_todos_by_owner("testuser")
        todo = todos[0]
        
        assert hasattr(todo, 'id')
        assert hasattr(todo, 'title')
        assert hasattr(todo, 'details')
        assert hasattr(todo, 'priority')
        assert hasattr(todo, 'status')
        assert hasattr(todo, 'owner')
        assert hasattr(todo, 'created_at')
        assert hasattr(todo, 'updated_at')

    def test_get_todo_by_id_existing_todo(self, temp_data_dir):
        """Test retrieving a todo by its ID."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        created_todo = manager.create_todo(
            title="Find Me",
            details="By ID",
            priority=Priority.MID,
            owner="testuser"
        )
        
        retrieved_todo = manager.get_todo_by_id(created_todo.id)
        
        assert retrieved_todo is not None
        assert retrieved_todo.id == created_todo.id
        assert retrieved_todo.title == "Find Me"

    def test_get_todo_by_id_nonexistent_todo(self, temp_data_dir):
        """Test retrieving a todo that doesn't exist."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        retrieved_todo = manager.get_todo_by_id("nonexistent-id")
        
        assert retrieved_todo is None


class TestTodoEditing:
    """Tests for editing todo items."""

    def test_edit_todo_title(self, temp_data_dir):
        """Test editing a todo's title."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todo = manager.create_todo(
            title="Original Title",
            details="Details",
            priority=Priority.HIGH,
            owner="testuser"
        )
        
        todo.title = "Updated Title"
        manager.update_todo(todo)
        
        updated_todo = manager.get_todo_by_id(todo.id)
        assert updated_todo.title == "Updated Title"

    def test_edit_todo_details(self, temp_data_dir):
        """Test editing a todo's details."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todo = manager.create_todo(
            title="Title",
            details="Original details",
            priority=Priority.MID,
            owner="testuser"
        )
        
        todo.details = "Updated details"
        manager.update_todo(todo)
        
        updated_todo = manager.get_todo_by_id(todo.id)
        assert updated_todo.details == "Updated details"

    def test_edit_todo_priority(self, temp_data_dir):
        """Test editing a todo's priority."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todo = manager.create_todo(
            title="Title",
            details="Details",
            priority=Priority.LOW,
            owner="testuser"
        )
        
        todo.priority = Priority.HIGH
        manager.update_todo(todo)
        
        updated_todo = manager.get_todo_by_id(todo.id)
        assert updated_todo.priority == Priority.HIGH

    def test_edit_todo_status(self, temp_data_dir):
        """Test editing a todo's status."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todo = manager.create_todo(
            title="Title",
            details="Details",
            priority=Priority.MID,
            owner="testuser"
        )
        
        assert todo.status == Status.PENDING
        
        todo.status = Status.COMPLETED
        manager.update_todo(todo)
        
        updated_todo = manager.get_todo_by_id(todo.id)
        assert updated_todo.status == Status.COMPLETED

    def test_edit_multiple_fields(self, temp_data_dir):
        """Test editing multiple fields of a todo."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todo = manager.create_todo(
            title="Original Title",
            details="Original details",
            priority=Priority.LOW,
            owner="testuser"
        )
        
        # Update multiple fields
        todo.title = "New Title"
        todo.details = "New details"
        todo.priority = Priority.HIGH
        todo.status = Status.COMPLETED
        manager.update_todo(todo)
        
        updated_todo = manager.get_todo_by_id(todo.id)
        assert updated_todo.title == "New Title"
        assert updated_todo.details == "New details"
        assert updated_todo.priority == Priority.HIGH
        assert updated_todo.status == Status.COMPLETED

    def test_edit_updates_updated_at_timestamp(self, temp_data_dir):
        """Test that updating a todo updates the updated_at timestamp."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todo = manager.create_todo(
            title="Title",
            details="Details",
            priority=Priority.MID,
            owner="testuser"
        )
        
        original_updated_at = todo.updated_at
        
        # Update the todo
        import time
        time.sleep(0.1)  # Small delay to ensure timestamp changes
        todo.title = "Updated Title"
        manager.update_todo(todo)
        
        updated_todo = manager.get_todo_by_id(todo.id)
        assert updated_todo.updated_at != original_updated_at

    def test_edit_preserves_created_at_timestamp(self, temp_data_dir):
        """Test that editing a todo preserves its created_at timestamp."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todo = manager.create_todo(
            title="Title",
            details="Details",
            priority=Priority.MID,
            owner="testuser"
        )
        
        original_created_at = todo.created_at
        
        # Update the todo
        todo.title = "Updated Title"
        manager.update_todo(todo)
        
        updated_todo = manager.get_todo_by_id(todo.id)
        assert updated_todo.created_at == original_created_at

    def test_edit_preserves_owner(self, temp_data_dir):
        """Test that editing a todo preserves its owner."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todo = manager.create_todo(
            title="Title",
            details="Details",
            priority=Priority.MID,
            owner="testuser"
        )
        
        # Update the todo
        todo.title = "Updated Title"
        manager.update_todo(todo)
        
        updated_todo = manager.get_todo_by_id(todo.id)
        assert updated_todo.owner == "testuser"

    def test_edit_preserves_todo_id(self, temp_data_dir):
        """Test that editing a todo preserves its ID."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todo = manager.create_todo(
            title="Title",
            details="Details",
            priority=Priority.MID,
            owner="testuser"
        )
        
        original_id = todo.id
        
        # Update the todo
        todo.title = "Updated Title"
        manager.update_todo(todo)
        
        updated_todo = manager.get_todo_by_id(todo.id)
        assert updated_todo.id == original_id

    def test_edit_todo_does_not_duplicate(self, temp_data_dir):
        """Test that editing a todo doesn't create duplicates."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        todo = manager.create_todo(
            title="Title",
            details="Details",
            priority=Priority.MID,
            owner="testuser"
        )
        
        # Update the todo multiple times
        for i in range(3):
            todo.title = f"Updated Title {i}"
            manager.update_todo(todo)
        
        todos = manager.get_todos_by_owner("testuser")
        assert len(todos) == 1
        assert todos[0].title == "Updated Title 2"


class TestTodoItemModel:
    """Tests for the TodoItem model."""

    def test_todo_item_creation(self):
        """Test creating a TodoItem directly."""
        todo = TodoItem(
            title="Test",
            details="Test details",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser"
        )
        
        assert todo.title == "Test"
        assert todo.details == "Test details"
        assert todo.priority == Priority.HIGH
        assert todo.status == Status.PENDING
        assert todo.owner == "testuser"

    def test_todo_item_to_dict(self):
        """Test converting TodoItem to dictionary."""
        todo = TodoItem(
            id="test-id",
            title="Test",
            details="Details",
            priority=Priority.MID,
            status=Status.COMPLETED,
            owner="testuser"
        )
        
        todo_dict = todo.to_dict()
        
        assert todo_dict["id"] == "test-id"
        assert todo_dict["title"] == "Test"
        assert todo_dict["details"] == "Details"
        assert todo_dict["priority"] == "MID"
        assert todo_dict["status"] == "COMPLETED"
        assert todo_dict["owner"] == "testuser"

    def test_todo_item_from_dict(self):
        """Test creating TodoItem from dictionary."""
        data = {
            "id": "test-id",
            "title": "Test",
            "details": "Details",
            "priority": "HIGH",
            "status": "PENDING",
            "owner": "testuser",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
        
        todo = TodoItem.from_dict(data)
        
        assert todo.id == "test-id"
        assert todo.title == "Test"
        assert todo.details == "Details"
        assert todo.priority == Priority.HIGH
        assert todo.status == Status.PENDING
        assert todo.owner == "testuser"

    def test_todo_item_default_values(self):
        """Test TodoItem default values."""
        todo = TodoItem()
        
        assert todo.title == ""
        assert todo.details == ""
        assert todo.priority == Priority.MID
        assert todo.status == Status.PENDING
        assert todo.owner == ""
        assert todo.id is not None  # Should have a UUID
        assert todo.created_at is not None
        assert todo.updated_at is not None


class TestIntegrationCreateEditView:
    """Integration tests for create, edit, and view workflows."""

    def test_create_view_and_edit_workflow(self, temp_data_dir):
        """Test the complete workflow: create, view, and edit a todo."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        # Create a todo
        todo = manager.create_todo(
            title="Complete Workflow",
            details="Testing full workflow",
            priority=Priority.LOW,
            owner="testuser"
        )
        
        # View the todo
        todos = manager.get_todos_by_owner("testuser")
        assert len(todos) == 1
        assert todos[0].title == "Complete Workflow"
        
        # Edit the todo
        retrieved_todo = manager.get_todo_by_id(todo.id)
        retrieved_todo.priority = Priority.HIGH
        retrieved_todo.details = "Updated details"
        manager.update_todo(retrieved_todo)
        
        # View again to verify changes
        updated_todos = manager.get_todos_by_owner("testuser")
        assert len(updated_todos) == 1
        assert updated_todos[0].priority == Priority.HIGH
        assert updated_todos[0].details == "Updated details"

    def test_create_edit_multiple_todos_independently(self, temp_data_dir):
        """Test that multiple todos can be created and edited independently."""
        manager = TodoManager(data_dir=temp_data_dir)
        
        # Create two todos
        todo1 = manager.create_todo(
            title="Todo 1",
            details="Details 1",
            priority=Priority.HIGH,
            owner="testuser"
        )
        
        todo2 = manager.create_todo(
            title="Todo 2",
            details="Details 2",
            priority=Priority.LOW,
            owner="testuser"
        )
        
        # Edit only todo1
        todo1.priority = Priority.LOW
        manager.update_todo(todo1)
        
        # Verify todo2 remains unchanged
        todos = manager.get_todos_by_owner("testuser")
        todo1_retrieved = next(t for t in todos if t.id == todo1.id)
        todo2_retrieved = next(t for t in todos if t.id == todo2.id)
        
        assert todo1_retrieved.priority == Priority.LOW
        assert todo2_retrieved.priority == Priority.LOW  # Originally LOW, should stay LOW
        assert todo1_retrieved.title == "Todo 1"
        assert todo2_retrieved.title == "Todo 2"
