import reflex as rx
import re
import httpx


# ESTADO DEL CONTADOR
class EstadoContador(rx.State):
    conteo: int = 0

    @rx.event
    def incrementar(self):
        self.conteo += 1

    @rx.event
    def disminuir(self):
        self.conteo -= 1

    @rx.event
    def reiniciar(self):
        self.conteo = 0


# ESTADO DE LAS TAREAS
class EstadoTareas(rx.State):
    tareas: list[str] = [
        "Diseñar interfaz",
        "Crear componentes",
        "Probar aplicación",
    ]

    nueva_tarea: str = ""
    mensaje: str = ""

    @rx.event
    def actualizar_nueva_tarea(self, valor: str):
        self.nueva_tarea = valor

    @rx.event
    def agregar_tarea(self, datos: dict[str, str]):
        tarea = datos.get("tarea", "").strip()

        if not tarea:
            self.mensaje = "Ingrese el nombre de una tarea."
        else:
            self.tareas = self.tareas + [tarea]
            self.nueva_tarea = ""
            self.mensaje = "Tarea agregada correctamente."

    @rx.event
    def eliminar_tarea(self, tarea: str):
        self.tareas = [
            elemento for elemento in self.tareas
            if elemento != tarea
        ]
        self.mensaje = "Tarea eliminada correctamente."


# ESTADO DEL FORMULARIO DE CONTACTO
class EstadoContacto(rx.State):
    mensaje_estado: str = ""
    es_error: bool = False

    @rx.event
    def enviar(self, datos: dict[str, str]):
        nombre = datos.get("nombre", "").strip()
        correo = datos.get("correo", "").strip()
        mensaje = datos.get("mensaje", "").strip()

        if not nombre:
            self.mensaje_estado = (
                "Error: el nombre no puede estar vacío."
            )
            self.es_error = True
            return

        patron_correo = r"^[\w.%+-]+@[\w\.-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(patron_correo, correo):
            self.mensaje_estado = (
                "Error: ingrese un correo válido, "
                "por ejemplo usuario@correo.com."
            )
            self.es_error = True
            return

        if not mensaje:
            self.mensaje_estado = (
                "Error: el mensaje no puede estar vacío."
            )
            self.es_error = True
            return

        if len(mensaje) < 10:
            self.mensaje_estado = (
                "Error: el mensaje debe tener "
                "como mínimo 10 caracteres."
            )
            self.es_error = True
            return

        self.mensaje_estado = (
            f"Formulario enviado correctamente. ¡Gracias, {nombre}!"
        )
        self.es_error = False


# ESTADO DE LOS USUARIOS DE LA API
class EstadoUsuarios(rx.State):
    usuarios: list[dict[str, str]] = []
    cargando: bool = False
    error: str = ""

    @rx.event
    async def cargar_usuarios(self):
        self.cargando = True
        self.error = ""
        yield

        try:
            async with httpx.AsyncClient(timeout=10.0) as cliente:
                respuesta = await cliente.get(
                    "https://jsonplaceholder.typicode.com/users"
                )
                respuesta.raise_for_status()
                datos = respuesta.json()

                self.usuarios = [
                    {
                        "name": str(usuario.get("name", "")),
                        "username": str(usuario.get("username", "")),
                        "email": str(usuario.get("email", "")),
                        "company": str(
                            usuario.get("company", {}).get("name", "")
                        ),
                    }
                    for usuario in datos
                ]

        except (httpx.HTTPError, ValueError):
            self.usuarios = []
            self.error = (
                "No se pudieron cargar los usuarios. "
                "Verifique su conexión e intente nuevamente."
            )

        finally:
            self.cargando = False


