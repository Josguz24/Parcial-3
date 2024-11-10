import matplotlib.pyplot as plt
import networkx as nx

class GrafoKruskal:
    def __init__(self):
        self.grafo = nx.Graph()  # Usamos NetworkX para facilitar la visualización

    def agregar_arista(self, nodo1, nodo2, peso):
        # Agrega una arista con peso entre nodo1 y nodo2
        self.grafo.add_edge(nodo1, nodo2, weight=peso)

    def kruskal(self, tipo='min'):
        # Obtener las aristas del grafo, ordenadas según el tipo de coste (mínimo o máximo)
        aristas = sorted(self.grafo.edges(data=True), key=lambda x: x[2]['weight'], reverse=(tipo == 'max'))
        mst = []
        conjuntos = {nodo: nodo for nodo in self.grafo.nodes()}  # Inicializar conjuntos disjuntos

        # Configuración de la visualización
        pos = nx.spring_layout(self.grafo)
        plt.ion()
        fig, ax = plt.subplots(figsize=(8, 6))

        def encontrar(conjuntos, nodo):
            # Encontrar la raíz del conjunto al que pertenece un nodo
            if conjuntos[nodo] != nodo:
                conjuntos[nodo] = encontrar(conjuntos, conjuntos[nodo])
            return conjuntos[nodo]

        def unir(conjuntos, nodo1, nodo2):
            # Unir dos conjuntos
            raiz1 = encontrar(conjuntos, nodo1)
            raiz2 = encontrar(conjuntos, nodo2)
            conjuntos[raiz2] = raiz1

        print(f"Iniciando el Algoritmo de Kruskal para el árbol de {'máximo' if tipo == 'max' else 'mínimo'} costo")

        for nodo1, nodo2, datos in aristas:
            peso = datos['weight']
            if encontrar(conjuntos, nodo1) != encontrar(conjuntos, nodo2):
                # Agregar la arista al árbol y unir conjuntos
                mst.append((nodo1, nodo2, peso))
                unir(conjuntos, nodo1, nodo2)
                print(f"Arista seleccionada: ({nodo1} --{peso}--> {nodo2})")

                # Dibujar el estado actual del árbol
                self.dibujar_grafo(pos, mst, nodo_actual=(nodo1, nodo2))

        plt.ioff()
        plt.show()
        return mst

    def dibujar_grafo(self, pos, mst, nodo_actual):
        plt.clf()
        # Dibujar el grafo original en color gris
        nx.draw(self.grafo, pos, with_labels=True, node_size=500, font_size=10, node_color="lightblue", edge_color="gray")
        
        # Mostrar los pesos de las aristas
        labels = nx.get_edge_attributes(self.grafo, 'weight')
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=labels, font_color="blue")
        
        # Resaltar el MST actual en rojo
        mst_edges = [(nodo1, nodo2) for nodo1, nodo2, _ in mst]
        nx.draw_networkx_edges(self.grafo, pos, edgelist=mst_edges, width=2, edge_color="red")
        
        # Resaltar la arista actual en naranja
        nx.draw_networkx_edges(self.grafo, pos, edgelist=[nodo_actual], width=2, edge_color="orange")

        plt.title("Árbol de Costo Mínimo/Máximo con Algoritmo de Kruskal")
        plt.draw()
        plt.pause(0.5)

# Ejemplo de uso
grafo = GrafoKruskal()
grafo.agregar_arista('A', 'B', 4)
grafo.agregar_arista('A', 'C', 2)
grafo.agregar_arista('B', 'C', 5)
grafo.agregar_arista('B', 'D', 10)
grafo.agregar_arista('C', 'D', 3)
grafo.agregar_arista('C', 'E', 8)
grafo.agregar_arista('D', 'E', 1)

# Ejecutar el algoritmo de Kruskal para el Árbol de Costo Mínimo
mst_min = grafo.kruskal(tipo='min')
print("\nÁrbol de Mínimo Costo (MST):")
for arista in mst_min:
    print(f"{arista[0]} --{arista[2]}--> {arista[1]}")

# Ejecutar el algoritmo de Kruskal para el Árbol de Costo Máximo
mst_max = grafo.kruskal(tipo='max')
print("\nÁrbol de Máximo Costo:")
for arista in mst_max:
    print(f"{arista[0]} --{arista[2]}--> {arista[1]}")
