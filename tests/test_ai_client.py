"""Tests for the AI client (advanced task #8).

A fake transport stands in for the network: it records the URL,
the key and the payload, then returns a canned response. One
test checks the real ``urllib.request`` transport against a
monkeypatched ``urlopen``.
"""

import json
import urllib.request
from typing import Any

import pytest

from lab8.ai_client import API_URL, AIClient


def canned_response(text: str) -> dict[str, Any]:
    """Build a chat-completions shaped response."""
    return {"choices": [{"message": {"content": text}}]}


def test_fake_transport_receives_url_key_payload() -> None:
    """The fake transport sees the URL, Bearer key and payload."""
    seen: list[tuple[str, str, dict[str, Any]]] = []

    def fake(
        url: str, key: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        seen.append((url, key, payload))
        return canned_response("Hello from fake")

    client = AIClient(
        model="gpt-4o-mini", api_key="sk-test", transport=fake
    )
    assert client.complete("Hi") == "Hello from fake"
    url, key, payload = seen[0]
    assert url == API_URL
    assert key == "sk-test"
    assert payload["model"] == "gpt-4o-mini"
    assert payload["messages"] == [
        {"role": "user", "content": "Hi"}
    ]


def test_env_variable_supplies_missing_key(monkeypatch) -> None:
    """Without api_key the key comes from the environment."""
    keys: list[str] = []

    def fake(
        url: str, key: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        keys.append(key)
        return canned_response("env key works")

    monkeypatch.setenv("OPENAI_API_KEY", "sk-env")
    client = AIClient(transport=fake)
    assert client.complete("ping") == "env key works"
    assert keys == ["sk-env"]


def test_missing_key_raises_runtime_error(monkeypatch) -> None:
    """No key at all means RuntimeError in the constructor."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        AIClient()


def test_malformed_response_raises_runtime_error() -> None:
    """An unexpected payload shape is reported as RuntimeError."""

    def fake(
        url: str, key: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return {"unexpected": True}

    client = AIClient(api_key="sk-test", transport=fake)
    with pytest.raises(RuntimeError):
        client.complete("hi")


def test_default_transport_posts_with_bearer_header(
    monkeypatch,
) -> None:
    """The default transport POSTs to the URL with the header."""
    captured: dict[str, Any] = {}

    class FakeResponse:
        """Context manager mimicking an urlopen reply."""

        def read(self) -> bytes:
            return json.dumps(canned_response("pong")).encode(
                "utf-8"
            )

        def __enter__(self) -> "FakeResponse":
            return self

        def __exit__(self, *args: object) -> bool:
            return False

    def fake_urlopen(
        request: urllib.request.Request, timeout: int = 0
    ) -> FakeResponse:
        captured["request"] = request
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    client = AIClient(api_key="sk-secret")
    assert client.complete("ping") == "pong"
    request: urllib.request.Request = captured["request"]
    assert request.get_method() == "POST"
    assert request.full_url == API_URL
    assert (
        request.get_header("Authorization") == "Bearer sk-secret"
    )
    assert b"gpt-4o-mini" in request.data
    assert captured["timeout"] == 30


def test_model_defaults_to_gpt_4o_mini(monkeypatch) -> None:
    """The default model is sent in the payload."""
    payloads: list[dict[str, Any]] = []

    def fake(
        url: str, key: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        payloads.append(payload)
        return canned_response("ok")

    monkeypatch.setenv("OPENAI_API_KEY", "sk-env")
    client = AIClient(transport=fake)
    assert client.model == "gpt-4o-mini"
    client.complete("hello")
    assert payloads[0]["model"] == "gpt-4o-mini"
