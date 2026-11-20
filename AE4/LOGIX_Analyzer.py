# LOGIX-Analyzer | AE4 | Alan Wetzel y Ciro Ferreira
# Analiza dependencias, costos y rutas para apoyar la modernizacion de LOGIX.
import os
CARPETA = os.path.dirname(os.path.abspath(__file__))

# Carga los modulos y valida la matriz de adyacencia.
def cargar(nombre):
    with open(os.path.join(CARPETA, nombre), encoding="utf-8") as f:
        lineas = [x.strip() for x in f if x.strip()]
    nombres = lineas[0].split(",")
    matriz = [[int(x) for x in fila.split(",")] for fila in lineas[1:]]
    n = len(nombres)
    if not n or n > 15 or len(set(nombres)) != n or len(matriz) != n:
        raise ValueError("Cantidad de modulos o filas incorrecta.")
    if any(len(f) != n or any(x not in (0, 1) for x in f) for f in matriz):
        raise ValueError("La matriz debe ser cuadrada y contener 0 o 1.")
    return nombres, matriz

# Muestra la matriz y calcula los grados de cada modulo.
def mostrar(nombres, matriz):
    print("     ", *nombres)
    for i in range(len(nombres)): print(nombres[i], matriz[i])
def grados(nombres, matriz):
    for i in range(len(nombres)):
        entrada = sum(matriz[j][i] for j in range(len(nombres)))
        print(nombres[i], "salida:", sum(matriz[i]), "entrada:", entrada)

# Warshall calcula las conexiones indirectas entre modulos.
def warshall(matriz):
    a = [f[:] for f in matriz]
    for k in range(len(a)):
        for i in range(len(a)):
            for j in range(len(a)):
                if a[i][k] and a[k][j]: a[i][j] = 1
    return a
def afectados(nombres, alcance, modulo):
    if modulo not in nombres: print("Modulo inexistente."); return
    j = nombres.index(modulo)
    lista = [nombres[i] for i in range(len(nombres)) if alcance[i][j] and i != j]
    print("Afectados:", lista if lista else "Ninguno")
# Los unos de la diagonal de A* identifican modulos que participan en ciclos.
def ciclos(nombres, alcance):
    lista = [nombres[i] for i in range(len(nombres)) if alcance[i][i]]
    print("Modulos que participan en ciclos:", lista if lista else "Ninguno")

# Gauss-Jordan resuelve sistemas cuadrados de hasta cinco incognitas.
def gauss_jordan(a, b):
    n = len(a)
    if not n or n > 5 or len(b) != n or any(len(f) != n for f in a):
        raise ValueError("El sistema debe ser cuadrado y de hasta 5x5.")
    m = [a[i][:] + [float(b[i])] for i in range(n)]
    fila, pivotes = 0, []
    for col in range(n):
        p = fila
        while p < n and abs(m[p][col]) < 1e-9: p += 1
        if p == n: continue
        m[fila], m[p] = m[p], m[fila]
        valor = m[fila][col]
        for j in range(n + 1): m[fila][j] /= valor
        for i in range(n):
            if i != fila:
                factor = m[i][col]
                for j in range(n + 1): m[i][j] -= factor * m[fila][j]
        pivotes.append(col); fila += 1
    for f in m:
        if all(abs(x) < 1e-9 for x in f[:n]) and abs(f[n]) >= 1e-9:
            return "Sin solucion", []
    if len(pivotes) < n: return "Infinitas soluciones", []
    return "Solucion unica", [m[i][n] for i in range(n)]

def equilibrio(f1, v1, f2, v2):
    if v1 == v2: return "No se cruzan" if f1 != f2 else "Son iguales"
    return (f2 - f1) / (v1 - v2)

# Carga las rutas como grafo no dirigido y admite el corredor del dron.
def cargar_rutas(nombre, dron=False):
    grafo = {}
    with open(os.path.join(CARPETA, nombre), encoding="utf-8") as f:
        for linea in f:
            a, b, peso = linea.strip().split(","); peso = int(peso)
            if peso < 0: raise ValueError("Dijkstra necesita pesos no negativos.")
            grafo.setdefault(a, []).append([b, peso]); grafo.setdefault(b, []).append([a, peso])
    if dron:
        grafo.setdefault("D", []).append(["Z3", 14]); grafo.setdefault("Z3", []).append(["D", 14])
    return grafo
