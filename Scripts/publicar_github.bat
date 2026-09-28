@echo off
title Publicar en GitHub - IBPSA Peru
echo =========================================================================
echo    PUBLICACION EN GITHUB - IBPSA PERU
echo =========================================================================
echo.

cd /d "%~dp0.."

echo [1/3] Verificando Git...
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git no esta instalado o no se encuentra en el PATH.
    echo Puedes descargarlo gratis desde: https://git-scm.com/
    echo.
    pause
    exit /b 1
)

echo [2/3] Repositorio local verificado.
echo.
echo =========================================================================
echo Pega a continuacion la URL HTTPS de tu repositorio de GitHub
echo (Ejemplo: https://github.com/ibpsaperu/auditoria-clima-peru.git)
echo =========================================================================
echo.
set /p REPO_URL="URL de GitHub: "

if "%REPO_URL%"=="" (
    echo No ingresaste ninguna URL. La operacion fue cancelada.
    echo.
    pause
    exit /b 0
)

echo.
echo [3/3] Conectando y subiendo a GitHub...
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo =========================================================================
    echo SUBIDA COMPLETADA CON EXITO A GITHUB!
    echo =========================================================================
    echo Ahora en tu repositorio ve a: Settings - Pages - Source: GitHub Actions
) else (
    echo.
    echo [AVISO] Si se abrio una ventana de inicio de sesion, completa el acceso.
    echo Si hubo un error de permisos, verifica la URL ingresada.
)

echo.
pause
