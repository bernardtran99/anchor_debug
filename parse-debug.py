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

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def generate_static_nodes():
    input_links = []

    for keys in nodeDict:
        for values in nodeDict[keys]:
            if isinstance(values, int):
                input_links.append((values,keys))
    print(input_links)

    G.add_edges_from(input_links)
    plt.clf()
    plt.title("Demo")
    nx.draw(G, pos, with_labels=True,node_size=node_sizes,edgecolors='black',node_color=node_colors,connectionstyle='arc3, rad = 0.1')
    plt.show()

def generate_dynamic_nodes(source, destination):
    input_dynamic_links.append((source, destination))
    G.add_edges_from(input_dynamic_links)
    plt.clf()
    plt.title("Demo")
    nx.draw(G, pos, with_labels=True,node_size=node_sizes,edgecolors='black',node_color=node_colors,connectionstyle='arc3, rad = 0.1')
    plt.show()
    time.sleep(5)

def generate_layer_2():
    G.add_edges_from(input_dynamic_links)
    plt.clf()
    plt.title("Layer 2")
    nx.draw(G, pos, with_labels=True,node_size=node_sizes,edgecolors='black',node_color=node_colors,connectionstyle='arc3, rad = 0.1')
    plt.show()

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

# def generate_node_interrupt(time):
#     #if list has changed from last time, then generate new image and save
#     if input_ancmt_list != prev_ancmt_list or input_layer2_list != prev_layer2_list
#         combined_list = input_ancmt_list + input_layer2_list
#         G.add_edges_from(combined_list)
#         plt.clf()
#         plt.title('Time = {} s'.format(time))
#         nx.draw(G, pos, with_labels=True,node_size=node_sizes,edgecolors='black',node_color=node_colors,connectionstyle='arc3, rad = 0.1')
#         #fig = plt.figure()
#         #fig.savefig("topology.png")
#         plt.savefig("topology-{}.png".format(pic_num))
#         pic_num += 1
#         plt.show(block=False)
#         plt.pause(0.01)
#     prev_ancmt_list = input_ancmt_list
#     prev_layer2_list = input_layer2_list

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
                                input_layer2_list.append((node_num, firstInterest[node_num]) 

# def readIn():
#     with open(inputFile, 'r+', encoding = "ISO-8859-1") as fd:

#         for line in fd:
#             # if "Is Anchor" in line:
#             #     strings = line.split()
#             #     node_ip = strings[2]
#             #     node_num = ipDict[node_ip]
#             #     nodeDict[node_num] = ["anchor"]

#             if "On Interest" or "Flooded Interest" in line:
#                 strings = line.split()
#                 #ip number
#                 node_ip = strings[2]
#                 for i in range(len(strings)):
#                     if strings[i] == "Interest:":
#                         #strings[i+1] = 80n 
#                         strings[i + 1] = remove_suffix(strings[i + 1], "On")
#                         # also account for remove suffix flooded
#                         string_value = int(strings[i + 1])
#                         if node_num in nodeDict:
#                             if string_value not in nodeDict[node_num]:
#                                 nodeDict[node_num].append(string_value)
#                                 #generate_dynamic_nodes(string_value, node_num)
#                         else:
#                             #this will only add the first node every time
#                             nodeDict[node_num] = [string_value]
#                             #generate_dynamic_nodes(string_value, node_num)
#                             input_dynamic_links.append((node_num, string_value))
#                     elif strings[i] == "Flooded":

#add_edges_from() takes in a list of tuples
def node():
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

    for epoch in range(1, 18):
        plt.clf()
        if epoch == 2:
            G.add_edges_from([(1, 2),(1, 3)])
            node_sizes[0]= 1200
            node_colors[0] = 'red'
        if epoch == 3:
            G.add_edges_from([(2,1),(3,1)])
        if epoch == 4:
            G.add_edges_from([(2, 4),(3, 4),(2, 5), (3, 6)])
        if epoch == 5:
            G.add_edges_from([(4,2)])
        if epoch == 6:
            G.add_edges_from([(4, 5),(4, 7), (4, 6),(5,7),(5, 8),(6,7),(6, 9)])
        if epoch == 7:
            G.add_edges_from([(7, 4),(5, 2), (6, 4)])
        if epoch == 8:
            G.add_edges_from([(7, 8),(7, 9)])   
        if epoch == 9:
            G.add_edges_from([(8, 7),(9, 6)]) 
        if epoch == 10:
            G.add_edges_from([(8, 10),(9, 10)]) 
        if epoch == 11:
            G.add_edges_from([(10, 8)]) 
        if epoch == 12:
            G.remove_edges_from([(1, 2),(1, 3),(2, 4),(3, 4),(2, 5), (3, 6),(4, 5),(4, 7), (4, 6),(5,7),(5, 8),(6,7),(6, 9),(7, 8),(7, 9),(8, 10),(9, 10)])
        
        if epoch == 13:
            node_sizes[5]= 800
            node_colors[5] = 'yellow'
            G.add_edge(6,4,weight=6)
        if epoch == 14:
            node_colors[3] = 'yellow'
        if epoch == 15:
            node_colors[1] = 'yellow'  
        if epoch == 16:
            node_colors[0] = 'yellow'
        if epoch == 17:
            node_colors[1] = 'green'
            node_colors[3] = 'green'
            node_colors[0] = 'red'
             
        #create a matplot figure in order to automatically change the figure
        plt.clf()
        plt.title('Time {}s'.format(epoch))
        nx.draw(G, pos, with_labels=True,node_size=node_sizes,edgecolors='black',node_color=node_colors,connectionstyle='arc3, rad = 0.1')        
        #display.clear_output(wait=True)
        #display.display(plt.gcf()) 
        plt.show(block=False)
        plt.pause(0.02)
        time.sleep(1)

    #time.sleep(0.003)

# readIn()
# print(nodeDict)
# generate_layer_2()

readIn()
print(input_ancmt_list)
print(input_layer2_list)

# while True:
#     current_time += 0.003
#     readIn()
#     generate_continuous_nodes(current_time)
#     time.sleep(0.002)

#--------------------------------
#generate_static_nodes()

#for synchrony over time 
# while True:
#     fd = open(inputFile, 'r+')
#     for line in fd:
#         if()
#     fd.close()
#     time.sleep(0.003)


# with open(inputFile, 'r+') as fd:
#     for line in fd:
#         print(line)
#         if "" in line:
#             strings = line.split()
#             del strings[5]
#             #print(type(strings))
#             print(strings)

#2 versions
#one with real time simulations
#one where we generate a new picture whenever the structure of the topology changes\
#counter for sleep cycle for 2nd version
#change ip for debug server when vm closes

        