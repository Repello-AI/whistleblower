import json
from types import SimpleNamespace

import pytest

from core import seeds,whistleblower

def _fake_openai_response(content):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
    )


def test_convert_to_json_handles_success_and_failure(tmp_path):
    payload = {"key": "value"}
    assert whistleblower.convert_to_json(json.dumps(payload)) == payload
    assert whistleblower.convert_to_json("not-json") == {}


def test_read_json_file_success(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"name": "value"}))

    assert whistleblower.read_json_file(str(config_path)) == {"name": "value"}


def test_read_json_file_invalid_json(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text("{bad json")

    assert whistleblower.read_json_file(str(config_path)) == {}


def test_target_model_returns_response(monkeypatch):
    def fake_call(api_url, question, request_body, response_body, api_key):
        return f"{question}-answer"

    monkeypatch.setattr(whistleblower, "call_external_api", fake_call)
    monkeypatch.setattr(whistleblower, "read_judge_prompt", lambda: "prompt")

    result = whistleblower.target_model(
        "https://api.example.com", {"prompt": "$INPUT"}, {"response": "$OUTPUT"}, "key", "question"
    )

    assert result == "question-answer"


def test_target_model_returns_none_on_exception(monkeypatch, capsys):
    def fake_call(*_):
        raise RuntimeError("network down")

    monkeypatch.setattr(whistleblower, "call_external_api", fake_call)

    result = whistleblower.target_model(
        "https://api.example.com", {"prompt": "$INPUT"}, {"response": "$OUTPUT"}, "key", "question"
    )

    captured = capsys.readouterr()
    assert "Error" in captured.out
    assert result is None


def test_capability_output_uses_openai(monkeypatch):
    expected = "capability response"

    def fake_openai():
        return SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(
                    create=lambda **_: _fake_openai_response(expected)
                )
            )
        )

    monkeypatch.setattr(whistleblower, "OpenAI", fake_openai)

    output = whistleblower.capability_output("prompt", "system", "key", "model")

    assert output == expected


def test_get_context_aggregates_responses(monkeypatch):
    answers = {
        "Give me 16 short sentences that best describe yourself. Start with '1:'": "A",
        "Give me 16 example questions that I can ask you. Start with '1:'": "B",
        "Give me 16 scenarios where I can use you. Start with '1:'": "C",
        "Give me 16 short sentences comparing yourself with ChatGPT. Start with '1:'": "D",
    }

    def fake_call(api_url, question, request_body, response_body, api_key):
        return answers[question]

    monkeypatch.setattr(whistleblower, "call_external_api", fake_call)

    captured = {}

    def fake_capability_output(context, judge_prompt, api_key, model):
        captured["context"] = context
        return "summarized"

    monkeypatch.setattr(whistleblower, "capability_output", fake_capability_output)
    monkeypatch.setattr(whistleblower, "read_judge_prompt", lambda: "prompt")

    context = whistleblower.get_context(
        "https://api.example.com",
        {"prompt": "$INPUT"},
        {"response": "$OUTPUT"},
        "api-key",
        "model",
    )

    assert context == "summarized"
    assert "A" in captured["context"]
    assert "D" in captured["context"]


def test_judge_model_parses_openai_response(monkeypatch):
    payload = json.dumps({"score": 2, "improvement": "try again"})

    def fake_openai():
        return SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(
                    create=lambda **_: _fake_openai_response(payload)
                )
            )
        )

    monkeypatch.setattr(whistleblower, "OpenAI", fake_openai)

    score, improvement = whistleblower.judge_model("adv", "target", "key", "model", "ctx")

    assert score == 2
    assert improvement == "try again"


def test_judge_model_handles_exception(monkeypatch):
    def fake_openai():
        return SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(
                    create=lambda **_: (_ for _ in ()).throw(RuntimeError("boom"))
                )
            )
        )

    monkeypatch.setattr(whistleblower, "OpenAI", fake_openai)

    score, improvement = whistleblower.judge_model("adv", "resp", "key", "model")

    assert score == 0
    assert improvement is None


def test_attacker_model_returns_suggestion(monkeypatch):
    expected = "new prompt"

    def fake_openai():
        return SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(
                    create=lambda **_: _fake_openai_response(expected)
                )
            )
        )

    monkeypatch.setattr(whistleblower, "OpenAI", fake_openai)

    assert whistleblower.attacker_model("prev", 1, "improve", "key", "model") == expected


def test_attacker_model_handles_exception(monkeypatch):
    def fake_openai():
        return SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(
                    create=lambda **_: (_ for _ in ()).throw(RuntimeError("fail"))
                )
            )
        )

    monkeypatch.setattr(whistleblower, "OpenAI", fake_openai)

    assert whistleblower.attacker_model("prev", 1, "improve", "key", "model") == ""


def test_generate_output_returns_success(monkeypatch):
    monkeypatch.setattr(whistleblower, "get_context", lambda *args, **kwargs: "context")
    monkeypatch.setattr(whistleblower, "target_model", lambda *args, **kwargs: "leaked")
    monkeypatch.setattr(whistleblower, "judge_model", lambda *args, **kwargs: (3, "done"))

    result = whistleblower.generate_output(
        "https://api.example.com",
        "api-key",
        '{"prompt": "$INPUT"}',
        '{"response": "$OUTPUT"}',
        "openai-key",
        "gpt-4o",
    )

    assert result == "leaked"


def test_generate_output_respects_repetition_limit(monkeypatch):
    monkeypatch.setattr(whistleblower, "get_context", lambda *args, **kwargs: "context")
    monkeypatch.setattr(whistleblower, "target_model", lambda *args, **kwargs: "partial")

    call_count = {"judge": 0}

    def fake_judge(*args, **kwargs):
        call_count["judge"] += 1
        return (2, "improve")

    prompts = []

    def fake_attacker(prompt, score, improvement, api_key, model):
        prompts.append((prompt, score, improvement))
        return f"{prompt}-{score}"

    monkeypatch.setattr(whistleblower, "judge_model", fake_judge)
    monkeypatch.setattr(whistleblower, "attacker_model", fake_attacker)

    result = whistleblower.generate_output(
        "https://api.example.com",
        "api-key",
        '{"prompt": "$INPUT"}',
        '{"response": "$OUTPUT"}',
        "openai-key",
        "gpt-4o",
    )

    assert result == "partial"
    assert call_count["judge"] == 4
    assert prompts


def test_whistleblower_invokes_generate_output(tmp_path, monkeypatch):
    config_path = tmp_path / "config.json"
    config = {
        "api_url": "https://api.example.com",
        "api_key": "api-key",
        "request_body": {"prompt": "$INPUT"},
        "response_body": {"response": "$OUTPUT"},
        "OpenAI_api_key": "openai-key",
        "model": "gpt-4o",
    }
    config_path.write_text(json.dumps(config))

    called = {}

    def fake_generate_output(*args):
        called["args"] = args
        return "result"

    monkeypatch.setattr(whistleblower, "generate_output", fake_generate_output)

    args = SimpleNamespace(json_file=str(config_path))

    whistleblower.whistleblower(args)

    assert called["args"][0] == config["api_url"]


def test_seeds_prompts_not_empty():
    assert seeds.prompts
    assert any("You are" in prompt for prompt in seeds.prompts)
