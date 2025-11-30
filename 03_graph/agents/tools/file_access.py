import os

def read_file(file_path: str) -> str:
    """
    Read the contents of a file and return it as a string. Use this when you want to see what's inside a file. Do not use this with directory names.

    Args:
        file_path (str): The path to the file to read.

    Returns:
        str: The contents of the file or an error message.
    """
    if not file_path:
        return ""

    if not os.path.exists(file_path):
        return f"Could not find file {file_path} in workspace"

    with open(file_path, 'r') as file:
        return file.read()

def edit_file(path: str, old_str: str, new_str: str) -> str:
    """
    Make edits to a text file.
    Replaces 'old_str' with 'new_str' in the given file. 'old_str' and 'new_str' MUST be different from each other.
    If the file specified with path doesn't exist, it will be created.

    Args:
        path (str): The path to the file to edit.
        old_str (str): Text to search for - must match exactly and must only have one match exactly
        new_str (str): Text to replace old_str with.

    Returns:
        str: A message indicating success or failure.
    """
    if not path.strip() or old_str == new_str:
        return "Edit failed: invalid input parameters."

    try:
        # Create the file if it does not exist
        if not os.path.exists(path):
            with open(path, 'w') as file:
                file.write(new_str)
            return f"Created new file {path} with content '{new_str}'"
        
        # Special case if no old string is given, append to file
        if not old_str:
            with open(path, 'a') as file:
                # ensure new string starts on a new line
                file.write("\n" + new_str)
            return f"Appended '{new_str}' to {path}."
        
        with open(path, 'r') as file:
            content = file.read()
            # Count occurrences first to ensure we have exactly one match
            count = content.count(old_str)
            if count == 0:
                return "Edit failed: old_str not found in file."
            if count > 1:
                return f"Edit failed: old_str found {count} times in file, must be unique."

        new_content = content.replace(old_str, new_str)

        with open(path, 'w') as file:
            file.write(new_content)

        return f"Replaced '{old_str}' with '{new_str}' in {path}."
    except Exception as e:
        return f"Error editing file {path}: {str(e)}"
    

def list_files(directory_path: str) -> list[str]:
    """
    List files and directories at a given path. If no path is provided, lists files and directories in the current directory.

    Args:
        directory_path (str): Optional relative path to list files from. Defaults to current directory if not provided.

    Returns:
        list[str]: A list of file names in the directory or an error message.
    """
    if not directory_path:
        directory_path = "."

    if not os.path.exists(directory_path):
        return [f"Could not find directory {directory_path}"]

    return os.listdir(directory_path)


