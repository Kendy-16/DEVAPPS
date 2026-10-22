# Ejercicio 1 · Tablero Kanban con filtro dinámico

El proyecto incluye **6 tareas** con identificador, título, descripción y estado. Se administran en `EstadoKanban(rx.State)`. `@rx.var tareas_visibles` aplica el filtro solo pendientes; otras propiedades calculadas distribuyen las tareas en tres columnas. `rx.foreach()` dibuja las tarjetas `tarjeta_tarea()`; cada tarjeta tiene un botón que cambia el estado (Pendiente → En progreso → Completada → Pendiente). Se contempla lista vacía tras el filtro y cada columna indica cuando está vacía.

**Pruebas para el informe:**

1. Abrir el tablero y fotografiar sus **6 tareas iniciales** repartidas entre los tres estados.
2. Presionar **Filtrar pendientes** y comprobar que solo se vean las tareas pendientes. Capturar pantalla.
3. Desactivar el filtro, mover `K-101` a En progreso y comprobar su traslado de columna.
4. Para probar un filtro sin coincidencias: mover todas las tareas pendientes a En progreso, activar **Filtrar pendientes** y capturar el aviso «No hay tareas que coincidan».
5. Volver a activar la vista general y mover tareas hasta comprobar los tres estados.

**Ruta de código:** `kanban_app/kanban_app.py`. CSS: `assets/estilos.css`.

## Inicio

**Windows:** doble clic en `iniciar_windows.bat` (debes tener `uv` en PATH y Python 3.13 instalado). Espera a que la terminal indique que el frontend y backend están listos. Abre `http://localhost:3000` si la consola indica ese puerto.

**Manual / otras plataformas:** abrir una terminal **en esta carpeta** y ejecutar:

```bash
uv sync --python 3.13
uv run reflex run
```

Para detener el servidor, `Ctrl+C`. **No ejecutes dos ejercicios al mismo tiempo** usando los mismos puertos. El proyecto gestiona sus dependencias dentro de `.venv`. Las carpetas `.web`, `.venv` y el archivo `uv.lock` se crean automáticamente.
