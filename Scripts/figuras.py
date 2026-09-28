#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
figuras.py — Paso 6. Las ocho figuras de la auditoria.

Escribe PNG individuales a Temp/renders/ y una hoja de contacto
Temp/renders/00_hoja_contacto.png para revisarlas de un vistazo.

SOP-02 I2: ninguna figura se da por buena sin mirarla.
Las que pasan compuerta se copian a "Final Results/figuras/".

Uso: python Scripts/figuras.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
REND = RAIZ / "Temp" / "renders"
REND.mkdir(parents=True, exist_ok=True)

MESES = ["ene", "feb", "mar", "abr", "may", "jun",
         "jul", "ago", "sep", "oct", "nov", "dic"]
MESES_ET = ["E", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]

ZONA = {
    "Lima": "costa desertica", "Trujillo": "costa norte", "Piura": "costa norte",
    "Tacna": "costa sur arida", "Arequipa": "altiplano arido",
    "Cusco": "altura", "Juliaca": "altiplano frio", "Iquitos": "selva humeda",
}
COLOR = {
    "Iquitos": "#1b7837", "Piura": "#d95f02", "Trujillo": "#e7a03c",
    "Lima": "#0570b0", "Tacna": "#7570b3", "Arequipa": "#a6611a",
    "Cusco": "#984ea3", "Juliaca": "#4d4d4d",
}
plt.rcParams.update({"figure.dpi": 110, "font.size": 9,
                     "axes.grid": True, "grid.alpha": 0.25})


def cargar():
    t = pd.read_csv(RAIZ / "Data" / "metricas_todas_v1.csv")
    t["ventana"] = t["archivo"].str.extract(r"TMYx\.?(\d{4}-\d{4})?")[0].fillna("completo")
    e = pd.read_csv(RAIZ / "Data" / "metricas_escenarios_v1.csv")
    e = e[~e["archivo"].str.contains("BASE_TMYx", na=False)].copy()
    e["escenario"] = e["archivo"].str.extract(r"_(BASE|ssp\d{3})_")[0]
    r = json.loads((RAIZ / "Data" / "analisis_cuatro_v1.json").read_text(encoding="utf-8"))
    return t, e, r


def guardar(fig, nombre):
    ruta = REND / nombre
    fig.savefig(ruta, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  {nombre}")
    return ruta


# 1 ── elevacion vs temperatura media
def fig1(t):
    d = t[t.ventana == "2011-2025"]
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    # Lima, Trujillo y Piura estan las tres entre 32 y 35 m: rotularlas dentro del
    # grafico es imposible por mucho que se desplace el texto. Se sustituye el
    # rotulado inline por una LEYENDA, que es lo que el caso pedia (ver D-13).
    for _, r in d.sort_values("elevacion_m").iterrows():
        ax.scatter(r.elevacion_m, r.dbt_media, s=95, color=COLOR.get(r.ciudad, "k"),
                   edgecolor="k", linewidth=0.6, zorder=3,
                   label=f"{r.ciudad} · {r.elevacion_m:.0f} m · {ZONA.get(r.ciudad,'')}")
    x = d.elevacion_m.to_numpy(float); y = d.dbt_media.to_numpy(float)
    m, c = np.polyfit(x, y, 1)
    xs = np.linspace(0, 4100, 50)
    ax.plot(xs, m * xs + c, "--", color="gray", linewidth=1, zorder=1,
            label=f"gradiente: {m*1000:+.2f} C por 1000 m (r={np.corrcoef(x,y)[0,1]:.2f})")
    ax.set_xlabel("Elevacion de la estacion (m sobre el nivel del mar)")
    ax.set_ylabel("Temperatura de bulbo seco media anual (C)")
    ax.set_title("1 · Las ocho ciudades: elevacion vs temperatura media\n"
                 "TMYx ventana 2011-2025", fontsize=10)
    ax.set_xlim(-250, 4300)
    ax.set_ylim(6.5, 28.0)
    ax.legend(fontsize=7.5, loc="upper right", framealpha=0.95)
    return guardar(fig, "fig1_elevacion_vs_temperatura.png")


# 2 ── perfiles mensuales
def fig2(t):
    d = t[t.ventana == "2011-2025"].sort_values("elevacion_m", ascending=False)
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    for _, r in d.iterrows():
        y = [r[f"dbt_media_{m}"] for m in MESES]
        ax.plot(range(12), y, marker="o", ms=3.5, linewidth=1.6,
                color=COLOR.get(r.ciudad, "k"),
                label=f"{r.ciudad} ({r.elevacion_m:.0f} m)")
    ax.set_xticks(range(12)); ax.set_xticklabels(MESES_ET)
    ax.set_xlabel("Mes (hemisferio sur: verano en el centro-izquierda)")
    ax.set_ylabel("Temperatura de bulbo seco media mensual (C)")
    ax.set_title("2 · Perfiles mensuales de temperatura, TMYx 2011-2025", fontsize=10)
    ax.legend(fontsize=7.5, ncol=2, loc="lower center")
    ax.set_ylim(bottom=min(0, ax.get_ylim()[0]))
    return guardar(fig, "fig2_perfiles_mensuales.png")


# 3 ── dT por ciudad y escenario
def fig3(res):
    b = pd.DataFrame(res["B_deltas_por_zona"]["tabla"]).sort_values("elevacion_m")
    ciudades = b.ciudad.unique()
    x = np.arange(len(ciudades)); w = 0.38
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    for i, (esc, col, et) in enumerate([
            ("ssp245", "#4292c6", "SSP2-4.5 (escenario central)"),
            ("ssp585", "#cb181d", "SSP5-8.5 (caso de estres, NO pronostico)")]):
        v = [b[(b.ciudad == c) & (b.escenario == esc)].dT_C.iloc[0] for c in ciudades]
        bars = ax.bar(x + (i - 0.5) * w, v, w, color=col, label=et, edgecolor="k", linewidth=0.4)
        ax.bar_label(bars, fmt="%+.2f", fontsize=7, padding=1)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{c}\n{b[b.ciudad==c].elevacion_m.iloc[0]:.0f} m"
                        for c in ciudades], fontsize=8)
    ax.set_ylabel("Cambio de temperatura media anual a 2050 (C)")
    ax.set_title("3 · Delta-T por ciudad y escenario\n"
                 "base: TMYx 2011-2025 · ordenado por elevacion", fontsize=10)
    ax.legend(fontsize=8); ax.set_ylim(0, 2.85)
    return guardar(fig, "fig3_dT_por_ciudad_escenario.png")


