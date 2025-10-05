import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('ws://127.0.0.1:5001/ws?access_token=123') as ws:
            print('connected')
            msg = await ws.receive()
            print(msg.json())
    print('disconnected')

if __name__ == '__main__':
    asyncio.run(main())
