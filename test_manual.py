#!/usr/bin/env python3
"""Manual test script for the Todo List application."""

from managers import AuthManager, TodoManager
from models import Priority, Status


def test_auth_and_todos():
    """Test authentication and todo operations."""
    auth = AuthManager()
    todo_mgr = TodoManager()

    # Test 1: Sign up
    print("Test 1: Sign up new user")
    assert auth.sign_up("alice", "password123"), "Sign up failed"
    print("✓ Sign up successful")

    # Test 2: Login with correct credentials
    print("\nTest 2: Login with correct credentials")
    assert auth.login("alice", "password123"), "Login failed"
    print("✓ Login successful")

    # Test 3: Login with incorrect credentials
    print("\nTest 3: Login with incorrect credentials")
    assert not auth.login("alice", "wrongpassword"), "Should have failed"
    print("✓ Correctly rejected wrong password")

    # Test 4: Create todo
    print("\nTest 4: Create a todo item")
    todo1 = todo_mgr.create_todo(
        title="Learn Python",
        details="Complete Python basics course",
        priority=Priority.HIGH,
        owner="alice",
    )
    print(f"✓ Todo created: {todo1.title} (ID: {todo1.id})")

    # Test 5: Create another todo
    print("\nTest 5: Create another todo item")
    todo2 = todo_mgr.create_todo(
        title="Buy groceries",
        details="Milk, eggs, bread",
        priority=Priority.MID,
        owner="alice",
    )
    print(f"✓ Todo created: {todo2.title} (ID: {todo2.id})")

    # Test 6: Get todos by owner
    print("\nTest 6: Retrieve all todos for alice")
    todos = todo_mgr.get_todos_by_owner("alice")
    print(f"✓ Found {len(todos)} todos")
    for todo in todos:
        print(f"  - {todo.title} [{todo.priority.value}] ({todo.status.value})")

    # Test 7: Update todo
    print("\nTest 7: Edit a todo item")
    todo1.title = "Learn Python 3.11+"
    todo1.priority = Priority.LOW
    todo_mgr.update_todo(todo1)
    print(f"✓ Todo updated: {todo1.title}")

    # Test 8: Mark as completed
    print("\nTest 8: Mark todo as completed")
    todo2.status = Status.COMPLETED
    todo_mgr.update_todo(todo2)
    print(f"✓ Todo marked as completed: {todo2.title}")

    # Test 9: Get updated todos
    print("\nTest 9: View updated todos")
    todos = todo_mgr.get_todos_by_owner("alice")
    for todo in todos:
        print(f"  - {todo.title} [{todo.priority.value}] ({todo.status.value})")
        print(f"    Details: {todo.details}")

    # Test 10: Delete todo
    print("\nTest 10: Delete a todo")
    assert todo_mgr.delete_todo(todo1.id), "Delete failed"
    todos = todo_mgr.get_todos_by_owner("alice")
    print(f"✓ Todo deleted. Remaining todos: {len(todos)}")

    print("\n" + "=" * 40)
    print("All tests passed! ✓")
    print("=" * 40)


if __name__ == "__main__":
    test_auth_and_todos()
