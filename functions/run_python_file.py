import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified file at {file_path} with optional arguments ({args}) using a python command",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to run, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="(OPTIONAL) Arguments to be passed to the command (e.g. python main.py {args})",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):


    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))
        valid_target_file = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory
         
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory' 
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        
        if args:
            command.extend(args)
            
        execution_results = subprocess.run(command, cwd=abs_working_directory, capture_output=True, text=True, timeout=30)
        
        exit_code = execution_results.returncode
        stdout = execution_results.stdout
        stderr = execution_results.stderr
        
        final_result = [f"Process exited with code {exit_code}"]
        
        if not stdout and not stderr:
            final_result.append("No output produced")
        
        final_result.append(f"STDOUT: {stdout}")
        final_result.append(f"STDERR: {stderr}")
        
        return "\n".join(final_result)

     
    except Exception as e:
        return f"Error: executing Python file: {e}"
