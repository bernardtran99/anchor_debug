import socket
import asyncio
import sys
import time

#python3

# HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
# PORT = 8888     # Port to listen on (non-privileged ports are > 1023)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             print(data.decode("utf-8"))
#             if not data:
#                 break
#             conn.sendall(data)

async def handle_client(reader, writer):
    request = None
    while request != 'quit':
        request = (await reader.read(255)).decode('utf8')
        print(request)
        #response = str(eval(request)) + '\n'
        response = "OK"
        writer.write(response.encode('utf8'))
        await writer.drain()
    writer.close()

async def run_server():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 8888)
    async with server:
        await server.serve_forever()

asyncio.run(run_server())