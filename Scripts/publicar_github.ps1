# Script PowerShell para publicar en GitHub & GitHub Pages - IBPSA Perú
$ErrorActionPreference = "Continue"

Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host "   PUBLICACIÓN EN GITHUB & GITHUB PAGES - IBPSA PERÚ" -ForegroundColor Cyan
Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host ""

$RootPath = (Get-Item $PSScriptRoot).Parent.FullName
Set-Location $RootPath

# 1. Comprobar Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git no está instalado en el sistema. Descárgalo desde https://git-scm.com/"
    exit 1
}

# 2. Inicializar si no existe
if (-not (Test-Path ".git")) {
    Write-Host "[1/3] Inicializando repositorio Git local..." -ForegroundColor Green
    git init -b main
} else {
    Write-Host "[1/3] Repositorio Git ya existente." -ForegroundColor Green
}

# 3. Añadir archivos y commit
Write-Host "[2/3] Registrando archivos respetando .gitignore..." -ForegroundColor Green
git add .
git commit -m "Publicación v1.13.0: Auditoría climática EPW Perú - IBPSA Perú"

Write-Host ""
Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host "Pega la URL de tu repositorio en GitHub si ya lo creaste" -ForegroundColor Yellow
Write-Host "(Ejemplo: https://github.com/ibpsaperu/auditoria-clima-peru.git)" -ForegroundColor Gray
Write-Host "O presiona ENTER para omitir por ahora:" -ForegroundColor Yellow
$repoUrl = Read-Host "URL en GitHub"

if ($repoUrl -and $repoUrl.Trim() -ne "") {
    git remote remove origin 2>$null
    git remote add origin $repoUrl.Trim()
    Write-Host "Subiendo a GitHub (rama main)..." -ForegroundColor Green
    git push -u origin main
    Write-Host ""
    Write-Host "¡Repositorio subido con éxito!" -ForegroundColor Green
    Write-Host "En GitHub ve a Settings > Pages y verifica que esté en 'GitHub Actions'." -ForegroundColor Cyan
} else {
    Write-Host "Repositorio local preparado. Puedes conectar el remoto cuando gustes con:" -ForegroundColor Yellow
    Write-Host "  git remote add origin <URL>" -ForegroundColor Gray
    Write-Host "  git push -u origin main" -ForegroundColor Gray
}
