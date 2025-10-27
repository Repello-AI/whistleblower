import sys
import os
import json

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from core.whistleblower import generate_output

with open('styles.css', 'r') as file:
    css = file.read()

with open('script.js', 'r') as file:
    js_code = f'<script>{file.read()}</script>'

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

def validate_input(api_url, api_key, payload_format, request_body_kv, request_body_json, response_body_kv , response_body_json, openai_key, model):
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

    return generate_output(api_url, api_key, request_body, response_body, openai_key, model)

def update_payload_format(payload_format):
    if payload_format == "JSON":
        return gr.update(visible=False), gr.update(visible=True) , gr.update(visible=False), gr.update(visible=True)
    else:
        return gr.update(visible=True), gr.update(visible=False) , gr.update(visible=True), gr.update(visible=False)

with gr.Blocks(css=css, head=js_code) as iface:
    gr.Markdown("# Whistleblower 📣\nA tool for leaking system prompts of LLM Apps, built by Repello AI.")

    # Main horizontal layout: left for inputs, right for output
    with gr.Row():
        # --- Left Column (Inputs) ---
        # assign an elem_id so JS can reliably target this column
        with gr.Column(elem_id="input-column"):
            # Group for API connection inputs
            with gr.Group():
                with gr.Row():
                    # Textbox for the target API URL
                    api_url = gr.Textbox(
                        label="Target API URL",
                        lines=1,
                        placeholder="https://example.com/query",
                        info="Endpoint to send the synthesized request to"
                    )
                    # Optional API key/token for the target API
                    api_key = gr.Textbox(
                        label="Optional API Key",
                        lines=1,
                        placeholder="Bearer ... or API key (if required)",
                        info="Optional key or token to access the target API"
                    )

            # Group for payload format selection and body templates
            with gr.Group():
                # Dropdown to choose Key-Value or JSON payload entry
                payload_format = gr.Dropdown(
                    choices=["Key-Value", "JSON"],
                    label="Payload Format",
                    value="Key-Value",
                    info="Choose how you'll enter the request/response bodies"
                )

                # Two columns inside this group: request templates and response templates
                with gr.Row():
                    with gr.Column():
                        # Key/Value style request body textbox (visible by default)
                        request_body_kv = gr.Textbox(
                            label='Request body — Key/Value (use $INPUT)',
                            lines=4,
                            placeholder='prompt: $INPUT\nuser_id: 123',
                            info="Enter each pair on its own line as key: value. Use $INPUT placeholder where the user input should go."
                        )
                        # JSON style request body textbox (hidden by default)
                        request_body_json = gr.Textbox(
                            label='Request body — JSON (use $INPUT)',
                            lines=6,
                            placeholder='{\n  \"prompt\": \"$INPUT\"\n}',
                            visible=False,
                            info="Enter a valid JSON payload. Include $INPUT somewhere in the values."
                        )

                    with gr.Column():
                        # Key/Value style response body textbox (visible by default)
                        response_body_kv = gr.Textbox(
                            label='Response body — Key/Value (use $OUTPUT)',
                            lines=4,
                            placeholder='response: $OUTPUT\nconfidence: 0.9',
                            info="Each pair on its own line. Use $OUTPUT to indicate where the model output will be placed."
                        )
                        # JSON style response body textbox (hidden by default)
                        response_body_json = gr.Textbox(
                            label='Response body — JSON (use $OUTPUT)',
                            lines=6,
                            placeholder='{\n  \"response\": \"$OUTPUT\"\n}',
                            visible=False,
                            info="Enter a valid JSON template. Include $OUTPUT somewhere in the values."
                        )

            # Group for OpenAI extraction key and model selection
            with gr.Group():
                # Hidden/password textbox for the OpenAI API key
                openai_key = gr.Textbox(
                    label="OpenAI API Key",
                    type="password",
                    placeholder="sk-...",
                    info="OpenAI key used to run the extraction model (kept hidden)."
                )
                # Dropdown to select which OpenAI model to use
                model = gr.Dropdown(
                    choices=["gpt-4o", "gpt-4", "gpt-3.5-turbo"],
                    label="Model",
                    value="gpt-4o",
                    info="Select the OpenAI model to use for extracting the hidden prompt."
                )

        # --- Right Column (Output) ---
        # Single column that holds the non-interactive output textbox
        # give it an elem_id so JS can target it and find the inner textarea reliably
        with gr.Column(elem_classes="full-height-col"):
            output = gr.Textbox(
                label="Extracted Prompt",
                lines=27,
                interactive=False,
                placeholder="The extracted system prompt will appear here after submission.",
                elem_id="extracted-prompt"
            )

    payload_format.change(
        fn=update_payload_format,
        inputs=payload_format,
        outputs=[request_body_kv, request_body_json , response_body_kv , response_body_json]
    )

    submit_btn = gr.Button("Submit")
    submit_btn.click(
        fn=validate_input,
        inputs=[api_url, api_key, payload_format, request_body_kv, request_body_json, response_body_kv, response_body_json, openai_key, model],
        outputs=output
    )

iface.launch()
