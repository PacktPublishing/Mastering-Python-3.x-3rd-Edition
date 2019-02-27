def add(pair):
    return pair[0] + pair[1]


def even(a):
    return a % 2 == 0


def map(func, objects):
    return [func(x) for x in objects]


def filter(func, objects):
    return [x for x in objects if func(x)]
