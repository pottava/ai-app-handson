---
name: fix
description: Fix a bug systematically with root cause analysis and regression prevention.
claudecode:
  argument-hint: '<bug description>'
  allowed-tools: Read, Grep, Glob, WebSearch, Agent, AskUserQuestion, TodoWrite, Edit, Write, Bash
  disable-model-invocation: true
---

# Bug Fix Workflow

**Bug**: $ARGUMENTS

---

## Core Principles

- **Reproduce First**: NEVER start implementation before ensuring the bug is consistently reproducible.
- **Identify Root Cause**: Determine the underlying cause to implement a permanent solution, not just a temporary fix.
- **Verify with Tests**: Validate the fix and prevent regressions through comprehensive testing.
- **Minimize Impact**: Fix only what is broken — do not touch unrelated code.
- **Plan First, Then Execute**: NEVER start implementation (Phase 6) before presenting a concrete Implementation Plan (Phase 5) and receiving explicit user approval. This is CRITICAL.

---

## Phase Execution Protocol

**Always start from Phase 1, even when resuming a previous session or working from a compacted summary.**

This is an **interactive, human-in-the-loop workflow**. For each phase: **Execute** → **Report** findings in **Japanese** → **Confirm** using your interactive confirmation capability → **Wait** for approval before advancing.

**Phases 1–5 are read-only** (`Read / Grep / Glob / WebSearch / Agent` only). `Edit / Write / Bash` are not permitted until Phase 6.

**During investigation phases (Phase 1–2)**, actively use `WebSearch` to look up:

- Official documentation and changelogs for relevant libraries/frameworks (ADK, aiohttp, pytest, ruff, etc.)
- Known bugs, open issues, and community discussions (GitHub Issues, Stack Overflow, etc.)
- Latest best practices that may apply to the root cause

Subagent delegation:

- **Code exploration & root cause identification** → launch the `analyst` subagent via the `Agent` tool (Phase 2)
- **Code review** → launch the `reviewer` subagent via the `Agent` tool (Phase 7)

---

## Phase 1: Bug Reproduction & Analysis

**Goal**: Accurately reproduce the reported bug and clarify its symptoms, conditions, and scope.

**Actions**:

1. **Review Bug Report**: Understand reproduction steps, expected vs. actual behavior, error messages, and stack traces.
2. **Attempt Reproduction**: Follow the reported steps using `uv run adk run app` (interactive) or `uv run pytest tests/ -v` (unit). If unsuccessful, request additional context (input values, environment, Vertex AI authentication status).
3. **Analyze Symptoms**: Categorize the bug type:

   | Category           | Symptoms                                                                             |
   | ------------------ | ------------------------------------------------------------------------------------ |
   | Return value       | `result` field is a string instead of numeric; missing `status` key; returns `None` |
   | Type hint          | Missing annotations, `Any` used, runtime type mismatch                              |
   | Async              | `await` on sync function; sync function performing I/O without `async def`          |
   | Exception handling | Bare `except`; wrong exception type caught; error message not in Japanese           |
   | Tool registration  | Tool function not added to the named set in `app/tools/__init__.py`                 |
   | Agent definition   | Wrong model; unclear instruction; wrong tool set passed to `tools=` in `app/agent.py` |
   | API / HTTP         | `aiohttp.ClientError` unhandled; response JSON parsing fails; authentication error  |
   | Docstring          | Missing Google-style docstring; incorrect `Args` / `Returns` description            |

4. **Collect Evidence**: Note exact error messages, stack traces, failing test cases, and input values.
5. **Identify Scope**: Which tool functions or agents are affected?

> **⏸️ STOP — Phase 1 complete.**
> Report your findings (bug symptoms, category, affected scope) to the user **in Japanese**.
> Use your interactive confirmation capability to request explicit approval before proceeding to Phase 2.
> **Do NOT begin Phase 2 until the user explicitly approves.**

---

## Phase 2: Codebase Exploration & Root Cause Identification

**Goal**: Identify the code related to the bug and pinpoint its root cause.

**Approach**: Follow the **`exploration` skill** for what to read and how to research externally. Launch the `analyst` subagent to trace the data flow from symptom back to source.

**Actions**:

1. **Trace the Data Flow**: Follow the chain from the failing output back to the source:

   ```
   User prompt
       ↓
   LlmAgent (app/agent.py) — instruction, model, tools list
       ↓
   Tool set (app/tools/__init__.py) — named set of exported functions
       ↓
   Tool function (app/tools/<domain>.py) — sync or async def
       ↓
   External API (aiohttp.ClientSession) or local computation
   ```

