from pathlib import Path
import sys
from datetime import datetime
import pytest

# Ensure the `src` directory is on sys.path so imports work during tests
ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from managers import TodoManager, AuthManager
from models import TodoItem, Priority, Status


@pytest.fixture
def test_env():
    """Setup and teardown for each test."""
    data_dir = Path("data_test")
    # Ensure clean test directory
    if data_dir.exists():
        for f in data_dir.iterdir():
            f.unlink()
    else:
        data_dir.mkdir()

    yield {
        "data_dir": data_dir,
        "auth_mgr": AuthManager(data_dir=str(data_dir)),
        "todo_mgr": TodoManager(data_dir=str(data_dir)),
    }

    # Cleanup after test
    if data_dir.exists():
        for f in data_dir.iterdir():
            f.unlink()
        data_dir.rmdir()


def test_mark_completed_success(test_env):
    """Test successfully marking a todo as completed."""
    todo_mgr = test_env["todo_mgr"]
    auth_mgr = test_env["auth_mgr"]
    username = "tester"

    # Create user and todo
    auth_mgr.sign_up(username, "pass")
    todo = todo_mgr.create_todo(
        title="Test todo",
        details="details",
        priority=Priority.HIGH,
        owner=username,
    )

    # Assert initially pending
    assert todo.status == Status.PENDING

    # Mark as completed
    result = todo_mgr.mark_as_completed(todo.id, username)
    assert result is True, "mark_as_completed should return True"

    # Reload and verify status changed
    reloaded = todo_mgr.get_todo_by_id(todo.id)
    assert reloaded is not None
    assert reloaded.status == Status.COMPLETED


def test_mark_completed_updates_timestamp(test_env):
    """Test that marking as completed updates the updated_at timestamp."""
    todo_mgr = test_env["todo_mgr"]
    auth_mgr = test_env["auth_mgr"]
    username = "tester"

    # Create user and todo
    auth_mgr.sign_up(username, "pass")
    todo = todo_mgr.create_todo(
        title="Test todo",
        details="details",
        priority=Priority.MID,
        owner=username,
    )

    original_timestamp = todo.updated_at

    # Small delay to ensure timestamp difference
    import time
    time.sleep(0.01)

    # Mark as completed
    todo_mgr.mark_as_completed(todo.id, username)

    # Reload and verify timestamp updated
    reloaded = todo_mgr.get_todo_by_id(todo.id)
    assert reloaded.updated_at != original_timestamp
    # Ensure new timestamp is more recent
    original_dt = datetime.fromisoformat(original_timestamp)
    new_dt = datetime.fromisoformat(reloaded.updated_at)
    assert new_dt > original_dt


def test_mark_completed_nonexistent_todo(test_env):
    """Test marking a non-existent todo returns False."""
    todo_mgr = test_env["todo_mgr"]
    username = "tester"

    # Try to mark non-existent todo
    result = todo_mgr.mark_as_completed("nonexistent-id", username)
    assert result is False, "Should return False for non-existent todo"


def test_mark_completed_wrong_owner(test_env):
    """Test that a user cannot mark another user's todo as completed."""
    todo_mgr = test_env["todo_mgr"]
    auth_mgr = test_env["auth_mgr"]

    # Create two users
    auth_mgr.sign_up("user1", "pass1")
    auth_mgr.sign_up("user2", "pass2")

    # User1 creates a todo
    todo = todo_mgr.create_todo(
        title="User1's todo",
        details="Details",
        priority=Priority.HIGH,
        owner="user1",
    )

    # User2 tries to mark it as completed
    result = todo_mgr.mark_as_completed(todo.id, "user2")
    assert result is False, "Different user should not be able to mark todo as completed"

    # Verify todo still pending
    reloaded = todo_mgr.get_todo_by_id(todo.id)
    assert reloaded.status == Status.PENDING


