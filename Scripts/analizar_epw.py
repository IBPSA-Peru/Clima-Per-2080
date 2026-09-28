#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analizar_epw.py — Motor de metricas del proyecto de Auditoria de Clima Peru.

Recorre una carpeta de archivos EPW y escribe una fila de metricas por archivo en
Data\\metricas_todas_vN.csv.

Uso:
    python Scripts/analizar_epw.py                       # usa Input/clima -> Data/
    python Scripts/analizar_epw.py --entrada RUTA --salida RUTA.csv
    python Scripts/analizar_epw.py --forzar              # ignora el checkpoint
    python Scripts/analizar_epw.py --autotest            # prueba sobre EPW sintetico

Idempotencia y checkpointing (SOP-02 H1, G3):
    Se guarda un hash SHA-256 del contenido de cada EPW. Si el archivo no cambio y
    ya hay fila en el CSV de salida, no se recalcula. La verificacion es por
    contenido, no por fecha de modificacion.

Convencion de unidades — se reporta en la unidad del problema (SOP-02 F2):
    temperatura  C            humedad absoluta  g/kg aire seco
    irradiancia  kWh/m2-ano   grados-hora       C-h
    viento       m/s          rachas            dias

Dependencias: pandas, numpy. Nada mas.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# ── Estructura del EPW ────────────────────────────────────────────────────────
# El EPW son 8 lineas de cabecera y luego 8760 lineas de datos horarios.
EPW_COLS = [
    "yr", "mo", "dy", "hr", "mn", "flags", "dbt", "dpt", "rh", "pres",
    "exhor", "exdn", "ir", "ghi", "dni", "dhi", "gh_ill", "dn_ill",
    "dh_ill", "zlum", "wdir", "wspd", "tsky", "osky", "vis", "ceil",
    "pwo", "pwc", "pwat", "aod", "snow", "dsnow", "alb", "lpd", "lpq",
]

# Centinelas de "dato ausente" del formato EPW. Se convierten a NaN.
CENTINELAS = {
    "dbt": 99.9, "dpt": 99.9, "rh": 999.0, "pres": 999999.0,
    "ghi": 9999.0, "dni": 9999.0, "dhi": 9999.0, "wspd": 999.0,
}

MESES = ["ene", "feb", "mar", "abr", "may", "jun",
         "jul", "ago", "sep", "oct", "nov", "dic"]

# Bases de grados-hora y umbrales pedidos en el Paso 4 del prompt.
BASES_ENFRIAMIENTO = [18, 24, 26, 28]
BASE_CALEFACCION = 18
UMBRALES_CALOR = [26, 28, 30, 32]
UMBRALES_FRIO = [10, 5]

# Clausius-Clapeyron a HR constante: la humedad absoluta de saturacion crece
# ~6.2 %/K cerca de temperatura ambiente. Umbral de sospecha del prompt: 4 pp.
CC_PCT_POR_K = 6.2
CC_DESVIO_SOSPECHOSO_PP = 4.0


# ── Lectura ───────────────────────────────────────────────────────────────────
def hash_archivo(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(65536), b""):
            h.update(bloque)
    return h.hexdigest()


