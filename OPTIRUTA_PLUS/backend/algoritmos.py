def quicksort_distancias(nodos, distancias):
    """
    Organizador ultra rápido. 
    Toma una lista de lugares y los ordena del más cercano al más lejano.
    """
    if len(nodos) <= 1:
        return nodos
    
    pivote = nodos[len(nodos) // 2]
    
    izq = [x for x in nodos if distancias[x] < distancias[pivote]]
    medio = [x for x in nodos if distancias[x] == distancias[pivote]]
    der = [x for x in nodos if distancias[x] > distancias[pivote]]
    
    return quicksort_distancias(izq, distancias) + medio + quicksort_distancias(der, distancias)

def optimizar_carga_dp(paquetes, capacidad_peso, capacidad_volumen):
    """
    La Mochila (Programación Dinámica Multidimensional).
    Decide qué paquetes subir al vehículo evaluando PESO y VOLUMEN simultáneamente.
    """
    n = len(paquetes)
    # Escalamos el volumen por 100 para manejar decimales como enteros en la matriz
    cap_v = int(capacidad_volumen * 100)
    
    # Creamos la matriz 3D: dp[paquetes][peso][volumen]
    dp = [[[0 for _ in range(cap_v + 1)] for _ in range(capacidad_peso + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        peso = paquetes[i-1]['peso_kg']
        vol = int(paquetes[i-1]['volumen'] * 100)
        valor = paquetes[i-1]['prioridad']
        
        for w in range(capacidad_peso + 1):
            for v in range(cap_v + 1):
                if peso <= w and vol <= v:
                    dp[i][w][v] = max(dp[i-1][w][v], dp[i-1][w - peso][v - vol] + valor)
                else:
                    dp[i][w][v] = dp[i-1][w][v]
                
    seleccionados = []
    w, v = capacidad_peso, cap_v
    for i in range(n, 0, -1):
        if dp[i][w][v] != dp[i-1][w][v]:
            seleccionados.append(paquetes[i-1])
            w -= paquetes[i-1]['peso_kg']
            v -= int(paquetes[i-1]['volumen'] * 100)
            
    return seleccionados

def ruta_voraz(matriz, nodo_inicio=0):
    """
    El conductor instintivo (Algoritmo Voraz).
    Traza una ruta rápida yendo siempre al cliente que le quede más cerquita.
    """
    n = len(matriz)
    visitados = [False] * n
    visitados[nodo_inicio] = True
    ruta = [nodo_inicio]
    distancia_total = 0.0
    nodo_actual = nodo_inicio

    for _ in range(n - 1):
        distancia_minima = float('inf')
        siguiente_nodo = None
        for j in range(n):
            if not visitados[j] and matriz[nodo_actual][j] < distancia_minima:
                distancia_minima = matriz[nodo_actual][j]
                siguiente_nodo = j
                
        ruta.append(siguiente_nodo)
        distancia_total += distancia_minima
        visitados[siguiente_nodo] = True
        nodo_actual = siguiente_nodo
    
    distancia_total += matriz[nodo_actual][nodo_inicio]
    ruta.append(nodo_inicio)
    return ruta, distancia_total

class BacktrackingInteractivo:
    """
    El cerebro que busca la ruta perfecta.
    Prueba caminos posibles, cortando (poda) si se excede peso, volumen o distancia.
    """
    def __init__(self, matriz, nodos_rutear, capacidad_max, volumen_max):
        self.matriz = matriz
        self.n = len(matriz)
        self.nodos_rutear = nodos_rutear
        self.capacidad_max = capacidad_max
        self.volumen_max = volumen_max
        self.mejor_ruta = []
        self.mejor_distancia = float('inf')
        self.historial = [] 
        
        self.vecinos_ordenados = []
        for i in range(self.n):
            vecinos = [j for j in range(self.n) if j != i]
            self.vecinos_ordenados.append(quicksort_distancias(vecinos, self.matriz[i]))

    def registrar_paso(self, accion, ruta_actual, distancia):
        if len(self.historial) < 800 or accion == "nueva_mejor":
            self.historial.append({
                "accion": accion,
                "ruta": list(ruta_actual),
                "distancia": round(distancia, 2)
            })

    def buscar_ruta(self, limite_voraz):
        self.mejor_distancia = limite_voraz
        visitados = [False] * self.n
        visitados[0] = True 
        self._backtrack(0, 0.0, 0, 0.0, [0], visitados)
        return self.mejor_ruta, self.mejor_distancia, self.historial

    def _backtrack(self, nodo_actual, dist_acumulada, peso_acumulado, vol_acumulado, ruta_actual, visitados):
        # 1. PODA POR PESO
        if peso_acumulado > self.capacidad_max:
            self.registrar_paso("poda", ruta_actual, dist_acumulada)
            return
            
        # 1.1 PODA POR VOLUMEN (Advertencia explícita)
        if vol_acumulado > self.volumen_max:
            self.registrar_paso("poda", ruta_actual, dist_acumulada)
            return

        # 2. PODA POR DISTANCIA
        if dist_acumulada >= self.mejor_distancia:
            self.registrar_paso("poda", ruta_actual, dist_acumulada)
            return

        self.registrar_paso("explorar", ruta_actual, dist_acumulada)

        if len(ruta_actual) == self.n:
            dist_final = dist_acumulada + self.matriz[nodo_actual][0]
            if dist_final < self.mejor_distancia:
                self.mejor_distancia = dist_final
                self.mejor_ruta = list(ruta_actual) + [0]
                self.registrar_paso("nueva_mejor", self.mejor_ruta, dist_final)
            return

        for sig_nodo in self.vecinos_ordenados[nodo_actual]:
            if not visitados[sig_nodo]:
                visitados[sig_nodo] = True
                dist_extra = self.matriz[nodo_actual][sig_nodo]
                peso_extra = self.nodos_rutear[sig_nodo]['peso_kg']
                vol_extra = self.nodos_rutear[sig_nodo].get('volumen', 0)
                ruta_actual.append(sig_nodo)
                
                self._backtrack(sig_nodo, 
                                dist_acumulada + dist_extra, 
                                peso_acumulado + peso_extra, 
                                vol_acumulado + vol_extra, 
                                ruta_actual, 
                                visitados)
                
                ruta_actual.pop()
                visitados[sig_nodo] = False