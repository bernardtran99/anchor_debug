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

class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        print(self.transport.get_extra_info('peername'))

        # print('Send: {!r}'.format(message))
        # self.transport.write(data)

        # print('Close the client socket')
        #self.transport.close()


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '0.0.0.0', 8888)

    async with server:
        await server.serve_forever()


asyncio.run(main())