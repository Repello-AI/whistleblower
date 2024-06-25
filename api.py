import requests

def call_external_api(url, message, request_body , response_body , api_key=None):
    headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}
    response = requests.post(url, json={request_body: message}, headers=headers)
    response.raise_for_status()
    return response.json()[response_body] 