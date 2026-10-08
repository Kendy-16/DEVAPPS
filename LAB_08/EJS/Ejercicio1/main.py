
import json
import hmac
import re
import logging
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
from http import HTTPStatus

HOST = "127.0.0.1"
PUERTO = 8011

TOKEN_VALIDO = "Bearer TOKEN_SECRETO_2026"

# Máximo permitido: 1 MB por petición.
MAX_PAYLOAD = 1024 * 1024

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("MicroFrameworkWSGI")


# ============================================================
# 1. EXCEPCIONES PERSONALIZADAS
# ============================================================

class ErrorHTTP(Exception):
    """Representa un error HTTP controlado."""

    def __init__(self, codigo, mensaje, detalle=None):
        super().__init__(mensaje)
        self.codigo = codigo
        self.mensaje = mensaje
        self.detalle = detalle


# ============================================================
# 1. MOTOR DE RESPUESTAS HTTP
# ============================================================

def responder_json(start_response, codigo, datos, extras=None):
    """
    Serializa un diccionario a JSON UTF-8.

    Cumple PEP 3333:
    - Invoca start_response.
    - Proporciona cabeceras HTTP.
    - Retorna un iterable de bytes.
    """

    cuerpo = json.dumps(
        datos,
        ensure_ascii=False,
        indent=4
    ).encode("utf-8")

    estado = f"{codigo} {HTTPStatus(codigo).phrase}"

    cabeceras = [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(cuerpo))),
        ("Cache-Control", "no-store"),
        ("X-Content-Type-Options", "nosniff")
    ]

    if extras:
        cabeceras.extend(extras)

    start_response(estado, cabeceras)

    return [cuerpo]


def responder_error(start_response, error):
    """Convierte excepciones controladas a respuestas JSON."""

    datos = {
        "estado": "error",
        "codigo": error.codigo,
        "mensaje": error.mensaje
    }

    if error.detalle is not None:
        datos["detalle"] = error.detalle

    extras = []

    if error.codigo == 405:
        extras.append(("Allow", "POST"))

    return responder_json(
        start_response,
        error.codigo,
        datos,
        extras
    )


# ============================================================
# 2. MICRO-FRAMEWORK WSGI CON DECORADORES
# ============================================================

class MicroFrameworkWSGI:
    """
    Motor de enrutamiento orientado a objetos.

    Utiliza:
    - Patrón Decorador
    - Diccionario Hash para rutas
    - Contrato Callable WSGI
    - Manejo centralizado de errores
    """

    def __init__(self):
        self.rutas = {}

    def registrar_ruta(self, ruta, metodos=None):
        """
        Decorador que registra un controlador.

        Ejemplo:
        @app.registrar_ruta("/api/inscripciones", ["POST"])
        """

        if metodos is None:
            metodos = ["GET"]

        metodos = tuple(m.upper() for m in metodos)

        def decorador(funcion):
            if ruta in self.rutas:
                raise ValueError(f"Ruta duplicada: {ruta}")

            self.rutas[ruta] = {
                "metodos": metodos,
                "controlador": funcion
            }

            return funcion

        return decorador

    def __call__(self, environ, start_response):
        """
        Punto de entrada del contrato PEP 3333.

        environ: diccionario de variables HTTP/CGI.
        start_response: callback para la respuesta.
        """

        metodo = environ.get("REQUEST_METHOD", "GET").upper()
        ruta = environ.get("PATH_INFO", "/")

        logger.info("Petición: %s %s", metodo, ruta)

        try:
            # Verificación del endpoint solicitado.
            if ruta not in self.rutas:
                raise ErrorHTTP(
                    404,
                    "Endpoint no encontrado",
                    f"La ruta '{ruta}' no existe."
                )

            configuracion = self.rutas[ruta]

            # Verificación del método HTTP.
            if metodo not in configuracion["metodos"]:
                raise ErrorHTTP(
                    405,
                    "Método HTTP no permitido",
                    "Este endpoint solamente admite POST."
                )

            # Despacho hacia el controlador registrado.
            controlador = configuracion["controlador"]

            datos, codigo = controlador(environ)

            return responder_json(
                start_response,
                codigo,
                datos
            )

        except ErrorHTTP as error:
            logger.warning(
                "Error controlado: %s - %s",
                error.codigo,
                error.mensaje
            )

            return responder_error(start_response, error)

        except Exception:
            # Se registra la excepción, pero no se expone
            # información sensible al cliente.
            logger.exception("Error interno del servidor")

            return responder_json(
                start_response,
                500,
                {
                    "estado": "error",
                    "codigo": 500,
                    "mensaje": "Error interno del servidor"
                }
            )


