from typing import Tuple, Iterable, Callable

Pair = Tuple[int, int]


def add(pair: Pair) -> int:
    return pair[0] + pair[1]


def even(a: int) -> bool:
    ret: int = a % 2
    return ret == 0


def map(func: Callable[[Pair], int], objects: Iterable[Pair]) -> Iterable[int]:
    return [func(x) for x in objects]


def filter(func: Callable[[int], bool], objects: Iterable[int]) -> Iterable[int]:
    return [x for x in objects if func(x)]


if __name__ == "__main__":
    print(filter(even, map(add, [(1, 2), (2, 2), (2, 1), (5, 1)])))
    print(filter(even, map(add, [(1, 2), (2, 2), ("hello", "there"), (5, 1)])))
