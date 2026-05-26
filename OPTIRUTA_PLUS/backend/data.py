nodos_ibague = [
    # 0. Bodega Central
    {"id": 0, "nombre": "Plaza de Bolívar - Bodega Central", "lat": 4.444829727028302, "lon": -75.24302122452401, "peso_kg": 0, "volumen": 0, "prioridad": 0, "prioridad_txt": "BASE", "cliente": "Centro de Despacho"},
    
    # Clientes ajustados a la capacidad real:
    {"id": 1, "nombre": "Parque de El Salado", "lat": 4.449580833909641, "lon": -75.14501378249666, "peso_kg": 5, "volumen": 0.1, "prioridad": 100, "prioridad_txt": "ALTA", "cliente": "Ramon Castro"},
    {"id": 2, "nombre": "Glorieta Mirolindo", "lat": 4.422231817988396, "lon": -75.1858556758677, "peso_kg": 2, "volumen": 0.05, "prioridad": 80, "prioridad_txt": "MEDIA", "cliente": "Ana Martinez"},
    {"id": 3, "nombre": "Ricaute", "lat": 4.431360546201808, "lon": -75.2445320051487, "peso_kg": 45, "volumen": 1.5, "prioridad": 90, "prioridad_txt": "ALTA", "cliente": "Carlos Rodriguez"},
    {"id": 4, "nombre": "C.C. Multicentro", "lat": 4.436758355778967, "lon": -75.20171371819622, "peso_kg": 80, "volumen": 3.0, "prioridad": 50, "prioridad_txt": "BAJA", "cliente": "Andres Navarro"},
    {"id": 5, "nombre": "Universidad del Tolima", "lat": 4.428801128393785, "lon": -75.21348760655391, "peso_kg": 55, "volumen": 2.0, "prioridad": 40, "prioridad_txt": "BAJA", "cliente": "Claudia Vargas"},
    {"id": 6, "nombre": "Terminal de Transportes", "lat": 4.4373915025320345, "lon": -75.23474440470348, "peso_kg": 12, "volumen": 0.3, "prioridad": 60, "prioridad_txt": "MEDIA", "cliente": "Isabel Romero"},
    {"id": 7, "nombre": "Glorieta Picaleña", "lat": 4.399953355284915, "lon": -75.14568312084515, "peso_kg": 95, "volumen": 4.5, "prioridad": 75, "prioridad_txt": "MEDIA", "cliente": "Luis Fernandez"},
    {"id": 8, "nombre": "Estadio Murillo Toro", "lat": 4.430157037629767, "lon": -75.21817280470357, "peso_kg": 8, "volumen": 0.2, "prioridad": 150, "prioridad_txt": "URGENTE", "cliente": "Carmen Soto"},
    {"id": 9, "nombre": "SENA Av. Ferrocarril", "lat": 4.432731336353074, "lon": -75.211627417008, "peso_kg": 20, "volumen": 0.8, "prioridad": 85, "prioridad_txt": "MEDIA", "cliente": "Valentina Lozano"},
    {"id": 10, "nombre": "Mercacentro 10", "lat": 4.416602638146012, "lon": -75.17631930470358, "peso_kg": 110, "volumen": 5.0, "prioridad": 110, "prioridad_txt": "ALTA", "cliente": "Jorge Silva"},
    {"id": 11, "nombre": "C.C. La Estación", "lat": 4.445560630157438, "lon": -75.20485426237506, "peso_kg": 10, "volumen": 1.2, "prioridad": 60, "prioridad_txt": "MEDIA", "cliente": "Diana Gomez"},
    {"id": 12, "nombre": "Clínica Nuestra", "lat": 4.430777921341513, "lon": -75.19992103538965, "peso_kg": 4, "volumen": 0.1, "prioridad": 160, "prioridad_txt": "URGENTE", "cliente": "Hospital Central"},
    {"id": 13, "nombre": "Parque Deportivo", "lat": 4.427382028826051, "lon": -75.18326863353933, "peso_kg": 18, "volumen": 0.6, "prioridad": 65, "prioridad_txt": "BAJA", "cliente": "Liga Deportes"},
    {"id": 14, "nombre": "Boquerón (Vía Principal)", "lat": 4.408306078409527, "lon": -75.26476258240481, "peso_kg": 35, "volumen": 1.8, "prioridad": 40, "prioridad_txt": "BAJA", "cliente": "Ferreteria Ruiz"},
    {"id": 15, "nombre": "Barrio Belén", "lat": 4.448553823181195, "lon": -75.24145265550702, "peso_kg": 6, "volumen": 0.2, "prioridad": 90, "prioridad_txt": "BAJA", "cliente": "Marta Rojas"},
    {"id": 16, "nombre": "Barrio Cádiz", "lat": 4.439653917980909, "lon": -75.20694895386313, "peso_kg": 3, "volumen": 0.05, "prioridad": 88, "prioridad_txt": "ALTA", "cliente": "Pedro Alcantara"},
    {"id": 17, "nombre": "Piedrapintada", "lat": 4.436167507079064, "lon": -75.20738752670697, "peso_kg": 5, "volumen": 0.1, "prioridad": 75, "prioridad_txt": "BAJA", "cliente": "Sofia Lara"},
    {"id": 18, "nombre": "Universidad de Ibagué", "lat": 4.449301943098596, "lon": -75.20004527586772, "peso_kg": 25, "volumen": 0.9, "prioridad": 85, "prioridad_txt": "MEDIA", "cliente": "Biblioteca Uni"},
    {"id": 19, "nombre": "Barrio Vergel", "lat": 4.450734628366723, "lon": -75.19414567017999, "peso_kg": 4, "volumen": 0.1, "prioridad": 55, "prioridad_txt": "MEDIA", "cliente": "Conjunto Los Alpes"},
    {"id": 20, "nombre": "Colegio San Simón", "lat": 4.439066728608031, "lon": -75.21909044703199, "peso_kg": 40, "volumen": 2.2, "prioridad": 95, "prioridad_txt": "ALTA", "cliente": "Rectoria"},
    {"id": 21, "nombre": "Las Ferias", "lat": 4.430219572552161, "lon": -75.22918833309043, "peso_kg": 15, "volumen": 0.5, "prioridad": 60, "prioridad_txt": "BAJA", "cliente": "Almacen El Toro"},
    {"id": 22, "nombre": "Villa Café", "lat": 4.428299725200508, "lon": -75.18965461832255, "peso_kg": 6, "volumen": 0.2, "prioridad": 120, "prioridad_txt": "BAJA", "cliente": "Cafeteria Central"},
    {"id": 23, "nombre": "Barrio Topacio", "lat": 4.440745237568769, "lon": -75.16727554998424, "peso_kg": 10, "volumen": 0.3, "prioridad": 130, "prioridad_txt": "ALTA", "cliente": "Drogueria 24h"},
    {"id": 24, "nombre": "Barrio Gaitán", "lat": 4.442449920835278, "lon": -75.21272412004659, "peso_kg": 7, "volumen": 0.2, "prioridad": 50, "prioridad_txt": "BAJA", "cliente": "Familia Lopez"}
]