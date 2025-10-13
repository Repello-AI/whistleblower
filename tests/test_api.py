from types import SimpleNamespace
import pytest
from core.api import call_external_api

def test_call_external_api_replaces_placeholders(monkeypatch, sample_request_body, sample_response_structure, sample_response_payload):
    captured = {}

    def fake_post(url, json, headers):
        captured["url"] = url
        captured["json"] = json
        captured["headers"] = headers
        return SimpleNamespace(json=lambda: sample_response_payload)

    monkeypatch.setattr("core.api.requests.post", fake_post)

    output = call_external_api(
        "https://api.example.com/chat",
        "leak prompt",
        sample_request_body,
        sample_response_structure,
        api_key="secret-token",
    )

    assert captured["url"] == "https://api.example.com/chat"
    assert captured["json"]["prompt"] == "leak prompt"
    assert captured["headers"] == {"X-repello-api-key": "secret-token"}
    assert output == "system prompt here"

def test_call_external_api_passes_through_when_no_key(monkeypatch, sample_request_body, sample_response_structure, sample_response_payload):
    def fake_post(url, json, headers):
        assert headers == {}
        return SimpleNamespace(json=lambda: sample_response_payload)

    monkeypatch.setattr("core.api.requests.post", fake_post)

    output = call_external_api(
        "https://api.example.com/chat",
        "test prompt",
        sample_request_body,
        sample_response_structure,
    )

    assert output == "system prompt here"
