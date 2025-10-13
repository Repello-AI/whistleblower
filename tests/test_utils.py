from copy import deepcopy
from core.utils import extract_nested_value, replace_nested_value

def test_extract_nested_value_success(sample_response_payload, sample_response_structure):
    value = extract_nested_value(sample_response_payload, sample_response_structure, "$OUTPUT")
    assert value == "system prompt here"

def test_extract_nested_value_missing(sample_response_payload):
    structure_without_placeholder = {"data": {"result": "not-a-placeholder"}}
    value = extract_nested_value(sample_response_payload, structure_without_placeholder, "$OUTPUT")
    assert value is None

def test_replace_nested_value_updates_only_placeholder(sample_request_body):
    updated = replace_nested_value(deepcopy(sample_request_body), "$INPUT", "example message")
    assert updated["prompt"] == "example message"
    assert updated["metadata"]["language"] == "en"
