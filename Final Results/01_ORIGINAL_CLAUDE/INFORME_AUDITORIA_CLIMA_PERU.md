# Auditoría de archivos climáticos para simulación energética de edificios en Perú

**IBPSA Perú** · Vía: investigación, no comercial · v1.0 · 26 de julio de 2026
Agente ejecutor: Cowork/Claude · Protocolo: SOP-01 y SOP-02

---

## 1. Resumen ejecutivo

1. **El vintage de un TMYx introduce ruido, no un sesgo corregible.** La tendencia es de +0.18 °C por década de diferencia de año centroide, pero explica solo el 13 % de la varianza (r² = 0.13, n = 29). El ΔT aparente entre ventanas de una misma ciudad va de −0.91 a +3.64 °C. No existe factor de corrección: hay que leer el año centroide del archivo concreto.
2. **La ventana TMYx 2004-2018 está comprometida en las tres estaciones andinas** y en ninguna costera: Cusco +2.96 °C, Arequipa +1.20 °C y Juliaca −1.62 °C contra la mediana de su propia ciudad. Juliaca además cambia de estructura temporal (autocorrelación 0.377 frente a 0.85 en sus otras cuatro ventanas).
3. **El calentamiento proyectado a 2050 no es uniforme y escala con la altura**: de +1.40 °C en Piura (35 m) a +1.83 °C en Juliaca (3826 m) bajo SSP2-4.5, con r = +0.73 contra elevación. Pero la consecuencia energética va al revés: Juliaca tiene el mayor ΔT del país y prácticamente ninguna carga de enfriamiento.
4. **Dos métodos independientes discrepan en 0.70 °C** para Lima 2050 una vez alineadas las líneas base: Meteonorm RCP8.5 da 20.93 °C y FWG SSP5-8.5 da 21.62 °C. La comparación es indicativa, no una validación cruzada: RCP8.5 es CMIP5 y SSP5-8.5 es CMIP6.
5. **El morphing de FWG preserva la estructura temporal** (máximo |Δautocorrelación| = 0.047; racha cálida máxima idéntica en 16 de 16 casos). La pregunta de si los archivos *sintetizados* subestiman los episodios multi-día **queda sin responder**: no se dispuso de ningún archivo generado por síntesis estocástica.

---

## 2. Metodología

### Archivos

40 archivos TMYx de climate.onebuilding.org, descarga directa sin credenciales, 26 de julio de 2026. Ocho estaciones × cinco ventanas temporales cada una: periodo completo, 2004-2018, 2007-2021, 2009-2023 y 2011-2025.

Se descargaron las cinco ventanas de cada ciudad, no solo dos. El Análisis A correlaciona ΔT contra diferencia de año centroide: con dos puntos por ciudad sale una recta forzada; con cinco sale una dispersión real y un r² honesto. Esa decisión es la que permite reportar el hallazgo 1.

### Herramientas

| Herramienta | Versión | Uso |
|---|---|---|
| Future Weather Generator | 4.2.0 (JAR de 3 680 843 597 bytes) | morphing a 2050 |
| Java | OpenJDK 17.0.19 LTS (Microsoft) | ejecución del JAR |
| Python | 3.10.12 | motor de métricas y análisis |
| pandas / numpy / matplotlib / scipy | 2.3.3 / 2.2.6 / 3.10.9 / 1.15.3 | cálculo y figuras |

**Nota sobre FWG v4.2.0:** no acepta bandera de escenario ni de horizonte. Una sola pasada de `-g` emite los cuatro SSP (1-2.6, 2-4.5, 3-7.0, 5-8.5) × dos horizontes (2050, 2080). Buscar un parámetro `-ssp` es un callejón sin salida. El parámetro `-uhi` se dejó en su valor por defecto `false:1:1`: este trabajo audita archivos climáticos, no isla de calor urbana.

Modelo climático: ensemble de los 23 modelos CMIP6 empaquetados en el JAR. Interpolación de malla IDW a cuatro puntos. Base del morphing: el TMYx de ventana 2011-2025 de cada ciudad, es decir la menos envejecida disponible.

### Verificación

