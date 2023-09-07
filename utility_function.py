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
Dato il grafo G e 2 nodi calcola da quale noto passare facendo una deviazione 
Ritorna il nodo da cui passare e il costo della deviazione (somma del costo dei 2 archi)
'''
def cheapest_deviation(G :nx.Graph, nodo_attuale : int, nodo_successivo : int, nodi_da_visitare : list):
    lenght_list = []
    for i in nodi_da_visitare:
        i = int(i)
        #non vale dare deviazione da uno dei nodi della soluzione
        if i == nodo_attuale or i == nodo_successivo:
            continue

        #calcolo il costo della deviazione
        costo_deviazione = G[nodo_attuale][i]['weight'] + G[i][nodo_successivo]['weight']
        lenght_list.append ((costo_deviazione,i))
    
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
        #trasperenza
        G[u][v]['color'] = "#00000033"

    #coloro gli archi della soluzione di rosso
    for i in range(len(soluzione)-1):
        if soluzione[i] == soluzione[i+1]:
                continue
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

        #print("arco:",soluzione[i], soluzione[i+1], "costo:", G[soluzione[i]][soluzione[i+1]]['weight'])

        #costo strada
        if soluzione[i] == soluzione[i+1]:
              continue
        costo_strada += G[soluzione[i]][soluzione[i+1]]['weight']

        #se ho ricaricato la batteria
        if batteria_per_nodo[i+1] > batteria_per_nodo[i]:
            #costo batteria
            costo_batteria += batteria_per_nodo[i+1] - batteria_per_nodo[i]
            #print("costo batteria:", batteria_per_nodo[i+1] - batteria_per_nodo[i])

    return int(costo_strada + costo_batteria) #approssimiamo all'intero più vicino


'''
Dato un grafo G, una soluzione e la batteria massima di un veicolo calcola la batteria rimanente per ogni nodo
'''
def calcolo_batteria_per_nodo(G : nx.Graph, tour : list, batteria_max : int):
        batteria_per_nodo = [batteria_max]
        for i in range(1,len(tour)):
                #controllo se il nodo è di tipo cliente o colonnina
                if(G.nodes[tour[i]]['type'] == "colonnina"):
                        batteria_per_nodo.append(batteria_max)
                elif tour[i] == tour [i-1]:
                        batteria_per_nodo.append(batteria_per_nodo[i-1])                  
                else:
                        batteria = batteria_per_nodo[i-1] - G[tour[i-1]][tour[i]]['weight']
                        batteria_per_nodo.append(batteria)
                               
        return batteria_per_nodo

def check_batteria_negativa(batteria_per_nodo : list):
        for i in batteria_per_nodo:
                if i < 0:
                        return True
        return False


def get_farthest_node(G: nx.Graph, nodo_attuale: int, nodi_da_visitare: list):
    lenght_list = []
    for i in nodi_da_visitare:
        i = int(i)  # altrimenti è una stringa
        if i == nodo_attuale:
            continue
        #print(G[nodo_attuale][i]['weight'])
        lenght_list.append((G[nodo_attuale][i]['weight'], i))
    
    return max(lenght_list, key=lambda x: x[0])



def add_colonnine_to_tour(G : nx.Graph, tour : list, batteria_per_nodo : list, batteria_max : int):
        #controllo che ci sia un valore di batteria per ogni nodo del tour
        if(len(batteria_per_nodo) != len(tour)):
                print("errore: lunghezza batteria per nodo diversa da lunghezza tour")
                return None
        #scorro la lista finché nessun tratto sia negativo
        while(check_batteria_negativa(batteria_per_nodo)):

                for i in range(len(tour)-1,0,-1):
                #for i in range(0,len(tour)):
                        #print("i: ", i)
                        if(batteria_per_nodo[i] < 0):
                                #print("Sistemo un nodo")
                                #devo aggiungere una colonnina prima di tour[i]
                                tour, batteria_per_nodo = add_colonnina_before_i(G, tour, batteria_max, i)
                                break
        return tour, batteria_per_nodo

def add_colonnine_to_tour_reverse(G : nx.Graph, tour : list, batteria_per_nodo : list, batteria_max : int):
        #controllo che ci sia un valore di batteria per ogni nodo del tour
        if(len(batteria_per_nodo) != len(tour)):
                print("errore: lunghezza batteria per nodo diversa da lunghezza tour")
                return None
        #scorro la lista finché nessun tratto sia negativo
        while(check_batteria_negativa(batteria_per_nodo) == True):
              

                for i in range(len(tour)):
                #for i in range(0,len(tour)):
                       
                        if(batteria_per_nodo[i] < 0):
                             
                                #devo aggiungere una colonnina prima di tour[i]
                                tour, batteria_per_nodo = add_colonnina_before_i(G, tour, batteria_max, i)
                                
                                break
        return tour, batteria_per_nodo


def add_colonnina_before_i(G : nx.graph, tour : list, batteria_max : int, i : int):
        colonnine = [node for node in G.nodes if G.nodes[node]['type'] == "colonnina"]
        best_inserzione = (int(1000000000),0)
        for j in range(0,i): #i nodo batteria negativa
                        
                #prendo a due a due i nodi in tour 
                nodo_attuale = tour[j]
                nodo_successivo = tour[j+1]

                temp_tour = tour.copy()

                #trovo il nodo più vicino a nodo_attuale e nodo_successivo
                inserzione = cheapest_deviation(G, nodo_attuale, nodo_successivo, colonnine)
                #print("inserisco fra ", nodo_attuale, " e ", nodo_successivo, "colonnina:" , inserzione[1])
                temp_tour.insert(j+1,inserzione[1])
                batteria_per_nodo_temp = calcolo_batteria_per_nodo(G,temp_tour,batteria_max)
                #coppia costo totale deviazione e nodo da cui passare

                #print("temp tour; ", temp_tour)
                #print("batteria per nodo temp: ", batteria_per_nodo_temp)
                
                if inserzione[0] < best_inserzione[0] and batteria_per_nodo_temp[i+1] > 0:
                        #print("best inserzione trovata")
                        best_inserzione = inserzione
                        best_tour = temp_tour
                        best_batteria_per_nodo = batteria_per_nodo_temp

        return best_tour, best_batteria_per_nodo

def draw_notext(G : nx.Graph, soluzione : list, costo : int):

    colors_dict={"deposito":"blue", "cliente":"grey", "colonnina":"green"}

    #coloro tutti gli archi di nero
   
    #coloro gli archi della soluzione di rosso
    for i in range(len(soluzione)-1):
        if soluzione[i] == soluzione[i+1]:
                continue
        G[soluzione[i]][soluzione[i+1]]['color'] = "red"

    #aggiungiamo la soluzione all'immagine
    fig, axe = plt.subplots(figsize=(12,7))
    
    pos = graphviz_layout(G, prog="dot")

    #disegno del grafo
    nx.draw(G,
         with_labels=True, 
         node_color=  [colors_dict[G.nodes[node]['type']] for node in G],
         pos = nx.get_node_attributes(G, 'pos'), #così viene proporzionato in base alla distanza
         edge_color = [G[u][v]['color'] for u,v in G.edges] #coloro gli archi
         )
    
    plt.show()
    
def generate_combination(soluzione,taglio):
    '''
    Data una soluzione e una lista di 3 tagli  genera tutte le possibili combinazioni in cui è possibile ricostruire il tour. Senza toccare il primo e l'ultimo segmento.
    '''

    #ordino i tagli
    taglio = list(taglio)
    taglio.sort()

    #genero le 4 parti del tour
    t1=soluzione[:taglio[0]]
    t2=soluzione[taglio[0]:taglio[1]]
    t3=soluzione[taglio[1]:taglio[2]]
    t4=soluzione[taglio[2]:]

    sol1 = t1 + t2[::-1] + t3 + t4
    sol2 = t1 + t2 + t3[::-1] + t4
    sol3 = t1 + t2[::-1] + t3[::-1] + t4

    sol4 = t1 + t3 + t2 + t4
    sol5 = t1 + t3[::-1] + t2 + t4
    sol6 = t1 + t3 + t2[::-1] + t4
    sol7 = t1 + t3[::-1] + t2[::-1] + t4

    sol_list = [sol1, sol2, sol3, sol4, sol5, sol6, sol7]

    return sol_list

def compact_list(lista):
    '''
    Rimuove i duplicati da una lista
    '''
    lista_compatta = []
    for i in lista:
        if i not in lista_compatta or i==0:
            lista_compatta.append(i)
    return lista_compatta


def differenza_batteria_per_nodo( bpn1 : list, bpn2 : list):
        if len(bpn1) != len(bpn2):
            print("errore: lunghezza batteria per nodo diversa")
            return None
      
        diff = []
        for i in range(len(bpn1)):
                diff.append(bpn1[i] - bpn2[i])

        #ritorno la somma delle differenze
        return sum(diff)


def add_colonnina_rapporto(G : nx.graph, tour : list,  batteria_per_nodo : list, batteria_max : int):
        #provo tutte le colonnine che non sono nel tour
        colonnine = [node for node in G.nodes if G.nodes[node]['type'] == "colonnina"]
        #clienti = [node for node in G.nodes if G.nodes[node]['type'] == "cliente"]

        best_ratio = 0
        for j in range(0,len(tour)-1): #i nodo batteria negativa
                #prendo a due a due i nodi in tour 
                nodo_attuale = tour[j]
                nodo_successivo = tour[j+1]

                temp_tour = tour.copy()


                #trovo il nodo più vicino a nodo_attuale e nodo_successivo
                
                costo_inserzione, colonnina = cheapest_deviation(G, nodo_attuale, nodo_successivo, colonnine)
                guadagno_inserzione = batteria_max - G[colonnina][nodo_successivo]['weight'] - batteria_per_nodo[j+1] 
              
                ratio = guadagno_inserzione/costo_inserzione
          
                #aggiungo la colonnina a temp_tour
                temp_tour.insert(j+1,colonnina)
                
                if ratio > best_ratio:
                        #print("best inserzione trovata")
                        best_ratio = ratio
                        best_tour = temp_tour
                        best_batteria_per_nodo = calcolo_batteria_per_nodo(G,best_tour,batteria_max)
        
        return best_tour, best_batteria_per_nodo


def add_colonnine_to_tour_rapporto(G : nx.Graph, tour : list, batteria_per_nodo : list, batteria_max : int):
    #controllo che ci sia un valore di batteria per ogni nodo del tour
    if(len(batteria_per_nodo) != len(tour)):
        print("errore: lunghezza batteria per nodo diversa da lunghezza tour")
        return None

    #finchè la soluzione non diventa ammissibile
    while check_batteria_negativa(batteria_per_nodo) == True:
        tour, batteria_per_nodo = add_colonnina_rapporto(G, tour, batteria_per_nodo, batteria_max)

    return tour, batteria_per_nodo
