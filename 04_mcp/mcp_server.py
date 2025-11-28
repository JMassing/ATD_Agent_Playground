from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Optional

from fastmcp import FastMCP

from agents.test_generator_agent import TestGeneratorAgent
from agents.test_runner_agent import TestRunnerAgent

mcp = FastMCP("ATD Test Automation MCP Server")

def _serialize_result(result: Any) -> Any:
    """Normalize agent outputs so MCP clients always receive JSON-serializable data."""
    if result is None:
        return None

    model_dump = getattr(result, "model_dump", None)
    if callable(model_dump):
        try:
            return model_dump()
        except TypeError:
            pass

    if is_dataclass(result):
        return asdict(result)

    if isinstance(result, (str, int, float, bool)):
        return result

    if isinstance(result, (list, dict)):
        return result

    attrs = getattr(result, "__dict__", None)
    if isinstance(attrs, dict):
        return attrs

    return str(result)


@mcp.tool(name="test_generator")
async def test_generator(
    code_path: str,
    output_path: str,
    function_name: Optional[str] = None,
    extra_instructions: Optional[str] = None,
) -> Any:
    """Generate or extend tests for the target code file using the TestGenerator agent."""
    prompt_parts: list[str] = []

    if function_name:
        prompt_parts.append(
            f"Generate test cases specifically for the function: {function_name} in the file {code_path}."
        )
    else:
        prompt_parts.append(f"Generate test cases for all functions in the file {code_path}.")

    prompt_parts.append(f"Save the generated tests to: {output_path}")

    if extra_instructions:
        prompt_parts.append(extra_instructions)

    prompt = "\n".join(prompt_parts)
    result = await TestGeneratorAgent.agent.run(prompt)
    serialized = _serialize_result(result)

    if serialized is None:
        return {
            "status": "completed",
            "details": "Test generator agent finished without returning additional content.",
        }

    return serialized


@mcp.tool(name="test_runner")
async def test_runner(
    test_file: str,
    verbose: bool = False,
    coverage: bool = True,
    extra_instructions: Optional[str] = None,
) -> Any:
    """Execute tests through the TestRunner agent and return structured results."""
    prompt_parts = ["Run test cases for the following file.", f"Test File:\n{test_file}"]

    if verbose:
        prompt_parts.append("Enable verbose output.")

    if not coverage:
        prompt_parts.append("Skip coverage collection.")

    if extra_instructions:
        prompt_parts.append(extra_instructions)

    prompt = "\n".join(prompt_parts)
    result = await TestRunnerAgent.agent.run(prompt)
    serialized = _serialize_result(result)

    if serialized is None:
        return {
            "status": "completed",
            "details": "Test runner agent finished without returning additional content.",
        }

    return serialized


if __name__ == "__main__":
    mcp.run()
