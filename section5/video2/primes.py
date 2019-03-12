import multiprocessing
from itertools import count

PRIMES_PER_PROCESS = 16


def check_divisbility(primes, number):
    return all(number % x for x in primes)


def checker(primes, in_potentials, out_primes, out_potentials):
    maximum = primes[-1] ** 2

    while True:
        potential = in_potentials.get()

        if potential == "stop":
            out_potentials.put("stop")
            return

        if check_divisbility(primes, potential):
            if potential < maximum:
                out_primes.put(potential)
            else:
                out_potentials.put(potential)


def printer(in_primes):
    while True:
        num = in_primes.get()

        if num == "stop":
            return

        print("Prime:", num)


def main():
    integers = count(2)

    initial_primes = []
    while len(initial_primes) < multiprocessing.cpu_count() * PRIMES_PER_PROCESS:
        num = next(integers)
        if check_divisbility(initial_primes, num):
            initial_primes.append(num)

    primes = multiprocessing.Queue()
    for p in initial_primes:
        primes.put(p)

    source = top = multiprocessing.Queue()

    print_process = multiprocessing.Process(target=printer, args=(primes,))
    print_process.start()

    processes = []

    for i in range(0, len(initial_primes), PRIMES_PER_PROCESS):
        potentials = multiprocessing.Queue()

        proc = multiprocessing.Process(
            target=checker,
            args=(
                initial_primes[i : i + PRIMES_PER_PROCESS],
                source,
                primes,
                potentials,
            ),
        )

        proc.start()

        processes.append(proc)

        source = potentials

    for i in range(initial_primes[-1] + 1, initial_primes[-1] ** 2):
        top.put(i)

    top.put("stop")

    for proc in processes:
        proc.join()

    primes.put("stop")
    print_process.join()

if __name__ == "__main__":
    main()
