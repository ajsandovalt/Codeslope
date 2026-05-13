import os
from utilities.config import *
from google.genai import types

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Opens the specified file and returns it's content as plain text, relative to the working directory. Only file are allowed directories will return an error.",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to open and get plain text, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    

    try:

        abs_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))
        valid_target_file = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory
         
        if not valid_target_file:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_file) as file:
            file_content = file.read(MAX_CHARS)
            if file.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
        return file_content

    except Exception as e:
         return f'Error: The following exception was encountered: {e}'    
        
