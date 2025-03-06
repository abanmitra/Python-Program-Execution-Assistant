import os
import time
import json

import streamlit as st
from crewai import Crew
from dotenv import load_dotenv

from agents.ollama.ProgramExecutionAgents import ProgramExecutionAgents
from src.exec_tools.ProgramDiscoveryTools import ProgramDiscoveryTools
from src.tasks.ProgramExecutionTasks import ProgramExecutionTasks

load_dotenv()


class ProgramExecutionApp:
    def __init__(self):
        self.default_programs_directory = os.getenv('DEFAULT_PROGRAMS_DIRECTORY', 'D:/work/GenAI/crewai/sample_app')
        # Initialize with None, will be set by user
        self.programs_directory = None
        # Initialize agents and tasks after user selects directory
        self.agents = None
        self.tasks = None

    def run_streamlit_app(self):
        st.set_page_config(layout="wide", page_title="Python Program Execution Assistant")
        
        st.title("🐍 Python Program Execution Assistant")
        
        # Directory Selection Section
        st.header("🔍 Select Programs Directory")
        
        # Create a two-column layout for directory selection
        dir_col1, dir_col2 = st.columns([1, 1])
        
        with dir_col1:
            # Manual directory input
            user_input_directory = st.text_input(
                "Enter programs directory path:", 
                value=self.default_programs_directory,
                placeholder="e.g., C:/Users/username/my_python_programs",
                help="Enter the full path to the directory containing your Python programs"
            )
        
        with dir_col2:
            # Alternative: Directory browser
            st.write("Or use directory browser:")
            browse_directory = st.checkbox("Browse for directory", value=False)
            
            if browse_directory:
                st.info("Note: Due to security restrictions, the file browser can only show files, not folders. "
                       "Please select any file from your target directory, and we'll use its parent directory.")
                uploaded_file = st.file_uploader(
                    "Select any file from your target directory:", 
                    type=["py", "txt", "md", "json"],
                    help="We'll use the parent directory of the selected file"
                )
                
                if uploaded_file:
                    # In a real environment, we would extract the directory path
                    # For now, show a dialog to manually confirm the directory
                    st.success("File selected. Please confirm the directory path below.")
                    file_directory = st.text_input(
                        "Confirm directory path:", 
                        value=os.path.dirname(user_input_directory)
                    )
                    if file_directory:
                        user_input_directory = file_directory
        
        # Directory confirmation button
        if st.button("Confirm Directory"):
            # Validate directory exists
            if os.path.exists(user_input_directory) and os.path.isdir(user_input_directory):
                self.programs_directory = user_input_directory
                st.session_state.selected_directory = user_input_directory
                
                # Initialize the agents and tasks with the selected directory
                self.agents = ProgramExecutionAgents(self.programs_directory)
                self.tasks = ProgramExecutionTasks()
                
                st.success(f"Directory confirmed: {self.programs_directory}")
            else:
                st.error(f"Directory does not exist or is not valid: {user_input_directory}")
                self.programs_directory = None
                if 'selected_directory' in st.session_state:
                    del st.session_state.selected_directory
        
        # Store directory in session state for persistence
        if 'selected_directory' in st.session_state:
            self.programs_directory = st.session_state.selected_directory
            # Ensure agents and tasks are initialized
            if self.agents is None:
                self.agents = ProgramExecutionAgents(self.programs_directory)
            if self.tasks is None:
                self.tasks = ProgramExecutionTasks()
        
        # Only display rest of the app if directory is selected
        if self.programs_directory:
            st.markdown("---")
            # Create a two-column layout for the main interface
            left_col, right_col = st.columns([2, 3])
            
            with left_col:
                # Program Discovery
                st.header("Program Discovery")
                if st.button("Discover Available Programs"):
                    with st.spinner("Discovering programs..."):
                        programs = ProgramDiscoveryTools.find_python_programs(self.programs_directory)
                    
                    # Store discovered programs in session state
                    st.session_state.discovered_programs = programs
                    
                    st.write("Discovered Programs:")
                    if programs:
                        for program in programs:
                            with st.expander(f"{program['name']}"):
                                st.write(f"Path: {program['path']}")
                                st.write("Parameters:")
                                for param in program['parameters']:
                                    st.write(f"- {param}")
                    else:
                        st.warning(f"No Python programs with execute() function found in {self.programs_directory}")
                
                # Show previously discovered programs if available
                elif 'discovered_programs' in st.session_state:
                    st.write("Discovered Programs:")
                    programs = st.session_state.discovered_programs
                    if programs:
                        for program in programs:
                            with st.expander(f"{program['name']}"):
                                st.write(f"Path: {program['path']}")
                                st.write("Parameters:")
                                for param in program['parameters']:
                                    st.write(f"- {param}")
                    else:
                        st.warning(f"No Python programs with execute() function found in {self.programs_directory}")

                # Program Selection and Execution
                st.header("Program Execution")
                
                # Only show program selection if programs are discovered
                if 'discovered_programs' in st.session_state and st.session_state.discovered_programs:
                    # Create a dropdown for program selection instead of text input
                    program_names = [p['name'] for p in st.session_state.discovered_programs]
                    selected_program_name = st.selectbox("Select Program", options=program_names)
                    
                    if selected_program_name:
                        # Get details of selected program
                        selected_program = next((p for p in st.session_state.discovered_programs if p['name'] == selected_program_name), None)
                        
                        if selected_program:
                            st.write(f"Selected Program: {selected_program['name']}")
                            st.write(f"Path: {selected_program['path']}")
                            
                            # Dynamic Parameter Collection
                            parameters = {}
                            for param in selected_program['parameters']:
                                param_value = st.text_input(f"Enter value for parameter '{param}'")
                                if param_value:
                                    parameters[param] = param_value
                        else:
                            st.error(f"Program '{selected_program_name}' not found.")
                else:
                    st.info("Please discover programs first using the button above.")
            
            # Create a container for execution output in the right column with matching height
            with right_col:
                st.header("Execution Output")
                # Calculate approximate height to match the left side input area
                output_container = st.container()
                
                # Only show the execution button in the left column after setup
                if 'discovered_programs' in st.session_state and st.session_state.discovered_programs and 'selected_program' in locals() and selected_program:
                    with left_col:
                        execute_button = st.button("Execute Program")
                        
                        if execute_button:
                            # Initialize CrewAI Agents and Tasks
                            program_agent = self.agents.program_execution_agent()
                            
                            # Create the execution task
                            execute_task = self.tasks.execute_selected_program(
                                program_agent,
                                selected_program,
                                parameters
                            )
                            
                            crew = Crew(
                                agents=[program_agent],
                                tasks=[execute_task],
                                verbose=True
                            )
                            
                            # Show progress and execution details in the right column
                            with output_container:
                                # Create progress display with percentage
                                progress_placeholder = st.empty()
                                status_text = st.empty()
                                
                                # Add a scrollable container with fixed height for execution logs
                                # This will match the approximate height of the input area
                                log_container = st.container()
                                execution_log = log_container.empty()
                                
                                # Prepare execution logs
                                execution_logs = []
                                
                                # Step 1: Initialize
                                progress_value = 10
                                progress_placeholder.progress(progress_value / 100)
                                status_text.write(f"⏳ Initializing execution environment... ({progress_value}%)")
                                execution_logs.append("🚀 Starting execution of program: " + selected_program['name'])
                                execution_log.code("\n".join(execution_logs), language="text", height=600)
                                time.sleep(0.5)
                                
                                # Step 2: Parameter validation
                                progress_value = 30
                                progress_placeholder.progress(progress_value / 100)
                                status_text.write(f"⏳ Validating parameters... ({progress_value}%)")
                                execution_logs.append("✅ Parameters validated:")
                                for key, value in parameters.items():
                                    execution_logs.append(f"  - {key}: {value}")
                                execution_log.code("\n".join(execution_logs), language="text", height=600)
                                time.sleep(0.5)
                                
                                # Step 3: Loading program
                                progress_value = 50
                                progress_placeholder.progress(progress_value / 100)
                                status_text.write(f"⏳ Loading program... ({progress_value}%)")
                                execution_logs.append(f"📂 Loading program from {selected_program['path']}")
                                execution_log.code("\n".join(execution_logs), language="text", height=600)
                                time.sleep(0.5)
                                
                                # Step 4: Executing
                                progress_value = 75
                                progress_placeholder.progress(progress_value / 100)
                                status_text.write(f"⏳ Executing program... ({progress_value}%)")
                                execution_logs.append("⚙️ Executing program with provided parameters")
                                execution_log.code("\n".join(execution_logs), language="text", height=600)
                                
                                # Step 5: Execute program using CrewAI
                                try:
                                    # Capture CrewAI's verbose output
                                    import io
                                    import sys
                                    from contextlib import redirect_stdout

                                    # Redirect stdout to capture CrewAI's verbose output
                                    f = io.StringIO()
                                    with redirect_stdout(f):
                                        result = crew.kickoff()
                                    
                                    # Get the CrewAI output and add it to execution logs
                                    crewai_output = f.getvalue()
                                    execution_logs.append("\n--- Agent Execution Details ---\n")
                                    execution_logs.append(crewai_output)
                                    
                                    progress_value = 100
                                    progress_placeholder.progress(progress_value / 100)
                                    status_text.write(f"✅ Program executed successfully! ({progress_value}%)")
                                    execution_logs.append("\n✅ Execution completed successfully")
                                    execution_log.code("\n".join(execution_logs), language="text", height=600)
                                    
                                    # Store the full results
                                    st.session_state.execution_result = result
                                    st.session_state.execution_success = True
                                    st.session_state.crewai_output = crewai_output
                                except Exception as e:
                                    progress_value = 100
                                    progress_placeholder.progress(progress_value / 100)
                                    status_text.write(f"❌ Program execution failed! ({progress_value}%)")
                                    execution_logs.append(f"❌ Execution error: {str(e)}")
                                    execution_log.code("\n".join(execution_logs), language="text", height=600)
                                    st.session_state.execution_result = str(e)
                                    st.session_state.execution_success = False
        
        # Create a dedicated results section at the bottom
        if 'execution_result' in st.session_state:
            st.markdown("---")
            st.header("📊 Execution Results")
            
            # Different styling based on success/failure
            if st.session_state.execution_success:
                # Try to parse the result if it's in JSON format
                try:
                    if isinstance(st.session_state.execution_result, str):
                        result_data = json.loads(st.session_state.execution_result)
                    else:
                        result_data = st.session_state.execution_result
                    
                    # Enhanced visualization with better formatting
                    st.success("✨ Program executed successfully!")
                    
                    # Format results in a more user-friendly way
                    self.display_formatted_results(result_data)
                        
                except (json.JSONDecodeError, AttributeError, TypeError):
                    # If not JSON or an error occurs during parsing
                    st.success("✨ Program executed successfully!")
                    st.markdown(f"**Program Output:**\n{st.session_state.execution_result}")
            else:
                # Error result
                st.error("⚠️ Program execution failed")
                st.markdown("### Error Details")
                st.code(st.session_state.execution_result)
    
    def display_formatted_results(self, result_data):
        """Display results in a beautiful and user-friendly format"""
        if isinstance(result_data, dict):
            # Skip technical sections
            sections_to_skip = ['pydantic', 'json_dict']
            
            # Replace technical section names with user-friendly ones
            friendly_names = {
                'raw': 'Complete Output',
                'tasks_output': 'Task Results',
                'token_usage': 'Performance Metrics'
            }
            
            # Find if there's a summary section
            if 'summary' in result_data:
                st.markdown("### Key Findings")
                st.markdown(result_data['summary'])
                st.markdown("---")
            
            # Display each section with improved formatting
            for key, value in result_data.items():
                # Skip technical sections
                if key in sections_to_skip:
                    continue
                
                # Use friendly names
                display_name = friendly_names.get(key, key.replace('_', ' ').title())
                
                if key != 'summary':  # Already displayed summary above
                    st.markdown(f"### {display_name}")
                    
                    # Format the section based on its content type
                    if isinstance(value, dict):
                        # For dictionary values
                        for subkey, subvalue in value.items():
                            st.markdown(f"#### {subkey.replace('_', ' ').title()}")
                            if isinstance(subvalue, list):
                                for item in subvalue:
                                    if isinstance(item, dict):
                                        # Handle nested dictionaries
                                        st.markdown("---")
                                        for ikey, ivalue in item.items():
                                            st.markdown(f"**{ikey.replace('_', ' ').title()}**: {ivalue}")
                                    else:
                                        st.markdown(f"• {item}")
                            elif isinstance(subvalue, dict):
                                # Handle nested dictionaries
                                for nkey, nvalue in subvalue.items():
                                    st.markdown(f"**{nkey.replace('_', ' ').title()}**: {nvalue}")
                            else:
                                st.markdown(f"{subvalue}")
                    
                    elif isinstance(value, list):
                        # For list values, create bullet points
                        for item in value:
                            if isinstance(item, dict):
                                # For a list of dictionaries, create subsections
                                st.markdown("---")
                                for ikey, ivalue in item.items():
                                    st.markdown(f"**{ikey.replace('_', ' ').title()}**: {ivalue}")
                            else:
                                st.markdown(f"• {item}")
                    else:
                        # For simple values
                        st.markdown(f"{value}")
            
            # Display any numeric data as a chart
            numeric_data = {k: v for k, v in result_data.items() 
                            if isinstance(v, (int, float)) and k not in ['status_code']}
            if numeric_data:
                st.markdown("### Key Metrics")
                st.bar_chart(numeric_data)
        
        elif isinstance(result_data, list):
            # For list results
            st.markdown("### Results Summary")
            
            # Create a more attractive display for lists
            if all(isinstance(item, dict) for item in result_data):
                # If it's a list of dictionaries, show as a table
                st.markdown(f"**Found {len(result_data)} items**")
                st.dataframe(result_data)
            else:
                # For other lists
                for idx, item in enumerate(result_data):
                    st.markdown(f"**Item {idx+1}**")
                    st.markdown(f"{item}")
        
        else:
            # For simple types
            st.markdown("### Program Output")
            st.markdown(f"{result_data}")


def main():
    app = ProgramExecutionApp()
    app.run_streamlit_app()


if __name__ == "__main__":
    main()