# ============================================================
# 3. MIDDLEWARE DE SEGURIDAD POR TOKEN
# ============================================================

class MiddlewareTokenSeguridad:
    """
    Implementa el patrón Cadena de Responsabilidad.

    Intercepta todas las peticiones antes de que
    lleguen al micro-framework principal.
    """

    def __init__(self, aplicacion):
        self.aplicacion = aplicacion

    def __call__(self, environ, start_response):

        token_recibido = environ.get(
            "HTTP_AUTHORIZATION",
            ""
        )

        # Comparación de cadenas evitando diferencias
        # de tiempo dependientes del contenido.
        autorizado = hmac.compare_digest(
            token_recibido.encode("utf-8"),
            TOKEN_VALIDO.encode("utf-8")
        )

        if not autorizado:
            logger.warning(
                "Acceso denegado desde %s",
                environ.get("REMOTE_ADDR", "desconocido")
            )

            # SHORT-CIRCUIT:
            # No se llama a la aplicación principal.
            return responder_json(
                start_response,
                401,
                {
                    "estado": "error",
                    "codigo": 401,
                    "mensaje": "No autorizado",
                    "detalle": "Token ausente o inválido"
                },
                [
                    ("WWW-Authenticate", "Bearer")
                ]
            )

        logger.info("Autenticación correcta")

        # Delegación hacia la siguiente capa WSGI.
        return self.aplicacion(environ, start_response)


# ============================================================
# 4. CONTROL ESTRICTO DE ENTRADA / SALIDA
# ============================================================

def leer_cuerpo_seguro(environ):
    """
    Lee exclusivamente los bytes declarados
    en CONTENT_LENGTH, sin consumir el flujo
    indefinidamente.
    """

    longitud_texto = environ.get("CONTENT_LENGTH", "")

    if not longitud_texto or not longitud_texto.isdecimal():
        raise ErrorHTTP(
            400,
            "Content-Length inválido",
            "Debe especificarse una longitud entera válida."
        )

    longitud = int(longitud_texto)

    if longitud == 0:
        raise ErrorHTTP(
            400,
            "Payload vacío",
            "Debe enviar los datos del aspirante."
        )

    if longitud > MAX_PAYLOAD:
        raise ErrorHTTP(
            413,
            "Payload demasiado grande",
            "Se permite un máximo de 1 MB."
        )

    flujo = environ["wsgi.input"]

    # No se usa read() sin un tamaño explícito.
    cuerpo = flujo.read(longitud)

    if len(cuerpo) != longitud:
        raise ErrorHTTP(
            400,
            "Cuerpo HTTP incompleto",
            "La cantidad de bytes no coincide con Content-Length."
        )

    return cuerpo


# ============================================================
# 5. DESERIALIZADOR POLIMÓRFICO
# ============================================================

def deserializar_payload(environ):
    """
    Acepta:
    - application/json
    - application/x-www-form-urlencoded

    Ambos formatos retornan un diccionario.
    """

    tipo_contenido = environ.get(
        "CONTENT_TYPE",
        ""
    ).split(";", 1)[0].strip().lower()

    tipos_permitidos = (
        "application/json",
        "application/x-www-form-urlencoded"
    )

    if tipo_contenido not in tipos_permitidos:
        raise ErrorHTTP(
            415,
            "Formato no soportado",
            "Solo se admite JSON o x-www-form-urlencoded."
        )

    cuerpo_bytes = leer_cuerpo_seguro(environ)

    try:
        cuerpo_texto = cuerpo_bytes.decode("utf-8")

        # Estrategia A: aplicaciones móviles / API.
        if tipo_contenido == "application/json":
            datos = json.loads(cuerpo_texto)

        # Estrategia B: formularios HTML tradicionales.
        else:
            parametros = parse_qs(
                cuerpo_texto,
                keep_blank_values=True,
                strict_parsing=True,
                max_num_fields=100,
                encoding="utf-8",
                errors="strict"
            )

            # Evita ambigüedades por campos repetidos.
            for clave, valores in parametros.items():
                if len(valores) != 1:
                    raise ErrorHTTP(
                        400,
                        "Parámetro duplicado",
                        f"El campo '{clave}' debe aparecer una sola vez."
                    )

            # Aplanamiento obligatorio de listas.
            datos = {
                k: v[0]
                for k, v in parametros.items()
            }

    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ErrorHTTP(
            400,
            "Payload mal formado",
            "No fue posible deserializar los datos enviados."
        ) from error

    if not isinstance(datos, dict):
        raise ErrorHTTP(
            400,
            "Estructura incorrecta",
            "La carga útil debe representar un objeto JSON."
        )

    return datos


