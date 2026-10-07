import os
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer


class ServidorEstaticoFortificado(BaseHTTPRequestHandler):

    def do_GET(self):

        # 1. Directorio público permitido
        directorio_base = os.getcwd()

        # Elimina el / inicial
        ruta_cruda = self.path.lstrip('/')

        if not ruta_cruda:
            ruta_cruda = 'index.html'

        # 2. Resolución de la ruta
        ruta_resuelta = os.path.abspath(
            os.path.join(directorio_base, ruta_cruda)
        )

        # 3. Validación contra Path Traversal
        if not ruta_resuelta.startswith(directorio_base) or not os.path.isfile(ruta_resuelta):
            self.send_error(
                404,
                "Recurso no encontrado o acceso estrictamente denegado."
            )
            return

        # 4. Determinar tipo MIME
        tipo_mime, _ = mimetypes.guess_type(ruta_resuelta)

        # 5. Leer y transmitir archivo
        try:
            with open(ruta_resuelta, 'rb') as archivo_fisico:
                contenido = archivo_fisico.read()

            self.send_response(200)
            self.send_header(
                'Content-Type',
                tipo_mime or 'application/octet-stream'
            )
            self.send_header(
                'Content-Length',
                str(len(contenido))
            )
            self.end_headers()

            self.wfile.write(contenido)

        except IOError:
            self.send_error(
                500,
                "Error del sistema al intentar acceder al archivo físico."
            )


servidor = HTTPServer(('localhost', 8000), ServidorEstaticoFortificado)

print("Servidor ejecutándose en http://localhost:8000")
print("Presiona CTRL+C para detenerlo.")

servidor.serve_forever()