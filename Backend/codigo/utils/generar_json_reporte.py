# Backend/codigo/utils/generar_json_reporte.py
import json
from datetime import datetime

def generar_json_reporte(obj):
    data = {
        "archivo": obj.nombre_archivo,
        "fecha_analisis": obj.fecha_analisis.strftime("%Y-%m-%d %H:%M:%S"),

        "modelo": {
            "es_ia": obj.ia_es_generado,
            "confianza": obj.ia_confianza,
            "metodo": obj.ia_metodo,
            "detalles": obj.ia_detalles,
            "version_modelo": obj.version_modelo,
            "timestamp_modelo": str(obj.timestamp_modelo) if obj.timestamp_modelo else None
        },

        "analisis_sintactico": {
            "complejidad_ciclomatica": obj.complejidad_ciclomatica,
            "variabilidad_funciones": obj.variabilidad_funciones,
            "patrones_control": obj.patrones_control,
            "patrones_comunes": obj.patrones_comunes,
            "idiosincrasias": obj.idiosincrasias,
            "indice_predictibilidad": obj.indice_predictibilidad,
        },

        "deteccion_lineas": {
            "lineas_sospechosas": obj.lineas_sospechosas,
            "bloques_sospechosos": obj.bloques_sospechosos,
        },

        "ast_fragmento": str(obj.ast_json)[:2000]
    }

    return data
