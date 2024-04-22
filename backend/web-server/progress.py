import asyncio
import websockets

async def run_socket_server() :
    async def deal_message(websocket, path):
        async for message in websocket:
            if message == "hello server!!!" :
                await websocket.send(str(progress))
            else :
                print(message)
                progress = int(message)

    start_server = websockets.serve(deal_message, 'localhost', 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()