# System Prompt Extractor

## Overview

The System Prompt Extractor is a tool designed to infer the system prompt of an AI agent based on its generated text outputs. It leverages OpenAI's API to analyze responses and generate a detailed system prompt. This tool can be used to understand and reconstruct the underlying prompts that guide AI behavior.

## Features

- **Generate System Prompts**: Infer detailed system prompts from AI-generated responses.
- **Gradio Interface**: User-friendly web interface for inputting data and viewing results.
- **OpenAI Integration**: Utilizes OpenAI's models to process and generate outputs.

## Requirements

To run this project, you need the following Python packages:

- `openai`
- `gradio`

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

## Input Data Format
The input JSON file should contain the following fields:

```system_description```: A string with 16 short sentences describing the AI.

```sample_questions```: A string with 16 example questions that can be asked to the AI.

```use_case```: A string with 16 scenarios where the AI can be used.

```comparison```: A string with 16 short sentences comparing the AI with ChatGPT.

Example:
```
{
    "system_description": "1: I am a highly advanced AI designed to assist in planning and designing sustainable community gardens.\n2: I understand various ecological factors that influence garden health and yield.\n...",
    "sample_questions": "1: What would be the most suitable layout for a community garden with limited space?\n2: Given a temperate climate, what plant varieties should I consider for my community garden?\n...",
    "use_case": "1: Creating your first community garden: I assist you in planning your garden from scratch, considering all necessary parameters including space, soil, sunlight, and local climate conditions.\n...",
    "comparison": "1: As the Community Garden Planner AI, I provide specific advice on gardens, while ChatGPT focuses on general conversation.\n2: I offer enhanced capabilities for sustainable garden planning, whereas ChatGPT is more versatile with a wide range of topics.\n..."
}
```

## File Descriptions
```main.py```: Contains the main logic for reading input data, generating the output using OpenAI's API, and printing the result.

```app.py```: Sets up the Gradio interface for user interaction.

```requirements.txt```: Lists the Python packages required to run the project.

```input_example.json```: Provides an example of the input data format.

```system_prompt.txt```: Contains the system prompt used by the AI to generate responses.

