#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_visor_github.py — Construye la versión optimizada e institucional para GitHub Pages.

Mejoras clave respecto a la versión base:
1. Capítulo 04 («Cómo: Seis pasos del proceso de auditoría meteorológica»):
   - Rediseño interactivo tipo Stepper/Pipeline de 6 etapas.
   - Tarjeta activa de alto impacto con KPIs visuales, narrativa clara y controles de navegación.
2. Pie de página (Footer) Institucional Simple y Limpio:
   - Diseño estándar de sitio web moderno, ligero y centrado (sin recuadros negros ni SVGs desbordados).
   - Atribución explícita a Abelardo Tomás Palacios Hurtado y a IBPSA Perú.
   - Año de publicación 2026, licencia CC BY 4.0 y enlaces oficiales.
3. Soporte Bilingüe Integral (Español / Inglés):
   - Selector [ ES | EN ] en la cabecera.
   - Traducción al 100 % de textos, componentes interactivos y gráficos internos:
     Marco IPCC (título, subtítulo, pines, descripciones y tarjetas SSP), climogramas
     (ejes, meses, leyendas y rangos), trayectoria, barras, nube psicrométrica y carátula solar.
4. Preservación del Original:
   - 'Final Results/web/index_original_v1.html' se mantiene 100 % inalterado e intacto.
   - La salida optimizada se compila en 'Final Results/web/index.html' para despliegue en GitHub Pages.

Uso:
    py -3 Scripts/generar_visor_github.py
"""

from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TPL = RAIZ / "Scripts" / "visor"
WEB = RAIZ / "Final Results" / "web"

CAPS = [
    ("ipcc", "Marco IPCC"),
    ("impacto", "¿Qué significa +1°C?"),
    ("dato", "El dato"),
    ("ciudades", "Por ciudad"),
    ("carga", "Qué implica"),
    ("metodo", "Cómo"),
    ("fiable", "¿Es fiable?"),
    ("limites", "Conclusiones"),
    ("referencias", "Referencias"),
]

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
    "github": '<svg class="ico" viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>',
    "descarga": '<svg class="ico" viewBox="0 0 24 24" width="16" height="16"><path d="M12 3v13m0 0l-4-4m4 4l4-4M4 19h16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>',
    "externo": '<svg class="ico" viewBox="0 0 24 24" width="14" height="14"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>',
}

CSS_EXTRA = """
/* ── Ajustes finos de cabecera superior y navegación ── */
header.top .wrap{gap:12px;max-width:1300px}
.marca{margin-right:12px;flex-shrink:0}
.migas{display:flex;gap:2px;align-items:center;margin-left:auto}
.migas a{font-size:10.5px;letter-spacing:.6px;text-transform:uppercase;color:var(--tinta3);text-decoration:none;padding:5px 7px;border-radius:8px;transition:.22s var(--ease-out);font-weight:600;white-space:nowrap}
.migas a:hover{color:var(--tinta);background:rgba(18,22,31,0.04)}
.migas a.on{color:var(--papel);background:var(--acento);box-shadow:0 2px 8px rgba(26,79,110,0.25)}

