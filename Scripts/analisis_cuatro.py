#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analisis_cuatro.py — Paso 5. Los cuatro analisis de la auditoria.

  A. Auditoria de vintage      cuanto "calentamiento" de un TMYx es artefacto
                               de que anos se eligieron
  B. Deltas climaticos por zona  el calentamiento proyectado, es uniforme?
  C. Convergencia de metodos     FWG (morphing) vs Meteonorm (sintesis)
  D. Firma de sintesis           subestiman los sinteticos los episodios calidos?

Entradas:  Data/metricas_todas_v1.csv        (40 TMYx)
           Data/metricas_escenarios_v1.csv   (bases + escenarios FWG 2050)
Salida:    Data/analisis_cuatro_v1.json  y  Temp/analisis_cuatro.md

Uso: python Scripts/analisis_cuatro.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent

# Zonas climaticas. Asignadas por elevacion y regimen, no por departamento.
ZONA = {
    "Lima": "costa desertica", "Trujillo": "costa norte", "Piura": "costa norte",
    "Tacna": "costa sur arida", "Arequipa": "altiplano arido",
    "Cusco": "altura", "Juliaca": "altiplano frio", "Iquitos": "selva humeda",
}
ANDINAS = {"Arequipa", "Cusco", "Juliaca"}

# Hallazgo previo sobre Meteonorm 8.0.2 RCP8.5 2050 para Lima.
# NO verificado por este proyecto: el archivo no esta disponible. Se usa tal como
# viene declarado en el enunciado y se marca como tal en todas las salidas.
METEONORM_LIMA = {
    "fuente": "hallazgo previo declarado en el prompt; archivo NO disponible",
    "verificado_aqui": False,
    "dT_vs_tmyx_completo_C": 1.65,
    "autocorr_lag1": 0.929,
    "autocorr_lag1_medido_referencia": 0.963,
    "escenario": "RCP8.5 (CMIP5)",
}


def cargar():
    t = pd.read_csv(RAIZ / "Data" / "metricas_todas_v1.csv")
    t["ventana"] = t["archivo"].str.extract(r"TMYx\.?(\d{4}-\d{4})?")[0].fillna("completo")
    e = pd.read_csv(RAIZ / "Data" / "metricas_escenarios_v1.csv")
    # Filtra el duplicado heredado del piloto de Lima.
    e = e[~e["archivo"].str.contains("BASE_TMYx", na=False)].copy()
    e["escenario"] = e["archivo"].str.extract(r"_(BASE|ssp\d{3})_")[0]
    return t, e


# ── A. Vintage ────────────────────────────────────────────────────────────────
def analisis_A(t: pd.DataFrame) -> dict:
    """Correlaciona el delta-T aparente contra la diferencia de anos centroides.

    Para cada ciudad se toma el TMYx de periodo completo como referencia y se mide,
    contra cada ventana, cuanto cambia la temperatura media y cuanto cambia el ano
    centroide. Si la pendiente es positiva y consistente, buena parte del
    "calentamiento" que un consultor leeria de un TMYx es seleccion de anos.
    """
    filas = []
    for ciudad, g in t.groupby("ciudad"):
        base = g[g["ventana"] == "completo"]
        if base.empty:
            continue
        b = base.iloc[0]
        for _, r in g[g["ventana"] != "completo"].iterrows():
            filas.append({
                "ciudad": ciudad, "zona": ZONA.get(ciudad, "?"), "ventana": r["ventana"],
                "andina": ciudad in ANDINAS,
                "d_centroide_anos": r["ano_centroide"] - b["ano_centroide"],
                "dT_aparente_C": r["dbt_media"] - b["dbt_media"],
                "centroide_completo": b["ano_centroide"],
                "centroide_ventana": r["ano_centroide"],
            })
    d = pd.DataFrame(filas)

    def ajuste(sub, etiqueta):
        x = sub["d_centroide_anos"].to_numpy(float)
        y = sub["dT_aparente_C"].to_numpy(float)
        ok = ~(np.isnan(x) | np.isnan(y))
        x, y = x[ok], y[ok]
        if len(x) < 3:
            return {"etiqueta": etiqueta, "n": int(len(x)), "nota": "muestra insuficiente"}
        m, c = np.polyfit(x, y, 1)
        r = np.corrcoef(x, y)[0, 1]
        return {"etiqueta": etiqueta, "n": int(len(x)),
                "pendiente_C_por_ano": float(m), "intercepto_C": float(c),
                "r": float(r), "r2": float(r ** 2),
                "calentamiento_por_decada_C": float(m * 10)}

    return {
        "tabla": d.to_dict("records"),
        "ajuste_todas": ajuste(d, "todas las ciudades"),
        "ajuste_sin_andinas_2004_2018": ajuste(
            d[~((d["andina"]) & (d["ventana"] == "2004-2018"))],
            "excluyendo la ventana 2004-2018 de las 3 ciudades andinas (ver D-08)"),
        "rango_dT": {"min_C": float(d["dT_aparente_C"].min()),
                     "max_C": float(d["dT_aparente_C"].max()),
                     "mediana_C": float(d["dT_aparente_C"].median())},
    }


