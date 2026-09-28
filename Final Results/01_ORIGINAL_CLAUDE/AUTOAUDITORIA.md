# Autoauditoría

*Documento interno. Existe para ahorrarte tiempo de revisión, no para quedar bien.*

---

## ¿Qué conclusión de este informe es la MÁS débil?

**El Análisis C, la convergencia de métodos.** No es débil por un matiz: es débil porque uno de los dos términos de la comparación no existe en el proyecto.

El archivo Meteonorm 8.0.2 RCP8.5 2050 de Lima no está en ninguna carpeta accesible. Busqué `.epw` y patrones `meteonorm`/`RCP` en los dos montajes y no aparece. Los valores que uso —ΔT +1.65 °C, autocorrelación 0.929— vienen del enunciado del propio proyecto. **No los verifiqué. Los cité.**

Eso significa que la cifra de titular del Análisis C, la divergencia de +0.70 °C, es una resta donde uno de los sumandos es un dato de segunda mano. Si ese +1.65 °C fuera en realidad +1.85, la divergencia cae a 0.50 y el hallazgo pierde fuerza. Si fuera +1.25, sube a 1.10 y la gana.

Lo que sí es mío y sí es verificable: el desfase de +0.35 °C entre las dos líneas base de Lima, y la observación de que la mitad de la diferencia entre los ΔT publicados es artefacto de qué archivo se llamó "presente". Eso se sostiene aunque el número de Meteonorm esté mal.

La segunda más débil es el **Análisis D**, y por la misma causa. Verifiqué que FWG preserva la estructura temporal, lo cual era el resultado *esperable* —un morphing escala una serie existente, sería noticia que la rompiera— y no verifiqué lo que el proyecto quería saber, que era si un archivo sintetizado la degrada. Respondí la mitad fácil.

---

## ¿Qué dato falta que cambiaría materialmente los resultados?

**Uno, y es el mismo: un archivo generado por síntesis estocástica.** Con el Meteonorm de Lima en la mano, el Análisis C se vuelve una comparación real y el D pasa de "el morphing no rompe nada" a responder la pregunta original. Son dos de los cuatro análisis del proyecto los que dependen de un solo archivo ausente.

**Segundo: irradiancia medida en la costa.** El archivo de Lima reporta 2 177 kWh/m² anuales, más que Cusco (1 991 kWh/m²) que está 3 276 m más alto y sin estrato encima. Eso no me cuadra físicamente. Puede ser correcto —Cusco tiene estación húmeda con mucha nubosidad convectiva— pero también puede ser que el reanálisis no resuelva la panza de burro. No tengo forma de distinguir las dos cosas sin un piranómetro. Lo dejé como limitación declarada, pero si alguien va a usar estos archivos para fotovoltaica, ese número es el que primero hay que contrastar.

**Tercero: la dispersión intermodelo.** Corrí el ensemble de 23 modelos CMIP6 y reporto la media. No reporto la desviación entre modelos, que en proyecciones regionales suele ser del mismo orden que la diferencia entre escenarios. Un ΔT de "+1.51 °C bajo SSP2-4.5" suena más preciso de lo que es. FWG guarda las variables por modelo en `03_model_variables/`; el dato está, no lo procesé.

---

## ¿Dónde tuve que asumir más de lo que me habría gustado?

**En las estaciones sustitutas.** El proyecto pedía Puno y Trujillo. Usé Juliaca y Huanchaco. Huanchaco *es* el aeropuerto de Trujillo, así que ahí no hay problema. Juliaca está a 45 km de Puno y a 3826 m contra los 3827 de Puno, pero Puno está a orillas del Titicaca y Juliaca no. El lago modera la temperatura y el rango diario de forma apreciable. **Juliaca es más extremo que Puno.** Lo traté como "altiplano frío" sin más, y para una tipología de altiplano genérico vale, pero no es intercambiable con Puno ciudad.

**En la atribución del atípico 2004-2018.** Encontré que las tres estaciones andinas se desvían en esa ventana y en ninguna otra, y ninguna costera lo hace. Escribí que apunta a cobertura METAR deficiente en los Andes. **Eso es una inferencia, no una comprobación.** No fui a los registros de la estación a contar horas faltantes. El patrón es real y el diagnóstico es plausible; la causa concreta no la verifiqué.

**En la elección de la base de morphing.** Usé la ventana 2011-2025 razonando que es la menos envejecida. Es defendible, pero también es la de registro más corto y por tanto la más expuesta a que un solo año anómalo pese mucho. No comparé cómo cambiarían los resultados morfando desde 2009-2023. Debería haberlo hecho: es barato y habría dado una banda de sensibilidad.

---

## Si un revisor externo quisiera atacar este trabajo, ¿por dónde entraría?

**1. Por el r² de 0.13 del Análisis A.** Diría: "presentas una pendiente de +0.18 °C/década con un r² de 0.13 y n=29; eso no es una relación, es una nube de puntos con una recta encima". Y tendría parte de razón. Mi defensa es que el hallazgo *es* precisamente que la relación es débil, y que lo digo en el titular. Pero si alguien cita solo el "+0.18 °C/década" fuera de contexto, el informe habrá fallado. **Es el riesgo de mala cita más grande del documento.**

**2. Por el n de las ciudades.** Ocho estaciones, y tres de ellas (Lima, Trujillo, Piura) en el mismo régimen costero. Para afirmar "el calentamiento escala con la altura, r = +0.73" tengo ocho puntos con un hueco enorme entre 469 m y 2562 m. Un revisor pediría estaciones intermedias antes de aceptar el gradiente. Existen en el catálogo; no las bajé porque el enunciado fijaba la lista.

**3. Por usar el ensemble sin desagregar.** Ya está dicho arriba. Un revisor de clima lo señalaría en el primer párrafo.

**4. Por la circularidad de validar FWG con FWG.** El Análisis D concluye que el morphing preserva la estructura temporal comparando la salida de FWG contra su propia entrada. Es una comprobación de consistencia interna, no una validación. Nada me dice que la estructura *preservada* sea la correcta para 2050 — solo que es la misma que hoy. De hecho es casi seguro que no lo sea: el cambio climático altera la persistencia de las olas de calor, y un morphing por construcción no puede capturar eso. **Esa es la crítica más seria que se le puede hacer al método completo, y el informe la menciona demasiado de pasada.**

**5. Por el salto de "archivo climático" a "implicancia de diseño".** La sección 5 recomienda dimensionar por carga latente en Iquitos. Eso lo deduzco de +1.58 g/kg de humedad absoluta, no de una simulación energética de un edificio real. Es una inferencia razonable de un ingeniero, pero no está respaldada por un cálculo de carga en este trabajo.

---

## Lo que no está roto pero conviene saber

- El motor `analizar_epw.py` está validado contra un EPW sintético, no contra otra implementación. Si tuviera un error sistemático compartido con mi test, no lo habría detectado. Un contraste contra las estadísticas de los `.stat` que vienen con cada TMYx sería una verificación independiente barata, y no la hice.
- Los archivos de 2080 están generados y sin analizar. Salieron gratis en la misma pasada de FWG. Si en algún momento interesa el horizonte largo, el dato ya está en `Temp/fwg/`.
- El proyecto vive en `P2\03_AUDITORIA_CLIMA_Archivos_EPW_Peru\` y no en la raíz de `PROJECTS\` como pedía el enunciado, porque el agente solo tenía montadas P1 y P2. Todas las rutas internas son relativas: mover la carpeta no rompe nada.
