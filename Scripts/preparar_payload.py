#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
preparar_payload.py — Arma el JSON que consume el visor web.

Salida: Data/web/payload_v3.json

Contiene, por ciudad y escenario, los CUATRO horizontes (hoy, 2030, 2050, 2080), y
para Lima la nube psicrometrica horaria en los cuatro estados, para poder animar la
transicion completa y no solo un antes-y-despues.

2030 es INTERPOLACION LINEAL entre la linea base y 2050. FWG v4.2.0 no emite ese
horizonte. Va marcado con la bandera "interpolado": un valor derivado sin marcar seria
un dato inventado (SOP-02 A2).

Idempotente (SOP-02 H1). Uso: python Scripts/preparar_payload.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "Scripts"))
from analizar_epw import leer_datos, humedad_absoluta_gkg  # noqa: E402

MES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
ZONA = {"Lima": "costa desértica", "Trujillo": "costa norte", "Piura": "costa norte",
        "Tacna": "costa sur árida", "Arequipa": "altiplano árido", "Cusco": "altura",
        "Juliaca": "altiplano frío", "Iquitos": "selva húmeda"}
PASO_NUBE = 6      # 1 de cada 6 horas -> 1460 puntos por estado

# Contorno de Peru. Fuente: world.geo.json (dominio publico), descargado 26/07/2026.
PERU = json.loads((RAIZ / "Data" / "web" / "peru_contorno.json").read_text(encoding="utf-8"))


