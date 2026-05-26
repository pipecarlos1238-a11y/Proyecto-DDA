import math

def calcular_distancia(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia real en kilómetros entre dos puntos del mapa.
    Usa la fórmula de Haversine porque la Tierra es curva, no plana.
    """
    R = 6371.0 # Radio de la Tierra en km
    
    # 1. Pasamos los grados de Google Maps a radianes para que funcione la matemática
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # 2. Calculamos la diferencia entre los puntos
    dlat, dlon = lat2 - lat1, lon2 - lon1
    
    # 3. Aplicamos la fórmula de Haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def generar_matriz_distancias(nodos):
    """
    Crea una "tabla" (matriz) cruzando todos los clientes contra todos.
    Guarda las distancias pre-calculadas para que el Backtracking no pierda 
    tiempo haciendo los cálculos matemáticos de arriba una y otra vez.
    """
    n = len(nodos)
    
    # Construye la matriz. Si se compara un punto consigo mismo (i == j), la distancia es 0.
    return [
        [
            calcular_distancia(
                nodos[i]["lat"], nodos[i]["lon"], 
                nodos[j]["lat"], nodos[j]["lon"]
            ) if i != j else 0.0 
            for j in range(n)
        ] 
        for i in range(n)
    ]