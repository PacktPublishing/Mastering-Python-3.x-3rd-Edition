import io

class ByteFIFO:
    def __init__(self):
        self.data = bytearray()

    def add(self, more):
        self.data.extend(more)
        return self

    def remove(self, count):
        del self.data[:count]

    def as_file(self):
        return io.BytesIO(self.data)