El motor `analizar_epw.py` se validó antes de tocar los datos reales, contra un EPW sintético de propiedades conocidas (media 20 °C, ciclo diurno ±5 °C, pico a las 15:00–16:00, años fuente 2010-2021): ocho comprobaciones, ocho correctas. Dos fallos iniciales resultaron ser errores del test —el EPW rotula las horas 1–24, y guarda el bulbo seco con un decimal— y no del motor.

Coherencia física de cada escenario: la humedad absoluta debe seguir a la temperatura según Clausius-Clapeyron a HR constante (~6.2 %/K). Los cuatro escenarios de Lima quedan entre 7.60 y 7.79 %/K, o sea desvíos de +1.4 a +1.6 puntos porcentuales, bien por debajo del umbral de sospecha de 4 pp.

---

## 3. Inventario de archivos disponibles para Perú

| Ciudad | Estación | WMO | Elev. (m) | Zona climática | Ventanas | Año centroide (completo → 2011-2025) |
|---|---|---|---|---|---|---|
| Trujillo | Huanchaco-Pinillos Intl AP | 845010 | 32 | costa norte | 5 | 2001.6 → 2018.9 |
| Lima | Jorge Chávez Intl AP | 846280 | 34 | costa desértica | 5 | 1999.4 → 2017.6 |
| Piura | Iberico Intl AP | 844010 | 35 | costa norte | 5 | 1990.9 → 2017.4 |
| Iquitos | Secada Intl AP | 843770 | 93 | selva húmeda | 5 | 1997.8 → 2016.2 |
| Tacna | Ciriani Intl AP | 847820 | 469 | costa sur árida | 5 | 1986.9 → 2018.3 |
| Arequipa | Rodríguez Ballón AP | 847520 | 2562 | altiplano árido | 5 | 1987.0 → 2017.9 |
| Cusco | Velasco Astete Intl AP | 846860 | 3310 | altura | 5 | 1995.1 → 2018.2 |
| Juliaca | Manco Cápac AP | 847350 | 3826 | altiplano frío | 5 | 1998.4 → 2018.7 |

Procedencia: climate.onebuilding.org, región WMO 3 South America, carpeta PER_Peru. Los 40 archivos traen las 8760 filas completas y ninguno tiene huecos en bulbo seco.

**Sustituciones respecto al enunciado.** No existe estación en Puno ciudad ni en Trujillo ciudad. Se usó Juliaca-Manco (a 45 km de Puno, mismo régimen de altiplano) y Huanchaco-Pinillos, que es el aeropuerto que sirve a Trujillo. Chiclayo (844520) queda identificado como reserva no descargada.

**Condiciones de diseño:** 35 de los 40 archivos las traen. Las cinco ventanas de **Juliaca** no las incluyen, lo que impide usar ese archivo directamente para dimensionamiento sin calcularlas aparte.

---

## 4. Los cuatro análisis

### A · Auditoría de vintage

*Figura 7 · `Data/analisis_cuatro_v1.json` → `A_vintage`*

Para cada ciudad se tomó el TMYx de periodo completo como referencia y se midió, contra cada una de las cuatro ventanas, cuánto cambia la temperatura media anual y cuánto cambia el año centroide. Son 32 pares.

| Ajuste | n | Pendiente | r² |
|---|---|---|---|
| Todas las ciudades | 32 | +0.18 °C/década | 0.02 |
| Excluyendo la ventana 2004-2018 andina | 29 | +0.18 °C/década | 0.13 |

La pendiente es estable y su magnitud es la esperable del calentamiento observado. **El r² no lo es.** Incluso depurando los tres atípicos, el año centroide explica el 13 % de la variación. El ΔT aparente tiene mediana +0.35 °C y rango −0.91 a +3.64 °C.

La lectura práctica: **un TMYx de periodo completo no está "frío" en una cantidad predecible**. Está desplazado en una cantidad que depende de qué doce meses concretos le tocaron, y eso no se deduce del año centroide. Para Lima, que es el caso más usado del país, el desplazamiento es de +0.35 °C entre el archivo de periodo completo (centroide 1999.4) y el de 2011-2025 (centroide 2017.6). Un consultor que morfe desde el archivo completo hacia 2050 está contando ese tercio de grado dos veces: una vez como calentamiento ya ocurrido y otra como proyección.

