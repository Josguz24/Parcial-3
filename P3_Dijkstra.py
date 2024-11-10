import heapq
import matplotlib.pyplot as plt
import networkx as nx
import time

class Grafo:
    def __init__(self):
        self.grafo = nx.Graph()

    def agregar_arista(self, nodo1, nodo2, peso):
        self.grafo.add_edge(nodo1, nodo2, weight=peso)

    def dijkstra(self, origen):
        distancias = {nodo: float('inf') for nodo in self.grafo.nodes()}
        distancias[origen] = 0
        predecesores = {nodo: None for nodo in self.grafo.nodes()}
        cola_prioridad = [(0, origen)]

        # Distribución del grafo con mejor separación
        pos = nx.spring_layout(self.grafo)
        plt.ion()
        fig, ax = plt.subplots(figsize=(8, 6))

        while cola_prioridad:
            distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

            # Mostrar el estado actual en la consola
            print(f"\nNodo actual: {nodo_actual}, Distancia acumulada: {distancia_actual}")
            print(f"Distancias actuales: {distancias}")
            print(f"Predecesores actuales: {predecesores}")

            # Dibujar el estado actual del grafo
            self.dibujar_grafo(pos, distancias, origen, predecesores, nodo_actual)

            for vecino in self.grafo.neighbors(nodo_actual):
                peso = self.grafo[nodo_actual][vecino]['weight']
                distancia = distancia_actual + peso

                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    predecesores[vecino] = nodo_actual
                    heapq.heappush(cola_prioridad, (distancia, vecino))
                    print(f"    Actualizado: {vecino}, Nueva distancia: {distancia}, Predecesor: {nodo_actual}")

            time.sleep(1)

        plt.ioff()
        plt.show()
        return distancias, predecesores

    def dibujar_grafo(self, pos, distancias, origen, predecesores, nodo_actual):
        plt.clf()
        # Ajustar el tamaño de los nodos y el color
        nx.draw(self.grafo, pos, with_labels=False, node_size=500, font_size=8, node_color="lightblue", edge_color="gray")
        
        # Mostrar etiquetas de las aristas (pesos)
        labels = nx.get_edge_attributes(self.grafo, 'weight')
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=labels, font_color="blue")
        
        # Resaltar el nodo actual en naranja
        nx.draw_networkx_nodes(self.grafo, pos, nodelist=[nodo_actual], node_color="orange", node_size=500)
        
        # Resaltar el camino más corto encontrado hasta el momento en rojo
        for nodo, predecesor in predecesores.items():
            if predecesor is not None:
                nx.draw_networkx_edges(self.grafo, pos, edgelist=[(predecesor, nodo)], width=2, edge_color="red")
        
        # Ajustar etiquetas para las distancias, colocándolas justo afuera de cada nodo
        dist_labels = {nodo: f"{dist if dist < float('inf') else '∞'}" for nodo, dist in distancias.items()}
        nx.draw_networkx_labels(self.grafo, pos, labels=dist_labels, font_size=10, font_color="black", verticalalignment='center', horizontalalignment='right')
        
        # Etiquetas de nodos ligeramente desplazadas para mejor visibilidad
        nodo_labels = {nodo: nodo for nodo in self.grafo.nodes()}
        nx.draw_networkx_labels(self.grafo, pos, labels=nodo_labels, font_size=10, font_color="black", verticalalignment='top')

        plt.title(f"Algoritmo de Dijkstra desde el nodo {origen}\nNodo actual: {nodo_actual}")
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

# Ejecutar el algoritmo de Dijkstra con visualización en consola y gráfica desde el nodo 'A'
distancias, predecesores = grafo.dijkstra('A')

print("\nDistancias finales desde el nodo origen 'A':", distancias)
print("Predecesores para reconstruir caminos más cortos:", predecesores)
