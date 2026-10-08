
import json
import urllib.request
import urllib.error
from urllib.parse import urlencode


URL = "http://127.0.0.1:8011/api/inscripciones"
TOKEN = "Bearer TOKEN_SECRETO_2026"

datos_validos = {
    "dni": "76543210",
    "correo_electronico": "alumno@ucsm.edu.pe",
    "programa_academico": "Ingenieria de Sistemas"
}


def ejecutar_prueba(nombre, metodo="POST", datos=None,
                   token=TOKEN, tipo="application/json",
                   ruta=URL, esperado=201):

    cuerpo = None

    if datos is not None:
        if tipo == "application/x-www-form-urlencoded":
            cuerpo = urlencode(datos).encode("utf-8")
        elif tipo == "application/json":
            cuerpo = json.dumps(datos).encode("utf-8")
        else:
            cuerpo = b"datos de prueba"

    cabeceras = {
        "Content-Type": tipo
    }

    if token is not None:
        cabeceras["Authorization"] = token

    peticion = urllib.request.Request(
        ruta,
        data=cuerpo,
        headers=cabeceras,
        method=metodo
    )

    try:
        with urllib.request.urlopen(peticion, timeout=5) as respuesta:
            codigo = respuesta.status
            contenido = json.loads(
                respuesta.read().decode("utf-8")
            )

    except urllib.error.HTTPError as error:
        codigo = error.code
        contenido = json.loads(
            error.read().decode("utf-8")
        )

    excepto = codigo == esperado

    print("\n" + "=" * 60)
    print("PRUEBA:", nombre)
    print("Código esperado:", esperado)
    print("Código recibido:", codigo)
    print("Resultado:", "APROBADO" if excepto else "FALLIDO")
    print(json.dumps(contenido, indent=4, ensure_ascii=False))

    return excepto


if __name__ == "__main__":

    resultados = []

    # 1. Registro correcto mediante JSON.
    resultados.append(ejecutar_prueba(
        "Inscripción JSON válida",
        datos=datos_validos,
        esperado=201
    ))

    # 2. Registro correcto mediante formulario.
    resultados.append(ejecutar_prueba(
        "Inscripción formulario válida",
        datos=datos_validos,
        tipo="application/x-www-form-urlencoded",
        esperado=201
    ))

    # 3. Token ausente.
    resultados.append(ejecutar_prueba(
        "Acceso sin token",
        datos=datos_validos,
        token=None,
        esperado=401
    ))

    # 4. Token incorrecto.
    resultados.append(ejecutar_prueba(
        "Token incorrecto",
        datos=datos_validos,
        token="Bearer TOKEN_INCORRECTO",
        esperado=401
    ))

    # 5. Método no permitido.
    resultados.append(ejecutar_prueba(
        "Método GET rechazado",
        metodo="GET",
        esperado=405
    ))

    # 6. Endpoint inexistente.
    resultados.append(ejecutar_prueba(
        "Ruta inexistente",
        metodo="GET",
        ruta="http://127.0.0.1:8011/api/otra-ruta",
        esperado=404
    ))

    # 7. Campo obligatorio ausente.
    resultados.append(ejecutar_prueba(
        "Falta programa académico",
        datos={
            "dni": "76543210",
            "correo_electronico": "alumno@ucsm.edu.pe"
        },
        esperado=400
    ))

    # 8. DNI incorrecto.
    resultados.append(ejecutar_prueba(
        "DNI inválido",
        datos={
            **datos_validos,
            "dni": "123"
        },
        esperado=400
    ))

    # 9. Correo incorrecto.
    resultados.append(ejecutar_prueba(
        "Correo electrónico inválido",
        datos={
            **datos_validos,
            "correo_electronico": "correo-invalido"
        },
        esperado=400
    ))

    # 10. Campo vacío.
    resultados.append(ejecutar_prueba(
        "Programa académico vacío",
        datos={
            **datos_validos,
            "programa_academico": ""
        },
        esperado=400
    ))

    # 11. Formato no soportado.
    resultados.append(ejecutar_prueba(
        "Formato no soportado",
        datos={"contenido": "prueba"},
        tipo="text/plain",
        esperado=415
    ))

    # 12. Cuerpo vacío.
    resultados.append(ejecutar_prueba(
        "Petición sin payload",
        datos=None,
        esperado=400
    ))

    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)

    aprobadas = sum(resultados)

    print(f"Pruebas aprobadas: {aprobadas}/{len(resultados)}")

    if all(resultados):
        print("RESULTADO FINAL: TODAS LAS PRUEBAS APROBADAS")
    else:
        print("RESULTADO FINAL: EXISTEN PRUEBAS FALLIDAS")
