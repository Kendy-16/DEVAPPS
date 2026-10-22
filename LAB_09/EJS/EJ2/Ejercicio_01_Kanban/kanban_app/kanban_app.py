"""Ejercicio 1: tablero Kanban con filtro calculado y cambios de estado.

En el ejercicio 2 se reutiliza este tablero y se agregan indicadores.
"""
import reflex as rx


TAREAS_INICIALES = [
    {"id": "K-101", "titulo": "Definir arquitectura", "descripcion": "Delimitar componentes y responsabilidades del prototipo.", "estado": "Pendiente"},
    {"id": "K-102", "titulo": "Crear navegación", "descripcion": "Conectar las vistas principales de la aplicación.", "estado": "En progreso"},
    {"id": "K-103", "titulo": "Diseñar identidad visual", "descripcion": "Elegir una composición coherente con el producto.", "estado": "Completada"},
    {"id": "K-104", "titulo": "Validar formulario", "descripcion": "Comprobar entradas vacías y formatos incorrectos.", "estado": "Pendiente"},
    {"id": "K-105", "titulo": "Preparar evidencias", "descripcion": "Organizar capturas del funcionamiento del sistema.", "estado": "En progreso"},
    {"id": "K-106", "titulo": "Documentar las pruebas", "descripcion": "Redactar los resultados y observaciones finales.", "estado": "Completada"},
]


class EstadoKanban(rx.State):
    """Estado central de la colección, filtro y movimientos del tablero."""

    tareas: list[dict[str, str]] = TAREAS_INICIALES
    mostrar_solo_pendientes: bool = False

    @rx.event
    def alternar_filtro(self):
        self.mostrar_solo_pendientes = not self.mostrar_solo_pendientes

    @rx.event
    def cambiar_estado(self, identificador: str):
        """Avanzar cíclicamente: Pendiente -> En progreso -> Completada -> Pendiente."""
        transiciones = {
            "Pendiente": "En progreso",
            "En progreso": "Completada",
            "Completada": "Pendiente",
        }
        self.tareas = [
            {**tarea, "estado": transiciones.get(tarea["estado"], "Pendiente")}
            if tarea["id"] == identificador else tarea
            for tarea in self.tareas
        ]

    @rx.var
    def tareas_visibles(self) -> list[dict[str, str]]:
        """Filtro solicitado explícitamente por la guía."""
        if self.mostrar_solo_pendientes:
            return [tarea for tarea in self.tareas if tarea["estado"] == "Pendiente"]
        return self.tareas

    @rx.var
    def pendientes_visibles(self) -> list[dict[str, str]]:
        return [tarea for tarea in self.tareas_visibles if tarea["estado"] == "Pendiente"]

    @rx.var
    def progreso_visibles(self) -> list[dict[str, str]]:
        return [tarea for tarea in self.tareas_visibles if tarea["estado"] == "En progreso"]

    @rx.var
    def completadas_visibles(self) -> list[dict[str, str]]:
        return [tarea for tarea in self.tareas_visibles if tarea["estado"] == "Completada"]

    @rx.var
    def cantidad_pendientes_visibles(self) -> int:
        return len(self.pendientes_visibles)

    @rx.var
    def cantidad_progreso_visibles(self) -> int:
        return len(self.progreso_visibles)

    @rx.var
    def cantidad_completadas_visibles(self) -> int:
        return len(self.completadas_visibles)

    @rx.var
    def total_visibles(self) -> int:
        return len(self.tareas_visibles)

    @rx.var
    def total_tareas(self) -> int:
        return len(self.tareas)

    @rx.var
    def total_pendientes(self) -> int:
        return sum(1 for tarea in self.tareas if tarea["estado"] == "Pendiente")

    @rx.var
    def total_progreso(self) -> int:
        return sum(1 for tarea in self.tareas if tarea["estado"] == "En progreso")

    @rx.var
    def total_completadas(self) -> int:
        return sum(1 for tarea in self.tareas if tarea["estado"] == "Completada")

    @rx.var
    def porcentaje_completadas(self) -> int:
        total = len(self.tareas)
        return round(100 * self.total_completadas / total) if total else 0

    @rx.var
    def ancho_progreso(self) -> str:
        return f"{self.porcentaje_completadas}%"


def etiqueta_estado(estado):
    return rx.cond(
        estado == "Pendiente",
        rx.text("● PENDIENTE", class_name="status status-wait"),
        rx.cond(
            estado == "En progreso",
            rx.text("● EN PROGRESO", class_name="status status-doing"),
            rx.text("● COMPLETADA", class_name="status status-done"),
        ),
    )


