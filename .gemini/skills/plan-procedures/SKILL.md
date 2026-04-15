---
name: plan-procedures
description: >-
  How to create, present, and register a step-by-step implementation plan before
  any code is written
---
# Planning Procedures

## Goal

Produce a concrete, ordered, step-by-step plan and register it as a TODO list **before any code is written**. This is the critical gate between investigation and implementation.

## Rules

- Do NOT write, edit, or run any code during this phase.
- Using `Edit`, `Write`, or `Bash` before the user explicitly approves the plan is strictly forbidden.
- The plan must reflect the design decisions made in the Design phase.

## Standard Step Template

```
Step 1:  Confirm current state of target files (re-read to get latest version)

Step 2:  [🔴 RED] Write unit tests for the tool function(s)
         File: tests/test_<domain>.py
         Run: uv run pytest tests/test_<domain>.py -v → confirm all new tests FAIL

Step 3:  [🟢 GREEN] Implement the tool function(s) in app/tools/<domain>.py
         Run: uv run pytest tests/test_<domain>.py -v → confirm all tests PASS

Step 4:  Update app/tools/__init__.py — add the new function(s) to the named set

Step 5:  [If agent changes are needed] Update tools= in app/agent.py

Step 6:  [Pipeline type only] Implement sub-agent definitions and wiring

Step 7:  [🔴 RED e2e] Write eval dataset and test runner (without adding tool to set yet)
         Run: uv run pytest tests/ -m e2e -v → confirm e2e FAILS

Step 8:  [🟢 GREEN e2e] Add tool to arithmetic_tools (or relevant set) in __init__.py
         Run: uv run pytest tests/ -m e2e -v → confirm e2e PASSES

Step 9:  Run full test suite: uv run pytest tests/ -m "not e2e" -v → all GREEN

Step 10: Run static analysis:
         uv run ruff check app/ tests/
         uv run ruff format --check app/ tests/
         → no issues

Step 11: Manual check: uv run adk run app — verify agent behavior interactively
```

Omit steps that do not apply to the current task (e.g., skip e2e steps if no eval dataset is planned; skip Step 5 if agent.py does not need updating).

## Registering as a TODO List

After presenting the plan to the user, register every step as a TODO item using `TodoWrite`. Each step becomes one item.

Mark each item as completed **immediately** after its corresponding test(s) are GREEN — do not batch completions.

## Presenting the Plan

Present the plan in Japanese with the step list, then ask for explicit user approval via `AskUserQuestion` before proceeding to implementation.

Example approval question:
> "Does this implementation plan look good? If approved, I will proceed to Phase 6 (TDD Implementation)."