def climograma(ruta: Path) -> dict:
    """Por mes: media de las maximas DIARIAS, media de las minimas DIARIAS, y los
    extremos absolutos. La 'maxima de febrero' que la gente percibe es la primera,
    no el record absoluto: por eso se reportan las dos."""
    d = leer_datos(ruta)
    d = d.assign(dia=(d.index // 24) + 1)
    out = {"maxm": [], "minm": [], "maxabs": [], "minabs": [], "media": []}
    for m in range(1, 13):
        s = d[d.mo == m]
        pordia = s.groupby("dia").dbt
        out["maxm"].append(round(float(pordia.max().mean()), 1))
        out["minm"].append(round(float(pordia.min().mean()), 1))
        out["maxabs"].append(round(float(s.dbt.max()), 1))
        out["minabs"].append(round(float(s.dbt.min()), 1))
        out["media"].append(round(float(s.dbt.mean()), 1))
    return out


def nube(ruta: Path) -> list:
    """Cada punto es una hora: [bulbo seco, humedad absoluta, mes, hora del dia].
    El mes permite colorear por estacion, que es informacion NUEVA; colorear por
    temperatura duplicaba el eje X y no anadia nada."""
    d = leer_datos(ruta)
    dbt = d.dbt.to_numpy(float)
    w = humedad_absoluta_gkg(dbt, d.rh.to_numpy(float), d.pres.to_numpy(float) / 1000.0)
    mo = d.mo.to_numpy()
    hr = d.hr.to_numpy()
    i = np.arange(0, 8760, PASO_NUBE)
    return [[round(float(dbt[k]), 1), round(float(w[k]), 1), int(mo[k]), int(hr[k])] for k in i]


def main() -> int:
    D = RAIZ / "Data"
    t = pd.read_csv(D / "metricas_todas_v1.csv")
    t["v"] = t.archivo.str.extract(r"TMYx\.?(\d{4}-\d{4})?")[0].fillna("completo")
    base = t[t.v == "2011-2025"].set_index("ciudad")

    e = pd.read_csv(D / "metricas_escenarios_v1.csv")
    e = e[~e.archivo.str.contains("BASE_TMYx", na=False)]
    e["esc"] = e.archivo.str.extract(r"_(BASE|ssp\d{3})_")[0]
    f80 = pd.read_csv(D / "metricas_2080_v1.csv")
    f80["esc"] = f80.archivo.str.extract(r"_(ssp\d{3})_")[0]

    def campos(r):
        return dict(T=round(float(r.dbt_media), 2), W=round(float(r.w_media_gkg), 2),
                    gh=round(float(r.gh_enfriamiento_b24)), h26=int(r.horas_sobre_26),
                    p99=round(float(r["dbt_p99.0"]), 1), mx=round(float(r.dbt_max), 1),
                    tcal=round(float(r["dbt_p0.4"]), 1), tref=round(float(r["dbt_p99.6"]), 1))

    ciudades = []
    for n in sorted(e.ciudad.unique()):
        m = base.loc[n]
        y0 = float(m.ano_centroide)
        c = dict(n=n, zona=ZONA[n], lat=float(m.lat), lon=float(m.lon),
                 elev=float(m.elevacion_m), y0=round(y0, 1),
                 ghi=round(float(m.ghi_anual_kwh_m2)), ac=round(float(m.autocorr_lag1), 3),
                 racha=int(m.rachas_p90_dur_max),
                 mens=[round(float(m[f"dbt_media_{x}"]), 2) for x in MES])
        # Serie OBSERVADA: cada ventana TMYx situada en su ano centroide. Son datos
        # medidos (METAR ensamblado), no modelo. Ver la advertencia en el visor: las
        # ventanas se solapan y cada una es un ano tipico, no una observacion anual.
        obs = t[t.ciudad == n][["v", "ano_centroide", "dbt_media"]].dropna()
        c["obs"] = sorted([[round(float(r.ano_centroide), 1), round(float(r.dbt_media), 2),
                            str(r.v)] for _, r in obs.iterrows()])
        b = e[(e.ciudad == n) & (e.esc == "BASE")].iloc[0]
        # Climograma: hoy es comun a los dos escenarios; 2050 y 2080 dependen de cada uno.
        base_epw = next((RAIZ / "Data" / "escenarios_v1" / n).glob("*_BASE_*.epw"))
        cg_hoy = climograma(base_epw)
        for s, k in [("ssp245", "s245"), ("ssp585", "s585")]:
            H = {"hoy": campos(b),
                 "a2050": campos(e[(e.ciudad == n) & (e.esc == s)].iloc[0]),
                 "a2080": campos(f80[(f80.ciudad == n) & (f80.esc == s)].iloc[0])}
            fr = (2030 - y0) / (2050 - y0)          # interpolacion lineal hasta 2050
            H["a2030"] = {kk: round(H["hoy"][kk] + (H["a2050"][kk] - H["hoy"][kk]) * fr,
                                    2 if kk in ("T", "W") else (1 if kk in ("p99", "mx", "tcal", "tref") else 0))
                          for kk in H["hoy"]}
            cg = {"hoy": cg_hoy,
                  "a2050": climograma(next((RAIZ / "Data" / "escenarios_v1" / n)
                                           .glob(f"*_{s}_2050.epw"))),
                  "a2080": climograma(next((RAIZ / "Data" / "escenarios_2080_v1" / n)
                                           .glob(f"*_{s}_2080.epw")))}
            cg["a2030"] = {campo: [round(cg["hoy"][campo][i]
                                         + (cg["a2050"][campo][i] - cg["hoy"][campo][i]) * fr, 1)
                                   for i in range(12)] for campo in cg["hoy"]}
            c[k] = {"H": H, "CG": cg}
        ciudades.append(c)

    # Nubes psicrometricas para todas las ciudades en los cuatro estados (SSP5-8.5).
    nubes = {}
    for c_obj in ciudades:
        n_city = c_obj["n"]
        dir_v1 = D / "escenarios_v1" / n_city
        dir_v80 = D / "escenarios_2080_v1" / n_city
        base_f = next(dir_v1.glob("*_BASE_*.epw"))
        f50 = next(dir_v1.glob("*_ssp585_2050.epw"))
        f80 = next(dir_v80.glob("*_ssp585_2080.epw"))

        nh_c = nube(base_f)
        n50_c = nube(f50)
        n80_c = nube(f80)
        y0_c = c_obj["y0"]
        fr_c = (2030 - y0_c) / (2050 - y0_c)
        n30_c = [[round(a[0] + (b[0] - a[0]) * fr_c, 1), round(a[1] + (b[1] - a[1]) * fr_c, 1), a[2], a[3]]
                 for a, b in zip(nh_c, n50_c)]
        nubes[n_city] = {"hoy": nh_c, "a2030": n30_c, "a2050": n50_c, "a2080": n80_c}

    res = json.loads((D / "analisis_cuatro_v1.json").read_text(encoding="utf-8"))
    ipcc = json.loads((D / "web" / "ipcc_data.json").read_text(encoding="utf-8"))
    out = {
        "peru": PERU, "ciudades": ciudades,
        "nubes": nubes,
        "nube_escenario": "SSP5-8.5",
        "ipcc": ipcc,
        "vintage": [dict(c=r.ciudad, v=r.ventana, a=bool(r.andina),
                         x=round(float(r.d_centroide_anos), 1),
                         y=round(float(r.dT_aparente_C), 2))
                    for _, r in pd.DataFrame(res["A_vintage"]["tabla"]).iterrows()],
        "ajuste": res["A_vintage"]["ajuste_sin_andinas_2004_2018"],
        "conv": res["C_convergencia_metodos"],
        "interpolado": ["a2030"],
    }
    sal = D / "web" / "payload_v3.json"
    sal.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"  {sal}  ({sal.stat().st_size/1024:.0f} KB)")
    print(f"  {len(ciudades)} ciudades × 2 escenarios × 4 horizontes")
    print(f"  nubes: {len(nubes)} ciudades × {len(next(iter(nubes.values()))['hoy'])} puntos × 4 estados ({res and 'SSP5-8.5'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
