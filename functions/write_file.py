import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the {content} to the specified {file_path}. If the specified folder structure doesn't exists it will create it for you. If the file doesn't exists will create a new file for you.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory (default is the working directory itself), will automatically create the specified folder structure if dones't exists.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written to the specified file (Will create a new file if it doesn't exists)",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):


    try:
        
        abs_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))
        valid_target_file = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory
         
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        
        with open(target_file, mode='w') as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: An exception has occurred: {e}"