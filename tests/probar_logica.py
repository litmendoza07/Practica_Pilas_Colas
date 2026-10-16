import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logic


def reiniciar():
    logic.cola_pendientes.clear()
    logic.pila_historial.clear()
    logic.siguiente_id = 1


def probar_registro_y_validacion():
    reiniciar()
    ana = logic.registrar_solicitud(" Ana ", " Wi-Fi ")
    luis = logic.registrar_solicitud("Luis", "Impresora")

    assert ana["id"] == 1
    assert ana["cliente"] == "Ana"
    assert luis["id"] == 2
    assert logic.registrar_solicitud("", "Asunto") is None
    assert logic.registrar_solicitud("Ana", "Wi-Fi") is None
    assert [item["id"] for item in logic.cola_pendientes] == [1, 2]
    print("OK: registro, IDs consecutivos, campos vacíos y duplicados")


def probar_atender_y_deshacer():
    reiniciar()
    logic.registrar_solicitud("Ana", "A")
    logic.registrar_solicitud("Luis", "B")
    logic.registrar_solicitud("Sofía", "C")

    assert logic.atender_siguiente()["cliente"] == "Ana"
    assert logic.atender_siguiente()["cliente"] == "Luis"
    assert [item["cliente"] for item in logic.cola_pendientes] == ["Sofía"]
    assert logic.deshacer_ultima_atencion()["cliente"] == "Luis"
    assert [item["cliente"] for item in logic.cola_pendientes] == ["Luis", "Sofía"]
    assert logic.deshacer_ultima_atencion()["cliente"] == "Ana"
    assert [item["cliente"] for item in logic.cola_pendientes] == [
        "Ana", "Luis", "Sofía"
    ]
    assert logic.atender_siguiente()["cliente"] == "Ana"
    print("OK: orden FIFO y restauración en el orden original")


def probar_casos_vacios():
    reiniciar()
    assert logic.atender_siguiente() is None
    assert logic.deshacer_ultima_atencion() is None
    assert logic.consultar_siguiente() is None
    assert logic.buscar_solicitud(100) is None
    assert logic.cancelar_solicitud(100) is None
    assert logic.deshacer_varias_atenciones(2) == 0
    print("OK: operaciones con cola e historial vacíos")


def probar_retos():
    reiniciar()
    ana = logic.registrar_solicitud("Ana", "A")
    logic.registrar_solicitud("Luis", "B")
    largo = len(logic.cola_pendientes)
    assert logic.consultar_siguiente()["id"] == ana["id"]
    assert logic.consultar_siguiente()["id"] == ana["id"]
    assert len(logic.cola_pendientes) == largo
    assert logic.buscar_solicitud(2)["estado"] == "pendiente"
    assert logic.cancelar_solicitud(2)["estado"] == "cancelada"
    assert logic.buscar_solicitud(2) is None

    logic.atender_siguiente()
    logic.registrar_solicitud("Sofía", "C")
    logic.atender_siguiente()
    assert logic.deshacer_varias_atenciones(4) == 2
    assert [item["cliente"] for item in logic.cola_pendientes] == ["Ana", "Sofía"]
    assert logic.deshacer_varias_atenciones(0) == 0

    estadisticas = logic.obtener_estadisticas()
    assert estadisticas == {
        "total_registradas": 3,
        "pendientes": 2,
        "atendidas": 0,
    }
    print("OK: consulta, búsqueda, cancelación, varios deshacer y estadísticas")


probar_registro_y_validacion()
probar_atender_y_deshacer()
probar_casos_vacios()
probar_retos()
print("Todas las pruebas terminaron correctamente.")