# 4 ── grados-hora de enfriamiento presente vs 2050
def fig4(res):
    b = pd.DataFrame(res["B_deltas_por_zona"]["tabla"])
    b = b[b.escenario == "ssp245"].sort_values("GH24_base_Ch", ascending=False)
    x = np.arange(len(b)); w = 0.38
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    b1 = ax.bar(x - w/2, b.GH24_base_Ch, w, color="#bdbdbd",
                label="hoy (TMYx 2011-2025)", edgecolor="k", linewidth=0.4)
    b2 = ax.bar(x + w/2, b.GH24_fut_Ch, w, color="#cb181d",
                label="2050 SSP2-4.5", edgecolor="k", linewidth=0.4)
    ax.bar_label(b1, fmt="%.0f", fontsize=6.5, padding=1)
    ax.bar_label(b2, fmt="%.0f", fontsize=6.5, padding=1)
    ax.set_xticks(x); ax.set_xticklabels(b.ciudad, fontsize=8)
    ax.set_ylabel("Grados-hora de enfriamiento, base 24 C (C-h por ano)")
    ax.set_title("4 · Carga de enfriamiento: hoy vs 2050\n"
                 "escala logaritmica — el rango cubre cinco ordenes de magnitud",
                 fontsize=10, pad=34)
    ax.set_yscale("symlog", linthresh=1)
    # Aire arriba para que las etiquetas de las barras altas no toquen el titulo.
    ax.set_ylim(0, ax.get_ylim()[1] * 3.2)
    # Leyenda FUERA del area de ejes: dentro tapaba etiquetas de barras se pusiera
    # donde se pusiera (ver D-13).
    ax.legend(fontsize=8, ncol=2, loc="lower left", bbox_to_anchor=(0, 1.005, 1, 0.06),
              mode="expand", borderaxespad=0, frameon=False)
    return guardar(fig, "fig4_grados_hora_enfriamiento.png")