**Hallazgo colateral, y probablemente el más accionable.** Al comparar cada ventana contra la mediana de su propia ciudad, los únicos tres atípicos son la misma ventana en las tres estaciones de altura:

| Ciudad | Elev. | Ventana | Media anual | Mediana de la ciudad | Diferencia |
|---|---|---|---|---|---|
| Cusco | 3310 m | 2004-2018 | 12.29 °C | 9.33 °C | **+2.96 °C** |
| Arequipa | 2562 m | 2004-2018 | 14.68 °C | 13.48 °C | +1.20 °C |
| Juliaca | 3826 m | 2004-2018 | 7.77 °C | 9.39 °C | **−1.62 °C** |

Ninguna estación costera muestra nada parecido. Juliaca 2004-2018 además trae autocorrelación de la media diaria de 0.377 frente a 0.845 en sus otras cuatro ventanas: no es un sesgo de nivel, es otra estructura temporal. Un patrón que aparece solo en altura apunta a cobertura METAR deficiente en los Andes durante ese periodo. **Recomendación: no usar la ventana 2004-2018 para ciudades andinas peruanas.**

### B · Deltas climáticos por zona

*Figuras 3 y 4 · `B_deltas_por_zona`*

Base: TMYx 2011-2025. Escenarios: ensemble CMIP6 de FWG a 2050.

| Ciudad | Elev. | ΔT SSP2-4.5 | ΔT SSP5-8.5 | ΔW SSP2-4.5 | GH b24 hoy → 2050 (SSP2-4.5) |
|---|---|---|---|---|---|
| Trujillo | 32 m | +1.49 °C | +1.95 °C | +1.46 g/kg | 184 → 890 °C·h |
| Lima | 34 m | +1.51 °C | +1.99 °C | +1.36 g/kg | 1 227 → 2 907 °C·h |
| Piura | 35 m | +1.40 °C | +1.83 °C | +1.53 g/kg | 15 873 → 22 352 °C·h |
| Iquitos | 93 m | +1.71 °C | +2.30 °C | +1.58 g/kg | 20 907 → 33 724 °C·h |
| Tacna | 469 m | +1.72 °C | +2.28 °C | +1.02 g/kg | 1 210 → 2 868 °C·h |
| Arequipa | 2562 m | +1.74 °C | +2.29 °C | +1.02 g/kg | 0 → 49 °C·h |
| Cusco | 3310 m | +1.73 °C | +2.26 °C | +1.07 g/kg | 1 → 11 °C·h |
| Juliaca | 3826 m | +1.83 °C | +2.41 °C | +0.93 g/kg | 0 → 1 °C·h |

El calentamiento **no es uniforme**: bajo SSP2-4.5 la dispersión entre ciudades es de 0.43 °C y correlaciona con la elevación (r = +0.73). Es calentamiento dependiente de elevación, un fenómeno bien documentado en los Andes.

Pero **el mapa térmico y el mapa energético no coinciden**. Juliaca tiene el mayor ΔT del país y su carga de enfriamiento pasa de 0 a 1 °C·h al año: irrelevante. Iquitos tiene un ΔT intermedio y su carga pasa de 20 907 a 33 724 °C·h, un aumento de 12 817 °C·h que es, en términos absolutos, el mayor del país.

**La carga latente pesa más que la sensible en la selva y la costa norte.** Iquitos gana +1.58 g/kg y Piura +1.53 g/kg de humedad absoluta, frente a +0.93 g/kg de Juliaca. En un clima ya saturado, ese incremento se traduce en carga de deshumidificación que un análisis de solo bulbo seco no ve. Para Iquitos, las horas sobre 26 °C pasan de 3 237 a 5 210 al año bajo SSP2-4.5 — del 37 % al 59 % del año.

Un contraste que conviene tener presente al leer porcentajes: en Trujillo la carga de enfriamiento se multiplica por 4.8, y en Piura solo por 1.4. Pero el aumento absoluto de Trujillo es de 706 °C·h y el de Piura de 6 479 °C·h. **El múltiplo grande está sobre la base pequeña.**

### C · Convergencia de métodos (solo Lima)

*Figura 8 · `C_convergencia_metodos`*

Los dos números que circulan no son comparables tal cual, porque parten de líneas base distintas. Alineados a temperatura absoluta de 2050:

