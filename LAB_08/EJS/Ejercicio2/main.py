
import os
import json
import re
import mimetypes
import logging

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlsplit, unquote, parse_qs

HOST = "127.0.0.1"
PUERTO = 8012

DIRECTORIO_BASE = os.path.abspath(os.path.dirname(__file__))
DIRECTORIO_PUBLICO = os.path.abspath(os.path.join(DIRECTORIO_BASE, "public"))
DIRECTORIO_PUBLICO_REAL = os.path.realpath(DIRECTORIO_PUBLICO)

LIMITE_PREDETERMINADO = 10
LIMITE_MAXIMO = 100
MAX_PAGINA = 1_000_000
MAX_FILTRO = 100

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("ServidorHibrido")


def crear_inventario():
    productos_base = [
        ("Mouse Logitech", "Perifericos", 85.00),
        ("Teclado Mecanico", "Perifericos", 190.00),
        ("Monitor Samsung", "Monitores", 750.00),
        ("Disco SSD Kingston", "Almacenamiento", 250.00),
        ("Laptop Lenovo", "Computadoras", 2800.00)
    ]

    inventario = []

    for i in range(1, 251):
        indice = (i - 1) % len(productos_base)
        nombre, categoria, precio = productos_base[indice]

        inventario.append({
            "id": i,
            "nombre": f"{nombre} {i}",
            "categoria": categoria,
            "precio": precio,
            "stock": (i * 7) % 51
        })

    return inventario


INVENTARIO = crear_inventario()


class ErrorHTTP(Exception):
    def __init__(self, codigo, mensaje, detalle=None):
        super().__init__(mensaje)
        self.codigo = codigo
        self.mensaje = mensaje
        self.detalle = detalle


class MotorInventario:
    def __init__(self, registros):
        self.registros = registros

    @staticmethod
    def obtener_entero(parametros, clave, defecto, maximo):
        valor = parametros.get(clave, [str(defecto)])[0]

        if not re.fullmatch(r"[0-9]{1,9}", valor):
            raise ErrorHTTP(
                400,
                "Parámetro numérico inválido",
                f"'{clave}' debe ser un entero positivo."
            )

        numero = int(valor)

        if numero < 1:
            raise ErrorHTTP(
                400,
                "Valor fuera de rango",
                f"'{clave}' debe ser mayor que cero."
            )

        if clave == "limite":
            return min(numero, maximo)

        if numero > maximo:
            raise ErrorHTTP(
                400,
                "Página fuera del rango permitido",
                f"'{clave}' no puede superar {maximo}."
            )

        return numero

    def consultar(self, query_string):
        try:
            parametros = parse_qs(
                query_string,
                keep_blank_values=True,
                strict_parsing=True,
                max_num_fields=20,
                encoding="utf-8",
                errors="strict"
            )
        except (ValueError, UnicodeDecodeError):
            raise ErrorHTTP(
                400,
                "Query String inválida",
                "Los parámetros no tienen un formato válido."
            )

        for clave, valores in parametros.items():
            if len(valores) != 1:
                raise ErrorHTTP(
                    400,
                    "Parámetro duplicado",
                    f"El parámetro '{clave}' está repetido."
                )

        parametros_permitidos = {"pagina", "limite", "filtro"}

        for clave in parametros:
            if clave not in parametros_permitidos:
                raise ErrorHTTP(
                    400,
                    "Parámetro desconocido",
                    f"El parámetro '{clave}' no está permitido."
                )

        limite = self.obtener_entero(
            parametros, "limite", LIMITE_PREDETERMINADO, LIMITE_MAXIMO
        )

        pagina = self.obtener_entero(
            parametros, "pagina", 1, MAX_PAGINA
        )

        filtro = parametros.get("filtro", [""])[0].strip()

        if len(filtro) > MAX_FILTRO:
            raise ErrorHTTP(
                400,
                "Filtro demasiado largo",
                "El filtro admite un máximo de 100 caracteres."
            )

        filtro_normalizado = filtro.casefold()

        resultados = [
            articulo
            for articulo in self.registros
            if (
                filtro_normalizado in articulo["nombre"].casefold()
                or filtro_normalizado in articulo["categoria"].casefold()
            )
        ]

        total = len(resultados)
        desplazamiento = (pagina - 1) * limite
        indice_final = desplazamiento + limite
        articulos_paginados = resultados[desplazamiento:indice_final]
        total_paginas = (total + limite - 1) // limite

        return {
            "estado": "exito",
            "mensaje": "Consulta realizada correctamente",
            "metadatos": {
                "pagina_actual": pagina,
                "limite": limite,
                "limite_maximo": LIMITE_MAXIMO,
                "total_registros": total,
                "total_paginas": total_paginas,
                "registros_mostrados": len(articulos_paginados),
                "filtro_aplicado": filtro,
                "hay_pagina_siguiente": pagina < total_paginas,
                "hay_pagina_anterior": pagina > 1
            },
            "datos": articulos_paginados
        }


