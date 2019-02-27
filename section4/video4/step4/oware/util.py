from __future__ import annotations
from typing import List
import io
import asyncio

class ByteFIFO:
    def __init__(self: ByteFIFO):
        self.data: bytearray = bytearray()
        self.waiting: List[asyncio.Future[bool]] = []

    def add(self: ByteFIFO, more: bytes) -> ByteFIFO:
        self.data.extend(more)

        waiting = self.waiting
        self.waiting = []
        for fut in waiting:
            fut.set_result(True)

        return self

    def remove(self: ByteFIFO, count: int) -> None:
        del self.data[:count]

    def as_file(self: ByteFIFO) -> io.BytesIO:
        return io.BytesIO(self.data)

    async def more_data(self: ByteFIFO) -> bool:
        fut = asyncio.get_running_loop().create_future()
        self.waiting.append(fut)
        result: bool = await fut
        return result
