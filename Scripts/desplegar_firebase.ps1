# Script PowerShell de despliegue a Google Firebase Hosting - IBPSA Perú
# Cuenta: ibpsaperu2026@gmail.com

$ErrorActionPreference = "Stop"
Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host "   DESPLIEGUE A GOOGLE FIREBASE HOSTING - IBPSA PERÚ" -ForegroundColor Cyan
Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Este script publicará la herramienta interactiva en la red global de Google."
Write-Host "Cuenta Google asociada: ibpsaperu2026@gmail.com" -ForegroundColor Yellow
Write-Host ""

$RootPath = (Get-Item $PSScriptRoot).Parent.FullName
Set-Location $RootPath

# 1. Comprobar Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js no está instalado. Instálalo desde https://nodejs.org/"
    exit 1
}

# 2. Iniciar sesión en Google
Write-Host "[1/3] Validando sesión de Google..." -ForegroundColor Green
npx --yes firebase-tools login

# 3. Desplegar
Write-Host "[2/3] Subiendo y activando versión en Google Firebase Hosting..." -ForegroundColor Green
npx --yes firebase-tools deploy --only hosting

Write-Host ""
Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host "¡Despliegue finalizado con éxito!" -ForegroundColor Green
Write-Host "Tu sitio web está activo en los servidores de Google con HTTPS gratuito." -ForegroundColor Green
Write-Host "=========================================================================" -ForegroundColor Cyan
