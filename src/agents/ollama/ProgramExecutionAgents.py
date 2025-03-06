import os
from textwrap import dedent

from crewai import Agent
from dotenv import load_dotenv
import litellm
from langchain.llms.base import LLM
from typing import Any, Dict, List, Mapping, Optional

# Import the custom tools
from src.exec_tools.CustomTools import ProgramDiscoveryTool, ProgramExecutionTool

load_dotenv()


# Create a custom LangChain LLM that uses LiteLLM directly
class LiteLLMWrapper(LLM):
    model_name: str = None
    temperature: float = None
    
    def _llm_type(self) -> str:
        return "custom_litellm"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        response = litellm.completion(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            stop=stop
        )
        return response.choices[0].message.content


class ProgramExecutionAgents:
    def __init__(self, programs_directory):
        """
        Initialize agents with a specific programs directory.

        Args:
            programs_directory (str): Path to the directory containing Python programs
        """
        self.programs_directory = programs_directory
 
        # Direct LiteLLM integration
        self.llm = LiteLLMWrapper(
            model_name=os.getenv("OLLAMA_MODEL", "ollama/llama3").strip(),
            model_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip(),
            temperature=float(os.getenv("OLLAMA_TEMPERATURE", 0.7))
        )        

    def program_execution_agent(self):
        """
        Create an agent for program discovery and execution.

        Returns:
            Agent: Configured CrewAI agent
        """
        # Create tool instances with the programs directory
        discovery_tool = ProgramDiscoveryTool(self.programs_directory)
        execution_tool = ProgramExecutionTool()

        # Get the LangChain Tool objects
        discovery_langchain_tool = discovery_tool.get_tool()
        execution_langchain_tool = execution_tool.get_tool()

        return Agent(
            role="Python Program Execution Specialist",
            backstory=dedent("""
            A friendly and intelligent AI assistant specialized in discovering, understanding, 
            and executing Python programs. Skilled at interactive communication, parameter 
            validation, and ensuring smooth program execution.
            """),
            goal=dedent("""
            Assist users in discovering, understanding, and successfully executing 
            Python programs by gathering accurate information, verifying parameters, 
            and providing clear guidance throughout the process.
            """),
            tools=[
                discovery_langchain_tool,
                execution_langchain_tool
            ],
            verbose=True,
            llm=self.llm
        )