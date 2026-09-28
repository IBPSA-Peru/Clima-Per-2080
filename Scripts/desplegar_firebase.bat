@echo off
chcp 65001 > nul
echo =========================================================================
echo    DESPLIEGUE A GOOGLE FIREBASE HOSTING - IBPSA PERÚ
echo =========================================================================
echo.
echo Este script publicará la herramienta interactiva en los servidores de Google.
echo Cuenta institucional requerida: ibpsaperu2026@gmail.com
echo.

cd /d "%~dp0\.."

echo [1/3] Verificando Node.js / NPM...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js no está instalado o no está en el PATH del sistema.
    echo Por favor instala Node.js desde https://nodejs.org/
    pause
    exit /b 1
)

echo [2/3] Verificando inicio de sesión con Google (ibpsaperu2026@gmail.com)...
call npx --yes firebase-tools login --reauth

echo.
echo [3/3] Desplegando archivos a Google Firebase Hosting...
call npx --yes firebase-tools deploy --only hosting

echo.
echo =========================================================================
echo ¡Despliegue completado con éxito en la infraestructura de Google!
echo Tu sitio ya está disponible mundialmente con certificado SSL gratuito.
echo =========================================================================
pause
