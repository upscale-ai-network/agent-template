import pytest

from fib import fib, fib_sequence


def test_fib_base_values():
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(10) == 55


def test_fib_sequence_and_negative():
    assert fib_sequence(6) == [0, 1, 1, 2, 3, 5]
    with pytest.raises(ValueError):
        fib(-1)
