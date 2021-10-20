import socket
import asyncio
import sys
import time
from datetime import datetime
import os
import networkx as nx
import matplotlib.pyplot as plt
import pprint
from IPython import display

NODE1 = "155.246.44.142"
NODE2 = "155.246.215.101"
NODE3 = "155.246.202.145"
NODE4 = "155.246.216.113"
NODE5 = "155.246.203.173"
NODE6 = "155.246.216.39"
NODE7 = "155.246.202.111"
NODE8 = "155.246.212.111"
NODE9 = "155.246.213.83"
NODE10 = "155.246.210.98"

#ip lookup dictionary
ipDict = {
    NODE1 : 1,
    NODE2 : 2,
    NODE3 : 3,
    NODE4 : 4,
    NODE5 : 5,
    NODE6 : 6,
    NODE7 : 7,
    NODE8 : 8,
    NODE9 : 9,
    NODE10 : 10
}

G = nx.MultiDiGraph()
G.add_node(1,pos=(2,6))
G.add_node(2,pos=(4,10))
G.add_node(3,pos=(4,2))
G.add_node(4,pos=(6,6))
G.add_node(5,pos=(8,10))
G.add_node(6,pos=(8,2))
G.add_node(7,pos=(10,6))
G.add_node(8,pos=(12,10))
G.add_node(9,pos=(12,2))
G.add_node(10,pos=(14,6))
pos = nx.get_node_attributes(G,'pos')
node_sizes = [500]*10
node_colors = ['green']*10

#python3

class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        #time stamp, ip, node num, data
        message = data.decode("ISO-8859-1")
        node_info = self.transport.get_extra_info('peername')
        node_ip = peer_info[0]
        now = datetime.now()
        print('{} FROM: {!r} MESSAGE: {!r}'.format(now, node_ip, message))

        strings = message.split()
        node_num = ipDict[node_ip]
        if "Is Anchor" in message:
            node_sizes[0] = 1000
            node_colors[0] = 'red'
        if "On Interest" in message:

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