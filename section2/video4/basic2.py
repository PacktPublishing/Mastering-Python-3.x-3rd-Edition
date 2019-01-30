import rx, rx.operators as ops


def source(observer, scheduler):
    for x in range(37):
        observer.on_next(x)
    observer.on_completed()


def main():
    origin = rx.create(source)

    origin.pipe(
        ops.skip(20),
        ops.map(lambda x: x % 7),
        ops.filter(lambda x: x > 3),
    ).subscribe_(on_next = print)

if __name__ == "__main__":
    main()