| | Temperatura media anual |
|---|---|
| TMYx periodo completo (centroide 1999.4) | 19.28 °C |
| TMYx 2011-2025 (centroide 2017.6) | 19.63 °C |
| **Meteonorm 2050, RCP8.5 (CMIP5)** — no verificado aquí | **20.93 °C** |
| **FWG 2050, SSP5-8.5 (CMIP6)** | **21.62 °C** |

**Divergencia: +0.70 °C.** El desfase entre las dos líneas base es de +0.35 °C, o sea que la mitad de la diferencia entre los dos "ΔT" publicados (+1.65 contra +1.99) es puro artefacto de qué archivo se tomó como presente.

Tres advertencias, en orden de importancia:

- **RCP8.5 y SSP5-8.5 no son el mismo escenario.** Forzamiento radiativo similar a 2100, pero trayectorias, generación de modelos (CMIP5 vs CMIP6) y sensibilidad climática distintas. Esto es una comparación indicativa, no una validación cruzada.
- **El archivo Meteonorm no estuvo disponible** para esta auditoría. Los valores citados provienen del enunciado del proyecto y no fueron verificados aquí. Si esos valores fueran incorrectos, la magnitud de la divergencia cambia; la conclusión cualitativa —que hay que declarar la línea base antes de comparar métodos— se sostiene igual.
- Convergencia entre métodos independientes sería un argumento fuerte. Lo que hay es divergencia de 0.70 °C, que en el contexto de un ΔT de ~2 °C es un tercio de la señal.

### D · Firma de síntesis

*Figura 5 · `D_firma_sintesis`*

Estructura temporal de los archivos base (TMYx 2011-2025):

| Ciudad | Autocorrelación lag 1 | Racha cálida máx. | Rango diario medio |
|---|---|---|---|
| Iquitos | 0.544 | 5 d | 8.57 °C |
| Cusco | 0.716 | 11 d | 12.38 °C |
| Arequipa | 0.821 | 5 d | 12.30 °C |
| Juliaca | 0.845 | 9 d | 15.02 °C |
| Piura | 0.963 | 14 d | 10.19 °C |
| Trujillo | 0.967 | 33 d | 3.73 °C |
| Tacna | 0.978 | 18 d | 8.09 °C |
| Lima | 0.982 | 18 d | 4.46 °C |

La costa peruana tiene persistencia altísima (0.96–0.98) y rango diario pequeño (3.7–4.5 °C en Lima y Trujillo): es el régimen de estrato marino. La selva tiene la persistencia más baja del país (0.544) porque su variabilidad diaria es ruido convectivo sobre una media casi constante.

**Efecto del morphing:** máximo |Δautocorrelación| = 0.047 sobre 16 casos, máximo |Δrango diario| = 0.151 °C, y la racha cálida máxima **no cambia en ninguno de los 16 casos**. Esto es lo esperable: el morphing desplaza y escala una serie existente, no la regenera.

**Lo que este análisis NO puede responder.** La pregunta del proyecto era si los archivos *sintéticos* subestiman los episodios cálidos multi-día. Responderla exige un archivo generado por síntesis estocástica —Meteonorm— que no estuvo disponible. Lo único que se puede afirmar es que FWG no degrada la estructura. El dato previo de que Meteonorm baja la autocorrelación de Lima a 0.929 frente a 0.963 de un archivo medido apunta en la dirección de la hipótesis, pero no se verificó aquí. **Esta es la limitación más seria del trabajo.**

---

## 5. Implicancias prácticas para quien simula edificios en Perú

