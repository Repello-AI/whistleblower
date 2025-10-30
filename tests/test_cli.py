import json
import sys
from pathlib import Path
import pytest

main = pytest.importorskip("main", reason="main module missing")
whistleblower = pytest.importorskip("core.whistleblower", reason="core.whistleblower module missing")

def test_read_json_file_valid(tmp_path):
    data = {"api_url": "http://example.com"}
    json_path = tmp_path / "config.json"
    json_path.write_text(json.dumps(data))

    loaded = whistleblower.read_json_file(str(json_path))

    assert loaded == data

def test_read_json_file_invalid(tmp_path, capsys):
    json_path = tmp_path / "invalid.json"
    json_path.write_text("{invalid")

    loaded = whistleblower.read_json_file(str(json_path))

    assert loaded == {}

def test_main_invokes_whistleblower(monkeypatch, tmp_path):
    config_path = tmp_path / "input.json"
    config_path.write_text(
        json.dumps(
            {
                "api_url": "http://example.com",
                "request_body": {"prompt": "$INPUT"},
                "response_body": {"response": "$OUTPUT"},
                "OpenAI_api_key": "key",
                "model": "gpt-4",
            }
        )
    )

    called = {}

    def fake_whistleblower(args):
        called["json_file"] = args.json_file
        return "done"

    monkeypatch.setattr(main, "whistleblower", fake_whistleblower)
    monkeypatch.setattr(sys, "argv", ["main.py", "--json_file", str(config_path)])

    result = main.main()

    assert called["json_file"] == str(config_path)
    assert result == "done"