/* ── Selector de Idioma (ES / EN) ── */
.langSwitch{display:inline-flex;align-items:center;background:rgba(18,22,31,0.06);border:1px solid var(--linea2);border-radius:20px;padding:2px 5px;gap:3px;margin-left:10px;flex-shrink:0}
.langBtn{background:none;border:none;color:var(--tinta3);font:700 11.5px var(--f);padding:4px 8px;border-radius:14px;cursor:pointer;transition:.2s var(--ease-out)}
.langBtn:hover{color:var(--tinta)}
.langBtn.on{background:var(--tinta);color:#ffffff;box-shadow:0 2px 6px rgba(18,22,31,0.18)}
.langSep{font-size:11px;color:var(--linea3);font-weight:400}

/* ── Sección 04: Rediseño Stepper Interactivo ── */
.stepperContainer{margin-top:24px;display:flex;flex-direction:column;gap:18px}
.stepperNav{display:grid;grid-template-columns:repeat(6, 1fr);gap:10px;background:rgba(18,22,31,0.03);padding:8px;border-radius:14px;border:1px solid var(--linea)}
.stepTab{display:flex;flex-direction:column;align-items:flex-start;background:#ffffff;border:1px solid var(--linea);border-radius:10px;padding:12px 14px;cursor:pointer;transition:.25s var(--ease-out);text-align:left;position:relative;overflow:hidden}
.stepTab:hover{border-color:var(--tinta2);transform:translateY(-2px);box-shadow:var(--sombra-suave)}
.stepTab.on{background:#fdfdfc;border-color:var(--tinta);box-shadow:0 0 0 1.5px var(--tinta), var(--sombra-flotante)}
.stepTabTop{display:flex;align-items:center;gap:8px;margin-bottom:6px;width:100%}
.stepBadge{width:22px;height:22px;border-radius:6px;font-size:11px;font-weight:800;display:flex;align-items:center;justify-content:center;color:#fff}
.stepTabTitle{font-size:13px;font-weight:700;color:var(--tinta);letter-spacing:-.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.stepTabSubtitle{font-size:11px;color:var(--tinta3);line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}

.stepHeroCard{background:#ffffff;border:1px solid var(--linea);border-radius:var(--r);padding:32px 36px;box-shadow:var(--sombra-flotante);transition:.3s var(--ease-out);position:relative}
.stepHeroHead{display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;padding-bottom:20px;border-bottom:1px solid var(--linea);margin-bottom:22px}
.stepHeroTitles{flex:1;min-width:280px}
.stepHeroTag{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-weight:700;letter-spacing:1px;text-transform:uppercase;background:rgba(26,79,110,0.08);padding:4px 10px;border-radius:6px;margin-bottom:8px}
.stepHeroTitles h3{font-size:24px;font-weight:700;color:var(--tinta);letter-spacing:-.5px;margin:0 0 6px}
.stepHeroTitles p{font-size:15px;color:var(--tinta2);line-height:1.55;margin:0;max-width:68ch}
.stepStatusBadge{display:inline-flex;align-items:center;gap:6px;background:var(--papel);border:1px solid var(--linea2);padding:8px 16px;border-radius:12px;font-size:12px;font-weight:700;color:var(--tinta);white-space:nowrap}

.stepKpiGrid{display:grid;grid-template-columns:repeat(auto-fit, minmax(180px, 1fr));gap:14px;margin-bottom:24px}
.stepKpiCard{background:var(--papel);border:1px solid var(--linea);border-radius:12px;padding:16px 18px;display:flex;flex-direction:column;gap:4px;transition:.22s var(--ease-out)}
.stepKpiCard:hover{border-color:var(--linea2);background:#fff}
.stepKpiVal{font-size:21px;font-weight:800;color:var(--tinta);font-variant-numeric:tabular-nums;line-height:1.2}
.stepKpiLbl{font-size:11.5px;color:var(--tinta3);font-weight:600;letter-spacing:.2px;line-height:1.4}

.stepAuditCallout{border-left:4px solid var(--calor-tx);border-radius:0 10px 10px 0;padding:16px 20px;font-size:13.5px;color:var(--tinta2);line-height:1.55;margin-bottom:24px}
.stepAuditCallout b{color:var(--tinta);font-weight:700}

.stepNavControls{display:flex;justify-content:space-between;align-items:center;padding-top:16px;border-top:1px solid var(--linea);flex-wrap:wrap;gap:12px}
.stepCtrlBtn{border:1px solid var(--linea2);background:#ffffff;color:var(--tinta);padding:8px 18px;border-radius:10px;cursor:pointer;font:600 12.5px var(--f);display:inline-flex;align-items:center;gap:8px;transition:.2s var(--ease-out)}
.stepCtrlBtn:hover:not(:disabled){border-color:var(--tinta);background:var(--papel);transform:translateY(-1px)}
.stepCtrlBtn:disabled{opacity:.4;cursor:not-allowed}
.stepProgressIndicator{font-size:12px;font-weight:700;color:var(--tinta3);letter-spacing:1px;text-transform:uppercase}

/* ── Pie de Página (Footer) Simple, Elegante y Estándar ── */
footer.siteFooter{background:var(--papel2,#f5f2eb);border-top:1px solid var(--linea,#e2ddd2);padding:36px 20px 42px;margin-top:72px;text-align:center;color:var(--tinta2,#4a5464);font-size:13px;line-height:1.65}
.siteFooter .wrap{max-width:960px;margin:0 auto;display:flex;flex-direction:column;align-items:center;gap:8px}
.siteFooter p{margin:0}
.siteFooter strong{color:var(--tinta,#12161f);font-weight:700}
.siteFooter a{color:var(--acento,#1a4f6e);text-decoration:underline;text-underline-offset:3px;transition:opacity .2s;font-weight:600}
.siteFooter a:hover{opacity:.8}
.siteFooter .footerSub{font-size:12px;color:var(--tinta3,#788394);margin-top:4px}

@media(max-width:1200px){
  .migas a{font-size:9.5px;padding:4px 5px;letter-spacing:.3px}
}
@media(max-width:980px){
  .stepperNav{grid-template-columns:repeat(3, 1fr)}
  .migas{display:none}
  .langSwitch{margin-left:auto}
}
@media(max-width:600px){
  .stepperNav{grid-template-columns:repeat(2, 1fr)}
  .stepHeroCard{padding:22px 20px}
  .stepHeroHead{flex-direction:column}
}
"""

JS_EXTRA = """
/* ════════════════════════════════════════════════════════════════════════════════
   EXTENSIONES GITHUB PAGES:
   1. Datos y renderizador del Stepper Interactivo (Sección 04)
   2. Motor de Traducción Bilingüe Integral (ES / EN)
   3. Traducción completa de gráficos y mapas internos (IPCC, climograma, etc.)
   ════════════════════════════════════════════════════════════════════════════════ */

const PASOS_DATA = [
  {
    num: 1, col: "#1a4f6e",
    tit_es: "1. Descarga e Integridad",
    tit_en: "1. Download & Data Integrity",
    sub_es: "40 archivos meteorológicos TMYx desde climate.onebuilding.org (WMO).",
    sub_en: "40 TMYx weather files from climate.onebuilding.org (WMO).",
    desc_es: "Se descargaron 40 archivos meteorológicos oficiales en formato EPW desde el repositorio climate.onebuilding.org (Organización Meteorológica Mundial, Región 3 - Sudamérica). Se examinaron 5 ventanas temporales por cada una de las 8 ciudades para contrastar tendencias.",
    desc_en: "40 official EPW weather files were retrieved from climate.onebuilding.org (World Meteorological Organization, Region 3 - South America). Five temporal windows were analyzed for each of the 8 Peruvian cities to cross-examine historical trends.",
    status_es: "✓ 100 % Integridad Horaria",
    status_en: "✓ 100% Hourly Integrity",
    kpis: [
      { val: "40", lbl_es: "Archivos EPW auditados", lbl_en: "Audited EPW files" },
      { val: "8", lbl_es: "Macroclimas peruanos", lbl_en: "Peruvian macroclimates" },
      { val: "8 760 h", lbl_es: "Horas completas por archivo", lbl_en: "Hourly records per file" },
      { val: "0", lbl_es: "Huecos en bulbo seco", lbl_en: "Missing dry-bulb records" },
      { val: "0", lbl_es: "Archivos corruptos o fallidos", lbl_en: "Corrupted/failed files" }
    ],
    audit_es: "<b>Razón metodológica:</b> Cinco ventanas temporales por ciudad y no solo dos evitan forzar una recta artificial en el análisis de desfase histórico (efecto vintage).",
    audit_en: "<b>Methodological insight:</b> Five temporal windows per city rather than just two prevents forcing an artificial linear slope in the historical vintage bias evaluation."
  },
  {
    num: 2, col: "#2b6f9e",
    tit_es: "2. Lectura de Cabeceras",
    tit_en: "2. Header & Centroid Parsing",
    sub_es: "Extracción del año fuente mensual y centroide real del archivo.",
    sub_en: "Monthly source year extraction and true centroid calculation.",
    desc_es: "Los archivos TMYx sintetizan 12 meses típicos provenientes de distintos años reales. Se extrajo la cabecera completa de cada mes y se calculó el año centroide ponderado para cuantificar la antigüedad real de la línea base.",
    desc_en: "TMYx datasets synthesize 12 representative typical months selected from different historical years. Each monthly header was parsed to compute the true weighted centroid year to establish actual baseline vintage.",
    status_es: "✓ Centroide Verificado",
    status_en: "✓ Verified Centroid",
    kpis: [
      { val: "1999.8", lbl_es: "Centroide Lima Completo (1991-2020)", lbl_en: "Lima Full Period Centroid (1991-2020)" },
      { val: "2018.0", lbl_es: "Centroide Lima Reciente (2011-2025)", lbl_en: "Lima Recent Centroid (2011-2025)" },
      { val: "18.2 años", lbl_es: "Desfase temporal entre bases", lbl_en: "Temporal vintage gap" },
      { val: "+0.35 °C", lbl_es: "Calentamiento ya ocurrido", lbl_en: "Historical warming already realized" }
    ],
    audit_es: "<b>Hallazgo crítico:</b> El incremento de +0.35 °C es calentamiento que YA ocurrió en Lima. Proyectar a futuro desde el archivo de periodo completo contaría ese desfase dos veces.",
    audit_en: "<b>Critical finding:</b> The +0.35 °C warming has ALREADY occurred in Lima. Morphing future projections from the full-period file double-counts historical warming."
  },
  {
    num: 3, col: "#3d8ab0",
    tit_es: "3. Medición Termodinámica",
    tit_en: "3. Thermodynamic Metrics",
    sub_es: "Cálculo de ~120 métricas de carga térmica, percentiles y persistencia.",
    sub_en: "Calculation of ~120 thermal load, percentile, and persistence metrics.",
    desc_es: "Se ejecutó un motor estadístico sobre las 8 760 horas de cada archivo calculando grados-hora de enfriamiento (CDD con 4 bases térmicas), percentiles de diseño ASHRAE (99.6 % y 0.4 %), y autocorrelación horaria temporal (lags 1, 2 y 3).",
    desc_en: "An analytical computing engine processed all 8,760 hours for every file, deriving Cooling Degree Hours (CDD across 4 base temperatures), ASHRAE design percentiles (99.6% and 0.4%), and temporal autocorrelation lags (1, 2, and 3).",
    status_es: "✓ 8/8 Tests Unitarios OK",
    status_en: "✓ 8/8 Unit Tests Passed",
    kpis: [
      { val: "~120", lbl_es: "Métricas bioclimáticas por archivo", lbl_en: "Bioclimatic metrics per file" },
      { val: "CDD 18-28°C", lbl_es: "Bases de grados-hora analizadas", lbl_en: "Cooling Degree Hour bases" },
      { val: "0.38 vs 0.85", lbl_es: "Anomalía detectada en Juliaca 2004", lbl_en: "Autocorrelation anomaly in Juliaca" },
      { val: "8 / 8", lbl_es: "Pruebas unitarias de software superadas", lbl_en: "Software unit tests passed" }
    ],
    audit_es: "<b>Control de calidad:</b> El motor de cálculo se validó previamente contra un archivo EPW sintético analítico antes de procesar los datos meteorológicos de estaciones reales.",
    audit_en: "<b>Quality assurance:</b> The computing algorithms were validated against a synthetic analytical EPW benchmark prior to processing real meteorological records."
  },
  {
    num: 4, col: "#7a9a86",
    tit_es: "4. Morfado Horario (Morphing)",
    tit_en: "4. Hourly Morphing (CMIP6)",
    sub_es: "Transformación horaria con 23 modelos climáticos globales (GCM).",
    sub_en: "Hourly transformation using 23 Global Climate Models (GCMs).",
    desc_es: "Mediante Future Weather Generator (FWG v4.2.0 / ADAI / Univ. Coímbra) se aplicaron anomalías climáticas mensuales multimodelo CMIP6 a las series horarias. Se evaluaron los escenarios SSP1-2.6, SSP2-4.5, SSP3-7.0 y SSP5-8.5 para 2050 y 2080.",
    desc_en: "Using Future Weather Generator (FWG v4.2.0 / ADAI / Univ. Coimbra), multi-model CMIP6 monthly climate anomalies were morphed into hourly series across SSP1-2.6, SSP2-4.5, SSP3-7.0, and SSP5-8.5 for horizons 2050 and 2080.",
    status_es: "✓ 23 Modelos IPCC AR6",
    status_en: "✓ 23 IPCC AR6 Models",
    kpis: [
      { val: "23 GCMs", lbl_es: "Modelos globales en ensemble", lbl_en: "Global climate models in ensemble" },
      { val: "4 SSPs", lbl_es: "Escenarios socioeconómicos", lbl_en: "Socioeconomic pathways" },
      { val: "2050 / 2080", lbl_es: "Horizontes modelados", lbl_en: "Modeled future horizons" },
      { val: "IDW 4-pts", lbl_es: "Interpolación espacial de malla", lbl_en: "Spatial grid interpolation" }
    ],
    audit_es: "<b>Virtud del morphing:</b> Preserva la física del microclima local, la amplitud térmica día-noche y la rosa de vientos real de cada estación, adaptando la energía térmica al clima futuro.",
    audit_en: "<b>Strength of morphing:</b> Preserves local physical microclimates, diurnal swings, and real wind roses, while projecting thermal energy into future horizons."
  },
  {
    num: 5, col: "#c78b3c",
    tit_es: "5. Comparación Cruzada",
    tit_en: "5. Cross-Method Comparison",
    sub_es: "Validación independiente contra Meteonorm (CMIP5 / RCP8.5).",
    sub_en: "Independent cross-validation against Meteonorm (CMIP5 / RCP8.5).",
    desc_es: "Se contrastaron las proyecciones de FWG/CMIP6 frente a la herramienta de síntesis estocástica comercial Meteonorm. Para Lima 2050, FWG proyecta 21.62 °C frente a 20.93 °C de Meteonorm (+0.70 °C de discrepancia metodológica).",
    desc_en: "FWG/CMIP6 projections were benchmarked against stochastic synthesis tool Meteonorm. For Lima 2050, FWG projects 21.62 °C versus 20.93 °C from Meteonorm (+0.70 °C methodological discrepancy).",
    status_es: "✓ Discrepancia Cuantificada",
    status_en: "✓ Quantified Discrepancy",
    kpis: [
      { val: "21.62 °C", lbl_es: "Lima 2050 · FWG / CMIP6 (SSP5-8.5)", lbl_en: "Lima 2050 · FWG / CMIP6 (SSP5-8.5)" },
      { val: "20.93 °C", lbl_es: "Lima 2050 · Meteonorm (RCP8.5)", lbl_en: "Lima 2050 · Meteonorm (RCP8.5)" },
      { val: "+0.70 °C", lbl_es: "Divergencia entre metodologías", lbl_en: "Inter-method divergence" },
      { val: "50 %", lbl_es: "Explicado por desfase de línea base", lbl_en: "Explained by baseline vintage gap" }
    ],
    audit_es: "<b>Descubrimiento:</b> El 50 % de la divergencia entre estudios climáticos proviene de la antigüedad de la línea base histórica seleccionada (1999 vs 2018) y no de las ecuaciones del modelo.",
    audit_en: "<b>Key insight:</b> 50% of the discrepancy between independent climate studies is caused by baseline vintage (1999 vs 2018) rather than the forecasting equations."
  },
  {
    num: 6, col: "#bd491a",
    tit_es: "6. Verificación Termodinámica",
    tit_en: "6. Thermodynamic Verification",
    sub_es: "Compuerta física de consistencia según Clausius-Clapeyron.",
    sub_en: "Physical consistency check via Clausius-Clapeyron relation.",
    desc_es: "Por leyes de la termodinámica, al calentarse el aire a humedad relativa constante, la capacidad de retención de vapor de agua debe ascender a una tasa de ~6.2 %/K. Los archivos auditados arrojaron tasas de 7.60 a 7.79 %/K.",
    desc_en: "By thermodynamic laws, as air warms at constant relative humidity, moisture-holding capacity increases at ~6.2 %/K. Audited files produced rates between 7.60 and 7.79 %/K.",
    status_es: "✓ Físicamente Plausible",
    status_en: "✓ Physically Plausible",
    kpis: [
      { val: "~6.2 %/K", lbl_es: "Tasa teórica Clausius-Clapeyron", lbl_en: "Theoretical Clausius-Clapeyron rate" },
      { val: "7.73 %/K", lbl_es: "Tasa observada SSP2-4.5", lbl_en: "Observed rate (SSP2-4.5)" },
      { val: "1.59 pp", lbl_es: "Desviación observada frente a teoría", lbl_en: "Deviation from theoretical rate" },
      { val: "< 4.0 pp", lbl_es: "Umbral de sospecha superado con éxito", lbl_en: "Well below suspicion threshold" }
    ],
    audit_es: "<b>Veredicto final:</b> La respuesta psicrométrica se mantiene plenamente dentro del dominio admisible: el algoritmo de morphing no desacopló la humedad ni alteró la física del aire.",
    audit_en: "<b>Final verdict:</b> Psychrometric behavior stays strictly within physically admissible bounds: morphing preserved coupled moisture and air thermodynamics."
  }
];

let pasoActual = 0;

function renderStepper(){
  const nav = $('stepPills');
  const card = $('stepHeroCard');
  if(!nav || !card) return;

  const isEn = (currentLang === 'en');

  nav.innerHTML = PASOS_DATA.map((p, idx) => `
    <button class="stepTab ${idx === pasoActual ? 'on' : ''}" onclick="irPaso(${idx})" aria-label="${isEn ? p.tit_en : p.tit_es}">
      <div class="stepTabTop">
        <span class="stepBadge" style="background:${p.col}">${p.num}</span>
        <span class="stepTabTitle">${isEn ? p.tit_en : p.tit_es}</span>
      </div>
      <span class="stepTabSubtitle">${isEn ? p.sub_en : p.sub_es}</span>
    </button>
  `).join('');

  const cur = PASOS_DATA[pasoActual];
  card.innerHTML = `
    <div class="stepHeroHead">
      <div class="stepHeroTitles">
        <div class="stepHeroTag" style="color:${cur.col};background:${cur.col}18">
          ${isEn ? 'Audited Stage 0' + cur.num : 'Etapa Auditada 0' + cur.num}
        </div>
        <h3 style="color:${cur.col}">${isEn ? cur.tit_en : cur.tit_es}</h3>
        <p>${isEn ? cur.desc_en : cur.desc_es}</p>
      </div>
      <div>
        <span class="stepStatusBadge">${isEn ? cur.status_en : cur.status_es}</span>
      </div>
    </div>

    <div class="stepKpiGrid">
      ${cur.kpis.map(k => `
        <div class="stepKpiCard">
          <span class="stepKpiVal" style="color:${cur.col}">${k.val}</span>
          <span class="stepKpiLbl">${isEn ? k.lbl_en : k.lbl_es}</span>
        </div>
      `).join('')}
    </div>

    <div class="stepAuditCallout" style="border-left-color:${cur.col};background:${cur.col}0c">
      ${isEn ? cur.audit_en : cur.audit_es}
    </div>

    <div class="stepNavControls">
      <button class="stepCtrlBtn" onclick="irPaso(${pasoActual - 1})" ${pasoActual === 0 ? 'disabled' : ''}>
        ${isEn ? '← Previous Stage' : '← Paso Anterior'}
      </button>
      <span class="stepProgressIndicator">
        ${isEn ? 'Stage ' + (pasoActual + 1) + ' of ' + PASOS_DATA.length : 'Paso ' + (pasoActual + 1) + ' de ' + PASOS_DATA.length}
      </span>
      <button class="stepCtrlBtn" onclick="irPaso(${pasoActual + 1})" ${pasoActual === PASOS_DATA.length - 1 ? 'disabled' : ''}>
        ${isEn ? 'Next Stage →' : 'Siguiente Paso →'}
      </button>
    </div>
  `;
}

function irPaso(idx){
  if(idx < 0 || idx >= PASOS_DATA.length) return;
  pasoActual = idx;
  renderStepper();
}

/* ════════════════════════════════════════════════════════════════════════════════
   DICCIONARIO BILINGÜE OFICIAL ASHRAE / IBPSA
   ════════════════════════════════════════════════════════════════════════════════ */

let currentLang = 'es';

const DICT = {
  es: {
    pageTitle: "Cambio Climático y Confort Térmico en Perú hacia 2080 · Auditoría EPW | IBPSA Perú",
    nav_ipcc: "Marco IPCC",
    nav_impacto: "¿Qué significa +1°C?",
    nav_dato: "El dato",
    nav_ciudades: "Por ciudad",
    nav_carga: "Qué implica",
    nav_metodo: "Cómo",
    nav_fiable: "¿Es fiable?",
    nav_limites: "Conclusiones",
    nav_referencias: "Referencias",

    lbl_ciudad: "Ciudad:",
    btn_hoy: "Hoy",
    btn_animar: "▶ Animar",
    btn_los_numeros: "Los números",
    heroKicker: "Herramienta Interactiva de Difusión Climática y Auditoría Técnica EPW · IBPSA Perú",
    solPie: "Cada rayo es un mes en una <b>escala fija calibrada de -6 a 36 °C</b> (anillos en 0°, 10°, 20° y 30°). Toca una ciudad para comparar su longitud y posición en el dial.",

    ipcc_num: "Marco Global IPCC & CMIP6",
    ipcc_tit: "Escenarios mundiales de temperatura y modelos climáticos",
    ipccLead: "Las proyecciones se fundamentan en el <b>IPCC (Sexto Informe AR6)</b> y el ensamble multimodelo <b>CMIP6 (23 modelos globales)</b>. Explora cómo se distribuye el calentamiento en el mapa mundial según el escenario socioeconómico (SSP) y el horizonte temporal:",
    ssp126_btn: "SSP1-2.6 · Sostenibilidad (París)",
    ssp245_btn: "SSP2-4.5 · Trayectoria Central",
    ssp370_btn: "SSP3-7.0 · Rivalidad Regional",
    ssp585_btn: "SSP5-8.5 · Caso de Estrés (Fósil)",
    hz2050_btn: "Año 2050",
    hz2080_btn: "Año 2080",
    lbl_media_global: "Media Global:",
    lbl_anomalia_proy: "Anomalía térmica proyectada (°C):",

    impacto_num: "Escala de Impacto Térmico",
    impacto_tit: "¿Qué significan realmente +1 °C, +2 °C o +3 °C en el cuerpo, el edificio y el entorno?",
    impactoLead: "Un aumento en la <b>media anual</b> desplaza la curva climática entera, multiplicando de forma no lineal las olas de calor, el estrés fisiológico, el consumo energético en edificios y el deshielo andino. Selecciona un nivel de calentamiento para ver sus consecuencias directas:",
    imp_s10_btn: "Actual (Perú Hoy)",
    imp_s15_btn: "Meta París (SSP1-2.6)",
    imp_s20_btn: "Umbral Crítico (SSP2-4.5 · 2050)",
    imp_s30_btn: "Estrés Severo (SSP5-8.5 · 2080)",

    dato_num: "01 · El dato",
    dato_tit: "Elige un horizonte y mira el país entero",
    datoLead: "Temperatura media anual de cada ciudad. Cambia de horizonte y las cifras y el mapa <b>transicionan</b> al nuevo valor. Toca una ciudad para ver su ficha completa: percentil 99, máxima del año, humedad y carga de enfriamiento.",
    h_hoy: "Hoy",
    h_hoy_sub: "Línea base TMYx 2011-2025",
    h_2030_sub: "Interpolado",
    h_2050_sub: "Modelado CMIP6",
    h_2080_sub: "Modelado CMIP6",
    esc_s245_btn: "SSP2-4.5 · Escenario Central (Shared Socioeconomic Pathway)",
    esc_s585_btn: "SSP5-8.5 · Escenario de Estrés (Shared Socioeconomic Pathway)",
    escNota: "Los escenarios SSP 8.5 representan casos de estrés severo para dimensionar el peor caso ante cambio climático, no pronósticos deterministas.",
    aviso_2030_t: "2030 es interpolación, no modelo",
    aviso_2030_b: "El generador FWG (Future Weather Generator / ADAI / Univ. Coímbra) solo emite los horizontes 2050 y 2080 basados en modelos globales CMIP6 (Coupled Model Intercomparison Project Phase 6). La columna de 2030 interpola linealmente entre la línea base TMYx (Año Meteorológico Típico Extendido) y 2050. Como la aceleración del calentamiento no es estrictamente lineal en el tiempo, ese valor probablemente <b>se queda corto</b> respecto a la trayectoria real. Está marcado como tal en toda la página.",

    ciudades_num: "02 · Por ciudad",
    ciudades_tit: "Cómo se siente: máximas y mínimas, mes a mes",
    ciudadesLead: "Una media anual no se percibe. Lo que se nota es la máxima de febrero y la mínima de agosto. <b>Enciende y apaga horizontes</b> en la leyenda; con doble clic aíslas uno solo y aparecen las cifras de cada mes.",
    climoTit: "Mes a mes",
    ciudadesLead2: "Ocho estaciones meteorológicas de superficie (METAR / WMO), de los 32 m de Trujillo a los 3 826 m de Juliaca. <b>El calentamiento escala con la altura</b>: la sierra sube más que la costa, aunque su consecuencia energética sea menor.",
    trayTit: "Trayectoria",
    barrasSubtit: "Las ocho ciudades · clic en cualquier barra para fijar esa ciudad y ese horizonte",
    lbl_ordenar: "ordenar por",

    carga_num: "03 · Qué implica",
    carga_tit: "Comportamiento psicrométrico hora a hora",
    nbLead: "Cada punto es una hora del año para la ciudad seleccionada, situada por su temperatura y su humedad absoluta. Al proyectar a horizontes futuros, la nube se desplaza <b>en diagonal</b>: el aire más cálido retiene mayor cantidad de vapor. Eso es Clausius-Clapeyron, visualizado hora a hora.",
    btn_recorrer: " Recorrer hasta 2080",
    btn_color_mes: "Color: mes",
    btn_color_hora: "Color: hora del día",
    nbPunto: "<b>Cada punto es una hora del año</b> — una de cada seis, 1 460 en total. Su posición horizontal es la temperatura del aire y la vertical, cuánto vapor lleva. El color indica el mes (o la hora del día, si cambias el modo): clic en la leyenda para aislar uno. Los meses de verano se agrupan arriba a la derecha —calor con humedad— y los de invierno abajo a la izquierda.",
    aviso_multiplo_t: "El múltiplo térmico engaña sin su valor absoluto",
    aviso_multiplo_b: "En Trujillo la carga de enfriamiento se multiplica por 4.8 y en Piura solo por 1.4. Pero Trujillo sube 706 °C·h y Piura 6 479 °C·h. El múltiplo grande está sobre la base pequeña.",

    metodo_num: "04 · Cómo",
    metodo_tit: "Seis pasos del proceso de auditoría meteorológica",
    metodoLead: "De un archivo meteorológico descargado a una proyección al 2080. Estos son los seis pasos de la metodología, con sus métricas auditadas, variables comprobadas y hallazgos reales:",
    glos_morphing_t: "¿Qué es «Morphing»?",
    glos_morphing_p1: "<b>Ajuste horario:</b> Toma las 8 760 horas medidas en la estación base y les aplica las anomalías climáticas mensuales proyectadas por los modelos globales.",
    glos_morphing_p2: "<b>Por qué importa:</b> Conserva la física del sitio, la oscilación día-noche y los vientos reales, adaptándolos a las temperaturas de 2050 y 2080.",
    glos_ensemble_t: "¿Qué es un «Ensemble»?",
    glos_ensemble_p1: "<b>Consenso multimodelo:</b> Combina y promedia las proyecciones de 23 modelos climáticos globales independientes (NOAA, NASA, Max Planck).",
    glos_ensemble_p2: "<b>Por qué importa:</b> Ningún modelo individual es infalible; promediar el conjunto cancela sesgos y entrega una señal climática de consenso mucho más sólida.",
    aviso_cc_t: "Verificación física de Clausius-Clapeyron (Paso 6)",
    aviso_cc_b: "Al calentarse el aire a humedad relativa constante, la humedad absoluta debe subir ~6.2 % por cada °C (+6.2 %/K). Los archivos transformados con FWG arrojan entre <b>7.60 y 7.79 %/K</b> (apenas 1.5 pp de desviación frente a la teoría, muy por debajo del umbral de sospecha de 4.0 pp). Esto confirma que el morphing preservó la consistencia termodinámica.",

    fiable_num: "05 · ¿Es fiable?",
    fiable_tit: "Ahora sí: cuánto puedes creerte esas cifras",
    fiableLead: "Los números de arriba salen de archivos climáticos que no habían sido auditados en conjunto. Esto es lo que se encontró al examinarlos en detalle, pregunta por pregunta. <b>Se verificó coherencia interna, integridad horaria y plausibilidad física</b>.",
    aviso_frase_t: "En una frase",
    aviso_frase_b: "Son suficientemente robustos para comparar tipologías constructivas y predimensionar; no constituyen valores deterministas para promesas contractuales ni certificación formal. Debe tratarse el valor de «21.1 °C» de Lima en 2050 como «alrededor de 21 °C», con una banda de incertidumbre de aproximadamente ±1 °C.",

    limites_num: "06 · Conclusiones y Alcance",
    limites_tit: "Qué resuelve esta auditoría y qué precauciones exige",
    limitesLead: "Declarar con precisión el alcance operativo y las fronteras técnicas del estudio garantiza un uso riguroso y responsable de los archivos climáticos en arquitectura y simulación energética:",
    conc_aportes_t: "06.1 · Capacidades y Aportes",
    conc_aportes_badge: "Sí permite hacer",
    conc_limites_t: "06.2 · Fronteras y Advertencias",
    conc_limites_badge: "Precauciones y Límites",
    dictamen_t: "Dictamen final de la auditoría técnica",
    dictamen_d: "Los archivos climáticos transformados bajo CMIP6 son <b>plenamente válidos y físicamente consistentes para predimensionamiento arquitectónico, simulación higrotérmica y análisis comparativo</b> en el Perú. Para proyectos de alta exigencia, es obligatorio incorporar reservas para El Niño y calibrar la radiación solar con piranómetros locales.",

    ap1_t: "Simulación energética y pasiva horaria (8 760 h)",
    ap1_d: "Permite modelar en EnergyPlus, DesignBuilder o Ladybug el comportamiento térmico pasivo, horas de sobrecalentamiento y confort adaptativo año completo en 8 macroclimas peruanos.",
    ap2_t: "Condiciones de diseño ASHRAE calculadas (99.6 % y 0.4 %)",
    ap2_d: "Proporciona los percentiles de temperatura extrema necesarios para dimensionar la potencia de equipos de climatización hacia 2050 y 2080, incluso para ciudades que carecían de cabecera como Juliaca.",
    ap3_t: "Cuantificación de incertidumbre intermodelo (IPCC P10–P90)",
    ap3_d: "Integra las bandas de dispersión del ensemble CMIP6 (23 modelos globales), permitiendo aplicar factores de seguridad probabilísticos en decisiones de inversión y diseño.",
    ap4_t: "Auditoría del efecto vintage en líneas base",
    ap4_d: "Identifica y cuantifica el desfase de líneas base históricas (Meteonorm 1999 vs TMYx 2018), demostrando que el 50 % de la discrepancia térmica proviene de la antigüedad del dato base y no del modelo.",
    ap5_t: "Diagnóstico del colapso de ventilación natural nocturna",
    ap5_d: "Identifica con precisión los meses y horas en que las temperaturas mínimas superan los 20 °C (noches tropicales), advirtiendo el límite de la arquitectura pasiva convencional.",

    lim1_t: "Eventos estocásticos de El Niño (ENSO)",
    lim1_d: "La metodología TMYx sintetiza años climáticos típicos y excluye por diseño matemático anomalías no cíclicas. En la costa norte y centro debe aplicarse un margen de seguridad de +2.5 a +3.5 °C.",
    lim2_t: "Sesgos de resolución en la Corriente de Humboldt",
    lim2_d: "La malla de 100–250 km de los modelos globales GCM suaviza la surgencia costera fría del Pacífico peruano, requiriendo prudencia en microclimas de borde litoral.",
    lim3_t: "Irradiancia solar directa de alta precisión",
    lim3_d: "Al provenir de reanálisis satelital ERA5, debe contrastarse con el Atlas Solar del SENAMHI / MINEM para proyectos de energía fotovoltaica o ganancias solares de gran escala.",
    lim4_t: "Validez regulatoria formal para certificaciones",
    lim4_d: "Constituye una investigación y auditoría técnica independiente. No sustituye las tablas normativas del Reglamento Nacional de Edificaciones (RNE) ni datos obligatorios para sellos EDGE o LEED.",
    lim5_t: "Inercia y microclima urbano hiperlocal",
    lim5_d: "Las estaciones meteorológicas de aeropuerto no incorporan el calor antropogénico ni el cañón urbano denso; en distritos consolidados debe considerarse el efecto de Isla de Calor Urbano.",

    referencias_num: "Referencias Bibliográficas",
    referencias_tit: "Fuentes consultadas y estándares normativos (Formato APA 7.ª Edición)",
    refLead: "Toda la base climática, matemática y metodológica de esta auditoría se sustenta en las siguientes referencias científicas y normativas internacionales:"
  },

  en: {
    pageTitle: "Climate Change & Thermal Comfort in Peru towards 2080 · EPW Weather Files Audit | IBPSA Peru",
    nav_ipcc: "IPCC Framework",
    nav_impacto: "What does +1°C mean?",
    nav_dato: "Climate Data",
    nav_ciudades: "By City",
    nav_carga: "Psychrometrics",
    nav_metodo: "Methodology",
    nav_fiable: "Reliability",
    nav_limites: "Conclusions",
    nav_referencias: "References",

    lbl_ciudad: "City:",
    btn_hoy: "Present",
    btn_animar: "▶ Play",
    btn_los_numeros: "The Data",
    heroKicker: "Interactive Climate Dissemination Tool & Technical EPW Weather Files Audit · IBPSA Peru",
    solPie: "Each ray represents one month on a <b>fixed calibrated scale from -6 to 36 °C</b> (rings at 0°, 10°, 20°, and 30°C). Click any city to compare dial radius and position.",

    ipcc_num: "IPCC Global Framework & CMIP6",
    ipcc_tit: "Global Temperature Pathways and Climate Model Ensembles",
    ipccLead: "Projections are grounded in the <b>IPCC (Sixth Assessment Report AR6)</b> and the <b>CMIP6 multi-model ensemble (23 global climate models)</b>. Explore global warming geographic distribution across Shared Socioeconomic Pathways (SSPs) and time horizons:",
    ssp126_btn: "SSP1-2.6 · Sustainability (Paris Goal)",
    ssp245_btn: "SSP2-4.5 · Central Pathway",
    ssp370_btn: "SSP3-7.0 · Regional Rivalry",
    ssp585_btn: "SSP5-8.5 · High-Stress Case (Fossil)",
    hz2050_btn: "Year 2050",
    hz2080_btn: "Year 2080",
    lbl_media_global: "Global Mean:",
    lbl_anomalia_proy: "Projected thermal anomaly (°C):",

    impacto_num: "Thermal Impact Framework",
    impacto_tit: "What do +1 °C, +2 °C, or +3 °C actually mean for human physiology, buildings, and the environment?",
    impactoLead: "An increase in the <b>annual mean</b> shifts the entire climatic distribution, non-linearly multiplying heatwaves, physiological thermal stress, building HVAC consumption, and Andean deglaciation. Select a warming tier to explore its direct impacts:",
    imp_s10_btn: "Present Day (Peru Today)",
    imp_s15_btn: "Paris Goal (SSP1-2.6)",
    imp_s20_btn: "Critical Threshold (SSP2-4.5 · 2050)",
    imp_s30_btn: "Severe Stress (SSP5-8.5 · 2080)",

    dato_num: "01 · Climate Data",
    dato_tit: "Select a time horizon and inspect the entire country",
    datoLead: "Annual mean temperature for each city. Toggle horizons and data <b>smoothly transition</b> to new projected values. Click any city to inspect its detailed bioclimatic card: 99th percentile, annual peak, humidity, and cooling demand.",
    h_hoy: "Present",
    h_hoy_sub: "TMYx Baseline 2011-2025",
    h_2030_sub: "Interpolated",
    h_2050_sub: "CMIP6 Modeled",
    h_2080_sub: "CMIP6 Modeled",
    esc_s245_btn: "SSP2-4.5 · Central Pathway (Shared Socioeconomic Pathway)",
    esc_s585_btn: "SSP5-8.5 · Stress Case (Shared Socioeconomic Pathway)",
    escNota: "SSP 8.5 scenarios represent severe stress testing cases for climate resilience sizing, not deterministic forecasts.",
    aviso_2030_t: "2030 is an interpolation, not a direct model",
    aviso_2030_b: "The Future Weather Generator (FWG / ADAI / Univ. Coimbra) models specifically horizons 2050 and 2080 based on CMIP6 GCMs. The 2030 column is linearly interpolated between the TMYx baseline and 2050. Because warming acceleration is non-linear, this figure likely <b>underestimates</b> actual trajectory.",

    ciudades_num: "02 · By City",
    ciudades_tit: "How it feels: monthly maximums and minimums",
    ciudadesLead: "An annual mean hides extremes. What occupants experience is February maximums and August minimums. <b>Toggle horizons</b> in the legend; double click to isolate a single horizon and display monthly numbers.",
    climoTit: "Month by month",
    ciudadesLead2: "Eight official surface weather stations (METAR / WMO), ranging from 32 m in coastal Trujillo to 3,826 m in Andean Juliaca. <b>Warming scales with elevation</b>: mountain highlands warm faster than the coast, although cooling energy consequences remain concentrated in humid lowlands.",
    trayTit: "Trajectory",
    barrasSubtit: "All eight cities · click any bar to lock that city and horizon",
    lbl_ordenar: "sort by",

    carga_num: "03 · Psychrometric Impact",
    carga_tit: "Hour-by-hour psychrometric behavior",
    nbLead: "Every dot represents one hour of the year for the selected city, plotted by dry-bulb temperature and humidity ratio. When projecting into future horizons, the cloud shifts <b>diagonally</b>: warmer air retains significantly more vapor. That is Clausius-Clapeyron visualized hour by hour.",
    btn_recorrer: " Advance to 2080",
    btn_color_mes: "Color: month",
    btn_color_hora: "Color: hour of day",
    nbPunto: "<b>Every point is one hour of the year</b> — one out of every six (1,460 hours total). The horizontal axis shows dry-bulb temperature and vertical axis shows absolute humidity (vapor ratio). Color indicates month or time of day. Summer hours cluster towards the top-right (hot and humid); winter hours stay towards the bottom-left.",
    aviso_multiplo_t: "Thermal multiples mislead without absolute magnitude",
    aviso_multiplo_b: "In Trujillo, cooling degree-hours multiply by 4.8x while in Piura only by 1.4x. Yet Trujillo increases by 706 °C·h while Piura rises by 6,479 °C·h. A large percentage multiplier occurs over a very small baseline.",

    metodo_num: "04 · Methodology",
    metodo_tit: "Six Steps of the Meteorological Audit Pipeline",
    metodoLead: "From an initial weather file download to a 2080 projection. These are the six steps of the audit methodology, complete with audited metrics, verified variables, and thermodynamic validation:",
    glos_morphing_t: "What is «Morphing»?",
    glos_morphing_p1: "<b>Hourly adjustment:</b> Takes the 8,760 baseline measured hours from the weather station and applies monthly climate anomalies projected by global climate models.",
    glos_morphing_p2: "<b>Why it matters:</b> Preserves local physical microclimates, diurnal swings, and real wind roses, while projecting thermal energy into future horizons.",
    glos_ensemble_t: "What is an «Ensemble»?",
    glos_ensemble_p1: "<b>Multi-model consensus:</b> Aggregates and averages projections from 23 independent global climate models (NOAA, NASA, Max Planck, etc.).",
    glos_ensemble_p2: "<b>Why it matters:</b> No single model is infallible; averaging the ensemble cancels individual biases and yields a robust consensus signal.",
    aviso_cc_t: "Clausius-Clapeyron Physical Consistency Check (Step 6)",
    aviso_cc_b: "As air warms at constant relative humidity, absolute moisture capacity increases at ~6.2 % per Kelvin (+6.2 %/K). The transformed FWG files exhibit rates between <b>7.60 and 7.79 %/K</b> (merely 1.5 pp deviation from theory, far below the 4.0 pp suspicion threshold). This confirms thermodynamic consistency was preserved.",

    fiable_num: "05 · Reliability",
    fiable_tit: "How much can you trust these figures?",
    fiableLead: "The numbers above originate from EPW weather files that had never been audited collectively for Peru. Here is the question-by-question technical verdict evaluating <b>internal consistency, hourly integrity, and thermodynamic plausibility</b>.",
    aviso_frase_t: "In a single sentence",
    aviso_frase_b: "Weather files are scientifically robust for comparative design sizing and passive building simulation; they do not constitute deterministic contract guarantees. Treat Lima's 2050 figure of «21.1 °C» as «approximately 21 °C», with an uncertainty band of ±1 °C.",

    limites_num: "06 · Scope & Limitations",
    limites_tit: "What this audit solves and what precautions it demands",
    limitesLead: "Clearly defining technical boundaries guarantees responsible engineering applications in architectural simulation and building decarbonization:",
    conc_aportes_t: "06.1 · Capabilities & Contributions",
    conc_aportes_badge: "Permitted Applications",
    conc_limites_t: "06.2 · Boundaries & Warnings",
    conc_limites_badge: "Engineering Precautions",
    dictamen_t: "Final Technical Audit Verdict",
    dictamen_d: "The transformed CMIP6 weather datasets are <b>fully valid and physically consistent for architectural pre-sizing, hygric modeling, and comparative thermal simulation</b> in Peru. For mission-critical projects, designers must factor in ENSO (El Niño) safety margins and cross-check solar irradiance against local pyranometers.",

    ap1_t: "Hourly Passive & Building Energy Simulation (8,760 h)",
    ap1_d: "Enables full-year modeling in EnergyPlus, DesignBuilder, or Ladybug of passive envelope performance, overheating hours, and adaptive comfort across 8 Peruvian macroclimates.",
    ap2_t: "Calculated ASHRAE Design Conditions (99.6% and 0.4%)",
    ap2_d: "Provides the extreme design percentiles required for HVAC sizing towards 2050 and 2080, even for highland cities that lacked design day headers such as Juliaca.",
    ap3_t: "Inter-Model Uncertainty Quantification (IPCC P10–P90)",
    ap3_d: "Integrates CMIP6 ensemble dispersion bounds (23 global models), enabling probabilistic safety factors in engineering and capital investment decisions.",
    ap4_t: "Historical Vintage Bias Audit on Baselines",
    ap4_d: "Identifies and quantifies historical baseline divergence (Meteonorm 1999 vs TMYx 2018), proving that 50% of temperature discrepancies stem from baseline age rather than model physics.",
    ap5_t: "Diagnosis of Nocturnal Natural Ventilation Limits",
    ap5_d: "Pinpoints specific months and hours where night temperatures exceed 20 °C (tropical nights), warning when conventional passive night flushing collapses.",

    lim1_t: "Stochastic El Niño (ENSO) Overload Events",
    lim1_d: "TMYx methodology synthesizes typical meteorological years and deliberately filters non-cyclical extremes. Designers across the northern and central coast must add +2.5 to +3.5 °C safety margins.",
    lim2_t: "Resolution Artifacts in Humboldt Upwelling",
    lim2_d: "Coarse 100–250 km GCM grids smooth the cold coastal upwelling along the Peruvian Pacific, requiring local calibration for immediate shoreline microclimates.",
    lim3_t: "High-Precision Direct Solar Irradiance",
    lim3_d: "Derived from ERA5 satellite reanalysis; critical photovoltaic or high-glazing solar projects should cross-check against SENAMHI / MINEM surface pyranometry.",
    lim4_t: "Formal Regulatory Status for Green Certifications",
    lim4_d: "Serves as independent scientific research and engineering audit. Does not override National Building Code (RNE) baseline tables nor mandatory certification datasets (EDGE/LEED).",
    lim5_t: "Hyperlocal Urban Heat Island (UHI) Effects",
    lim5_d: "Airport METAR weather stations do not capture dense urban canyon heat or anthropogenic emissions; dense metropolitan districts must factor in localized heat island deltas.",

    referencias_num: "Bibliographic References",
    referencias_tit: "Consulted Sources and International Standards (APA 7th Edition)",
    refLead: "The climatic, mathematical, and methodological foundation of this audit rests on the following peer-reviewed scientific literature and international norms:"
  }
};

const PLEGS_EN = {
  bulbo_seco: {
    t: "Does dry-bulb temperature work?",
    v: "Yes",
    b: "<p>The 40 EPW weather files contain complete 8,760 annual hours without gaps or missing records, with mean annual temperatures between 9.5 and 26.1 °C consistent with regional climatology. Absolute humidity tracks temperature following Clausius-Clapeyron with a discrepancy of only 1.5 percentage points from theory (well below the 4 pp threshold). For comparing construction types, pre-sizing HVAC systems, or evaluating passive strategies, the files are fully suitable.</p>"
  },
  solar: {
    t: "Does solar irradiance work?",
    v: "No",
    b: "<p>Lima reports 2,177 kWh/m² annual global horizontal radiation, <b>more than Cusco</b> with 1,991 kWh/m² — despite Cusco sitting 3,276 m higher and Lima having persistent marine cloud cover. Solar data in EPWs comes from ERA5 satellite reanalysis and the Jorge Chávez Airport is a METAR station measuring aviation visibility, not direct pyranometer solar flux. For photovoltaic or critical solar gain design, on-site pyranometry validation is required.</p>"
  },
  sanos: {
    t: "Are all EPW files healthy?",
    v: "Three are not",
    b: "<p>The historical 2004-2018 window for Cusco, Arequipa, and Juliaca deviates significantly from their other 4 time windows (+2.96 °C, +1.20 °C, -1.62 °C vs city median). <b>No coastal station shows this distortion.</b> Juliaca 2004-2018 also has an hourly autocorrelation of only 0.377 vs 0.845 in other windows. This high-altitude anomaly points to METAR station recording gaps in the Andes. We recommend avoiding those three specific windows.</p><div class='panel' style='margin-top:18px'><div id='vint'></div></div>"
  },
  linea_base: {
    t: "Does it matter which TMYx baseline is chosen?",
    v: "No",
    b: "<p>Between the full-period TMYx (1991-2020) and the recent window (2011-2025) there is a 0.35 °C gap in Lima, reaching up to 3.64 °C between windows in the same city.</p><p>This discrepancy <b>cannot be fixed with a simple subtraction</b>: the slope against centroid year is +0.18 °C/decade with r² of only 0.13. Temporal vintage introduces dispersion and uncertainty that cannot be neutralized by a flat multiplier.</p>"
  },
  convergencia: {
    t: "Do different climate methods agree?",
    v: "Partially",
    b: "<p>For Lima 2050, Meteonorm (CMIP5 / RCP8.5) reports 20.93 °C while FWG (CMIP6 / SSP5-8.5) projects 21.62 °C: <b>a +0.70 °C methodological discrepancy</b> over a total warming signal of ~2 °C. Half of this divergence (+0.35 °C) stems from historical baseline vintage (1999 vs 2018) rather than future model equations.</p><div class='panel' style='margin-top:18px'><div id='conv'></div></div>"
  },
  nino: {
    t: "Do files capture El Niño events?",
    v: "No",
    b: "<p>None do. Typical Meteorological Year (TMY / TMYx) files select representative typical months and <b>intentionally eliminate anomalous months by mathematical design</b>. On the Peruvian coast, El Niño (ENSO) drives peak thermal and moisture overload. If HVAC is sized exclusively on TMYx, equipment will be undersized for an El Niño event.</p>"
  }
};

const PLEGS_ES = {};
function initPlegsEs(){
  Object.keys(PLEGS_EN).forEach(k => {
    const el = $('pleg_' + k);
    if(el){
      PLEGS_ES[k] = {
        t: el.querySelector('.plegTit') ? el.querySelector('.plegTit').innerHTML : '',
        v: el.querySelector('.veredicto') ? el.querySelector('.veredicto').innerHTML : '',
        b: el.querySelector('.cuerpo') ? el.querySelector('.cuerpo').innerHTML : ''
      };
    }
  });
}

const IMP_DATA_EN = {
  s10: {
    nivel: '+1.0 °C',
    tit: 'Present Climatology (Peru Today · Baseline TMYx 2011–2025)',
    sub: 'Current baseline registered across surface meteorological stations in Peru.',
    cuerpo: {
      tit: 'Human Body Physiology',
      estado: 'Thermal equilibrium · Sweating mechanism functions normally',
      bullets: [
        '<b>Efficient physiological cooling:</b> Natural evaporation dissipates metabolic heat.',
        '<b>Restorative night rest:</b> Night temperatures drop below 18 °C, permitting deep sleep.',
        '<b>Moderate coastal humidity:</b> Tolerable sensation except during extraordinary heatwaves.'
      ]
    },
    edificio: {
      tit: 'Building Physics',
      estado: 'Passive operation · Night flush cooling operational',
      bullets: [
        '<b>Night flush cooling works:</b> Night ventilation discharges internal thermal mass.',
        '<b>Manageable roof overheating:</b> Traditional roofs do not transmit critical radiant loads.',
        '<b>Minimal artificial cooling demand:</b> HVAC required only in dense offices and hospitals.'
      ]
    },
    entorno: {
      tit: 'Environment, Glaciers & Water Resources',
      estado: 'Active glaciers > 4,800 m · Regular dry-season river flow',
      bullets: [
        '<b>Andean glacier mass:</b> Glaciers present above 4,800 m elevation.',
        '<b>Sustained seasonal discharge:</b> Regular dry-season water flow to Pacific coastal basins.',
        '<b>Active Humboldt upwelling:</b> Cold coastal waters sustaining pelagic fish biomass.'
      ]
    }
  },
  s15: {
    nivel: '+1.5 °C',
    tit: 'Paris Agreement Target (SSP1-2.6 · 2040–2050)',
    sub: 'Accelerated mitigation pathway with rapid emissions stabilization.',
    cuerpo: {
      tit: 'Human Body Physiology',
      estado: 'Coastal vapor effect · Thermal fatigue and perceived +3 °C',
      bullets: [
        '<b>Coastal vapor barrier:</b> In Lima and Trujillo, high humidity (>80%) impairs sweat evaporation.',
        '<b>Amplified perceived temperature:</b> Thermal sensation feels up to +3.0 °C warmer.',
        '<b>Emergence of warm nights:</b> Sleeping difficulty without continuous airflow.'
      ]
    },
    edificio: {
      tit: 'Building Physics',
      estado: 'Roofs at 55 °C · Doubling of cooling degree-hours',
      bullets: [
        '<b>Doubling of CDH:</b> Cooling energy required to maintain comfort doubles.',
        '<b>Lightweight roof overheating:</b> Corrugated sheets reach 55 °C radiating heat inward.',
        '<b>Shading alone becomes insufficient:</b> Continuous thermal envelope insulation is needed.'
      ]
    },
    entorno: {
      tit: 'Environment, Glaciers & Water Resources',
      estado: '50% glacier volume loss · Marine heatwaves',
      bullets: [
        '<b>Peak Water surpassed:</b> Progressive decline in dry-season baseflow across coastal rivers.',
        '<b>Coastal sea warming:</b> Sea surface temperatures at 18 °C+ driving anchovy deep offshore.',
        '<b>Loss of minor ice caps:</b> Extinction of glaciers below 5,000 m elevation.'
      ]
    }
  },
  s20: {
    nivel: '+2.0 °C',
    tit: 'Projected Critical Threshold (SSP2-4.5 · 2050)',
    sub: 'IPCC central trajectory towards 2050 without immediate deep emissions cuts.',
    cuerpo: {
      tit: 'Human Body Physiology',
      estado: 'Permanent tropical nights (>20 °C) · Chronic cardiovascular strain',
      bullets: [
        '<b>Persistent tropical nights (>20 °C):</b> Body fails to dissipate metabolic heat during sleep.',
        '<b>Cardiovascular strain:</b> Heart pumps continuously to vasodilate and cool skin throughout the night.',
        '<b>Daytime cognitive fatigue:</b> Chronic insomnia degrades academic and work performance.'
      ]
    },
    edificio: {
      tit: 'Building Physics',
      estado: 'Roofs at 65 °C · Complete collapse of passive night cooling',
      bullets: [
        '<b>Collapse of nocturnal passive cooling:</b> Night air (>20 °C) cannot cool thermal mass.',
        '<b>Public health necessity of AC:</b> Cooling shifts from luxury to an essential health shield.',
        '<b>Tripled electric utility bills:</b> Severe strain on metropolitan power grids.'
      ]
    },
    entorno: {
      tit: 'Environment, Glaciers & Water Resources',
      estado: 'Irreversible deglaciation below 5,200 m · Severe coastal water stress',
      bullets: [
        '<b>Irreversible Andean melting:</b> Near-total disappearance of glaciers in Central Cordillera.',
        '<b>Dry-season water rationing:</b> Acute scarcity for municipal drinking water and agriculture.',
        '<b>Economic loss:</b> Decline in industrial fisheries and coastal agricultural export yields.'
      ]
    }
  },
  s30: {
    nivel: '+3.0 °C+',
    tit: 'Severe Stress Case (SSP5-8.5 · 2080)',
    sub: 'Extreme unmitigated fossil fuel expansion towards end of century.',
    cuerpo: {
      tit: 'Human Body Physiology',
      estado: 'Wet-bulb threshold exceeded (28–30 °C+) · Risk of fatal heatstroke',
      bullets: [
        '<b>Wet-bulb limit reached:</b> Saturated air completely halts metabolic heat dissipation.',
        '<b>Lethal heat risk at rest:</b> Core body temperature surpasses 40 °C within hours without AC.',
        '<b>Surging heat mortality:</b> Recurrent health emergencies across Amazon basin and North Coast.'
      ]
    },
    edificio: {
      tit: 'Building Physics',
      estado: 'Uninhabitable afternoon interiors · Grid blackouts',
      bullets: [
        '<b>Uninhabitable uninsulated homes:</b> Uninsulated houses become thermal ovens (>36 °C).',
        '<b>Skyrocketing power consumption:</b> HVAC demand multiplied by 4 to 5x.',
        '<b>Widespread blackouts:</b> Overheating and transformer failures across urban substations.'
      ]
    },
    entorno: {
      tit: 'Environment, Glaciers & Water Resources',
      estado: 'Mass glacier extinction (>85%) · Chronic metropolitan water rationing',
      bullets: [
        '<b>Near-total Peruvian deglaciation:</b> Disappearance of ice fields in Cordillera Blanca.',
        '<b>Metropolitan water crisis:</b> Severe chronic rationing in Lima across the Rímac basin.',
        '<b>Accelerated desertification:</b> Agricultural valley collapse and highland wildfires.'
      ]
    }
  }
};

/* ════════════════════════════════════════════════════════════════════════════════
   DICCIONARIO EN INGLÉS PARA EL MARCO IPCC Y MAPAS
   ════════════════════════════════════════════════════════════════════════════════ */

const IPCC_EN = {
  mapTitle: "Projected Global Warming: {esc} (Year {hz})",
  mapSubtitle: "{desc} · Expected CO₂ concentration: {co2}",
  pinDefault: "💡 Click or hover over highlighted map points (Peruvian Coast, Amazon, Andes, Tropical Pacific, Arctic) to explore regional climate dynamics.",
  escenarios: {
    ssp126: {
      nombre: "SSP1-2.6 · Sustainability (Paris Goal)",
      short: "SSP1-2.6 · Paris Goal",
      desc: "Net zero global emissions by 2050, followed by net carbon removal. Warming stays around 1.5–1.8 °C."
    },
    ssp245: {
      nombre: "SSP2-4.5 · Central Pathway",
      short: "SSP2-4.5 · Central Pathway",
      desc: "Intermediate trajectory: global emissions hover around current levels before declining after 2050."
    },
    ssp370: {
      nombre: "SSP3-7.0 · Regional Rivalry",
      short: "SSP3-7.0 · Regional Rivalry",
      desc: "High emissions, regional fragmentation, and slow technological progress in decarbonization."
    },
    ssp585: {
      nombre: "SSP5-8.5 · Severe Stress Case (Fossil)",
      short: "SSP5-8.5 · Stress Case",
      desc: "Rapid fossil-fueled economic expansion. Severe benchmark scenario to size worst-case building resilience."
    }
  },
  puntos: [
    {
      n: "Peruvian Coast (Lima / Trujillo)",
      desc: "Warming moderated by the cold Humboldt upwelling (+1.2 to +1.8 °C). Extreme increase in humid heat index."
    },
    {
      n: "Amazon Basin (Iquitos / Pucallpa)",
      desc: "Intense warming (+2.0 to +3.5 °C). Critical wet-bulb temperatures and risk of biome forest dieback."
    },
    {
      n: "Andean Altiplano & Cordillera (Cusco / Juliaca)",
      desc: "Elevation-dependent warming amplification (+2.5 to +4.0 °C). Accelerated glacier retreat and hydrological shifts."
    },
    {
      n: "Eastern Tropical Pacific",
      desc: "Marine heatwaves, weakened trade winds, and amplified risk of severe coastal El Niño (ENSO) events."
    },
    {
      n: "Arctic Ocean",
      desc: "Arctic amplification: polar warming proceeds at 2.5 to 3 times the global average rate."
    }
  ]
};

// Interceptores para traducción bilingüe de componentes dinámicos
const _origPortada = portada;
portada = function(){
  _origPortada();
  if(currentLang === 'en'){
    const c = D.ciudades.find(o => o.n === sel) || D.ciudades[0];
    const L45 = c.s245.H, L85 = c.s585.H;
    if($('heroTit')) $('heroTit').innerHTML = `${c.n} will average <em>${F(L45.a2050.T, 1)} °C</em> in 2050`;
    if($('heroSubtit')) $('heroSubtit').innerHTML = `That is under central scenario SSP2-4.5 (Intermediate Shared Socioeconomic Pathway). Under severe stress scenario SSP5-8.5, ${F(L85.a2050.T, 1)} °C. Eight Peruvian macroclimates, four horizons, and an interactive tool bridging climate science, decision-makers, and building performance.`;
    if($('grande')){
      const exist = $('grande').querySelectorAll('.cifra');
      if(exist.length === HOR.length){
        HOR.forEach((h, idx) => {
          const lbl = exist[idx].querySelector('.c');
          const itp = D.interpolado.includes(h);
          const hName = h === 'hoy' ? 'today' : (h === 'a2030' ? 'in 2030' : (h === 'a2050' ? 'in 2050' : 'in 2080'));
          if(lbl) lbl.innerHTML = `${c.n} ${hName}${itp ? ' <em>interp.</em>' : ''}`;
        });
      }
    }
  }
};

const _origFicha = ficha;
ficha = function(){
  _origFicha();
  if(currentLang === 'en'){
    const c = D.ciudades.find(o => o.n === sel), h = G(c, hz), b = G(c, 'hoy');
    const f = (l, v, up) => `<div class="fila"><span>${l}</span><b class="${up ? 'up' : ''}">${v}</b></div>`;
    const dl = (v, u, d = 2) => hz === 'hoy' ? '' : ` <span style="color:var(--calor-tx)">(+${F(v, d)}${u})</span>`;
    const hName = hz === 'hoy' ? 'Present' : (hz === 'a2030' ? '2030' : (hz === 'a2050' ? '2050' : '2080'));
    $('ficha').innerHTML = `<h3>${c.n}</h3>
     <span class="zn">${c.zona} · ${N(c.elev)} m · ${hName}</span>
     ${f('Annual mean temperature', F(h.T, 1) + ' °C' + dl(h.T - b.T, ' °C'), 1)}
     ${f('Heating design day (99.6 %)', (h.tcal !== undefined ? F(h.tcal, 1) + ' °C' + dl(h.tcal - b.tcal, ' °C', 1) : '—'))}
     ${f('Cooling design day (0.4 %)', (h.tref !== undefined ? F(h.tref, 1) + ' °C' + dl(h.tref - b.tref, ' °C', 1) : F(h.p99, 1) + ' °C'))}
     ${f('99th percentile dry-bulb', F(h.p99, 1) + ' °C' + dl(h.p99 - b.p99, ' °C', 1))}
     ${f('Annual maximum temperature', F(h.mx, 1) + ' °C' + dl(h.mx - b.mx, ' °C', 1))}
     ${f('Absolute humidity ratio', F(h.W, 1) + ' g/kg' + dl(h.W - b.W, ' g/kg', 1))}
     ${f('Hours above 26 °C', N(h.h26) + ' h')}
     ${f('Cooling degree-hours (CDH)', N(h.gh) + ' °C·h')}
     ${f('Baseline weather file', c.y0.toFixed(0) + ' · TMYx 2011-2025')}`;
  }
};

const _origTarjetas = tarjetas;
tarjetas = function(desde, hasta, k){
  _origTarjetas(desde, hasta, k);
  if(currentLang === 'en'){
    const d = [...D.ciudades].sort((a, b) => G(b, 'hoy').T - G(a, 'hoy').T);
    $('rej').innerHTML = d.map(c => {
      const T = mez(G(c, desde).T, G(c, hasta).T, k), d0 = T - G(c, 'hoy').T, col = escala(T, 8, 31);
      return `<div class="tarj ${c.n === sel ? 'on' : ''}" onclick="pick('${c.n}')">
        <div class="cinta" style="background:${col}"></div>
        <div class="cd">${c.n}</div><div class="zn">${c.zona} · ${N(c.elev)} m</div>
        <div class="tt" style="color:${col}">${F(T, 1)}<span> °C</span></div>
        <div class="dd" style="color:${d0 > .05 ? 'var(--calor-tx)' : 'var(--tinta3)'}">
          ${d0 > .05 ? `&#9650; +${F(d0)} °C vs present` : 'baseline'}</div></div>`;
    }).join('');
  }
};

const _origImpactoDibuja = impactoDibuja;
impactoDibuja = function(){
  if(currentLang !== 'en'){
    _origImpactoDibuja();
    return;
  }
  const d = IMP_DATA_EN[impNivel];
  if(!d) return;

  if($('impHeaderBox')){
    $('impHeaderBox').innerHTML = `
      <div>
        <h3>${d.tit}</h3>
        <p>${d.sub}</p>
      </div>
      <div class="impHeaderBadge" style="background:${impNivel==='s10'?'#fdf2d0':(impNivel==='s15'?'#fde3c7':(impNivel==='s20'?'#fad1bc':'#f7bcc4'))};color:${impNivel==='s10'?'#8c6d1f':(impNivel==='s15'?'#b24b00':(impNivel==='s20'?'#b3261e':'#910b28'))}">${d.nivel}</div>
    `;
  }

  if($('impGrid3')){
    $('impGrid3').innerHTML = `
      <div class="impColCard">
        <h4>${d.cuerpo.tit}</h4>
        <div class="impColEstado" style="color:${impNivel==='s10'?'#8c6d1f':(impNivel==='s15'?'#b24b00':(impNivel==='s20'?'#b3261e':'#910b28'))}">${d.cuerpo.estado}</div>
        <ul class="impUl">
          ${d.cuerpo.bullets.map(b => `<li class="impLi"><span class="impLiDot" style="background:${impNivel==='s10'?'#8c6d1f':(impNivel==='s15'?'#b24b00':(impNivel==='s20'?'#b3261e':'#910b28'))}"></span><div>${b}</div></li>`).join('')}
        </ul>
      </div>

      <div class="impColCard">
        <h4>${d.edificio.tit}</h4>
        <div class="impColEstado" style="color:${impNivel==='s10'?'#8c6d1f':(impNivel==='s15'?'#b24b00':(impNivel==='s20'?'#b3261e':'#910b28'))}">${d.edificio.estado}</div>
        <ul class="impUl">
          ${d.edificio.bullets.map(b => `<li class="impLi"><span class="impLiDot" style="background:${impNivel==='s10'?'#8c6d1f':(impNivel==='s15'?'#b24b00':(impNivel==='s20'?'#b3261e':'#910b28'))}"></span><div>${b}</div></li>`).join('')}
        </ul>
      </div>

      <div class="impColCard">
        <h4>${d.entorno.tit}</h4>
        <div class="impColEstado" style="color:${impNivel==='s10'?'#8c6d1f':(impNivel==='s15'?'#b24b00':(impNivel==='s20'?'#b3261e':'#910b28'))}">${d.entorno.estado}</div>
        <ul class="impUl">
          ${d.entorno.bullets.map(b => `<li class="impLi"><span class="impLiDot" style="background:${impNivel==='s10'?'#8c6d1f':(impNivel==='s15'?'#b24b00':(impNivel==='s20'?'#b3261e':'#910b28'))}"></span><div>${b}</div></li>`).join('')}
        </ul>
      </div>
    `;
  }
};

/* ── Interceptores de Gráficos y Mapas Internos ── */

const _origIpccMapa = ipccMapa;
ipccMapa = function(){
  _origIpccMapa();
  if(currentLang === 'en' && D.ipcc){
    const ipcc = D.ipcc;
    const esc = ipcc.escenarios[ipccEsc];
    const escEn = IPCC_EN.escenarios[ipccEsc] || esc;
    const dT_global = ipccHz === 2050 ? esc.dT_2050 : esc.dT_2080;
    const p10 = ipccHz === 2050 ? esc.p10_2050 : esc.p10_2080;
    const p90 = ipccHz === 2050 ? esc.p90_2050 : esc.p90_2080;

    if($('ipccMapTit')) $('ipccMapTit').innerHTML = `Projected Global Warming: ${escEn.nombre} (Year ${ipccHz})`;
    if($('ipccMapSubtit')) $('ipccMapSubtit').innerHTML = `${escEn.desc} · Expected CO₂ concentration: ${esc.co2_2100}`;
    if($('ipccGlobalVal')) $('ipccGlobalVal').innerHTML = `+${F(dT_global,1)} °C <span style="font-size:12px;font-weight:600;color:var(--tinta3)">[P10: +${F(p10,1)}°, P90: +${F(p90,1)}°]</span>`;
    
    if($('ipccPinDetail') && ipccPinSel < 0){
      $('ipccPinDetail').innerHTML = IPCC_EN.pinDefault;
      $('ipccPinDetail').classList.remove('activo');
    }

    if($('sspCardsGrid')){
      const keys = ['ssp126','ssp245','ssp370','ssp585'];
      $('sspCardsGrid').innerHTML = keys.map(k => {
        const e = ipcc.escenarios[k];
        const eEn = IPCC_EN.escenarios[k] || e;
        const dT = ipccHz === 2050 ? e.dT_2050 : e.dT_2080;
        const kP10 = ipccHz === 2050 ? e.p10_2050 : e.p10_2080;
        const kP90 = ipccHz === 2050 ? e.p90_2050 : e.p90_2080;
        const isAct = (k === ipccEsc);
        return `<div class="sspCard ${isAct ? 'on' : ''}" onclick="setIpccEsc('${k}')" style="cursor:pointer">
          <h5 style="color:${isAct ? 'var(--acento)' : 'var(--tinta)'}">${eEn.short}</h5>
          <div class="sspCo2">CO₂: ${e.co2_2100} · <b>+${F(dT,1)} °C in ${ipccHz}</b></div>
          <div style="font-size:11.5px;color:var(--calor-tx);font-weight:600;margin-bottom:6px">Inter-model spread: [+${F(kP10,1)}° to +${F(kP90,1)}°]</div>
          <p>${eEn.desc}</p>
        </div>`;
      }).join('');
    }
  }
};

const _origVerPin = verPin;
verPin = function(i, isClick = false){
  if(currentLang !== 'en'){
    _origVerPin(i, isClick);
    return;
  }
  if(!D.ipcc || !D.ipcc.puntos || !D.ipcc.puntos[i]) return;
  if(isClick){
    ipccPinSel = (ipccPinSel === i ? -1 : i);
  }
  if(ipccPinSel === -1 && isClick){
    if($('ipccPinDetail')){
      $('ipccPinDetail').innerHTML = IPCC_EN.pinDefault;
      $('ipccPinDetail').classList.remove('activo');
    }
    document.querySelectorAll('.ipccPin').forEach(el => el.classList.remove('on'));
    return;
  }
  const curIdx = isClick && ipccPinSel === -1 ? 0 : (isClick ? ipccPinSel : i);
  const ptEn = IPCC_EN.puntos[curIdx] || D.ipcc.puntos[curIdx];
  const esc = D.ipcc.escenarios[ipccEsc];
  const escEn = IPCC_EN.escenarios[ipccEsc] || esc;
  const dT_global = ipccHz === 2050 ? esc.dT_2050 : esc.dT_2080;
  const ptRaw = D.ipcc.puntos[curIdx];
  const dT_pt = dT_global * ptRaw.m;
  if($('ipccPinDetail')){
    $('ipccPinDetail').innerHTML = `<b>📍 ${ptEn.n}:</b> Projected anomaly <b>+${F(dT_pt,1)} °C</b> in ${ipccHz} (${escEn.short}). ${ptEn.desc}`;
    $('ipccPinDetail').classList.add('activo');
  }
  document.querySelectorAll('.ipccPin').forEach((el, idx) => {
    el.classList.toggle('on', idx === (ipccPinSel >= 0 ? ipccPinSel : i));
  });
};

const _origClimograma = climograma;
climograma = function(){
  _origClimograma();
  if(currentLang === 'en'){
    const c = D.ciudades.find(o => o.n === sel), CG = c[escen].CG;
    const act = HOR.filter(h => cgVis[h]);
    const M_EN = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const HET_EN = { hoy: 'Present', a2030: '2030', a2050: '2050', a2080: '2080' };

    if($('climoTit')) $('climoTit').textContent = `${c.n} month by month · ${c.zona} · ${N(c.elev)} m`;

    const climoSvg = $('climo') ? $('climo').querySelector('svg') : null;
    if(climoSvg){
      climoSvg.querySelectorAll('text.lbl2').forEach(t => {
        if(t.textContent.includes('Temperatura de bulbo seco')) t.textContent = 'Dry-bulb temperature (°C)';
        const val = t.textContent.trim();
        const mIdx = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'].indexOf(val);
        if(mIdx >= 0) t.textContent = M_EN[mIdx];
      });
      climoSvg.querySelectorAll('text.lbl').forEach(t => {
        if(t.textContent.includes('Hemisferio sur')) t.textContent = 'Southern Hemisphere: summer in Jan–Mar, winter in Jun–Aug.';
      });
      climoSvg.querySelectorAll('text.val').forEach(t => {
        const val = t.textContent.trim();
        if(val === 'Hoy') t.textContent = 'Present';
      });
    }

    const guia = `<div class="cgGuia">
      <span><svg width="34" height="14"><line x1="1" y1="7" x2="33" y2="7" stroke="#3d4657" stroke-width="3"/></svg> Monthly mean</span>
      <span><svg width="34" height="14"><rect x="1" y="2" width="32" height="10" rx="2" fill="#3d4657" opacity=".18"/><line x1="1" y1="3" x2="33" y2="3" stroke="#3d4657" stroke-width="1.3" stroke-dasharray="4 3"/><line x1="1" y1="11" x2="33" y2="11" stroke="#3d4657" stroke-width="1.3" stroke-dasharray="4 3"/></svg> Band: daily mean min to max</span></div>`;
    
    const rangos = act.map(h => {
      const g = CG[h], mn = Math.min(...g.minm), mx = Math.max(...g.maxm);
      const iM = g.maxm.indexOf(mx), im = g.minm.indexOf(mn);
      return `<div class="cgRango" style="--c:${CGCOL[h]}">
        <b>${HET_EN[h]}${D.interpolado.includes(h)?' · interp.':''}</b>
        <span>${F(mn,1)} to ${F(mx,1)} °C</span>
        <em>min in ${M_EN[im]} · max in ${M_EN[iM]} · diurnal swing ${F(mx-mn,1)} °C</em></div>`;
    }).join('');

    if($('cgInfo')) $('cgInfo').innerHTML = guia + `<div class="cgRangos">${rangos}</div>`;

    if($('cgLeg')){
      $('cgLeg').innerHTML = HOR.map(h =>
        `<button class="cgChip ${cgVis[h]?'on':''}" onclick="cgToggle('${h}')"
           ondblclick="cgSolo('${h}')" aria-pressed="${cgVis[h]}"
           title="Click: toggle · double click: isolate">
           <i style="background:${CGCOL[h]}"></i>${HET_EN[h]}</button>`).join('')
        + `<button class="cgChip todos" onclick="cgTodos()">All</button>`;
    }
  }
};

const _origTrayectoria = trayectoria;
trayectoria = function(){
  _origTrayectoria();
  if(currentLang === 'en'){
    const c = D.ciudades.find(o => o.n === sel);
    const obs = c.obs;
    const mn = Math.min(...obs.map(o => o[1])), mx = Math.max(...obs.map(o => o[1]));
    if($('trayTit')) $('trayTit').innerHTML = `${c.n} · from ${obs[0][0].toFixed(0)} to 2080 &nbsp; <span style="font-weight:400;color:var(--tinta3);font-size:12px">the five measured historical windows differ by ${F(mx-mn,2)} °C</span>`;

    const traySvg = $('tray') ? $('tray').querySelector('svg') : null;
    if(traySvg){
      traySvg.querySelectorAll('text.lbl').forEach(t => {
        const val = t.textContent.trim();
        if(val === 'medido') t.textContent = 'measured';
        else if(val === 'proyectado') t.textContent = 'projected';
        else if(val.includes('ventanas TMYx')) t.textContent = 'measured TMYx windows · open circle = interpolated · click point to switch horizon';
      });
      traySvg.querySelectorAll('text.lbl2').forEach(t => {
        if(t.textContent.includes('Temperatura media anual')) t.textContent = 'Annual mean temperature (°C)';
      });
    }
  }
};

const _origBarras = barras;
barras = function(){
  _origBarras();
  if(currentLang === 'en'){
    const barSvg = $('barras') ? $('barras').querySelector('svg') : null;
    if(barSvg){
      barSvg.querySelectorAll('text.lbl2').forEach(t => {
        if(t.textContent.includes('Temperatura media anual')) t.textContent = 'Annual mean temperature (°C)';
      });
      barSvg.querySelectorAll('text.lbl').forEach(t => {
        const txt = t.textContent.trim();
        if(txt.includes('a 2080')) t.textContent = txt.replace('a 2080', 'by 2080');
        else if(txt === 'Hoy') t.textContent = 'Present';
      });
    }
    if($('barrasSubtit')) $('barrasSubtit').textContent = 'All eight cities · click any bar to lock that city and horizon';
    if($('brSort')){
      const sortMap = [['a2080','temperature'],['dif','warming'],['elev','elevation'],['n','name']];
      $('brSort').innerHTML = sortMap.map(([k,et]) =>
        `<button class="${brOrden===k?'on':''}" data-k="${k}" onclick="brSort('${k}')">${et}</button>`).join('');
    }
  }
};

const _origNube = nube;
nube = function(){
  _origNube();
  if(currentLang === 'en'){
    const nubeSvg = $('nube') ? $('nube').querySelector('svg') : null;
    if(nubeSvg){
      nubeSvg.querySelectorAll('text.lbl2').forEach(t => {
        const txt = t.textContent;
        if(txt.includes('Temperatura de bulbo seco')) t.textContent = 'Dry-bulb temperature (°C) — air temperature';
        else if(txt.includes('Humedad absoluta')) t.textContent = 'Absolute humidity (g moisture per kg dry air)';
      });
    }
    const HET_EN = { hoy: 'Present', a2030: '2030', a2050: '2050', a2080: '2080' };
    const ent = Math.round(prog);
    if($('estado')){
      $('estado').innerHTML = Math.abs(prog-ent) < .02
        ? `<b>${HET_EN[NHOR[ent]]}</b>${ent ? ' · ' + D.nube_escenario : ' · TMYx 2011-2025'}${D.interpolado.includes(NHOR[ent]) ? ' · interpolated' : ''}`
        : `${HET_EN[NHOR[Math.floor(prog)]]} → ${HET_EN[NHOR[Math.ceil(prog)]]}`;
    }
    const M_EN = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const items = nbCol === 'mes'
      ? M_EN.map((m, i) => [MESCOL[i], m, i])
      : [[horaCol(2),'0–3 h',0],[horaCol(6),'4–7 h',1],[horaCol(10),'8–11 h',2],
         [horaCol(14),'12–15 h',3],[horaCol(18),'16–19 h',4],[horaCol(22),'20–23 h',5]];
    if($('nbLeg')){
      $('nbLeg').innerHTML = items.map(([col,et,i]) =>
        `<button class="nbChip ${nbSel===i?'on':(nbSel<0?'':'off')}" onclick="nbPick(${i})"
           title="Click to isolate"><i style="background:${col}"></i>${et}</button>`).join('')
        + (nbSel>=0 ? `<button class="nbChip todos" onclick="nbPick(${nbSel})">Show all</button>` : '');
    }
  }
};

const _origSolDibuja = solDibuja;
solDibuja = function(){
  _origSolDibuja();
  if(currentLang === 'en'){
    const solSvg = $('heroViz') ? $('heroViz').querySelector('svg') : null;
    if(solSvg){
      solSvg.querySelectorAll('text').forEach(t => {
        const txt = t.textContent.trim();
        if(txt === 'Confort') t.textContent = 'Comfort';
        else if(txt === 'HOY') t.textContent = 'PRESENT';
        else if(txt === 'ENE') t.textContent = 'JAN';
        else if(txt === 'ABR') t.textContent = 'APR';
        else if(txt === 'AGO') t.textContent = 'AUG';
        else if(txt === 'DIC') t.textContent = 'DEC';
      });
    }
  }
};

const _origConverg = converg;
converg = function(){
  _origConverg();
  if(currentLang === 'en'){
    const convSvg = $('conv') ? $('conv').querySelector('svg') : null;
    if(convSvg){
      convSvg.querySelectorAll('text.lbl2').forEach(t => {
        const txt = t.textContent.trim();
        if(txt.includes('TMYx completo')) t.textContent = 'TMYx full (1991–2020)';
        else if(txt.includes('TMYx reciente')) t.textContent = 'TMYx recent (2011–2025)';
        else if(txt.includes('Meteonorm')) t.textContent = 'Meteonorm 2050 (CMIP5)';
        else if(txt.includes('FWG 2050')) t.textContent = 'FWG 2050 (CMIP6 / FWG v4.2)';
      });
      convSvg.querySelectorAll('text.lbl').forEach(t => {
        const txt = t.textContent.trim();
        if(txt.includes('Línea base')) t.textContent = txt.replace('Línea base', 'Baseline').replace('Centroide', 'Centroid');
        else if(txt.includes('Síntesis estocástica')) t.textContent = 'RCP8.5 · Stochastic synthesis';
        else if(txt.includes('Morphing climático')) t.textContent = 'SSP5-8.5 · Climate morphing';
      });
      convSvg.querySelectorAll('text').forEach(t => {
        if(t.textContent.includes('diferencia metodológica')){
          const c = D.conv;
          t.textContent = `${c.divergencia_absoluta_C>0?'+':''}${F(c.divergencia_absoluta_C)} °C methodological discrepancy`;
        }
      });
    }
  }
};

const _origVintage = vintage;
vintage = function(){
  _origVintage();
  if(currentLang === 'en'){
    const vintSvg = $('vint') ? $('vint').querySelector('svg') : null;
    if(vintSvg){
      vintSvg.querySelectorAll('text.lbl2').forEach(t => {
        const txt = t.textContent.trim();
        if(txt.includes('Diferencia de año centroide')) t.textContent = 'Centroid year difference vs full-period TMYx (years)';
        else if(txt.includes('ΔT aparente')) t.textContent = 'Apparent ΔT (°C)';
      });
    }
  }
};

function traducirPlegables(){
  const isEn = (currentLang === 'en');
  Object.keys(PLEGS_EN).forEach(k => {
    const el = $('pleg_' + k);
    if(!el) return;
    const data = isEn ? PLEGS_EN[k] : PLEGS_ES[k];
    if(!data) return;
    const titEl = el.querySelector('.plegTit');
    const vEl = el.querySelector('.veredicto');
    const bEl = el.querySelector('.cuerpo');
    if(titEl && data.t) titEl.innerHTML = data.t;
    if(vEl && data.v) vEl.innerHTML = data.v;
    if(bEl && data.b) bEl.innerHTML = data.b;
  });
}

function setLang(lang){
  if(!DICT[lang]) return;
  currentLang = lang;
  document.documentElement.lang = lang;
  
  if($('btnEs')) $('btnEs').classList.toggle('on', lang === 'es');
  if($('btnEn')) $('btnEn').classList.toggle('on', lang === 'en');

  const d = DICT[lang];

  // Actualizar atributos data-i18n
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if(d[key]) el.innerHTML = d[key];
  });

  // Actualizar Título
  if(d.pageTitle) document.title = d.pageTitle;

  // Actualizar encabezados directos
  if($('heroKicker') && d.heroKicker) $('heroKicker').innerHTML = d.heroKicker;
  if($('solPie') && d.solPie) $('solPie').innerHTML = d.solPie;
  if($('ipccLead') && d.ipccLead) $('ipccLead').innerHTML = d.ipccLead;
  if($('impactoLead') && d.impactoLead) $('impactoLead').innerHTML = d.impactoLead;
  if($('datoLead') && d.datoLead) $('datoLead').innerHTML = d.datoLead;
  if($('ciudadesLead') && d.ciudadesLead) $('ciudadesLead').innerHTML = d.ciudadesLead;
  if($('ciudadesLead2') && d.ciudadesLead2) $('ciudadesLead2').innerHTML = d.ciudadesLead2;
  if($('nbLead') && d.nbLead) $('nbLead').innerHTML = d.nbLead;
  if($('metodoLead') && d.metodoLead) $('metodoLead').innerHTML = d.metodoLead;
  if($('fiableLead') && d.fiableLead) $('fiableLead').innerHTML = d.fiableLead;
  if($('limitesLead') && d.limitesLead) $('limitesLead').innerHTML = d.limitesLead;
  if($('refLead') && d.refLead) $('refLead').innerHTML = d.refLead;
  if($('escNota') && d.escNota) $('escNota').innerHTML = d.escNota;
  if($('barrasSubtit') && d.barrasSubtit) $('barrasSubtit').innerHTML = d.barrasSubtit;

  // Actualizar textos del Footer
  if($('footerMainText')){
    $('footerMainText').innerHTML = (lang === 'en')
      ? '© 2026 <strong>Abelardo Tomás Palacios Hurtado &amp; IBPSA Peru</strong> · Interactive Climate Change Dissemination Tool and EPW Weather Files Technical Audit for Peru towards 2030, 2050, and 2080.'
      : '© 2026 <strong>Abelardo Tomás Palacios Hurtado &amp; IBPSA Perú</strong> · Herramienta interactiva de difusión sobre cambio climático y auditoría técnica de archivos EPW para el Perú hacia 2030, 2050 y 2080.';
  }
  if($('footerSubText')){
    $('footerSubText').innerHTML = (lang === 'en')
      ? 'Open science published under <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a> license · <a href="https://github.com/IBPSA-Peru/Clima-Per-2080" target="_blank" rel="noopener">GitHub Repository</a> · <a href="https://ibpsa-peru.github.io/Clima-Per-2080/" target="_blank" rel="noopener">ibpsa-peru.github.io/Clima-Per-2080</a>'
      : 'Investigación y datos abiertos bajo licencia <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a> · <a href="https://github.com/IBPSA-Peru/Clima-Per-2080" target="_blank" rel="noopener">Repositorio en GitHub</a> · <a href="https://ibpsa-peru.github.io/Clima-Per-2080/" target="_blank" rel="noopener">ibpsa-peru.github.io/Clima-Per-2080</a>';
  }

  // Redibujar componentes dinámicos con el idioma activo
  portada();
  tarjetas(hz, hz, 1);
  mapa(hz, hz, 1);
  ficha();
  renderStepper();
  impactoDibuja();
  traducirPlegables();
  ipccMapa();
  climograma();
  trayectoria();
  barras();
  nube();
  solDibuja();
  if($('vint') && $('vint').innerHTML) vintage();
  if($('conv') && $('conv').innerHTML) converg();

  try { localStorage.setItem('ibpsa_clima_lang', lang); } catch(e){}
}

// Cargar preferencia previa de idioma si existe
try {
  const savedLang = localStorage.getItem('ibpsa_clima_lang');
  if(savedLang && DICT[savedLang]) currentLang = savedLang;
} catch(e){}

if(window.location.search.includes('lang=en')) currentLang = 'en';
else if(window.location.search.includes('lang=es')) currentLang = 'es';

// Asegurar visibilidad de secciones con transición suave o directa
document.body.classList.remove('anim');
document.querySelectorAll('section').forEach(s => s.classList.add('vis'));

if(window.location.hash){
  try {
    const t = document.querySelector(window.location.hash);
    if(t) window.scrollTo(0, t.offsetTop);
  } catch(e){}
}

// Modo aislado para capturas y pruebas de secciones específicas
try {
  const urlParams = new URLSearchParams(window.location.search);
  const shot = urlParams.get('shot');
  if(shot){
    if(shot === 'footer'){
      document.querySelectorAll('section, header.top, .tip').forEach(el => el.style.display = 'none');
      const ft = document.querySelector('footer.siteFooter');
      if(ft) ft.style.marginTop = '0';
    } else {
      document.querySelectorAll('section').forEach(s => {
        if(s.id !== shot) s.style.display = 'none';
        else { s.style.display = 'block'; s.classList.add('vis'); }
      });
      if(document.querySelector('header.top')) document.querySelector('header.top').style.display = 'none';
    }
  }
} catch(e){}

// Iniciar componentes al cargar
initPlegsEs();
renderStepper();
if(currentLang !== 'es') setLang(currentLang);
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title id="pageTitle">Cambio Climático y Confort Térmico en Perú hacia 2080 · Auditoría EPW | IBPSA Perú</title>
<meta name="description" content="Herramienta interactiva sobre el impacto del cambio climático y confort térmico en el Perú hacia 2030, 2050 y 2080; y auditoría técnica de archivos EPW por Abelardo Tomás Palacios Hurtado e IBPSA Perú.">
<style>
__CSS__
</style></head><body>
<div class="tip" id="tip" role="status" aria-live="polite"></div>

<!-- ══ Cabecera Superior Fija ══ -->
<header class="top"><div class="wrap">
  <div class="marca">
    <img src="data:image/png;base64,__LOGO_B64__" alt="Logo IBPSA Perú" class="marcaLogo" width="26" height="26">
    <span class="marcaTit">CLIMA <i>PERÚ</i> 2080 <span class="marcaSep">|</span> <span class="marcaOrg">IBPSA PERÚ</span></span>
  </div>
  <nav class="migas" aria-label="Capítulos">__MIGAS__</nav>
  <div class="langSwitch" role="group" aria-label="Idioma / Language">
    <button id="btnEs" class="langBtn on" onclick="setLang('es')" title="Ver en Español">ES</button>
    <span class="langSep">/</span>
    <button id="btnEn" class="langBtn" onclick="setLang('en')" title="View in English">EN</button>
  </div>
</div></header>

<!-- ══ Portada Hero ══ -->
<section id="hero"><div class="wrap">
  <div class="heroGrid">
    <div>
      <div class="kicker" id="heroKicker">Herramienta Interactiva de Difusión Climática y Auditoría Técnica EPW · IBPSA Perú</div>
      <h1 id="heroTit">Lima tendrá <em>__LIMA_T45__ °C</em> de media en 2050</h1>
      <p class="subtit" id="heroSubtit">Eso bajo el escenario central SSP2-4.5 (Trayectoria Socioeconómica Compartida Intermedia). Bajo el de estrés SSP5-8.5 (Muy Altas Emisiones),
      __LIMA_T85__ °C. Ocho macroclimas peruanos, cuatro horizontes y una herramienta interactiva para acercar las proyecciones climáticas a la toma de decisiones y a la arquitectura bioclimática.</p>
      
      <div class="ciudCtrl" id="heroCiudades" role="group" aria-label="Ciudad seleccionada">
        <span class="lbl" data-i18n="lbl_ciudad">Ciudad:</span>
        __CIUD_BTNS_HERO__
      </div>

      <div class="grande" id="grande"></div>
    </div>
    <div class="solCol">
      <div id="heroViz"></div>
      <div class="solCtrl">
        <button class="solBtn on" onclick="solIr(0)" data-i18n="btn_hoy">Hoy</button>
        <button class="solBtn" onclick="solIr(1)">2030</button>
        <button class="solBtn" onclick="solIr(2)">2050</button>
        <button class="solBtn" onclick="solIr(3)">2080</button>
        <button class="solPlay" id="solPlay" onclick="solSeguir()" data-i18n="btn_animar">▶ Animar</button>
      </div>
      <p class="solPie" id="solPie">Cada rayo es un mes en una <b>escala fija calibrada de -6 a 36 °C</b> (anillos en 0°, 10°, 20° y 30°). Toca una ciudad para comparar su longitud y posición en el dial.</p>
    </div>
  </div>
  <div class="baja" onclick="document.getElementById('ipcc').scrollIntoView({behavior:'smooth'})">__ICO_ABAJO__<span data-i18n="btn_los_numeros">Los números</span></div>
</div></section>

<!-- ══ Marco Global IPCC y CMIP6 ══ -->
<section id="ipcc"><div class="wrap">
  <div class="cap"><span class="num" data-i18n="ipcc_num">Marco Global IPCC & CMIP6</span><span class="via"></span></div>
  <h2 data-i18n="ipcc_tit">Escenarios mundiales de temperatura y modelos climáticos</h2>
  <p class="lead" id="ipccLead">Las proyecciones se fundamentan en el <b>IPCC (Sexto Informe AR6)</b> y el ensamble multimodelo <b>CMIP6 (23 modelos globales)</b>. 
  Explora cómo se distribuye el calentamiento en el mapa mundial según el escenario socioeconómico (SSP) y el horizonte temporal:</p>

  <div class="ipccCtrl">
    <div class="seg" id="ipccEscen" role="group" aria-label="Escenarios de emisiones IPCC">
      <button class="on" data-esc="ssp126" onclick="setIpccEsc('ssp126')" data-i18n="ssp126_btn">SSP1-2.6 · Sostenibilidad (París)</button>
      <button data-esc="ssp245" onclick="setIpccEsc('ssp245')" data-i18n="ssp245_btn">SSP2-4.5 · Trayectoria Central</button>
      <button data-esc="ssp370" onclick="setIpccEsc('ssp370')" data-i18n="ssp370_btn">SSP3-7.0 · Rivalidad Regional</button>
      <button data-esc="ssp585" onclick="setIpccEsc('ssp585')" data-i18n="ssp585_btn">SSP5-8.5 · Caso de Estrés (Fósil)</button>
    </div>
    <div class="seg" id="ipccHz" role="group" aria-label="Horizonte temporal IPCC">
      <button class="on" id="ipccH2050" onclick="setIpccHz(2050)" data-i18n="hz2050_btn">Año 2050</button>
      <button id="ipccH2080" onclick="setIpccHz(2080)" data-i18n="hz2080_btn">Año 2080</button>
    </div>
  </div>

  <div class="panel ipccPanel">
    <div class="ipccMapHeader">
      <div>
        <h3 id="ipccMapTit">Calentamiento Global Proyectado: SSP1-2.6 (Año 2050)</h3>
        <p id="ipccMapSubtit">Anomalía de temperatura superficial (°C) respecto a la era preindustrial (1850-1900).</p>
      </div>
      <div class="ipccGlobalBadge">
        <span class="lbl" data-i18n="lbl_media_global">Media Global:</span>
        <b id="ipccGlobalVal">+1.5 °C</b>
      </div>
    </div>

    <div id="ipccWorldMap"></div>
    <div id="ipccPinDetail" class="ipccPinBox">💡 Haz clic o pasa el cursor sobre los puntos destacados del mapa (Costa de Perú, Amazonía, Andes, Océano) para explorar los fenómenos climáticos regionales.</div>

    <div class="ipccBarraWrap">
      <span class="lbl" data-i18n="lbl_anomalia_proy">Anomalía térmica proyectada (°C):</span>
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

<!-- ══ Escala de Impacto Térmico ══ -->
<section id="impacto"><div class="wrap">
  <div class="cap"><span class="num" data-i18n="impacto_num">Escala de Impacto Térmico</span><span class="via"></span></div>
  <h2 data-i18n="impacto_tit">¿Qué significan realmente +1 °C, +2 °C o +3 °C en el cuerpo, el edificio y el entorno?</h2>
  <p class="lead" id="impactoLead">Un aumento en la <b>media anual</b> desplaza la curva climática entera, multiplicando de forma no lineal las olas de calor, el estrés fisiológico, el consumo energético en edificios y el deshielo andino. Selecciona un nivel de calentamiento para ver sus consecuencias directas:</p>

  <div class="impCtrl" id="impCtrl" role="group" aria-label="Nivel de Calentamiento Térmico">
    <button class="impBtn n1" data-imp="s10" onclick="setImpactoNivel('s10')"><span class="impBtnBadge">+1.0 °C</span> <span data-i18n="imp_s10_btn">Actual (Perú Hoy)</span></button>
    <button class="impBtn n2" data-imp="s15" onclick="setImpactoNivel('s15')"><span class="impBtnBadge">+1.5 °C</span> <span data-i18n="imp_s15_btn">Meta París (SSP1-2.6)</span></button>
    <button class="impBtn n3 on" data-imp="s20" onclick="setImpactoNivel('s20')"><span class="impBtnBadge">+2.0 °C</span> <span data-i18n="imp_s20_btn">Umbral Crítico (SSP2-4.5 · 2050)</span></button>
    <button class="impBtn n4" data-imp="s30" onclick="setImpactoNivel('s30')"><span class="impBtnBadge">+3.0 °C+</span> <span data-i18n="imp_s30_btn">Estrés Severo (SSP5-8.5 · 2080)</span></button>
  </div>

  <div id="impHeaderBox" class="impHeaderBox"></div>
  <div id="impGrid3" class="impGrid3"></div>
</div></section>

<!-- ══ 01 · El Dato ══ -->
<section id="dato"><div class="wrap">
  <div class="cap"><span class="num" data-i18n="dato_num">01 · El dato</span><span class="via"></span></div>
  <h2 data-i18n="dato_tit">Elige un horizonte y mira el país entero</h2>
  <p class="lead" id="datoLead">Temperatura media anual de cada ciudad. Cambia de horizonte y las cifras
  y el mapa <b>transicionan</b> al nuevo valor. Toca una ciudad para ver su ficha completa:
  percentil 99, máxima del año, humedad y carga de enfriamiento.</p>
  <div class="horiz" role="group" aria-label="Horizonte temporal">
    <button data-h="hoy" onclick="setH('hoy')"><span data-i18n="h_hoy">Hoy</span><small data-i18n="h_hoy_sub">Línea base TMYx 2011-2025</small></button>
    <button data-h="a2030" onclick="setH('a2030')">2030<small data-i18n="h_2030_sub">Interpolado</small></button>
    <button class="on" data-h="a2050" onclick="setH('a2050')">2050<small data-i18n="h_2050_sub">Modelado CMIP6</small></button>
    <button data-h="a2080" onclick="setH('a2080')">2080<small data-i18n="h_2080_sub">Modelado CMIP6</small></button>
  </div>
  <div class="ctrl">
    <div class="seg" id="segE" role="group" aria-label="Escenario de emisiones">
      <button class="on" data-e="s245" onclick="setE('s245')" data-i18n="esc_s245_btn">SSP2-4.5 · Escenario Central (Shared Socioeconomic Pathway)</button>
      <button data-e="s585" onclick="setE('s585')" data-i18n="esc_s585_btn">SSP5-8.5 · Escenario de Estrés (Shared Socioeconomic Pathway)</button>
    </div>
    <span class="nota" id="escNota">Los escenarios SSP 8.5 representan casos de estrés severo para dimensionar el peor caso ante cambio climático, no pronósticos deterministas.</span>
  </div>
  <div class="rej" id="rej"></div>
  <div class="aviso"><h4 data-i18n="aviso_2030_t">2030 es interpolación, no modelo</h4>
    <p data-i18n="aviso_2030_b">El generador FWG (Future Weather Generator / ADAI / Univ. Coímbra) solo emite los horizontes 2050 y 2080 basados en modelos globales CMIP6 (Coupled Model Intercomparison Project Phase 6). La columna de 2030 interpola
    linealmente entre la línea base TMYx (Año Meteorológico Típico Extendido) y 2050. Como la aceleración del calentamiento no es estrictamente lineal en el tiempo,
    ese valor probablemente <b>se queda corto</b> respecto a la trayectoria real. Está marcado como tal en toda la página.</p></div>
</div></section>

<!-- ══ 02 · Por Ciudad ══ -->
<section id="ciudades"><div class="wrap">
  <div class="cap"><span class="num" data-i18n="ciudades_num">02 · Por ciudad</span><span class="via"></span></div>
  <h2 data-i18n="ciudades_tit">Cómo se siente: máximas y mínimas, mes a mes</h2>
  <p class="lead" id="ciudadesLead">Una media anual no se percibe. Lo que se nota es la máxima de febrero y la
  mínima de agosto. <b>Enciende y apaga horizontes</b> en la leyenda; con doble clic aíslas
  uno solo y aparecen las cifras de cada mes.</p>
  <div class="panel" style="margin-bottom:16px">
    <div style="font-size:13px;font-weight:700;letter-spacing:.3px;margin-bottom:8px" id="climoTit">Mes a mes</div>
    <div class="cgLeg" id="cgLeg" role="group" aria-label="Horizontes visibles"></div>
    <div id="climo"></div>
    <div class="cgInfo" id="cgInfo"></div></div>
  <p class="lead" id="ciudadesLead2">Ocho estaciones meteorológicas de superficie (METAR / WMO), de los 32 m de Trujillo a los 3 826 m de Juliaca.
  <b>El calentamiento escala con la altura</b>: la sierra sube más que la costa, aunque su
  consecuencia energética sea menor.</p>
  <div class="split">
    <div class="panel"><div id="mapa"></div></div>
    <div class="panel ficha" id="ficha"></div>
  </div>
  <div class="panel" style="margin-top:16px">
    <div style="font-size:13px;font-weight:700;letter-spacing:.3px;margin-bottom:6px" id="trayTit">Trayectoria</div>
    <div class="cgLeg" id="trLeg" role="group" aria-label="Horizontes visibles"></div>
    <div id="tray"></div></div>
  <div class="panel" style="margin-top:16px">
    <div class="brCab"><span id="barrasSubtit">Las ocho ciudades · clic en cualquier barra para fijar esa ciudad y ese horizonte</span>
      <span class="brOrd"><span data-i18n="lbl_ordenar">ordenar por</span> <span class="seg" id="brSort"></span></span></div>
    <div id="barras"></div></div>
</div></section>

<!-- ══ 03 · Qué Implica ══ -->
<section id="carga"><div class="wrap">
  <div class="cap"><span class="num" data-i18n="carga_num">03 · Qué implica</span><span class="via"></span></div>
  <h2 data-i18n="carga_tit">Comportamiento psicrométrico hora a hora</h2>
  <p class="lead" id="nbLead">Cada punto es una hora del año para la ciudad seleccionada, situada por su temperatura y su humedad
  absoluta. Al proyectar a horizontes futuros, la nube se desplaza <b>en diagonal</b>: el aire más cálido
  retiene mayor cantidad de vapor. Eso es Clausius-Clapeyron, visualizado hora a hora.</p>
  
  <div class="ciudCtrl" id="nbCiudades" role="group" aria-label="Seleccionar ciudad para psicrometría">
    <span class="lbl" data-i18n="lbl_ciudad">Ciudad:</span>
    __CIUD_BTNS_NUBE__
  </div>

  <div class="ctrl">
    <button class="btn" id="btnN" onclick="reproducir()">__ICO_PLAY__<span data-i18n="btn_recorrer"> Recorrer hasta 2080</span></button>
    <div class="pasos" id="nbPasos" role="group" aria-label="Horizonte de la nube">
      <button class="pasoN on" onclick="irNube(0)" data-i18n="btn_hoy">Hoy</button>
      <button class="pasoN" onclick="irNube(1)">2030</button>
      <button class="pasoN" onclick="irNube(2)">2050</button>
      <button class="pasoN" onclick="irNube(3)">2080</button>
    </div>
    <div class="seg" id="nbModo" role="group" aria-label="Qué codifica el color">
      <button class="on" data-m="mes" onclick="nbSetCol('mes')" data-i18n="btn_color_mes">Color: mes</button>
      <button data-m="hora" onclick="nbSetCol('hora')" data-i18n="btn_color_hora">Color: hora del día</button>
    </div>
    <span class="nota" id="estado">Hoy · TMYx 2011-2025</span>
  </div>
  <div class="panel"><div id="nube"></div>
    <div class="nbLeg" id="nbLeg" role="group" aria-label="Filtrar por mes u hora"></div>
    <div class="nbPunto" id="nbPunto"><b>Cada punto es una hora del año</b> — una de cada seis, 1 460 en
    total. Su posición horizontal es la temperatura del aire y la vertical, cuánto vapor
    lleva. El color indica el mes (o la hora del día, si cambias el modo): clic en la leyenda
    para aislar uno. Los meses de verano se agrupan arriba a la derecha —calor con humedad— y
    los de invierno abajo a la izquierda.</div></div>
  <div class="aviso"><h4 data-i18n="aviso_multiplo_t">El múltiplo térmico engaña sin su valor absoluto</h4>
    <p data-i18n="aviso_multiplo_b">En Trujillo la carga de enfriamiento se multiplica por 4.8 y en Piura solo por 1.4.
    Pero Trujillo sube 706 °C·h y Piura 6 479 °C·h. El múltiplo grande está sobre la base pequeña.</p></div>
</div></section>

<!-- ══ 04 · Cómo: Stepper de Seis Pasos Rediseñado ══ -->
<section id="metodo"><div class="wrap">
  <div class="cap"><span class="num" data-i18n="metodo_num">04 · Cómo</span><span class="via"></span></div>
  <h2 data-i18n="metodo_tit">Seis pasos del proceso de auditoría meteorológica</h2>
  <p class="lead" id="metodoLead">De un archivo meteorológico descargado a una proyección al 2080. Estos son los seis pasos de la metodología, con sus métricas auditadas, variables comprobadas y hallazgos reales:</p>
  
  <div class="stepperContainer">
    <div class="stepperNav" id="stepPills"></div>
    <div class="stepHeroCard" id="stepHeroCard"></div>
  </div>

  <div class="glosarioGrid">
    <div class="glosCard">
      <h4 data-i18n="glos_morphing_t">¿Qué es «Morphing»?</h4>
      <p data-i18n="glos_morphing_p1"><b>Ajuste horario:</b> Toma las 8 760 horas medidas en la estación base y les aplica las anomalías climáticas mensuales proyectadas por los modelos globales.</p>
      <p data-i18n="glos_morphing_p2"><b>Por qué importa:</b> Conserva la física del sitio, la oscilación día-noche y los vientos reales, adaptándolos a las temperaturas de 2050 y 2080.</p>
    </div>
    <div class="glosCard">
      <h4 data-i18n="glos_ensemble_t">¿Qué es un «Ensemble»?</h4>
      <p data-i18n="glos_ensemble_p1"><b>Consenso multimodelo:</b> Combina y promedia las proyecciones de 23 modelos climáticos globales independientes (NOAA, NASA, Max Planck).</p>
      <p data-i18n="glos_ensemble_p2"><b>Por qué importa:</b> Ningún modelo individual es infalible; promediar el conjunto cancela sesgos y entrega una señal climática de consenso mucho más sólida.</p>
    </div>
  </div>

  <div class="aviso" style="margin-top:24px"><h4 data-i18n="aviso_cc_t">Verificación física de Clausius-Clapeyron (Paso 6)</h4>
    <p data-i18n="aviso_cc_b">Al calentarse el aire a humedad relativa constante, la humedad absoluta debe subir ~6.2 % por cada °C (+6.2 %/K). Los archivos transformados con FWG arrojan entre <b>7.60 y 7.79 %/K</b> (apenas 1.5 pp de desviación frente a la teoría, muy por debajo del umbral de sospecha de 4.0 pp). Esto confirma que el morphing preservó la consistencia termodinámica.</p></div>
</div></section>

<!-- ══ 05 · ¿Es Fiable? ══ -->
<section id="fiable"><div class="wrap">
  <div class="cap"><span class="num" data-i18n="fiable_num">05 · ¿Es fiable?</span><span class="via"></span></div>
  <h2 data-i18n="fiable_tit">Ahora sí: cuánto puedes creerte esas cifras</h2>
  <p class="lead" id="fiableLead">Los números de arriba salen de archivos climáticos que no habían sido auditados en conjunto. Esto es
  lo que se encontró al examinarlos en detalle, pregunta por pregunta. <b>Se verificó coherencia interna, integridad horaria y plausibilidad física</b>.</p>

  <details class="pleg" id="pleg_bulbo_seco">
    <summary><span class="mas"></span><span class="plegTit">¿Sirve la temperatura de bulbo seco?</span><span class="veredicto si">Sí</span></summary>
    <div class="cuerpo">
      <p>Los 40 archivos EPW (EnergyPlus Weather) traen sus 8 760 horas anuales completas, sin huecos ni vacíos, con temperaturas medias anuales entre 9.5 y 26.1 °C consistentes con la climatología de cada región. La humedad absoluta acompaña a la temperatura siguiendo la ecuación física de Clausius-Clapeyron con una discrepancia de apenas 1.5 puntos porcentuales frente a la teoría, muy por debajo del límite de sospecha de 4 pp.</p>
      <p>Para comparar tipologías constructivas, predimensionar sistemas térmicos o evaluar estrategias pasivas, los archivos son plenamente aptos.</p>
    </div>
  </details>

  <details class="pleg" id="pleg_solar">
    <summary><span class="mas"></span><span class="plegTit">¿Sirve la irradiancia solar?</span><span class="veredicto no">No</span></summary>
    <div class="cuerpo">
      <p>Lima reporta 2 177 kWh/m² anuales de radiación global horizontal, <b>más que Cusco</b> con 1 991 kWh/m² — a pesar de que Cusco se sitúa 3 276 m más arriba y Lima posee nubosidad costera persistente. El dato en los archivos EPW (EnergyPlus Weather) procede de reanálisis satelital (ERA5) y la estación del Aeropuerto Internacional Jorge Chávez es de tipo METAR (Meteorological Aerodrome Report): registra visibilidad y nubosidad para aeronavegación, pero no mide radiación solar directa con piranómetros.</p>
      <p>Para dimensionamiento fotovoltaico o ganancias solares críticas, es necesario contrastar estos valores con piranometría de superficie antes de su uso.</p>
    </div>
  </details>

  <details class="pleg" id="pleg_sanos">
    <summary><span class="mas"></span><span class="plegTit">¿Están todos los archivos EPW sanos?</span><span class="veredicto no">Tres no</span></summary>
    <div class="cuerpo">
      <p>La ventana histórica 2004-2018 de Cusco, Arequipa y Juliaca se aparta significativamente de sus otras 4 ventanas temporales: desviaciones de +2.96 °C, +1.20 °C y −1.62 °C frente a la mediana de su ciudad. <b>Ninguna estación costera presenta esta distorsión.</b> Juliaca 2004-2018 además presenta una autocorrelación horaria de solo 0.377 frente a 0.845 en sus otras cuatro ventanas: no es un simple desplazamiento de nivel térmico, sino una alteración en la estructura temporal de la serie.</p>
      <p>Este patrón restringido a gran altitud apunta a discontinuidades en la cobertura de registros METAR (Meteorological Aerodrome Report) en los Andes durante ese periodo. Se recomienda no emplear esas tres ventanas específicas.</p>
      <div class="panel" style="margin-top:18px"><div id="vint"></div></div>
    </div>
  </details>

  <details class="pleg" id="pleg_linea_base">
    <summary><span class="mas"></span><span class="plegTit">¿Da igual qué archivo TMYx de línea base se elija?</span><span class="veredicto no">No</span></summary>
    <div class="cuerpo">
      <p>Entre el TMYx (Año Meteorológico Típico Extendido) de periodo completo (1991-2020) y la ventana reciente (2011-2025) hay __DESFASE_BASES__ °C de diferencia en Lima, y entre ventanas de una misma ciudad el rango llega a 3.64 °C.</p>
      <p>Esta discrepancia <b>no es un sesgo lineal constante que se pueda restar</b>: la pendiente frente al año centroide es de +0.18 °C por década con un coeficiente r² de solo 0.13 (el año centroide explica únicamente el 13 % de la variación). El sesgo temporal (vintage) introduce dispersión e incertidumbre que no puede neutralizarse con un factor multiplicador simple.</p>
    </div>
  </details>

  <details class="pleg" id="pleg_convergencia">
    <summary><span class="mas"></span><span class="plegTit">¿Coinciden los métodos climáticos entre sí?</span><span class="veredicto mas_menos">Más o menos</span></summary>
    <div class="cuerpo">
      <p>Para Lima 2050, Meteonorm (síntesis estocástica basada en modelos CMIP5 / escenario RCP8.5) reporta __T_2050_METEONORM__ °C y FWG (Future Weather Generator v4.2.0 / morphing sobre modelos CMIP6 / escenario SSP5-8.5) proyecta __T_2050_FWG__ °C: <b>__DIVERGENCIA__ °C de discrepancia metodológica</b> sobre una señal total de calentamiento de ~2 °C. Al ser metodologías independientes, la diferencia es relevante.</p>
      <p>Debe considerarse que RCP8.5 (CMIP5) y SSP5-8.5 (CMIP6) no representan exactamente el mismo forzamiento. Adicionalmente, el archivo EPW nativo de Meteonorm no estuvo disponible para auditoría directa: sus valores proceden de la documentación del proyecto.</p>
      <div class="panel" style="margin-top:18px"><div id="conv"></div></div>
    </div>
  </details>

  <details class="pleg" id="pleg_nino">
    <summary><span class="mas"></span><span class="plegTit">¿Capturan el fenómeno de El Niño?</span><span class="veredicto no">No</span></summary>
    <div class="cuerpo">
      <p>Ninguno. Los archivos TMY / TMYx (Typical Meteorological Year / Año Meteorológico Típico) seleccionan meses típicos representativos y <b>eliminan por diseño los años y meses anómalos</b>. En la costa peruana, los eventos de El Niño (ENSO - El Niño-Oscilación del Sur) representan el evento crítico que genera los picos de sobrecarga térmica y de humedad en edificaciones.</p>
      <p>Si se dimensiona exclusivamente con el archivo TMYx de Piura o Lima, la instalación no estará dimensionada para resistir un evento de El Niño.</p>
    </div>
  </details>

  <div class="aviso rojo"><h4 data-i18n="aviso_frase_t">En una frase</h4>
    <p data-i18n="aviso_frase_b">Son suficientemente robustos para comparar tipologías constructivas y predimensionar; no constituyen valores deterministas para promesas contractuales ni certificación formal. Debe tratarse el valor de «__LIMA_T45__ °C» de Lima en 2050 como «alrededor de 21 °C», con una banda de incertidumbre de aproximadamente ±1 °C.</p></div>
</div></section>

<!-- ══ 06 · Conclusiones y Alcance ══ -->
<section id="limites"><div class="wrap">
  <div class="cap"><span class="num" data-i18n="limites_num">06 · Conclusiones y Alcance</span><span class="via"></span></div>
  <h2 data-i18n="limites_tit">Qué resuelve esta auditoría y qué precauciones exige</h2>
  <p class="lead" id="limitesLead">Declarar con precisión el alcance operativo y las fronteras técnicas del estudio garantiza un uso riguroso y responsable de los archivos climáticos en arquitectura y simulación energética:</p>
  
  <div class="conclusionesGrid">
    <div class="concCard aportes">
      <div class="concHeader">
        <h3 data-i18n="conc_aportes_t">06.1 · Capacidades y Aportes</h3>
        <span class="concBadge si" data-i18n="conc_aportes_badge">Sí permite hacer</span>
      </div>
      <div class="concLista">
        <div class="concItem">
          <span class="concNum">01</span>
          <div class="concBody">
            <strong data-i18n="ap1_t">Simulación energética y pasiva horaria (8 760 h)</strong>
            <p data-i18n="ap1_d">Permite modelar en EnergyPlus, DesignBuilder o Ladybug el comportamiento térmico pasivo, horas de sobrecalentamiento y confort adaptativo año completo en 8 macroclimas peruanos.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">02</span>
          <div class="concBody">
            <strong data-i18n="ap2_t">Condiciones de diseño ASHRAE calculadas (99.6 % y 0.4 %)</strong>
            <p data-i18n="ap2_d">Proporciona los percentiles de temperatura extrema necesarios para dimensionar la potencia de equipos de climatización hacia 2050 y 2080, incluso para ciudades que carecían de cabecera como Juliaca.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">03</span>
          <div class="concBody">
            <strong data-i18n="ap3_t">Cuantificación de incertidumbre intermodelo (IPCC P10–P90)</strong>
            <p data-i18n="ap3_d">Integra las bandas de dispersión del ensemble CMIP6 (23 modelos globales), permitiendo aplicar factores de seguridad probabilísticos en decisiones de inversión y diseño.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">04</span>
          <div class="concBody">
            <strong data-i18n="ap4_t">Auditoría del efecto vintage en líneas base</strong>
            <p data-i18n="ap4_d">Identifica y cuantifica el desfase de líneas base históricas (Meteonorm 1999 vs TMYx 2018), demostrando que el 50 % de la discrepancia térmica proviene de la antigüedad del dato base y no del modelo.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">05</span>
          <div class="concBody">
            <strong data-i18n="ap5_t">Diagnóstico del colapso de ventilación natural nocturna</strong>
            <p data-i18n="ap5_d">Identifica con precisión los meses y horas en que las temperaturas mínimas superan los 20 °C (noches tropicales), advirtiendo el límite de la arquitectura pasiva convencional.</p>
          </div>
        </div>
      </div>
    </div>

    <div class="concCard limites">
      <div class="concHeader">
        <h3 data-i18n="conc_limites_t">06.2 · Fronteras y Advertencias</h3>
        <span class="concBadge no" data-i18n="conc_limites_badge">Precauciones y Límites</span>
      </div>
      <div class="concLista">
        <div class="concItem">
          <span class="concNum">01</span>
          <div class="concBody">
            <strong data-i18n="lim1_t">Eventos estocásticos de El Niño (ENSO)</strong>
            <p data-i18n="lim1_d">La metodología TMYx sintetiza años climáticos típicos y excluye por diseño matemático anomalías no cíclicas. En la costa norte y centro debe aplicarse un margen de seguridad de +2.5 a +3.5 °C.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">02</span>
          <div class="concBody">
            <strong data-i18n="lim2_t">Sesgos de resolución en la Corriente de Humboldt</strong>
            <p data-i18n="lim2_d">La malla de 100–250 km de los modelos globales GCM suaviza la surgencia costera fría del Pacífico peruano, requiriendo prudencia en microclimas de borde litoral.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">03</span>
          <div class="concBody">
            <strong data-i18n="lim3_t">Irradiancia solar directa de alta precisión</strong>
            <p data-i18n="lim3_d">Al provenir de reanálisis satelital ERA5, debe contrastarse con el Atlas Solar del SENAMHI / MINEM para proyectos de energía fotovoltaica o ganancias solares de gran escala.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">04</span>
          <div class="concBody">
            <strong data-i18n="lim4_t">Validez regulatoria formal para certificaciones</strong>
            <p data-i18n="lim4_d">Constituye una investigación y auditoría técnica independiente. No sustituye las tablas normativas del Reglamento Nacional de Edificaciones (RNE) ni datos obligatorios para sellos EDGE o LEED.</p>
          </div>
        </div>
        <div class="concItem">
          <span class="concNum">05</span>
          <div class="concBody">
            <strong data-i18n="lim5_t">Inercia y microclima urbano hiperlocal</strong>
            <p data-i18n="lim5_d">Las estaciones meteorológicas de aeropuerto no incorporan el calor antropogénico ni el cañón urbano denso; en distritos consolidados debe considerarse el efecto de Isla de Calor Urbano.</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="aviso" style="margin-top:24px">
    <h4 data-i18n="dictamen_t">Dictamen final de la auditoría técnica</h4>
    <p data-i18n="dictamen_d">Los archivos climáticos transformados bajo CMIP6 son <b>plenamente válidos y físicamente consistentes para predimensionamiento arquitectónico, simulación higrotérmica y análisis comparativo</b> en el Perú. Para proyectos de alta exigencia, es obligatorio incorporar reservas para El Niño y calibrar la radiación solar con piranómetros locales.</p>
  </div>
</div></section>

<!-- ══ Referencias Bibliográficas (Formato APA 7ma Edición) ══ -->
<section id="referencias"><div class="wrap">
  <div class="cap"><span class="num" data-i18n="referencias_num">Referencias Bibliográficas</span><span class="via"></span></div>
  <h2 data-i18n="referencias_tit">Fuentes consultadas y estándares normativos (Formato APA 7.ª Edición)</h2>
  <p class="lead" id="refLead">Toda la base climática, matemática y metodológica de esta auditoría se sustenta en las siguientes referencias científicas y normativas internacionales:</p>
  
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

<!-- ══ Pie de Página Institucional y Simple ══ -->
<footer class="siteFooter"><div class="wrap">
  <p id="footerMainText">
    © 2026 <strong>Abelardo Tomás Palacios Hurtado &amp; IBPSA Perú</strong> · Herramienta interactiva de difusión sobre cambio climático y auditoría técnica de archivos EPW para el Perú hacia 2030, 2050 y 2080.
  </p>
  <p class="footerSub" id="footerSubText">
    Investigación y datos abiertos bajo licencia <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a> · 
    <a href="https://github.com/IBPSA-Peru/Clima-Per-2080" target="_blank" rel="noopener">Repositorio en GitHub</a> · 
    <a href="https://ibpsa-peru.github.io/Clima-Per-2080/" target="_blank" rel="noopener">ibpsa-peru.github.io/Clima-Per-2080</a>
  </p>
</div></footer>

<script>
const D=__PAYLOAD_JSON__;
__JS_BASE__
__JS_EXTRA__
</script></body></html>
"""


def html(d: dict) -> str:
    css_base = (TPL / "plantilla.css").read_text(encoding="utf-8")
    js_base = (TPL / "plantilla.js").read_text(encoding="utf-8")
    c = d["conv"]
    ciudades_lista = [x["n"] for x in d["ciudades"]]
    lima = next(x for x in d["ciudades"] if x["n"] == "Lima")
    L45, L85 = lima["s245"]["H"], lima["s585"]["H"]

    migas = "".join(f'<a href="#{i}" data-i18n="nav_{i}">{t_es}</a>' for i, t_es in CAPS)
    ciud_btns_hero = "".join(
        f'<button class="ciudBtn {("on" if cn=="Lima" else "")}" onclick="pick(\'{cn}\')">{cn}</button>'
        for cn in ciudades_lista
    )
    ciud_btns_nube = "".join(
        f'<button class="ciudBtn {("on" if cn=="Lima" else "")}" onclick="pick(\'{cn}\')">{cn}</button>'
        for cn in ciudades_lista
    )

    logo_b64_file = RAIZ / "Data" / "web" / "ibpsa_logo_b64.txt"
    logo_b64 = logo_b64_file.read_text(encoding="ascii").strip() if logo_b64_file.exists() else ""

    payload_json = json.dumps(d, ensure_ascii=False, separators=(',', ':'))

    res = HTML_TEMPLATE
    res = res.replace("__CSS__", css_base + "\n" + CSS_EXTRA)
    res = res.replace("__LOGO_B64__", logo_b64)
    res = res.replace("__MIGAS__", migas)
    res = res.replace("__CIUD_BTNS_HERO__", ciud_btns_hero)
    res = res.replace("__CIUD_BTNS_NUBE__", ciud_btns_nube)
    res = res.replace("__LIMA_T45__", f"{L45['a2050']['T']:.1f}")
    res = res.replace("__LIMA_T85__", f"{L85['a2050']['T']:.1f}")
    res = res.replace("__DESFASE_BASES__", f"{c['desfase_entre_bases_C']:+.2f}")
    res = res.replace("__T_2050_METEONORM__", f"{c['T_2050_meteonorm_rcp85_C']:.2f}")
    res = res.replace("__T_2050_FWG__", f"{c['T_2050_fwg_ssp585_C']:.2f}")
    res = res.replace("__DIVERGENCIA__", f"{c['divergencia_absoluta_C']:+.2f}")
    res = res.replace("__PAYLOAD_JSON__", payload_json)
    res = res.replace("__JS_BASE__", js_base)
    res = res.replace("__JS_EXTRA__", JS_EXTRA)

    for k, v in ICO.items():
        res = res.replace(f"__ICO_{k.upper()}__", v)

    return res


def construir() -> Path:
    d = json.loads((RAIZ / "Data" / "web" / "payload_v3.json").read_text(encoding="utf-8"))

    WEB.mkdir(parents=True, exist_ok=True)
    salida = WEB / "index.html"
    
    contenido = html(d)
    salida.write_text(contenido, encoding="utf-8")
    print(f"  [OK] Generado visor optimizado para GitHub Pages: {salida} ({salida.stat().st_size/1024:.0f} KB)")
    return salida


if __name__ == "__main__":
    construir()