class ServidorHibrido(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    timeout = 10

    def enviar_json(self, codigo, datos, cabeceras_extra=None):
        cuerpo = json.dumps(
            datos,
            ensure_ascii=False,
            indent=4
        ).encode("utf-8")

        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Connection", "close")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")

        if cabeceras_extra:
            for clave, valor in cabeceras_extra:
                self.send_header(clave, valor)

        self.end_headers()
        self.close_connection = True

        if self.command != "HEAD":
            self.wfile.write(cuerpo)

    def enviar_error_json(self, codigo, mensaje, detalle=None):
        respuesta = {
            "estado": "error",
            "codigo": codigo,
            "mensaje": mensaje
        }

        if detalle is not None:
            respuesta["detalle"] = detalle

        cabeceras = []

        if codigo == 405:
            cabeceras.append(("Allow", "GET, HEAD"))

        self.enviar_json(codigo, respuesta, cabeceras)

    def procesar_peticion(self):
        try:
            componentes = urlsplit(self.path)
            ruta_cruda = componentes.path
            query_string = componentes.query

            try:
                ruta = unquote(
                    ruta_cruda,
                    encoding="utf-8",
                    errors="strict"
                )
            except UnicodeDecodeError:
                raise ErrorHTTP(400, "Codificación de URL inválida")

            if "\x00" in ruta or "\\" in ruta:
                raise ErrorHTTP(
                    403,
                    "Ruta no permitida",
                    "Se detectaron caracteres peligrosos."
                )

            if ruta == "/api/inventario":
                motor = MotorInventario(INVENTARIO)
                respuesta = motor.consultar(query_string)
                self.enviar_json(200, respuesta)
                return

            if ruta == "/api" or ruta.startswith("/api/"):
                raise ErrorHTTP(
                    404,
                    "Endpoint no encontrado",
                    "El recurso solicitado no existe."
                )

            self.servir_archivo_estatico(ruta)

        except ErrorHTTP as error:
            logger.warning(
                "HTTP %s: %s",
                error.codigo,
                error.mensaje
            )

            self.enviar_error_json(
                error.codigo,
                error.mensaje,
                error.detalle
            )

        except Exception:
            logger.exception("Error interno no controlado")
            self.enviar_error_json(500, "Error interno del servidor")

    def servir_archivo_estatico(self, ruta):
        if ruta == "/":
            ruta_relativa = "index.html"

        elif ruta == "/public":
            ruta_relativa = "index.html"

        elif ruta.startswith("/public/"):
            ruta_relativa = ruta[len("/public/"):]

            if not ruta_relativa:
                ruta_relativa = "index.html"

        else:
            raise ErrorHTTP(
                404,
                "Recurso no encontrado",
                "Solo se permiten archivos de /public."
            )

        ruta_absoluta = os.path.abspath(
            os.path.join(DIRECTORIO_PUBLICO, ruta_relativa)
        )

        try:
            ruta_pertenece = (
                os.path.commonpath([
                    DIRECTORIO_PUBLICO,
                    ruta_absoluta
                ]) == DIRECTORIO_PUBLICO
            )
        except ValueError:
            ruta_pertenece = False

        if not ruta_pertenece:
            raise ErrorHTTP(
                403,
                "Acceso prohibido",
                "Intento de Path Traversal detectado."
            )

        ruta_real = os.path.realpath(ruta_absoluta)

        try:
            ruta_real_permitida = (
                os.path.commonpath([
                    DIRECTORIO_PUBLICO_REAL,
                    ruta_real
                ]) == DIRECTORIO_PUBLICO_REAL
            )
        except ValueError:
            ruta_real_permitida = False

        if not ruta_real_permitida:
            raise ErrorHTTP(
                403,
                "Acceso prohibido",
                "El archivo está fuera del directorio público."
            )

        if not os.path.isfile(ruta_real):
            raise ErrorHTTP(
                404,
                "Archivo no encontrado",
                "El archivo solicitado no existe."
            )

        tipo_mime, _ = mimetypes.guess_type(ruta_real)

        if not tipo_mime:
            tipo_mime = "application/octet-stream"

        if tipo_mime.startswith("text/"):
            tipo_mime += "; charset=utf-8"

        try:
            with open(ruta_real, "rb") as archivo:
                tamanio = os.fstat(archivo.fileno()).st_size

                self.send_response(200)
                self.send_header("Content-Type", tipo_mime)
                self.send_header("Content-Length", str(tamanio))
                self.send_header("Connection", "close")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.end_headers()

                self.close_connection = True

                if self.command == "HEAD":
                    return

                while True:
                    bloque = archivo.read(64 * 1024)

                    if not bloque:
                        break

                    self.wfile.write(bloque)

        except OSError:
            logger.exception("Fallo durante la transmisión del archivo")
            self.close_connection = True

    def do_GET(self):
        self.procesar_peticion()

    def do_HEAD(self):
        self.procesar_peticion()

    def do_POST(self):
        self.enviar_error_json(
            405,
            "Método no permitido",
            "Este servidor solo admite GET y HEAD."
        )
        self.close_connection = True

    def do_PUT(self):
        self.do_POST()

    def do_DELETE(self):
        self.do_POST()

    def do_PATCH(self):
        self.do_POST()

    def log_message(self, formato, *argumentos):
        logger.info(
            "%s - %s",
            self.client_address[0],
            formato % argumentos
        )


