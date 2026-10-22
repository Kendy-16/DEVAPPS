# Ejercicio 2 · Panel de indicadores de tareas

**Reutiliza las seis tareas, eventos y tablero del Ejercicio 1**. Se incorpora `panel_indicadores()` con tarjetas reutilizables (`tarjeta_indicador()`) y propiedades `@rx.var`: total de tareas, pendientes, en progreso, completadas y porcentaje completado (control de división por cero). La barra de progreso depende de `ancho_progreso`, una propiedad calculada.

**Valores iniciales esperados:** 6 tareas; 2 pendientes; 2 en progreso; 2 completadas; **33 %** de avance (2/6 redondeado). Los resultados cambian al pulsar **Avanzar estado**.

**Pruebas para el informe:**

1. Captura del tablero junto con sus **cuatro indicadores y la barra de progreso**.
2. Mover `K-101` de Pendiente a En progreso: pendientes = 1 y en progreso = 3.
3. Mover `K-102` de En progreso a Completada: completadas = 3; porcentaje = **50 %**.
4. Comprobar que filtrar el tablero **no modifica** los indicadores globales, porque se calculan sobre la colección completa.
5. Revisar en el código la condición `if total else 0` que evita división entre cero.

**Ruta de código:** `indicadores_app/indicadores_app.py`.

## Inicio

**Windows:** doble clic en `iniciar_windows.bat` (debes tener `uv` en PATH y Python 3.13 instalado). Espera a que la terminal indique que el frontend y backend están listos. Abre `http://localhost:3000` si la consola indica ese puerto.

**Manual / otras plataformas:** abrir una terminal **en esta carpeta** y ejecutar:

```bash
uv sync --python 3.13
uv run reflex run
```

Para detener el servidor, `Ctrl+C`. **No ejecutes dos ejercicios al mismo tiempo** usando los mismos puertos. El proyecto gestiona sus dependencias dentro de `.venv`. Las carpetas `.web`, `.venv` y el archivo `uv.lock` se crean automáticamente.
