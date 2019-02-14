import asyncio
import rx, rx.subjects, rx.operators as ops
import aiohttp, aiohttp.web as web
from base64 import b64decode
from rx.concurrency.mainloopscheduler import AsyncIOScheduler


async def crc(message, send, confirm = 0):
    # Simple but inefficient 3-bit CRC
    divisor = 0b1011
    mask = 0b1111
    message = (message << 3) | confirm

    full = message.bit_length() - 4

    while message > 7:
        offset = message.bit_length() - 4
        message = (((message >> offset) ^ divisor) << offset) | message & ~(mask << offset)
        await send({'progress': (full - offset) / full})

    await send({'crc': message})

async def connection(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.BINARY:
            request.app["subject"].on_next((msg.data, ws.send_json))

        elif msg.type == aiohttp.WSMsgType.ERROR:
            print("ERROR:", ws.exception())

    return ws


async def setup(app):
    app["scheduler"] = sched = AsyncIOScheduler()
    app["subject"] = subject = rx.subjects.Subject()

    subject.pipe(
        ops.map(lambda x: (b64decode(x[0]), x[1])),
        ops.map(lambda x: (int.from_bytes(x[0], "big", signed=False), x[1])),
    ).subscribe_(
        on_next=(lambda x: asyncio.create_task(crc(x[0], x[1]))), on_error=print
    )


def main():
    app = web.Application()
    app.on_startup.append(setup)
    app.add_routes([web.get("/", connection)])

    web.run_app(app)


if __name__ == "__main__":
    main()
