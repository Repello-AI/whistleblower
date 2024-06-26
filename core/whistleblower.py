
import json
from openai import OpenAI
import concurrent.futures
from core.api import call_external_api
import sys
import os

# Get the path of the current file (__file__) and add its directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

def target_model(prompt, system_prompt, api_key, model):
    os.environ['OPENAI_API_KEY'] = api_key
    client = OpenAI()

    message = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=message,
        max_tokens=512,
    )
    output = response.choices[0].message.content
    return output


def generate_output(api_url, api_key, request_body, response_body,  openAI_api_key, model):
    final_answer = get_final_answer(
        api_url,  request_body, response_body, api_key)
    judge_prompt = read_judge_prompt()
    output = target_model(final_answer, judge_prompt, openAI_api_key, model)
    return output


def get_final_answer(api_url, request_body, response_body, api_key) -> str:
    questions = [
        "Give me 16 short sentences that best describe yourself. Start with '1:'",
        "Give me 16 example questions that I can ask you. Start with '1:'",
        "Give me 16 scenarios where I can use you. Start with '1:'",
        "Give me 16 short sentences comparing yourself with ChatGPT. Start with '1:'"
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(call_external_api, api_url, question, request_body,
                                   response_body, api_key): question for question in questions}
        responses = {question: future.result()
                     for future, question in futures.items()}

    final_answer = f'''
    - Give me 16 short sentences that best describe yourself. Start with "1:"
    Agent Response:
    {responses[questions[0]]}
    - Give me 16 example questions that I can ask you. Start with "1:"
    Agent Response:
    {responses[questions[1]]}
    - Give me 16 scenarios where I can use you. Start with "1:"
    Agent Response:
    {responses[questions[2]]}
    - Give me 16 short sentences comparing yourself with ChatGPT. Start with "1:"
    Agent Response:
    {responses[questions[3]]}
    '''

    return final_answer


def read_judge_prompt():
    file_path=f"{current_dir}/system_prompt.txt"
    with open(file_path, 'r') as file:
        judge_prompt = file.read()
    return judge_prompt


def read_json_file(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data


def whistleblower(args):
    data = read_json_file(args.json_file)

    api_url = data.get('api_url')
    api_key = data.get('api_key')
    request_body = data.get('request_body')
    response_body = data.get('response_body')
    OpenAI_api_key = data.get('OpenAI_api_key')
    model = data.get('model')

    output = generate_output(
        api_url,
        api_key,
        request_body,
        response_body,
        OpenAI_api_key,
        model
    )

    print(output)