# TARJETA DE TAREA
def tarjeta_tarea(tarea):
    return rx.hstack(
        rx.text(
            tarea,
            color="white",
            flex="1",
        ),
        rx.button(
            "Eliminar",
            on_click=lambda: EstadoTareas.eliminar_tarea(tarea),
            color_scheme="red",
            size="2",
        ),
        padding="1em",
        border="1px solid #A78BFA",
        background_color="#321064",
        border_radius="10px",
        width="100%",
        max_width="500px",
        align="center",
        justify="between",
        box_shadow="0 4px 10px rgba(0, 0, 0, 0.2)",
        transition="all 0.2s ease",
    )


# LISTA DE TAREAS
def lista_tareas():
    return rx.vstack(
        rx.heading(
            "Lista de tareas",
            size="6",
            color="white",
        ),

        rx.form(
            rx.vstack(
                rx.input(
                    name="tarea",
                    placeholder="Escribe una nueva tarea",
                    value=EstadoTareas.nueva_tarea,
                    on_change=EstadoTareas.actualizar_nueva_tarea,
                    required=True,
                    width="100%",
                    max_width="500px",
                ),

                rx.button(
                    "Agregar tarea",
                    type="submit",
                    color_scheme="blue",
                    width="100%",
                    max_width="500px",
                ),

                spacing="3",
                width="100%",
                align="center",
            ),
            on_submit=EstadoTareas.agregar_tarea,
            reset_on_submit=False,
            width="100%",
        ),

        rx.text(
            EstadoTareas.mensaje,
            color="#C4B5FD",
            weight="bold",
        ),

        rx.cond(
            EstadoTareas.tareas.length() > 0,
            rx.vstack(
                rx.foreach(
                    EstadoTareas.tareas,
                    tarjeta_tarea,
                ),
                spacing="3",
                width="100%",
                align="center",
            ),
            rx.text(
                "No hay tareas registradas",
                color="white",
                weight="bold",
            ),
        ),

        spacing="3",
        align="center",
        width="100%",
    )


# FORMULARIO DE CONTACTO
def formulario_contacto():
    return rx.vstack(
        rx.heading(
            "Formulario de contacto",
            size="6",
            color="white",
        ),

        rx.form(
            rx.vstack(
                rx.text(
                    "Nombre completo",
                    color="white",
                ),

                rx.input(
                    name="nombre",
                    placeholder="Escribe tu nombre completo",
                    required=False,
                    width="100%",
                ),

                rx.text(
                    "Correo electrónico",
                    color="white",
                ),

                rx.input(
                    name="correo",
                    placeholder="ejemplo@correo.com",
                    type="text",
                    required=False,
                    width="100%",
                ),

                rx.text(
                    "Mensaje",
                    color="white",
                ),

                rx.text_area(
                    name="mensaje",
                    placeholder=(
                        "Escribe tu mensaje aquí "
                        "(mínimo 10 caracteres)"
                    ),
                    required=False,
                    width="100%",
                    min_height="120px",
                ),

                rx.button(
                    "Enviar formulario",
                    type="submit",
                    color_scheme="blue",
                    width="100%",
                ),

                spacing="2",
                width="100%",
            ),

            on_submit=EstadoContacto.enviar,
            reset_on_submit=False,
            width="100%",
        ),

        rx.text(
            EstadoContacto.mensaje_estado,
            color=rx.cond(
                EstadoContacto.es_error,
                "#FCA5A5",
                "#86EFAC",
            ),
            weight="bold",
            width="100%",
        ),

        padding="1.5em",
        border="1px solid #A78BFA",
        border_radius="12px",
        background="#321064",
        width="100%",
        max_width="500px",
        align="center",
        box_shadow="0 6px 18px rgba(0, 0, 0, 0.25)",
    )


# TARJETA DE USUARIO
def tarjeta_usuario(usuario):
    return rx.vstack(
        rx.heading(
            usuario["name"],
            size="4",
            color="white",
        ),

        rx.text(
            "Usuario: ",
            usuario["username"],
            color="#DDD6FE",
        ),

        rx.text(
            "Correo: ",
            usuario["email"],
            color="#DDD6FE",
        ),

        rx.text(
            "Empresa: ",
            usuario["company"],
            color="#DDD6FE",
            weight="medium",
        ),

        spacing="2",
        align="start",
        padding="1.25em",
        border="1px solid #8B5CF6",
        background="#321064",
        border_radius="12px",
        width="100%",
        max_width="500px",
        box_shadow="0 6px 15px rgba(0, 0, 0, 0.25)",
        transition="all 0.2s ease",
    )


