import os

def get_files_info(working_directory, directory="."):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_directory, directory))
        valid_target_dir = os.path.commonpath([abs_working_directory, target_dir]) == abs_working_directory
         
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
     
        if not os.path.isdir(target_dir):
            return f'Error: Cannot list "{directory}" as is not a directory'
     
        dir_content = os.listdir(path=target_dir)
        
        files_info = []
        for file in dir_content:
            abs_file = os.path.join(target_dir, file)
            files_info.append(f"- {abs_file}: file_size={os.path.getsize(abs_file)}, is_dir={os.path.isdir(abs_file)}")
        
        return "\n".join(files_info)
            
        
    except Exception as e:
       return f"Error: An exception has occurred: {e}"