import json
import importlib
import sys
import gradio as gr
import pytest
import sys
from pathlib import Path

ROOT = str(Path(__file__).resolve().parents[1])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

@pytest.fixture
def sample_request_body():
    return {
        "prompt": "$INPUT",
        "metadata": {
            "language": "en",
            "extras": ["a", "b"],
        },
    }

@pytest.fixture
def sample_response_structure():
    return {
        "data": {
            "result": "$OUTPUT",
        }
    }

@pytest.fixture
def sample_response_payload():
    return {
        "data": {
            "result": "system prompt here",
        }
    }

@pytest.fixture
def request_body_json(sample_request_body):
    return json.dumps(sample_request_body)

@pytest.fixture
def response_body_json(sample_response_structure):
    return json.dumps(sample_response_structure)

@pytest.fixture
def ui_app(monkeypatch):
    pytest.importorskip("core.whistleblower", reason="core.whistleblower module missing")
    monkeypatch.setattr(gr.Blocks, "launch", lambda self: None)
    module_name = "ui.app"
    if module_name in sys.modules:
        module = importlib.reload(sys.modules[module_name])
    else:
        module = importlib.import_module(module_name)
    return module