def test_mark_completed_already_completed(test_env):
    """Test marking an already completed todo as completed again."""
    todo_mgr = test_env["todo_mgr"]
    auth_mgr = test_env["auth_mgr"]
    username = "tester"

    # Create user and todo
    auth_mgr.sign_up(username, "pass")
    todo = todo_mgr.create_todo(
        title="Test todo",
        details="Details",
        priority=Priority.LOW,
        owner=username,
    )

    # Mark as completed twice
    result1 = todo_mgr.mark_as_completed(todo.id, username)
    assert result1 is True

    result2 = todo_mgr.mark_as_completed(todo.id, username)
    assert result2 is True, "Should be able to mark already completed todo again"

    # Verify status remains completed
    reloaded = todo_mgr.get_todo_by_id(todo.id)
    assert reloaded.status == Status.COMPLETED


def test_mark_completed_persists_to_file(test_env):
    """Test that completion status is persisted to the JSON file."""
    todo_mgr = test_env["todo_mgr"]
    auth_mgr = test_env["auth_mgr"]
    username = "tester"

    # Create user and todo
    auth_mgr.sign_up(username, "pass")
    todo = todo_mgr.create_todo(
        title="Test todo",
        details="Details",
        priority=Priority.HIGH,
        owner=username,
    )

    todo_id = todo.id

    # Mark as completed
    todo_mgr.mark_as_completed(todo_id, username)

    # Create a new TodoManager instance to simulate app restart
    new_todo_mgr = TodoManager(data_dir=str(test_env["data_dir"]))

    # Reload and verify status persisted
    reloaded = new_todo_mgr.get_todo_by_id(todo_id)
    assert reloaded is not None
    assert reloaded.status == Status.COMPLETED


def test_mark_completed_with_multiple_todos(test_env):
    """Test marking specific todos as completed with multiple todos present."""
    todo_mgr = test_env["todo_mgr"]
    auth_mgr = test_env["auth_mgr"]
    username = "tester"

    # Create user
    auth_mgr.sign_up(username, "pass")

    # Create multiple todos
    todo1 = todo_mgr.create_todo(
        title="Todo 1", details="Details 1", priority=Priority.HIGH, owner=username
    )
    todo2 = todo_mgr.create_todo(
        title="Todo 2", details="Details 2", priority=Priority.MID, owner=username
    )
    todo3 = todo_mgr.create_todo(
        title="Todo 3", details="Details 3", priority=Priority.LOW, owner=username
    )

    # Mark only todo2 as completed
    result = todo_mgr.mark_as_completed(todo2.id, username)
    assert result is True

    # Verify only todo2 is completed
    reloaded1 = todo_mgr.get_todo_by_id(todo1.id)
    reloaded2 = todo_mgr.get_todo_by_id(todo2.id)
    reloaded3 = todo_mgr.get_todo_by_id(todo3.id)

    assert reloaded1.status == Status.PENDING
    assert reloaded2.status == Status.COMPLETED
    assert reloaded3.status == Status.PENDING


def test_mark_completed_empty_string_id(test_env):
    """Test marking a todo with empty string ID returns False."""
    todo_mgr = test_env["todo_mgr"]
    username = "tester"

    result = todo_mgr.mark_as_completed("", username)
    assert result is False


def test_mark_completed_empty_string_owner(test_env):
    """Test marking a todo with empty string owner returns False."""
    todo_mgr = test_env["todo_mgr"]
    auth_mgr = test_env["auth_mgr"]
    username = "tester"

    # Create user and todo
    auth_mgr.sign_up(username, "pass")
    todo = todo_mgr.create_todo(
        title="Test todo",
        details="Details",
        priority=Priority.HIGH,
        owner=username,
    )

    # Try to mark with empty owner
    result = todo_mgr.mark_as_completed(todo.id, "")
    assert result is False

    # Verify todo still pending
    reloaded = todo_mgr.get_todo_by_id(todo.id)
    assert reloaded.status == Status.PENDING
