
import json
import http.client
from urllib.parse import urlencode

HOST = "127.0.0.1"
PUERTO = 8012

APROBADAS = 0
TOTAL = 0


def probar(nombre, ruta, esperado, verificar=None, metodo="GET"):
    global APROBADAS, TOTAL

    TOTAL += 1

    conexion = http.client.HTTPConnection(
        HOST,
        PUERTO,
        timeout=5
    )

    try:
        conexion.request(metodo, ruta)

        respuesta = conexion.getresponse()
        codigo = respuesta.status
        cuerpo = respuesta.read()
        contenido = None

        content_type = respuesta.getheader("Content-Type", "")

        if content_type.startswith("application/json") and cuerpo:
            contenido = json.loads(cuerpo.decode("utf-8"))

        correcto = codigo == esperado

        if correcto and verificar is not None:
            correcto = bool(verificar(contenido))

        if correcto:
            APROBADAS += 1

        print("=" * 60)
        print("PRUEBA:", nombre)
        print("Código esperado:", esperado)
        print("Código recibido:", codigo)
        print("Resultado:", "APROBADO" if correcto else "FALLIDO")

        if contenido is not None:
            texto = json.dumps(
                contenido,
                ensure_ascii=False,
                indent=2
            )
            print(texto[:1200])

    except Exception as error:
        print("=" * 60)
        print("PRUEBA:", nombre)
        print("Resultado: FALLIDO")
        print("Detalle:", error)

    finally:
        conexion.close()


if __name__ == "__main__":

    probar(
        "01 - Interfaz HTML",
        "/",
        200
    )

    probar(
        "02 - Archivo CSS",
        "/public/styles.css",
        200
    )

    probar(
        "03 - Archivo JavaScript",
        "/public/script.js",
        200
    )

    probar(
        "04 - Consulta general de inventario",
        "/api/inventario",
        200,
        lambda d: d["metadatos"]["total_registros"] == 250
    )

    probar(
        "05 - Paginación con límite 5",
        "/api/inventario?limite=5&pagina=2",
        200,
        lambda d: (
            len(d["datos"]) == 5
            and d["datos"][0]["id"] == 6
        )
    )

    probar(
        "06 - Hard limit de 100 registros",
        "/api/inventario?limite=500",
        200,
        lambda d: (
            d["metadatos"]["limite"] == 100
            and len(d["datos"]) == 100
        )
    )

    probar(
        "07 - Búsqueda parcial por nombre",
        "/api/inventario?filtro=Laptop",
        200,
        lambda d: d["metadatos"]["total_registros"] == 50
    )

    ruta_busqueda = "/api/inventario?" + urlencode({
        "filtro": "Disco SSD",
        "limite": 10
    })

    probar(
        "08 - Búsqueda con espacios",
        ruta_busqueda,
        200,
        lambda d: d["metadatos"]["total_registros"] == 50
    )

    probar(
        "09 - Búsqueda sin coincidencias",
        "/api/inventario?filtro=Inexistente",
        200,
        lambda d: len(d["datos"]) == 0
    )

    probar(
        "10 - Página no numérica",
        "/api/inventario?pagina=abc",
        400
    )

    probar(
        "11 - Límite no numérico",
        "/api/inventario?limite=cinco",
        400
    )

    probar(
        "12 - Límite cero",
        "/api/inventario?limite=0",
        400
    )

    probar(
        "13 - Página negativa",
        "/api/inventario?pagina=-2",
        400
    )

    probar(
        "14 - Parámetro duplicado",
        "/api/inventario?pagina=1&pagina=2",
        400
    )

    probar(
        "15 - Parámetro desconocido",
        "/api/inventario?orden=desc",
        400
    )

    probar(
        "16 - Path Traversal con ../",
        "/public/../../main.py",
        403
    )

    probar(
        "17 - Path Traversal codificado",
        "/public/%2e%2e/%2e%2e/main.py",
        403
    )

    probar(
        "18 - Archivo inexistente",
        "/public/no_existe.html",
        404
    )

    probar(
        "19 - Endpoint inexistente",
        "/api/usuarios",
        404
    )

    probar(
        "20 - Método POST rechazado",
        "/api/inventario",
        405,
        metodo="POST"
    )

    probar(
        "21 - Cabeceras HEAD",
        "/public/index.html",
        200,
        metodo="HEAD"
    )

    probar(
        "22 - Búsqueda sin distinguir mayúsculas",
        "/api/inventario?filtro=lApToP",
        200,
        lambda d: d["metadatos"]["total_registros"] == 50
    )

    print()
    print("=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    print(f"Pruebas aprobadas: {APROBADAS}/{TOTAL}")

    if APROBADAS == TOTAL:
        print("RESULTADO FINAL: TODAS LAS PRUEBAS APROBADAS")
    else:
        print("RESULTADO FINAL: EXISTEN PRUEBAS FALLIDAS")

    print("=" * 60)
