from concurrent.futures import ProcessPoolExecutor


def worker(base):
    result = 1
    for x in range(2, base + 1):
        result *= x
    return (base, result)


def controller():
    executor = ProcessPoolExecutor()

    for result in executor.map(worker, range(1000)):
        print(f"{result[0]}! = {result[1]}")

    executor.shutdown()


if __name__ == "__main__":
    controller()
