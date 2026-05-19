import math

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def generar_matriz_distancias(nodos):
    n = len(nodos)
    return [[calcular_distancia(nodos[i]["lat"], nodos[i]["lon"], nodos[j]["lat"], nodos[j]["lon"]) if i != j else 0.0 for j in range(n)] for i in range(n)]