def tarjeta_tarea(tarea):
    """Componente reutilizable de representación de una tarea."""
    return rx.box(
        rx.hstack(
            rx.text(tarea["id"], class_name="task-id"),
            etiqueta_estado(tarea["estado"]),
            justify="between", align="center", width="100%",
        ),
        rx.heading(tarea["titulo"], size="4", class_name="task-title"),
        rx.text(tarea["descripcion"], class_name="task-description"),
        rx.button(
            rx.cond(tarea["estado"] == "Completada", "Volver a pendiente ↺", "Avanzar estado ↗"),
            on_click=EstadoKanban.cambiar_estado(tarea["id"]),
            class_name="task-action", variant="ghost",
        ),
        class_name="task-card",
    )


def columna(nombre, subtitulo, tareas, numero, clase):
    return rx.box(
        rx.hstack(
            rx.box(
                rx.text(nombre, class_name="column-name"),
                rx.text(subtitulo, class_name="column-caption"),
            ),
            rx.box(rx.text(numero), class_name="column-count"),
            align="center", justify="between", width="100%",
        ),
        rx.box(
            rx.foreach(tareas, tarjeta_tarea),
            rx.cond(numero == 0, rx.text("Sin tareas en esta columna.", class_name="column-empty")),
            class_name="task-stack",
        ),
        class_name=f"board-column {clase}",
    )


def tablero():
    return rx.box(
        rx.hstack(
            rx.box(
                rx.text("VISTA GENERAL / CONTROL DE FLUJO", class_name="eyebrow"),
                rx.heading("Tablero de trabajo", size="7", class_name="section-title"),
            ),
            rx.button(
                rx.cond(EstadoKanban.mostrar_solo_pendientes, "Ver todas las tareas", "Filtrar pendientes"),
                on_click=EstadoKanban.alternar_filtro,
                class_name="filter-button", variant="ghost",
            ),
            align="center", justify="between", width="100%", class_name="toolbar",
        ),
        rx.cond(
            EstadoKanban.total_visibles == 0,
            rx.box(
                rx.heading("No hay tareas que coincidan", size="5"),
                rx.text("Desactiva el filtro o cambia el estado de una tarea."),
                class_name="empty-state",
            ),
            rx.box(
                columna("01 / POR HACER", "Ideas a transformar", EstadoKanban.pendientes_visibles, EstadoKanban.cantidad_pendientes_visibles, "lane-wait"),
                columna("02 / EN MARCHA", "Trabajo en desarrollo", EstadoKanban.progreso_visibles, EstadoKanban.cantidad_progreso_visibles, "lane-doing"),
                columna("03 / TERMINADO", "Resultados listos", EstadoKanban.completadas_visibles, EstadoKanban.cantidad_completadas_visibles, "lane-done"),
                class_name="kanban-grid",
            ),
        ),
        class_name="board-section",
    )


def cabecera():
    return rx.box(
        rx.box(
            rx.text("REFLEX / LABORATORIO 09", class_name="eyebrow"),
            rx.heading("El progreso también se diseña.", size="9", class_name="hero-title"),
            rx.text(
                "Seis tareas, tres estados y un flujo que cambia sin recargar la página. "
                "Explora el tablero, filtra pendientes y mueve las tarjetas.",
                class_name="hero-description",
            ),
            class_name="hero-copy",
        ),
        rx.box(
            rx.text("BITÁCORA DIGITAL", class_name="sticker-top"),
            rx.text("06", class_name="sticker-number"),
            rx.text("TAREAS PARA EMPEZAR", class_name="sticker-bottom"),
            class_name="hero-sticker",
        ),
        class_name="hero",
    )





def index():
    return rx.box(
        rx.box(
            rx.hstack(
                rx.text("▣  STUDIO / FLOW", class_name="brand"),
                rx.text("PANEL INTERACTIVO • 2026", class_name="topbar-right"),
                align="center", justify="between", width="100%",
            ),
            class_name="topbar",
        ),
        rx.box(
            cabecera(),
                    tablero(),
            rx.text("Construido con Python, rx.State, @rx.var, rx.foreach() y rx.cond().", class_name="footnote"),
            class_name="main-shell",
        ),
        class_name="page",
    )


app = rx.App(stylesheets=["/estilos.css"])
app.add_page(index, title="Studio Flow | Tablero Kanban", description="Laboratorio 09 Reflex: Kanban reactivo")
