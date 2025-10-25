# Teacher Agent Project

## Overview
The Teacher Agent Project is a backend service for experimenting with AI "teacher"
personas that guide a user through a conversation. The system uses a LangGraph
workflow to orchestrate persona-specific responses, automatic conversation
summarisation, retrieval-augmented generation (RAG), and optional Brave Search
lookups. Configuration is handled through Pydantic settings so that the agent can
run locally while remaining easy to deploy with environment variables.

## Repository Layout
```
.
├── README.md                # Project documentation (this file)
└── backend/
    ├── pyproject.toml       # Python package metadata and dependency list
    ├── src/maestro/
    │   ├── application/     # Conversation workflow, RAG helpers, orchestration
    │   ├── config.py        # Centralised environment configuration
    │   ├── domain/          # Teacher personas, prompt templates, domain types
    │   └── infrastructure/  # API layer, database and external integrations
    └── tools/               # Utility scripts for working with the agent
```

### Application layer highlights
* **Conversation service (`application/conversation_service`)** – Defines the
  LangGraph state machine that powers a chat between the user and a selected
  teacher persona. Nodes handle response generation, Brave Search integration and
  conversation summarisation while edges decide when to branch based on LLM
  outputs or heuristics.
* **RAG utilities (`application/rag`)** – Provides embedding, retrieval and text
  splitting helpers used by the conversation workflow and tools.
* **Domain module (`domain`)** – Contains teacher definitions, prompt templates
  and supporting domain logic exposed through the `TeacherFactory`.
* **Infrastructure (`infrastructure`)** – Hosts integration points such as the
  MongoDB client, indexing helpers and API scaffolding.

## Getting Started
### Prerequisites
* Python 3.12+
* (Optional) Access to an Ollama instance serving the configured chat models
* (Optional) Brave Search API key for web augmentation
* (Optional) MongoDB instance if you plan to persist memories

### Installation
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   ```
2. Install the backend package and its dependencies:
   ```bash
   cd backend
   pip install -e .
   ```
   The code imports packages such as `langgraph`, `langchain_core`,
   `langchain_community`, and `pydantic-settings`. Add them to `backend/pyproject.toml`
   if they are not already declared before installing.

### Environment configuration
Configuration lives in `maestro/config.py` and is driven by environment
variables (or a `.env` file). Key settings include:

| Variable | Description |
| --- | --- |
| `BRAVE_SEARCH_API_KEY` | Optional key used by Brave Search tools. |
| `OLLAMA_MODEL_NAME` / `OLLAMA_SUMMARY_MODEL` | Default model names served by your local Ollama deployment. |
| `MONGO_URI` | Connection string for MongoDB used to persist conversations. |
| `TOTAL_MESSAGES_SUMMARY_TRIGGER` | Number of messages before the workflow attempts a summary. |
| `RAG_*` variables | Control embedding model, dimensions, top-k results, device and chunk size. |

Create a `.env` file in the repository root or export the variables in your shell
before running the application.

## Running the conversation workflow
The LangGraph workflow can be exercised directly from the command line. Ensure
`backend/src` is on your `PYTHONPATH` (for example, by running commands from the
`backend` directory or exporting `PYTHONPATH=backend/src`), then execute:

```bash
python -m maestro.application.conversation_service.workflow.graph
```

The script compiles the state graph, loads a sample teacher persona and prints
the resulting state after running a test prompt.

## Tooling and scripts
The `backend/tools` directory contains helper scripts that interact with the
agent for evaluation and memory management:

* `call_agent.py` – Invoke the agent over a prompt.
* `create_long_term_memory.py` / `delete_long_term_memory.py` – Manage stored
  conversation memory entries.
* `evaluate_agent.py` and `generate_evaluation.py` – Run evaluation workflows.

Run these scripts with `python -m backend.tools.<script_name>` after installing
the package.

## Development tips
* Keep `backend/src` importable by adding it to your IDE or setting `PYTHONPATH`.
* Add new dependencies to `backend/pyproject.toml` so they are installed with the
  package.
* Consider adding tests with `pytest` (once tests exist you can run them via
  `pytest` from the repository root or `backend` directory).
* When introducing new environment variables, document them in this README and in
  `maestro/config.py`.

## Contributing
1. Fork or branch from `work`.
2. Make your changes following the existing module structure.
3. Run any relevant scripts or tests.
4. Submit a pull request summarising your changes.

## License
This project currently does not specify a license. Add one if you plan to share
or distribute the code publicly.

