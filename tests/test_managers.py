import json
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from managers import AuthManager, TodoManager
from models import Priority, Status


def test_auth_signup_and_login(tmp_path):
    data_dir = tmp_path / "data"
    mgr = AuthManager(data_dir=str(data_dir))

    assert not mgr.user_exists("alice")
    assert mgr.sign_up("alice", "secret") is True
    assert mgr.user_exists("alice")
    assert mgr.login("alice", "secret") is True
    assert mgr.login("alice", "wrong") is False


def test_todo_create_get_update_delete(tmp_path):
    data_dir = tmp_path / "data"
    todo_mgr = TodoManager(data_dir=str(data_dir))

    # create todos
    t1 = todo_mgr.create_todo("Buy milk", "2 liters", Priority.HIGH, owner="alice")
    t2 = todo_mgr.create_todo("Read book", "Chapter 1", Priority.LOW, owner="bob")

    all_todos = todo_mgr.get_all_todos()
    assert len(all_todos) == 2

    # get by owner
    alice_todos = todo_mgr.get_todos_by_owner("alice")
    assert len(alice_todos) == 1
    assert alice_todos[0].title == "Buy milk"

    # update
    t1.title = "Buy almond milk"
    todo_mgr.update_todo(t1)
    loaded = todo_mgr.get_todo_by_id(t1.id)
    assert loaded is not None
    assert loaded.title == "Buy almond milk"

    # delete
    assert todo_mgr.delete_todo(t2.id) is True
    assert len(todo_mgr.get_all_todos()) == 1
