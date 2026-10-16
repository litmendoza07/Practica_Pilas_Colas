from flask import Flask, redirect, render_template, request, url_for

import logic


app = Flask(__name__)


# Reto 1: consultar el siguiente turno sin retirarlo de la cola.
# Reto 5: mostrar estadísticas de las solicitudes.
@app.get("/")
def inicio():
    return render_template(
        "index.html",
        pendientes=logic.cola_pendientes,
        historial=logic.pila_historial,
        siguiente=logic.consultar_siguiente(),
        estadisticas=logic.obtener_estadisticas(),
        mensaje=request.args.get("mensaje", ""),
        resultado_busqueda=None,
        busqueda_realizada=False,
    )


# Reto 5: evitar registrar solicitudes que ya están pendientes.
@app.post("/registrar")
def registrar():
    cliente = request.form.get("cliente", "")
    asunto = request.form.get("asunto", "")

    if logic.solicitud_duplicada(cliente, asunto):
        mensaje = "Esa solicitud ya está pendiente."
    elif logic.registrar_solicitud(cliente, asunto):
        mensaje = "Solicitud registrada."
    else:
        mensaje = "Escribe un cliente y un asunto."

    return redirect(url_for("inicio", mensaje=mensaje))


@app.post("/atender")
def atender():
    solicitud = logic.atender_siguiente()
    mensaje = "Solicitud atendida." if solicitud else "No hay solicitudes pendientes."
    return redirect(url_for("inicio", mensaje=mensaje))


@app.post("/deshacer")
def deshacer():
    solicitud = logic.deshacer_ultima_atencion()
    mensaje = "Atención deshecha." if solicitud else "No hay atenciones para deshacer."
    return redirect(url_for("inicio", mensaje=mensaje))


# Reto 2: buscar una solicitud por ID y mostrar si está pendiente o atendida.
@app.get("/buscar")
def buscar():
    identificador = request.args.get("id", "")
    try:
        identificador = int(identificador)
    except ValueError:
        resultado = None
    else:
        resultado = logic.buscar_solicitud(identificador)

    return render_template(
        "index.html",
        pendientes=logic.cola_pendientes,
        historial=logic.pila_historial,
        siguiente=logic.consultar_siguiente(),
        estadisticas=logic.obtener_estadisticas(),
        mensaje="",
        resultado_busqueda=resultado,
        busqueda_realizada=True,
    )


# Reto 3: cancelar una solicitud pendiente usando una ruta POST.
@app.post("/cancelar/<int:identificador>")
def cancelar(identificador):
    solicitud = logic.cancelar_solicitud(identificador)
    mensaje = "Solicitud cancelada." if solicitud else "No existe ese pendiente."
    return redirect(url_for("inicio", mensaje=mensaje))


# Reto 4: deshacer varias atenciones según una cantidad validada.
@app.post("/deshacer-varias")
def deshacer_varias():
    try:
        cantidad = int(request.form.get("cantidad", ""))
    except ValueError:
        cantidad = 0

    if cantidad < 1:
        mensaje = "Escribe una cantidad entera mayor que cero."
    else:
        restauradas = logic.deshacer_varias_atenciones(cantidad)
        mensaje = f"Se restauraron {restauradas} solicitud(es)."

    return redirect(url_for("inicio", mensaje=mensaje))


if __name__ == "__main__":
    app.run(debug=True)
