"""Demo entry point: run ``python -m lab8`` for all tasks.

The demo never starts the microservice; it prints start-up
instructions for it and runs offline quick examples for the
other four tasks.
"""

from typing import Any

from lab8.ai_client import AIClient
from lab8.calculator import add, div, mul, sub
from lab8.cli import main as cli_main
from lab8.mvc import TaskStore, handle_add, handle_complete


def medium_tasks() -> None:
    """Print quick examples for the three medium tasks."""
    print("=== Medium tasks ===")
    print("[#4] Calculator (TDD: red -> green -> refactor)")
    print(f"    add(2, 3) = {add(2, 3)}, sub(2, 3) = {sub(2, 3)}")
    print(f"    mul(2, 3) = {mul(2, 3)}, div(6, 3) = {div(6, 3)}")
    print("    tests: tests/test_calculator.py")
    print("[#8] CLI on argparse (0 ok, 1 bad number, 2 usage)")
    print("    quick example: python -m lab8.cli greet MTP")
    cli_main(["greet", "MTP"])
    print("[#10] MVC: controller -> model -> view")
    store = TaskStore()
    print(f"    {handle_add(store, 'write report')}")
    print(f"    {handle_complete(store, 1)}")
    print("    docs: docs/mvc.md")


def advanced_tasks() -> None:
    """Print instructions and an offline demo for advanced tasks."""
    print("=== Advanced tasks ===")
    print("[#1] Mini microservice on FastAPI (server not started)")
    print("    start: uv run --with fastapi --with uvicorn \\")
    print("           uvicorn lab8.microservice:app --reload")
    print('    check: curl http://127.0.0.1:8000/health')
    print('    routes: GET /health -> {"status": "ok"},')
    print("            GET /items, POST /items, GET /items/{id}")
    print("[#8] External AI API client (offline demo below)")
    print("    key: only api_key=... or env OPENAI_API_KEY;")
    print("         keys are never stored in the repository")

    def fake_transport(
        url: str, key: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """Return a canned answer without touching the network."""
        prompt = payload["messages"][0]["content"]
        return {"choices": [{"message": {"content": f"echo: {prompt}"}}]}

    client = AIClient(api_key="demo-key", transport=fake_transport)
    answer = client.complete("Explain TDD in one sentence")
    print(f'    complete("...") -> "{answer}"')


def main() -> int:
    """Print every demo section."""
    medium_tasks()
    advanced_tasks()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
