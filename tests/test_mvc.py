"""Tests for the MVC example (task #10): controller flow."""

import pytest

from lab8.mvc import (
    TaskStore,
    handle_add,
    handle_complete,
    render_tasks,
)
from lab8.mvc.model import Task


def test_add_then_render_contains_title() -> None:
    """Controller flow: add a task, see it in the rendered text."""
    store = TaskStore()
    output = handle_add(store, "write report")
    assert "write report" in output
    assert "[ ]" in output
    assert len(store.tasks()) == 1


def test_complete_marks_second_task_done() -> None:
    """Complete flips only the selected task to [x]."""
    store = TaskStore()
    handle_add(store, "first")
    handle_add(store, "second")
    output = handle_complete(store, 2)
    assert "[x] second" in output
    assert "[ ] first" in output
    assert store.tasks()[1].done is True


def test_complete_unknown_number_raises_index_error() -> None:
    """The controller propagates the model's IndexError."""
    store = TaskStore()
    handle_add(store, "only")
    with pytest.raises(IndexError):
        handle_complete(store, 5)


def test_render_empty_store_shows_placeholder() -> None:
    """An empty store renders the documented placeholder."""
    store = TaskStore()
    assert render_tasks(store.tasks()) == "(no tasks)"


def test_task_defaults_to_not_done() -> None:
    """A fresh Task is not done by default."""
    task = Task(title="clean up")
    assert task.done is False
