import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from core.whistleblower import generate_output

with open('styles.css', 'r') as file:
    css = file.read()

def validate_input(api_url, api_key, request_body, response_body, openai_key, model):
    if not request_body.strip():
        raise gr.Error("Request body cannot be empty.")
    if not response_body.strip():
        raise gr.Error("Response body cannot be empty.")
    return generate_output(api_url, api_key, request_body, response_body, openai_key, model)

iface = gr.Interface(
    fn=validate_input,
    inputs=[
        gr.Textbox(label='API URL', lines=1),
        gr.Textbox(label='Optional API Key', lines=1),
        gr.Textbox(label='Request body (replace input field value with $INPUT)' , lines=3, placeholder='{"prompt" : $INPUT}'),
        gr.Textbox(label='Response body (replace output field value with $OUTPUT)', lines=3, placeholder='{"response" : $OUTPUT}'),
        gr.Textbox(label="OpenAI API Key"),
        gr.Dropdown(choices=["gpt-4o", "gpt-3.5-turbo", "gpt-4"], label="Model")
    ],
    outputs=gr.Textbox(label="Output", lines=27),
    title="Whistleblower 📣",
    description="A tool for inferring AI system prompts from generated responses, built by Repello AI.",
    theme="base",
    css=css
)

iface.launch()