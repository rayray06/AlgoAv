
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def DisplayGraph(graph,FrontPath = [], FrontNode = None,EdgeWeigth = [],DisplayWeigth = False,DeleteOrNew = False):
    if(DeleteOrNew):
        plt.figure()
    else:
        plt.cls()
    G = nx.from_numpy_matrix(npGraph)
    
    pos = nx.spring_layout(G)
    node_colors = ['green' if i == FrontNode else 'red' for i in range(len(G.nodes))]
    print(G.edges)
    edge_colors = ['green' if (FrontPath[i],FrontPath[i+1]) in G.edges else 'red' for i in range(len(FrontPath)-1)]
    nx.draw_networkx(G, pos, with_labels=True, font_weight='bold',node_color=node_colors,edge_color=edge_colors,width=EdgeWeigth)
    if DisplayWeigth :
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    plt.show()
