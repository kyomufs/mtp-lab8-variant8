"""Model layer: in-memory storage of tasks (task #10)."""

from dataclasses import dataclass


@dataclass
class Task:
    """A single task with a completion flag."""

    title: str
    done: bool = False


class TaskStore:
    """Ordered in-memory collection of :class:`Task` items."""

    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def add(self, title: str) -> Task:
        """Append a new not-done task and return it."""
        task = Task(title=title)
        self._tasks.append(task)
        return task

    def complete(self, number: int) -> Task:
        """Mark the task with 1-based ``number`` as done.

        Raises:
            IndexError: if ``number`` is outside the store.
        """
        if not 1 <= number <= len(self._tasks):
            raise IndexError(f"no task with number {number}")
        task = self._tasks[number - 1]
        task.done = True
        return task

    def tasks(self) -> list[Task]:
        """Return a shallow copy of tasks in insertion order."""
        return list(self._tasks)
