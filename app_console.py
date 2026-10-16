cola_pendientes = []
pila_historial = []
siguiente_id = 1


def mostrar_estado():
    print("\nPendientes:", cola_pendientes)
    print("Historial:", pila_historial)


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


def ejecutar_menu():
    while True:
        print("\nGestor de solicitudes")
        print("1. Registrar solicitud")
        print("2. Atender siguiente")
        print("3. Deshacer última atención")
        print("4. Mostrar estado")
        print("5. Salir")
        print("6. Consultar siguiente sin atender")
        print("7. Buscar solicitud por ID")
        print("8. Cancelar solicitud pendiente")
        print("9. Deshacer varias atenciones")
        print("10. Mostrar estadísticas")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            cliente = input("Cliente: ")
            asunto = input("Asunto: ")
            if solicitud_duplicada(cliente, asunto):
                print("Esa solicitud ya está pendiente.")
            else:
                resultado = registrar_solicitud(cliente, asunto)
                print("Registrada:", resultado if resultado else "Datos inválidos")
        elif opcion == "2":
            print("Atendida:", atender_siguiente())
        elif opcion == "3":
            print("Restaurada:", deshacer_ultima_atencion())
        elif opcion == "4":
            mostrar_estado()
        elif opcion == "5":
            break
        elif opcion == "6":
            print("Siguiente:", consultar_siguiente())
        elif opcion == "7":
            try:
                identificador = int(input("ID: "))
            except ValueError:
                print("El ID debe ser un número.")
            else:
                print("Solicitud:", buscar_solicitud(identificador))
        elif opcion == "8":
            try:
                identificador = int(input("ID pendiente que desea cancelar: "))
            except ValueError:
                print("El ID debe ser un número.")
            else:
                print("Cancelada:", cancelar_solicitud(identificador))
        elif opcion == "9":
            try:
                cantidad = int(input("Cantidad de atenciones por deshacer: "))
            except ValueError:
                print("La cantidad debe ser un número.")
            else:
                print("Solicitudes restauradas:", deshacer_varias_atenciones(cantidad))
        elif opcion == "10":
            print("Estadísticas:", obtener_estadisticas())
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    ejecutar_menu()
