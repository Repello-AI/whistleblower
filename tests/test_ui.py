import json

import gradio as gr
import pytest


def test_check_for_placeholders(ui_app, request_body_json):
    assert ui_app.check_for_placeholders(request_body_json, "$INPUT")
    assert not ui_app.check_for_placeholders({"prompt": "hello"}, "$INPUT")


def test_check_for_placeholders_list(ui_app):
    payload = json.dumps({"messages": [{"text": "$INPUT"}]})

    assert ui_app.check_for_placeholders(payload, "$INPUT")


def test_validate_input_json_success(ui_app, request_body_json, response_body_json, monkeypatch):
    captured = {}

    def fake_generate_output(*args):
        captured["args"] = args
        return "result-json"

    monkeypatch.setattr(ui_app, "generate_output", fake_generate_output)

    output = ui_app.validate_input(
        "https://api.example.com",
        "api-key",
        "JSON",
        "",
        request_body_json,
        "",
        response_body_json,
        "openai-key",
        "gpt-4",
    )

    assert output == "result-json"
    assert captured["args"][0] == "https://api.example.com"
    assert json.loads(captured["args"][2])["prompt"] == "$INPUT"


def test_validate_input_json_empty_request_raises(ui_app):
    with pytest.raises(gr.Error) as excinfo:
        ui_app.validate_input(
            "https://api.example.com",
            "",
            "JSON",
            "",
            "",
            "",
            "{}",
            "",
            "gpt-4o",
        )

    assert "Request body cannot be empty" in str(excinfo.value)


def test_validate_input_json_invalid_request_raises(ui_app):
    with pytest.raises(gr.Error) as excinfo:
        ui_app.validate_input(
            "https://api.example.com",
            "",
            "JSON",
            "",
            "{bad json",
            "",
            '{"response": "$OUTPUT"}',
            "",
            "gpt-4o",
        )

    assert "Invalid JSON format in request body." in str(excinfo.value)


def test_validate_input_json_missing_output_placeholder_raises(ui_app):
    with pytest.raises(gr.Error) as excinfo:
        ui_app.validate_input(
            "https://api.example.com",
            "",
            "JSON",
            "",
            '{"prompt": "$INPUT"}',
            "",
            '{"response": "missing"}',
            "",
            "gpt-4o",
        )

    assert "Response body must contain the $OUTPUT placeholder." in str(excinfo.value)


def test_validate_input_key_value_success(ui_app, monkeypatch):
    captured = {}

    def fake_generate_output(*args):
        captured["args"] = args
        return "result-kv"

    monkeypatch.setattr(ui_app, "generate_output", fake_generate_output)

    output = ui_app.validate_input(
        "https://api.example.com",
        "",
        "Key-Value",
        "prompt: $INPUT\nstatic: value",
        "",
        "response: $OUTPUT",
        "",
        "service-key",
        "gpt-4o",
    )

    assert output == "result-kv"
    request_dict = captured["args"][2]
    assert request_dict["prompt"] == "$INPUT"
    assert request_dict["static"] == "value"
    response_dict = captured["args"][3]
    assert response_dict["response"] == "$OUTPUT"


def test_validate_input_key_value_empty_fields_raise(ui_app):
    with pytest.raises(gr.Error) as excinfo:
        ui_app.validate_input(
            "https://api.example.com",
            "",
            "Key-Value",
            "",
            "",
            "response: $OUTPUT",
            "",
            "openai-key",
            "gpt-4o",
        )

    assert "Request body cannot be empty." in str(excinfo.value)


def test_validate_input_missing_placeholder_raises(ui_app):
    with pytest.raises(gr.Error):
        ui_app.validate_input(
            "https://api.example.com",
            "",
            "JSON",
            "",
            '{"prompt": "no placeholder"}',
            "",
            '{"response": "$OUTPUT"}',
            "",
            "gpt-4o",
        )
