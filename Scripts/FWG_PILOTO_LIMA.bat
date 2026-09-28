@echo off
REM ============================================================
REM  FWG_PILOTO_LIMA.bat - Paso 3, piloto
REM  Corre Future Weather Generator sobre UNA sola ciudad (Lima)
REM  para descubrir empiricamente:
REM    - que escenarios y horizontes emite (no hay bandera SSP)
REM    - como nombra los archivos de salida
REM    - cuanto tarda una ciudad
REM  Antes de lanzar las 8. Verificar barato antes de gastar caro.
REM
REM  -uhi se deja en su default false:1:1 A PROPOSITO: este proyecto
REM  audita archivos climaticos, no isla de calor urbana.
REM ============================================================
setlocal
cd /d "%~dp0.."
set JAR=C:\Users\Usuario\Downloads\FutureWeatherGenerator_v4.2.0.jar
set BASE=Input\clima\Lima\PER_LMA_Lima-Chavez.Intl.AP.846280_TMYx.2011-2025.epw
set SALIDA=Temp\fwg\Lima
set CACHE=Temp\fwg\_modelos
set LOG=Context\log_fwg_piloto.txt

if not exist "%BASE%" (
    echo NO SE ENCUENTRA EL EPW BASE: %BASE%
    pause
    exit /b 1
)
if not exist "%SALIDA%" mkdir "%SALIDA%"
if not exist "%CACHE%" mkdir "%CACHE%"

echo === Piloto FWG Lima %DATE% %TIME% === > "%LOG%"
echo JAR: %JAR% >> "%LOG%"
echo BASE: %BASE% >> "%LOG%"
echo. >> "%LOG%"
echo.
echo   Corriendo Future Weather Generator sobre Lima...
echo   Descomprime modelos CMIP6 de un JAR de 3.7 GB. Puede tardar bastante.
echo   No cierres esta ventana.
echo.

java -jar "%JAR%" -g -epw="%BASE%" -ensemble=true -multithread=true ^
     -output_type=EPW -output_folder="%SALIDA%" -model_unzipped_folder="%CACHE%" ^
     -uhi=false:1:1 >> "%LOG%" 2>&1

echo. >> "%LOG%"
echo --- SALIDAS GENERADAS --- >> "%LOG%"
dir /b /s "%SALIDA%" >> "%LOG%" 2>&1
echo === Fin %DATE% %TIME% === >> "%LOG%"

echo.
echo   ---------------------------------------------------------
echo   Listo. Resultado en Context\log_fwg_piloto.txt
echo   ---------------------------------------------------------
echo.
pause
endlocal
