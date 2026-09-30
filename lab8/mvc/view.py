"""View layer: render tasks as plain text lines (task #10)."""

from collections.abc import Sequence

from lab8.mvc.model import Task


def render_tasks(tasks: Sequence[Task]) -> str:
    """Return a numbered checklist for ``tasks``.

    An empty sequence renders the ``"(no tasks)"`` placeholder;
    completed tasks are marked with ``[x]``, pending ones with
    ``[ ]``. The function never mutates the input.
    """
    if not tasks:
        return "(no tasks)"
    lines = [
        f"{number}. [{'x' if task.done else ' '}] {task.title}"
        for number, task in enumerate(tasks, start=1)
    ]
    return "\n".join(lines)
