---
name: build
description: Plan-first, phase-gated workflow for AI agent development with Python and Google ADK. Use this for adding or modifying agents, tools, and multi-agent pipelines.
claudecode:
  argument-hint: '[agent|tool|pipeline] <description>'
  allowed-tools: Read, Grep, Glob, WebSearch, Agent, AskUserQuestion, TodoWrite, Edit, Write, Bash
  disable-model-invocation: true
---

# Build Workflow

**Request**: $ARGUMENTS

**Always start from Phase 0, even when resuming a previous session or working from a compacted summary.**

---

## Core Principles

- **Requirements first**: Clarify all ambiguities before any investigation or design.
- **Investigate before designing**: Phases 0–5 are read-only. Do NOT modify any files.
- **Approval gates**: Obtain explicit user approval after every phase before advancing.
- **Plan as TODO list**: Register the implementation plan (Phase 5) as a `TodoWrite` TODO list before implementation begins.
- **Test-first (TDD)**: Write failing tests before implementing production code. Confirm RED before GREEN.

---

## Phase Execution Protocol

**Always start from Phase 0.**

For each phase: **Execute** → **Report findings in Japanese** → Ask for confirmation via `AskUserQuestion` → **Wait for approval before advancing**.

**Phases 0–5 are read-only** (`Read / Grep / Glob / WebSearch / Agent / AskUserQuestion` only).
`Edit / Write / Bash` are strictly forbidden until Phase 6 is explicitly approved.

---

## Phase 0: Work Type Identification

**Goal**: Determine the type of work from `$ARGUMENTS`.

- `agent` — Adding a new agent or modifying how an existing agent behaves (its role, the model it uses, or which tools it can call)
- `tool` — Adding a new capability function the agent can call, or changing an existing one (files under `app/tools/`)
- `pipeline` — Connecting multiple agents together so they collaborate on a task

If the type is unclear or not specified, use `AskUserQuestion` to ask the user before proceeding.

> **⏸️ STOP — Phase 0 complete.**
> Confirm the resolved work type with the user in Japanese.
> Use `AskUserQuestion` to request explicit approval before proceeding to Phase 1.
> **Do NOT begin Phase 1 until the user explicitly approves.**

---

## Phase 1: Requirements Gathering

**Goal**: Clarify all requirements before any investigation or design. Assumptions here cause large-scale rework.

Present all questions together in one message and wait for the user's answers. Ask follow-up questions as needed. Ask questions in plain language — avoid framework-specific terms the user may not be familiar with.

### Universal questions (all types)

- **User goal**: What problem does this solve? How does the user expect to interact with it end-to-end?
- **Inputs and outputs**: What information goes in, and what should come back out?
- **Error handling**: What should happen when something goes wrong (e.g. a network call fails or times out)?
- **Scope constraints**: Are there any known limitations or out-of-scope items?

### Agent questions

- What is the agent's overall role — what kinds of requests should it handle?
- How should the agent behave when it is unsure?
- Which existing capabilities (tools) should it use? Should any be added or removed?
- Should this agent hand off work to other agents, or work independently?

### Tool questions

- What specific task should this tool perform?
- Does it need to call an external service or API? If so, which one, and how is it authenticated?
- Is this synchronous, or does it involve waiting for a network response?
- What should the return value look like on success? And on failure?
- Should this be added to an existing group of tools, or form its own group?

### Pipeline questions

- How many agents are involved, and what is each one responsible for?
- Should they run sequentially or in parallel?
- What data needs to be passed from one agent to the next?

> **⏸️ STOP — Phase 1 complete.**
> Use `AskUserQuestion` to present all questions in Japanese and collect the user's answers.
> Do NOT begin Phase 2 until all ambiguities are resolved and the user explicitly approves.

---

## Phase 2: Codebase Exploration

**Goal**: Understand the current codebase. Read-only.

Follow the **`exploration` skill** for what to read and how to research externally.

> **⏸️ STOP — Phase 2 complete.**
> Report: key files examined, existing patterns found, external research findings, and any gaps.
> Do NOT begin Phase 3 until the user explicitly approves.

---

## Phase 3: Clarifying Questions

**Goal**: Resolve any remaining ambiguities discovered during codebase exploration.

- Do any existing tools overlap in name or responsibility with what we are adding?
- Are new third-party libraries needed? (Would `pyproject.toml` need to be updated?)
- Could any existing tests break as a result of this change?
- Is there a consistent error response format already in use that we should follow?

> **⏸️ STOP — Phase 3 complete.**
> Use `AskUserQuestion` to present all open questions in Japanese and collect answers.
> Do NOT begin Phase 4 until all questions are answered and the user explicitly approves.

---

## Phase 4: Design

**Goal**: Design the full implementation — file layout, function signatures, and test plan.

Follow the **`design` skill** for conventions on function signatures, return value rules, and test plan structure.
Follow the **`tests` skill** for unit test layout, e2e eval dataset format, and mocking strategy.

> **⏸️ STOP — Phase 4 complete.**
> Present the full design (signatures, file layout, test plan) in Japanese.
> Do NOT begin Phase 5 until the user explicitly approves.

---

## Phase 5: Implementation Plan

**Goal**: Create a detailed, ordered, step-by-step plan. CRITICAL: DO NOT START IMPLEMENTATION.

Follow the **`plan-procedures` skill** for the standard step template and TODO registration procedure.

After presenting the plan, use `TodoWrite` to register all steps as a TODO list.

> **⏸️ STOP — Phase 5 complete. This is the critical gate before any code changes.**
> Present the full step-by-step implementation plan in Japanese.
> Use the `TodoWrite` tool to create a TODO list from the plan steps.
> Do NOT write, edit, or run any code until the user explicitly approves the plan.
> Using `Edit`, `Write`, or `Bash` before this approval is strictly forbidden.

---

## Phase 6: TDD Implementation

**Goal**: Implement each unit using strict TDD (🔴 RED → 🟢 GREEN → 🔵 REFACTOR).

Follow the **`implement` skill** for the TDD cycle, coding rules, and file layout.

Work one unit at a time, in the order defined in Phase 5.
**Do not move to the next unit until the current unit's tests are GREEN.**
**Mark each TODO item as completed immediately after its tests are GREEN.**

---

## Phase 7: Quality Review

**Goal**: Confirm the implementation is correct and introduces no regressions.

Follow the **`evaluation` skill** for the full automated + manual verification checklist.

---

## Phase 8: Summary

**Goal**: Document the completed work.

Follow the **`evaluation` skill** summary report format:

1. **What was built**: Overview of the changes
2. **Changed files**: Grouped by layer (tools / agent / tests)
3. **Test results**: pytest pass/fail count (unit and e2e separately)
