from __future__ import annotations

from typing import Any

from miyouqian.core import captcha
from miyouqian.core.config import DEFAULT_CONFIG, normalize_config


class FakeClient:
    def __init__(self, response: dict[str, Any] | None = None, error: Exception | None = None):
        self.response = response or {}
        self.error = error
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def get_json(self, url: str, **kwargs: Any) -> dict[str, Any]:
        self.calls.append((url, kwargs))
        if self.error:
            raise self.error
        return self.response


def test_test_nine_calls_url_with_only_gt_and_challenge_and_parses_nested_validate() -> None:
    client = FakeClient({"data": {"validate": "solved-value"}})
    config = {
        "captcha": {
            "enable": True,
            "channels": [
                {"provider": "test_nine", "enable": True, "url": "https://example.invalid/solve", "timeout": 45}
            ],
        }
    }

    result = captcha.solve_game_captcha(client, config, "gt-value", "challenge-value")  # type: ignore[arg-type]

    assert result == captcha.CaptchaSolution(validate="solved-value", challenge="challenge-value")
    assert len(client.calls) == 1
    url, kwargs = client.calls[0]
    assert url == "https://example.invalid/solve"
    assert kwargs["params"] == {"gt": "gt-value", "challenge": "challenge-value"}
    assert kwargs["timeout"] == 45
    assert "headers" not in kwargs


def test_test_nine_accepts_top_level_validate() -> None:
    client = FakeClient({"validate": "top-level-value"})
    config = {
        "captcha": {
            "enable": True,
            "channels": [{"provider": "test_nine", "enable": True, "url": "https://example.invalid/solve"}],
        }
    }

    result = captcha.solve_game_captcha(client, config, "gt", "challenge")  # type: ignore[arg-type]

    assert result == captcha.CaptchaSolution(validate="top-level-value", challenge="challenge")


def test_test_nine_missing_validate_returns_none_and_emits_error() -> None:
    client = FakeClient({"data": {}})
    messages: list[str] = []
    config = {
        "captcha": {
            "enable": True,
            "channels": [{"provider": "test_nine", "enable": True, "url": "https://example.invalid/solve"}],
        }
    }

    result = captcha.solve_game_captcha(client, config, "gt", "challenge", messages.append)  # type: ignore[arg-type]

    assert result is None
    assert messages and "validate" in messages[0]


def test_config_normalizes_test_nine_without_token_or_api_key() -> None:
    config = {
        **DEFAULT_CONFIG,
        "captcha": {
            "enable": True,
            "channels": [{"provider": "test_nine", "enable": True, "url": "https://example.invalid/solve"}],
        },
    }

    normalize_config(config)
    channel = next(item for item in config["captcha"]["channels"] if item["provider"] == "test_nine")

    assert channel["enable"] is True
    assert channel["url"] == "https://example.invalid/solve"
    assert "api_key" not in channel
    assert "token" not in channel
    assert captcha.is_enabled(config)
