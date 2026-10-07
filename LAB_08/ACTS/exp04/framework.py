from wsgiref.simple_server import make_server


# Núcleo del micro-framework
class NúcleoWSGI:

    def __init__(self):
        # Tabla de rutas
        self.mapa_enrutamiento = {}

    # Decorador para registrar endpoints
    def registrar_endpoint(self, ruta_esperada):

        def envoltura_compilacion(funcion_controlador):

            self.mapa_enrutamiento[ruta_esperada] = funcion_controlador

            return funcion_controlador

        return envoltura_compilacion

    # Dispatcher WSGI
    def __call__(self, environ, start_response):

        ruta_solicitada = environ.get(
            'PATH_INFO',
            '/'
        )

        if ruta_solicitada in self.mapa_enrutamiento:

            respuesta_texto = self.mapa_enrutamiento[
                ruta_solicitada
            ](environ)

            estado = '200 OK'

        else:

            respuesta_texto = (
                "Error 404: Endpoint huérfano "
                "o no implementado."
            )

            estado = '404 Not Found'

        payload = respuesta_texto.encode('utf-8')

        start_response(
            estado,
            [
                ('Content-Type', 'text/plain; charset=utf-8'),
                ('Content-Length', str(len(payload)))
            ]
        )

        return [payload]


# Middleware de auditoría
class MiddlewareAuditoria:

    def __init__(self, aplicacion_interior):
        self.aplicacion_interior = aplicacion_interior

    def __call__(self, environ, start_response):

        verbo = environ.get('REQUEST_METHOD')
        uri = environ.get('PATH_INFO')

        print(
            f"[Capa de Seguridad] -> "
            f"Intento de acceso: {verbo} a la ruta {uri}"
        )

        return self.aplicacion_interior(
            environ,
            start_response
        )


# Crear aplicación
app = NúcleoWSGI()


# Registrar endpoint mediante decorador
@app.registrar_endpoint('/saludo')
def vista_saludo(environ):

    return (
        "Micro-Framework funcionando "
        "mediante abstracción declarativa."
    )


# Envolver la aplicación con middleware
aplicacion_fortificada = MiddlewareAuditoria(app)


# Crear servidor WSGI
servidor = make_server(
    '127.0.0.1',
    8081,
    aplicacion_fortificada
)

print("Micro-framework ejecutándose en http://127.0.0.1:8081")
print("Presiona CTRL+C para detenerlo.")

servidor.serve_forever()