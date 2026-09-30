"""Arithmetic helpers written test-first (task #4, TDD).

The module documents one full TDD cycle:

* **red** — ``tests/test_calculator.py`` was committed first and
  failed with ``ModuleNotFoundError`` because the module did not
  exist yet (commit ``test: add calculator tests for TDD red
  phase``);
* **green** — this implementation was added next just enough to
  make every test pass (commit ``feat: implement calculator to
  pass tests``);
* **refactor** — the public surface stays small: four annotated
  functions with precise docstrings, no duplicated logic.
"""


def add(a: float | int, b: float | int) -> float | int:
    """Return the sum of ``a`` and ``b``."""
    return a + b


def sub(a: float | int, b: float | int) -> float | int:
    """Return ``a`` minus ``b``."""
    return a - b


def mul(a: float | int, b: float | int) -> float | int:
    """Return the product of ``a`` and ``b``."""
    return a * b


def div(a: float | int, b: float | int) -> float:
    """Return ``a`` divided by ``b`` using true division.

    Raises:
        ZeroDivisionError: if ``b`` is zero.
    """
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b
