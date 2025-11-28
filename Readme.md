# AI Agent Playground – Agile Testing Days 2025

## Introduction
This repository contains the material for the **AI Agent Playground** session at **Agile Testing Days 2025**. It is a hands‑on workshop where participants learn how to:

- Build their first AI agents
- Create simple agentic workflows using **pydantic-ai** and **pydantic-graph**
- Implement a simple **MCP (Model Context Protocol) server** to expose these agents as tools (e.g., to GitHub Copilot in Visual Studio Code)

The goal of this session is to introduce the basic concepts of AI agents and give you a practical starting point so you can continue learning and exploring on your own.

- Agile Testing Days website: https://agiletestingdays.com/
- pydantic.ai: https://pydantic.ai/

---

## Prerequisites

- **Python**: Version **3.12** or higher  
  Download from: https://www.python.org/downloads/

---

## Getting Started

All commands below are meant to be run from the repository root unless noted otherwise.

### 1. Install Python

Make sure Python 3.12+ is installed and available on your PATH.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it (PowerShell on Windows):

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install requirements

```powershell
pip install -r requirements.txt
```

### 4. Set up OpenAI access

1. Go to https://platform.openai.com/ and create an account (if you don’t have one yet).
2. Navigate to https://platform.openai.com/api-keys and create a new **secret key**.
3. Add your key as an environment variable named `OPENAI_API_KEY`:

**On Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your-secret-api-key-here"
```

**On macOS/Linux (Bash):**
```bash
export OPENAI_API_KEY="your-secret-api-key-here"
```

> **Note:** This sets the variable for the current session only. For persistent configuration, add it to your shell profile (e.g., `.bashrc`, `.zshrc`) or use a `.env` file with a tool like `python-dotenv`.

```env
OPENAI_API_KEY=your-secret-api-key-here
```

---

## Workshop Flow & Exercises

Wherever possible, participants are encouraged to **build or extend the agents themselves**, using this repo as a reference and the official documentation at https://ai.pydantic.dev/ as their primary guide.

The system prompts in this workshop are intentionally kept **very simple** so that you can experiment with changing and extending them yourself (e.g., adding role definitions, style constraints, or safety rules) and directly observe how this affects the model's behavior.

### Exercise 0 – Setup

Goal: Everyone can run a simple script that calls the OpenAI API.

Steps:
- Clone this repository and open it in VS Code.
- Follow the steps in **Getting Started** (virtual env, `pip install -r requirements.txt`, `.env` with `OPENAI_API_KEY`).
- Optionally run a quick smoke test (e.g., one of the chatbot or agent scripts) to verify the key and environment.

### Exercise 1 – Your First Chatbot (`01_chatbot`)

Goal: Understand the basic request/response loop with an LLM.

Folder: `01_chatbot`

1. Change into the directory:

  ```powershell
  cd 01_chatbot
  ```

2. Run the chatbot:

  ```powershell
  python chat_bot.py
  ```

3. Try prompts such as:

  > Please create unit tests for the following function: `def sum(a, b): return a + b`

Think about these questions:
- How is the prompt constructed in code?
- What are different ways to run the chatbot e.g., sync vs. async, streamed output (see https://ai.pydantic.dev/agents/)
- Where do you configure the model and temperature? How can you configure a different model than OpenAI (see https://ai.pydantic.dev/models/overview/)
- How would you constrain the output (e.g., “only give me pytest tests”)?

### Exercise 2 – Tool-Using Agent (`02_agent`)

Goal: See how an agent can call tools to work with code and tests, not just chat.

Folder: `02_agent`

What this agent can do:
- **File system access**: Read and (where implemented) write files in the project, so the agent can inspect and modify code or other artifacts.
- **Tool documentation**:   Behind the scenes, each tool's docstring is turned into a natural-language description that the model sees, which helps it understand what the tool does and when it should be called.
- **Test runner**: Run unit tests using **pytest**, allowing the agent to execute tests and reason about failures.

Steps:
1. Change into the directory:

  ```powershell
  cd 02_agent
  ```

2. Run the agent:

  ```powershell
  python agent.py
  ```

3. Ask the agent to, for example:
  - List files in the current directory
  - Create unit tests for one of the files in the tools folder and save them to a file. 
  - Run the tests using its pytest tool.
  - Fix a failing test based on the error output.

> **Note:** Pytest will only auto-discover test files whose filenames start with `test_` (for example, `test_file_access.py`), so make sure any new test files you create follow this naming convention.

Ideas for exploration:
- Try using a different model and explore the effect
- Generate tests multiple times
- Create a file in a different programming language and generate tests. Add a new tool to run the tests in that language with a different unit testing framework.
 
Think about these questions:
- How are tools defined and registered with the agent?
- Is there an easier way to register multiple tools to the agent than with the tool decorator?
- What is the difference between tool and tool_plain?
- How are the tool docstrings used to describe behavior and guide the model to pick the right tool?
- How does the agent decide when to call which tool?
- What guardrails or limits would you add for production use?
- How can the system prompt be improved for specific tasks such as unit testing?

### Exercise 3 – Agentic Workflows with Graphs (`03_graph`)

Goal: Learn how to structure multi-step workflows using **pydantic-graph**.

Folder: `03_graph`

Ideas for exploration:
- Inspect the graph definition and identify the nodes/steps.
- Run the provided examples (see `graph.py`, `test_generator.py`, `test_runner.py`).
- Try to extend the graph with new steps (e.g., "generate tests" → "run tests" → "summarize results" → "fix broken tests").
- What are other multi agent patterns, and when are they a better choice than graphs?

### Exercise 4 – MCP Server & IDE Integration (`04_mcp`)

Goal: Expose your agents/workflows as MCP tools and call them from compatible clients (e.g., GitHub Copilot in VS Code).

Folder: `04_mcp`

Ideas for exploration:
- Walk through `mcp_server.py` and identify:
  - How tools are exposed.
  - How requests and responses are structured.
- Start the MCP server and configure your IDE/client to connect to it.
- Call one of your tools from the IDE and observe the behavior.

Think about these questions:
- What parts of the agent stack (chatbot, tools, graphs, MCP) feel most relevant to your daily work?
- What would be a first small experiment to try after the conference?