def iniciar_servidor():
    if not os.path.isdir(DIRECTORIO_PUBLICO):
        logger.error("No existe la carpeta public.")
        return

    try:
        with ThreadingHTTPServer(
            (HOST, PUERTO),
            ServidorHibrido
        ) as servidor:

            servidor.daemon_threads = True

            print("=" * 65)
            print(" EJERCICIO 02 - SERVIDOR HÍBRIDO HTTP NATIVO")
            print("=" * 65)
            print(f"Servidor: http://{HOST}:{PUERTO}")
            print(f"Interfaz: http://{HOST}:{PUERTO}/")
            print(f"API: http://{HOST}:{PUERTO}/api/inventario")
            print(f"Directorio público: {DIRECTORIO_PUBLICO}")
            print(f"Artículos disponibles: {len(INVENTARIO)}")
            print("Límite máximo: 100 registros")
            print("Seguridad Path Traversal: HABILITADA")
            print("Servidor concurrente: HABILITADO")
            print("=" * 65)
            print("Presione CTRL+C para detener el servidor.")

            servidor.serve_forever()

    except KeyboardInterrupt:
        print("\nServidor detenido correctamente.")

    except OSError as error:
        logger.error("Error al iniciar servidor: %s", error)


if __name__ == "__main__":
    iniciar_servidor()
