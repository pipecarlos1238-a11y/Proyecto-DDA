# backend/data.py

# Coordenadas 100% reales y exactas sobre la malla urbana de Ibagué
nodos_ibague = [
    # 0. BODEGA CENTRAL (Punto de Partida - Plaza de Bolívar)
    {"id": 0, "nombre": "Plaza de Bolívar (Centro)", "lat": 4.4388, "lon": -75.2342, "peso_kg": 0, "prioridad": 0},
    
    # === PAQUETES VIP (Los que la Mochila elegirá sí o sí) ===
    # Forzarán al camión a hacer un recorrido hermoso por toda la ciudad
    {"id": 1, "nombre": "Parque de El Salado", "lat": 4.4589, "lon": -75.1768, "peso_kg": 10, "prioridad": 500},
    {"id": 2, "nombre": "Glorieta Mirolindo", "lat": 4.4168, "lon": -75.1852, "peso_kg": 12, "prioridad": 600},
    {"id": 3, "nombre": "Ricaurte (Iglesia)", "lat": 4.4111, "lon": -75.2142, "peso_kg": 15, "prioridad": 550},
    {"id": 4, "nombre": "C.C. Multicentro", "lat": 4.4363, "lon": -75.2014, "peso_kg": 10, "prioridad": 450},
    {"id": 5, "nombre": "Universidad del Tolima", "lat": 4.4262, "lon": -75.2125, "peso_kg": 8, "prioridad": 400},
    {"id": 6, "nombre": "Terminal de Transportes", "lat": 4.4287, "lon": -75.2045, "peso_kg": 10, "prioridad": 380},
    {"id": 7, "nombre": "Glorieta Picaleña", "lat": 4.4042, "lon": -75.1585, "peso_kg": 10, "prioridad": 350},
    
    # === PAQUETES DESCARTADOS (Demostración del filtro de peso) ===
    # Caerán sobre calles reales, pero se quedarán en gris
    {"id": 8, "nombre": "Estadio Murillo Toro", "lat": 4.4261, "lon": -75.2177, "peso_kg": 40, "prioridad": 50},
    {"id": 9, "nombre": "SENA Av. Ferrocarril", "lat": 4.4326, "lon": -75.2198, "peso_kg": 35, "prioridad": 80},
    {"id": 10, "nombre": "Mercacentro 10", "lat": 4.4068, "lon": -75.1695, "peso_kg": 30, "prioridad": 100},
    {"id": 11, "nombre": "C.C. La Estación", "lat": 4.4385, "lon": -75.2065, "peso_kg": 45, "prioridad": 60},
    {"id": 12, "nombre": "Clínica Nuestra", "lat": 4.4281, "lon": -75.1802, "peso_kg": 50, "prioridad": 70},
    {"id": 13, "nombre": "Parque Deportivo", "lat": 4.4225, "lon": -75.1755, "peso_kg": 38, "prioridad": 110},
    {"id": 14, "nombre": "Boquerón (Vía Principal)", "lat": 4.4022, "lon": -75.2285, "peso_kg": 42, "prioridad": 40},
    {"id": 15, "nombre": "Barrio Belén", "lat": 4.4355, "lon": -75.2445, "peso_kg": 30, "prioridad": 90},
    {"id": 16, "nombre": "Barrio Cádiz", "lat": 4.4338, "lon": -75.2255, "peso_kg": 33, "prioridad": 65},
    {"id": 17, "nombre": "Piedrapintada", "lat": 4.4422, "lon": -75.2105, "peso_kg": 28, "prioridad": 75},
    {"id": 18, "nombre": "Universidad de Ibagué", "lat": 4.4498, "lon": -75.2005, "peso_kg": 40, "prioridad": 85},
    {"id": 19, "nombre": "Barrio Vergel", "lat": 4.4485, "lon": -75.1955, "peso_kg": 45, "prioridad": 55},
    {"id": 20, "nombre": "Colegio San Simón", "lat": 4.4352, "lon": -75.2205, "peso_kg": 32, "prioridad": 95},
    {"id": 21, "nombre": "Las Ferias", "lat": 4.4125, "lon": -75.2055, "peso_kg": 36, "prioridad": 60},
    {"id": 22, "nombre": "Villa Café", "lat": 4.4185, "lon": -75.1955, "peso_kg": 31, "prioridad": 120},
    {"id": 23, "nombre": "Barrio Topacio", "lat": 4.4475, "lon": -75.1855, "peso_kg": 34, "prioridad": 130},
    {"id": 24, "nombre": "Barrio Gaitán", "lat": 4.4450, "lon": -75.2250, "peso_kg": 27, "prioridad": 50}
]