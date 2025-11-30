from dataclasses import dataclass

@dataclass
class TestState:
    code_path: str    # Path to the code file or directory to generate tests for
    output_path: str    # Path to the output file or directory where generated tests will be saved
    function_name: str = "" # Specific function name to generate tests for (optional)
