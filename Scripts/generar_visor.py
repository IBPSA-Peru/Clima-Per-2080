#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_visor.py — Construye el visor HTML interactivo de la auditoria.

Salida: "Final Results/web/index.html", UN solo archivo autocontenido.
Los datos van como JSON inline y todas las escenas se dibujan como SVG desde ese
dato. Sin CDN, sin servidor, sin imagenes. Los iconos son SVG de trazo, en linea.

Narrativa (v1.3.0): primero el numero que se busca —temperatura por horizonte—,
despues el examen de si ese numero es fiable. El orden inverso escondia el
resultado detras del metodo.

Fuentes que ensambla:
    Scripts/visor/plantilla.css   estilos
    Scripts/visor/plantilla.js    logica y dibujo
    Data/web/payload_v3.json      datos (lo produce preparar_payload)

Idempotente (SOP-02 H1). El HTML es SALIDA DE BUILD: no se edita a mano.

Uso: python Scripts/generar_visor.py
"""

from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TPL = RAIZ / "Scripts" / "visor"
WEB = RAIZ / "Final Results" / "web"

CAPS = [("ipcc", "Marco IPCC"), ("impacto", "¿Qué significa +1°C?"), ("dato", "El dato"), ("ciudades", "Por ciudad"), ("carga", "Qué implica"),
        ("metodo", "Cómo"), ("fiable", "¿Es fiable?"), ("limites", "Conclusiones"), ("referencias", "Referencias")]

# Iconos de trazo, geometricos, a juego con la tipografia. Sin dependencias.
ICO = {
    "flecha": '<svg class="ico" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "abajo": '<svg class="ico" viewBox="0 0 24 24" width="15" height="15"><path d="M12 5v14M6 13l6 6 6-6"/></svg>',
    "play": '<svg class="ico" viewBox="0 0 24 24"><path d="M7 4l12 8-12 8z"/></svg>',
    "sol": '<svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19"/></svg>',
    "onda": '<svg class="ico" viewBox="0 0 24 24"><path d="M2 9c3-3 5.5 3 8.5 0S16 6 19 9M2 15c3-3 5.5 3 8.5 0S16 12 19 15"/></svg>',
    "globo": '<svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19M12 2.5c2.5 2.6 3.8 6 3.8 9.5s-1.3 6.9-3.8 9.5c-2.5-2.6-3.8-6-3.8-9.5S9.5 5.1 12 2.5z"/></svg>',
    "archivo": '<svg class="ico" viewBox="0 0 24 24"><path d="M14 2.5H6.5a2 2 0 0 0-2 2v15a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V8z"/><path d="M14 2.5V8h5.5"/></svg>',
    "alerta": '<svg class="ico" viewBox="0 0 24 24"><path d="M12 3L2 20h20z"/><path d="M12 10v4M12 17.2v.1"/></svg>',
    "regla": '<svg class="ico" viewBox="0 0 24 24"><path d="M3 8h18v8H3z"/><path d="M7 8v3M11 8v4M15 8v3M19 8v4"/></svg>',
    "solanim": ('<svg class="ico solanim" viewBox="0 0 24 24" aria-hidden="true">'
        '<g class="rayos"><path d="M12 1.4v3M12 19.6v3M1.4 12h3M19.6 12h3'
        'M4.5 4.5l2.1 2.1M17.4 17.4l2.1 2.1M19.5 4.5l-2.1 2.1M6.6 17.4l-2.1 2.1"/></g>'
        '<circle class="nucleo" cx="12" cy="12" r="5"/>'
        '<path class="onda" d="M7 12.6c1.7-2 3.3-2 5 0s3.3 2 5 0"/></svg>'),
    "sello": '<svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5"/><path d="M7.5 12.5l3 3 6-6.5"/></svg>',
}


def html(d: dict) -> str:
    css = (TPL / "plantilla.css").read_text(encoding="utf-8")
    js = (TPL / "plantilla.js").read_text(encoding="utf-8")
    c = d["conv"]
    ciudades_lista = [x["n"] for x in d["ciudades"]]
    lima = next(x for x in d["ciudades"] if x["n"] == "Lima")
    L45, L85 = lima["s245"]["H"], lima["s585"]["H"]

    migas = "".join(f'<a href="#{i}">{t}</a>' for i, t in CAPS)

    def cap(n, t):
        return f'<div class="cap"><span class="num">{n}</span><span class="via"></span></div><h2>{t}</h2>'

    def pleg(titulo, veredicto, clase, cuerpo):
        return (f'<details class="pleg"><summary><span class="mas"></span>{titulo}'
                f'<span class="veredicto {clase}">{veredicto}</span></summary>'
                f'<div class="cuerpo">{cuerpo}</div></details>')

    ciud_btns_hero = "".join(f'<button class="ciudBtn {("on" if cn=="Lima" else "")}" onclick="pick(\'{cn}\')">{cn}</button>' for cn in ciudades_lista)
    ciud_btns_nube = "".join(f'<button class="ciudBtn {("on" if cn=="Lima" else "")}" onclick="pick(\'{cn}\')">{cn}</button>' for cn in ciudades_lista)

    pasos_data = [
        {
            "num": 1, "col": "#1a4f6e", "titulo": "1. Descargar",
            "desc": "40 archivos meteorológicos TMYx (Año Meteorológico Típico Extendido / Typical Meteorological Year) desde la plataforma pública climate.onebuilding.org (WMO - Organización Meteorológica Mundial).",
            "ev": [
                ("Ciudades auditadas", "8 ciudades del Perú"),
                ("Ventanas temporales por ciudad", "5 ventanas (1991-2005 a 2011-2025 y completo)"),
                ("Archivos EPW (EnergyPlus Weather)", "40 archivos descargados"),
                ("Fallos de descarga o archivos corruptos", "0 fallos"),
                ("Horas por cada archivo", "8 760 horas completas"),
                ("Huecos en temperatura de bulbo seco", "0 huecos (100 % de integridad)")
            ],
            "nota": "Cinco ventanas temporales por ciudad y no solo dos: con solo dos puntos temporales el análisis de tendencia histórica (vintage) forzaría una recta artificial."
        },
        {
            "num": 2, "col": "#2b6f9e", "titulo": "2. Leer cabecera",
            "desc": "De cada archivo EPW (EnergyPlus Weather) se extrae el año fuente de CADA MES del año. Su promedio ponderado determina el año centroide real del archivo.",
            "ev": [
                ("Lima · Periodo completo (1991-2020)", "Centroide año 1999.8"),
                ("Lima · Ventana reciente (2011-2025)", "Centroide año 2018.0"),
                ("Desfase temporal real", "18.2 años de diferencia"),
                ("ΔT previo ya ocurrido", "+0.35 °C de calentamiento histórico"),
                ("Archivos con centroide no legible", "0 de 40 archivos")
            ],
            "nota": "Ese incremento de +0.35 °C es calentamiento que YA ocurrió en Lima. Morfar proyecciones futuras partiendo del archivo de periodo completo contaría ese calentamiento dos veces."
        },
        {
            "num": 3, "col": "#3d8ab0", "titulo": "3. Medir",
            "desc": "Cálculo de ~120 métricas termodinámicas, bioclimáticas y temporales por cada archivo EPW (EnergyPlus Weather): estadística, carga térmica y persistencia temporal.",
            "ev": [
                ("Grados-hora de enfriamiento (CDD)", "Bases 18 °C, 24 °C, 26 °C y 28 °C"),
                ("Frecuencia de cruce de umbrales", "26 °C, 28 °C, 30 °C y 32 °C"),
                ("Autocorrelación temporal", "Lags horarios 1, 2 y 3 (inercia térmica)"),
                ("Rachas sobre percentil 90 (P90)", "Frecuencia y duración de olas de calor"),
                ("Autotest del motor de cálculo", "8 de 8 pruebas unitarias superadas")
            ],
            "nota": "El motor analítico se validó contra un archivo EPW sintético de propiedades físicas conocidas ANTES de procesar datos de estaciones reales."
        },
        {
            "num": 4, "col": "#7a9a86", "titulo": "4. Morfar (Morphing)",
            "desc": "La herramienta FWG (Future Weather Generator v4.2.0 - ADAI / Universidad de Coímbra) transforma la serie horaria aplicando modelos climáticos globales CMIP6 (Coupled Model Intercomparison Project Phase 6).",
            "ev": [
                ("Modelos climáticos globales (GCM) en ensemble", "23 modelos CMIP6"),
                ("Escenarios de emisiones evaluados", "SSP1-2.6, SSP2-4.5, SSP3-7.0 y SSP5-8.5"),
                ("Horizontes temporales proyectados", "Años 2050 y 2080"),
                ("Interpolación espacial de malla", "IDW (Ponderación por Distancia Inversa, 4 puntos)"),
                ("Efecto de Isla de Calor Urbano (UHI)", "Desactivado (auditoría meteorológica pura)"),
                ("Tasa de fallos en las 8 ciudades", "0 errores en ejecución")
            ],
            "nota": "El algoritmo morphing de FWG procesa y emite automáticamente los cuatro escenarios SSP (Shared Socioeconomic Pathways) para 2050 y 2080 en una sola pasada."
        },
        {
            "num": 5, "col": "#c78b3c", "titulo": "5. Comparar",
            "desc": "Contrastación de cada proyección futura contra su línea base histórica correspondiente y contra una herramienta independiente de síntesis climática (Meteonorm).",
            "ev": [
                ("Lima 2050 · SSP2-4.5 (FWG / CMIP6)", "21.14 °C (Media anual)"),
                ("Lima 2050 · SSP5-8.5 (FWG / CMIP6)", "21.62 °C (Media anual)"),
                ("Lima 2050 · Meteonorm (RCP8.5 / CMIP5)", "20.93 °C (Media anual)"),
                ("Divergencia entre métodos independientes", "+0.70 °C de discrepancia metodológica"),
                ("Desfase atribuible a la línea base (vintage)", "+0.35 °C por selección del archivo de origen")
            ],
            "nota": "La mitad de la discrepancia (+0.70 °C) observada entre estudios se debe al desfase del archivo histórico utilizado como presente (1999 vs. 2018) y no al modelo de proyección futura."
        },
        {
            "num": 6, "col": "#bd491a", "titulo": "6. Verificar",
            "desc": "Compuerta termodinámica fundamental según la ley física de Clausius-Clapeyron: la humedad absoluta debe aumentar coherentemente con el calentamiento del aire.",
            "ev": [
                ("Tasa física teórica a HR constante", "~6.2 % de vapor por Kelvin (+6.2 %/K)"),
                ("SSP1-2.6 observado (Sostenibilidad)", "7.60 %/K"),
                ("SSP2-4.5 observado (Intermedio / Central)", "7.73 %/K"),
                ("SSP3-7.0 observado (Rivalidad regional)", "7.64 %/K"),
                ("SSP5-8.5 observado (Muy altas emisiones)", "7.79 %/K"),
                ("Desviación máxima frente al límite físico", "1.59 pp vs. umbral de sospecha de 4.0 pp")
            ],
            "nota": "La respuesta higrotérmica se mantiene plenamente dentro del rango físico admisible: el morphing de FWG no desacopló la humedad relativa ni la temperatura."
        }
    ]

    cards_html = []
    for p in pasos_data:
        filas = "".join(f'<div class="pasoFila"><span>{k}</span><b>{v}</b></div>' for k, v in p["ev"])
        cards_html.append(f"""
        <div class="pasoCard">
          <div class="pasoCardTop">
            <span class="pasoBadge" style="background:{p['col']}">{p['num']}</span>
            <h4 style="color:{p['col']}">{p['titulo']}</h4>
          </div>
          <p class="pasoDesc">{p['desc']}</p>
          <div class="pasoTabla">{filas}</div>
          <div class="pasoAudit"><b>Nota técnica:</b> {p['nota']}</div>
        </div>""")
    pasos_grid_html = "".join(cards_html)

    logo_b64_file = RAIZ / "Data" / "web" / "ibpsa_logo_b64.txt"
    logo_b64 = logo_b64_file.read_text(encoding="ascii").strip() if logo_b64_file.exists() else ""

    return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>¿Qué temperatura hará en Perú en 2050?</title>
<style>{css}</style></head><body>
<div class="tip" id="tip" role="status" aria-live="polite"></div>

<header class="top"><div class="wrap">
  <div class="marca">
    <img src="data:image/png;base64,{logo_b64}" alt="Logo IBPSA Perú" class="marcaLogo" width="26" height="26">
    <span class="marcaTit">CLIMA <i>PERÚ</i> 2080 <span class="marcaSep">|</span> <span class="marcaOrg">IBPSA PERÚ</span></span>
  </div>
  <nav class="migas" aria-label="Capítulos">{migas}</nav>
</div></header>

<!-- ══ portada ══ -->
<section id="hero"><div class="wrap">
  <div class="heroGrid">
    <div>
      <div class="kicker">Auditoría Climática de Archivos EPW · IBPSA Perú</div>
      <h1 id="heroTit">Lima tendrá <em>{L45['a2050']['T']:.1f} °C</em> de media en 2050</h1>
      <p class="subtit" id="heroSubtit">Eso bajo el escenario central SSP2-4.5 (Trayectoria Socioeconómica Compartida Intermedia). Bajo el de estrés SSP5-8.5 (Muy Altas Emisiones),
      {L85['a2050']['T']:.1f} °C. Ocho ciudades peruanas, cuatro horizontes y una pregunta
      incómoda: ¿cuánto puedes fiarte de estos archivos?</p>
      
      <div class="ciudCtrl" id="heroCiudades" role="group" aria-label="Ciudad seleccionada">
        <span class="lbl">Ciudad:</span>
        {ciud_btns_hero}
      </div>

      <div class="grande" id="grande"></div>
    </div>
    <div class="solCol">
      <div id="heroViz"></div>
      <div class="solCtrl">
        <button class="solBtn on" onclick="solIr(0)">Hoy</button>
        <button class="solBtn" onclick="solIr(1)">2030</button>
        <button class="solBtn" onclick="solIr(2)">2050</button>
        <button class="solBtn" onclick="solIr(3)">2080</button>
        <button class="solPlay" id="solPlay" onclick="solSeguir()">▶ Animar</button>
      </div>
      <p class="solPie">Cada rayo es un mes en una <b>escala fija calibrada de -6 a 36 °C</b> (anillos en 0°, 10°, 20° y 30°). Toca una ciudad para comparar su longitud y posición en el dial.</p>
    </div>
  </div>
  <div class="baja">{ICO['abajo']}<span>Los números</span></div>
</div></section>

<!-- ══ marco global IPCC y CMIP6 ══ -->
<section id="ipcc"><div class="wrap">
  {cap('Marco Global IPCC & CMIP6', 'Escenarios mundiales de temperatura y modelos climáticos')}
  <p class="lead">Las proyecciones se fundamentan en el <b>IPCC (Sexto Informe AR6)</b> y el ensamble multimodelo <b>CMIP6 (23 modelos globales)</b>. 
  Explora cómo se distribuye el calentamiento en el mapa mundial según el escenario socioeconómico (SSP) y el horizonte temporal:</p>

  <div class="ipccCtrl">
    <div class="seg" id="ipccEscen" role="group" aria-label="Escenarios de emisiones IPCC">
      <button class="on" data-esc="ssp126" onclick="setIpccEsc('ssp126')">SSP1-2.6 · Sostenibilidad (París)</button>
      <button data-esc="ssp245" onclick="setIpccEsc('ssp245')">SSP2-4.5 · Trayectoria Central</button>
      <button data-esc="ssp370" onclick="setIpccEsc('ssp370')">SSP3-7.0 · Rivalidad Regional</button>
      <button data-esc="ssp585" onclick="setIpccEsc('ssp585')">SSP5-8.5 · Caso de Estrés (Fósil)</button>
    </div>
    <div class="seg" id="ipccHz" role="group" aria-label="Horizonte temporal IPCC">
      <button class="on" id="ipccH2050" onclick="setIpccHz(2050)">Año 2050</button>
      <button id="ipccH2080" onclick="setIpccHz(2080)">Año 2080</button>
    </div>
  </div>

  <div class="panel ipccPanel">
    <div class="ipccMapHeader">
      <div>
        <h3 id="ipccMapTit">Calentamiento Global Proyectado: SSP1-2.6 (Año 2050)</h3>
        <p id="ipccMapSubtit">Anomalía de temperatura superficial (°C) respecto a la era preindustrial (1850-1900).</p>
      </div>
      <div class="ipccGlobalBadge">
        <span class="lbl">Media Global:</span>
        <b id="ipccGlobalVal">+1.5 °C</b>
      </div>
    </div>

    <div id="ipccWorldMap"></div>
    <div id="ipccPinDetail" class="ipccPinBox">💡 Haz clic o pasa el cursor sobre los puntos destacados del mapa (Costa de Perú, Amazonía, Andes, Ártico, Océano) para explorar los fenómenos climáticos regionales.</div>

    <div class="ipccBarraWrap">
      <span class="lbl">Anomalía térmica proyectada (°C):</span>
      <div class="ipccBarra"></div>
      <div class="ipccBarraNums">
        <span>+0.5°</span>
        <span>+1.0°</span>
        <span>+1.5°</span>
        <span>+2.0°</span>
        <span>+3.0°</span>
        <span>+4.0°</span>
        <span>+5.0°</span>
        <span>+7.0°+</span>
      </div>
    </div>
  </div>

  <div class="sspGrid" id="sspCardsGrid"></div>
</div></section>

<!-- ══ qué significa +1 °C, +2 °C o +3 °C: 3 pilares didácticos (Cuerpo, Edificio, Entorno) ══ -->
<section id="impacto"><div class="wrap">
  {cap('Escala de Impacto Térmico', '¿Qué significan realmente +1 °C, +2 °C o +3 °C en el cuerpo, el edificio y el entorno?')}
  <p class="lead">Un aumento en la <b>media anual</b> desplaza la curva climática entera, multiplicando de forma no lineal las olas de calor, el estrés fisiológico, el consumo energético en edificios y el deshielo andino. Selecciona un nivel de calentamiento para ver sus consecuencias directas:</p>

  <!-- Selector de Nivel de Calentamiento -->
  <div class="impCtrl" id="impCtrl" role="group" aria-label="Nivel de Calentamiento Térmico">
    <button class="impBtn n1" data-imp="s10" onclick="setImpactoNivel('s10')"><span class="impBtnBadge">+1.0 °C</span> Actual (Perú Hoy)</button>
    <button class="impBtn n2" data-imp="s15" onclick="setImpactoNivel('s15')"><span class="impBtnBadge">+1.5 °C</span> Meta París (SSP1-2.6)</button>
    <button class="impBtn n3 on" data-imp="s20" onclick="setImpactoNivel('s20')"><span class="impBtnBadge">+2.0 °C</span> Umbral Crítico (SSP2-4.5 · 2050)</button>
    <button class="impBtn n4" data-imp="s30" onclick="setImpactoNivel('s30')"><span class="impBtnBadge">+3.0 °C+</span> Estrés Severo (SSP5-8.5 · 2080)</button>
  </div>

  <!-- Contenedor dinámico de los 3 pilares visuales -->
  <div id="impHeaderBox" class="impHeaderBox"></div>
  <div id="impGrid3" class="impGrid3"></div>
</div></section>

<!-- ══ 01 · el dato ══ -->
<section id="dato"><div class="wrap">
  {cap('01 · El dato', 'Elige un horizonte y mira el país entero')}
  <p class="lead">Temperatura media anual de cada ciudad. Cambia de horizonte y las cifras
  y el mapa <b>transicionan</b> al nuevo valor. Toca una ciudad para ver su ficha completa:
  percentil 99, máxima del año, humedad y carga de enfriamiento.</p>
  <div class="horiz" role="group" aria-label="Horizonte temporal">
    <button data-h="hoy" onclick="setH('hoy')">Hoy<small>Línea base TMYx 2011-2025</small></button>
    <button data-h="a2030" onclick="setH('a2030')">2030<small>Interpolado</small></button>
    <button class="on" data-h="a2050" onclick="setH('a2050')">2050<small>Modelado CMIP6</small></button>
    <button data-h="a2080" onclick="setH('a2080')">2080<small>Modelado CMIP6</small></button>
  </div>
  <div class="ctrl">
    <div class="seg" id="segE" role="group" aria-label="Escenario de emisiones">
      <button class="on" data-e="s245" onclick="setE('s245')">SSP2-4.5 · Escenario Central (Shared Socioeconomic Pathway)</button>
      <button data-e="s585" onclick="setE('s585')">SSP5-8.5 · Escenario de Estrés (Shared Socioeconomic Pathway)</button>
    </div>
    <span class="nota">Los escenarios SSP 8.5 representan casos de estrés severo para dimensionar el peor caso ante cambio climático, no pronósticos deterministas.</span>
  </div>
  <div class="rej" id="rej"></div>
  <div class="aviso"><h4>2030 es interpolación, no modelo</h4>
    <p>El generador FWG (Future Weather Generator / ADAI / Univ. Coímbra) solo emite los horizontes 2050 y 2080 basados en modelos globales CMIP6 (Coupled Model Intercomparison Project Phase 6). La columna de 2030 interpola
    linealmente entre la línea base TMYx (Año Meteorológico Típico Extendido) y 2050. Como la aceleración del calentamiento no es estrictamente lineal en el tiempo,
    ese valor probablemente <b>se queda corto</b> respecto a la trayectoria real. Está marcado como tal en toda la página.</p></div>
</div></section>

<!-- ══ 02 · por ciudad ══ -->
<section id="ciudades"><div class="wrap">
  {cap('02 · Por ciudad', 'Cómo se siente: máximas y mínimas, mes a mes')}
  <p class="lead">Una media anual no se percibe. Lo que se nota es la máxima de febrero y la
  mínima de agosto. <b>Enciende y apaga horizontes</b> en la leyenda; con doble clic aíslas
  uno solo y aparecen las cifras de cada mes.</p>
  <div class="panel" style="margin-bottom:16px">
    <div style="font-size:13px;font-weight:700;letter-spacing:.3px;margin-bottom:8px"
      id="climoTit">Mes a mes</div>
    <div class="cgLeg" id="cgLeg" role="group" aria-label="Horizontes visibles"></div>
    <div id="climo"></div>
    <div class="cgInfo" id="cgInfo"></div></div>
  <p class="lead">Ocho estaciones meteorológicas de superficie (METAR / WMO), de los 32 m de Trujillo a los 3 826 m de Juliaca.
  <b>El calentamiento escala con la altura</b>: la sierra sube más que la costa, aunque su
  consecuencia energética sea menor.</p>
  <div class="split">
    <div class="panel"><div id="mapa"></div></div>
    <div class="panel ficha" id="ficha"></div>
  </div>
  <div class="panel" style="margin-top:16px">
    <div style="font-size:13px;font-weight:700;letter-spacing:.3px;margin-bottom:6px"
      id="trayTit">Trayectoria</div>
    <div class="cgLeg" id="trLeg" role="group" aria-label="Horizontes visibles"></div>
    <div id="tray"></div></div>
  <div class="panel" style="margin-top:16px">
    <div class="brCab"><span>Las ocho ciudades · clic en cualquier barra para fijar
      esa ciudad y ese horizonte</span>
      <span class="brOrd">ordenar por <span class="seg" id="brSort"></span></span></div>
    <div id="barras"></div></div>
</div></section>

<!-- ══ 03 · qué implica ══ -->
<section id="carga"><div class="wrap">
  {cap('03 · Qué implica', 'Comportamiento psicrométrico hora a hora')}
  <p class="lead" id="nbLead">Cada punto es una hora del año para la ciudad seleccionada, situada por su temperatura y su humedad
  absoluta. Al proyectar a horizontes futuros, la nube se desplaza <b>en diagonal</b>: el aire más cálido
  retiene mayor cantidad de vapor. Eso es Clausius-Clapeyron, visualizado hora a hora.</p>
  
  <div class="ciudCtrl" id="nbCiudades" role="group" aria-label="Seleccionar ciudad para psicrometría">
    <span class="lbl">Ciudad:</span>
    {ciud_btns_nube}
  </div>

  <div class="ctrl">
    <button class="btn" id="btnN" onclick="reproducir()">{ICO['play']}<span> Recorrer hasta 2080</span></button>
    <div class="pasos" id="nbPasos" role="group" aria-label="Horizonte de la nube">
      <button class="pasoN on" onclick="irNube(0)">Hoy</button>
      <button class="pasoN" onclick="irNube(1)">2030</button>
      <button class="pasoN" onclick="irNube(2)">2050</button>
      <button class="pasoN" onclick="irNube(3)">2080</button>
    </div>
    <div class="seg" id="nbModo" role="group" aria-label="Qué codifica el color">
      <button class="on" data-m="mes" onclick="nbSetCol('mes')">Color: mes</button>
      <button data-m="hora" onclick="nbSetCol('hora')">Color: hora del día</button>
    </div>
    <span class="nota" id="estado">Hoy · TMYx 2011-2025</span>
  </div>
  <div class="panel"><div id="nube"></div>
    <div class="nbLeg" id="nbLeg" role="group" aria-label="Filtrar por mes u hora"></div>
    <div class="nbPunto"><b>Cada punto es una hora del año</b> — una de cada seis, 1 460 en
    total. Su posición horizontal es la temperatura del aire y la vertical, cuánto vapor
    lleva. El color indica el mes (o la hora del día, si cambias el modo): clic en la leyenda
    para aislar uno. Los meses de verano se agrupan arriba a la derecha —calor con humedad— y
    los de invierno abajo a la izquierda.</div></div>
  <div class="aviso"><h4>El múltiplo térmico engaña sin su valor absoluto</h4>
    <p>En Trujillo la carga de enfriamiento se multiplica por 4.8 y en Piura solo por 1.4.
    Pero Trujillo sube 706 °C·h y Piura 6 479 °C·h. El múltiplo grande está sobre la base pequeña.</p></div>
</div></section>

<!-- ══ 04 · cómo ══ -->
<section id="metodo"><div class="wrap">
  {cap('04 · Cómo', 'Seis pasos del proceso de auditoría meteorológica')}
  <p class="lead">De un archivo meteorológico descargado a una proyección al 2080. Estos son los seis pasos de la metodología, con sus métricas auditadas, variables comprobadas y hallazgos reales:</p>
  
  <div class="pasosGrid">
    {pasos_grid_html}
  </div>

  <div class="glosarioGrid">
    <div class="glosCard">
      <h4>¿Qué es «Morphing»?</h4>
      <p><b>Ajuste horario:</b> Toma las 8 760 horas medidas en la estación base y les aplica las anomalías climáticas mensuales proyectadas por los modelos globales.</p>
      <p><b>Por qué importa:</b> Conserva la física del sitio, la oscilación día-noche y los vientos reales, adaptándolos a las temperaturas de 2050 y 2080.</p>
    </div>
    <div class="glosCard">
      <h4>¿Qué es un «Ensemble»?</h4>
      <p><b>Consenso multimodelo:</b> Combina y promedia las proyecciones de 23 modelos climáticos globales independientes (NOAA, NASA, Max Planck).</p>
      <p><b>Por qué importa:</b> Ningún modelo individual es infalible; promediar el conjunto cancela sesgos y entrega una señal climática de consenso mucho más sólida.</p>
    </div>
  </div>

  <div class="aviso" style="margin-top:24px"><h4>Verificación física de Clausius-Clapeyron (Paso 6)</h4>
    <p>Al calentarse el aire a humedad relativa constante, la humedad absoluta debe subir ~6.2 % por cada °C (+6.2 %/K). Los archivos transformados con FWG arrojan entre <b>7.60 y 7.79 %/K</b> (apenas 1.5 pp de desviación frente a la teoría, muy por debajo del umbral de sospecha de 4.0 pp). Esto confirma que el morphing preservó la consistencia termodinámica.</p></div>
</div></section>

<!-- ══ 05 · ¿es fiable? ══ -->
<section id="fiable"><div class="wrap">
  {cap('05 · ¿Es fiable?', 'Ahora sí: cuánto puedes creerte esas cifras')}
  <p class="lead">Los números de arriba salen de archivos climáticos que no habían sido auditados en conjunto. Esto es
  lo que se encontró al examinarlos en detalle, pregunta por pregunta. <b>Se verificó coherencia interna, integridad horaria y plausibilidad física</b>.</p>

  {pleg('¿Sirve la temperatura de bulbo seco?', 'Sí', 'si',
    '<p>Los 40 archivos EPW (EnergyPlus Weather) traen sus 8 760 horas anuales completas, sin huecos ni vacíos, con temperaturas medias anuales entre 9.5 y 26.1 °C consistentes con la climatología de cada región. La humedad absoluta acompaña a la temperatura siguiendo la ecuación física de Clausius-Clapeyron con una discrepancia de apenas 1.5 puntos porcentuales frente a la teoría, muy por debajo del límite de sospecha de 4 pp.</p><p>Para comparar tipologías constructivas, predimensionar sistemas térmicos o evaluar estrategias pasivas, los archivos son plenamente aptos.</p>')}

  {pleg('¿Sirve la irradiancia solar?', 'No', 'no',
    '<p>Lima reporta 2 177 kWh/m² anuales de radiación global horizontal, <b>más que Cusco</b> con 1 991 kWh/m² — a pesar de que Cusco se sitúa 3 276 m más arriba y Lima posee nubosidad costera persistente. El dato en los archivos EPW (EnergyPlus Weather) procede de reanálisis satelital (ERA5) y la estación del Aeropuerto Internacional Jorge Chávez es de tipo METAR (Meteorological Aerodrome Report): registra visibilidad y nubosidad para aeronavegación, pero no mide radiación solar directa con piranómetros.</p>'
    '<p>Para dimensionamiento fotovoltaico o ganancias solares críticas, es necesario contrastar estos valores con piranometría de superficie antes de su uso.</p>')}

  {pleg('¿Están todos los archivos EPW sanos?', 'Tres no', 'no',
    '<p>La ventana histórica 2004-2018 de Cusco, Arequipa y Juliaca se aparta significativamente de sus otras 4 ventanas temporales: desviaciones de +2.96 °C, +1.20 °C y −1.62 °C frente a la mediana de su ciudad. <b>Ninguna estación costera presenta esta distorsión.</b> Juliaca 2004-2018 además presenta una autocorrelación horaria de solo 0.377 frente a 0.845 en sus otras cuatro ventanas: no es un simple desplazamiento de nivel térmico, sino una alteración en la estructura temporal de la serie.</p>'
    '<p>Este patrón restringido a gran altitud apunta a discontinuidades en la cobertura de registros METAR (Meteorological Aerodrome Report) en los Andes durante ese periodo. Se recomienda no emplear esas tres ventanas específicas.</p>'
    '<div class="panel" style="margin-top:18px"><div id="vint"></div></div>')}

  {pleg('¿Da igual qué archivo TMYx de línea base se elija?', 'No', 'no',
    f'<p>Entre el TMYx (Año Meteorológico Típico Extendido) de periodo completo (1991-2020) y la ventana reciente (2011-2025) hay {c["desfase_entre_bases_C"]:+.2f} °C '
    'de diferencia en Lima, y entre ventanas de una misma ciudad el rango llega a 3.64 °C.</p>'
    '<p>Esta discrepancia <b>no es un sesgo lineal constante que se pueda restar</b>: la pendiente frente al año centroide es de +0.18 °C por década con un coeficiente r² de solo 0.13 (el año centroide explica únicamente el 13 % de la variación). El sesgo temporal (vintage) introduce dispersión e incertidumbre que no puede neutralizarse con un factor multiplicador simple.</p>')}

  {pleg('¿Coinciden los métodos climáticos entre sí?', 'Más o menos', 'mas_menos',
    f'<p>Para Lima 2050, Meteonorm (síntesis estocástica basada en modelos CMIP5 / escenario RCP8.5) reporta {c["T_2050_meteonorm_rcp85_C"]:.2f} °C y FWG (Future Weather Generator v4.2.0 / morphing sobre modelos CMIP6 / escenario SSP5-8.5) '
    f'proyecta {c["T_2050_fwg_ssp585_C"]:.2f} °C: <b>{c["divergencia_absoluta_C"]:+.2f} °C de discrepancia metodológica</b> '
    'sobre una señal total de calentamiento de ~2 °C. Al ser metodologías independientes, la diferencia es relevante.</p>'
    '<p>Debe considerarse que RCP8.5 (CMIP5) y SSP5-8.5 (CMIP6) no representan exactamente el mismo forzamiento. Adicionalmente, el archivo EPW nativo de Meteonorm no estuvo disponible para auditoría directa: sus valores proceden de la documentación del proyecto.</p>'
    '<div class="panel" style="margin-top:18px"><div id="conv"></div></div>')}

  {pleg('¿Capturan el fenómeno de El Niño?', 'No', 'no',
    '<p>Ninguno. Los archivos TMY / TMYx (Typical Meteorological Year / Año Meteorológico Típico) seleccionan meses típicos representativos y <b>eliminan por diseño los años y meses anómalos</b>. En la costa peruana, los eventos de El Niño (ENSO - El Niño-Oscilación del Sur) representan el evento crítico que genera los picos de sobrecarga térmica y de humedad en edificaciones.</p>'
    '<p>Si se dimensiona exclusivamente con el archivo TMYx de Piura o Lima, la instalación no estará dimensionada para resistir un evento de El Niño.</p>')}

  <div class="aviso rojo"><h4>En una frase</h4>
    <p>Son suficientemente robustos para comparar tipologías constructivas y predimensionar; no constituyen valores deterministas para promesas contractuales ni certificación formal. Debe tratarse el valor de «{L45['a2050']['T']:.1f} °C» de Lima en 2050 como «alrededor de 21 °C», con una banda de incertidumbre de aproximadamente ±1 °C.</p></div>
</div></section>

<!-- ══ 06 · conclusiones y alcance ══ -->
<section id="limites"><div class="wrap">
  {cap('06 · Conclusiones y Alcance', 'Qué resuelve esta auditoría y qué precauciones exige')}
  <p class="lead">Declarar con precisión el alcance operativo y las fronteras técnicas del estudio garantiza un uso riguroso y responsable de los archivos climáticos en arquitectura y simulación energética:</p>
  
  <div class="conclusionesGrid">
    <div class="concCard aportes">
      <div class="concHeader">
        <h3>06.1 · Capacidades y Aportes</h3>
        <span class="concBadge si">Sí permite hacer</span>
      </div>
      <div class="concLista">
        <div class="concItem">
          <span class="concNum">01</span>
          <div class="concBody">
            <strong>Simulación energética y pasiva horaria (8 760 h)</strong>
            <p>Permite modelar en EnergyPlus, DesignBuilder o Ladybug el comportamiento térmico pasivo, horas de sobrecalentamiento y confort adaptativo año completo en 8 macroclimas peruanos.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">02</span>
          <div class="concBody">
            <strong>Condiciones de diseño ASHRAE calculadas (99.6 % y 0.4 %)</strong>
            <p>Proporciona los percentiles de temperatura extrema necesarios para dimensionar la potencia de equipos de climatización hacia 2050 y 2080, incluso para ciudades que carecían de cabecera como Juliaca.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">03</span>
          <div class="concBody">
            <strong>Cuantificación de incertidumbre intermodelo (IPCC P10–P90)</strong>
            <p>Integra las bandas de dispersión del ensemble CMIP6 (23 modelos globales), permitiendo aplicar factores de seguridad probabilísticos en decisiones de inversión y diseño.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">04</span>
          <div class="concBody">
            <strong>Auditoría del efecto vintage en líneas base</strong>
            <p>Identifica y cuantifica el desfase de líneas base históricas (Meteonorm 1999 vs TMYx 2018), demostrando que el 50 % de la discrepancia térmica proviene de la antigüedad del dato base y no del modelo.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">05</span>
          <div class="concBody">
            <strong>Diagnóstico del colapso de ventilación natural nocturna</strong>
            <p>Identifica con precisión los meses y horas en que las temperaturas mínimas superan los 20 °C (noches tropicales), advirtiendo el límite de la arquitectura pasiva convencional.</p>
          </div>
        </div>
      </div>
    </div>

    <div class="concCard limites">
      <div class="concHeader">
        <h3>06.2 · Fronteras y Advertencias</h3>
        <span class="concBadge no">Precauciones y Límites</span>
      </div>
      <div class="concLista">
        <div class="concItem">
          <span class="concNum">01</span>
          <div class="concBody">
            <strong>Eventos estocásticos de El Niño (ENSO)</strong>
            <p>La metodología TMYx sintetiza años climáticos típicos y excluye por diseño matemático anomalías no cíclicas. En la costa norte y centro debe aplicarse un margen de seguridad de +2.5 a +3.5 °C.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">02</span>
          <div class="concBody">
            <strong>Sesgos de resolución en la Corriente de Humboldt</strong>
            <p>La malla de 100–250 km de los modelos globales GCM suaviza la surgencia costera fría del Pacífico peruano, requiriendo prudencia en microclimas de borde litoral.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">03</span>
          <div class="concBody">
            <strong>Irradiancia solar directa de alta precisión</strong>
            <p>Al provenir de reanálisis satelital ERA5, debe contrastarse con el Atlas Solar del SENAMHI / MINEM para proyectos de energía fotovoltaica o ganancias solares de gran escala.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">04</span>
          <div class="concBody">
            <strong>Validez regulatoria formal para certificaciones</strong>
            <p>Constituye una investigación y auditoría técnica independiente. No sustituye las tablas normativas del Reglamento Nacional de Edificaciones (RNE) ni datos obligatorios para sellos EDGE o LEED.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">05</span>
          <div class="concBody">
            <strong>Inercia y microclima urbano hiperlocal</strong>
            <p>Las estaciones meteorológicas de aeropuerto no incorporan el calor antropogénico ni el cañón urbano denso; en distritos consolidados debe considerarse el efecto de Isla de Calor Urbano.</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="aviso" style="margin-top:24px">
    <h4>Dictamen final de la auditoría técnica</h4>
    <p>Los archivos climáticos transformados bajo CMIP6 son <b>plenamente válidos y físicamente consistentes para predimensionamiento arquitectónico, simulación higrotérmica y análisis comparativo</b> en el Perú. Para proyectos de alta exigencia, es obligatorio incorporar reservas para El Niño y calibrar la radiación solar con piranómetros locales.</p>
  </div>
</div></section>

<!-- ══ referencias bibliográficas formato APA 7ma Edición ══ -->
<section id="referencias"><div class="wrap">
  {cap('Referencias Bibliográficas', 'Fuentes consultadas y estándares normativos (Formato APA 7.ª Edición)')}
  <p class="lead">Toda la base climática, matemática y metodológica de esta auditoría se sustenta en las siguientes referencias científicas y normativas internacionales:</p>
  
  <div class="apaWrap">
    <ul class="apaLista">
      <li class="apaItem">ADAI &amp; University of Coimbra. (2023). <em>Future Weather Generator (FWG) v4.2.0: Morphing EPW weather files using CMIP6 Global Climate Models</em>. Associação para o Desenvolvimento da Aerodinâmica Industrial, Portugal. <a href="https://futureweathergenerator.com" target="_blank" rel="noopener">https://futureweathergenerator.com</a></li>
      <li class="apaItem">American Society of Heating, Refrigerating and Air-Conditioning Engineers [ASHRAE]. (2021). <em>2021 ASHRAE Handbook—Fundamentals (SI Edition)</em>. Chapter 14: Climatic Design Information. ASHRAE, Atlanta, GA.</li>
      <li class="apaItem">Belcher, S. E., Hacker, J. N., &amp; Powell, D. S. (2005). Constructing design weather data for future climates. <em>Building Services Engineering Research and Technology</em>, 26(1), 49–61. <a href="https://doi.org/10.1191/0143624405bt112oa" target="_blank" rel="noopener">https://doi.org/10.1191/0143624405bt112oa</a></li>
      <li class="apaItem">Crawley, D. B., &amp; Lawrie, L. K. (2023). <em>Climate.OneBuilding.Org: Free global weather data for building simulation</em> (Repository for WMO Region 3 - South America, Peru). <a href="https://climate.onebuilding.org" target="_blank" rel="noopener">https://climate.onebuilding.org</a></li>
      <li class="apaItem">Intergovernmental Panel on Climate Change [IPCC]. (2021). <em>Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change</em> (V. Masson-Delmotte et al., Eds.). Cambridge University Press. <a href="https://doi.org/10.1017/9781009157896" target="_blank" rel="noopener">https://doi.org/10.1017/9781009157896</a></li>
      <li class="apaItem">Meteotest. (2020). <em>Meteonorm Version 8.0: Global Meteorological Database for Engineers, Planners and Education (Handbook Part I: Software; Part II: Theory)</em>. Meteotest AG, Bern, Switzerland. <a href="https://meteonorm.com" target="_blank" rel="noopener">https://meteonorm.com</a></li>
      <li class="apaItem">Servicio Nacional de Meteorología e Hidrología del Perú [SENAMHI] &amp; Ministerio de Energía y Minas [MINEM]. (2003). <em>Atlas de Radiación Solar del Perú</em>. Dirección General de Medio Ambiente, Lima, Perú.</li>
      <li class="apaItem">World Meteorological Organization [WMO]. (2023). <em>WMO Guidelines on the Calculation of Climate Normals</em> (WMO-No. 1203). World Meteorological Organization, Geneva, Switzerland.</li>
    </ul>
  </div>
</div></section>

<footer><div class="wrap">
  Fuentes: climate.onebuilding.org (WMO - Organización Meteorológica Mundial, Región 3 - América del Sur, PER_Peru), descarga del 26/07/2026 ·
  Future Weather Generator v4.2.0, ADAI (Asociación para el Desarrollo de la Aerodinámica Industrial) / Universidad de Coímbra, CC BY-NC-SA · CMIP6 (Coupled Model Intercomparison Project Phase 6, ensemble de 23 modelos climáticos globales) · Contorno cartográfico de Perú: world.geo.json, dominio público.<br><br>
  Trazabilidad completa en <code>Context/SUPUESTOS.md</code>, <code>Context/DECISIONS.md</code>
  y <code>Final Results/AUTOAUDITORIA.md</code>. El informe escrito está en
  <code>Final Results/INFORME_AUDITORIA_CLIMA_PERU.md</code>.<br>
  Generado por <code>Scripts/generar_visor.py</code>. No editar a mano: se regenera.
</div></footer>

<script>
const D={json.dumps(d, ensure_ascii=False, separators=(',', ':'))};
{js}</script></body></html>"""


def construir() -> Path:
    d = json.loads((RAIZ / "Data" / "web" / "payload_v3.json").read_text(encoding="utf-8"))

    WEB.mkdir(parents=True, exist_ok=True)
    salida = WEB / "index.html"
    salida_opt = RAIZ / "Final Results" / "02_OPTIMIZADO_ANTIGRAVITY" / "web" / "index.html"
    salida_opt.parent.mkdir(parents=True, exist_ok=True)
    
    contenido = html(d)
    salida.write_text(contenido, encoding="utf-8")
    salida_opt.write_text(contenido, encoding="utf-8")
    print(f"  {salida}  ({salida.stat().st_size/1024:.0f} KB)")
    print(f"  {salida_opt}  ({salida_opt.stat().st_size/1024:.0f} KB)")
    return salida


if __name__ == "__main__":
    print("Construyendo visor HTML autocontenido...")
    construir()