def leer_cabecera(ruta: Path) -> dict:
    """Extrae procedencia del EPW: estacion, WMO, coordenadas, periodo, mes-a-ano.

    Devuelve un dict con lo que se pudo leer. Los campos que no aparecen quedan
    en None: un hueco declarado, nunca un valor inventado (SOP-02 A1).
    """
    with open(ruta, "r", encoding="latin-1") as f:
        lineas = [f.readline() for _ in range(8)]

    info: dict = {
        "estacion": None, "wmo": None, "lat": None, "lon": None,
        "huso": None, "elevacion_m": None, "fuente": None,
        "periodo_registro": None, "tiene_cond_diseno": False,
        "anos_por_mes": None, "ano_centroide": None,
    }

    # LOCATION,ciudad,estado,pais,fuente,WMO,lat,lon,husohorario,elevacion
    p = lineas[0].strip().split(",")
    if p and p[0].upper() == "LOCATION" and len(p) >= 10:
        info["estacion"] = p[1].strip()
        info["fuente"] = p[4].strip()
        info["wmo"] = p[5].strip()
        for clave, idx in (("lat", 6), ("lon", 7), ("huso", 8), ("elevacion_m", 9)):
            try:
                info[clave] = float(p[idx])
            except (ValueError, IndexError):
                pass

    # DESIGN CONDITIONS,<n>,...  n=0 significa que no trae condiciones de diseno.
    p1 = lineas[1].strip().split(",")
    if p1 and p1[0].upper().startswith("DESIGN CONDITIONS"):
        try:
            info["tiene_cond_diseno"] = int(p1[1]) > 0
        except (ValueError, IndexError):
            info["tiene_cond_diseno"] = len(p1) > 3

    # COMMENTS 1/2 traen, en los TMYx, el periodo y el ano fuente de cada mes.
    comentarios = " ".join(l.strip() for l in lineas[5:7])
    info["periodo_registro"] = _extraer_periodo(comentarios)

    anos = _extraer_anos_por_mes(comentarios)
    if anos:
        info["anos_por_mes"] = ";".join(str(a) if a else "" for a in anos)
        validos = [a for a in anos if a]
        if validos:
            # Ano centroide = media de los anos fuente de los 12 meses. Es la
            # variable que el Analisis A correlaciona contra el delta-T aparente.
            info["ano_centroide"] = round(sum(validos) / len(validos), 1)

    return info


def _extraer_periodo(texto: str) -> str | None:
    """Busca un rango de anos tipo 1960-2025 o 2009-2023 en los comentarios."""
    import re
    m = re.findall(r"\b(19\d{2}|20\d{2})\s*[-–]\s*(19\d{2}|20\d{2})\b", texto)
    if not m:
        return None
    # Se queda con el rango mas ancho: es el periodo de registro de la estacion.
    ini, fin = max(m, key=lambda t: int(t[1]) - int(t[0]))
    return f"{ini}-{fin}"


def _extraer_anos_por_mes(texto: str) -> list[int | None] | None:
    """Los TMYx listan, mes a mes, de que ano salio. Formato tipico:
    'Jan:1969, Feb:2011, ...' o 'Jan=1969 Feb=2011'.
    """
    import re
    abrev = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    anos: list[int | None] = []
    encontrados = 0
    for a in abrev:
        m = re.search(rf"\b{a}[a-z]*\b\s*[:=\-]?\s*(19\d{{2}}|20\d{{2}})", texto, re.I)
        if m:
            anos.append(int(m.group(1)))
            encontrados += 1
        else:
            anos.append(None)
    return anos if encontrados >= 6 else None


