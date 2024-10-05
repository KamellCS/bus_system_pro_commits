# datos.py – version final
USUARIOS = [
    {"usuario": "admin",    "clave": "admin123",    "rol": "Administrador"},
    {"usuario": "vendedor", "clave": "vendedor123", "rol": "Vendedor"},
]
RUTAS = [
    {"id": 1, "origen": "Lima", "destino": "Ica",     "hora": "08:00", "precio": 45.0, "asientos": 40},
    {"id": 2, "origen": "Lima", "destino": "Huacho",  "hora": "10:00", "precio": 30.0, "asientos": 32},
    {"id": 3, "origen": "Lima", "destino": "Trujillo","hora": "22:00", "precio": 65.0, "asientos": 44},
    {"id": 4, "origen": "Lima", "destino": "Cusco",   "hora": "20:00", "precio": 90.0, "asientos": 40},
]
PASAJEROS = []
_id_ruta = [5]; _id_pasajero = [1]

USO_METODOS = {
    "Burbuja": 0, "Seleccion": 0, "Insercion": 0,
    "Merge Sort": 0, "Quick Sort": 0
}

def registrar_uso_metodo(nombre):
    if nombre in USO_METODOS:
        USO_METODOS[nombre] += 1

def ruta_por_id(ruta_id):
    for r in RUTAS:
        if r["id"] == ruta_id: return r
    return None

def asientos_ocupados(ruta_id, excluir_pasajero_id=None):
    return {p["asiento"] for p in PASAJEROS
            if p["ruta_id"] == ruta_id and p["id"] != excluir_pasajero_id}

def agregar_ruta(origen, destino, hora, precio, asientos):
    r = {"id": _id_ruta[0], "origen": origen, "destino": destino,
         "hora": hora, "precio": float(precio), "asientos": int(asientos)}
    _id_ruta[0] += 1; RUTAS.append(r); return r

def agregar_pasajero(nombre, dni, telefono, ruta_id, asiento, fecha):
    ruta = ruta_por_id(ruta_id)
    if asiento in asientos_ocupados(ruta_id):
        raise ValueError(f"El asiento {asiento} ya esta ocupado.")
    p = {"id": _id_pasajero[0], "nombre": nombre, "dni": dni,
         "telefono": telefono, "ruta_id": ruta_id, "asiento": asiento,
         "fecha": fecha, "precio": ruta["precio"], "destino": ruta["destino"]}
    _id_pasajero[0] += 1; PASAJEROS.append(p); return p

def modificar_pasajero(pasajero_id, nombre, dni, telefono, ruta_id, asiento, fecha):
    ruta = ruta_por_id(ruta_id)
    if not ruta:
        raise ValueError("Ruta no encontrada.")
    ocup = asientos_ocupados(ruta_id, excluir_pasajero_id=pasajero_id)
    if asiento in ocup:
        raise ValueError(f"El asiento {asiento} ya esta ocupado por otro pasajero.")
    for p in PASAJEROS:
        if p["id"] == pasajero_id:
            p["nombre"] = nombre; p["dni"] = dni; p["telefono"] = telefono
            p["ruta_id"] = ruta_id; p["asiento"] = asiento; p["fecha"] = fecha
            p["precio"] = ruta["precio"]; p["destino"] = ruta["destino"]
            return p
    raise ValueError("Pasajero no encontrado.")

def anular_pasajero(pasajero_id):
    for i, p in enumerate(PASAJEROS):
        if p["id"] == pasajero_id:
            PASAJEROS.pop(i); return True
    return False
