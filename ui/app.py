import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from core.whistleblower import generate_output

with open('styles.css', 'r') as file:
    css = file.read()

iface = gr.Interface(
    fn=generate_output,
    inputs=[
        gr.Textbox(label='API URL', lines=1),
        gr.Textbox(label='Optional API Key', lines=1),
        gr.Textbox(label='Request body input field' , lines=1),
        gr.Textbox(label='Response body output field', lines=1),
        gr.Textbox(label="OpenAI API Key"),
        gr.Dropdown(choices=["gpt-4o", "gpt-3.5-turbo", "gpt-4"], label="Model")
    ],
    outputs=gr.Textbox(label="Output", lines=20),
    title="Whistleblower 📣",
    description="A tool for inferring AI system prompts from generated responses, built by Repello AI.",
    theme="base",
    css=css
)

iface.launch()
