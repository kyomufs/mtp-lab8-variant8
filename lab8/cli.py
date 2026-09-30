"""Argument-parser based command line interface (task #8).

Subcommands::

    add A B     print A + B
    sub A B     print A - B
    greet NAME  print a greeting

``main`` returns the process exit code instead of calling
``sys.exit`` itself, so tests call it directly: argparse usage
errors map to 2 (argparse default), unparsable numeric operands
map to 1 with a message on stderr, success maps to 0.
"""

import argparse
import sys

from lab8.calculator import add, sub


def build_parser() -> argparse.ArgumentParser:
    """Create the parser with the ``add``, ``sub`` and ``greet``."""
    parser = argparse.ArgumentParser(
        prog="lab8-cli",
        description="Tiny calculator and greeting CLI.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    add_parser = commands.add_parser("add", help="print A + B")
    add_parser.add_argument("a", type=str, help="left operand")
    add_parser.add_argument("b", type=str, help="right operand")

    sub_parser = commands.add_parser("sub", help="print A - B")
    sub_parser.add_argument("a", type=str, help="left operand")
    sub_parser.add_argument("b", type=str, help="right operand")

    greet_parser = commands.add_parser("greet", help="print a greeting")
    greet_parser.add_argument("name", type=str, help="who to greet")
    return parser


def parse_number(raw: str) -> int | float:
    """Convert ``raw`` to ``int`` when possible, else to ``float``.

    Raises:
        ValueError: if ``raw`` is not a number.
    """
    try:
        return int(raw)
    except ValueError:
        try:
            return float(raw)
        except ValueError as exc:
            raise ValueError(f"not a number: {raw!r}") from exc


def format_number(value: float | int) -> str:
    """Render integral floats without a trailing ``.0``."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def main(argv: list[str] | None = None) -> int:
    """Run the CLI for ``argv`` (``None`` means ``sys.argv[1:]``).

    Returns:
        0 on success, 2 on argparse usage errors, 1 when a
        numeric operand cannot be parsed.
    """
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        if code is None:
            return 0
        if isinstance(code, int):
            return code
        return 1
    if args.command == "greet":
        print(f"Hello, {args.name}!")
        return 0
    try:
        left = parse_number(args.a)
        right = parse_number(args.b)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.command == "add":
        print(format_number(add(left, right)))
    else:
        print(format_number(sub(left, right)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
