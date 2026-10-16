# Gestor de solicitudes: pilas y colas

Práctica educativa de Python para administrar solicitudes de soporte. La lógica
principal usa listas, diccionarios, funciones, ciclos y condicionales; no usa
clases, base de datos ni bibliotecas de pilas o colas.

## Consola

Ejecuta desde la carpeta del proyecto:

```text
python app_console.py
```

El menú permite registrar, atender y deshacer atenciones, consultar el siguiente
turno, buscar o cancelar solicitudes y ver estadísticas.

## Pruebas de la lógica

No necesitan instalar paquetes:

```text
python tests/probar_logica.py
```

## Aplicación web opcional con Flask

Flask es la única dependencia externa. En Windows puedes instalarla y ejecutar
la aplicación así:

```text
python -m pip install -r requirements.txt
python app.py
```

Abre `http://127.0.0.1:5000` en el navegador. La página usa Bootstrap desde una
hoja de estilos CDN. La información se conserva solo mientras el servidor está
encendido; es una versión local de aprendizaje, no para producción.

La cola atiende primero la solicitud más antigua (FIFO). El historial funciona
como pila (LIFO): deshacer recupera la última solicitud atendida y la coloca al
inicio de la cola para conservar su prioridad original.

## Reflexión

En esta práctica, `pop(0)` y `insert(0, ...)` pueden desplazar los demás
elementos de una lista, por lo que cuestan O(n) cuando la lista crece.
`collections.deque` permite sacar y agregar elementos en los extremos en O(1),
y sería una mejora adecuada para una cola grande. Aquí se conservan las listas
para practicar las estructuras solicitadas.

Una cola FIFO común no adelanta solicitudes urgentes: solo respeta el orden de
llegada. Para manejar prioridades habría que registrar ese nivel y elegir
primero entre las solicitudes urgentes (por ejemplo, con una cola de prioridad),
definiendo también qué hacer con las solicitudes de igual prioridad.