# DIRECTORIO DE USUARIOS
def directorio_usuarios():
    return rx.vstack(
        rx.heading(
            "Directorio de usuarios",
            size="6",
            color="white",
        ),

        rx.text(
            "Usuarios obtenidos desde una API externa.",
            color="#DDD6FE",
            text_align="center",
        ),

        rx.button(
            "Cargar usuarios",
            on_click=EstadoUsuarios.cargar_usuarios,
            color_scheme="violet",
            disabled=EstadoUsuarios.cargando,
        ),

        rx.cond(
            EstadoUsuarios.cargando,
            rx.text(
                "Cargando usuarios...",
                color="#C4B5FD",
                weight="bold",
            ),
            rx.fragment(),
        ),

        rx.cond(
            EstadoUsuarios.error != "",
            rx.text(
                EstadoUsuarios.error,
                color="#FCA5A5",
                weight="bold",
            ),
            rx.fragment(),
        ),

        rx.cond(
            EstadoUsuarios.usuarios.length() > 0,
            rx.vstack(
                rx.foreach(
                    EstadoUsuarios.usuarios,
                    tarjeta_usuario,
                ),
                spacing="3",
                width="100%",
                align="center",
            ),
            rx.text(
                "Presiona el botón para cargar los usuarios.",
                color="white",
            ),
        ),

        spacing="3",
        align="center",
        width="100%",
    )


# INTERFAZ PRINCIPAL
def index():
    return rx.vstack(
        rx.heading(
            "Mi primera aplicación Reflex",
            size="8",
            color="#A78BFA",
            text_align="center",
        ),

        rx.heading(
            "Equipo: DEVAPPS - Equipo 1",
            size="5",
            color="white",
            text_align="center",
        ),

        rx.text(
            "Aplicación web interactiva desarrollada "
            "con Python y Reflex.",
            text_align="center",
            color="#DDD6FE",
        ),

        rx.button(
            "Comenzar",
            on_click=EstadoContador.incrementar,
            color_scheme="blue",
        ),

        rx.divider(),

        rx.heading(
            "Contador interactivo",
            size="6",
        ),

        rx.heading(
            EstadoContador.conteo,
            size="9",
        ),

        rx.hstack(
            rx.button(
                "Incrementar (+)",
                on_click=EstadoContador.incrementar,
                color_scheme="green",
            ),

            rx.button(
                "Disminuir (-)",
                on_click=EstadoContador.disminuir,
                color_scheme="red",
            ),

            rx.button(
                "Reiniciar",
                on_click=EstadoContador.reiniciar,
                color_scheme="gray",
            ),

            spacing="3",
            wrap="wrap",
            justify="center",
        ),

        rx.cond(
            EstadoContador.conteo > 0,
            rx.text(
                "El contador es positivo.",
                color="#86EFAC",
                weight="bold",
            ),
            rx.cond(
                EstadoContador.conteo < 0,
                rx.text(
                    "El contador es negativo.",
                    color="#FCA5A5",
                    weight="bold",
                ),
                rx.text(
                    "El contador es igual a cero.",
                    color="#D1D5DB",
                    weight="bold",
                ),
            ),
        ),

        rx.divider(),

        lista_tareas(),

        rx.divider(),

        formulario_contacto(),

        rx.divider(),

        directorio_usuarios(),

        spacing="5",
        align="center",
        justify="center",
        width="100%",
        min_height="100vh",
        padding="2em",
        background="#1C054B",
        color="white",
    )


app = rx.App()
app.add_page(index)