# ── B. Deltas por zona ────────────────────────────────────────────────────────
def analisis_B(e: pd.DataFrame) -> dict:
    """Delta-T, delta-humedad y delta-carga entre la base 2011-2025 y los 2050.

    Se separa carga SENSIBLE (grados-hora sobre 24 C) de proxy de carga LATENTE
    (humedad absoluta), porque en clima humedo el segundo pesa mas que el primero
    y un analisis que solo mire bulbo seco subestima el problema.
    """
    filas = []
    for ciudad, g in e.groupby("ciudad"):
        base = g[g["escenario"] == "BASE"]
        if base.empty:
            continue
        b = base.iloc[0]
        for esc in ("ssp245", "ssp585"):
            sub = g[g["escenario"] == esc]
            if sub.empty:
                continue
            r = sub.iloc[0]
            filas.append({
                "ciudad": ciudad, "zona": ZONA.get(ciudad, "?"), "escenario": esc,
                "elevacion_m": float(b["elevacion_m"]),
                "T_base_C": float(b["dbt_media"]), "dT_C": float(r["dbt_media"] - b["dbt_media"]),
                "W_base_gkg": float(b["w_media_gkg"]),
                "dW_gkg": float(r["w_media_gkg"] - b["w_media_gkg"]),
                "dW_pct": float((r["w_media_gkg"] - b["w_media_gkg"]) / b["w_media_gkg"] * 100),
                "GH24_base_Ch": float(b["gh_enfriamiento_b24"]),
                "GH24_fut_Ch": float(r["gh_enfriamiento_b24"]),
                "dGH24_Ch": float(r["gh_enfriamiento_b24"] - b["gh_enfriamiento_b24"]),
                "h_sobre_26_base": int(b["horas_sobre_26"]),
                "h_sobre_26_fut": int(r["horas_sobre_26"]),
            })
    d = pd.DataFrame(filas)
    res = {"tabla": d.to_dict("records")}
    for esc in ("ssp245", "ssp585"):
        s = d[d["escenario"] == esc]
        if s.empty:
            continue
        res[f"resumen_{esc}"] = {
            "dT_min_C": float(s["dT_C"].min()), "dT_max_C": float(s["dT_C"].max()),
            "dT_media_C": float(s["dT_C"].mean()),
            "ciudad_menor_dT": s.loc[s["dT_C"].idxmin(), "ciudad"],
            "ciudad_mayor_dT": s.loc[s["dT_C"].idxmax(), "ciudad"],
            "rango_dT_C": float(s["dT_C"].max() - s["dT_C"].min()),
            "corr_dT_elevacion": float(np.corrcoef(s["elevacion_m"], s["dT_C"])[0, 1]),
            "dW_max_gkg": float(s["dW_gkg"].max()),
            "ciudad_mayor_dW": s.loc[s["dW_gkg"].idxmax(), "ciudad"],
        }
    return res


