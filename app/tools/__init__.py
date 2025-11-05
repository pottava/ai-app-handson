from .arithmetic_operations import (
    add,
    divide,
    multiply,
    subtract,
    factorial,
)
from .apis import get_users, get_user_by_id


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
