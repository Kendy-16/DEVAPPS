@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
set "UV_LINK_MODE=copy"
echo ============================================================
echo   Laboratorio 09 - Ejercicios Reflex
echo ============================================================
where uv >nul 2>nul
if errorlevel 1 (
  echo ERROR: No se encontro uv en el PATH.
  echo Agrega uv al PATH o instalalo con: py -m pip install uv
  pause
  exit /b 1
)
echo.
echo Preparando entorno virtual con Python 3.13...
uv sync --python 3.13
if errorlevel 1 (
  echo.
  echo ERROR: Fallo la instalacion. Comprueba Python 3.13 y tu conexion.
  pause
  exit /b 1
)
echo.
echo Iniciando Reflex. ESPERA hasta que indique Frontend y Backend.
echo Abre http://localhost:3000 (o el puerto que indique Reflex).
echo.
uv run reflex run
if errorlevel 1 echo Reflex se detuvo por un error; revisa las lineas anteriores.
pause
