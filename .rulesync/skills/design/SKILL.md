---
name: design
description: Design conventions for Google ADK tool functions, agent definitions, and multi-agent pipelines
claudecode:
  user-invocable: false
---

# Design Conventions

## Goal

Produce a concrete design — file layout, function signatures, and test plan — before any code is written. Use `WebSearch` proactively to verify best practices, check for known pitfalls, and look up library APIs.

## Tool Function Signature

```python
# app/tools/<domain>.py

def <tool_name>(<arg>: <type>, ...) -> dict:
    """One-line summary.

    Args:
        <arg>: Description of the argument.

    Returns:
        On success: {"status": "success", "result": <numeric_value>}
        On failure: {"status": "error", "message": "<explanation in Japanese>"}
    """
```

For tools that call external APIs:

```python
async def <tool_name>(<arg>: <type>, ...) -> dict:
    """One-line summary.

    Args:
        <arg>: Description.

    Returns:
        On success: {"status": "success", "<key>": <value>}
        On failure: {"status": "error", "message": "<explanation in Japanese>"}
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                data = await response.json()
                return {"status": "success", ...}
        except aiohttp.ClientError as e:
            return {"status": "error", "message": str(e)}
```

## Return Value Rules

- Always return a `dict`. Never return a string, number, or None directly.
- Use `{"status": "success", ...}` for success and `{"status": "error", "message": "..."}` for failure.
- The `result` field must always be a **numeric type** (`int` or `float`), never a string like `f"{value}"`.
- Error messages should be written in Japanese so the agent can relay them naturally to users.

## Tool Set Update (`app/tools/__init__.py`)

Specify which existing named set to extend, or define a new one:

```python
from .arithmetic_operations import add, divide, factorial, multiply, power, subtract
from .apis import get_user_by_id, get_users

arithmetic_tools = {add, subtract, multiply, divide, factorial, power}
user_apis = {get_users, get_user_by_id}
```

## Agent Definition (`app/agent.py`)

```python
from google.adk.agents import LlmAgent
from .tools import arithmetic_tools

root_agent = LlmAgent(
    name="arithmetic_operations_agent",
    model="gemini-2.5-flash",
    instruction="""
        あなたは算術演算を支援する優秀なアシスタントです。
        直感で質問に答えず、できる限り利用可能なツールを鑑み
        事前にどのように応答するかを慎重に計画、冷静に答えてください。
        """.strip(),
    tools=arithmetic_tools,
)
```

For pipeline type, add `sub_agents=[sub_agent_1, sub_agent_2]`.

## Test Plan

List every test case to be written **before** implementation (TDD RED phase):

```
tests/test_<domain>.py
  class Test<ToolName>:
    test_happy_path          — returns {"status": "success", "result": <expected>}
    test_edge_case_X         — boundary or special input
    test_error_case          — invalid input or simulated failure
    test_result_is_numeric   — isinstance(result["result"], (int, float))
```

For async tools that call external APIs, specify mocking strategy:

- Use `unittest.mock.AsyncMock` or `pytest-mock` to stub `aiohttp.ClientSession`
- Test both success and `aiohttp.ClientError` failure paths
