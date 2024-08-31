# ui/app.py

import sys
import os

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import gradio as gr
from core.whistleblower import generate_output
from core.webhook_wrapper import WebhookWrapper

with open(os.path.join(os.path.dirname(__file__), 'styles.css'), 'r') as file:
    css = file.read()

def validate_input(host, openai_key, model):
    webhook_wrapper = WebhookWrapper(host)
    if not webhook_wrapper.connect():
        raise gr.Error("Failed to connect to the webhook. Please check your configuration.")

    try:
        return generate_output(webhook_wrapper, openai_key, model)
    finally:
        webhook_wrapper.close()

with gr.Blocks(css=css) as iface:
    gr.Markdown("# Whistleblower 📣\nA tool for leaking system prompts of LLM Apps, built by Repello AI.")
    with gr.Row():
        with gr.Column():
            host = gr.Textbox(label='Host', lines=1, value="sandbox-chat.leena.ai")
            openai_key = gr.Textbox(label="OpenAI API Key")
            model = gr.Dropdown(choices=["gpt-4-0314", "gpt-3.5-turbo", "gpt-4"], label="Model")
        with gr.Column():
            output = gr.Textbox(label="Output", lines=27)

    submit_btn = gr.Button("Submit")
    submit_btn.click(
        fn=validate_input,
        inputs=[host, openai_key, model],
        outputs=output
    )

if __name__ == "__main__":
    iface.launch()