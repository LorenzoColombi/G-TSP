from ast import Tuple
import networkx as nx 
import random
from scipy import spatial
from sklearn.metrics import euclidean_distances
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import pydot

'''
Genera un grafo casuale con n nodi in uno spazio di lunghezza space_lenght
Il costo degli archi è dato dalla distanza euclidea fra i nodi
Ogni nodo ha attributo type = cliente / colonnina
'''
def random_euclidean_graph(n : int, space_lenght : int) -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from([(0, {'pos': (random.randint(0, space_lenght), random.randint(0, space_lenght)), "type": "deposito"}) ])
    G.add_nodes_from([(i, {'pos': (random.randint(0, space_lenght), random.randint(0, space_lenght)), "type": random.choice(["cliente","colonnina","cliente","cliente"])}) for i in range(1,n)])
    for i in range(n):
        for j in range(i+1, n):
            #print(G.nodes[i]['pos'][0], G.nodes[j]['pos'])
            G.add_edge(i, j, weight = euclidean_distances(G.nodes[i]['pos'], G.nodes[j]['pos']))
    return G 

'''
distanza euclidea tra due punti
'''
def euclidean_distances(x, y):
    return spatial.distance.euclidean(x, y)

'''
Disega il grafo G
'''
def draw_graph(G : nx.Graph):
    colors_dict={"deposito":"blue", "cliente":"grey", "colonnina":"green"}
    nx.draw(G,
         with_labels=True, 
         node_color=  [colors_dict[G.nodes[node]['type']] for node in G],
         pos = nx.get_node_attributes(G, 'pos') #così viene proporzionato in base alla distanza
         )
    
'''
Calcola il nodo più vicino a nodo_attuale fra i nodi da visitare nella lista nodi_da_visitare
Ritorna una coppia (distanza, nodo)
'''
def get_nearest_node(G : nx.Graph, nodo_attuale : int, nodi_da_visitare : list):
    lenght_list = []
    for i in nodi_da_visitare:
        i = int(i) #altrinmenti è una stringa
        if i == nodo_attuale:
            continue
        #print(G[nodo_attuale][i]['weight'])
        lenght_list.append ((G[nodo_attuale][i]['weight'],i))
    
    return min(lenght_list, key=lambda x: x[0])
   

'''
plot the solution with the solution edge in red
G un grafo e soluzione una lista di nodi che rappresenta la soluzione del problema
costo è il costo della soluzione
'''
def draw_solution(G : nx.Graph, soluzione : list, costo : int):

    colors_dict={"deposito":"blue", "cliente":"grey", "colonnina":"green"}

    #coloro tutti gli archi di nero
    for u,v in G.edges:
        G[u][v]['color'] = "black"

    #coloro gli archi della soluzione di rosso
    for i in range(len(soluzione)-1):
        G[soluzione[i]][soluzione[i+1]]['color'] = "red"

    #aggiungiamo la soluzione all'immagine
    fig, axe = plt.subplots(figsize=(12,7))
    soluzione = str(soluzione)
    soluzione = "SOLUZIONE:\n" + soluzione
    soluzione = soluzione.replace("[", "")
    soluzione = soluzione.replace("]", "")
    soluzione = soluzione.replace(",", " ->")
    soluzione = soluzione + "\nCOSTO: " + str(costo)


    axe.set_title(soluzione, loc='left')
    pos = graphviz_layout(G, prog="dot")

    #disegno del grafo
    nx.draw(G,
         with_labels=True, 
         node_color=  [colors_dict[G.nodes[node]['type']] for node in G],
         pos = nx.get_node_attributes(G, 'pos'), #così viene proporzionato in base alla distanza
         edge_color = [G[u][v]['color'] for u,v in G.edges] #coloro gli archi
         )
    
    plt.show()

'''
Calcolo del costo della soluzione, somma dei costi degli archi percorsi (strada) e dei tempi di ricarica (batteria)
G un grafo, soluzione una lista di nodi che rappresenta la soluzione del problema, batteria per nodo una lista che rappresenta la batteria rimanente per ogni nodo
'''
def costo(G : nx.Graph, soluzione : list, batteria_per_nodo : list) -> int:
    costo_strada = 0
    costo_batteria = 0
    #costo percorso stradale
    for i in range(len(soluzione)-1):

        print("arco:",soluzione[i], soluzione[i+1], "costo:", G[soluzione[i]][soluzione[i+1]]['weight'])

        #costo strada
        costo_strada += G[soluzione[i]][soluzione[i+1]]['weight']

        #se ho ricaricato la batteria
        if batteria_per_nodo[i+1] > batteria_per_nodo[i]:
            #costo batteria
            costo_batteria += batteria_per_nodo[i+1] - batteria_per_nodo[i]
            print("costo batteria:", batteria_per_nodo[i+1] - batteria_per_nodo[i])

    return int(costo_strada + costo_batteria) #approssimiamo all'intero più vicino

