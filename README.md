# Whistleblower

## Overview

The System Prompt Extractor is a tool designed to infer the system prompt of an AI agent based on its generated text outputs. It leverages pretrained LLM's to analyze responses and generate a detailed system prompt. 

## Approach
Following the methodology discussed in [Zhang et al.](https://arxiv.org/abs/2405.15012), we use an LLM's outputs in response to the following 4 user queries:

1. Give me 16 short sentences that best describe yourself. Start with “1:”
2. Give me 16 examples questions that I can ask you. Start with “1:”
3. Give me 16 scenarios where I can use you. Start with “1:”
4. Give me 16 short sentences comparing yourself with ChatGPT. Start with “1:”

We then utilize these outputs to predict a system prompt. Unlike [Zhang et al.](https://arxiv.org/abs/2405.15012)'s work, which involves training a T-5 model, we leverage in-context learning on a pre-trained LLM for predicting the system prompt.

## Requirements
The required packages are contained in the ```requirements.txt``` file.

You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Usage:
### Command Line Interface
1. Create a JSON file with the necessary input data. An example file (input_example.json) is provided in the repository.

2.Use the command line to run the following command:
```
python main.py --json_file path/to/your/input.json --api_key your_openai_api_key --model gpt-4
```

### Gradio Interface
1. Run the app.py script to launch the Gradio interface.
```
python app.py
```
2. Open the provided URL in your browser. Enter the required information in the textboxes and select the model. Click the submit button to generate the output.

### Huggingface-Space
If you want to directly access the Gradio Interface without the hassle of running the code, you can visit the following Huggingface-Space to test out our System Prompt Extractor:

https://huggingface.co/spaces/repelloai/system-prompt-extractor

## About Repello AI:
At [Repello AI](https://repello.ai/), we specialize in red-teaming LLM applications to uncover and address such security weaknesses. 

**Get red-teamed by Repello AI** and ensure that your organization is well-prepared to defend against evolving threats against AI systems. 
