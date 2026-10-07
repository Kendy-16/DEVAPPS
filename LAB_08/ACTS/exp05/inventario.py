import json
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server


# Simulación de una colección de 100 registros
base_de_datos = [
    {
        "id": i,
        "articulo": f"Item {i}",
        "valor": i * 10
    }
    for i in range(1, 101)
]


def endpoint_inventario_paginado(environ, start_response):

    # 1. Obtener Query String
    cadena_consulta = environ.get(
        'QUERY_STRING',
        ''
    )

    # 2. Convertir Query String en diccionario
    parametros_url = parse_qs(cadena_consulta)

    try:

        # 3. Convertir parámetros a enteros
        limite_elementos = int(
            parametros_url.get(
                'limite',
                ['10']
            )[0]
        )

        pagina_actual = int(
            parametros_url.get(
                'pagina',
                ['1']
            )[0]
        )

    except ValueError:

        estado = '400 Bad Request'

        cuerpo = {
            "error": "Paginación exige numéricos"
        }

    else:

        # 4. Límite máximo indicado en la experiencia
        if limite_elementos > 50:
            limite_elementos = 50

        # Evitar páginas menores a 1
        if pagina_actual < 1:
            pagina_actual = 1

        # 5. Calcular desplazamiento
        indice_desplazamiento = (
            pagina_actual - 1
        ) * limite_elementos

        indice_corte = (
            indice_desplazamiento
            + limite_elementos
        )

        # 6. Obtener registros
        datos_cortados = base_de_datos[
            indice_desplazamiento:indice_corte
        ]

        estado = '200 OK'

        cuerpo = {
            "meta": {
                "pagina": pagina_actual,
                "limite_real": limite_elementos,
                "total_items": len(base_de_datos)
            },
            "registros": datos_cortados
        }

    # Convertir respuesta a JSON
    payload = json.dumps(
        cuerpo
    ).encode('utf-8')

    start_response(
        estado,
        [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(payload)))
        ]
    )

    return [payload]


# Servidor WSGI
servidor = make_server(
    '127.0.0.1',
    8082,
    endpoint_inventario_paginado
)

print("Servidor de inventario ejecutándose en:")
print("http://127.0.0.1:8082/api/inventario")
print("Presiona CTRL+C para detenerlo.")

servidor.serve_forever()