import rx, rx.operators as ops


def main():
    origin = rx.subjects.Subject()

    origin.pipe(
        ops.skip(20),
        ops.map(lambda x: x % 7),
        ops.filter(lambda x: x > 3),
    ).subscribe_(on_next = print)

    for x in range(37):
        origin.on_next(x)


if __name__ == "__main__":
    main()
