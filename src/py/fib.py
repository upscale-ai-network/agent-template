"""Fibonacci sample — pytest wiring smoke."""


def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fib_sequence(count: int) -> list[int]:
    if count < 0:
        raise ValueError("count must be non-negative")
    return [fib(i) for i in range(count)]


def main() -> None:
    print(" ".join(str(x) for x in fib_sequence(10)))


if __name__ == "__main__":
    main()
