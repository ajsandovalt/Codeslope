from google.genai import types
from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python_file import *

AVAILABLE_FUNCTIONS = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_files_content, schema_write_file, schema_run_python_file]
)

def call_function(function_call, verbose=False):
    function_name = function_call.name or ""
    function_args = dict(function_call.args) if function_call.args else {}
    function_args["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    function_map = {
        "get_files_info" : get_files_info,
        "get_file_content" : get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }
    
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
            )
    
    call_result = function_map[function_name](**function_args)
    
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": call_result},
        )
    ],
)
    
    pass