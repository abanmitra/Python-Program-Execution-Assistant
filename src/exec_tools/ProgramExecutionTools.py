import importlib.util
import os
import sys
import traceback


class ProgramExecutionTools:
    @staticmethod
    def execute_program(file_path, parameters=None):
        """
        Dynamically load and execute a Python program with optional parameters.

        Args:
            file_path (str): Full path to the Python file
            parameters (dict, optional): Parameters to pass to execute() function

        Returns:
            tuple: (success, result/error)
        """
        try:
            # Add the directory containing the program to Python path
            sys.path.insert(0, os.path.dirname(file_path))

            module_name = os.path.splitext(os.path.basename(file_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Call execute function with parameters
            execute_func = getattr(module, 'execute', None)

            if not execute_func:
                return False, "No execute() function found in the program"

            # Prepare parameters
            parameters = parameters or {}
            result = execute_func(**parameters)

            return True, result

        except Exception as e:
            error_details = {
                'error_message': str(e),
                'traceback': traceback.format_exc()
            }
            return False, error_details
        finally:
            # Remove the temporarily added path
            sys.path.pop(0)
