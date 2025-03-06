from typing import Dict, Any, List, Optional
from langchain_core.tools import BaseTool, Tool

class ProgramDiscoveryTool:
    """Wrapper for the program discovery functionality"""
    
    def __init__(self, programs_directory: str):
        self.programs_directory = programs_directory
        
    def __call__(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """Run the tool"""
        from src.exec_tools.ProgramDiscoveryTools import ProgramDiscoveryTools
        return ProgramDiscoveryTools.find_python_programs(self.programs_directory)
        
    def get_tool(self) -> Tool:
        """Create a LangChain Tool instance"""
        return Tool(
            name="program_discovery_tool",
            func=self.__call__,
            description="Discovers Python programs with execute() functions in a specified directory"
        )


class ProgramExecutionTool:
    """Wrapper for the program execution functionality"""
    
    def __call__(self, program: Dict[str, Any], parameters: Optional[Dict[str, Any]] = None) -> Any:
        """Run the tool"""
        from src.exec_tools.ProgramExecutionTools import ProgramExecutionTools
        
        # Ensure parameters is a dictionary
        parameters = parameters or {}
        
        # Execute the program
        success, result = ProgramExecutionTools.execute_program(
            program['path'],
            parameters
        )
        
        # Handle the result
        if success:
            return result
        else:
            raise Exception(f"Program Execution Failed: {result}")
    
    def get_tool(self) -> Tool:
        """Create a LangChain Tool instance"""
        return Tool(
            name="program_execution_tool",
            func=self.__call__,
            description="Executes a Python program with specified parameters"
        )