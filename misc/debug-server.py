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

NODE1 = "155.246.44.31"
NODE2 = "155.246.215.26"
NODE3 = "155.246.202.145"
NODE4 = "155.246.216.79"
NODE5 = "155.246.203.173"
NODE6 = "155.246.216.46"
NODE7 = "155.246.202.56"
NODE8 = "155.246.212.111"
NODE9 = "155.246.213.56"
NODE10 = "155.246.210.55"

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
graph_title = "Anchor Demo"
data_received_bool = 0
input_ancmt_list = []
input_layer2_list = []
firstInterest = {}
node8_list = []
node9_list = []
prev_node8 = 0
prev_node9 = 0
colors = 0
#create a global module later

class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        node_ip = peername[0]
        node_num = ipDict[node_ip]
        print('Connection from {} (Node {})'.format(peername, node_num))
        self.transport = transport

    def data_received(self, data):
        #time stamp, ip, node num, data
        message = data.decode("ISO-8859-1")
        node_info = self.transport.get_extra_info('peername')
        node_ip = node_info[0]
        now = datetime.now()
        strings = message.split()
        node_num = ipDict[node_ip]
        print('{} FROM: Node {!r} MESSAGE: {!r}'.format(now, node_num, message))

        
        if "Is Anchor" in message:
            node_sizes[0] = 1000
            node_colors[0] = 'red'
        if ("On Interest" in message) or ("Flooded Interest" in message):
            for i in range(len(strings)):
                global input_ancmt_list
                global input_layer2_list
                global firstInterest
                if strings[i] == "Interest:":
                    string_value = int(strings[i+1])
                    if node_num not in firstInterest:
                        firstInterest[node_num] = string_value
                    if (string_value, node_num) not in input_ancmt_list:
                        input_ancmt_list.append((string_value, node_num))
                    global G
                    G.add_edges_from([(string_value, node_num)])
                if (strings[i] == "Flooded") and (node_num != 1) and ((node_num, firstInterest[node_num]) not in input_layer2_list):
                    input_layer2_list.append((node_num, firstInterest[node_num]))
                    G.add_edges_from([(node_num, firstInterest[node_num])], color='b')
        if "Data" in message:
            global data_received_bool
            if data_received_bool == 0:
                G.remove_edges_from(input_ancmt_list)
                G.remove_edges_from(input_layer2_list)
                global graph_title
                graph_title = "Data Path"
                data_received_bool = 1
            if "Data Sent" in message:
                node_sizes[node_num-1] = 1000
                node_colors[node_num-1] = 'yellow'
                if node_num == 8:
                    global node8_list
                    G.remove_edges_from(node8_list)
                    global prev_node8
                    prev_node8 = 8
                    node8_list = []
                if node_num == 9:
                    global node9_list
                    G.remove_edges_from(node9_list)
                    global prev_node9
                    prev_node9 = 9
                    node9_list = []
            if "On Data: 8" in message:
                if (prev_node8, node_num) != (1,1) :
                    G.add_edges_from([(prev_node8, node_num)])
                node8_list.append((prev_node8, node_num))
                prev_node8 = node_num
            if "On Data: 9" in message:
                if (prev_node9, node_num) != (1,1) :
                    G.add_edges_from([(prev_node9, node_num)])
                node9_list.append((prev_node9, node_num))
                prev_node9 = node_num

        edges = G.edges()
        global colors
        colors = [G[u][v]['color'] for u,v in edges]
        plt.clf()
        plt.title(graph_title)
        nx.draw(G, pos, with_labels=True,node_size=node_sizes,edgecolors='black',node_color=node_colors,connectionstyle='arc3, rad = 0.1')
        nx.draw_networkx_edges(G, edge_color = colors)
        plt.show(block=False)
        plt.pause(0.000001)

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