"""Unit tests for Task 6: View to-do-list item details.

These tests verify the `App.view_todo_details` behavior for valid,
nonexistent and empty ID inputs.
"""

import sys
from pathlib import Path

# Make sure src is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from managers import TodoManager
from main import App
from models import Priority


def test_view_todo_details_shows_all_fields(monkeypatch, capsys, temp_data_dir):
    manager = TodoManager(data_dir=temp_data_dir)
    todo = manager.create_todo(
        title="Detail Test",
        details="Some details",
        priority=Priority.HIGH,
        owner="tester",
    )

    app = App()
    # Use the test data dir
    app.todo_manager = TodoManager(data_dir=temp_data_dir)
    app.current_user = "tester"

    # Simulate user entering the todo id
    monkeypatch.setattr("builtins.input", lambda prompt='': todo.id)

    app.view_todo_details()
    captured = capsys.readouterr()

    assert "Title: Detail Test" in captured.out
    assert "Details: Some details" in captured.out
    assert "Priority: HIGH" in captured.out
    assert "Status: PENDING" in captured.out
    assert "Owner: tester" in captured.out
    assert "Created:" in captured.out
    assert "Updated:" in captured.out


def test_view_todo_details_nonexistent_id(monkeypatch, capsys, temp_data_dir):
    app = App()
    app.todo_manager = TodoManager(data_dir=temp_data_dir)
    app.current_user = "tester"

    monkeypatch.setattr("builtins.input", lambda prompt='': "nonexistent-id")

    app.view_todo_details()
    captured = capsys.readouterr()

    assert "Todo not found." in captured.out


def test_view_todo_details_empty_id(monkeypatch, capsys, temp_data_dir):
    app = App()
    app.todo_manager = TodoManager(data_dir=temp_data_dir)
    app.current_user = "tester"

    monkeypatch.setattr("builtins.input", lambda prompt='': "")

    app.view_todo_details()
    captured = capsys.readouterr()

    assert "ID cannot be empty." in captured.out
