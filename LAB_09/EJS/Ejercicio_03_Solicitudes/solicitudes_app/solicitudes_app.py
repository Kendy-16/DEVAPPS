
"""Ejercicio 03 - Laboratorio N.° 09.
Sistema de registro de solicitudes con Reflex.
"""

import re
import reflex as rx

TIPOS = ["Consulta", "Incidencia", "Requerimiento"]

PATRON_CORREO = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


class EstadoSolicitudes(rx.State):
    solicitudes: list[dict[str, str]] = []
    siguiente_id: int = 1
    mensaje_respuesta: str = ""
    exito: bool = False

    nombre_input: str = ""
    correo_input: str = ""
    tipo_input: str = "Consulta"
    descripcion_input: str = ""

    @rx.event
    def actualizar_nombre(self, valor: str):
        self.nombre_input = valor

    @rx.event
    def actualizar_correo(self, valor: str):
        self.correo_input = valor

    @rx.event
    def actualizar_tipo(self, valor: str):
        self.tipo_input = valor

    @rx.event
    def actualizar_descripcion(self, valor: str):
        self.descripcion_input = valor

    @rx.event
    def registrar(self, datos: dict[str, str]):
        nombre = datos.get("nombre", "").strip()
        correo = datos.get("correo", "").strip()
        tipo = datos.get("tipo", "").strip()
        descripcion = datos.get("descripcion", "").strip()

        self.exito = False

        if not nombre:
            self.mensaje_respuesta = (
                "Introduce el nombre del solicitante."
            )
            return

        if not PATRON_CORREO.fullmatch(correo):
            self.mensaje_respuesta = (
                "El correo debe tener un formato válido "
                "(ejemplo@dominio.com)."
            )
            return

        if tipo not in TIPOS:
            self.mensaje_respuesta = (
                "Selecciona un tipo de solicitud válido."
            )
            return

        if len(descripcion) < 10:
            self.mensaje_respuesta = (
                "La descripción debe tener al menos 10 caracteres."
            )
            return

        nuevo = {
            "id": f"SOL-{self.siguiente_id:03d}",
            "nombre": nombre,
            "correo": correo,
            "tipo": tipo,
            "descripcion": descripcion,
        }

        self.solicitudes = [nuevo, *self.solicitudes]
        self.siguiente_id += 1

        self.exito = True
        self.mensaje_respuesta = (
            f"Solicitud registrada correctamente. Gracias, {nombre}."
        )

        # Limpiar los campos después del registro correcto.
        self.nombre_input = ""
        self.correo_input = ""
        self.tipo_input = "Consulta"
        self.descripcion_input = ""

    @rx.event
    def eliminar(self, identificador: str):
        self.solicitudes = [
            solicitud
            for solicitud in self.solicitudes
            if solicitud["id"] != identificador
        ]

        self.exito = True
        self.mensaje_respuesta = (
            "Solicitud eliminada correctamente."
        )

    @rx.var
    def total_solicitudes(self) -> int:
        return len(self.solicitudes)


def campo_etiquetado(etiqueta: str, control):
    return rx.box(
        rx.text(
            etiqueta,
            class_name="input-caption",
        ),
        control,
        class_name="field",
    )


def formulario_solicitud():
    return rx.box(
        rx.text(
            "NUEVO / TICKET",
            class_name="overline",
        ),

        rx.heading(
            "Cuéntanos qué necesitas.",
            size="7",
            class_name="panel-heading",
        ),

        rx.text(
            "Registra consultas, incidencias o requerimientos. "
            "Todos los campos son obligatorios.",
            class_name="form-intro",
        ),

        rx.form(
            rx.box(
                campo_etiquetado(
                    "01 · NOMBRE COMPLETO",
                    rx.input(
                        name="nombre",
                        placeholder="Nombre y apellido",
                        required=True,
                        value=EstadoSolicitudes.nombre_input,
                        on_change=EstadoSolicitudes.actualizar_nombre,
                        class_name="form-input",
                    ),
                ),

                campo_etiquetado(
                    "02 · CORREO ELECTRÓNICO",
                    rx.input(
                        name="correo",
                        type="email",
                        placeholder="ejemplo@correo.com",
                        required=True,
                        value=EstadoSolicitudes.correo_input,
                        on_change=EstadoSolicitudes.actualizar_correo,
                        class_name="form-input",
                    ),
                ),

                campo_etiquetado(
                    "03 · TIPO DE SOLICITUD",
                    rx.select(
                        TIPOS,
                        name="tipo",
                        required=True,
                        value=EstadoSolicitudes.tipo_input,
                        on_change=EstadoSolicitudes.actualizar_tipo,
                        class_name="form-select",
                    ),
                ),

                campo_etiquetado(
                    "04 · DESCRIPCIÓN",
                    rx.text_area(
                        name="descripcion",
                        placeholder=(
                            "Describe la solicitud en al menos "
                            "10 caracteres..."
                        ),
                        required=True,
                        rows="5",
                        min_length=10,
                        value=EstadoSolicitudes.descripcion_input,
                        on_change=EstadoSolicitudes.actualizar_descripcion,
                        class_name="form-input form-textarea",
                    ),
                ),

                rx.button(
                    "Registrar solicitud  ↗",
                    type="submit",
                    class_name="submit-button",
                ),

                class_name="fields-layout",
            ),

            on_submit=EstadoSolicitudes.registrar,
            reset_on_submit=False,
        ),

        rx.cond(
            EstadoSolicitudes.mensaje_respuesta != "",
            rx.box(
                rx.text(
                    EstadoSolicitudes.mensaje_respuesta
                ),
                class_name=rx.cond(
                    EstadoSolicitudes.exito,
                    "notice notice-ok",
                    "notice notice-error",
                ),
            ),
        ),

        class_name="form-panel",
    )


