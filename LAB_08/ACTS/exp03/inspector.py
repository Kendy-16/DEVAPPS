import json
from wsgiref.simple_server import make_server


# Aplicación WSGI
def inspector_entorno_wsgi(environ, start_response):

    # 1. Filtrar únicamente variables que sean texto
    entorno_legible = {}

    for clave, valor in environ.items():
        if isinstance(valor, str):
            entorno_legible[clave] = valor

    # 2. Convertir el diccionario a JSON
    texto_diagnostico = json.dumps(
        entorno_legible,
        indent=4
    )

    # Convertir a bytes
    cuerpo_bytes = texto_diagnostico.encode('utf-8')

    # 3. Preparar la respuesta HTTP
    start_response(
        '200 OK',
        [
            ('Content-Type', 'application/json; charset=utf-8'),
            ('Content-Length', str(len(cuerpo_bytes)))
        ]
    )

    # 4. Retornar el contenido
    return [cuerpo_bytes]


# Crear servidor WSGI
servidor_diagnostico = make_server(
    '127.0.0.1',
    8080,
    inspector_entorno_wsgi
)

print("Servidor WSGI ejecutándose en http://127.0.0.1:8080")
print("Presiona CTRL+C para detenerlo.")

servidor_diagnostico.serve_forever()