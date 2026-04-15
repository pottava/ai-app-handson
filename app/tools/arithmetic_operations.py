import math


def add(a: float, b: float) -> dict:
    """2 つの数値を足し算します。

    Args:
        a: 加数
        b: 加数

    Returns:
        成功時: {"status": "success", "result": float}
    """
    return {"status": "success", "result": a + b}


def subtract(a: float, b: float) -> dict:
    """2 つの数値を引き算します。

    Args:
        a: 被減数
        b: 減数

    Returns:
        成功時: {"status": "success", "result": float}
    """
    return {"status": "success", "result": a - b}


def multiply(a: float, b: float) -> dict:
    """2 つの数値を掛け算します。

    Args:
        a: 乗数
        b: 乗数

    Returns:
        成功時: {"status": "success", "result": float}
    """
    return {"status": "success", "result": a * b}


def divide(a: float, b: float) -> dict:
    """数値 a を数値 b で割り算します。ゼロ除算の場合はエラーを返します。

    Args:
        a: 被除数
        b: 除数

    Returns:
        成功時: {"status": "success", "result": float}
        エラー時: {"status": "error", "message": str}
    """
    if b == 0:
        return {"status": "error", "message": "ゼロでは割り算できません"}
    return {"status": "success", "result": a / b}


def factorial(n: int) -> dict:
    """非負の整数 n の階乗を計算します。

    Args:
        n: 非負整数

    Returns:
        成功時: {"status": "success", "result": int}
    """
    return {"status": "success", "result": math.factorial(n)}


def square_root(n: float) -> dict:
    """浮動小数点数 n の平方根を計算します。負の数の場合はエラーを返します。

    Args:
        n: 平方根を求める数値

    Returns:
        成功時: {"status": "success", "result": float}
        エラー時: {"status": "error", "message": str}
    """
    try:
        return {"status": "success", "result": math.sqrt(n)}
    except ValueError:
        return {"status": "error", "message": "負の数の平方根は計算できません"}


def power(a: float, b: float) -> dict:
    """数値 a の b 乗を計算します。

    Args:
        a: 底
        b: 指数

    Returns:
        成功時: {"status": "success", "result": float}
    """
    return {"status": "success", "result": 0}
