import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logic
from app import app


def reiniciar():
    logic.cola_pendientes.clear()
    logic.pila_historial.clear()
    logic.siguiente_id = 1


reiniciar()
app.config["TESTING"] = True
cliente = app.test_client()

respuesta = cliente.get("/")
assert respuesta.status_code == 200

respuesta = cliente.post(
    "/registrar", data={"cliente": "Ana", "asunto": "Wi-Fi"}, follow_redirects=True
)
assert respuesta.status_code == 200
assert b"Solicitud registrada." in respuesta.data
assert logic.cola_pendientes[0]["id"] == 1

respuesta = cliente.post(
    "/registrar", data={"cliente": "Ana", "asunto": "Wi-Fi"}, follow_redirects=True
)
assert b"ya est\xc3\xa1 pendiente" in respuesta.data
assert len(logic.cola_pendientes) == 1

respuesta = cliente.get("/buscar?id=1")
assert b"pendiente" in respuesta.data
assert cliente.get("/buscar?id=no-es-numero").status_code == 200
assert cliente.get("/buscar?id=99").status_code == 200

cliente.post("/atender")
assert logic.buscar_solicitud(1)["estado"] == "atendida"
cliente.post("/deshacer")
assert logic.consultar_siguiente()["id"] == 1

cliente.post("/registrar", data={"cliente": "Luis", "asunto": "Impresora"})
respuesta = cliente.post(
    "/cancelar/2", follow_redirects=True
)
assert b"Solicitud cancelada." in respuesta.data
assert logic.buscar_solicitud(2) is None

cliente.post("/atender")
assert cliente.post(
    "/deshacer-varias", data={"cantidad": "no-numero"}, follow_redirects=True
).status_code == 200
assert cliente.post(
    "/deshacer-varias", data={"cantidad": "3"}, follow_redirects=True
).status_code == 200
assert [item["id"] for item in logic.cola_pendientes] == [1]

cliente.post("/atender")
cliente.post("/atender")
cliente.post("/deshacer")
assert logic.deshacer_ultima_atencion() is None

print("Todas las pruebas de las rutas Flask terminaron correctamente.")
