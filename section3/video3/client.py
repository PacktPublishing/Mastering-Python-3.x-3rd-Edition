import sys
import asyncio
import base64
import aiohttp


async def main():
    with open(sys.argv[1], 'rb') as f:
        encoded = base64.b64encode(f.read())

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('http://127.0.0.1:8080/') as ws:
            await ws.send_bytes(encoded)
            print('Sent bytes')
            while True:
                result = await ws.receive_json()
                if 'crc' in result:
                    break
                print('=' * int(50 * result['progress']))
            print('3-bit CRC is', result['crc'])

if __name__ == '__main__':
    asyncio.run(main())