2. **Check Architecture Layers**:
   - **Agent**: Is the model correct (`gemini-2.5-flash`)? Is the instruction clear? Is the correct named tool set passed to `tools=`?
   - **Tool set**: Is the function exported from `__init__.py`? Is it included in the correct named set?
   - **Tool function**: Does it return `dict`? Is the `result` field a numeric type (`int`/`float`)? Are all type hints present and correct? Is `Any` absent?
   - **Exception handling**: Is a specific exception caught (`aiohttp.ClientError`, `ValueError`, `ZeroDivisionError`, etc.)? Are error messages in Japanese?
   - **Async**: Is `async def` used for functions that call external APIs? Is `aiohttp.ClientSession` used correctly with `async with`?
   - **Docstring**: Is a Google-style docstring present with correct `Args` and `Returns` sections?

3. **Check Recent Changes**:

   ```bash
   git log --since="2 weeks ago" --name-only --oneline
   git diff HEAD~1 -- app/tools/
   git diff HEAD~1 -- app/agent.py
   git diff HEAD~1 -- app/tools/__init__.py
   ```

4. **Review Existing Tests**: Check `tests/test_<domain>.py` for related tests and confirm whether they currently fail.

5. **Search the Web**: Use `WebSearch` to research the root cause hypothesis:
   - Official ADK documentation and changelogs
   - `aiohttp`, `pytest`, `ruff`, or Gemini API known issues
   - Python best practices related to the observed symptoms

6. **Identify Root Cause**: Pinpoint the fundamental cause — wrong return type, missing tool registration, unhandled exception, incorrect `async def` usage, malformed docstring, etc.

> **⏸️ STOP — Phase 2 complete.**
> Report your root cause hypothesis and the key files examined to the user **in Japanese**.
> Use your interactive confirmation capability to request explicit approval before proceeding to Phase 3.
> **Do NOT begin Phase 3 until the user explicitly approves.**

---

## Phase 3: Clarifying Questions

**Goal**: Resolve all ambiguities before designing the fix. Assumptions here will negatively impact the fix.

**Actions**:

Compile unclear points and present them to the user before proceeding:

- Does the bug reproduce in unit tests (no authentication needed) or only end-to-end via Vertex AI?
- Is this a regression? If so, which commit introduced it?
- Does the bug affect all inputs or only specific edge cases (e.g., zero, empty string, very large numbers)?
- Is the expected behavior clearly specified in the tool's docstring?

> **⏸️ STOP — Phase 3 complete.**
> Use the `AskUserQuestion` tool to present all unresolved questions **in Japanese** and collect answers interactively.
> Use your interactive confirmation capability to request explicit approval before proceeding to Phase 4.
> **Do NOT begin Phase 4 until the user has answered all questions and approved.**

---

## Phase 4: Solution Design & Test Plan

**Goal**: Design a concrete fix and a test plan to verify its correctness.

**Actions**:

1. **Design Fix**: Define the minimal code change to resolve the root cause. Follow the **`design` skill** for conventions:
   - Which file(s) need to change?
   - Does the fix affect other tool functions that share the same pattern?
   - Are type hint changes required?
   - Does `app/tools/__init__.py` or `app/agent.py` need updating?

2. **Formulate Test Plan**: Follow the **`tests` skill** for unit test layout, mocking strategy, and e2e eval format.
   - **Regression test first** (required): Write one test that currently FAILS and will PASS after the fix.
     Name it with the bug symptom — not the fix:
     ```python
     class TestDivideBug:
         def test_bug_result_is_not_string(self) -> None:
             # currently fails — will pass after fix
             result = divide(10, 3)
             assert isinstance(result["result"], float)
     ```
   - **Boundary conditions**: Apply the `tests` skill boundary checklist to the inputs involved in the bug.
   - **Regression scope**: Which existing tests might be affected by the change?

   Present the test plan as a concrete list — file name and test case names.
   Do not begin Phase 5 until the test plan is approved alongside the fix design.

> **⏸️ STOP — Phase 4 complete.**
> Present the fix design and test plan to the user **in Japanese**.
> Use your interactive confirmation capability to request explicit approval before proceeding to Phase 5.
> **Do NOT begin Phase 5 until the user explicitly approves.**

---

## Phase 5: Implementation Plan (THE PLAN)