# ── C. Convergencia de metodos ────────────────────────────────────────────────
def analisis_C(t: pd.DataFrame, e: pd.DataFrame) -> dict:
    """FWG (morphing determinista) contra Meteonorm (sintesis estocastica), Lima.

    El punto delicado: los dos numeros NO se pueden comparar directamente porque
    parten de lineas base distintas. Meteonorm se reporto contra el TMYx de periodo
    completo (centroide 1999.4); FWG se corrio sobre la ventana 2011-2025
    (centroide 2017.6). Se llevan ambos a temperatura ABSOLUTA de 2050, que si es
    comparable.
    """
    lt = t[t["ciudad"] == "Lima"]
    completo = lt[lt["ventana"] == "completo"]
    reciente = lt[lt["ventana"] == "2011-2025"]
    le = e[e["ciudad"] == "Lima"]
    fwg585 = le[le["escenario"] == "ssp585"]
    if completo.empty or reciente.empty or fwg585.empty:
        return {"estado": "NO COMPLETADO", "motivo": "faltan archivos de Lima"}

    T_completo = float(completo.iloc[0]["dbt_media"])
    T_reciente = float(reciente.iloc[0]["dbt_media"])
    T_fwg_2050 = float(fwg585.iloc[0]["dbt_media"])
    T_mn_2050 = T_completo + METEONORM_LIMA["dT_vs_tmyx_completo_C"]

    return {
        "estado": "PARCIAL — Meteonorm no verificado (archivo no disponible)",
        "meteonorm": METEONORM_LIMA,
        "linea_base_completo_C": T_completo,
        "centroide_completo": float(completo.iloc[0]["ano_centroide"]),
        "linea_base_reciente_C": T_reciente,
        "centroide_reciente": float(reciente.iloc[0]["ano_centroide"]),
        "desfase_entre_bases_C": T_reciente - T_completo,
        "T_2050_meteonorm_rcp85_C": T_mn_2050,
        "T_2050_fwg_ssp585_C": T_fwg_2050,
        "divergencia_absoluta_C": T_fwg_2050 - T_mn_2050,
        "dT_meteonorm_declarado_C": METEONORM_LIMA["dT_vs_tmyx_completo_C"],
        "dT_fwg_sobre_su_base_C": T_fwg_2050 - T_reciente,
        "advertencia": ("RCP8.5 es CMIP5 y SSP5-8.5 es CMIP6: no son el mismo escenario. "
                        "Forzamiento radiativo similar a 2100, trayectorias y modelos distintos. "
                        "La comparacion es indicativa, no una validacion cruzada estricta."),
    }


# ── D. Firma de sintesis ──────────────────────────────────────────────────────
def analisis_D(t: pd.DataFrame, e: pd.DataFrame) -> dict:
    """Estructura temporal: TMYx (ensamblado de meses medidos) contra FWG (morphing).

    Hipotesis del prompt: los sinteticos subestiman los episodios calidos multi-dia.
    El morphing de FWG NO deberia alterar la estructura, porque desplaza y escala la
    serie existente. Si la altera, es un hallazgo. Meteonorm, que si sintetiza
    estocasticamente, es el caso donde se espera degradacion — y no lo tenemos.
    """
    filas = []
    for ciudad, g in e.groupby("ciudad"):
        base = g[g["escenario"] == "BASE"]
        if base.empty:
            continue
        b = base.iloc[0]
        for esc in ("ssp245", "ssp585"):
            sub = g[g["escenario"] == esc]
            if sub.empty:
                continue
            r = sub.iloc[0]
            filas.append({
                "ciudad": ciudad, "escenario": esc,
                "autocorr_base": float(b["autocorr_lag1"]),
                "autocorr_fut": float(r["autocorr_lag1"]),
                "d_autocorr": float(r["autocorr_lag1"] - b["autocorr_lag1"]),
                "racha_max_base_d": int(b["rachas_p90_dur_max"]),
                "racha_max_fut_d": int(r["rachas_p90_dur_max"]),
                "racha_media_base_d": float(b["rachas_p90_dur_media"]),
                "racha_media_fut_d": float(r["rachas_p90_dur_media"]),
                "rango_diario_base_C": float(b["rango_diario_medio"]),
                "rango_diario_fut_C": float(r["rango_diario_medio"]),
                "d_rango_diario_C": float(r["rango_diario_medio"] - b["rango_diario_medio"]),
            })
    d = pd.DataFrame(filas)
    return {
        "tabla": d.to_dict("records"),
        "resumen": {
            "d_autocorr_max_abs": float(d["d_autocorr"].abs().max()),
            "d_rango_diario_max_abs_C": float(d["d_rango_diario_C"].abs().max()),
            "casos_racha_max_cambia": int((d["racha_max_base_d"] != d["racha_max_fut_d"]).sum()),
            "n_casos": int(len(d)),
            "veredicto": ("el morphing de FWG preserva la estructura temporal"
                          if d["d_autocorr"].abs().max() < 0.05 else
                          "el morphing ALTERA la estructura temporal — investigar"),
        },
        "limitacion": ("No se pudo contrastar contra un archivo sinteticamente generado "
                       "(Meteonorm). Sin ese contraste, la pregunta del prompt —si los "
                       "sinteticos subestiman los episodios calidos multi-dia— queda "
                       "SIN RESPONDER con datos propios."),
    }


