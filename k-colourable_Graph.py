from z3 import *
import argparse
import itertools
import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

print("Hey There!! This is a k-colourable graph visualizer.\nLets try out \nGive me the number of nodes in graph")
n=int(input())
print("Give me the number of edges in the graph")
e=int(input())
if(e>n*(n-1)/2):
    print("Number of edges is greater than the number of possible edges.\nPlease enter a smaller number of edges")
    exit()
print("Give me the number of colours you want to use")
k=int(input())
print("I can generate a random graph with given number of nodes and edges.\nIf you want to generate a random graph, press 1.\nIf you want to enter the graph manually, press 2.")

edges = []
# reading edges from a file
if input() == '1':
    for i in range(e):
        x=random.randint(0,n-1)
        y=random.randint(0,n-1)
        while(x==y or [x,y] in edges or [y,x] in edges):
            x=random.randint(0,n-1)
            y=random.randint(0,n-1)
        edges.append([x,y])
    # print(edges)
else:
    print("Give me the edges in the graph \neg. 0,1 means edge between node 0 and node 1")
    for i in range(e):
        edges.append(input().split(","))
        edges[i][0]=int(edges[i][0])
        edges[i][1]=int(edges[i][1])

print("Hold on!! I am generating the graph for you")


# declare variables 'k' colors and 'n' nodes
vs = [[Bool("e_%i_%i" % (i, j)) for j in range(k)] for i in range(n)]

nodes = []
# encode each nodes has at least one color
for i in range(n):
    nodes.append(Or([vs[i][j] for j in range(k)]))

# encode each neighbours have different color
neigh = []
for e in edges:
    for c in range(k):
        neigh.append(Implies(vs[e[0]][c], Not(vs[e[1]][c])))


#list of 'k' beautiful colors
color = ["#%06X" % random.randint(0, 0xffffff) for i in range(k)]

result = Solver()
result.add(nodes)
result.add(neigh)
if str(result.check()) == "sat":
    m = result.model()
    color_map = []
    for i in range(n):
        for j in range(k):
            if m[vs[i][j]] == True:
                color_map.append(color[j])
                break

    G = nx.Graph()
    G.add_nodes_from(range(n))
    for e in edges:
        G.add_edge(e[0], e[1])
    pos=nx.nx_pydot.graphviz_layout(G,prog='dot')
    nx.draw(G,pos,node_color=color_map, with_labels=True)
    plt.show()
else:
    print(f"UnSAT : It is not {k} colorable.\nPro tip :) Increase the number of colors")
