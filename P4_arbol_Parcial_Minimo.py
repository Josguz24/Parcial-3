import heapq
import matplotlib.pyplot as plt
import networkx as nx
import time

class Grafo:
    def __init__(self):
        self.grafo = nx.Graph()

    def agregar_arista(self, nodo1, nodo2, peso):
        # Añade una arista con peso entre nodo1 y nodo2 en el grafo
        self.grafo.add_edge(nodo1, nodo2, weight=peso)

    def prim(self, inicio):
        # Almacena las aristas del MST y los nodos visitados
        mst = []
        visitado = set([inicio])
        # Corrección: Asegurarse de extraer los tres valores correctamente
        aristas = [(peso, inicio, vecino) for _, vecino, peso in self.grafo.edges(inicio, data='weight')]
        heapq.heapify(aristas)

        # Configuración inicial de la visualización
        pos = nx.spring_layout(self.grafo)
        plt.ion()
        fig, ax = plt.subplots(figsize=(8, 6))

        print(f"Inicializando en el nodo '{inicio}'")

        while aristas:
            peso, nodo_desde, nodo_hacia = heapq.heappop(aristas)
            
            if nodo_hacia in visitado:
                continue

            # Agregar la arista al MST y marcar el nodo como visitado
            mst.append((nodo_desde, nodo_hacia, peso))
            visitado.add(nodo_hacia)
            print(f"Arista seleccionada: ({nodo_desde} --{peso}--> {nodo_hacia})")
            
            # Dibujar el estado actual del MST
            self.dibujar_grafo(pos, mst, inicio, nodo_actual=nodo_hacia)

            # Agregar nuevas aristas del nodo recién visitado
            for _, vecino, peso in self.grafo.edges(nodo_hacia, data='weight'):
                if vecino not in visitado:
                    heapq.heappush(aristas, (peso, nodo_hacia, vecino))

            time.sleep(1)

        plt.ioff()
        plt.show()
        return mst

    def dibujar_grafo(self, pos, mst, inicio, nodo_actual):
        plt.clf()
        # Dibujar el grafo original en color gris
        nx.draw(self.grafo, pos, with_labels=True, node_size=500, font_size=10, node_color="lightblue", edge_color="gray")
        
        # Mostrar los pesos de las aristas en color azul
        labels = nx.get_edge_attributes(self.grafo, 'weight')
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=labels, font_color="blue")
        
        # Resaltar el MST actual en rojo
        mst_edges = [(nodo_desde, nodo_hacia) for nodo_desde, nodo_hacia, _ in mst]
        nx.draw_networkx_edges(self.grafo, pos, edgelist=mst_edges, width=2, edge_color="red")
        
        # Resaltar el nodo actual en naranja
        nx.draw_networkx_nodes(self.grafo, pos, nodelist=[nodo_actual], node_color="orange", node_size=500)

        plt.title(f"Árbol Parcial Mínimo (MST) con Algoritmo de Prim\nNodo actual: {nodo_actual}")
        plt.draw()
        plt.pause(0.1)

# Ejemplo de uso
grafo = Grafo()
grafo.agregar_arista('A', 'B', 4)
grafo.agregar_arista('A', 'C', 2)
grafo.agregar_arista('B', 'C', 5)
grafo.agregar_arista('B', 'D', 10)
grafo.agregar_arista('C', 'D', 3)
grafo.agregar_arista('C', 'E', 8)
grafo.agregar_arista('D', 'E', 1)

# Ejecutar el algoritmo de Prim con visualización en consola y gráfica desde el nodo 'A'
mst = grafo.prim('A')

print("\nÁrbol Parcial Mínimo (MST) resultante:")
for arista in mst:
    print(f"{arista[0]} --{arista[2]}--> {arista[1]}")
