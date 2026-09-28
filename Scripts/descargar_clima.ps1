# descargar_clima.ps1
# Descarga los TMYx listados en Data\manifiesto_descarga_v1.csv y los descomprime
# en Input\clima\{ciudad}\. Idempotente: salta lo que ya existe.
# Fuente: climate.onebuilding.org (descarga directa, sin login).

$ErrorActionPreference = 'Continue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$Raiz      = Split-Path -Parent $PSScriptRoot
$Manifiesto= Join-Path $Raiz 'Data\manifiesto_descarga_v1.csv'
$Destino   = Join-Path $Raiz 'Input\clima'
$TempZip   = Join-Path $Raiz 'Temp\zips'
$Log       = Join-Path $Raiz 'Context\log_descarga.txt'

New-Item -ItemType Directory -Force -Path $Destino, $TempZip, (Split-Path $Log) | Out-Null
"=== Descarga iniciada $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" | Out-File $Log -Append -Encoding utf8

if (-not (Test-Path $Manifiesto)) {
    "ERROR: no se encontro el manifiesto en $Manifiesto" | Tee-Object -FilePath $Log -Append
    exit 1
}

$filas = Import-Csv $Manifiesto
$ok = 0; $saltados = 0; $fallos = 0

foreach ($f in $filas) {
    $carpetaCiudad = Join-Path $Destino $f.ciudad
    New-Item -ItemType Directory -Force -Path $carpetaCiudad | Out-Null

    $nombreZip = Split-Path $f.url -Leaf
    $marca     = Join-Path $carpetaCiudad ($nombreZip -replace '\.zip$', '.epw')

    # Checkpointing: si ya hay un EPW cuyo nombre coincide con este zip, saltar.
    $yaEsta = Get-ChildItem -Path $carpetaCiudad -Filter '*.epw' -ErrorAction SilentlyContinue |
              Where-Object { $_.BaseName -eq ($nombreZip -replace '\.zip$','') }
    if ($yaEsta) {
        "SALTADO (ya existe): $($f.ciudad) / $nombreZip" | Tee-Object -FilePath $Log -Append
        $saltados++
        continue
    }

    $rutaZip = Join-Path $TempZip $nombreZip
    try {
        Invoke-WebRequest -Uri $f.url -OutFile $rutaZip -UseBasicParsing -TimeoutSec 120
        if ((Get-Item $rutaZip).Length -lt 1024) { throw "archivo demasiado pequeno ($((Get-Item $rutaZip).Length) bytes)" }

        Expand-Archive -Path $rutaZip -DestinationPath $carpetaCiudad -Force
        $epws = Get-ChildItem -Path $carpetaCiudad -Filter '*.epw' -ErrorAction SilentlyContinue
        if (-not $epws) { throw "el zip no contenia ningun .epw" }

        "OK: $($f.ciudad) / $nombreZip -> $($epws.Count) epw en carpeta" | Tee-Object -FilePath $Log -Append
        $ok++
    }
    catch {
        "FALLO: $($f.ciudad) / $nombreZip :: $($_.Exception.Message)" | Tee-Object -FilePath $Log -Append
        $fallos++
    }
}

$totalEpw = (Get-ChildItem -Path $Destino -Recurse -Filter '*.epw' -ErrorAction SilentlyContinue).Count
$resumen = "RESUMEN: descargados=$ok saltados=$saltados fallos=$fallos | EPW totales en Input\clima = $totalEpw"
$resumen | Tee-Object -FilePath $Log -Append
"=== Descarga terminada $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" | Out-File $Log -Append -Encoding utf8

Write-Host ""
Write-Host $resumen