**Goal**: Create a detailed, step-by-step plan for execution. CRITICAL: DO NOT START IMPLEMENTATION. ONLY CREATE THE PLAN.

Follow the **`plan-procedures` skill** for the standard step template and TODO registration procedure.

**Actions**:

Define detailed steps in order:

- Exact files to modify
- What change to make in each file
- Which tests to add or modify
- Dependency order if changes span multiple files

After presenting the plan to the user, use the `TodoWrite` tool to register all steps as a TODO list. Each step in the plan becomes one TODO item.

> **⏸️ STOP — Phase 5 complete. This is the critical gate before any code changes.**
> Present the full step-by-step implementation plan to the user **in Japanese**.
> Use the `TodoWrite` tool to create a TODO list from the plan steps.
> Use your interactive confirmation capability to request explicit approval before proceeding to Phase 6.
> **Do NOT write, edit, or run any code until the user explicitly approves the plan.**
> Using `Edit`, `Write`, or `Bash` before this approval is strictly forbidden.

Example plan structure:

```
Step 1: Write regression test in tests/test_<domain>.py — confirm it currently FAILS (🔴 RED)
Step 2: Fix the return value in app/tools/<domain>.py
         → hooks run automatically on Write/Edit: confirm lint, format, tests all pass (🟢 GREEN)
Step 3: Manual check: uv run adk run app — verify the agent behaves correctly end-to-end
```

---

## Phase 6: Implementation

**Goal**: Modify code and write tests according to the approved plan.

Follow the **`implement` skill** for the TDD cycle, coding rules, and file layout.

**Actions**:

1. **Write Regression Test (🔴 RED → 🟢 GREEN → 🔵 REFACTOR)**:
   - Write the regression test (and any boundary tests from the Phase 4 test plan)
   - Run `uv run pytest tests/<file>.py -v` → confirm it **FAILS** (🔴 RED).
     If it already passes: the bug is not reproduced — revise the test before continuing.
   - Apply the code fix
   - Confirm hooks pass (lint, format, unit tests run automatically on `Edit`/`Write`)
   - Run `uv run pytest tests/<file>.py -v` → confirm it **PASSES** (🟢 GREEN)
   - Refactor if needed → run again to confirm GREEN is maintained

2. **Apply Code Fix**: Make the minimal change defined in Phase 5.
3. **Update Affected Tests**: Modify any existing tests broken by the fix.

> Automated quality checks (lint, format, unit tests) run via hooks on every `Edit`/`Write`.
> Check hook output after each file save. Do not proceed to Phase 7 if hooks report failures.

**Key Guidelines**:

- Fix the root cause, not the symptom
- Do not touch unrelated code
- Follow existing patterns from the `implement` and `design` skills
- Add Japanese comments for non-obvious fixes

---

## Phase 7: Quality Review

**Goal**: Confirm the fix does not introduce new violations.

**Approach**: After automated checks pass, launch the `reviewer` subagent on modified files.

Follow the **`evaluation` skill** for the full verification checklist.

**Actions**:

1. **Verify Hook Results**: Confirm all hooks (lint, format, unit tests) passed after the last `Edit`/`Write`.

2. **Manual Verification**:
   - **Bug resolved**: Confirm the original bug no longer reproduces using steps from Phase 1
   - **Agent integration**: Run `uv run adk run app` and verify the agent handles the fixed case correctly
   - **No regressions**: Related tool functions still work correctly
   - **No `Any`**: Fix did not introduce untyped values
   - **Coding rules**: Type hints present, Google-style docstring correct, no bare `except`, `dict` returned

3. **Run e2e tests** (if applicable and Vertex AI authentication is available):

   ```bash
   uv run pytest tests/ -m e2e -v
   ```

4. **Reviewer subagent**: Pass the diff to the `reviewer` subagent. Only report issues with confidence ≥ 80.

---

## Phase 8: Summary & Documentation

**Goal**: Document the completed work.

**Actions**:

1. **Summarize Bug Fix**:
   - **What the bug was**: What was happening and in which tool/agent
   - **Root cause**: The underlying reason (e.g., `result` returned as string, missing tool registration, unhandled `ZeroDivisionError`)
   - **Fix**: What was changed (list of modified files)
   - **Tests**: Regression test added? Which file and test case name?

2. **Update Documentation**: If the bug reveals a misunderstood pattern, update the relevant skill file under `.rulesync/skills/` to prevent recurrence.

3. **Draft PR**: Output a PR title + body in a fenced Markdown block so the user can copy-paste it directly into GitHub.
