"""Tests for the argparse CLI (task #8).

Every test calls ``main([...])`` directly (no subprocess) and
checks the exit code together with captured stdout/stderr.
"""

import io
from contextlib import redirect_stderr, redirect_stdout

from lab8.cli import main


def run_cli(argv: list[str]) -> tuple[int, str, str]:
    """Call ``main`` and return its code, stdout and stderr."""
    out = io.StringIO()
    err = io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


def test_add_prints_sum() -> None:
    """add prints the sum and exits with 0."""
    code, out, err = run_cli(["add", "2", "3"])
    assert code == 0
    assert out == "5\n"
    assert err == ""


def test_sub_prints_difference() -> None:
    """sub prints the difference and exits with 0."""
    code, out, err = run_cli(["sub", "10", "4"])
    assert code == 0
    assert out == "6\n"
    assert err == ""


def test_greet_prints_greeting() -> None:
    """greet prints a greeting with the given name."""
    code, out, err = run_cli(["greet", "MTP"])
    assert code == 0
    assert out == "Hello, MTP!\n"
    assert err == ""


def test_float_operands_are_supported() -> None:
    """Float operands parse and integral results lose the .0."""
    code, out, err = run_cli(["add", "2.5", "0.5"])
    assert code == 0
    assert out == "3\n"
    assert err == ""


def test_negative_operands_are_supported() -> None:
    """Negative numbers are treated as positionals, not options."""
    code, out, err = run_cli(["sub", "0", "-5"])
    assert code == 0
    assert out == "5\n"
    assert err == ""


def test_invalid_number_returns_one() -> None:
    """A non-numeric operand exits with 1 and an stderr message."""
    code, out, err = run_cli(["add", "two", "3"])
    assert code == 1
    assert out == ""
    assert "not a number" in err


def test_missing_operand_returns_two() -> None:
    """argparse usage errors keep argparse's default code 2."""
    code, out, err = run_cli(["add", "2"])
    assert code == 2
    assert out == ""
    assert "required" in err


def test_unknown_command_returns_two() -> None:
    """An unknown subcommand is an argparse usage error."""
    code, out, err = run_cli(["mul", "2", "3"])
    assert code == 2
    assert out == ""
    assert "invalid choice" in err


def test_help_exits_zero_and_prints_usage() -> None:
    """--help prints usage on stdout and exits with 0."""
    code, out, err = run_cli(["--help"])
    assert code == 0
    assert "usage" in out
    assert err == ""
