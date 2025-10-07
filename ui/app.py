import sys
import os
import json

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from core.whistleblower import generate_output

with open('styles.css', 'r') as file:
    css = file.read()

def check_for_placeholders(data, placeholder):
    data = json.loads(data) if isinstance(data, str) else data
    if isinstance(data, dict):
        for key, value in data.items():
            if key == placeholder or value == placeholder:
                return True
            elif isinstance(value, (dict, list)):
                if check_for_placeholders(value, placeholder):
                    return True
    elif isinstance(data, list):
        for item in data:
            if item == placeholder:
                return True
            elif isinstance(item, (dict, list)):
                if check_for_placeholders(item, placeholder):
                    return True
    return False

def validate_input(api_url, api_key, payload_format, request_body_kv, request_body_json, response_body_kv , response_body_json, openai_key, model, transport):
    if payload_format == "JSON":
        if not request_body_json.strip():
            raise gr.Error("Request body cannot be empty.")
        if not response_body_json.strip():
            raise gr.Error("Response body cannot be empty.")
        request_body = request_body_json
        response_body = response_body_json
        try:
            request_body = json.dumps(json.loads(request_body))
        except json.JSONDecodeError:
            raise gr.Error("Invalid JSON format in request body.")
        try:
            response_body = json.dumps(json.loads(response_body))
        except json.JSONDecodeError:
            raise gr.Error("Invalid JSON format in response body.")
        if not check_for_placeholders(request_body, "$INPUT"):
            raise gr.Error("Request body must contain the $INPUT placeholder.")
        if not check_for_placeholders(response_body, "$OUTPUT"):
            raise gr.Error("Response body must contain the $OUTPUT placeholder.")
    else:
        if not request_body_kv.strip():
            raise gr.Error("Request body cannot be empty.")
        if not response_body_kv.strip():
            raise gr.Error("Response body cannot be empty.")
        request_body = {}
        for line in request_body_kv.split("\n"):
            if not line.strip():
                continue
            key, value = line.split(":")
            request_body[key.strip()] = value.strip()
        response_body = {}
        for line in response_body_kv.split("\n"):
            if not line.strip():
                continue
            key, value = line.split(":")
            response_body[key.strip()] = value.strip()
        

   
    return generate_output(api_url, api_key, request_body, response_body, openai_key, model, transport)

def update_payload_format(payload_format):
    if payload_format == "JSON":
        return gr.update(visible=False), gr.update(visible=True) , gr.update(visible=False), gr.update(visible=True)
    else:
        return gr.update(visible=True), gr.update(visible=False) , gr.update(visible=True), gr.update(visible=False)

with gr.Blocks(css=css) as iface:
    gr.Markdown("# Whistleblower 📣\nA tool for leaking system prompts of LLM Apps, built by Repello AI.")
    with gr.Row():
        with gr.Column():
                api_url = gr.Textbox(label='API URL', lines=1)
                api_key = gr.Textbox(label='Optional API Key', lines=1)
                payload_format = gr.Dropdown(choices=["Key-Value", "JSON"], label="Payload Format", value="Key-Value")
                transport = gr.Dropdown(choices=["REST", "WebSocket"], label="Transport", value="REST")
                request_body_kv = gr.Textbox(label='Request body (replace input field value with $INPUT)', lines=3, placeholder='prompt: $INPUT')
                request_body_json = gr.Textbox(label='Request body (replace input field value with $INPUT)', lines=3, placeholder='{\n\t"prompt": "$INPUT"\n}', visible=False)
                response_body_kv = gr.Textbox(label='Response body (replace output field value with $OUTPUT)', lines=3, placeholder='response: $OUTPUT')
                response_body_json = gr.Textbox(label='Response body (replace output field value with $OUTPUT)', lines=3, placeholder='{\n\t"response" : "$OUTPUT"\n}' , visible=False)
                openai_key = gr.Textbox(label="OpenAI API Key")
                model = gr.Dropdown(choices=["gpt-4o", "gpt-3.5-turbo", "gpt-4"], label="Model")
                with gr.Column():
                    output = gr.Textbox(label="Output", lines=27)
    
    payload_format.change(
        fn=update_payload_format,
        inputs=payload_format,
        outputs=[request_body_kv, request_body_json , response_body_kv , response_body_json]
    )
    
    submit_btn = gr.Button("Submit")
    submit_btn.click(
        fn=validate_input,
        inputs=[api_url, api_key, payload_format, request_body_kv, request_body_json, response_body_kv, response_body_json, openai_key, model, transport],
        outputs=output
    )

iface.launch()
