import pytest
from py_simple_package.src.py_simple import is_perfect_square as public_is_perfect_square

from py_simple_package.src.py_simple.easy_math import (
    divisors,
    factorial,
    fibonacci,
    get_least_common_multiple,
    is_perfect_square,
    prime_factorization,
    sum_of_digits,
)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (4, 6, 12),
        (3, 7, 21),
        (12, 18, 36),
        (6, 8, 24),
        (0, 5, 0),
        (5, 0, 0),
        (21, 6, 42),
        (-4, -6, 12),
        (-4, 6, 12),
    ],
)
def test_get_least_common_multiple(a, b, expected):
    assert get_least_common_multiple(a, b) == expected


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 1),
        (1, 1),
        (5, 120),
        (10, 3628800),
    ],
)
def test_factorial(n, expected):
    assert factorial(n) == expected


@pytest.mark.parametrize("n", [-1, -5, 2.5])
def test_factorial_rejects_invalid_input(n):
    with pytest.raises(ValueError):
        factorial(n)


@pytest.mark.parametrize(
    "count, expected",
    [
        (1, [0]),
        (2, [0, 1]),
        (5, [0, 1, 1, 2, 3]),
        (10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]),
    ],
)
def test_fibonacci(count, expected):
    assert fibonacci(count) == expected


@pytest.mark.parametrize("count", [0, -3, 1.5])
def test_fibonacci_rejects_invalid_count(count):
    with pytest.raises(ValueError):
        fibonacci(count)


@pytest.mark.parametrize(
    "n, expected",
    [
        (1, []),
        (2, [2]),
        (7, [7]),
        (12, [2, 2, 3]),
        (100, [2, 2, 5, 5]),
        (360, [2, 2, 2, 3, 3, 5]),
    ],
)
def test_prime_factorization(n, expected):
    assert prime_factorization(n) == expected


@pytest.mark.parametrize("n", [0, -1])
def test_prime_factorization_rejects_less_than_one(n):
    with pytest.raises(ValueError):
        prime_factorization(n)


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 0),
        (5, 5),
        (1234, 10),
        (100, 1),
        (-123, 6),
    ],
)
def test_sum_of_digits(n, expected):
    assert sum_of_digits(n) == expected


@pytest.mark.parametrize("n", [1.5, "12"])
def test_sum_of_digits_rejects_non_integer(n):
    with pytest.raises(ValueError):
        sum_of_digits(n)


@pytest.mark.parametrize(
    "n, expected",
    [
        (1, [1]),
        (7, [1, 7]),
        (12, [1, 2, 3, 4, 6, 12]),
        (16, [1, 2, 4, 8, 16]),
        (25, [1, 5, 25]),
    ],
)
def test_divisors(n, expected):
    assert divisors(n) == expected


@pytest.mark.parametrize("n", [0, -2])
def test_divisors_rejects_less_than_one(n):
    with pytest.raises(ValueError):
        divisors(n)


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, True),
        (1, True),
        (4, True),
        (49, True),
        (50, False),
        (10**12, True),
        (10**12 - 1, False),
    ],
)
def test_is_perfect_square(n, expected):
    assert is_perfect_square(n) is expected


def test_is_perfect_square_is_available_from_public_api():
    assert public_is_perfect_square is is_perfect_square


@pytest.mark.parametrize("n", [-1, -25, 4.0, "9"])
def test_is_perfect_square_rejects_invalid_input(n):
    with pytest.raises(ValueError):
        is_perfect_square(n)
