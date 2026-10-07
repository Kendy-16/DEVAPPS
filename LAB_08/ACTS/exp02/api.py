import json
from http.server import BaseHTTPRequestHandler, HTTPServer


# Colección almacenada temporalmente en memoria
coleccion_usuarios = [
    {
        "id": 100,
        "nombre": "Linus Torvalds",
        "perfil": "SysAdmin"
    }
]


class EnrutadorAPI(BaseHTTPRequestHandler):

    # Función auxiliar para enviar respuestas JSON
    def emitir_json(self, codigo_http, datos_diccionario):

        payload = json.dumps(datos_diccionario).encode('utf-8')

        self.send_response(codigo_http)
        self.send_header(
            'Content-Type',
            'application/json; charset=utf-8'
        )
        self.send_header(
            'Content-Length',
            str(len(payload))
        )
        self.end_headers()

        self.wfile.write(payload)

    # GET /api/usuarios
    def do_GET(self):

        if self.path == '/api/usuarios':

            self.emitir_json(
                200,
                {
                    "estado": "ok",
                    "total": len(coleccion_usuarios),
                    "datos": coleccion_usuarios
                }
            )

        else:

            self.emitir_json(
                404,
                {
                    "error": "Endpoint no mapeado en la API"
                }
            )

    # POST /api/usuarios
    def do_POST(self):

        if self.path == '/api/usuarios':

            # Leer Content-Length
            longitud = int(
                self.headers.get('Content-Length', 0)
            )

            # Leer exactamente esa cantidad de bytes
            bytes_recibidos = self.rfile.read(longitud)

            try:

                # Convertir JSON recibido a diccionario
                nuevo_registro = json.loads(
                    bytes_recibidos.decode('utf-8')
                )

                # Generar ID automáticamente
                nuevo_registro['id'] = (
                    coleccion_usuarios[-1]['id'] + 1
                    if coleccion_usuarios
                    else 1
                )

                # Guardar en memoria
                coleccion_usuarios.append(nuevo_registro)

                # Responder 201 Created
                self.emitir_json(
                    201,
                    {
                        "estado": "creado",
                        "datos": nuevo_registro
                    }
                )

            except json.JSONDecodeError:

                self.emitir_json(
                    400,
                    {
                        "error": "El cuerpo de la petición debe ser JSON válido."
                    }
                )

        else:

            self.emitir_json(
                404,
                {
                    "error": "Endpoint no mapeado en la API"
                }
            )


servidor = HTTPServer(
    ('localhost', 8001),
    EnrutadorAPI
)

print("API ejecutándose en http://localhost:8001")
print("Presiona CTRL+C para detenerla.")

servidor.serve_forever()