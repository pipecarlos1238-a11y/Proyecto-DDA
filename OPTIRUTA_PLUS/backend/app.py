from flask import Flask, jsonify, request
from flask_cors import CORS
from data import nodos_ibague
from utils import generar_matriz_distancias
from algoritmos import ruta_voraz, BacktrackingInteractivo, optimizar_carga_dp

app = Flask(__name__)
CORS(app) 

@app.route('/api/nodos', methods=['GET'])
def obtener_nodos():
    return jsonify(nodos_ibague)

@app.route('/api/simular', methods=['POST'])
def simular_logistica():
    datos = request.json
    capacidad_camion = int(datos.get('capacidad', 60))
    volumen_camion = float(datos.get('capacidad_volumen', 2.5)) # Capturamos el volumen
    modo = datos.get('modo', 'auto')
    nodos_manuales = datos.get('nodos_manuales', [])

    paquetes_clientes = nodos_ibague[1:]

    # Si es automático, DP Mochila decide (ahora usa peso y volumen). 
    # Si es manual, usamos los IDs seleccionados.
    if modo == 'auto':
        seleccionados = optimizar_carga_dp(paquetes_clientes, capacidad_camion, volumen_camion)
    else:
        seleccionados = [n for n in paquetes_clientes if n['id'] in nodos_manuales]
    
    # Límite de seguridad para evitar que el Backtracking congele la PC
    if len(seleccionados) > 10:
        seleccionados = seleccionados[:10]

    nodos_rutear = [nodos_ibague[0]] + seleccionados
    matriz = generar_matriz_distancias(nodos_rutear)
    
    # 1. Voraz (Punto de partida)
    _, dist_voraz = ruta_voraz(matriz)
    
    # 2. Backtracking + Poda (Ruta exacta)
    # Pasamos el volumen_camion como cuarto argumento
    motor = BacktrackingInteractivo(matriz, nodos_rutear, capacidad_camion, volumen_camion)
    ruta_optima, dist_optima, historial = motor.buscar_ruta(limite_voraz=dist_voraz)
    
    # Totales para el Dashboard
    peso_total = sum(p['peso_kg'] for p in seleccionados)
    volumen_total = sum(p['volumen'] for p in seleccionados)

    return jsonify({
        "nodos_rutear": nodos_rutear,
        "ids_seleccionados": [p['id'] for p in seleccionados],
        "totales": {
            "paquetes": len(seleccionados),
            "peso_kg": round(peso_total, 2),
            "volumen_m3": round(volumen_total, 2)
        },
        "voraz": {"distancia": round(dist_voraz, 2)},
        "optima": {"ruta": ruta_optima, "distancia": round(dist_optima, 2)},
        "historial": historial
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)