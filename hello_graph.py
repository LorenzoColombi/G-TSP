#Esempio di creazione grafo
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

nodes_list = [(1, {'color': 'blue'}), (2, {'color': 'red'}), (3, {'color': 'green'})]

G.add_nodes_from(nodes_list)


nx.draw(G)