def tarjeta_solicitud(solicitud):
    return rx.box(
        rx.hstack(
            rx.text(
                solicitud["id"],
                class_name="ticket-id",
            ),

            rx.cond(
                solicitud["tipo"] == "Incidencia",

                rx.text(
                    solicitud["tipo"],
                    class_name="ticket-tag tag-incidencia",
                ),

                rx.cond(
                    solicitud["tipo"] == "Consulta",

                    rx.text(
                        solicitud["tipo"],
                        class_name="ticket-tag tag-consulta",
                    ),

                    rx.text(
                        solicitud["tipo"],
                        class_name="ticket-tag tag-requerimiento",
                    ),
                ),
            ),

            align="center",
            justify="between",
            width="100%",
        ),

        rx.heading(
            solicitud["nombre"],
            size="4",
            class_name="ticket-title",
        ),

        rx.text(
            solicitud["correo"],
            class_name="ticket-email",
        ),

        rx.text(
            solicitud["descripcion"],
            class_name="ticket-description",
        ),

        rx.button(
            "Eliminar registro  ×",
            on_click=EstadoSolicitudes.eliminar(
                solicitud["id"]
            ),
            class_name="delete-button",
            variant="ghost",
        ),

        class_name="ticket-card",
    )


def listado_solicitudes():
    return rx.box(
        rx.hstack(
            rx.box(
                rx.text(
                    "REGISTRO / ACTUAL",
                    class_name="overline",
                ),

                rx.heading(
                    "Bandeja de atención",
                    size="6",
                    class_name="panel-heading",
                ),
            ),

            rx.box(
                rx.text(
                    EstadoSolicitudes.total_solicitudes
                ),
                class_name="counter-pill",
            ),

            justify="between",
            align="center",
            width="100%",
        ),

        rx.cond(
            EstadoSolicitudes.total_solicitudes == 0,

            rx.box(
                rx.text(
                    "✳",
                    class_name="empty-symbol",
                ),

                rx.heading(
                    "Todo en orden por aquí",
                    size="5",
                    class_name="empty-heading",
                ),

                rx.text(
                    "Tus solicitudes registradas "
                    "aparecerán en este espacio."
                ),

                class_name="empty-list",
            ),

            rx.box(
                rx.foreach(
                    EstadoSolicitudes.solicitudes,
                    tarjeta_solicitud,
                ),
                class_name="ticket-stack",
            ),
        ),

        class_name="tickets-panel",
    )


def index():
    return rx.box(
        rx.box(
            rx.text(
                "MESA / ABIERTA",
                class_name="brand",
            ),

            rx.text(
                "SERVICIOS UNIVERSITARIOS · 2026",
                class_name="small-stamp",
            ),

            class_name="topbar",
        ),

        rx.box(
            rx.box(
                rx.text(
                    "SOLICITUDES SIN COMPLICACIONES",
                    class_name="overline",
                ),

                rx.heading(
                    "Las buenas respuestas empiezan "
                    "con una solicitud clara.",
                    size="8",
                    class_name="hero-title",
                ),

                rx.text(
                    "Un pequeño centro de atención creado "
                    "con Python y Reflex. Sin base de datos: "
                    "almacenamiento temporal en memoria.",
                    class_name="hero-lead",
                ),

                class_name="hero",
            ),

            rx.box(
                formulario_solicitud(),
                listado_solicitudes(),
                class_name="columns",
            ),

            rx.text(
                "Laboratorio 09 · rx.form() · rx.State · "
                "rx.foreach() · Validación Python",
                class_name="footer-note",
            ),

            class_name="content-shell",
        ),

        class_name="page",
    )


app = rx.App(
    stylesheets=["/estilos.css"]
)

app.add_page(
    index,
    title="Mesa Abierta | Registro de solicitudes",
    description="Laboratorio 09 Reflex - Ejercicio 3",
)
