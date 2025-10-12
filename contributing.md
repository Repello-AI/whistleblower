# Contributing to Whistleblower

Thank you for your interest in contributing to Whistleblower! We welcome contributions from the community and are grateful for any help you can provide.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Guidelines](#coding-guidelines)
- [Questions](#questions)
- [Recognition](#recognition)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors. Please be kind and considerate in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/whistleblower.git
   cd whistleblower
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/Repello-AI/whistleblower.git
   ```

## How to Contribute

There are many ways to contribute to Whistleblower:

-  **Report bugs** - Help us identify and fix issues
-  **Suggest features** - Share ideas for new functionality
-  **Improve documentation** - Help make our docs clearer and more comprehensive
-  **Submit bug fixes** - Fix issues you've found
-  **Add new features** - Implement requested features or your own ideas
-  **Write tests** - Improve test coverage
-  **Improve UI/UX** - Enhance the Gradio interface

## Development Setup

1. **Install Python** (version 3.8 or higher recommended)

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables**:
   - Create a `.env` file for your OpenAI API key (never commit this file)

5. **Verify the installation**:
   ```bash
   python main.py --help
   ```

## Pull Request Process

1. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   Use descriptive branch names:
   - `feature/add-new-model-support`
   - `fix/gradio-input-validation`
   - `documentation/update-readme`

2. **Make your changes** following our [coding guidelines](#coding-guidelines)

3. **Test your changes** thoroughly

4. **Commit your changes** with clear, descriptive messages:
   ```bash
   git commit -m "Add support for Claude API integration"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub:
   - Provide a clear title and description
   - Reference any related issues (e.g., "Fixes #123")
   - Include screenshots for UI changes
   - List any breaking changes

7. **Respond to feedback** - Be open to suggestions and iterate on your PR

## Coding Guidelines

### Python Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use meaningful variable and function names
- Keep functions focused and modular
- Add docstrings to functions and classes

## Questions

Have questions about contributing? Here's how to get help:

- **GitHub Issues** - Open an issue with the `question` label
- **Documentation** - Check the [README](README.md) first
- **Repello AI** - Visit [repello.ai](https://repello.ai/) for more information

## Recognition

Contributors will be recognized in our repository and documentation. Thank you for helping make Whistleblower better!

---

**Note**: By contributing to this project, you agree that your contributions will be licensed under the same license as the project.
