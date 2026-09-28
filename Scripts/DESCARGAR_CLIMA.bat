@echo off
REM ============================================================
REM  DESCARGAR_CLIMA.bat  -  Paso 2 de la Auditoria de Clima Peru
REM  Descarga los TMYx de climate.onebuilding.org y los descomprime.
REM  Idempotente: si el EPW ya existe, no lo vuelve a bajar.
REM  Doble clic para ejecutar. No requiere escribir nada.
REM ============================================================
setlocal
cd /d "%~dp0.."
echo.
echo   Descargando archivos climaticos TMYx para Peru...
echo   Esto puede tardar unos minutos. No cierres esta ventana.
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0descargar_clima.ps1"
echo.
echo   ---------------------------------------------------------
echo   Listo. Revisa Input\clima\ y Context\log_descarga.txt
echo   ---------------------------------------------------------
echo.
pause
endlocal
