from concurrent.futures import ProcessPoolExecutor, as_completed
from time import sleep
from random import random

def worker(base):
    result = 1
    for x in range(2, base + 1):
        result *= x
    sleep(random())
    return (base, result)


def controller():
    with ProcessPoolExecutor() as executor:
        futures = []

        for base in range(1000):
            futures.append(executor.submit(worker, base))

        for future in as_completed(futures):
            result = future.result()
            print(f"{result[0]}! = {result[1]}")


if __name__ == "__main__":
    controller()
