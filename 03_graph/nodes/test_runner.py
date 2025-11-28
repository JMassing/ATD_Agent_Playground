from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext, End

from agents.test_runner_agent import TestRunnerAgent
from nodes.test_state import TestState

@dataclass
class TestRunner(BaseNode[TestState]):
    """
    A node that runs test cases for given code using an AI agent.
    """
    test_file: str

    async def run(self, ctx: GraphRunContext[TestState]) -> End[str]:
        prompt_parts = ["Run test cases for the following file."]
        prompt_parts.append(f"Test File:\n{self.test_file}")

        result = await TestRunnerAgent.agent.run("\n".join(prompt_parts))

        return End(result)