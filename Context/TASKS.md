# TASKS.md

| ID | Tarea | Estado | Tiempo real | Notas |
|---|---|---|---|---|
| T1.1 | Crear arbol SOP-01 | HECHO | ~1 min | nucleo + Data + Scripts + Temp\renders + figuras |
| T1.2 | P0.md con modulos activos | HECHO | ~2 min | 4 modulos activos declarados |
| T1.3 | environment.md | HECHO | ~2 min | incluye tabla de conectividad verificada |
| T1.4 | SUPUESTOS.md / TASKS.md / DECISIONS.md | HECHO | ~3 min | SUP-01 a SUP-04 registrados |
| T2.1 | Obtener catalogo PER_Peru | HECHO | ~2 min | via web_fetch; 40 zips de 8 ciudades |
| T2.2 | Manifiesto de descarga | HECHO | ~3 min | Data\manifiesto_descarga_v1.csv |
| T2.3 | Script de descarga para Windows | HECHO | ~5 min | Scripts\DESCARGAR_CLIMA.bat + descargar_clima.ps1 |
| T2.4 | Ejecutar la descarga | HECHO | ~25 min | 40/40 descargados, 0 fallos. Ver SUP-05: la ventana estaba en el segundo monitor |
| T2.5 | Data\inventario_epw.csv con ano centroide | HECHO | ~5 min | 40 filas, 8 ciudades, ano centroide legible en las 40 |
| T3.1 | FWG: verificar Java y sintaxis del JAR | HECHO | ~10 min | Java 17.0.19 OK. Sin bandera SSP: emite los 4 SSP x 2 horizontes |
| T3.2 | FWG: piloto sobre Lima | HECHO | ~15 min | 8 ensembles en 4 min. Coherencia C-C pasa, estructura temporal preservada |
| T3.3 | FWG: 7 ciudades restantes | HECHO | ~8 min | 8/8 ciudades, 0 errores. 32 escenarios 2050 + 32 de 2080 |
| T4 | Scripts\analizar_epw.py | HECHO | ~25 min | 8/8 comprobaciones del autotest OK sobre EPW sintetico |
| T5 | Los cuatro analisis | HECHO | ~30 min | Scripts\analisis_cuatro.py -> Data\analisis_cuatro_v1.json. C queda PARCIAL |
| T6 | Las ocho figuras | HECHO | ~50 min | 8/8 aprobadas tras 3 pasadas de revision visual. Ver D-13 y D-14 |
| T7 | INFORME_AUDITORIA_CLIMA_PERU.md | HECHO | ~40 min | 7 secciones. Todo multiplo lleva su absoluto (F1) |
| T8 | Cierre, autoauditoria y backup | HECHO | ~20 min | README v1.0.0, AUTOAUDITORIA.md, snapshot en Backup\ |

| T4.1 | Autotest del motor | HECHO | ~8 min | 2 fallos iniciales eran del test, no del motor: hora EPW 1-24 y redondeo a 1 decimal |
| T9 | Visor HTML v1 (M-WEB) | REEMPLAZADO | ~35 min | Era un informe maquetado, no interactivo. Ver D-15 |
| T10 | Visor interactivo v2 | HECHO | ~70 min | Mapa de Peru, nube animada, 8 escenas. 81 KB, todo SVG. 3 defectos hallados y corregidos en compuerta visual. Ver D-16 |
| T11 | Procesar horizonte 2080 | HECHO | ~10 min | 32 EPW que llevaban generados sin analizar. Data\metricas_2080_v1.csv |
| T12 | Visor v3: narrativa invertida, Futura, iconos | HECHO | ~90 min | Dato primero, fiabilidad despues. 4 horizontes interpolables. Ver D-17 |
| T13 | Auditoria WCAG 2.1 AA del visor | HECHO | ~20 min | 3 fallos de contraste corregidos; reduced-motion y aria. Ver D-17 |
| T14 | Corregir etiqueta erronea de la nube | HECHO | ~5 min | Decia 2080 y mostraba 2050. Ver D-18 |
| T15 | Tres horizontes en todas las vistas | HECHO | ~50 min | Portada 4 cifras, nube 4 estados, trayectoria por ciudad |
| T16 | Capitulo 04: diagrama del metodo | HECHO | ~30 min | 6 pasos con iconos de trazo y entrada escalonada |
| T17 | Climograma mensual max/min por horizonte | HECHO | ~45 min | Lo que se percibe, no la media anual. Ver D-19 |
| T18 | Portada animada y metodo interactivo | HECHO | ~40 min | 6 pasos clicables con cifras reales |
| T19 | Corregir arranque en zona muerta temporal | HECHO | ~5 min | Habria dejado la pagina en blanco. Ver D-19 |
| T20 | Climograma con 4 horizontes simultaneos | HECHO | ~35 min | 48 franjas verificadas por conteo. Ver D-20 |
| T21 | Restaurar icono de portada, animado | HECHO | ~10 min | Se habia eliminado por mala lectura de la peticion |
| T22 | Caratula: sol de doce meses interactivo | HECHO | ~40 min | 440 px, 12 rayos de dato, ciclo automatico. Ver D-21 |
| T23 | Climograma conmutable por leyenda | HECHO | ~35 min | Encender/apagar, aislar, cifras al quedar uno. Ver D-22 |
| T24 | Nube: color por mes u hora, con leyenda | HECHO | ~40 min | El color duplicaba el eje X. Ver D-23 |
| T25 | Climograma de bandas y linea de media | HECHO | ~45 min | Mas grande, con leyenda de trazos y rangos. Ver D-24 |
| T26 | Sol de portada al tamano de caratula | HECHO | ~15 min | 560 px de lienzo en contenedor de 660. Ver D-25 |
| T27 | Corregir sol invisible por opacity:0 | HECHO | ~20 min | Fallo critico de CSS. Ver D-26 |
| T28 | Serie observada en la trayectoria | HECHO | ~35 min | 40 puntos TMYx medidos, 1987-2019. Ver D-27 |
| T29 | Barras clicables con orden conmutable | HECHO | ~30 min | Ver D-28 |
| T30 | Sol al tamano de caratula, texto lateral | HECHO | ~20 min | 680 px de lienzo, 2/3 del ancho. Ver D-29 |
| T31 | Recuperar plantilla.js truncado por timeout | HECHO | ~10 min | Restaurado del backup. Ver D-30 |
