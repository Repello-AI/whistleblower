import gradio as gr
from main import generate_output

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
        gr.Dropdown(choices=["gpt-4o", "gpt-3.5-turbo", "gpt-4-0613"], label="Model")
    ],
    outputs=gr.Textbox(label="Output", lines=20),
    title="System Prompt Extractor",
    description="A tool for inferring AI system prompts from generated responses, built by Repello AI.",
    theme="base",
    css=css
)

iface.launch()