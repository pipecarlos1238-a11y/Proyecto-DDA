// ==========================================
// 1. CONEXIONES CON EL HTML Y CONFIGURACIÓN
// ==========================================

const DOM = {
    log: document.getElementById('log'), btnStart: document.getElementById('btnStart'),
    btnPause: document.getElementById('btnPause'), btnResume: document.getElementById('btnResume'),
    panelRuta: document.getElementById('panelRuta'), listaRuta: document.getElementById('listaRuta'),
    tablaBody: document.getElementById('tablaPaquetesBody'),
    dashVehiculo: document.getElementById('dashVehiculo'), dashPaquetes: document.getElementById('dashPaquetes'),
    dashPeso: document.getElementById('dashPeso'), dashVolumen: document.getElementById('dashVolumen'),
    lblOptima: document.getElementById('lblOptima'), lblTiempo: document.getElementById('lblTiempo'),
    lblSeleccionados: document.getElementById('lblSeleccionadosTabla'), modoSeleccion: document.getElementById('modoSeleccion'),
    treePanel: document.getElementById('treePanel'),
    statNodos: document.getElementById('statNodos'), statPoda: document.getElementById('statPoda'), statMejoras: document.getElementById('statMejoras')
};

let map = L.map('mapa', { zoomControl: false }).setView([4.4385, -75.2341], 14);
L.control.zoom({ position: 'bottomright' }).addTo(map);
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { attribution: '&copy; OpenStreetMap' }).addTo(map);

let layerMarcadores = L.layerGroup().addTo(map);
let layerRutas = L.layerGroup().addTo(map);

let cyInstance = null; 

