import requests

def call_external_api(url, message, api_key=None):
    headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}
    response = requests.post(url, json={'message': message}, headers=headers)
    response.raise_for_status()
    return response.json()['response'] 