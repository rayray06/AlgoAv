
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def DisplayGraph(graph,FrontPath = [], FrontNode = [],EdgeWeigth = [],DisplayWeigth = False,DeleteOrNew = True):
    if(DeleteOrNew):
        plt.figure()
    else:
        plt.cls()

    G = nx.from_numpy_matrix(np.asarray(np.round(graph)))
    
    pos = nx.spring_layout(G)
    node_colors = ['green' if i in FrontNode else 'red' for i in range(len(G.nodes))]

    edge_colors = ['green' if i in FrontPath else 'black' for i in G.edges]

    nx.draw_networkx(G, pos, with_labels=True, font_weight='bold',node_color=node_colors,edge_color=edge_colors,width=EdgeWeigth)

    if DisplayWeigth :
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    plt.show()
