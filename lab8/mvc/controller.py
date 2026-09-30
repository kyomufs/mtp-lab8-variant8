"""Controller layer: model updates plus view rendering (#10)."""

from lab8.mvc.model import TaskStore
from lab8.mvc.view import render_tasks


def handle_add(store: TaskStore, title: str) -> str:
    """Add ``title`` to ``store`` and return the rendered list."""
    store.add(title)
    return render_tasks(store.tasks())


def handle_complete(store: TaskStore, number: int) -> str:
    """Complete task ``number`` and return the rendered list.

    Propagates ``IndexError`` from the model when ``number`` is
    outside the store.
    """
    store.complete(number)
    return render_tasks(store.tasks())