# Dijkstra devuelve el camino y su costo minimo.
def dijkstra(grafo, inicio, fin):
    if inicio not in grafo or fin not in grafo: return [], float("inf")
    dist = {n: float("inf") for n in grafo}; anterior = {}; visitados = []
    dist[inicio] = 0
    while len(visitados) < len(grafo):
        actual = None
        for n in grafo:
            if n not in visitados and (actual is None or dist[n] < dist[actual]): actual = n
        if actual is None or dist[actual] == float("inf"): break
        visitados.append(actual)
        if actual == fin: break
        for vecino, peso in grafo[actual]:
            if vecino not in visitados and dist[actual] + peso < dist[vecino]:
                dist[vecino] = dist[actual] + peso; anterior[vecino] = actual
    if dist[fin] == float("inf"): return [], dist[fin]
    camino = [fin]
    while camino[0] != inicio: camino.insert(0, anterior[camino[0]])
    return camino, dist[fin]

# Orden topologico: primero se migran los modulos de los que otros dependen.
def migracion(nombres, matriz):
    n = len(nombres); pendientes = [sum(matriz[i]) for i in range(n)]
    siguientes = [[] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if matriz[i][j]: siguientes[j].append(i)
    cola = [i for i in range(n) if pendientes[i] == 0]; orden = []
    while cola:
        actual = cola.pop(0); orden.append(nombres[actual])
        for v in siguientes[actual]:
            pendientes[v] -= 1
            if pendientes[v] == 0: cola.append(v)
    return orden if len(orden) == n else []

# DFS recorre en profundidad con recursion y BFS utiliza una cola.
def recorridos(nombres, matriz, inicio):
    if inicio not in nombres: return [], []
    lista = {nombres[i]: [nombres[j] for j in range(len(nombres)) if matriz[i][j]] for i in range(len(nombres))}
    dfs = []
    def visitar(n):
        dfs.append(n)
        for v in lista[n]:
            if v not in dfs: visitar(v)
    visitar(inicio); cola = [inicio]; bfs = []
    while cola:
        n = cola.pop(0)
        if n not in bfs:
            bfs.append(n)
            for v in lista[n]:
                if v not in bfs and v not in cola: cola.append(v)
    return dfs, bfs

# Menu principal: ejecuta las funciones hasta que se elija salir.
def menu():
    try: nombres, matriz = cargar("dependencias.txt")
    except (OSError, ValueError, IndexError) as e: print("Error al cargar dependencias:", e); return
    while True:
        print("\nLOGIX-ANALYZER\n1 Matriz | 2 Grados | 3 Afectados | 4 Ciclos | 5 Gauss-Jordan")
        print("6 Equilibrio | 7 Dijkstra | 8 Migracion | 9 DFS/BFS | 0 Salir")
        op = input("Opcion: ")
        try:
            if op == "1": mostrar(nombres, matriz)
            elif op == "2": grados(nombres, matriz)
            elif op == "3":
                a = warshall(matriz); mostrar(nombres, a); afectados(nombres, a, input("Modulo: ").upper())
            elif op == "4": ciclos(nombres, warshall(matriz))
            elif op == "5":
                n = int(input("Cantidad de incognitas (1 a 5): "))
                if n < 1 or n > 5: print("La cantidad debe estar entre 1 y 5."); continue
                a, b = [], []
                for i in range(n):
                    fila = [float(x) for x in input("Fila de coeficientes: ").split()]
                    if len(fila) != n: raise ValueError("Cantidad de coeficientes incorrecta.")
                    a.append(fila); b.append(float(input("Termino independiente: ")))
                tipo, sol = gauss_jordan(a, b); print(tipo, sol)
            elif op == "6":
                f1 = float(input("Costo inicial A: ")); v1 = float(input("Costo anual A: "))
                f2 = float(input("Costo inicial B: ")); v2 = float(input("Costo anual B: "))
                print("Equilibrio:", equilibrio(f1, v1, f2, v2))
            elif op == "7":
                g = cargar_rutas("rutas.txt", input("Agregar corredor dron? s/n: ").lower() == "s")
                inicio = input("Origen (D, H1, H2, Z1, Z2, Z3): ").upper()
                fin = input("Destino (D, H1, H2, Z1, Z2, Z3): ").upper()
                camino, costo = dijkstra(g, inicio, fin); print("Camino:", camino if camino else "No existe", "Costo:", costo)
            elif op == "8":
                n, m = nombres, matriz
                if input("Grafo reestructurado? s/n: ").lower() == "s": n, m = cargar("dependencias_reestructuradas.txt")
                orden = migracion(n, m); print("Orden:", orden if orden else "No existe: hay ciclos.")
            elif op == "9":
                d, a = recorridos(nombres, matriz, input("Modulo inicial: ").upper()); print("DFS:", d, "BFS:", a)
            elif op == "0": print("Fin del programa."); break
            else: print("Opcion incorrecta.")
        except (ValueError, OSError, IndexError) as e: print("Entrada o archivo incorrecto:", e)

if __name__ == "__main__": menu()
