# Ejercicio 4 · Directorio de usuarios con búsqueda dinámica

Se consulta `https://jsonplaceholder.typicode.com/users` con `httpx.AsyncClient`. El manejador asincrónico `cargar_usuarios()` activa `cargando` y cede el control con `yield` para mostrar el estado de espera; al recibir datos los procesa y guarda nombre, nombre de usuario, correo, ciudad y empresa. `@rx.var usuarios_filtrados` busca por nombre sin distinguir mayúsculas/minúsculas (`casefold()`) y se actualiza con `on_change`. El directorio se genera con `rx.foreach()`. El botón de actualización vuelve a consultar la API.

**Pruebas para el informe:**

1. Antes de cargar, capturar la vista con el aviso de que no hay usuarios.
2. Pulsar **Cargar / actualizar**. Capturar tarjetas con nombre, usuario, correo, ciudad y empresa.
3. Escribir `leanne` y después `LEANNE` en el buscador; comprobar las mismas coincidencias.
4. Escribir `NOEXISTE_123` y capturar el mensaje «No hay coincidencias».
5. Pulsar **Simular fallo** y luego **Cargar / actualizar** para obtener un error HTTP 404. Capturar el aviso.
6. Pulsar **Restaurar API**, luego **Cargar / actualizar** para recuperar los datos.

**Requisitos externos:** conexión a Internet durante las consultas a JSONPlaceholder.

**Ruta de código:** `usuarios_app/usuarios_app.py`.

## Inicio

**Windows:** doble clic en `iniciar_windows.bat` (debes tener `uv` en PATH y Python 3.13 instalado). Espera a que la terminal indique que el frontend y backend están listos. Abre `http://localhost:3000` si la consola indica ese puerto.

**Manual / otras plataformas:** abrir una terminal **en esta carpeta** y ejecutar:

```bash
uv sync --python 3.13
uv run reflex run
```

Para detener el servidor, `Ctrl+C`. **No ejecutes dos ejercicios al mismo tiempo** usando los mismos puertos. El proyecto gestiona sus dependencias dentro de `.venv`. Las carpetas `.web`, `.venv` y el archivo `uv.lock` se crean automáticamente.
