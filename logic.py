cola_pendientes = []
pila_historial = []
siguiente_id = 1


def solicitud_duplicada(cliente, asunto):
    cliente = cliente.strip().lower()
    asunto = asunto.strip().lower()

    for solicitud in cola_pendientes:
        if (
            solicitud["cliente"].lower() == cliente
            and solicitud["asunto"].lower() == asunto
        ):
            return solicitud

    return None


def registrar_solicitud(cliente, asunto):
    global siguiente_id

    if not isinstance(cliente, str) or not isinstance(asunto, str):
        return None

    cliente = cliente.strip()
    asunto = asunto.strip()

    if not cliente or not asunto or solicitud_duplicada(cliente, asunto):
        return None

    solicitud = {
        "id": siguiente_id,
        "cliente": cliente,
        "asunto": asunto,
        "estado": "pendiente",
    }
    cola_pendientes.append(solicitud)
    siguiente_id += 1
    return solicitud


def atender_siguiente():
    if not cola_pendientes:
        return None

    solicitud = cola_pendientes.pop(0)
    solicitud["estado"] = "atendida"
    pila_historial.append(solicitud)
    return solicitud


def deshacer_ultima_atencion():
    if not pila_historial:
        return None

    solicitud = pila_historial.pop()
    solicitud["estado"] = "pendiente"
    cola_pendientes.insert(0, solicitud)
    return solicitud


def consultar_siguiente():
    if not cola_pendientes:
        return None

    return cola_pendientes[0]


def buscar_solicitud(identificador):
    for solicitud in cola_pendientes:
        if solicitud["id"] == identificador:
            return solicitud

    for solicitud in pila_historial:
        if solicitud["id"] == identificador:
            return solicitud

    return None


def cancelar_solicitud(identificador):
    for posicion in range(len(cola_pendientes)):
        if cola_pendientes[posicion]["id"] == identificador:
            solicitud = cola_pendientes.pop(posicion)
            solicitud["estado"] = "cancelada"
            return solicitud

    return None


def deshacer_varias_atenciones(cantidad):
    if not isinstance(cantidad, int) or cantidad < 1:
        return 0

    restauradas = 0
    while restauradas < cantidad and pila_historial:
        deshacer_ultima_atencion()
        restauradas += 1

    return restauradas


def obtener_estadisticas():
    return {
        "total_registradas": siguiente_id - 1,
        "pendientes": len(cola_pendientes),
        "atendidas": len(pila_historial),
    }
