import random
import time
import io, os, sys
import networkx as nx
import matplotlib.pyplot as plt
import math
import pickle
import collections
import array,re,itertools

def find_assortativity(graph):
    return nx.degree_assortativity_coefficient(graph)

def pearson_assortativity(graph):
    return nx.degree_pearson_correlation_coefficient(graph)

#the average number of 'differences' in node degrees between a node and its neighbour
# is a fair indicator of the 'disassortativity' of a node.
def avg_neigh_diff(g):
    data = {}
    for n in g.nodes():
        data[n] = float(sum(abs(g.degree(i)-g.degree(n)) for i in g[n]))/g.degree(n)
    return data

def node_assort(g,lambdaa):
    data = {}
    S=0
    for n in g.nodes():
        #computing the average number of 'differences' in node degrees between a node and its neighbour.
        data[n] = float(sum(abs(g.degree(i)-g.degree(n)) for i in g[n]))/g.degree(n) 
        S+=data[n]
    print"Sum of all values:",S

    #we scale the average neighbour 'difference' values for each node, by dividing it by the sum of such values, S.
    for n in g.nodes():
        data[n]=data[n]/S

    #The scaled values , will therefore have a sum of S'=1.
    #Now we add a scaling factor lambdaa so that some of the nodes become assortative. 
    #This scaling factor can be randomly chosen, and acts as a threshold which determines the number of assortative nodes in the network. 
    #Therefore, we will choose the scaling factor lambdaa such that N*(lambdaa)-S'=r, where N is the number of nodes.

    #Then the node assortativity of node can be calculated as lambdaa - scaled values.
    for n in g.nodes():
        data[n]=lambdaa-data[n]
        data[n]=round(data[n],5) #round off values (optional)
    return data


def plot(G,ns,name):
    print "\nPlotting Degree_Node Assortativity Distribution"
    fig = plt.figure()
    plt.ylabel("Node Assortativity ")
    plt.xlabel("Degree")
    #mini=min(v for (k,v) in ns) #setting values for better plot for large graphs.
    #maxi=max(v for (k,v) in ns)
    ax = fig.add_subplot(111)
    #ax.set_yticks([mini,maxi])
    #ax.set_ylim(mini,maxi)
    ax.scatter([G.degree(k) for (k,v) in ns],[v for (k,v) in ns])
    plt.title("Degree_Node Assortativity Distribution")
    fig.savefig(str(name)+"Degree_Node Assortativity Distribution.png")
    plt.show()
  


#create a example line graph.
line_graph =nx.Graph()
line_graph.add_edges_from([(1,2),(2,3),(3,1),(4,5),(5,6),(6,7),(7,4),(8,9),(9,10)])

#compute assortativity of graph 'r'
r=nx.degree_assortativity_coefficient(line_graph) 
print "\nAssortativity of Graph = 'r' =",r

#compute Average neighbor degree. 
print "\nAverage neighbor degree: ",nx.average_neighbor_degree(line_graph)

#compute scaling factor lambdaa so that some of the nodes become assortative. 
lambdaa=(r+1)/nx.number_of_nodes(line_graph)

#compute Average neighbor difference in node degrees between a node and its neighbour.
print "\nAverage neighbor difference: ",avg_neigh_diff(line_graph)

#compute node assortativity.
ns=node_assort(line_graph,lambdaa)
print "\nNode Assortativity: ",ns

#plotting Degree_Node Assortativity Distribution.
ns=ns.items()
plot(line_graph,ns,"Line Graph")