// ==========================================
// 2. EL CEREBRO DE LA INTERFAZ (Objeto App)
// ==========================================
const App = {
    nodosBase: [], timeoutId: null, isPaused: false, historial: [], optima: null, 
    indice: 0, vehiculoSeleccionado: 'Van', capacidad: 60, nodos_rutear: [],
    modo: 'auto', ids_manuales: [], stats: { nodos: 0, podas: 0, mejoras: 0 },

    escribirLog(texto, clase = '') {
        DOM.log.innerHTML += `<div class="${clase}">${texto}</div>`;
        DOM.log.scrollTop = DOM.log.scrollHeight;
    },

    seleccionarVehiculo(tipo, cap) {
        document.querySelectorAll('.vehiculo-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('v-' + tipo.toLowerCase().replace('ó','o')).classList.add('active');
        this.vehiculoSeleccionado = tipo;
        this.capacidad = cap;
        DOM.dashVehiculo.innerText = tipo;
        this.escribirLog(`Vehículo: ${tipo}. Límite Mochila: ${cap} kg.`, "log-info");
    },

    cambiarModo() {
        this.modo = DOM.modoSeleccion.value;
        this.ids_manuales = [];
        this.dibujarNodosClickables(this.nodosBase);
        this.llenarTablaPaquetes(this.nodosBase, this.ids_manuales);
        
        if(this.modo === 'manual') {
            this.escribirLog("Modo Manual: Haz clic en el mapa o en la tabla para agregar carga (Máx 8).", "log-warning");
        } else {
            this.escribirLog("Modo Automático: La Mochila DP decidirá qué llevar.", "log-info");
        }
    },

    toggleNodo(nodo) {
        if (this.modo === 'auto' || nodo.id === 0) return;
        
        const index = this.ids_manuales.indexOf(nodo.id);
        if (index > -1) {
            this.ids_manuales.splice(index, 1);
        } else {
            if (this.ids_manuales.length >= 8) {
                alert("Para evitar congelar el procesador con el Backtracking, solo puedes elegir un máximo de 8 destinos a la vez.");
                return;
            }
            this.ids_manuales.push(nodo.id);
        }
        
        this.dibujarNodosClickables(this.nodosBase);
        this.llenarTablaPaquetes(this.nodosBase, this.ids_manuales);
        
        let pesoTotalManual = 0; let volTotalManual = 0;
        this.ids_manuales.forEach(id => {
            let info = this.nodosBase.find(n => n.id === id);
            pesoTotalManual += info.peso_kg;
            volTotalManual += info.volumen;
        });
        
        DOM.dashPaquetes.innerText = this.ids_manuales.length;
        DOM.dashPeso.innerText = pesoTotalManual.toFixed(2);
        DOM.dashVolumen.innerText = volTotalManual.toFixed(2);

        // Advertencia Peso
        if (pesoTotalManual > this.capacidad) {
            this.escribirLog(`⚠️ ADVERTENCIA: Te excediste del límite de ${this.capacidad}kg. El Backtracking rechazará la ruta.`, "log-poda");
        }

        // Advertencia Volumen
        let volMax = 2.5; 
        if(this.vehiculoSeleccionado === 'Moto') volMax = 0.5;
        if(this.vehiculoSeleccionado === 'Camión') volMax = 6.0;
        
        if (volTotalManual > volMax) {
            this.escribirLog(`⚠️ ADVERTENCIA: Te excediste del límite de ${volMax}m3. El Backtracking rechazará la ruta.`, "log-poda");
        }
    },

    inicializarÁrbolVisual() {
        if (cyInstance) cyInstance.destroy();
        DOM.treePanel.style.display = 'flex';
        
        cyInstance = cytoscape({
            container: document.getElementById('tree-canvas'),
            boxSelectionEnabled: false, autounselectify: true,
            style: [
                { selector: 'node', style: { 'content': 'data(label)', 'text-valign': 'center', 'color': 'white', 'background-color': '#334155', 'font-size': '10px', 'width': '22px', 'height': '22px', 'border-width': '2px', 'border-color': '#64748b' } },
                { selector: 'edge', style: { 'width': 2, 'line-color': '#475569', 'target-arrow-color': '#475569', 'target-arrow-shape': 'triangle', 'curve-style': 'bezier' } },
                { selector: '.explorar', style: { 'background-color': '#3b82f6', 'border-color': '#93c5fd', 'width': '25px', 'height': '25px', 'font-weight': 'bold' } },
                { selector: '.poda', style: { 'background-color': '#ef4444', 'border-color': '#fca5a5', 'line-style': 'dashed' } },
                { selector: '.edge-explorar', style: { 'line-color': '#3b82f6', 'target-arrow-color': '#3b82f6', 'width': 3 } },
                { selector: '.edge-poda', style: { 'line-color': '#ef4444', 'target-arrow-color': '#ef4444', 'width': 3, 'line-style': 'dashed' } },
                { selector: '.nueva_mejor', style: { 'background-color': '#10b981', 'border-color': '#6ee7b7', 'font-weight': 'bold' } },
                { selector: '.edge-nueva_mejor', style: { 'line-color': '#10b981', 'target-arrow-color': '#10b981', 'width': 4 } }
            ],
            layout: { name: 'preset' } 
        });
    },

    async cargarNodosIniciales() {
        try {
            const req = await fetch('http://127.0.0.1:5000/api/nodos');
            this.nodosBase = await req.json();
            this.dibujarNodosClickables(this.nodosBase);
            this.llenarTablaPaquetes(this.nodosBase, []); 
        } catch(e) {
            this.escribirLog("⚠️ Backend desconectado. Revisa Python.", "log-poda");
        }
    },

    llenarTablaPaquetes(nodos, idsSeleccionados) {
        DOM.tablaBody.innerHTML = '';
        let count = 0;
        nodos.forEach(n => {
            if(n.id === 0) return;
            const seleccionado = idsSeleccionados.includes(n.id);
            if(seleccionado) count++;
            
            const tr = document.createElement('tr');
            if(seleccionado) tr.className = 'selected';
            
            tr.style.cursor = this.modo === 'manual' ? 'pointer' : 'default';
            tr.onclick = () => {
                if (this.modo === 'manual') this.toggleNodo(n);
                else this.escribirLog("⚠️ Cambia a 'Modo Manual' arriba para seleccionar.", "log-warning");
            };
            
            tr.innerHTML = `
                <td><input type="checkbox" ${seleccionado ? 'checked' : ''} style="pointer-events: none;"></td>
                <td>${n.id}</td>
                <td><b>${n.cliente}</b></td>
                <td>${n.nombre}</td>
                <td>${n.peso_kg}</td>
                <td>${n.volumen}</td>
                <td class="pri-${n.prioridad_txt}">${n.prioridad_txt}</td>
            `;
            DOM.tablaBody.appendChild(tr);
        });
        DOM.lblSeleccionados.innerText = `${count} paquetes asignados`;
    },

    dibujarNodosClickables(nodosA_Dibujar) {
        layerMarcadores.clearLayers();
        nodosA_Dibujar.forEach(n => {
            const esBodega = n.id === 0;
            const seleccionadoManual = this.modo === 'manual' && this.ids_manuales.includes(n.id);
            let color = esBodega ? '#f59e0b' : (seleccionadoManual ? '#10b981' : '#3b82f6');
            
            let popupText = esBodega ? `<b>${n.nombre}</b>` : `<b>${n.cliente}</b><br>${n.nombre}<br>Peso: ${n.peso_kg} kg | Pri: ${n.prioridad_txt}`;
            if(this.modo === 'manual' && !esBodega) popupText += `<br><i>(Clic para seleccionar)</i>`;

            const marker = L.circleMarker([n.lat, n.lon], { radius: esBodega ? 9 : (seleccionadoManual ? 8 : 6), color: color, fillColor: color, fillOpacity: 1 })
                .bindTooltip(popupText)
                .addTo(layerMarcadores);
            
            if(!esBodega) marker.on('click', () => this.toggleNodo(n));
        });
    },

    cambiarEstadoBotones(jugando) {
        DOM.btnStart.innerText = jugando ? "🔄 Reiniciar Simulación" : "🎯 Optimizar Ruta";
        DOM.btnPause.disabled = !jugando || this.isPaused;
        DOM.btnResume.disabled = !this.isPaused;
    },

    limpiarTodo() {
        if(this.timeoutId) clearTimeout(this.timeoutId);
        this.isPaused = false;
        this.ids_manuales = [];
        this.stats = { nodos: 0, podas: 0, mejoras: 0 };
        DOM.statNodos.innerText = "0"; DOM.statPoda.innerText = "0"; DOM.statMejoras.innerText = "0";
        layerRutas.clearLayers();
        this.dibujarNodosClickables(this.nodosBase);
        this.llenarTablaPaquetes(this.nodosBase, []);
        if (cyInstance) cyInstance.elements().remove();
        
        DOM.lblOptima.innerText = "--"; DOM.lblTiempo.innerText = "--";
        DOM.dashPaquetes.innerText = "0"; DOM.dashPeso.innerText = "0"; DOM.dashVolumen.innerText = "0";
        document.getElementById('btnExportar').style.display = 'none';
        DOM.panelRuta.style.display = 'none';
        DOM.treePanel.style.display = 'none';
        DOM.log.innerHTML = '';
        this.escribirLog("Sistema reseteado.", "log-info");
        this.cambiarEstadoBotones(false);
    },

    exportarHojaRuta() {
        if (!this.optima) return;
        let contenido = "🚚 HOJA DE RUTA - OPTIRUTA+ 🚚\n========================================\n\n";
        contenido += `Vehículo: ${this.vehiculoSeleccionado.toUpperCase()}\nDistancia Total: ${this.optima.distancia} km\n`;
        contenido += `Tiempo Estimado de Conducción: ${document.getElementById('lblTiempo').innerText} min\n\n`;
        contenido += "ORDEN DE ENTREGAS:\n----------------------------------------\n";
        
        this.optima.ruta.forEach((idEnArreglo, index) => {
            const infoNodo = this.nodos_rutear[idEnArreglo];
            if(infoNodo) {
                if(infoNodo.id === 0) contenido += `${index + 1}. [BASE] - ${infoNodo.nombre}\n`;
                else contenido += `${index + 1}. [ENTREGA] - ${infoNodo.cliente} -> ${infoNodo.nombre} (${infoNodo.prioridad_txt})\n`;
            }
        });
        const blob = new Blob([contenido], { type: "text/plain" });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url; a.download = "Hoja_de_Ruta.txt"; a.click();
        window.URL.revokeObjectURL(url);
    },

    mostrarOrdenRuta(nodos_rutear, indices_ruta) {
        DOM.listaRuta.innerHTML = ''; 
        indices_ruta.forEach((idEnArreglo, index) => {
            const infoLugar = nodos_rutear[idEnArreglo];
            const li = document.createElement('li');
            if (index === 0 || index === indices_ruta.length - 1) {
                li.innerHTML = `<b style="color: var(--warning);">🏠 ${infoLugar.nombre}</b>`;
            } else {
                li.innerHTML = `<div style="display:flex; justify-content:space-between;"><b style="color: #60a5fa;">${infoLugar.cliente}</b><span class="pri-${infoLugar.prioridad_txt}" style="font-size:11px;">${infoLugar.prioridad_txt}</span></div><span style="color:#94a3b8; font-size:11px;">${infoLugar.nombre}</span>`;
            }
            DOM.listaRuta.appendChild(li);
        });
        DOM.panelRuta.style.display = 'block'; 
    },

    async iniciarCalculo() {
        if(this.modo === 'manual' && this.ids_manuales.length === 0) {
            alert("En modo manual, debes hacer clic en al menos 1 cliente en el mapa o en la tabla.");
            return;
        }

        if(this.timeoutId) clearTimeout(this.timeoutId);
        layerRutas.clearLayers();
        DOM.panelRuta.style.display = 'none';
        document.getElementById('btnExportar').style.display = 'none';

        this.stats = { nodos: 0, podas: 0, mejoras: 0 };
        DOM.statNodos.innerText = "0"; DOM.statPoda.innerText = "0"; DOM.statMejoras.innerText = "0";

        this.inicializarÁrbolVisual();
        this.escribirLog("Enviando datos al pipeline logístico...", "log-info");

        try {
            const req = await fetch('http://127.0.0.1:5000/api/simular', {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    capacidad: this.capacidad, 
                    capacidad_volumen: 2.5, 
                    modo: this.modo, 
                    nodos_manuales: this.ids_manuales 
                })
            });
            const data = await req.json();
            
            DOM.dashPaquetes.innerText = data.totales.paquetes;
            DOM.dashPeso.innerText = data.totales.peso_kg;
            DOM.dashVolumen.innerText = data.totales.volumen_m3;
            
            if(this.modo === 'auto') {
                this.llenarTablaPaquetes(this.nodosBase, data.ids_seleccionados);
                this.ids_manuales = data.ids_seleccionados;
            }

            this.nodos_rutear = data.nodos_rutear;
            this.dibujarNodosClickables(this.nodosBase); 

            this.historial = data.historial; this.optima = data.optima; this.indice = 0; this.isPaused = false;
            this.cambiarEstadoBotones(true);
            this.animarBacktracking(this.nodos_rutear);

        } catch (e) {
            this.escribirLog("Error: El backend no responde.", "log-poda");
        }
    },

    pausarSimulacion() { this.isPaused = true; if(this.timeoutId) clearTimeout(this.timeoutId); this.cambiarEstadoBotones(true); },
    reanudarSimulacion() { this.isPaused = false; this.cambiarEstadoBotones(true); this.animarBacktracking(this.nodos_rutear); },

    trazarRutaRecta(rutaIndices, nodos_rutear, color, grosor) {
        if (rutaIndices.length < 2) return;
        const coords = rutaIndices.map(i => [nodos_rutear[i].lat, nodos_rutear[i].lon]);
        L.polyline(coords, { color: color, weight: grosor, opacity: 0.8 }).addTo(layerRutas);
    },

    async trazarRutaCallejera(rutaIndices, nodos_rutear, color, grosor, esFinal = false) {
        if (rutaIndices.length < 2) return;
        const coordenadas = rutaIndices.map(i => `${nodos_rutear[i].lon},${nodos_rutear[i].lat}`).join(';');
        try {
            const res = await fetch(`https://router.project-osrm.org/route/v1/driving/${coordenadas}?overview=full&geometries=geojson`);
            const data = await res.json();
            if (data.routes && data.routes[0]) {
                L.geoJSON(data.routes[0].geometry, { style: { color: color, weight: grosor, opacity: 0.9 } }).addTo(layerRutas);
                if (esFinal) {
                    const minutos = Math.round(data.routes[0].duration / 60);
                    DOM.lblTiempo.innerText = minutos;
                    document.getElementById('btnExportar').style.display = 'block';
                    this.escribirLog(`⏱️ Tiempo: ${minutos} min.`, 'log-info');
                }
            }
        } catch(e) {
            this.trazarRutaRecta(rutaIndices, nodos_rutear, color, grosor);
        }
    },

    async animarBacktracking(nodos_rutear) {
        if (this.isPaused) return;

        if (this.indice >= this.historial.length) {
            layerRutas.clearLayers();
            await this.trazarRutaCallejera(this.optima.ruta, nodos_rutear, '#10b981', 5, true);
            DOM.lblOptima.innerText = this.optima.distancia;
            this.mostrarOrdenRuta(nodos_rutear, this.optima.ruta);
            this.cambiarEstadoBotones(false);
            if (cyInstance) { cyInstance.layout({ name: 'breadthfirst', directed: true, padding: 10 }).run(); cyInstance.fit(); }
            return;
        }

        const paso = this.historial[this.indice];
        layerRutas.clearLayers();
        
        if(paso.accion === 'explorar') {
            this.stats.nodos++;
            DOM.statNodos.innerText = this.stats.nodos;
            this.trazarRutaRecta(paso.ruta, nodos_rutear, '#3b82f6', 3);
        } else if(paso.accion === 'poda') {
            this.stats.podas++;
            DOM.statPoda.innerText = this.stats.podas;
            this.trazarRutaRecta(paso.ruta, nodos_rutear, '#ef4444', 3);
            this.escribirLog(`Poda a ${paso.distancia}km.`, 'log-poda');
        } else if(paso.accion === 'nueva_mejor') {
            this.stats.mejoras++;
            DOM.statMejoras.innerText = this.stats.mejoras;
            DOM.lblOptima.innerText = paso.distancia;
        }

        if (cyInstance) {
            let currentPathIds = [];
            let edges = [];

            paso.ruta.forEach((mapIndex, depth) => {
                const nodoInfo = nodos_rutear[mapIndex];
                const cyId = (nodoInfo.id === 0) ? 'root' : `d${depth}_n${nodoInfo.id}`;
                const label = (nodoInfo.id === 0) ? 'B' : `N${nodoInfo.id}`;
                currentPathIds.push(cyId);

                if (cyInstance.getElementById(cyId).length === 0) {
                    cyInstance.add({
                        group: 'nodes',
                        data: { id: cyId, label: label, depth: depth },
                        position: { x: depth * 40, y: depth === 0 ? 0 : cyInstance.getElementById(currentPathIds[depth-1]).position('y') + (mapIndex * 5) }
                    });
                }

                if (depth > 0) {
                    const parentId = currentPathIds[depth - 1];
                    const edgeId = `e_${parentId}_${cyId}`;
                    if (cyInstance.getElementById(edgeId).length === 0) {
                        cyInstance.add({ group: 'edges', data: { id: edgeId, source: parentId, target: cyId } });
                    }
                    edges.push(edgeId);
                }
            });

            const lastNodeId = currentPathIds[currentPathIds.length - 1];
            const lastEdgeId = edges.length > 0 ? edges[edges.length - 1] : null;

            if (paso.accion === 'explorar') {
                cyInstance.getElementById(lastNodeId).flashClass('explorar', 100);
                if(lastEdgeId) cyInstance.getElementById(lastEdgeId).flashClass('edge-explorar', 100);
            } else if (paso.accion === 'poda') {
                cyInstance.getElementById(lastNodeId).addClass('poda');
                if(lastEdgeId) cyInstance.getElementById(lastEdgeId).addClass('edge-poda');
            } else if (paso.accion === 'nueva_mejor') {
                currentPathIds.forEach(id => cyInstance.getElementById(id).addClass('nueva_mejor'));
                edges.forEach(id => cyInstance.getElementById(id).addClass('edge-nueva_mejor'));
            }

            if (this.indice % 5 === 0) {
                cyInstance.layout({
                    name: 'breadthfirst', directed: true, padding: 10,
                    transform: (node, pos) => { return node.hasClass('poda') ? { x: pos.x + 20, y: pos.y } : pos; }
                }).run();
            }
            cyInstance.center(cyInstance.getElementById(lastNodeId));
        }

        this.indice++;
        this.timeoutId = setTimeout(() => this.animarBacktracking(nodos_rutear), 60);
    }
};

window.onload = () => App.cargarNodosIniciales();