import importlib.util
import inspect
import os


class ProgramDiscoveryTools:
    @staticmethod
    def find_python_programs(directory):
        """
        Find all Python files with an execute() function in the specified directory.

        Args:
            directory (str): Path to the directory containing Python programs

        Returns:
            list: List of discovered Python program details
        """
        programs = []

        # Ensure the directory exists and is a valid path
        if not os.path.exists(directory) or not os.path.isdir(directory):
            print(f"Warning: Directory {directory} does not exist or is not a directory.")
            return programs

        # Define directories and file patterns to ignore
        ignore_dirs = [
            '.venv', 'venv', 'env','.git', '.github',
            '__pycache__','site-packages','dist', 
            'build', 'Include', 'Lib', 'Scripts', 
            'tcl', 'Tools', 'DLLs', 'pyvenv.cfg',
            'share', 'bin', 'include', '.cfg'
        ]

        # Walk through the directory
        for root, dirs, files in os.walk(directory):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]

            for file in files:
                # Only process .py files that are not in ignored directories
                if file.endswith('.py') and not file.startswith('__'):
                    full_path = os.path.join(root, file)

                    # Skip files in virtual environment or package directories
                    if any(ignored in full_path.split(os.path.sep) for ignored in ignore_dirs):
                        continue

                    program_info = ProgramDiscoveryTools.inspect_program(full_path)
                    if program_info:
                        programs.append(program_info)

        return programs

    @staticmethod
    def inspect_program(file_path):
        """
        Inspect a Python file to check for an execute() function and its parameters.

        Args:
            file_path (str): Full path to the Python file

        Returns:
            dict: Program details or None if no execute() function found
        """
        try:
            # Validate file path
            if not os.path.isfile(file_path):
                return None

            module_name = os.path.splitext(os.path.basename(file_path))[0]

            # Use importlib to safely import the module
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)

            # Add the directory to sys.path temporarily
            import sys
            original_path = sys.path.copy()
            sys.path.insert(0, os.path.dirname(file_path))

            try:
                spec.loader.exec_module(module)
            except Exception as e:
                print(f"Error loading module {file_path}: {e}")
                return None
            finally:
                # Restore original sys.path
                sys.path = original_path

            # Find the execute function
            execute_func = getattr(module, 'execute', None)

            if execute_func and callable(execute_func):
                # Inspect function parameters
                signature = inspect.signature(execute_func)
                parameters = list(signature.parameters.keys())

                return {
                    'name': module_name,
                    'path': file_path,
                    'parameters': parameters
                }

        except Exception as e:
            print(f"Error inspecting {file_path}: {e}")

        return None
