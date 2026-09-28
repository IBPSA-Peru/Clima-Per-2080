# Herramienta interactiva sobre el impacto del cambio climático y confort térmico en el Perú hacia 2030, 2050 y 2080; y auditoría técnica de archivos EPW

**Autores:** Abelardo Tomás Palacios Hurtado & IBPSA Perú (Capítulo Peruano de la International Building Performance Simulation Association)  
**Acceso web interactivo:** [https://ibpsa-peru.github.io/Clima-Per-2080/](https://ibpsa-peru.github.io/Clima-Per-2080/)  
**Licencia:** Creative Commons Atribución 4.0 Internacional (CC BY 4.0) · Investigación y Acceso Abierto  

---

## Visión y Propósito

Este proyecto nace con una misión primordial: **acercar y hacer comprensible la ciencia del cambio climático y el confort térmico en el Perú** a tomadores de decisiones, directivos del sector público y privado, proyectistas, arquitectos, ingenieros, comunidad académica y ciudadanía en general.

En el Perú existía una doble problemática:
1. **La información sobre proyecciones climáticas solía estar confinada en informes densos** o en formatos incomprensibles para quienes definen políticas públicas, planes de inversión y proyectos de edificación.
2. **Las simulaciones energéticas y de confort higrotérmico en el país se han realizado históricamente a ciegas**, utilizando archivos climáticos (EPW) descargados sin verificar su procedencia, su año de referencia real ni su consistencia termodinámica.

Esta plataforma une ambos mundos: **comunicación climática visual, intuitiva e interactiva de primer nivel**, respaldada por una **rigurosa auditoría meteorológica y termodinámica de datos horarios** para ocho macroclimas representativos de la costa, sierra y selva peruanas hacia los horizontes 2030, 2050 y 2080.

---

## La Plataforma Interactiva (Visor Web)

El visor interactivo disponible en [ibpsa-peru.github.io/Clima-Per-2080](https://ibpsa-peru.github.io/Clima-Per-2080/) integra en una experiencia web fluida y bilingüe (Español / Inglés) los siguientes componentes:

1. **Marco Global IPCC AR6 & CMIP6:** Mapa mundial interactivo con anomalías de temperatura para 4 trayectorias socioeconómicas (SSP1-2.6, SSP2-4.5, SSP3-7.0 y SSP5-8.5) y análisis regional de puntos clave (Costa peruana, Amazonía, Andes, Océano Pacífico Tropical y Ártico).
2. **Escala Didáctica de Impacto Térmico:** ¿Qué significan realmente +1.0 °C, +1.5 °C, +2.0 °C o +3.0 °C? Desglose en 3 pilares clave: fisiología humana (estrés térmico y noches tropicales), física de la edificación (sobrecalentamiento de techos y demanda de climatización) y entorno natural (glaciares andinos y recursos hídricos).
3. **Explorador Climático por Horizontes (Hoy, 2030, 2050, 2080):** Transición animada entre horizontes temporales para 8 macroclimas (Lima, Trujillo, Piura, Arequipa, Cusco, Juliaca, Iquitos y Pucallpa).
4. **Climogramas Mensuales Dinámicos:** Rangos diarios de máximas y mínimas medias mes a mes, con aislamiento de series y cálculo de amplitudes térmicas.
5. **Comportamiento Psicrométrico Horario:** Nube de 1 460 horas anuales representativas que ilustra el acoplamiento físico entre temperatura de bulbo seco y humedad absoluta (consistencia según la ley de Clausius-Clapeyron).
6. **Metodología Auditada en 6 Etapas:** Stepper interactivo que documenta con métricas numéricas y KPIs cada paso del procesamiento de datos meteorológicos.
7. **Dictamen de Fiabilidad y Límites de Aplicación:** Evaluación transparente de fortalezas (temperatura de bulbo seco, consistencia física) y advertencias críticas (omisión del fenómeno de El Niño en años típicos, necesidad de calibrar la radiación solar satelital y cuantificación del efecto vintage en las líneas base).

---

## Respaldo Científico y Metodológico

Toda la plataforma se sustenta en una auditoría técnica profunda:

- **Inventario:** 40 archivos meteorológicos oficiales en formato EPW (TMYx) obtenidos de climate.onebuilding.org (Organización Meteorológica Mundial - WMO, Región 3).
- **Cobertura:** 8 ciudades que abarcan desde el nivel del mar (Trujillo, 32 m s. n. m.) hasta el altiplano andino (Juliaca, 3 826 m s. n. m.), pasando por la costa desértica, valles interandinos y la llanura amazónica.
- **Modelado Climático Futuro:** Generación de escenarios horarios mediante *morphing* con **Future Weather Generator (FWG v4.2.0)**, desarrollado por ADAI y la Universidad de Coímbra, integrando el ensamble multimodelo **CMIP6 (23 Modelos Climáticos Globales)** del Sexto Informe de Evaluación del IPCC (AR6).
- **Auditoría de Incertidumbre y Líneas Base:** Cuantificación del desfase histórico de líneas base (*vintage gap*: 1999 vs. 2018), demostrando que el 50 % de la divergencia entre metodologías proviene de la antigüedad de la línea base seleccionada y no de las ecuaciones del modelo.
- **Validación Termodinámica:** Verificación del cumplimiento de la ley de Clausius-Clapeyron: la humedad específica de los archivos transformados asciende entre 7.60 y 7.79 %/K, dentro del rango físico admisible (desviación de solo 1.5 pp frente al valor teórico de 6.2 %/K).

---

## Autoría, Dirección y Formulación Metodológica

- **Autor Principal, Dirección de Investigación e Ingeniería de Prompts:**  
  **Abelardo Tomás Palacios Hurtado**  
  *Especialista en Simulación Energética de Edificaciones y Arquitectura Bioclimática.*  
  - **Concepción y Dirección:** Formulación de hipótesis científicas, diseño conceptual y metodológico, toma de decisiones técnicas y supervisión integral de la auditoría meteorológica.
  - **Dirección Computacional y Prompts:** Redacción, iteración y calibración de todos los prompts de instrucción técnica para los entornos de IA a lo largo de todas las fases de la investigación.

- **Institución Promotora y Respaldante:**  
  **IBPSA Perú** (International Building Performance Simulation Association — Capítulo Peruano).

- **Asistencia Computacional por Inteligencia Artificial:**  
  Las herramientas de IA (**Claude / Cowork** en la fase de investigación inicial y **Google Antigravity** en la fase de publicación y difusión web) actuaron exclusivamente como **asistentes computacionales de ejecución y programación bajo la dirección técnica estricta, hipótesis y prompts formulados por Abelardo Tomás Palacios Hurtado**.

---

## Estructura del Repositorio

- `Final Results/web/index.html` — Visor web interactivo optimizado para despliegue en GitHub Pages (autocontenido, bilingüe ES/EN).
- `Final Results/INFORME_AUDITORIA_CLIMA_PERU.md` — Informe técnico completo y detallado de la auditoría.
- `Data/` — Inventario de 40 archivos EPW, métricas calculadas y bases de datos procesadas.
- `Scripts/` — Scripts de descarga, cálculo termodinámico, procesamiento de métricas y generación del visor.
- `Context/` — Manifiestos de supuestos, guías de publicación institucional y documentación metodológica.

---

## Historial de Versiones

| Versión | Fecha | Autor / Dirección Técnica | Asistencia IA | Descripción General |
|---|---|---|---|---|
| **v1.0** | Julio 2026 | Abelardo Tomás Palacios Hurtado (IBPSA Perú) | Cowork / Claude | Auditoría técnica y termodinámica de 40 archivos EPW para 8 macroclimas peruanos, generación de proyecciones climáticas futuras (CMIP6) y desarrollo de la primera versión del visor interactivo. |
| **v2.0** | Septiembre 2026 | Abelardo Tomás Palacios Hurtado (IBPSA Perú) | Antigravity | Rediseño para difusión pública institucional, incorporación del marco global del IPCC, plataforma interactiva bilingüe (español e inglés) y publicación en GitHub Pages. |

---

## Licencia y Citación Sugerida

Este proyecto se distribuye bajo licencia **Creative Commons Atribución 4.0 Internacional (CC BY 4.0)**. Se permite su libre uso, distribución y adaptación para investigación, educación, políticas públicas y ejercicio profesional en arquitectura e ingeniería, siempre que se cite la fuente:

> **Palacios Hurtado, A. T., & IBPSA Perú.** (2026). *Herramienta interactiva sobre el impacto del cambio climático y confort térmico en el Perú hacia 2030, 2050 y 2080; y auditoría técnica de archivos EPW*. International Building Performance Simulation Association - Capítulo Perú. https://ibpsa-peru.github.io/Clima-Per-2080/