1. **Mira el año centroide antes de usar un TMYx.** Está en la cabecera, mes a mes. Si vas a morfar a futuro, parte de la ventana más reciente, no del periodo completo: si no, cuentas dos veces el calentamiento ya ocurrido. En Lima ese doble conteo son 0.35 °C.
2. **No uses la ventana 2004-2018 para Cusco, Arequipa o Juliaca.** Los tres archivos se apartan de sus hermanos de forma que no es climática.
3. **En Iquitos y Piura, dimensiona por carga latente.** El aumento de humedad absoluta (+1.5 a +1.6 g/kg a 2050) pesa más en el equipo que el de bulbo seco, y no aparece si solo miras temperatura.
4. **En la sierra, el calentamiento no es un problema de enfriamiento.** Juliaca gana +1.83 °C y sigue sin carga de refrigeración. El efecto relevante ahí es sobre calefacción y confort en horas frías, no sobre aire acondicionado.
5. **Declara siempre escenario, horizonte y línea base con su periodo.** "ΔT +1.65 °C" no significa nada sin decir contra qué archivo. La mitad de la discrepancia entre métodos del Análisis C era eso.
6. **Los SSP5-8.5 son casos de estrés, no pronósticos.** Úsalos para dimensionar el peor caso, no para prometer un resultado.
7. **Si necesitas condiciones de diseño para Juliaca, calcúlalas.** El archivo no las trae en ninguna de sus cinco ventanas.

---

## 6. Limitaciones declaradas

- **Ningún archivo TMY representa un evento El Niño.** En la costa peruana ese es un riesgo más inmediato y de mayor magnitud que la tendencia de fondo. Un TMYx es, por construcción, el mes típico: elimina justamente el año anómalo que domina el diseño real.
- **Los modelos climáticos globales tienen sesgos conocidos en el Pacífico oriental tropical.** La surgencia de Humboldt y el ENSO están mal resueltos a resolución de GCM. Las proyecciones para la costa peruana son menos confiables que para latitudes medias, y eso afecta a Lima, Trujillo, Piura y Tacna: la mitad de la muestra.
- **La irradiancia proviene de reanálisis, no de medición.** Jorge Chávez es estación METAR y no mide irradiancia. Los 2 177 kWh/m² anuales que el archivo de Lima reporta son altos para una costa con estrato persistente —la panza de burro—, más altos que Cusco (1 991) pese a los 3 276 m de diferencia de altura. **Ese valor merece contraste con medición terrestre antes de usarse para fotovoltaica o ganancia solar.**
- **El archivo Meteonorm no estuvo disponible.** El Análisis C es parcial y el D queda a medias por la misma causa.
- **La comparación RCP8.5 contra SSP5-8.5 no es estrictamente válida** como validación cruzada.
- **Ensemble de 23 modelos, sin desagregar por modelo.** No se reporta la dispersión intermodelo, que es una fuente de incertidumbre de magnitud comparable a la diferencia entre escenarios.
- **Ocho estaciones para un país con la diversidad climática de Perú es poco.** No hay representación de la ceja de selva, ni de la sierra norte, ni de altitudes intermedias entre 500 y 2500 m.
- **Nada de esto constituye dato de cumplimiento** para EDGE ni ninguna otra certificación.

---

## 7. Referencias y procedencia

- **Archivos TMYx:** climate.onebuilding.org, región WMO 3 South America, carpeta PER_Peru. Descarga directa sin credenciales, 26 de julio de 2026. Manifiesto completo con URL por archivo en `Data/manifiesto_descarga_v1.csv`.
- **Future Weather Generator v4.2.0**, ADAI / Universidade de Coimbra, future-weather-generator.adai.pt. Licencia CC BY-NC-SA. Ayuda de línea de comandos completa en `Context/log_fwg.txt`.
- **CMIP6**, ensemble de 23 modelos empaquetados en el JAR de FWG.
- **Magnus-Tetens** para presión de saturación de vapor; razón de mezcla en g/kg de aire seco.
- **Meteonorm 8.0.2**, valores citados desde el enunciado del proyecto, **no verificados en esta auditoría**.

### Trazabilidad

| Documento | Contenido |
|---|---|
| `Context/SUPUESTOS.md` | los 7 supuestos y fallos, ordenados por impacto |
| `Context/DECISIONS.md` | las 14 decisiones con su justificación |
| `Context/environment.md` | versiones exactas y prueba de conectividad |
| `Data/inventario_epw.csv` | procedencia archivo por archivo |
| `Data/metricas_todas_v1.csv` | métricas de los 40 TMYx |
| `Data/metricas_escenarios_v1.csv` | métricas de bases y escenarios 2050 |
| `Data/analisis_cuatro_v1.json` | resultados numéricos completos de los cuatro análisis |
| `Final Results/AUTOAUDITORIA.md` | dónde atacaría un revisor externo |
