import signal

from pydantic_ai import Agent

from src.chat_loop import chat

SYSTEM_PROMPT = """You are a helpful AI assistant. Answer the user's questions to the best of your ability."""

agent = Agent('openai:gpt-5', system_prompt=SYSTEM_PROMPT)

# Run a chat with the agent
if __name__ == "__main__":
    chat(agent)