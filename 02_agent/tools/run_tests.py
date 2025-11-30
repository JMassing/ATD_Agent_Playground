import subprocess
import sys

def run_tests(test_path=None, verbose=True, coverage=False):
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
    cmd = [sys.executable, "-m", "pytest"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=.", "--cov-report=html", "--cov-report=term"])
    
    if test_path:
        cmd.append(test_path)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr
    return result.returncode, output


if __name__ == "__main__":
    exit_code, output = run_tests()
    print(output)
    sys.exit(exit_code)