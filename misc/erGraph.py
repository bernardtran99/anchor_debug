import networkx as nx
import time
import matplotlib.pyplot as plt
import random
from IPython import display
import operator
from functools import reduce
import numpy as np
import copy

p = 0.3 #The probability p in Erdos-Renyi random graph model
N = 20  # number of nodes
M = 10000  # A large number represents the maximum message limit
INF = 999  # distance upper bound

#The first function used to generate the graph
def BuildGraph_Matrix_1(n):
    Graph = [[0] * n for row in range(n)]#Initialize the graph

    for i in range(0, n):
        for j in range(0, n):
            if i == j:
                Graph[i][j] = 0
            else:
                Graph[i][j] = INF #Set disconnected nodes to INF(999)
    # randomly set edges base on p
    for i in range(0, n):
        for j in range(i, n):
            if i != j and random.random() <= p:
                Graph[i][j] = 1
                Graph[j][i] = 1
    return Graph

#Calculate the shortest distance between two nodes
def Floyd(vertex_total):
    distance = [[0] * vertex_total for row in range(vertex_total)]
    # initialize
    for i in range(0, vertex_total):
        for j in range(0, vertex_total):
            distance[i][j] = Graph_Matrix[i][j]
    # Use the Floyd algorithm to find the shortest distance between two vertices of all vertices
    for k in range(0, vertex_total):
        for i in range(0, vertex_total):
            for j in range(i, vertex_total):
                if distance[i][k] + distance[k][j] < distance[i][j]:
                    distance[i][j] = distance[i][k] + distance[k][j]
                    distance[j][i] = distance[i][k] + distance[k][j]
    return distance

Graph_Matrix = BuildGraph_Matrix_1(15)
distance=Floyd(15)

Graph_Matrix
distance

for i in range(0,15):
    print("Node %d's neighbor is :" % i)
    for j in range(0,15):
        if Graph_Matrix[i][j]==1:
            print("%d " % j)