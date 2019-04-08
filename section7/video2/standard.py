import threading
import sqlite3

if __name__ == "__main__":
    # Files are automatically closed
    print("The file is not yet open")

    with open("example.txt", "w") as f:
        f.write("Example file content\n")

    print("The file has already been closed")


    # Mutexes are acquired at the beginning and released at the end of the with block
    # This works for asyncio's Lock class as well
    lock = threading.Lock()

    print("The lock is available")

    with lock:
        print("The lock is acquired")

    print("The lock is available again")


    # SQLite database transactions are started at the beginning of the
    # with block, and automatically committed or rolled back depending
    # on whether an exception was raised within the block
    db = sqlite3.connect(":memory:")
    db.execute("create table item (id integer primary key, slug varchar unique)")

    try:
        with db:
            db.execute("insert into item (slug) values (:slug)", {"slug": "foo"})
    except sqlite3.IntegrityError:
        print("Commit 1 rolled back")
    else:
        print("Commit 1 succeeded")

    try:
        with db:
            db.execute("insert into item (slug) values (:slug)", {"slug": "foo"})
    except sqlite3.IntegrityError:
        print("Commit 2 rolled back")
    else:
        print("Commit 2 succeeded")


    # Multiple context managers can be used at once
    with open('example2.txt', 'w') as file_out, open('example.txt', 'r') as file_in:
        file_out.write(
            file_in.read()
        )
