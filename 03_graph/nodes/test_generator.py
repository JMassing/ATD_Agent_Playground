from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext

from agents.test_generator_agent import TestGeneratorAgent
from nodes.test_state import TestState
from nodes.test_runner import TestRunner

@dataclass
class TestGenerator(BaseNode[TestState]):
    """
    A node that generates test cases for given code using an AI agent.
    """

    async def run(self, ctx: GraphRunContext[TestState]) -> TestRunner:
        input_state = ctx.state

        prompt_parts = []

        if input_state.function_name:
            prompt_parts.append(
                f"Generate test cases specifically for the function: {input_state.function_name}"
                f" in the file {input_state.code_path}."
            )
        else:
            prompt_parts.append(f"Generate test cases for all functions in the file {input_state.code_path}.")

        prompt_parts.append(f"Save the generated tests to: {input_state.output_path}")
        _ = await TestGeneratorAgent.agent.run("\n".join(prompt_parts))

        return TestRunner(input_state.output_path)
    