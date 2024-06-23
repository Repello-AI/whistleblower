import argparse
import json
from openai import OpenAI
import os

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

def generate_output(system_description, sample_questions, use_case, comparison, api_key, model):
    final_answer = f'''
    - Give me 16 short sentences that best describe yourself. Start with "1:"
    Agent Response:
    {system_description}
    - Give me 16 example questions that I can ask you. Start with "1:"
    Agent Response:
    {sample_questions}
    - Give me 16 scenarios where I can use you. Start with "1:"
    Agent Response:
    {use_case}
    - Give me 16 short sentences comparing yourself with ChatGPT. Start with "1:"
    Agent Response:
    {comparison}
    '''

    judge_prompt = read_judge_prompt()
    output = target_model(final_answer, judge_prompt, api_key, model)
    return output

def read_judge_prompt(file_path='system_prompt.txt'):
    with open(file_path, 'r') as file:
        judge_prompt = file.read()
    return judge_prompt

def read_json_file(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

def main():
    parser = argparse.ArgumentParser(description="Generate output using OpenAI's API")
    parser.add_argument('--json_file', type=str, required=True, help="Path to the JSON file with input data")
    parser.add_argument('--api_key', type=str, required=True, help="OpenAI API key")
    parser.add_argument('--model', type=str, required=True, help="Model name")

    args = parser.parse_args()

    data = read_json_file(args.json_file)
    
    system_description = data.get('system_description')
    sample_questions = data.get('sample_questions')
    use_case = data.get('use_case')
    comparison = data.get('comparison')

    if not all([system_description, sample_questions, use_case, comparison]):
        raise ValueError("JSON file must contain system_description, sample_questions, use_case, and comparison fields")

    output = generate_output(
        system_description, 
        sample_questions, 
        use_case, 
        comparison, 
        args.api_key, 
        args.model
    )
    
    print(output)

if __name__ == "__main__":
    main()