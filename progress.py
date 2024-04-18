import asyncio
import websockets

progress = 0
async def echo(websocket, path):
    global progress
    async for message in websocket:
        if message == "hello server!!!" :
            await websocket.send(str(progress))
        else :
            print(message)
            progress = int(message)

start_server = websockets.serve(echo, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()