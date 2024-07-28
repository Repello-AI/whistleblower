import requests
from core.utils import replace_nested_value, extract_nested_value

def call_external_api(url, message, request_body : dict , response_body : dict , api_key=None):
    headers = {'X-repello-api-key': f'{api_key}'} if api_key else {}
    request_body = replace_nested_value(request_body, "$INPUT", message)
    response = requests.post(url, json=request_body, headers=headers)
    response_= extract_nested_value(response.json(), response_body, "$OUTPUT")
    return response_