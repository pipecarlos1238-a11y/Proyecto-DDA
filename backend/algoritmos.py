def optimizar_carga_dp(paquetes, capacidad_maxima):
    """Programación Dinámica (Mochila 0/1) para seleccionar los mejores paquetes."""
    n = len(paquetes)
    dp = [[0] * (capacidad_maxima + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacidad_maxima + 1):
            peso = paquetes[i-1]['peso_kg']
            valor = paquetes[i-1]['prioridad']
            if peso <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - peso] + valor)
            else:
                dp[i][w] = dp[i-1][w]
                
    seleccionados = []
    w = capacidad_maxima
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            seleccionados.append(paquetes[i-1])
            w -= paquetes[i-1]['peso_kg']
    return seleccionados

def ruta_voraz(matriz, nodo_inicio=0):
    """Algoritmo del vecino más cercano O(n^2)."""
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
    """Exploración de estados con doble poda."""
    def __init__(self, matriz):
        self.matriz = matriz
        self.n = len(matriz)
        self.mejor_ruta = []
        self.mejor_distancia = float('inf')
        self.historial = [] 

    def registrar_paso(self, accion, ruta_actual, distancia):
        self.historial.append({
            "accion": accion,
            "ruta": list(ruta_actual),
            "distancia": round(distancia, 2),
            "mejor_distancia_actual": round(self.mejor_distancia, 2) if self.mejor_distancia != float('inf') else "Infinita"
        })

    def buscar_ruta(self, limite_voraz):
        self.mejor_distancia = limite_voraz
        visitados = [False] * self.n
        visitados[0] = True
        self._backtrack(0, 0.0, [0], visitados)
        return self.mejor_ruta, self.mejor_distancia, self.historial

    def _backtrack(self, nodo_actual, dist_acumulada, ruta_actual, visitados):
        # PODA Branch & Bound
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
            else:
                self.registrar_paso("poda", ruta_actual + [0], dist_final)
            return

        for sig_nodo in range(self.n):
            if not visitados[sig_nodo]:
                visitados[sig_nodo] = True
                dist_extra = self.matriz[nodo_actual][sig_nodo]
                ruta_actual.append(sig_nodo)
                
                self._backtrack(sig_nodo, dist_acumulada + dist_extra, ruta_actual, visitados)
                
                ruta_actual.pop()
                visitados[sig_nodo] = False
                self.registrar_paso("retroceso", ruta_actual, dist_acumulada)