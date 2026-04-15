---
name: tests
description: Testing strategy covering unit tests, e2e evaluation with ADK AgentEvaluator, and static analysis
claudecode:
  user-invocable: false
---

# Testing Strategy

## Overview

Three layers of verification are used in this project:

| Layer | Tool | Speed | Requires API key |
| ----- | ---- | ----- | ---------------- |
| Unit | `pytest` | Fast | No |
| e2e | `pytest` + `AgentEvaluator` | Slow | Yes |
| Static analysis | `ruff` | Fast | No |

All commands are run from the **project root**.

---

## Unit Tests

### File layout

```
tests/
├── conftest.py              # sys.path setup — adds project root so `app` is importable
├── test_<domain>.py         # One file per tool domain
└── ...
```

### `conftest.py` (required)

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### Test class structure

```python
class Test<ToolName>:
    def test_happy_path(self) -> None:
        result = tool_function(...)
        assert result == {"status": "success", "result": <expected>}

    def test_edge_case(self) -> None:
        result = tool_function(...)
        assert result == {"status": "success", "result": <expected>}

    def test_error_case(self) -> None:
        result = tool_function_with_invalid_input(...)
        assert result["status"] == "error"
        assert "message" in result

    def test_result_is_numeric(self) -> None:
        result = tool_function(...)
        assert isinstance(result["result"], (int, float))
```

### Run command

```bash
# From the project root
uv run pytest tests/ -m "not e2e" -v
```

### Mocking async tools

Use `unittest.mock.AsyncMock` or `pytest-mock` to stub `aiohttp.ClientSession`:

```python
from unittest.mock import AsyncMock, patch

async def test_api_call_success() -> None:
    mock_response = AsyncMock()
    mock_response.json.return_value = {"id": 1, "name": "Alice"}
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=False)

    with patch("aiohttp.ClientSession.get", return_value=mock_response):
        result = await get_user_by_id(1)
    assert result["status"] == "success"
```

---

## e2e Tests with ADK AgentEvaluator

### Goal

Verify that the full agent (model + tools) produces correct responses to natural-language user inputs.

### File layout

```
tests/
├── test_agent_eval.py           # e2e test runner
└── eval/
    ├── <name>.test.json         # ADK eval dataset
    └── test_config.json         # Evaluation criteria (auto-discovered)
```

### Eval dataset format (`*.test.json`)

```json
[
  {
    "query": "3 と 4 を足してください",
    "expected_tool_use": [],
    "reference": "7"
  },
  {
    "query": "2 の 3 乗を計算してください",
    "expected_tool_use": [],
    "reference": "8"
  }
]
```

- `query`: natural-language user message
- `reference`: expected answer the agent's response should contain
- `expected_tool_use`: leave empty `[]` — use `response_match_score` instead of trajectory matching (avoids fragile argument-type mismatches like `2` vs `2.0`)

### Evaluation criteria (`test_config.json`)

```json
{"criteria": {"response_match_score": 0.3}}
```

- `response_match_score`: ROUGE-1 overlap between actual response and `reference`. Threshold `0.3` is lenient enough for full Japanese sentences but strict enough to detect wrong or missing answers.
- `test_config.json` is **auto-discovered** when placed in the same directory as the `.test.json` file. Do NOT pass `config_file_path` to `AgentEvaluator.evaluate()`.

### e2e test runner

```python
# tests/test_agent_eval.py
from pathlib import Path
import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

EVAL_DIR = Path(__file__).parent / "eval"

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_arithmetic_agent_eval() -> None:
    await AgentEvaluator.evaluate(
        agent_module="app",
        eval_dataset_file_path_or_dir=str(EVAL_DIR / "arithmetic_eval.test.json"),
    )
```

### Run command

```bash
# From the project root
uv run pytest tests/ -m e2e -v
```

Requires valid Vertex AI authentication. In local environments, use Application Default Credentials obtained via `gcloud auth application-default login`. In cloud environments, use a service account with the appropriate permissions. API keys are not used.

### TDD RED/GREEN for e2e

To achieve a valid RED state at the e2e level:

1. Implement the tool function in `app/tools/<domain>.py` (unit tests GREEN)
2. Write the e2e test while the tool is **not yet** added to the tool set in `app/tools/__init__.py`
3. Run e2e → confirm RED (agent can't call the tool)
4. Add the tool to the named set in `__init__.py`
5. Run e2e → confirm GREEN

---

## Static Analysis

### Lint (`ruff check`)

```bash
# From the project root
uv run ruff check app/ tests/
uv run ruff check --fix app/ tests/   # auto-fix safe issues
```

Selected rules (configured in `pyproject.toml`):

| Rule set | What it checks |
| -------- | -------------- |
| `E` | PEP 8 style errors |
| `F` | Pyflakes (unused imports, undefined names) |
| `I` | Import ordering |

Common errors to watch for:
- `F401`: unused import — fix by removing or aliasing (`from . import agent as agent`)
- `I001`: import order — fix with `--fix`

### Format (`ruff format`)

```bash
# Check only
uv run ruff format --check app/ tests/

# Apply
uv run ruff format app/ tests/
```

### Required dependencies

These must be in `[dependency-groups].dev` in `pyproject.toml`:

```toml
[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "ruff>=0.8.0",
]
```

For e2e evaluation, `google-adk[eval]` (not just `google-adk`) must be in `[project].dependencies` to include `pandas` and the `AgentEvaluator`.
