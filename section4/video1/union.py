from typing import Tuple, Iterable, Callable, Union

Pair = Union[Tuple[int, int], Tuple[str, str]]
Single = Union[int, str]


def add(pair: Pair) -> Single:
    return pair[0] + pair[1]


def even(a: Single) -> bool:
    if isinstance(a, str):
        return len(a) % 2 == 0
    return a % 2 == 0


def map(func: Callable[[Pair], Single], objects: Iterable[Pair]) -> Iterable[Single]:
    return [func(x) for x in objects]


def filter(
    func: Callable[[Single], bool], objects: Iterable[Single]
) -> Iterable[Single]:
    return [x for x in objects if func(x)]


if __name__ == "__main__":
    print(filter(even, map(add, [(1, 2), (2, 2), (2, 1), (5, 1)])))
    print(filter(even, map(add, [(1, 2), (2, 2), ("hello", "there"), (5, 1)])))
