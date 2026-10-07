import json
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server


def endpoint_recepcion_estricta(environ, start_response):

    # 1. Control del método HTTP
    metodo = environ.get(
        'REQUEST_METHOD'
    )

    if metodo not in ['POST', 'PUT']:

        start_response(
            '405 Method Not Allowed',
            [
                ('Content-Type', 'application/json')
            ]
        )

        return [
            b'{"error": "Metodo transaccional bloqueado"}'
        ]

    # 2. Obtener Content-Length
    tamano_buffer = int(
        environ.get(
            'CONTENT_LENGTH',
            '0'
        ) or '0'
    )

    # Rechazar cuerpo vacío
    if tamano_buffer == 0:

        start_response(
            '400 Bad Request',
            [
                ('Content-Type', 'application/json')
            ]
        )

        return [
            b'{"error": "Rechazo: Payload vacio (Zero Bytes)"}'
        ]

    # Leer exactamente los bytes indicados
    cuerpo_bytes = environ[
        'wsgi.input'
    ].read(tamano_buffer)

    # Obtener Content-Type
    metadato_formato = environ.get(
        'CONTENT_TYPE',
        ''
    )

    # 3. Deserialización polimórfica

    try:

        if 'application/json' in metadato_formato:

            dto_diccionario = json.loads(
                cuerpo_bytes.decode('utf-8')
            )

        elif 'application/x-www-form-urlencoded' in metadato_formato:

            diccionario_listas = parse_qs(
                cuerpo_bytes.decode('utf-8')
            )

            dto_diccionario = {
                k: v[0]
                for k, v in diccionario_listas.items()
            }

        else:

            start_response(
                '415 Unsupported Media Type',
                [
                    ('Content-Type', 'application/json')
                ]
            )

            return [
                b'{"error": "El servidor exige formatos JSON o URL-Encoded"}'
            ]

    except (
        json.JSONDecodeError,
        ValueError
    ):

        start_response(
            '400 Bad Request',
            [
                ('Content-Type', 'application/json')
            ]
        )

        return [
            b'{"error": "Corrupcion detectada en el formato de transferencia"}'
        ]

    # 4. Validación del esquema

    llaves_obligatorias = {
        'identificador',
        'token_operacion',
        'comando'
    }

    llaves_faltantes = (
        llaves_obligatorias
        - dto_diccionario.keys()
    )

    # 5. Fail-Fast
    if llaves_faltantes:

        start_response(
            '400 Bad Request',
            [
                ('Content-Type', 'application/json')
            ]
        )

        mensaje = json.dumps(
            {
                "error": (
                    "Violación del esquema. "
                    "Faltan propiedades: "
                    f"{list(llaves_faltantes)}"
                )
            }
        )

        return [
            mensaje.encode('utf-8')
        ]

    # 6. Respuesta exitosa

    respuesta_ok = json.dumps(
        {
            "estado": (
                "Payload estandarizado y "
                "auditado exitosamente"
            ),
            "datos": dto_diccionario
        }
    )

    cuerpo_respuesta = respuesta_ok.encode(
        'utf-8'
    )

    start_response(
        '200 OK',
        [
            ('Content-Type', 'application/json'),
            (
                'Content-Length',
                str(len(cuerpo_respuesta))
            )
        ]
    )

    return [
        cuerpo_respuesta
    ]


# Servidor WSGI
servidor = make_server(
    '127.0.0.1',
    8083,
    endpoint_recepcion_estricta
)

print("Servidor de payloads ejecutándose en:")
print("http://127.0.0.1:8083")
print("Presiona CTRL+C para detenerlo.")

servidor.serve_forever()