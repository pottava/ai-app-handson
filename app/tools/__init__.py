from .apis import get_user_by_id, get_users
from .arithmetic_operations import (
    add,
    divide,
    factorial,
    multiply,
    subtract,
)

arithmetic_tools = {
    add,
    subtract,
    multiply,
    divide,
    factorial,
}

user_apis = {
    get_users,
    get_user_by_id,
}
