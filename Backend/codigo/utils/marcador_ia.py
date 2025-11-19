# Backend/codigo/utils/marcador_ia.py
from ..modelos.production_code_detector import get_detector

def marcar_lineas_sospechosas(codigo_texto: str, tam_bloque=8, umbral=0.70):
    """
    Divide el código en bloques y detecta cuáles son generados por IA.
    Retorna:
    - lineas_sospechosas: lista de números de líneas
    - bloques_sospechosos: lista con {inicio, fin, score}
    """

    lineas = codigo_texto.splitlines()
    total = len(lineas)

    bloques_sospechosos = []
    lineas_sospechosas = []

    inicio = 0

    while inicio < total:
        fin = min(inicio + tam_bloque, total)
        bloque = "\n".join(lineas[inicio:fin])

        # IA real por bloque (robusto con fallback)
        try:
            resultado = get_detector().analizar(bloque)
            score = float(resultado.get("confidence", 0.0))
        except Exception:
            # Nunca fallar el marcado por ausencia/errores del modelo
            score = 0.0

        if score >= umbral:
            bloques_sospechosos.append({
                "inicio": inicio + 1,
                "fin": fin,
                "score": round(score, 3)
            })

            # Todas las líneas del bloque
            for i in range(inicio + 1, fin + 1):
                lineas_sospechosas.append(i)

        inicio += tam_bloque

    lineas_sospechosas = sorted(list(set(lineas_sospechosas)))
    return lineas_sospechosas, bloques_sospechosos
