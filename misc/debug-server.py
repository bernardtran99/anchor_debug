import socket
import asyncio
import sys
import time
from datetime import datetime

#python3

class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        #time stamp, ip, node num, data
        message = data.decode()
        peer_info = self.transport.get_extra_info('peername')
        peer_ip = peer_info[0]
        now = datetime.now()
        print('{} FROM: {!r} MESSAGE: {!r}'.format(now, peer_ip, message))

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