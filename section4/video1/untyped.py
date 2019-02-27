def add(pair):
    return pair[0] + pair[1]


def even(a):
    return a % 2 == 0


def map(func, objects):
    return [func(x) for x in objects]


def filter(func, objects):
    return [x for x in objects if func(x)]


if __name__ == "__main__":
    print(filter(even, map(add, [(1, 2), (2, 2), (2, 1), (5, 1)])))
    print(filter(even, map(add, [(1, 2), (2, 2), ("hello", "there"), (5, 1)])))
