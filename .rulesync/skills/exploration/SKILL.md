---
name: exploration
description: Codebase investigation and external research procedures used during the build workflow
claudecode:
  user-invocable: false
---

# Codebase Exploration

## Goal

Understand the existing codebase and gather external knowledge to inform the design. All steps are **read-only** — do NOT modify any files during exploration.

## Codebase Files to Read

| File | What to look for |
| ---- | ---------------- |
| `app/agent.py` | Agent name, model, instruction, and which tool sets are registered |
| `app/tools/__init__.py` | Named tool sets (`arithmetic_tools`, `user_apis`, etc.) and what's exported |
| `app/tools/*.py` | Type hint style, docstring format, return value shape, async vs sync patterns |
| `pyproject.toml` | Installed dependencies, Python version, pytest config, ruff config |
| `tests/` | How tests are structured: unit test class layout, conftest, eval datasets |

## Reference Points by Work Type

| Type | Primary reference files |
| ---- | ----------------------- |
| `tool` | `app/tools/arithmetic_operations.py` (sync), `app/tools/apis.py` (async HTTP) |
| `agent` | `app/agent.py` |
| `pipeline` | Overall structure of `app/agent.py`, any existing sub-agents |

## External Research

Actively use `WebSearch` and the `adk-docs-mcp` MCP server throughout exploration. Do not limit research to ADK documentation — also search for:

- Python best practices for the relevant pattern
- Third-party library documentation
- Known pitfalls and security considerations
- Error handling patterns
- Testing strategies

### MCP usage pattern

```
1. mcp__adk-docs-mcp__list_doc_sources  → list available docs URLs
2. mcp__adk-docs-mcp__fetch_docs        → read a specific page
3. Follow links in the content for deeper pages
```

## What to Report

After exploration, report:

1. **Key files examined** — what was found in each
2. **Existing patterns** — type hints style, return value conventions, async vs sync
3. **External research findings** — relevant library APIs, best practices, pitfalls
4. **Gaps** — missing tests, inconsistent patterns, dependencies that may need updating
