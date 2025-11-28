import signal

from pydantic_ai import Agent

from src.chat_loop import chat
from tools.file_access import read_file as read_file_tool, edit_file as edit_file_tool, list_files as list_files_tool
from tools.run_tests import run_tests as run_tests_tool

SYSTEM_PROMPT = """You are a helpful AI assistant. Answer the user's questions to the best of your ability."""

agent = Agent('openai:gpt-5', system_prompt=SYSTEM_PROMPT)

# Defining tools for the agent
@agent.tool_plain(docstring_format='google', require_parameter_descriptions=True)
def read_file(file_path: str) -> str:
    """
    Read the contents of a file and return it as a string. Use this when you want to see what's inside a file. Do not use this with directory names."

    Args:
        file_path (str): The path to the file to read.

    Returns:
        str: The contents of the file or an error message.
    """
    return read_file_tool(file_path)

@agent.tool_plain(docstring_format='google', require_parameter_descriptions=True)
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
    return edit_file_tool(path, old_str, new_str)

@agent.tool_plain(docstring_format='google', require_parameter_descriptions=True)
def list_files(directory_path: str) -> list[str]:
    """
    List files and directories at a given path. If no path is provided, lists files and directories in the current directory.

    Args:
        directory_path (str): Optional relative path to list files from. Defaults to current directory if not provided.

    Returns:
        list[str]: A list of file names in the directory or an error message.
    """
    return list_files_tool(directory_path)


@agent.tool_plain(docstring_format='google', require_parameter_descriptions=True)
def run_tests(test_path, verbose=False, coverage=True) -> tuple[int, str]:
    """
    Execute test cases using pytest.
    
    Args:
        test_path (str, optional): Path to specific test file or directory. 
                                   If None, runs all tests.
        verbose (bool): Run pytest in verbose mode. Default is True.
        coverage (bool): Generate coverage report. Default is False.
    
    Returns:
        tuple: (exit_code, output) where exit_code is 0 if all tests pass, 
               non-zero otherwise, and output is the pytest stdout/stderr
    """
    return run_tests_tool(test_path=test_path, verbose=verbose, coverage=coverage)

##### Code above is only for testing purposes, remove when done #####

# Run a chat with the agent
if __name__ == "__main__":
    chat(agent)