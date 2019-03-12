class CacheIncluded:
    def __init__(self, upper_bound):
        self.cache = {}
        self.upper_bound = upper_bound

    def fibonacci(self, x):
        if not 0 <= x < self.upper_bound:
            raise ValueError('Out of bounds', x)

        try:
            return self.cache[x]
        except KeyError:
            pass

        if x in (0, 1):
            result = x
        else:
            result = self.fibonacci(x - 2) + self.fibonacci(x - 1)

        self.cache[x] = result

        return result


class CacheExcluded(CacheIncluded):
    def __getstate__(self):
        return (self.upper_bound, max(self.cache))

    def __setstate__(self, state):
        upper_bound, num = state
        self.cache = {}
        self.upper_bound = upper_bound
        self.fibonacci(num)


def compare():
    import pickle
    import bz2

    o1 = CacheIncluded(1500)
    o2 = CacheExcluded(1500)

    o1.fibonacci(1000)
    o2.fibonacci(1000)

    p1 = pickle.dumps(o1)
    c1 = bz2.compress(p1)

    p2 = pickle.dumps(o2)
    c2 = bz2.compress(p2)

    print('len(p1) is', len(p1), 'bytes')
    print('len(c1) is', len(c1), 'bytes')
    print()
    print('len(p2) is', len(p2), 'bytes')
    print('len(c2) is', len(c2), 'bytes')

    r1 = pickle.loads(p1)
    r2 = pickle.loads(p2)
    r3 = pickle.loads(bz2.decompress(c1))
    r4 = pickle.loads(bz2.decompress(c2))

    if r1.cache == r2.cache == r3.cache == r4.cache:
        print()
        print('All reconsituted objects contain the same data')


if __name__ == '__main__':
    compare()
