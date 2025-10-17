# Contributing to Whistleblower

Thank you for your interest in contributing to Whistleblower! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Issue Reporting](#issue-reporting)
- [Documentation](#documentation)

## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

Whistleblower is a tool designed to infer the system prompt of an AI agent based on its generated text outputs. It leverages pretrained LLMs to analyze responses and generate detailed system prompts using the methodology from [Zhang et al.](https://arxiv.org/abs/2405.15012).

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Git

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/whistleblower.git
   cd whistleblower
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

4. **Test the installation**
   ```bash
   python main.py --json_file input_example.json
   ```

## Contributing Guidelines

### Types of Contributions

We welcome several types of contributions:

- **Bug fixes**: Fix issues in existing functionality
- **Feature enhancements**: Add new capabilities to the tool
- **Documentation improvements**: Update README, code comments, or this file
- **UI/UX improvements**: Enhance the Gradio interface
- **Performance optimizations**: Improve speed or efficiency
- **Testing**: Add unit tests or integration tests

### Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add appropriate comments
   - Update documentation if needed

3. **Test your changes**
   ```bash
   # Test command line interface
   python main.py --json_file input_example.json
   
   # Test web interface
   cd ui
   python app.py
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Project Structure

```
whistleblower/
├── core/                    # Core functionality
│   ├── __init__.py
│   ├── api.py              # External API communication
│   ├── attacker_system_prompt.txt  # Attacker model prompt
│   ├── judge_system_prompt.txt     # Judge model prompt
│   ├── seeds.py            # Seed data (if any)
│   ├── system_prompt.txt   # Main system prompt
│   ├── utils.py            # Utility functions
│   └── whistleblower.py    # Main logic
├── ui/                     # User interface
│   ├── __init__.py
│   ├── app.py             # Gradio web interface
│   └── styles.css         # UI styling
├── main.py                # Command line entry point
├── input_example.json     # Example configuration
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

### Key Components

- **`core/whistleblower.py`**: Main logic for system prompt extraction
- **`core/api.py`**: Handles external API calls to target models
- **`ui/app.py`**: Gradio web interface
- **`main.py`**: Command-line interface

## Testing

### Manual Testing

1. **Test with example configuration**
   ```bash
   python main.py --json_file input_example.json
   ```

2. **Test web interface**
   ```bash
   cd ui
   python app.py
   ```

3. **Test with different models**
   - Try different OpenAI models (gpt-4, gpt-3.5-turbo, gpt-4o)
   - Test with various API endpoints

### Automated Testing

We encourage adding unit tests for new functionality. Consider testing:

- API communication functions
- JSON parsing and validation
- Prompt generation logic
- Error handling

## Submitting Changes

### Pull Request Process

1. **Ensure your changes work**
   - Test both CLI and web interfaces
   - Verify with different model configurations
   - Check for any linting errors

2. **Write a clear description**
   - Explain what your changes do
   - Reference any related issues
   - Include screenshots for UI changes

3. **Follow the template**
   - Use the provided pull request template
   - Fill out all relevant sections

### Code Style Guidelines

- Use meaningful variable and function names
- Add docstrings for new functions
- Follow PEP 8 style guidelines
- Keep functions focused and modular
- Add type hints where appropriate

### Commit Message Format

Use clear, descriptive commit messages:

```
Add: feature description
Fix: bug description
Update: improvement description
Docs: documentation changes
```

## Issue Reporting

### Before Reporting

1. Check existing issues to avoid duplicates
2. Test with the latest version
3. Gather relevant information (error messages, logs, etc.)

### Bug Reports

Include the following information:

- **Description**: Clear description of the bug
- **Steps to reproduce**: Detailed steps to reproduce the issue
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: Python version, OS, dependencies
- **Configuration**: Your input JSON or API settings (remove sensitive keys)

### Feature Requests

For new features, please include:

- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives**: Other approaches you've considered

## Documentation

### Code Documentation

- Add docstrings to new functions and classes
- Include type hints for function parameters and returns
- Comment complex logic or algorithms

### User Documentation

- Update README.md for new features
- Add examples for new functionality
- Update this CONTRIBUTING.md as needed

## Security Considerations

⚠️ **Important Security Notes**

- Never commit API keys or sensitive credentials
- Be cautious when testing with production APIs
- Consider rate limiting and API usage costs
- Report security vulnerabilities privately to maintainers

## Community

- **Discussions**: Use GitHub Discussions for questions and ideas
- **Issues**: Use GitHub Issues for bugs and feature requests
- **Pull Requests**: Use GitHub Pull Requests for code contributions

## License

By contributing to Whistleblower, you agree that your contributions will be licensed under the same license as the project.

## Getting Help

If you need help getting started or have questions:

1. Check the [README.md](README.md) for basic usage
2. Look through existing [issues](https://github.com/Repello-AI/whistleblower/issues)
3. Start a [discussion](https://github.com/Repello-AI/whistleblower/discussions)
4. Contact the maintainers

Thank you for contributing to Whistleblower! 🚀
