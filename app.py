import gradio as gr
from main import generate_output

with open('styles.css', 'r') as file:
    css = file.read()

iface = gr.Interface(
    fn=generate_output,
    inputs=[
        gr.Textbox(label='''Give me 16 short sentences that best describe yourself. Start with "1:"''', lines=2),
        gr.Textbox(label='''Give me 16 example questions that I can ask you. Start with "1:"''', lines=2),
        gr.Textbox(label='''Give me 16 scenarios where I can use you. Start with "1:"''', lines=2),
        gr.Textbox(label='''Give me 16 short sentences comparing yourself with ChatGPT. Start with "1:"''', lines=2),
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