# ============================================================
# 6. VALIDACIÓN ESTRICTA DEL ESQUEMA
# ============================================================

def validar_inscripcion(datos):
    """
    Patrón Fail-Fast.

    Detiene inmediatamente el procesamiento
    cuando encuentra una violación del contrato.
    """

    campos_obligatorios = [
        "dni",
        "correo_electronico",
        "programa_academico"
    ]

    # 1. Validación de campos ausentes.
    for campo in campos_obligatorios:
        if campo not in datos:
            raise ErrorHTTP(
                400,
                "Violación del esquema",
                f"Falta el parámetro obligatorio '{campo}'."
            )

    # 2. Validación de tipos de datos.
    for campo in campos_obligatorios:
        if not isinstance(datos[campo], str):
            raise ErrorHTTP(
                400,
                "Tipo de dato inválido",
                f"El parámetro '{campo}' debe ser texto."
            )

    # 3. Validación de valores vacíos.
    for campo in campos_obligatorios:
        if not datos[campo].strip():
            raise ErrorHTTP(
                400,
                "Campo vacío",
                f"El parámetro '{campo}' no puede estar vacío."
            )

    # 4. Verificar DNI peruano de ocho dígitos.
    if not re.fullmatch(r"[0-9]{8}", datos["dni"]):
        raise ErrorHTTP(
            400,
            "DNI inválido",
            "El DNI debe contener exactamente 8 dígitos."
        )

    # 5. Validación sintáctica básica del correo.
    correo = datos["correo_electronico"]

    patron_correo = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

    if not re.fullmatch(patron_correo, correo):
        raise ErrorHTTP(
            400,
            "Correo electrónico inválido",
            "Debe proporcionar un correo con formato válido."
        )

    # 6. Validación de longitud.
    programa = datos["programa_academico"].strip()

    if len(programa) > 120:
        raise ErrorHTTP(
            400,
            "Programa académico inválido",
            "La longitud máxima es de 120 caracteres."
        )

    return {
        "dni": datos["dni"],
        "correo_electronico": correo.strip(),
        "programa_academico": programa
    }


# ============================================================
# 7. INSTANCIA DEL MICRO-FRAMEWORK
# ============================================================

app = MicroFrameworkWSGI()


# ============================================================
# 8. CONTROLADOR DE INSCRIPCIONES CON DECORADOR
# ============================================================

@app.registrar_ruta(
    "/api/inscripciones",
    metodos=["POST"]
)
def registrar_inscripcion(environ):
    """
    Endpoint exclusivo para la inscripción
    de aspirantes a una institución académica.
    """

    # Etapa 1: deserialización del payload.
    datos = deserializar_payload(environ)

    # Etapa 2: validación Fail-Fast.
    aspirante = validar_inscripcion(datos)

    # Etapa 3: confirmación de recepción y validación.
    # No persiste registros en una base de datos.
    logger.info(
        "Inscripción validada: DNI %s",
        aspirante["dni"]
    )

    respuesta = {
        "estado": "exito",
        "mensaje": "Inscripción recibida y validada correctamente",
        "inscripcion": aspirante
    }

    return respuesta, 201


# ============================================================
# 9. ENSAMBLAJE DE LA CADENA DE RESPONSABILIDAD
# ============================================================

aplicacion_segura = MiddlewareTokenSeguridad(app)


# ============================================================
# 10. INICIO DEL SERVIDOR WSGI
# ============================================================

if __name__ == "__main__":

    print("=" * 65)
    print(" EJERCICIO 01 - MICRO-FRAMEWORK WSGI SEGURO")
    print("=" * 65)
    print(f"Servidor: http://{HOST}:{PUERTO}")
    print("Endpoint: POST /api/inscripciones")
    print("Autorización: Bearer TOKEN_SECRETO_2026")
    print("Formatos: JSON / x-www-form-urlencoded")
    print("Límite del cuerpo: 1 MB")
    print("=" * 65)
    print("Presione CTRL+C para detener el servidor.")

    try:
        with make_server(HOST, PUERTO, aplicacion_segura) as servidor:
            servidor.serve_forever()

    except KeyboardInterrupt:
        print("\nServidor detenido correctamente.")

    except OSError as error:
        logger.error("No se pudo iniciar el servidor: %s", error)
