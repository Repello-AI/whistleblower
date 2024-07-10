import requests

def call_external_api(url, message, request_body : dict , response_body : dict , api_key=None):
    headers = {'X-repello-api-key': f'{api_key}'} if api_key else {}
    request_body = {k: (message if v == "$INPUT" else v) for k, v in request_body.items()}
    response = requests.post(url, json=request_body, headers=headers)  # Fixed json parameter
    #response.raise_for_status()
    response_key = next(k for k, v in response_body.items() if v == "$OUTPUT")
    return response.json()[response_key] 