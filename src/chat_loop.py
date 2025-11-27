import signal

from pydantic_ai import Agent

run_conversation = True

def stop_conversation(signum, frame):
    global run_conversation
    print("\nStopping the conversation...")
    run_conversation = False

def sync_chat_loop(agent: Agent):
    global run_conversation
    signal.signal(signal.SIGINT, stop_conversation)
    signal.signal(signal.SIGTERM, stop_conversation)

    print("Chat with OpenAI (use 'ctrl+c' to exit)")

    result = None
    while run_conversation:
        try:
            print("\033[92mUser:")
            prompt = input()

            # Skip empty prompt
            if not prompt.strip():
                continue

            if prompt.lower() in ["exit", "quit", "q"]:
                run_conversation = False
                break

            result = agent.run_sync(user_prompt=prompt, 
                                    message_history=result.all_messages() if result else None)

            print(f"\033[94mOpenAI:")
            print(f"{result.output}")
        except (KeyboardInterrupt, EOFError):
            break

    print("Conversation ended, goodbye")
