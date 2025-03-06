from textwrap import dedent

from crewai import Task

class ProgramExecutionTasks:

    def discover_programs(self, agent, directory):
        return Task(
            description=dedent(f"""
            Discover available Python programs in the specified directory.

            Parameters:
            - Directory: {directory}

            Task Instructions:
            1. Search the specified directory for Python programs
            2. Identify programs with an execute() function
            3. Collect program names, paths, and required parameters
            4. Present the discovered programs to the user
            """),
            agent=agent,
            expected_output=dedent("""
            A comprehensive list of discovered Python programs including:
            1. Program Name
            2. Full File Path
            3. Required Input Parameters (if any)
            4. Brief Description (if available)
            """)
        )

    def validate_program_parameters(self, agent, program_details):
        return Task(
            description=dedent(f"""
            Validate and collect parameters for the selected Python program.

            Program Details:
            - Name: {program_details['name']}
            - Path: {program_details['path']}
            - Required Parameters: {program_details['parameters']}

            Task Instructions:
            1. Interact with the user to collect all required parameters
            2. Validate each parameter's value and type
            3. Confirm parameter completeness and accuracy
            """),
            agent=agent,
            expected_output=dedent("""
            A validated set of parameters for program execution:
            1. Parameter Names
            2. Parameter Values
            3. Validation Confirmation
            4. User Approval Status
            """)
        )

    def execute_selected_program(self, agent, program_details, parameters):
        return Task(
            description=dedent(f"""
            Execute the selected Python program with validated parameters.

            Program Details:
            - Name: {program_details['name']}
            - Path: {program_details['path']}
            - Parameters: {parameters}

            Task Instructions:
            1. Load the Python program
            2. Call the execute() function with provided parameters
            3. Handle and report execution results
            4. Provide user-friendly output
            """),
            agent=agent,
            expected_output=dedent("""
            Execution Results:
            1. Execution Status (Success/Failure)
            2. Program Output
            3. Error Details (if applicable)
            4. Recommendations for further action
            """)
        )