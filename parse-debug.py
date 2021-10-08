import fileinput
import time
import os
import networkx as nx
import matplotlib.pyplot as plt
from IPython import display

inputFile = "/home/debug/Documents/anchor_debug/build/debug-output.txt"
outputFile = "/home/debug/Documents/anchor_debug/build/parsed-debug.txt"
onInterest = ""
nodeStart = ""
isAnchor = ""

ipDict = {
  "1": "155.246.44.142",
  "2": "155.246.215.101",
  "3": "155.246.202.145",
  "4": "155.246.216.113",
  "5": "155.246.203.173",
  "6": "155.246.216.33",
  "7": "155.246.202.111",
  "8": "155.246.212.111",
  "9": "155.246.213.83",
  "10": "155.246.210.98",
}

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

def node():
    plt.iot()
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
             
                  
        plt.clf()
        plt.title('Time {}s'.format(epoch))
        nx.draw(G, pos, with_labels=True,node_size=node_sizes,edgecolors='black',node_color=node_colors,connectionstyle='arc3, rad = 0.1')        
        #display.clear_output(wait=True)
        #display.display(plt.gcf()) 
        plt.draw()
        time.sleep(1)

node()

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
        