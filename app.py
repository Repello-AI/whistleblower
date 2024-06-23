import gradio as gr
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

iface = gr.Interface(
    fn=generate_output,
    inputs=[
        gr.Textbox(label='''Give me 16 short sentences that best describe yourself. Start with "1:"''', lines=5),
        gr.Textbox(label='''Give me 16 example questions that I can ask you. Start with "1:"''', lines=5),
        gr.Textbox(label='''Give me 16 scenarios where I can use you. Start with "1:"''', lines=5),
        gr.Textbox(label='''Give me 16 short sentences comparing yourself with ChatGPT. Start with "1:"''', lines=5),
        gr.Textbox(label="OpenAI API Key"),
        gr.Dropdown(choices=["gpt-4", "gpt-3.5-turbo", "gpt-4-0613"], label="Model")
    ],
    outputs=gr.Textbox(label="Output", lines=20),
    title="System Prompt Extractor",
    description="Enter the answers, OpenAI API key, and select a model to generate the evaluation."
)

iface.launch()