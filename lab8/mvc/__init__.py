"""Minimal MVC example: model, view and controller layers."""

from lab8.mvc.controller import handle_add, handle_complete
from lab8.mvc.model import Task, TaskStore
from lab8.mvc.view import render_tasks

__all__ = [
    "Task",
    "TaskStore",
    "handle_add",
    "handle_complete",
    "render_tasks",
]
