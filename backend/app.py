from flask import Flask, jsonify, request
from flask_cors import CORS
from data import nodos_ibague
from utils import generar_matriz_distancias
from algoritmos import ruta_voraz, BacktrackingInteractivo, optimizar_carga_dp

app = Flask(__name__)
CORS(app) 

@app.route('/api/simular', methods=['GET'])
def simular_logistica():
    # 1. Leer la capacidad manual enviada desde la interfaz web (por defecto 80)
    capacidad_camion = int(request.args.get('capacidad', 80))
    
    # 2. DP (Mochila): Filtrar paquetes según el nuevo límite
    paquetes_clientes = nodos_ibague[1:] # Todo menos la bodega
    seleccionados_dp = optimizar_carga_dp(paquetes_clientes, capacidad_camion)
    
    # Límite de seguridad: Si la capacidad es muy alta y selecciona más de 10, lo limitamos
    # para evitar que tu computadora se congele calculando más de 39 millones de combinaciones (11!)
    if len(seleccionados_dp) > 10:
        seleccionados_dp = seleccionados_dp[:10]
    
    # 3. Preparar el sub-problema
    nodos_rutear = [nodos_ibague[0]] + seleccionados_dp
    matriz = generar_matriz_distancias(nodos_rutear)
    
    # 4. Voraz (Para el límite de la poda)
    ruta_v, dist_v = ruta_voraz(matriz)
    
    # 5. Backtracking con poda 
    motor = BacktrackingInteractivo(matriz)
    ruta_optima, dist_optima, historial = motor.buscar_ruta(limite_voraz=dist_v)
    
    return jsonify({
        "nodos_totales": nodos_ibague,
        "nodos_rutear": nodos_rutear,
        "voraz": {"ruta": ruta_v, "distancia": round(dist_v, 2)},
        "optima": {"ruta": ruta_optima, "distancia": round(dist_optima, 2)},
        "historial": historial,
        "stats": {
            "total": len(paquetes_clientes),
            "elegidos": len(seleccionados_dp),
            "peso": sum(p['peso_kg'] for p in seleccionados_dp),
            "capacidad_maxima": capacidad_camion
        }
    })

if __name__ == '__main__':
    print("🚀 Servidor logístico interactivo iniciado...")
    app.run(debug=True, port=5000)