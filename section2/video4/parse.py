import rx, rx.operators as ops
import pprint


def main():
    origin = rx.subjects.Subject()

    origin.pipe(
        ops.flat_map(rx.from_),
        ops.map(lambda x: bytes([x])),
        ops.filter(RemoveComments().next_character),
        ops.flat_map(Tokenize().next_character),
        ops.filter(bool),
        ops.flat_map(Parse().next_token),
    ).subscribe_(on_next=pprint.pprint, on_error=print)

    read_into("parse.lisp", origin)


class RemoveComments:
    def __init__(self):
        self.in_comment = False

    def next_character(self, char):
        if char == b";":
            self.in_comment = True
            return False
        elif char in b"\r\n":
            self.in_comment = False
            return True
        elif self.in_comment:
            return False
        else:
            return True


class Tokenize:
    def __init__(self):
        self.in_string = False
        self.stored = []

    def next_character(self, char):
        if self.in_string:
            if char == b'"':
                stored = b"".join(self.stored).decode("utf8")
                self.stored = []
                self.in_string = False
                return rx.of(stored)
            else:
                self.stored.append(char)
                return rx.empty()
        elif char == b'"':
            self.in_string = True
            return rx.empty()
        elif char in b"() \r\n\t":
            stored = b"".join(self.stored)
            self.stored = []
            return rx.of(stored, char.strip())
        else:
            self.stored.append(char)
            return rx.empty()


class Parse:
    def __init__(self):
        self.stack = []

    def next_token(self, token):
        if token == b"(":
            self.stack.append([])
            return rx.empty()
        elif token == b")":
            part = self.stack.pop()
            if self.stack:
                self.stack[-1].append(part)
                return rx.empty()
            else:
                return rx.of(part)
        else:
            self.stack[-1].append(token)
            return rx.empty()


def read_into(filename, observer):
    with open(filename, "rb") as f:
        chunk = f.read(1024)
        while chunk:
            observer.on_next(chunk)
            chunk = f.read(1024)
        observer.on_completed()


if __name__ == "__main__":
    main()
