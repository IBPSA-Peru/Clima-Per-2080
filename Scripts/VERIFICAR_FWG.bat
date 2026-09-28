@echo off
REM ============================================================
REM  VERIFICAR_FWG.bat - Paso 3 de la Auditoria de Clima Peru
REM  NO genera nada. Solo verifica:
REM    1. Que version de Java esta instalada
REM    2. Donde esta el JAR de Future Weather Generator
REM    3. Que opciones de linea de comandos acepta ese JAR
REM  Todo queda escrito en Context\log_fwg.txt
REM ============================================================
setlocal enabledelayedexpansion
cd /d "%~dp0.."
set LOG=Context\log_fwg.txt

echo === Verificacion FWG %DATE% %TIME% === > "%LOG%"
echo.
echo   Verificando Java y el JAR de Future Weather Generator...
echo   Este JAR pesa mas de 3 GB, puede tardar en responder. No cierres la ventana.
echo.

echo. >> "%LOG%"
echo --- [1] JAVA --- >> "%LOG%"
java -version >> "%LOG%" 2>&1
if errorlevel 1 echo JAVA NO ENCONTRADO EN EL PATH >> "%LOG%"
where java >> "%LOG%" 2>&1

echo. >> "%LOG%"
echo --- [2] BUSQUEDA DEL JAR --- >> "%LOG%"
set JAR=
for %%D in ("%USERPROFILE%\Downloads" "%USERPROFILE%\Descargas" "Input" "%USERPROFILE%\Desktop") do (
    if exist %%D (
        for /f "delims=" %%F in ('dir /b /s "%%~D\FutureWeatherGenerator*.jar" 2^>nul') do (
            echo ENCONTRADO: %%F >> "%LOG%"
            if not defined JAR set "JAR=%%F"
        )
    )
)

if not defined JAR (
    echo NINGUN JAR FutureWeatherGenerator*.jar ENCONTRADO >> "%LOG%"
    echo   No se encontro el JAR. Revisa Context\log_fwg.txt
    pause
    exit /b 1
)

echo. >> "%LOG%"
echo JAR EN USO: !JAR! >> "%LOG%"
for %%A in ("!JAR!") do echo TAMANO BYTES: %%~zA >> "%LOG%"

echo. >> "%LOG%"
echo --- [3] AYUDA DEL JAR (-h) --- >> "%LOG%"
echo   Ejecutando java -jar con -h ... (puede tardar 1-2 min)
java -jar "!JAR!" -h >> "%LOG%" 2>&1

echo. >> "%LOG%"
echo --- [4] SIN ARGUMENTOS: NO SE PRUEBA --- >> "%LOG%"
echo Segun hallazgo previo, sin argumentos abre GUI y se queda esperando. >> "%LOG%"
echo No se ejecuta esa variante a proposito. >> "%LOG%"

echo. >> "%LOG%"
echo === Fin %DATE% %TIME% === >> "%LOG%"
echo.
echo   ---------------------------------------------------------
echo   Listo. Resultado en Context\log_fwg.txt
echo   ---------------------------------------------------------
echo.
pause
endlocal
