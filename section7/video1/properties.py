class Foo:
    def __init__(self, x, y=None):
        self.x = x
        if y is not None:
            self.y = y

    @property
    def z(self):
        return self.x * self.y

    @z.setter
    def z(self, value):
        self.y = value / self.x

    @z.deleter
    def z(self):
        del self.y


if __name__ == "__main__":
    foo = Foo(5, 7)

    print("foo.x ==", foo.x)
    print("foo.y ==", foo.y)
    print("foo.z ==", foo.z)

    print()
    foo.z = 20
    print("Assigned foo.z = 20")

    print()
    print("foo.x ==", foo.x)
    print("foo.y ==", foo.y)
    print("foo.z ==", foo.z)

    print()
    del foo.z
    print("Deleted foo.z")

    print()
    print("foo.x ==", foo.x)
    try:
        print("foo.y ==", foo.y)
    except AttributeError:
        print("foo.y does not exist")
    else:
        print("foo.z ==", foo.z)
