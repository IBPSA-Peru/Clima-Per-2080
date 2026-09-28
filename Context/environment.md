# environment.md

Capturado: 2026-07-26T17:20:59Z

## Entorno de computo del agente (sandbox Linux, Ubuntu 22.04)
| Item | Valor |
|---|---|
| Python | Python 3.10.12 |
| Java | openjdk version "11.0.31" 2026-04-21 |
| Nucleos CPU | 2 |
| Disco | 8.6G libres de 9.8G |
| Librerias | pandas 2.3.3 | numpy 2.2.6 | matplotlib 3.10.9 | requests 2.34.2 | scipy 1.15.3 |

## Entorno de la maquina del usuario (Windows)
| Item | Valor |
|---|---|
| Rol | ejecuta las descargas y, si aplica, el JAR de FWG |
| Java | POR VERIFICAR en Paso 3 |
| PowerShell | asumido >= 5.1 (Windows 10/11 de fabrica) |

## Red — verificado, no supuesto
Prueba con curl desde el sandbox, 2026-07-26:

| Host | Resultado |
|---|---|
| climate.onebuilding.org | 000 (bloqueado) |
| future-weather-generator.adai.pt | 000 (bloqueado) |
| pypi.org | 200 (permitido) |
| google.com | 000 (bloqueado) |

Consecuencia: el sandbox puede instalar paquetes de Python pero NO puede descargar
los archivos climaticos ni el JAR. Ver SUP-02 para la solucion adoptada.

## Notas de version relevantes
- El sandbox trae Java 11. El JAR de Future Weather Generator v4.x requiere Java 17.
  Java 11 no sirve para FWG aunque el sandbox pudiera descargarlo.
