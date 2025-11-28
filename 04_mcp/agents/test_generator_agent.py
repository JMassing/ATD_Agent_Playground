from pydantic_ai import Agent

from agents.src.chat_loop import chat
from agents.tools.file_access import read_file, edit_file, list_files

from dotenv import dotenv_values
config = dotenv_values(".env")
class TestGeneratorAgent:
    SYSTEM_PROMPT = """You are an expert software engineer. Your task is to create unit test cases.
                    You will be provided with the path to the source code file that needs to be tested.
                    Write comprehensive unit tests for the provided source code using the pytest framework.
                    Ensure that your tests cover various scenarios, including edge cases."""

    agent = Agent('openai:gpt-5', system_prompt=SYSTEM_PROMPT, tools=[read_file, edit_file, list_files])

# Run a chat with the agent
if __name__ == "__main__":
    chat(TestGeneratorAgent.agent)