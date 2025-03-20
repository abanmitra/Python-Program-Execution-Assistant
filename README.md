# 🐍 Python Program Execution Assistant

![Python Program Execution Assistant](https://img.shields.io/badge/Python-Program%20Execution-blue)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B)
![CrewAI](https://img.shields.io/badge/Powered%20by-CrewAI-green)

A powerful web application that helps you discover, manage, and execute Python programs with AI assistance. This tool simplifies the process of finding Python programs in a directory, understanding their parameters, and executing them with proper inputs.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
  - [Starting the Application](#starting-the-application)
  - [Selecting a Directory](#selecting-a-directory)
  - [Discovering Programs](#discovering-programs)
  - [Executing Programs](#executing-programs)
  - [Viewing Results](#viewing-results)
- [Code Structure](#code-structure)
- [Customization and Configuration](#customization-and-configuration)
  - [Environment Variables](#environment-variables)
  - [Adding Custom Tools](#adding-custom-tools)
- [Troubleshooting and FAQs](#troubleshooting-and-faqs)
- [Future Roadmap](#future-roadmap)
- [License](#license)
- [Contact Information](#contact-information)

## 🔍 Project Overview

The Python Program Execution Assistant is designed to help developers, data scientists, and even non-technical users run Python programs without needing to understand the underlying code. It uses AI-powered agents (via CrewAI) to:

1. **Discover** Python programs in a specified directory
2. **Identify** required parameters for execution
3. **Validate** user inputs
4. **Execute** programs and display results in a user-friendly format

This application is perfect for:
- Teams sharing Python utilities
- Data scientists running analysis scripts
- Educators demonstrating code execution
- Anyone who wants to run Python programs without writing code

## ✨ Features

- **Intuitive Web Interface**: Built with Streamlit for a clean, responsive user experience
- **Automatic Program Discovery**: Finds Python programs with `execute()` functions in any directory
- **Parameter Detection**: Automatically identifies required parameters for each program
- **AI-Assisted Execution**: Uses CrewAI to intelligently handle program execution
- **Beautiful Results Display**: Formats execution results in an easy-to-understand way
- **Error Handling**: Provides clear error messages and troubleshooting information
- **Customizable**: Configure the application to suit your needs

## 💻 Installation

### Prerequisites

Before installing the Python Program Execution Assistant, ensure you have:

- Python 3.8 or higher installed
- Pip package manager
- Ollama (for local LLM execution) or access to OpenAI API (optional)

### Setup Instructions

1. **Clone or download the repository**:

```bash
git clone https://github.com/abanmitra/Python-Program-Execution-Assistant.git
cd python-program-execution-assistant
```

2. **Create and activate a virtual environment** (recommended):

```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python -m venv .venv
source ./venv/bin/activate
```

3. **Install required dependencies**:

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:

Create a `.env` file in the root directory with the following configuration:

```
# Ollama Configuration (for local model)
OLLAMA_MODEL=ollama/deepseek-r1:14b
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TEMPERATURE=0.8

# Application Configuration
DEFAULT_PROGRAMS_DIRECTORY=/path/to/your/programs
```

5. **Install and start Ollama** (if using local models):

Follow the instructions at [Ollama's official website](https://ollama.ai/) to install Ollama and download the required model (e.g., `deepseek-r1:14b`).

## 🚀 Usage Guide

### Starting the Application

Run the application with:

```bash
application_root$ streamlit run .\src\app.py
```

This will start the web server and open the application in your default browser. If it doesn't open automatically, navigate to `http://localhost:8501`.

### Selecting a Directory

1. When the application starts, you'll see the directory selection section at the top.
2. You can either:
   - Enter the path manually in the text field
   - Use the directory browser (select any file in your target directory)
3. Click the "Confirm Directory" button to proceed.

### Discovering Programs

1. After confirming the directory, click the "Discover Available Programs" button.
2. The application will scan the directory for Python files with `execute()` functions.
3. Discovered programs will be displayed with their names, paths, and required parameters.

### Executing Programs

1. Select a program from the dropdown menu in the "Program Execution" section.
2. Fill in the required parameters for the selected program.
3. Click the "Execute Program" button to run the program.
4. The execution progress will be displayed in real-time in the right panel.

### Viewing Results

After execution:
1. The application will display a "Execution Results" section at the bottom.
2. For successful executions, you'll see:
   - Program output formatted in a user-friendly way
   - Key metrics (if available)
   - Visualizations (for numerical data)
3. For failed executions, you'll see detailed error information.

## 📁 Code Structure

The application is organized into the following structure:

```
my_project/
│
├── src/                  # Source code directory
├── .env                  # Environment variables
├── requirements.txt      # Dependencies
├── app.py                # Main application file
├── agents/               # AI Agents configuration
│     └── ollama/
│           └── ProgramExecutionAgents.py
├── tasks/                # Task definitions
│     └── ProgramExecutionTasks.py
└── exec_tools/           # Execution tools
      ├── CustomTools.py
      ├── ProgramDiscoveryTools.py
      └── ProgramExecutionTools.py
```

Key components:

- **app.py**: The main Streamlit application that defines the user interface and workflow
- **ProgramExecutionAgents.py**: Defines the AI agents that discover and execute programs
- **ProgramExecutionTasks.py**: Defines tasks for program discovery, parameter validation, and execution
- **CustomTools.py**: Wrapper classes for program discovery and execution tools
- **ProgramDiscoveryTools.py**: Tools for finding and inspecting Python programs
- **ProgramExecutionTools.py**: Tools for dynamically loading and executing Python programs

## ⚙️ Customization and Configuration

### Environment Variables

You can customize the application by modifying the following environment variables in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_MODEL` | The AI model to use for program execution | `ollama/deepseek-r1:14b` |
| `OLLAMA_BASE_URL` | URL for the Ollama API | `http://localhost:11434` |
| `OLLAMA_TEMPERATURE` | Temperature setting for the AI model (higher = more creative) | `0.8` |
| `DEFAULT_PROGRAMS_DIRECTORY` | Default directory to search for Python programs | - |

**Reference**: [Custom Ollama Model Creation](https://www.gpu-mart.com/blog/custom-llm-models-with-ollama-modelfile)


### Adding Custom Tools

To extend the application with custom tools:

1. Create a new Python file in the `src/exec_tools` directory.
2. Implement your tool class following the pattern in `CustomTools.py`.
3. Register your tool with the agent in `ProgramExecutionAgents.py`.

Example for a custom tool:

```python
# In a new file, e.g., MyCustomTool.py
from langchain_core.tools import Tool

class MyCustomTool:
    """A custom tool for specific functionality"""
    
    def __call__(self, *args, **kwargs):
        # Implement your functionality here
        return result
        
    def get_tool(self) -> Tool:
        """Create a LangChain Tool instance"""
        return Tool(
            name="my_custom_tool",
            func=self.__call__,
            description="Description of what your tool does"
        )

# Then in ProgramExecutionAgents.py, add:
from src.exec_tools.MyCustomTool import MyCustomTool

# And in the program_execution_agent method:
my_tool = MyCustomTool()
my_langchain_tool = my_tool.get_tool()

# Add to the tools list:
tools=[
    discovery_langchain_tool,
    execution_langchain_tool,
    my_langchain_tool
]
```

## ❓ Troubleshooting and FAQs

### Common Issues

#### 1. "Directory does not exist or is not valid" error
- Make sure the directory path is correct and accessible.
- Use absolute paths (like `C:/Users/username/projects`) instead of relative paths.

#### 2. "No Python programs with execute() function found" message
- Ensure your Python files have an `execute()` function.
- Check that the files don't have syntax errors.
- Make sure the directory doesn't contain only Python packages or modules.

#### 3. "Program execution failed" error
- Check that all required parameters are provided correctly.
- Look at the error details for specific error messages from your program.
- Make sure your `execute()` function handles exceptions properly.

#### 4. Ollama connection issues
- Ensure Ollama is installed and running (`ollama run deepseek-r1:14b`).
- Check that the `OLLAMA_BASE_URL` in your `.env` file matches your Ollama installation.
- Verify that the model specified in `OLLAMA_MODEL` is downloaded in Ollama.

### Frequently Asked Questions

#### What is the `execute()` function requirement?
The application looks for Python files that contain an `execute()` function. This function should:
- Accept parameters that users will provide through the UI
- Return results that can be displayed in the UI
- Handle exceptions gracefully

#### How do I create a compatible Python program?
Here's a simple example:

```python
# example_program.py

def execute(name="World", times=1):
    """
    A simple greeting program.
    
    Parameters:
    - name (str): Name to greet
    - times (int): Number of times to repeat the greeting
    
    Returns:
    - dict: Greeting results
    """
    try:
        # Convert times to int if it's a string
        times = int(times) if isinstance(times, str) else times
        
        # Create the greeting
        greeting = f"Hello, {name}!"
        repeated = [greeting] * times
        
        # Return results
        return {
            "greeting": greeting,
            "repeated": repeated,
            "count": times
        }
    except Exception as e:
        return {"error": str(e)}
```

#### Can I use the application with remote APIs?
Yes, you can modify the `.env` file to use OpenAI or other API-based models instead of Ollama. You'll need to update the configuration and potentially modify the agent setup in `ProgramExecutionAgents.py`.

## 🛣️ Future Roadmap [ not in near future 😊 ]

Future enhancements planned for the Python Program Execution Assistant:

- **Program Editing**: Add functionality to edit discovered programs directly from the UI
- **Batch Execution**: Enable running multiple programs in sequence
- **Scheduled Execution**: Add the ability to schedule program execution
- **Result Export**: Add options to export execution results in various formats
- **User Authentication**: Add user authentication for secure access
- **Program Templates**: Provide templates for creating new compatible programs
- **Custom UI Themes**: Allow users to customize the appearance of the application

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📬 Contact Information

For questions, support, or feedback, please contact:

- Email: difworksaban@gmail.com
- GitHub: [Python Program Execution Assistant](https://github.com/abanmitra/Python-Program-Execution-Assistant)

---

Thank you for using the Python Program Execution Assistant! We hope it makes your Python program management easier and more efficient.