# 5 ── autocorrelacion y rachas
def fig5(t, e):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 4.2))
    d = t[t.ventana == "2011-2025"].sort_values("autocorr_lag1")
    a1.barh(d.ciudad, d.autocorr_lag1, color=[COLOR.get(c, "k") for c in d.ciudad],
            edgecolor="k", linewidth=0.4)
    for i, v in enumerate(d.autocorr_lag1):
        a1.text(v + 0.012, i, f"{v:.3f}", va="center", fontsize=7.5)
    a1.set_xlabel("Autocorrelacion de la media diaria, lag 1")
    a1.set_xlim(0, 1.15)
    a1.set_title("Persistencia dia a dia\n(TMYx 2011-2025)", fontsize=9.5)

    dd = pd.DataFrame(res_global["D_firma_sintesis"]["tabla"])
    dd = dd[dd.escenario == "ssp245"].sort_values("racha_max_base_d")
    y = np.arange(len(dd)); w = 0.38
    a2.barh(y - w/2, dd.racha_max_base_d, w, color="#bdbdbd",
            label="TMYx 2011-2025 (medido)", edgecolor="k", linewidth=0.4)
    a2.barh(y + w/2, dd.racha_max_fut_d, w, color="#cb181d",
            label="FWG SSP2-4.5 2050 (morfado)", edgecolor="k", linewidth=0.4)
    a2.set_yticks(y); a2.set_yticklabels(dd.ciudad, fontsize=8)
    a2.set_xlabel("Racha calida mas larga sobre el percentil 90 (dias)")
    a2.set_title("Episodios calidos multi-dia\nel morphing los preserva", fontsize=9.5)
    a2.legend(fontsize=7.5, loc="lower right")
    fig.suptitle("5 · Estructura temporal: persistencia y rachas calidas", fontsize=10.5)
    fig.tight_layout()
    return guardar(fig, "fig5_autocorrelacion_rachas.png")


# 6 ── dispersion bulbo seco vs humedad absoluta, Lima
def fig6(e):
    import sys
    sys.path.insert(0, str(RAIZ / "Scripts"))
    from analizar_epw import leer_datos, humedad_absoluta_gkg
    base = RAIZ / "Data" / "escenarios_v1" / "Lima" / "LIMA_BASE_2011-2025.epw"
    fut = RAIZ / "Data" / "escenarios_v1" / "Lima" / "LIMA_ssp585_2050.epw"
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    for ruta, col, et, z in [(base, "#4292c6", "TMYx 2011-2025 (hoy)", 2),
                             (fut, "#cb181d", "FWG SSP5-8.5 2050", 1)]:
        df = leer_datos(ruta)
        dbt = df.dbt.to_numpy(float)
        w = humedad_absoluta_gkg(dbt, df.rh.to_numpy(float), df.pres.to_numpy(float)/1000.0)
        ax.scatter(dbt, w, s=1.6, alpha=0.16, color=col, zorder=z, label=et)
    ax.set_xlabel("Temperatura de bulbo seco (C)")
    ax.set_ylabel("Humedad absoluta (g de vapor por kg de aire seco)")
    ax.set_title("6 · Lima: bulbo seco vs humedad absoluta, 8760 horas\n"
                 "hoy vs 2050 caso de estres", fontsize=10)
    lg = ax.legend(fontsize=8, loc="upper left", markerscale=6)
    for h in lg.legend_handles:
        h.set_alpha(1)
    return guardar(fig, "fig6_psicrometrica_lima.png")