def main() -> int:
    t, e = cargar()
    res = {
        "A_vintage": analisis_A(t),
        "B_deltas_por_zona": analisis_B(e),
        "C_convergencia_metodos": analisis_C(t, e),
        "D_firma_sintesis": analisis_D(t, e),
    }
    sal = RAIZ / "Data" / "analisis_cuatro_v1.json"
    sal.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")

    a, b = res["A_vintage"], res["B_deltas_por_zona"]
    print("=== A · VINTAGE ===")
    for k in ("ajuste_todas", "ajuste_sin_andinas_2004_2018"):
        f = a[k]
        if "pendiente_C_por_ano" in f:
            print(f"  {f['etiqueta']}: n={f['n']}  "
                  f"{f['calentamiento_por_decada_C']:+.3f} C/decada  r2={f['r2']:.3f}")
    print(f"  dT aparente: mediana {a['rango_dT']['mediana_C']:+.2f} C, "
          f"rango {a['rango_dT']['min_C']:+.2f} a {a['rango_dT']['max_C']:+.2f} C")

    print("\n=== B · DELTAS POR ZONA (2050) ===")
    for esc in ("ssp245", "ssp585"):
        r = b.get(f"resumen_{esc}")
        if r:
            print(f"  {esc}: dT {r['dT_min_C']:+.2f} ({r['ciudad_menor_dT']}) a "
                  f"{r['dT_max_C']:+.2f} ({r['ciudad_mayor_dT']}) C, "
                  f"media {r['dT_media_C']:+.2f}, dispersion {r['rango_dT_C']:.2f} C | "
                  f"corr con elevacion r={r['corr_dT_elevacion']:+.2f}")

    c = res["C_convergencia_metodos"]
    print("\n=== C · CONVERGENCIA ===")
    print(f"  {c['estado']}")
    if "divergencia_absoluta_C" in c:
        print(f"  T 2050 Meteonorm RCP8.5 = {c['T_2050_meteonorm_rcp85_C']:.2f} C  |  "
              f"FWG SSP5-8.5 = {c['T_2050_fwg_ssp585_C']:.2f} C  |  "
              f"divergencia {c['divergencia_absoluta_C']:+.2f} C")

    dd = res["D_firma_sintesis"]["resumen"]
    print("\n=== D · FIRMA DE SINTESIS ===")
    print(f"  max |d autocorr| = {dd['d_autocorr_max_abs']:.4f}  |  "
          f"max |d rango diario| = {dd['d_rango_diario_max_abs_C']:.3f} C  |  "
          f"racha max cambia en {dd['casos_racha_max_cambia']}/{dd['n_casos']} casos")
    print(f"  -> {dd['veredicto']}")
    print(f"\nJSON completo -> {sal}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
