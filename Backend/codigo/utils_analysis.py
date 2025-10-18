import ast
import radon.complexity as cc
import statistics
import re
import math

def analizar_codigo(ruta):
    with open(ruta, 'r', encoding='utf8') as f:
        codigo = f.read()

    # --- AST
    try:
        tree = ast.parse(codigo)
    except SyntaxError as e:
        return {
            'error': f"Error de sintaxis: {e}",
            'ast': None,
            'complejidad': 0,
            'naming_score': 0,
            'repetitividad': 0,
            'predict_score': 0,
            'tipo_codigo': 'Desconocido'
        }

    # --- 1️⃣ Complejidad ciclomatica promedio
    complejidades = [b.complexity for b in cc.cc_visit(codigo)]
    complejidad_media = round(statistics.mean(complejidades), 2) if complejidades else 0

    # --- 2️⃣ Métricas de estilo (snake_case vs camelCase)
    nombres = re.findall(r'\bdef ([a-zA-Z_][a-zA-Z0-9_]*)', codigo)
    camel = sum(1 for n in nombres if re.match(r'[a-z]+[A-Z]', n))
    snake = sum(1 for n in nombres if '_' in n)
    naming_score = round((snake / max(1, len(nombres))) * 100, 2)

    # --- 3️⃣ Patrones repetitivos
    lineas = codigo.splitlines()
    repetidas = [l for l in set(lineas) if lineas.count(l) > 2 and len(l.strip()) > 4]
    repetitividad = round(len(repetidas) / max(1, len(lineas)) * 100, 2)

    # --- 4️⃣ “Predict Score” heurístico
    predict_score = round(1 - (abs(naming_score - 50) / 100 + repetitividad / 200 + complejidad_media / 200), 2)
    predict_score = max(0, min(1, predict_score))

    return {
        'ast': ast.dump(tree, indent=2),
        'complejidad': complejidad_media,
        'naming_score': naming_score,
        'repetitividad': repetitividad,
        'predict_score': predict_score,
        'tipo_codigo': 'IA' if predict_score < 0.45 else 'Humano',
    }
