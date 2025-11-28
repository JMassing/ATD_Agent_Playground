from pydantic_ai import Agent

from agents.src.chat_loop import chat
from agents.tools.run_tests import run_tests

from dotenv import dotenv_values
config = dotenv_values(".env")
class TestRunnerAgent:
    SYSTEM_PROMPT = """You are an expert software engineer. Your task is to run unit test cases.
                    You will be provided with the path to the source code file that needs to be run.
                    Execute the tests and provide a summary of the results."""

    agent = Agent('openai:gpt-5', system_prompt=SYSTEM_PROMPT, tools=[run_tests])

# Run a chat with the agent
if __name__ == "__main__":
    chat(TestRunnerAgent.agent)