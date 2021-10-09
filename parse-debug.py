import fileinput
import time
import os
import networkx as nx
import matplotlib.pyplot as plt
import pprint
from IPython import display

inputFile = "/home/debug/Documents/anchor_debug/build/debug-output.txt"
outputFile = "/home/debug/Documents/anchor_debug/build/parsed-debug.txt"

#ip lookup dictionary
ipDict = {
  "155.246.44.142" : 1,
  "155.246.215.101" : 2,
  "155.246.202.145" : 3,
  "155.246.216.113" : 4,
  "155.246.203.173" : 5,
  "155.246.216.33" : 6,
  "155.246.202.111" : 7,
  "155.246.212.111" : 8,
  "155.246.213.83" : 9,
  "155.246.210.98" : 10
}

#dictionary of nodes that have flooded
firstInterest = {}

#empty dict
nodeDict = {}
input_dynamic_links = []

input_ancmt_list = []
input_layer2_list = []
prev_ancmt_list = []
prev_layer2_list = []
combined_list = []

pic_num = 1

G=nx.MultiDiGraph()
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
pos=nx.get_node_attributes(G,'pos')
node_sizes = [500]*10
node_colors = ['green']*10
node_sizes[0] = 1200
node_colors[0] = 'red'

current_time = 0

#this is for real time video
def generate_continuous_nodes(time):
    combined_list = input_ancmt_list + input_layer2_list
    G.add_edges_from(combined_list)
    plt.clf()
    plt.title('Time = {} s'.format(time))
    nx.draw(G, pos, with_labels=True,node_size=node_sizes,edgecolors='black',node_color=node_colors,connectionstyle='arc3, rad = 0.1')
    if input_ancmt_list != prev_ancmt_list or input_layer2_list != prev_layer2_list:
        plt.savefig("topology-{}.png".format(pic_num))
        pic_num += 1
    plt.show(block=False)
    plt.pause(0.01)
    prev_ancmt_list = input_ancmt_list
    prev_layer2_list = input_layer2_list

def readIn():
    with open(inputFile, 'r+', encoding = "ISO-8859-1") as fd:
        for line in fd:
            if "On Interest" or "Flooded Interest" in line:
                strings = line.split()
                node_ip = strings[2]
                node_num = ipDict[node_ip]
                for i in range(len(strings)):
                    if strings[i] == "Interest:":
                        string_value = strings[i+1]
                        if node_num not in firstInterest:
                            firstInterest[node_num] = string_value
                        if (string_value, node_num) not in input_ancmt_list:
                            input_ancmt_list.append((string_value, node_num))
                    if strings[i] == "Flooded":
                        if node_num != 1:
                            if (node_num, firstInterest[node_num]) not in input_layer2_list:
                                input_layer2_list.append((node_num, firstInterest[node_num]))

readIn()
print(input_ancmt_list)
print(input_layer2_list)
generate_continuous_nodes(0)

# while True:
#     current_time += 0.003
#     readIn()
#     generate_continuous_nodes(current_time)
#     time.sleep(0.002)