"""Ejercicio 04 del Laboratorio N.° 09: API y búsqueda reactiva.

JSONPlaceholder /users -> HTTPX -> rx.State -> @rx.var -> rx.foreach.
"""
import httpx
import reflex as rx

URL_USUARIOS = "https://jsonplaceholder.typicode.com/users"
URL_ERROR = "https://jsonplaceholder.typicode.com/ruta-prueba-inexistente"


class EstadoUsuarios(rx.State):
    usuarios: list[dict[str, str]] = []
    busqueda: str = ""
    cargando: bool = False
    error: str = ""
    url_api: str = URL_USUARIOS

    @rx.event
    def cambiar_busqueda(self, valor: str):
        self.busqueda = valor

    @rx.event
    def probar_error(self):
        """Selecciona endpoint inexistente para probar el manejo de HTTP 404."""
        self.url_api = URL_ERROR
        self.error = ""

    @rx.event
    def restaurar_api(self):
        self.url_api = URL_USUARIOS
        self.error = ""

    @rx.event
    async def cargar_usuarios(self):
        """El primer yield muestra cargando=True antes de esperar a HTTPX."""
        self.cargando = True
        self.error = ""
        self.usuarios = []
        yield
        try:
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as cliente:
                respuesta = await cliente.get(self.url_api)
                respuesta.raise_for_status()
                datos = respuesta.json()

            if not isinstance(datos, list):
                raise ValueError("La API no devolvió una lista de usuarios.")

            self.usuarios = [
                {
                    "nombre": str(persona.get("name", "Sin nombre")),
                    "usuario": str(persona.get("username", "")),
                    "correo": str(persona.get("email", "")),
                    "ciudad": str((persona.get("address") or {}).get("city", "No indicada")),
                    "empresa": str((persona.get("company") or {}).get("name", "No indicada")),
                }
                for persona in datos
                if isinstance(persona, dict)
            ]
        except (httpx.HTTPError, ValueError, TypeError) as excepcion:
            self.error = f"No fue posible recuperar los usuarios. Detalle: {excepcion}"
        finally:
            self.cargando = False

    @rx.var
    def usuarios_filtrados(self) -> list[dict[str, str]]:
        """No distingue entre mayúsculas ni minúsculas; elimina espacios de búsqueda."""
        texto = self.busqueda.strip().casefold()
        if not texto:
            return self.usuarios
        return [u for u in self.usuarios if texto in u["nombre"].casefold()]

    @rx.var
    def cantidad_usuarios(self) -> int:
        return len(self.usuarios)

    @rx.var
    def cantidad_filtrados(self) -> int:
        return len(self.usuarios_filtrados)

    @rx.var
    def modo_api(self) -> str:
        return "MODO ERROR / URL INVALIDA" if self.url_api != URL_USUARIOS else "API DISPONIBLE / JSONPLACEHOLDER"


def tarjeta_usuario(usuario):
    """Representación reutilizable de los cinco atributos exigidos en el enunciado."""
    return rx.box(
        rx.hstack(
            rx.text("PERFIL / PÚBLICO", class_name="card-overline"),
            rx.text("↗", class_name="card-icon"),
            align="center", justify="between", width="100%",
        ),
        rx.heading(usuario["nombre"], size="5", class_name="user-name"),
        rx.text("@", usuario["usuario"], class_name="username"),
        rx.box(
            rx.text("CORREO", class_name="data-label"),
            rx.text(usuario["correo"], class_name="data-value"),
            class_name="data-row",
        ),
        rx.box(
            rx.text("CIUDAD", class_name="data-label"),
            rx.text(usuario["ciudad"], class_name="data-value"),
            class_name="data-row",
        ),
        rx.box(
            rx.text("EMPRESA", class_name="data-label"),
            rx.text(usuario["empresa"], class_name="data-value"),
            class_name="data-row",
        ),
        class_name="user-card",
    )


