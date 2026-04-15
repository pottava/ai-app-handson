---
name: implement
description: >-
  TDD implementation cycle and coding guidelines for Google ADK tool functions
  and agents
---
# Implementation Guidelines

## TDD Cycle

Work one unit at a time. Do not move to the next unit until the current unit's tests are GREEN.

```
a. Review the test cases planned during the Design phase
b. Write the test code
c. Run: uv run pytest tests/<target_test>.py -v  →  confirm 🔴 RED
   If already GREEN: the test exercises nothing — rewrite it before continuing
d. Write the minimum implementation to pass the test
e. Run: uv run pytest tests/<target_test>.py -v  →  confirm 🟢 GREEN
f. Refactor if needed → run again to confirm GREEN is maintained
g. Mark the TODO item as completed, then move to the next unit
```

All pytest commands are run from the **project root**.

## Coding Rules

### Type hints

Annotate **all** function arguments and return values. `Any` is forbidden.

```python
def add(a: float, b: float) -> dict:
    ...

async def get_user_by_id(user_id: int) -> dict:
    ...
```

### Docstrings (Google style)

Every tool function **must** have a Google-style docstring. The ADK framework reads this and presents it to the model as the tool description.

```python
def multiply(a: float, b: float) -> dict:
    """二つの数値の積を計算します。

    Args:
        a: 被乗数。
        b: 乗数。

    Returns:
        成功時: {"status": "success", "result": float}
    """
    return {"status": "success", "result": a * b}
```

### Return values

Always return a `dict`. Never return a bare string, number, or None.

```python
# ✅ Correct
return {"status": "success", "result": a / b}
return {"status": "error", "message": "ゼロでは割り算できません"}

# ❌ Wrong — result must be numeric, not a string
return {"status": "success", "result": f"{a / b}"}
```

### Async for external I/O

Any function that calls an external API must use `async def` and `aiohttp.ClientSession`.

```python
import aiohttp

async def get_user_by_id(user_id: int) -> dict:
    """指定された ID のユーザー情報を取得します。"""
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                data = await response.json()
                return {"status": "success", "user": data}
        except aiohttp.ClientError as e:
            return {"status": "error", "message": str(e)}
```

### Exception handling

Never use a bare `except`. Always catch a specific exception type.

```python
# ✅ Correct
except aiohttp.ClientError as e:
except ValueError as e:
except ZeroDivisionError as e:

# ❌ Wrong
except:
except Exception:
```

### Comments

Write Japanese comments for complex business logic. Variable names, function names, and identifiers stay in English.

## Registering a New Tool

After unit tests are GREEN, add the tool to its named set in `app/tools/__init__.py`:

```python
from .arithmetic_operations import add, divide, factorial, multiply, power, subtract

arithmetic_tools = {add, subtract, multiply, divide, factorial, power}
```

If the agent definition in `app/agent.py` needs updating (e.g., switching tool sets), do it last — after all unit tests and the tool export are in place.

## File Layout Summary

| Change | File |
| ------ | ---- |
| New tool function | `app/tools/<domain>.py` |
| Export and group registration | `app/tools/__init__.py` |
| Agent tool set change | `app/agent.py` |
| Unit tests | `tests/test_<domain>.py` |
| e2e eval dataset | `tests/eval/<name>.test.json` |
| e2e test runner | `tests/test_agent_eval.py` |