def leer_datos(ruta: Path) -> pd.DataFrame:
    df = pd.read_csv(
        ruta, skiprows=8, header=None, names=EPW_COLS,
        encoding="latin-1", usecols=range(len(EPW_COLS)), low_memory=False,
    )
    for col, centinela in CENTINELAS.items():
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df[col] >= centinela, col] = np.nan
    for col in ("mo", "dy", "hr"):
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    # Indice de dia del ano, para agrupar sin depender de fechas reales.
    df["dia"] = (df.index // 24) + 1
    return df


# ── Psicrometria ──────────────────────────────────────────────────────────────
def presion_saturacion_kpa(t_c: np.ndarray) -> np.ndarray:
    """Magnus-Tetens. Devuelve kPa. Valida entre -40 y +50 C, sobra para Peru."""
    return 0.61094 * np.exp((17.625 * t_c) / (t_c + 243.04))


def humedad_absoluta_gkg(t_c: np.ndarray, hr_pct: np.ndarray,
                         p_kpa: np.ndarray) -> np.ndarray:
    """Razon de mezcla en g de vapor por kg de aire seco."""
    pv = presion_saturacion_kpa(t_c) * np.clip(hr_pct, 0, 100) / 100.0
    pv = np.minimum(pv, p_kpa * 0.999)  # evita division por cero si pv -> p
    return 621.945 * pv / (p_kpa - pv)


# ── Metricas ──────────────────────────────────────────────────────────────────
def metricas_archivo(ruta: Path) -> dict:
    cab = leer_cabecera(ruta)
    df = leer_datos(ruta)

    m: dict = {"archivo": ruta.name, "ciudad": ruta.parent.name, **cab}

    # --- Integridad. Un EPW que no trae 8760 filas no es comparable. ---
    m["n_filas"] = len(df)
    m["integridad_8760"] = (len(df) == 8760)
    m["dbt_faltantes"] = int(df["dbt"].isna().sum())

    dbt = df["dbt"].to_numpy(dtype=float)
    rh = df["rh"].to_numpy(dtype=float)
    pres_kpa = df["pres"].to_numpy(dtype=float) / 1000.0
    # Si falta presion se usa la barometrica de la elevacion del sitio: es una
    # sustitucion fisica, no un relleno arbitrario. Se declara con una bandera.
    elev = cab.get("elevacion_m") or 0.0
    p_altitud = 101.325 * (1 - 2.25577e-5 * elev) ** 5.25588
    m["presion_sustituida"] = bool(np.isnan(pres_kpa).any())
    pres_kpa = np.where(np.isnan(pres_kpa), p_altitud, pres_kpa)

    w = humedad_absoluta_gkg(dbt, rh, pres_kpa)

    # --- Estadistica basica ---
    m["dbt_media"] = np.nanmean(dbt)
    m["dbt_min"] = np.nanmin(dbt)
    m["dbt_max"] = np.nanmax(dbt)
    for q in (0.4, 1.0, 99.0, 99.6):
        m[f"dbt_p{q}"] = np.nanpercentile(dbt, q)
    m["hr_media"] = np.nanmean(rh)
    m["dpt_media"] = np.nanmean(df["dpt"].to_numpy(dtype=float))
    m["dpt_p99"] = np.nanpercentile(df["dpt"].to_numpy(dtype=float), 99)
    m["w_media_gkg"] = np.nanmean(w)
    m["w_p99_gkg"] = np.nanpercentile(w, 99)
    m["wspd_media"] = np.nanmean(df["wspd"].to_numpy(dtype=float))

    # Irradiancia: la suma horaria de W/m2 son Wh/m2; /1000 -> kWh/m2-ano.
    m["ghi_anual_kwh_m2"] = np.nansum(df["ghi"].to_numpy(dtype=float)) / 1000.0
    m["dni_anual_kwh_m2"] = np.nansum(df["dni"].to_numpy(dtype=float)) / 1000.0

    # --- Carga termica ---
    for b in BASES_ENFRIAMIENTO:
        m[f"gh_enfriamiento_b{b}"] = float(np.nansum(np.clip(dbt - b, 0, None)))
    m[f"gh_calefaccion_b{BASE_CALEFACCION}"] = float(
        np.nansum(np.clip(BASE_CALEFACCION - dbt, 0, None)))
    for u in UMBRALES_CALOR:
        m[f"horas_sobre_{u}"] = int(np.nansum(dbt > u))
    for u in UMBRALES_FRIO:
        m[f"horas_bajo_{u}"] = int(np.nansum(dbt < u))

    # --- Estructura temporal: aqui es donde medido y sintetico se separan ---
    diario = df.groupby("dia")["dbt"]
    rango_diario = (diario.max() - diario.min()).to_numpy(dtype=float)
    m["rango_diario_medio"] = float(np.nanmean(rango_diario))
    m["rango_diario_p95"] = float(np.nanpercentile(rango_diario, 95))

    perfil_h = df.groupby("hr")["dbt"].mean()
    if len(perfil_h) > 0:
        m["amplitud_ciclo_diurno"] = float(perfil_h.max() - perfil_h.min())
        m["hora_pico"] = int(perfil_h.idxmax())
    else:
        m["amplitud_ciclo_diurno"] = np.nan
        m["hora_pico"] = None

    media_diaria = diario.mean().to_numpy(dtype=float)
    for lag in (1, 2, 3):
        m[f"autocorr_lag{lag}"] = _autocorr(media_diaria, lag)

    # Rachas calidas: dias consecutivos con media diaria sobre el percentil 90.
    p90 = np.nanpercentile(media_diaria, 90)
    rachas = _rachas(media_diaria > p90)
    m["rachas_p90_cantidad"] = len(rachas)
    m["rachas_p90_dur_media"] = float(np.mean(rachas)) if rachas else 0.0
    m["rachas_p90_dur_max"] = int(max(rachas)) if rachas else 0

    # Resolucion del dato. Un EPW medido en decimas trae ~300-600 valores unicos;
    # uno sintetizado o interpolado suele traer muchos mas, o muchos menos.
    m["dbt_valores_unicos"] = int(pd.Series(dbt).dropna().nunique())

    # --- Desagregado mensual ---
    for i, nombre in enumerate(MESES, start=1):
        sel = df["mo"] == i
        d_m = dbt[sel.to_numpy()]
        w_m = w[sel.to_numpy()]
        m[f"dbt_media_{nombre}"] = float(np.nanmean(d_m)) if d_m.size else np.nan
        m[f"dbt_max_{nombre}"] = float(np.nanmax(d_m)) if d_m.size else np.nan
        m[f"w_media_{nombre}"] = float(np.nanmean(w_m)) if w_m.size else np.nan
        ghi_m = df.loc[sel, "ghi"].to_numpy(dtype=float)
        m[f"ghi_{nombre}_kwh_m2"] = float(np.nansum(ghi_m)) / 1000.0

    m["hash_sha256"] = hash_archivo(ruta)
    return m


def _autocorr(x: np.ndarray, lag: int) -> float:
    x = x[~np.isnan(x)]
    if len(x) <= lag + 2:
        return np.nan
    a, b = x[:-lag], x[lag:]
    a = a - a.mean()
    b = b - b.mean()
    den = np.sqrt((a ** 2).sum() * (b ** 2).sum())
    return float((a * b).sum() / den) if den > 0 else np.nan


def _rachas(mascara: np.ndarray) -> list[int]:
    """Longitudes de las rachas contiguas de True."""
    out, actual = [], 0
    for v in mascara:
        if v:
            actual += 1
        elif actual:
            out.append(actual)
            actual = 0
    if actual:
        out.append(actual)
    return out


# ── Coherencia fisica: Clausius-Clapeyron ─────────────────────────────────────
def chequeo_clausius_clapeyron(base: dict, escenario: dict) -> dict:
    """Compara base contra escenario. A HR constante la humedad absoluta deberia
    crecer ~6.2 %/K. Un desvio grande delata morphing que no toco la humedad, o
    una sintesis que la desacoplo de la temperatura.

    Devuelve el desvio en PUNTOS PORCENTUALES, no en porcentaje del porcentaje:
    la diferencia entre el %/K observado y el %/K teorico.
    """
    dT = escenario["dbt_media"] - base["dbt_media"]
    if abs(dT) < 0.05:
        return {"cc_dT": dT, "cc_pct_por_K_obs": np.nan,
                "cc_desvio_pp": np.nan, "cc_sospechoso": False,
                "cc_nota": "delta-T casi nulo; el cociente no es informativo"}

    dW_pct = (escenario["w_media_gkg"] - base["w_media_gkg"]) / base["w_media_gkg"] * 100.0
    obs = dW_pct / dT
    desvio = obs - CC_PCT_POR_K
    return {
        "cc_dT": dT,
        "cc_pct_por_K_obs": obs,
        "cc_desvio_pp": desvio,
        "cc_sospechoso": bool(abs(desvio) > CC_DESVIO_SOSPECHOSO_PP),
        "cc_nota": "",
    }


# ── Orquestacion ──────────────────────────────────────────────────────────────
def recorrer(entrada: Path, salida: Path, forzar: bool = False) -> pd.DataFrame:
    archivos = sorted(entrada.rglob("*.epw"))
    if not archivos:
        print(f"[AVISO] No se encontro ningun .epw bajo {entrada}")
        print("        Si Input/clima esta vacio, falta correr Scripts/DESCARGAR_CLIMA.bat")
        return pd.DataFrame()

    previo = pd.DataFrame()
    if salida.exists() and not forzar:
        try:
            previo = pd.read_csv(salida)
        except Exception:
            previo = pd.DataFrame()

    ya = {}
    if not previo.empty and "hash_sha256" in previo.columns:
        ya = dict(zip(previo["archivo"], previo["hash_sha256"]))

    filas, reutilizados = [], 0
    for ruta in archivos:
        h = hash_archivo(ruta)
        if ya.get(ruta.name) == h:
            filas.append(previo[previo["archivo"] == ruta.name].iloc[0].to_dict())
            reutilizados += 1
            continue
        try:
            filas.append(metricas_archivo(ruta))
            print(f"  calculado  {ruta.parent.name}/{ruta.name}")
        except Exception as e:
            print(f"  [FALLO]    {ruta.parent.name}/{ruta.name} :: {e}")
            filas.append({"archivo": ruta.name, "ciudad": ruta.parent.name,
                          "error": str(e)})

    df = pd.DataFrame(filas)
    salida.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(salida, index=False)
    print(f"\n{len(df)} archivos ({reutilizados} reutilizados del checkpoint) "
          f"-> {salida}")
    return df


def verificar(df: pd.DataFrame) -> int:
    """Compuerta de coherencia interna (SOP-02 B2). Devuelve numero de problemas."""
    if df.empty:
        return 1
    problemas = 0

    incompletos = df[df.get("integridad_8760", pd.Series(dtype=bool)) == False]
    if len(incompletos):
        print(f"[REVISAR] {len(incompletos)} archivos no traen 8760 filas: "
              f"{list(incompletos['archivo'])}")
        problemas += len(incompletos)

    if "dbt_media" in df:
        # Peru va de la selva a 4000 m. Fuera de -15..40 C de media anual hay error.
        raros = df[(df["dbt_media"] < -15) | (df["dbt_media"] > 40)]
        if len(raros):
            print(f"[REVISAR] media anual fuera de rango plausible en "
                  f"{len(raros)} archivos")
            problemas += len(raros)

    if "ano_centroide" in df:
        sin = int(df["ano_centroide"].isna().sum())
        if sin:
            print(f"[REVISAR] {sin} de {len(df)} archivos sin ano centroide legible "
                  f"en la cabecera. El Analisis A depende de ese dato.")
            problemas += sin

    if problemas == 0:
        print("[OK] Coherencia interna: sin observaciones.")
    return problemas


# ── Autotest ──────────────────────────────────────────────────────────────────
def autotest() -> int:
    """Genera un EPW sintetico de propiedades conocidas y comprueba que el motor
    las recupera. Sirve para validar el codigo SIN los datos reales, que a esta
    altura del proyecto todavia no estan descargados.
    """
    import tempfile
    print("Autotest: generando EPW sintetico de propiedades conocidas...")

    MEDIA, AMPLITUD = 20.0, 5.0   # media 20 C, ciclo diurno de +-5 C (rango 10)
    horas = np.arange(8760)
    # Pico a las 15 h: coseno desfasado.
    dbt = MEDIA + AMPLITUD * np.cos(2 * np.pi * (horas % 24 - 15) / 24)
    rh = np.full(8760, 70.0)
    pres = np.full(8760, 101325.0)

    lineas = [
        "LOCATION,Ciudad Prueba,XX,PER,AUTOTEST,999999,-12.02,-77.11,-5.0,34.0",
        "DESIGN CONDITIONS,0",
        "TYPICAL/EXTREME PERIODS,0",
        "GROUND TEMPERATURES,0",
        "HOLIDAYS/DAYLIGHT SAVINGS,No,0,0,0",
        "COMMENTS 1,Sintetico para autotest. Periodo 2009-2023. "
        "Jan:2010, Feb:2011, Mar:2012, Apr:2013, May:2014, Jun:2015, "
        "Jul:2016, Aug:2017, Sep:2018, Oct:2019, Nov:2020, Dec:2021",
        "COMMENTS 2,-",
        "DATA PERIODS,1,1,Data,Sunday, 1/ 1,12/31",
    ]
    dias_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    i = 0
    for mes, nd in enumerate(dias_mes, start=1):
        for d in range(1, nd + 1):
            for h in range(1, 25):
                campos = ["2020", str(mes), str(d), str(h), "0", "?"]
                campos += [f"{dbt[i]:.1f}", "10.0", f"{rh[i]:.0f}", f"{pres[i]:.0f}"]
                campos += ["0"] * (len(EPW_COLS) - len(campos))
                lineas.append(",".join(campos))
                i += 1

    tmp = Path(tempfile.mkdtemp()) / "AUTOTEST"
    tmp.mkdir(parents=True, exist_ok=True)
    ruta = tmp / "PRUEBA_TMYx.epw"
    ruta.write_text("\n".join(lineas), encoding="latin-1")

    m = metricas_archivo(ruta)
    fallos = []

    def check(nombre, obtenido, esperado, tol):
        ok = obtenido is not None and abs(obtenido - esperado) <= tol
        print(f"  {'OK  ' if ok else 'FALLA'}  {nombre}: "
              f"obtenido={obtenido:.3f} esperado={esperado} tol={tol}")
        if not ok:
            fallos.append(nombre)

    check("filas", m["n_filas"], 8760, 0)
    check("dbt_media", m["dbt_media"], MEDIA, 0.05)
    check("amplitud_ciclo_diurno", m["amplitud_ciclo_diurno"], 2 * AMPLITUD, 0.3)
    check("rango_diario_medio", m["rango_diario_medio"], 2 * AMPLITUD, 0.3)
    # El EPW rotula las horas 1..24, donde la etiqueta h cubre el intervalo que
    # TERMINA a las h:00. El pico de la senoidal cae en 15:00-16:00, o sea "16".
    check("hora_pico", float(m["hora_pico"]), 16.0, 0.0)
    check("ano_centroide", m["ano_centroide"], 2015.5, 0.05)
    # Con temperatura estrictamente periodica, la media diaria es constante:
    # la autocorrelacion no esta definida y debe salir NaN, no un numero falso.
    print(f"  INFO   autocorr_lag1 = {m['autocorr_lag1']} "
          f"(serie diaria constante: NaN es la respuesta correcta)")
    # Grados-hora de enfriamiento base 18 sobre una senoidal de media 20, amp 5.
    # El EPW guarda el bulbo seco con UN decimal. El valor esperado se calcula
    # sobre la serie redondeada, que es lo que el motor lee de vuelta del archivo.
    esperado_gh18 = float(np.sum(np.clip(np.round(dbt, 1) - 18, 0, None)))
    check("gh_enfriamiento_b18", m["gh_enfriamiento_b18"], esperado_gh18, 1.0)
    # Humedad absoluta a 20 C y 70 % HR, 101.325 kPa: ~10.2 g/kg.
    check("w_media_gkg", m["w_media_gkg"], 10.2, 0.6)

    print(f"\nAutotest: {len(fallos)} fallos" +
          (f" -> {fallos}" if fallos else " . Motor validado."))
    return 1 if fallos else 0


# ── main ──────────────────────────────────────────────────────────────────────
def main() -> int:
    raiz = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entrada", type=Path, default=raiz / "Input" / "clima")
    ap.add_argument("--salida", type=Path, default=raiz / "Data" / "metricas_todas_v1.csv")
    ap.add_argument("--forzar", action="store_true",
                    help="recalcula todo, ignora el checkpoint")
    ap.add_argument("--autotest", action="store_true",
                    help="valida el motor sobre un EPW sintetico")
    args = ap.parse_args()

    if args.autotest:
        return autotest()

    print(f"Entrada: {args.entrada}")
    df = recorrer(args.entrada, args.salida, args.forzar)
    if df.empty:
        return 1
    problemas = verificar(df)
    return 0 if problemas == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
