import json
import asyncio
import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.put('http://127.0.0.1:8080/var/five', data = json.dumps(dict(value = 5))) as response:
            if response.status != 200:
                print(await response.read)

        async with session.post('http://127.0.0.1:8080/add', data = json.dumps(dict(first = 'five', second = 3))) as response:
            if response.status != 200:
                print(await response.read())
            else:
                print("Adding five and 3 produces", (await response.json())['value'])

if __name__ == '__main__':
    asyncio.run(main())
