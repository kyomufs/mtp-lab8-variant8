"""Tests for the calculator: the RED phase of the TDD cycle.

These tests were committed before the implementation (commit
``test: add calculator tests for TDD red phase``), so they failed
until ``lab8/calculator.py`` appeared in the next commit.
"""

import pytest

from lab8.calculator import add, div, mul, sub


def test_add_returns_sum() -> None:
    """add combines two integers."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_sub_returns_difference() -> None:
    """sub subtracts the second operand from the first."""
    assert sub(10, 4) == 6
    assert sub(0, 5) == -5


def test_mul_returns_product() -> None:
    """mul multiplies two operands."""
    assert mul(3, 4) == 12
    assert mul(-2, 3) == -6


def test_div_returns_float_quotient() -> None:
    """div always performs true division and returns a float."""
    result = div(10, 4)
    assert result == 2.5
    assert isinstance(result, float)
    assert div(9, 3) == 3.0


def test_div_by_zero_raises_zero_division_error() -> None:
    """div must raise ZeroDivisionError for a zero divisor."""
    with pytest.raises(ZeroDivisionError):
        div(1, 0)


def test_annotations_accept_float_operands() -> None:
    """Declared annotations are float | int for every function."""
    assert add(1.5, 2.25) == 3.75
    assert mul(2.5, 2.0) == 5.0
