---
root: true
targets: ['*']
description: 'Project overview and general development guidelines'
globs: ['**/*']
---

# Project Overview

A Python-based AI agent project built with Google ADK (Agent Development Kit).
The agent is defined in `app/agent.py` and all capability functions (tools) live under `app/tools/`.

## Tech Stack

| Component         | Details                                   |
| ----------------- | ----------------------------------------- |
| Language          | Python 3.13+                              |
| Agent framework   | Google ADK (`google-adk`)                 |
| Model             | Gemini 2.5 Flash (`gemini-2.5-flash`)     |
| Async HTTP        | `aiohttp`                                 |
| Package manager   | `uv` / `pyproject.toml`                   |
| Testing           | `pytest`, `pytest-asyncio`                |
| e2e Evaluation    | `google-adk[eval]` / `AgentEvaluator`     |
| Type checking     | `mypy` or `pyright`                       |
| Lint / Format     | `ruff`                                    |

## Directory Structure

```
<project-root>/
├── pyproject.toml             # uv project config, pytest config, ruff config
├── uv.lock                    # dependency lockfile
├── app/
│   ├── __init__.py            # from . import agent as agent
│   ├── agent.py               # Root agent definition
│   └── tools/
│       ├── __init__.py        # Exports tool functions and named tool sets
│       ├── <domain>.py        # Tool implementations, one file per domain
│       └── ...
└── tests/
    ├── conftest.py            # sys.path setup for app module discovery
    ├── test_<domain>.py       # Unit tests per tool domain
    ├── test_agent_eval.py     # e2e tests via ADK AgentEvaluator
    └── eval/
        ├── <name>.test.json   # ADK eval dataset
        └── test_config.json   # Evaluation criteria
```

## Dependency Management

All project dependencies are declared in `pyproject.toml` at the project root.
Production dependencies go in `[project].dependencies`; testing tools go in
`[dependency-groups].dev`.

```toml
# pyproject.toml

[project]
dependencies = [
    "google-adk[eval]>=1.30.0",
    "aiohttp>=3.13.5",
    ...
]

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "ruff>=0.8.0",
]
```

### Install / sync dependencies

```bash
# From the project root
uv sync --group dev

# Add a new runtime dependency
uv add <package>

# Add a new dev-only dependency
uv add --group dev <package>
```

## Development Commands

All commands are run from the **project root**.

| Task                        | Command                                                      |
| --------------------------- | ------------------------------------------------------------ |
| Unit tests (fast, no API)   | `uv run pytest tests/ -m "not e2e" -v`                      |
| e2e tests (needs Vertex AI auth) | `uv run pytest tests/ -m e2e -v`                       |
| All tests                   | `uv run pytest tests/ -v`                                   |
| Lint check                  | `uv run ruff check app/ tests/`                             |
| Lint auto-fix               | `uv run ruff check --fix app/ tests/`                       |
| Format check                | `uv run ruff format --check app/ tests/`                    |
| Format auto-apply           | `uv run ruff format app/ tests/`                            |
| Run agent (CLI)             | `uv run adk run app`                                        |
| Run agent (Web UI)          | `uv run adk web`                                            |

## Critical Rules

- **IMPORTANT: Respond in Japanese** — ALL responses to the user MUST be in Japanese. Code, identifiers, and commit messages stay in English.
- **Type hints required** — All function arguments and return values must be annotated. `Any` is forbidden.
- **Tool functions must return `dict`** — The agent framework serializes tool return values; always return a `dict`.
- **`result` field is always numeric** — Return `float`/`int`, never `f"{value}"` strings.
- **No bare `except`** — Always catch a specific exception: `except SomeError as e:`.
- **Async for external I/O** — Functions that call external APIs must use `async def` and `aiohttp`.
- **Docstrings required** — Every tool function must have a Google-style docstring; the framework uses it as the tool description shown to the model.
- **Agent definition lives in `app/agent.py` only** — Do not instantiate agents elsewhere.
- **Tool sets managed in `app/tools/__init__.py`** — Export named sets (e.g. `arithmetic_tools`, `user_apis`).

## Available MCP Servers

| Server            | Use for                                                    |
| ----------------- | ---------------------------------------------------------- |
| `adk-docs-mcp`    | ADK documentation: agents, tools, evaluation, deployment   |

Usage pattern:
1. `mcp__adk-docs-mcp__list_doc_sources` → get documentation URLs
2. `mcp__adk-docs-mcp__fetch_docs` → read specific page

## Workflow

- **Plan first**: Present an implementation plan and wait for user approval before making any changes.
- **Test-first (TDD)**: Write failing tests before implementing production code.
- **Verify**: After implementation, run `uv run pytest tests/ -m "not e2e" -v && uv run ruff check app/ tests/ && uv run ruff format --check app/ tests/`.
- **Manual check**: Start the agent with `uv run adk run app` (CLI) or `uv run adk web` (Web UI) and verify behavior interactively.

## Multi-Phase Workflow

All significant tasks use the `/build` command, which defines phase gates and requires explicit user approval at each step. Do not skip phases or begin implementation without an approved plan.

## Language & Communication

- **Responses**: All responses to the user MUST be in **Japanese**. This is VERY IMPORTANT.
- **Code comments**: Write in Japanese for complex business logic. Variable names, function names, and commit messages stay in English.
- **Human-in-the-loop**: When asking for permission or clarification, use clear and polite Japanese.
