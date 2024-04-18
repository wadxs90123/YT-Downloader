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



# import socket

# HOST = '127.0.0.1'
# PORT = 65432

# if __name__ == "__main__":
#     progress = 0
#     while True :
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.bind((HOST, PORT))
#             s.listen()

#             print(f'Server listening on {HOST}:{PORT}')

#             conn, addr = s.accept()
#             with conn:
#                 print('Connected by', addr)
#                 while True:
#                     data = conn.recv(1024)
#                     if not data:
#                         break
#                     decoded_data = data.decode('utf-8')
#                     if decoded_data == "Hello":
#                         # get progress
#                         conn.send(str(progress).encode())
#                     else:
#                         # update progress
#                         progress = int(decoded_data)