# Backend/codigo/utils/analizador_codigo.py
import ast
import radon.complexity as cc
import statistics
import re

def analizar_archivo_codigo(ruta):
    with open(ruta, "r", encoding="utf8") as f:
        codigo = f.read()

    try:
        tree = ast.parse(codigo)
        ast_json = ast.dump(tree, indent=2)
    except:
        return {
            "ast": None,
            "complejidad": 0,
            "variabilidad": 0,
            "patrones_control": {},
            "patrones_comunes": {},
            "idiosincrasias": {},
            "predict": 0,
        }

    # Complejidad ciclomática
    bloques = cc.cc_visit(codigo)
    comp_list = [b.complexity for b in bloques]
    complej = round(statistics.mean(comp_list), 2) if comp_list else 0

    # Variabilidad (HU-014)
    longitudes = [len(n.splitlines()) for n in codigo.split("\n\n")]
    variabilidad = round(statistics.pvariance(longitudes), 2) if len(longitudes) > 2 else 0

    # Patrones de control (HU-014)
    patrones_control = {
        "ifs": codigo.count("if "),
        "loops": codigo.count("for ") + codigo.count("while "),
        "trys": codigo.count("try:"),
    }

    # Patrones comunes (HU-014)
        # palabras repetidas
    palabras = re.findall(r"[a-zA-Z_]{3,}", codigo)
    comunes = {}
    for p in palabras:
        comunes[p] = comunes.get(p, 0) + 1
    comunes = {k: v for k, v in comunes.items() if v > 2}

    # Idiosincrasias
    idio = {
        "snake_case": len(re.findall(r"[a-z_]+", codigo)),
        "camelCase": len(re.findall(r"[a-z]+[A-Z][a-z]+", codigo)),
    }

    # Predictibilidad
    predict = round(
        1 - ((complej / 100) + (variabilidad / 200) + (len(comunes) / 300)),
        3
    )
    predict = max(0, min(1, predict))

    return {
        "ast": ast_json,
        "complejidad": complej,
        "variabilidad": variabilidad,
        "patrones_control": patrones_control,
        "patrones_comunes": comunes,
        "idiosincrasias": idio,
        "predict": predict,
    }
