"""算術演算ツール関数のユニットテスト"""

import math

from app.tools.arithmetic_operations import (
    add,
    divide,
    factorial,
    multiply,
    power,
    square_root,
    subtract,
)


class TestAdd:
    def test_positive_numbers(self) -> None:
        result = add(3.0, 4.0)
        assert result == {"status": "success", "result": 7.0}

    def test_negative_numbers(self) -> None:
        result = add(-1.0, -2.0)
        assert result == {"status": "success", "result": -3.0}

    def test_floats(self) -> None:
        result = add(1.5, 2.5)
        assert result == {"status": "success", "result": 4.0}

    def test_result_is_numeric(self) -> None:
        result = add(1.0, 2.0)
        assert isinstance(result["result"], (int, float))


class TestSubtract:
    def test_positive_result(self) -> None:
        result = subtract(5.0, 3.0)
        assert result == {"status": "success", "result": 2.0}

    def test_negative_result(self) -> None:
        result = subtract(3.0, 5.0)
        assert result == {"status": "success", "result": -2.0}

    def test_result_is_numeric(self) -> None:
        result = subtract(5.0, 3.0)
        assert isinstance(result["result"], (int, float))


class TestMultiply:
    def test_positive_numbers(self) -> None:
        result = multiply(4.0, 5.0)
        assert result == {"status": "success", "result": 20.0}

    def test_zero(self) -> None:
        result = multiply(0.0, 5.0)
        assert result == {"status": "success", "result": 0.0}

    def test_result_is_numeric(self) -> None:
        result = multiply(4.0, 5.0)
        assert isinstance(result["result"], (int, float))


class TestDivide:
    def test_normal_division(self) -> None:
        result = divide(10.0, 2.0)
        assert result == {"status": "success", "result": 5.0}

    def test_zero_numerator(self) -> None:
        result = divide(0.0, 5.0)
        assert result == {"status": "success", "result": 0.0}

    def test_zero_divisor_returns_error(self) -> None:
        result = divide(5.0, 0.0)
        assert result["status"] == "error"
        assert "message" in result

    def test_zero_divisor_error_message(self) -> None:
        result = divide(5.0, 0.0)
        assert "ゼロ" in result["message"]

    def test_result_is_numeric(self) -> None:
        result = divide(10.0, 4.0)
        assert isinstance(result["result"], (int, float))


class TestFactorial:
    def test_positive_integer(self) -> None:
        result = factorial(5)
        assert result == {"status": "success", "result": 120}

    def test_zero(self) -> None:
        result = factorial(0)
        assert result == {"status": "success", "result": 1}

    def test_result_is_numeric(self) -> None:
        result = factorial(5)
        assert isinstance(result["result"], (int, float))


class TestSquareRoot:
    def test_perfect_square(self) -> None:
        result = square_root(4.0)
        assert result == {"status": "success", "result": 2.0}

    def test_zero(self) -> None:
        result = square_root(0.0)
        assert result == {"status": "success", "result": 0.0}

    def test_non_perfect_square(self) -> None:
        result = square_root(2.0)
        assert result["status"] == "success"
        assert math.isclose(result["result"], math.sqrt(2.0))

    def test_negative_returns_error(self) -> None:
        result = square_root(-1.0)
        assert result["status"] == "error"
        assert "message" in result

    def test_result_is_numeric(self) -> None:
        result = square_root(4.0)
        assert isinstance(result["result"], (int, float))


class TestPower:
    def test_positive_exponent(self) -> None:
        result = power(2.0, 3.0)
        assert result == {"status": "success", "result": 8.0}

    def test_zero_exponent(self) -> None:
        result = power(5.0, 0.0)
        assert result == {"status": "success", "result": 1.0}

    def test_fractional_exponent(self) -> None:
        result = power(4.0, 0.5)
        assert result == {"status": "success", "result": 2.0}

    def test_negative_exponent(self) -> None:
        result = power(2.0, -1.0)
        assert result == {"status": "success", "result": 0.5}

    def test_result_is_numeric(self) -> None:
        result = power(2.0, 3.0)
        assert isinstance(result["result"], (int, float))
