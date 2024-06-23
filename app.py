import gradio as gr
from main import generate_output

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