def controles():
    return rx.box(
        rx.hstack(
            rx.box(
                rx.text("EXPLORAR / USUARIOS", class_name="kicker"),
                rx.heading("Directorio de personas", size="7", class_name="section-title"),
            ),
            rx.text(EstadoUsuarios.modo_api, class_name="api-badge"),
            justify="between", align="center", class_name="toolbar", width="100%",
        ),
        rx.box(
            rx.box(
                rx.text("BUSCAR POR NOMBRE", class_name="form-caption"),
                rx.input(
                    placeholder="Ej. Leanne, Chelsey, Clementine...",
                    value=EstadoUsuarios.busqueda,
                    on_change=EstadoUsuarios.cambiar_busqueda,
                    class_name="search-input",
                ),
                class_name="search-area",
            ),
            rx.box(
                rx.button("Cargar / actualizar  ↗", on_click=EstadoUsuarios.cargar_usuarios, disabled=EstadoUsuarios.cargando, class_name="primary-button"),
                rx.button("Simular fallo", on_click=EstadoUsuarios.probar_error, disabled=EstadoUsuarios.cargando, class_name="secondary-button", variant="ghost"),
                rx.button("Restaurar API", on_click=EstadoUsuarios.restaurar_api, disabled=EstadoUsuarios.cargando, class_name="secondary-button", variant="ghost"),
                class_name="action-area",
            ),
            class_name="control-panel",
        ),
        rx.hstack(
            rx.text("USUARIOS EN MEMORIA: ", EstadoUsuarios.cantidad_usuarios, class_name="result-count"),
            rx.text("COINCIDENCIAS: ", EstadoUsuarios.cantidad_filtrados, class_name="result-count"),
            justify="between", align="center", width="100%", class_name="results-bar",
        ),
    )


def directorio_usuarios():
    return rx.box(
        controles(),
        rx.cond(
            EstadoUsuarios.cargando,
            rx.box(
                rx.spinner(size="3", color="#ee6f4b"),
                rx.heading("Cargando usuarios...", size="5", class_name="empty-heading"),
                rx.text("Esperando la respuesta del servicio externo."),
                class_name="message-panel",
            ),
            rx.cond(
                EstadoUsuarios.error != "",
                rx.box(
                    rx.text("¡", class_name="message-sign"),
                    rx.heading("La consulta no pudo completarse", size="5", class_name="empty-heading"),
                    rx.text(EstadoUsuarios.error, class_name="error-message"),
                    rx.text("Pulsa «Restaurar API» y después «Cargar / actualizar» para volver a probar.", class_name="message-tip"),
                    class_name="message-panel message-error",
                ),
                rx.cond(
                    EstadoUsuarios.cantidad_usuarios == 0,
                    rx.box(
                        rx.text("✳", class_name="message-sign"),
                        rx.heading("Una lista por descubrir", size="5", class_name="empty-heading"),
                        rx.text("Todavía no hay usuarios cargados. Presiona «Cargar / actualizar»."),
                        class_name="message-panel",
                    ),
                    rx.cond(
                        EstadoUsuarios.cantidad_filtrados == 0,
                        rx.box(
                            rx.heading("No hay coincidencias", size="5", class_name="empty-heading"),
                            rx.text("Prueba otro nombre; el filtro ignora mayúsculas y minúsculas."),
                            class_name="message-panel",
                        ),
                        rx.box(rx.foreach(EstadoUsuarios.usuarios_filtrados, tarjeta_usuario), class_name="users-grid"),
                    ),
                ),
            ),
        ),
        class_name="directory",
    )


def index():
    return rx.box(
        rx.box(
            rx.hstack(
                rx.text("ARCHIVO / HUMANO", class_name="brand"),
                rx.text("EDICIÓN 004   •   REFLEX + HTTPX", class_name="header-note"),
                align="center", justify="between", width="100%",
            ),
            class_name="topbar",
        ),
        rx.box(
            rx.box(
                rx.text("DATOS REALES DE UNA API DE PRUEBA", class_name="kicker"),
                rx.heading("Una ventana a diez historias digitales.", size="9", class_name="hero-title"),
                rx.text("Consulta una API, descubre usuarios y filtra personas al instante. Las tarjetas combinan nombre, alias, correo, ciudad y empresa.", class_name="hero-subtitle"),
                class_name="hero",
            ),
            directorio_usuarios(),
            rx.text("Reflex · HTTPX · @rx.var · rx.foreach() · on_change · Manejo de errores", class_name="footer-note"),
            class_name="shell",
        ),
        class_name="page",
    )


app = rx.App(stylesheets=["/estilos.css"])
app.add_page(index, title="Archivo Humano | Directorio API", description="Laboratorio 09 Reflex - Ejercicio 4")
