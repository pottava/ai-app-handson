---
name: evaluation
description: Quality review checklist to run after implementation — automated tests, lint, format, and manual agent verification
claudecode:
  user-invocable: false
---

# Quality Review

## Goal

Confirm the implementation is complete, correct, and does not introduce regressions before reporting the work as done.

## Step 1: Verify Hook Results

Lint, format, and unit tests run **automatically** via the `PostToolUse` hook on every `Edit`/`Write`.

Check the hook output after the last file save and confirm all three passed:

| Check | Command (for manual re-run if needed) |
| ----- | ------------------------------------- |
| Lint | `uv run ruff check app/ tests/` |
| Format | `uv run ruff format --check app/ tests/` |
| Unit tests | `uv run pytest tests/ -m "not e2e" -v` |

If any hook reported a failure:

- **ruff check failure**: run `uv run ruff check --fix app/ tests/` to auto-fix safe issues; handle remaining issues manually.
- **ruff format failure**: run `uv run ruff format app/ tests/` to apply formatting, then re-check.
- **pytest failure**: diagnose the failing test, fix the implementation, and save the file again to trigger the hook.

Do not proceed to Step 2 until all hook checks pass.

## Step 2: e2e Evaluation (when applicable)

If an e2e eval dataset exists for the changed tool(s):

```bash
uv run pytest tests/ -m e2e -v
```

Requires valid Vertex AI authentication. In local environments, use Application Default Credentials obtained via `gcloud auth application-default login`. In cloud environments, use a service account with the appropriate permissions. API keys are not used. This step is skippable during development, but must be run before declaring completion.

## Step 3: Manual Verification Checklist

- [ ] **Happy path**: tool returns `{"status": "success", "result": <expected_numeric>}`
- [ ] **Error case**: failures return `{"status": "error", "message": "..."}` with Japanese message
- [ ] **Type correctness**: `result` field is `int` or `float`, not a string
- [ ] **Agent integration**: run `uv run adk run app` from the project root and verify the agent calls the new tool correctly in a real conversation
- [ ] **No regressions**: existing tool behaviors are unchanged

## Step 4: Summary Report

Report the following after all checks pass:

1. **What was built**: overview of the changes (new tool, bug fix, agent update, etc.)
2. **Changed files**: grouped by layer
   - `app/tools/<domain>.py`
   - `app/tools/__init__.py`
   - `app/agent.py` (if changed)
   - `tests/test_<domain>.py`
   - `tests/eval/*.test.json` (if added)
3. **Test results**: pytest pass/fail count (unit and e2e separately)
