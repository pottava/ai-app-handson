import aiohttp
import asyncio


async def get_users() -> dict:
    """
    ペットストアの全ユーザーをリストで返します

    Returns:
      ユーザー情報のリスト
    """
    timeout = aiohttp.ClientTimeout(total=5)
    users = []
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                "https://jsonplaceholder.typicode.com/users"
            ) as response:
                response.raise_for_status()  # HTTP エラーがあれば例外を発生
                users = await response.json()
        return {"status": "success", "users": users}

    except aiohttp.ClientError as e:
        return {"status": f"エラーが発生しました: {e}"}
    except asyncio.TimeoutError:
        return {"status": "エラー: リクエストがタイムアウトしました"}


async def get_user_by_id(user_id: int) -> dict:
    """
    指定された ID のペットストア ユーザー情報を取得します

    Args:
      user_id (int): 取得したいユーザーの ID

    Returns:
      ユーザー情報
    """
    if not isinstance(user_id, int):
        return {"status": "エラー: user_id は整数である必要があります"}

    timeout = aiohttp.ClientTimeout(total=5)
    user = {}
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                f"https://jsonplaceholder.typicode.com/users/{user_id}"
            ) as response:
                response.raise_for_status()
                user = await response.json()
        return {"status": "success", "user": user}

    except aiohttp.ClientError as e:
        return {"status": f"エラーが発生しました: {e}"}
    except asyncio.TimeoutError:
        return {"status": "エラー: リクエストがタイムアウトしました"}
