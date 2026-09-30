"""Client for an external chat-completions API (advanced task #8).

The API key is taken ONLY from the ``api_key`` argument or from
the ``OPENAI_API_KEY`` environment variable — no key is stored in
the repository. Without a key the constructor raises
``RuntimeError``.

The default transport performs a POST request with
``urllib.request`` to ``API_URL`` and sets the
``Authorization: Bearer <key>`` header. Tests inject a fake
``transport`` instead, so no network access is needed.
"""

import json
import os
import urllib.request
from collections.abc import Callable
from typing import Any

API_URL = "https://api.openai.com/v1/chat/completions"
ENV_VAR = "OPENAI_API_KEY"
DEFAULT_MODEL = "gpt-4o-mini"

Transport = Callable[[str, str, dict[str, Any]], dict[str, Any]]
"""``(url, api_key, payload) -> decoded JSON response``."""


def http_transport(
    url: str, api_key: str, payload: dict[str, Any]
) -> dict[str, Any]:
    """POST ``payload`` to ``url`` and return the decoded JSON.

    Raises:
        RuntimeError: if the response body is not a JSON object.
    """
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as reply:
        decoded: Any = json.loads(reply.read().decode("utf-8"))
    if not isinstance(decoded, dict):
        raise RuntimeError("unexpected response from the API")
    return decoded


class AIClient:
    """Thin wrapper around a chat-completions endpoint."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        api_key: str | None = None,
        transport: Transport | None = None,
    ) -> None:
        """Resolve the key, model and transport.

        Args:
            model: model identifier sent in the payload.
            api_key: key for the Authorization header; ``None``
                falls back to the ``OPENAI_API_KEY`` variable.
            transport: optional ``(url, api_key, payload)``
                callable; the default is :func:`http_transport`.

        Raises:
            RuntimeError: if no API key is available.
        """
        key = (
            api_key
            if api_key is not None
            else os.environ.get(ENV_VAR)
        )
        if not key:
            raise RuntimeError(
                "API key is missing: pass api_key=... or set "
                f"{ENV_VAR} in the environment"
            )
        self._model = model
        self._api_key = key
        self._transport: Transport = (
            transport if transport is not None else http_transport
        )

    @property
    def model(self) -> str:
        """Model identifier used in request payloads."""
        return self._model

    def complete(self, prompt: str) -> str:
        """Send ``prompt`` as a user message, return the answer.

        Raises:
            RuntimeError: if the transport response has an
                unexpected shape.
        """
        payload: dict[str, Any] = {
            "model": self._model,
            "messages": [{"role": "user", "content": prompt}],
        }
        response = self._transport(API_URL, self._api_key, payload)
        try:
            content: Any = response["choices"][0]["message"][
                "content"
            ]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                "unexpected response from the API"
            ) from exc
        if not isinstance(content, str):
            raise RuntimeError("unexpected response from the API")
        return content