# 7 ── vintage
def fig7(res):
    a = pd.DataFrame(res["A_vintage"]["tabla"])
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    for and_, mk, et in [(False, "o", "costa y selva"), (True, "^", "andinas")]:
        s = a[a.andina == and_]
        ax.scatter(s.d_centroide_anos, s.dT_aparente_C, marker=mk, s=55,
                   c=[COLOR.get(c, "k") for c in s.ciudad],
                   edgecolor="k", linewidth=0.5, label=et, zorder=3)
    # Los tres atipicos de D-08 se rotulan: son el hallazgo, no ruido a esconder.
    # Se rotulan SOLO los tres atipicos de D-08 (ventana 2004-2018 de las ciudades
    # andinas). Rotular todo lo que pasaba de 0.9 C metia etiquetas encabalgadas
    # que no aportaban nada.
    for _, r in a[(a.andina) & (a.ventana == "2004-2018")].iterrows():
        ax.annotate(f"{r.ciudad} 2004-2018", (r.d_centroide_anos, r.dT_aparente_C),
                    textcoords="offset points", xytext=(10, 4), fontsize=7.5,
                    color="#333333", ha="left")
    at = res["A_vintage"]["ajuste_sin_andinas_2004_2018"]
    xs = np.linspace(a.d_centroide_anos.min(), a.d_centroide_anos.max(), 40)
    ax.plot(xs, at["pendiente_C_por_ano"] * xs + at["intercepto_C"], "--", color="k",
            linewidth=1.2,
            label=f"ajuste sin atipicos: {at['calentamiento_por_decada_C']:+.2f} C/decada, "
                  f"r2={at['r2']:.2f}")
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_xlabel("Diferencia de ano centroide contra el TMYx de periodo completo (anos)")
    ax.set_ylabel("Delta-T aparente (C)")
    ax.set_title("7 · Vintage: el ano centroide explica poco del delta-T\n"
                 "cada punto es una ventana TMYx contra el periodo completo de su ciudad",
                 fontsize=10)
    # Ambas leyendas DENTRO del marco, en la zona vacia de la derecha: sacarlas
    # fuera con bbox_to_anchor las dejaba cortadas al guardar.
    from matplotlib.lines import Line2D
    manual = [Line2D([], [], marker="o", ls="", mfc=COLOR[c], mec="k", ms=6, label=c)
              for c in sorted(COLOR)]
    l1 = ax.legend(fontsize=7.5, loc="upper left", framealpha=0.95)
    ax.add_artist(l1)
    ax.legend(handles=manual, fontsize=7, loc="upper right", ncol=2,
              title="ciudad", title_fontsize=7.5, framealpha=0.95)
    ax.set_xlim(5.5, 36.5)
    ax.set_ylim(-1.35, 5.6)
    return guardar(fig, "fig7_vintage.png")


# 8 ── convergencia de metodos
def fig8(res):
    c = res["C_convergencia_metodos"]
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    et = ["TMYx completo\n(centroide %.0f)" % c["centroide_completo"],
          "TMYx 2011-2025\n(centroide %.0f)" % c["centroide_reciente"],
          "Meteonorm 2050\nRCP8.5 (CMIP5)\nNO VERIFICADO",
          "FWG 2050\nSSP5-8.5 (CMIP6)"]
    val = [c["linea_base_completo_C"], c["linea_base_reciente_C"],
           c["T_2050_meteonorm_rcp85_C"], c["T_2050_fwg_ssp585_C"]]
    col = ["#bdbdbd", "#969696", "#fdae61", "#cb181d"]
    bars = ax.bar(et, val, color=col, edgecolor="k", linewidth=0.5)
    ax.bar_label(bars, fmt="%.2f C", fontsize=8.5, padding=2)
    ax.set_ylim(18.5, 22.4)
    ax.set_ylabel("Temperatura de bulbo seco media anual, Lima (C)")
    ax.set_title("8 · Convergencia de metodos en Lima\n"
                 "divergencia entre metodos independientes: %+.2f C" % c["divergencia_absoluta_C"],
                 fontsize=10)
    ax.tick_params(axis="x", labelsize=7.5)
    ax.annotate("", xy=(2, c["T_2050_meteonorm_rcp85_C"]), xytext=(3, c["T_2050_fwg_ssp585_C"]),
                arrowprops=dict(arrowstyle="<->", color="k", linewidth=1.2))
    ax.text(2.5, (c["T_2050_meteonorm_rcp85_C"] + c["T_2050_fwg_ssp585_C"]) / 2 + 0.12,
            f"{c['divergencia_absoluta_C']:+.2f} C", ha="center", fontsize=8.5, weight="bold")
    return guardar(fig, "fig8_convergencia_metodos.png")


def hoja_contacto(rutas):
    import matplotlib.image as mpimg
    fig, axes = plt.subplots(4, 2, figsize=(13, 20))
    for ax, r in zip(axes.ravel(), rutas):
        ax.imshow(mpimg.imread(r)); ax.axis("off")
    for ax in axes.ravel()[len(rutas):]:
        ax.axis("off")
    fig.suptitle("Hoja de contacto — revisar cada figura antes de aprobarla (SOP-02 I2)",
                 fontsize=13)
    fig.tight_layout()
    return guardar(fig, "00_hoja_contacto.png")


if __name__ == "__main__":
    t, e, res_global = cargar()
    print("Generando figuras en Temp/renders/ ...")
    rutas = [fig1(t), fig2(t), fig3(res_global), fig4(res_global),
             fig5(t, e), fig6(e), fig7(res_global), fig8(res_global)]
    hoja_contacto(rutas)
    print(f"\n{len(rutas)} figuras + hoja de contacto.")
