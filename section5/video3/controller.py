import subprocess

NUM_WORKERS = 16


def main():
    workers = []

    for i in range(NUM_WORKERS):
        workers.append(
            subprocess.Popen(
                ["python", "worker.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
            )
        )

    for num in range(100_000):
        workers[num % NUM_WORKERS].stdin.write(f"{num}\n")
        workers[num % NUM_WORKERS].stdin.flush()

    for num in range(100_000):
        print(num, workers[num % NUM_WORKERS].stdout.readline(), end="")

    for i, w in enumerate(workers):
        w.stdin.write("-1\n")
        w.stdin.flush()
        w.wait()

        if w.returncode != 0:
            print("Error in worker", i)


if __name__ == "__main__":
    main()
