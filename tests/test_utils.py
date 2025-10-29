from copy import deepcopy

from core.utils import extract_nested_value, replace_nested_value


def test_extract_nested_value_success(sample_response_payload, sample_response_structure):
    value = extract_nested_value(sample_response_payload, sample_response_structure, "$OUTPUT")
    assert value == "system prompt here"


def test_extract_nested_value_handles_list_structure():
    payload = {"items": [{"value": "skip"}, {"value": "system prompt here"}]}
    structure = {"items": [{}, {"value": "$OUTPUT"}]}

    value = extract_nested_value(payload, structure, "$OUTPUT")

    assert value == "system prompt here"


def test_extract_nested_value_missing(sample_response_payload):
    structure_without_placeholder = {"data": {"result": "not-a-placeholder"}}
    value = extract_nested_value(sample_response_payload, structure_without_placeholder, "$OUTPUT")
    assert value is None


def test_extract_nested_value_returns_none_for_none_payload():
    payload = {"data": {"result": None}}
    structure = {"data": {"result": "$OUTPUT"}}

    assert extract_nested_value(payload, structure, "$OUTPUT") is None


def test_replace_nested_value_updates_only_placeholder(sample_request_body):
    updated = replace_nested_value(deepcopy(sample_request_body), "$INPUT", "example message")
    assert updated["prompt"] == "example message"
    assert updated["metadata"]["language"] == "en"


def test_replace_nested_value_updates_nested_lists():
    data = {"items": ["$INPUT", {"nested": ["keep", "$INPUT"]}]}

    updated = replace_nested_value(deepcopy(data), "$INPUT", "filled")

    assert updated["items"][0] == "filled"
    assert updated["items"][1]["nested"][1] == "filled"
    assert updated["items"][1]["nested"][0] == "keep"
