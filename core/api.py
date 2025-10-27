import requests
from core.utils import replace_nested_value, extract_nested_value
try:
    # Optional dependency used only for WebSocket transport
    from websocket import create_connection
except Exception:
    create_connection = None

def call_external_api(url, message, request_body : dict , response_body : dict , api_key=None):
    headers = {'X-repello-api-key': f'{api_key}'} if api_key else {}
    request_body = replace_nested_value(request_body, "$INPUT", message)
    response = requests.post(url, json=request_body, headers=headers)
    
    # Check if response is successful
    response.raise_for_status()
    
    # Parse JSON response
    try:
        response_data = response.json()
    except ValueError as e:
        raise ValueError(f"Invalid JSON response from {url}: {e}")
    
    response_= extract_nested_value(response_data, response_body, "$OUTPUT")
    return response_


def call_external_ws(url, message, request_body: dict, response_body: dict, api_key=None):
    """
    Send a single-message request over WebSocket and extract a field from the JSON response.

    Expects the server to reply with a single JSON message containing the output structure.
    """
    if create_connection is None:
        raise RuntimeError("websocket-client is not installed. Please add 'websocket-client' to requirements.")

    payload = replace_nested_value(dict(request_body), "$INPUT", message)

    # Prepare optional headers for the WS handshake
    headers = []
    if api_key:
        headers.append(f"X-repello-api-key: {api_key}")

    ws = create_connection(url, header=headers)  # May raise if URL/handshake is invalid
    try:
        import json as _json
        ws.send(_json.dumps(payload))
        raw_msg = ws.recv()
        data = _json.loads(raw_msg)
        extracted = extract_nested_value(data, response_body, "$OUTPUT")
        return extracted
    finally:
        try:
            ws.close()
        except Exception:
            pass