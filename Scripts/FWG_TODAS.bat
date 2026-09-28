@echo off
REM ============================================================
REM  FWG_TODAS.bat - Paso 3, corrida completa
REM  Corre Future Weather Generator sobre el TMYx de ventana mas
REM  reciente (2011-2025) de cada ciudad.
REM
REM  FWG no acepta bandera de escenario ni de horizonte: emite
REM  los 4 SSP x 2 horizontes (2050, 2080) en una sola pasada.
REM  Nos quedaremos con ssp245 y ssp585 a 2050, pero el resto
REM  se conserva porque no cuesta nada extra.
REM
REM  Idempotente: si ya existe la salida de una ciudad, la salta.
REM  -uhi queda en false:1:1 (default): este proyecto audita
REM  archivos climaticos, no isla de calor urbana.
REM ============================================================
setlocal enabledelayedexpansion
cd /d "%~dp0.."
set JAR=C:\Users\Usuario\Downloads\FutureWeatherGenerator_v4.2.0.jar
set CACHE=Temp\fwg\_modelos
set LOG=Context\log_fwg_todas.txt

if not exist "%CACHE%" mkdir "%CACHE%"
echo === Corrida FWG completa %DATE% %TIME% === > "%LOG%"
echo.
echo   Generando escenarios futuros para todas las ciudades.
echo   Lima tardo unos 4 minutos. Calcula algo asi por ciudad.
echo   No cierres esta ventana.
echo.

for /d %%C in (Input\clima\*) do (
    set "CIUDAD=%%~nxC"
    set "BASE="
    for %%F in ("%%C\*_TMYx.2011-2025.epw") do set "BASE=%%F"

    if not defined BASE (
        echo [SALTADA] !CIUDAD!: sin TMYx.2011-2025 >> "%LOG%"
        echo   [SALTADA] !CIUDAD! - no tiene ventana 2011-2025
    ) else (
        set "SAL=Temp\fwg\!CIUDAD!"
        REM Checkpointing: si ya hay un ensemble ssp585_2050, no rehacer.
        set "HECHO="
        for %%E in ("!SAL!\*_Ensemble_ssp585_2050.epw") do set "HECHO=1"

        if defined HECHO (
            echo [YA ESTABA] !CIUDAD! >> "%LOG%"
            echo   [YA ESTABA] !CIUDAD!
        ) else (
            if not exist "!SAL!" mkdir "!SAL!"
            echo   Procesando !CIUDAD! ...
            echo. >> "%LOG%"
            echo --- !CIUDAD! : !BASE! --- >> "%LOG%"
            java -jar "%JAR%" -g -epw="!BASE!" -ensemble=true -multithread=true ^
                 -output_type=EPW -output_folder="!SAL!" -model_unzipped_folder="%CACHE%" ^
                 -uhi=false:1:1 >> "%LOG%" 2>&1
            echo   Terminada !CIUDAD!
        )
    )
)

echo. >> "%LOG%"
echo --- RESUMEN: ensembles 2050 generados --- >> "%LOG%"
dir /b /s "Temp\fwg\*_Ensemble_ssp*_2050.epw" >> "%LOG%" 2>&1
echo === Fin %DATE% %TIME% === >> "%LOG%"

echo.
echo   ---------------------------------------------------------
echo   Listo. Resultado en Context\log_fwg_todas.txt
echo   ---------------------------------------------------------
echo.
pause
endlocal
