# Green-TSP

"Green Reverend enters a bar. TSP!"
Ricordiamo che il TSP è un problema TOUR-ing completo :P

## Testo del problema

Un commesso viaggiatore deve visitare N clienti percorrendo un tour che inizia e termina al deposito. Poiché utilizza un veicolo elettrico che ha autonomia K km, all’occorrenza tra un cliente e il successivo, può visitare una stazione di ricarica dove esegue la ricarica completa acquistando nuovamente autonomia K. Noti i tempi di percorrenza degli archi tra il deposito, i clienti e le stazioni di ricarica, e ipotizzando una curva di ricarica lineare col tempo (per ogni istante di tempo si ricarica di una quantità pari a percorrere una unità di spazio), si determini il tour di durata minima. Si può considerare il grafo come completamente connesso ed è possibile passare più volte dalla stessa colonna di ricarica ma non dallo stesso cliente.

## Prerequisiti

- Python 3.9
- pip
- networkx
- pydot
- graphviz
- matplotlib

Per installare le librerie Pythons necessarie usare il comando:

```bash
apt install graphviz graphviz-dev
pip install networkx pydot matplotlib
```

## Funzioni utili

- Esportazione e importazione grafi:

```python
import networkx as nx
nx.write_gexf(G, "filename.gexf")
nx.read_gexf("filename.gexf",  destringizer=int)
```

## Istanze

Segniamo qui le informazioni sulle istanze che abbiamo utilizzato per testare il nostro algoritmo. Si trovano tutte nella cartella `instances`.
