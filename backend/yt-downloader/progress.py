import asyncio
import websockets

clients = {}

async def deal_message(websocket, path):
    async for message in websocket:
        message_list = message.split(',')
        if not (message_list[0] == "Hello" or message_list[0] == "goodbye") :
            # update progress
            print(message)
            try:
                await clients[message_list[1]].send(message)
            except websockets.ConnectionClosed:
                pass
            
        else :
            print(message)
            # 紀錄每個連線
            if(message_list[0] == "Hello") :
                # 新增連線
                clients[message_list[1]] = websocket
                # print(clients[message_list[1]])
            else :
                # 刪除連線
                del clients[message_list[1]]
            
            try:
                await websocket.send(message)
            except websockets.ConnectionClosed:
                pass

start_server = websockets.serve(deal_message, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()