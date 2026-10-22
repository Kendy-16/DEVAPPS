# Ejercicio 3 · Sistema de registro de solicitudes

Formulario reactivo con nombre, correo, tipo de solicitud (Consulta, Incidencia, Requerimiento) y descripción. El manejador `registrar()` valida en Python: nombre obligatorio, correo con expresión regular, tipo reconocido y descripción con mínimo 10 caracteres. Los controles HTML también usan `required`, correo tipo `email` y `min_length=10` donde corresponde. Los registros válidos se guardan temporalmente en `EstadoSolicitudes.solicitudes` y se muestran con `rx.foreach()`. Se pueden eliminar sin recarga.

**Pruebas para el informe:**

1. Capturar el formulario vacío y la bandeja sin solicitudes.
2. Probar envío vacío y correo mal escrito: observar la validación **del navegador** (puede impedir el envío a Python).
3. Probar una descripción de menos de 10 caracteres: el navegador puede bloquear el envío; Python también lo verifica por seguridad.
4. Enviar correctamente: `Ana Torres`, `ana.torres@ejemplo.com`, `Incidencia`, `No puedo acceder al aula virtual.`. Capturar el mensaje de éxito con nombre y la tarjeta registrada.
5. Comprobar que los campos se limpian tras un registro correcto y que se pueden enviar más solicitudes.
6. Eliminar el registro y capturar la bandeja vacía.

**Importante:** los registros están solo en memoria y no envían correos ni se guardan en una base de datos.

**Ruta de código:** `solicitudes_app/solicitudes_app.py`.

## Inicio

**Windows:** doble clic en `iniciar_windows.bat` (debes tener `uv` en PATH y Python 3.13 instalado). Espera a que la terminal indique que el frontend y backend están listos. Abre `http://localhost:3000` si la consola indica ese puerto.

**Manual / otras plataformas:** abrir una terminal **en esta carpeta** y ejecutar:

```bash
uv sync --python 3.13
uv run reflex run
```

Para detener el servidor, `Ctrl+C`. **No ejecutes dos ejercicios al mismo tiempo** usando los mismos puertos. El proyecto gestiona sus dependencias dentro de `.venv`. Las carpetas `.web`, `.venv` y el archivo `uv.lock` se crean automáticamente.
