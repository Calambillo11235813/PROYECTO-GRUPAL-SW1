# Backend/codigo/views/historial_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.db import models   # IMPORTANTE
from django.utils import timezone
import datetime
from ..models import AnalisisCodigo
from ..serializers import AnalisisCodigoSerializer


# ===============================
#  HISTORIAL + FILTROS
# ===============================
class HistorialAnalisisView(APIView):

    def get(self, request):
        qs = AnalisisCodigo.objects.all()

        # Filtro por nombre
        nombre = request.GET.get("nombre")
        if nombre:
            qs = qs.filter(nombre_archivo__icontains=nombre)

        # Filtro por lenguaje
        lenguaje = request.GET.get("lenguaje")
        if lenguaje:
            qs = qs.filter(lenguaje__icontains=lenguaje)

        # Filtro por IA / Humano
        es_ia = request.GET.get("ia")
        if es_ia == "true":
            qs = qs.filter(ia_es_generado=True)
        elif es_ia == "false":
            qs = qs.filter(ia_es_generado=False)

        # Filtro por fecha
        fecha_inicio = request.GET.get("inicio")
        fecha_fin = request.GET.get("fin")
        if fecha_inicio and fecha_fin:
            qs = qs.filter(fecha_analisis__range=[fecha_inicio, fecha_fin])

        # Orden descendente
        qs = qs.order_by("-fecha_analisis")

        return Response(AnalisisCodigoSerializer(qs, many=True).data)


# ===============================
#  COMPARADOR SIDE-BY-SIDE
# ===============================
class CompararAnalisisView(APIView):
    """
    Soporta GET (id1,id2) para compatibilidad y POST con JSON { ids: [1,2,...] }.
    Devuelve el payload esperado por el frontend:
    {
      "comparaciones": [ ... ],
      "diferencias": { "confianza": .., "complejidad": .., "predictibilidad": .. }
    }
    """
    def get(self, request):
        # Compatibilidad: acepta id1 e id2 en query params
        id1 = request.GET.get("id1")
        id2 = request.GET.get("id2")

        if not id1 or not id2:
            return Response({"error": "Se requieren id1 e id2"}, 400)

        try:
            a1 = AnalisisCodigo.objects.get(id=id1)
            a2 = AnalisisCodigo.objects.get(id=id2)
        except AnalisisCodigo.DoesNotExist:
            return Response({"error": "Uno de los análisis no existe"}, 404)

        data1 = AnalisisCodigoSerializer(a1).data
        data2 = AnalisisCodigoSerializer(a2).data

        comparaciones = [data1, data2]

        # Calcular diferencias sencillas
        confianza_diff = abs((a1.ia_confianza or 0) - (a2.ia_confianza or 0)) * 100
        complejidad_diff = abs((a1.complejidad_ciclomatica or 0) - (a2.complejidad_ciclomatica or 0))
        predict_diff = abs((a1.indice_predictibilidad or 0) - (a2.indice_predictibilidad or 0)) * 100

        diferencias = {
            "confianza": round(confianza_diff, 1),
            "complejidad": round(complejidad_diff, 2),
            "predictibilidad": round(predict_diff, 1),
        }

        return Response({"comparaciones": comparaciones, "diferencias": diferencias})

    def post(self, request):
        # Espera JSON: { ids: [1,2,...] }
        ids = request.data.get("ids") or request.data.get("ids")
        if not ids or not isinstance(ids, (list, tuple)):
            return Response({"error": "Se requiere 'ids' como lista"}, 400)

        objects = AnalisisCodigo.objects.filter(id__in=ids)
        if not objects.exists():
            return Response({"error": "No se encontraron análisis para los ids proporcionados"}, 404)

        serialized = AnalisisCodigoSerializer(objects.order_by("-fecha_analisis"), many=True).data

        diferencias = {}
        if len(serialized) >= 2:
            # tomar los dos primeros para diferencia
            a = objects.order_by("-fecha_analisis")[0]
            b = objects.order_by("-fecha_analisis")[1]
            confianza_diff = abs((a.ia_confianza or 0) - (b.ia_confianza or 0)) * 100
            complejidad_diff = abs((a.complejidad_ciclomatica or 0) - (b.complejidad_ciclomatica or 0))
            predict_diff = abs((a.indice_predictibilidad or 0) - (b.indice_predictibilidad or 0)) * 100

            diferencias = {
                "confianza": round(confianza_diff, 1),
                "complejidad": round(complejidad_diff, 2),
                "predictibilidad": round(predict_diff, 1),
            }

        return Response({"comparaciones": serialized, "diferencias": diferencias})


# ===============================
#  ESTADÍSTICAS GENERALES
# ===============================
class EstadisticasHistorialView(APIView):
    def get(self, request):
        total = AnalisisCodigo.objects.count()
        ia = AnalisisCodigo.objects.filter(ia_es_generado=True).count()
        humano = AnalisisCodigo.objects.filter(ia_es_generado=False).count()

        # Promedio de complejidad
        complej_media = AnalisisCodigo.objects.aggregate(
            avg=models.Avg("complejidad_ciclomatica")
        )["avg"]

        # Promedio de confianza IA
        promedio_confianza = AnalisisCodigo.objects.aggregate(
            avg=models.Avg("ia_confianza")
        )["avg"] or 0

        # Distribución por lenguaje
        por_lenguaje_qs = AnalisisCodigo.objects.values_list("lenguaje", flat=True)
        por_lenguaje = {}
        for lang in por_lenguaje_qs:
            key = lang or "Unknown"
            por_lenguaje[key] = por_lenguaje.get(key, 0) + 1

        # Últimos 30 días
        now = timezone.now()
        inicio_30 = now - datetime.timedelta(days=30)
        ult_30_qs = AnalisisCodigo.objects.filter(fecha_analisis__gte=inicio_30)
        ult_30_total = ult_30_qs.count()
        ult_30_ia = ult_30_qs.filter(ia_es_generado=True).count()
        ult_30_hum = ult_30_qs.filter(ia_es_generado=False).count()
        ult_30_promedio_conf = ult_30_qs.aggregate(avg=models.Avg("ia_confianza"))["avg"] or 0

        # Métricas promedio adicionales
        metricas_qs = AnalisisCodigo.objects.all()
        metricas_promedio = {
            "complejidad_ciclomatica": round((metricas_qs.aggregate(avg=models.Avg("complejidad_ciclomatica"))["avg"] or 0), 2),
            "indice_predictibilidad": round(((metricas_qs.aggregate(avg=models.Avg("indice_predictibilidad"))["avg"] or 0) * 100), 1),
            "lineas_sospechosas": 0,
        }
        # calcular promedio de lineas_sospechosas (longitudes) si existe
        total_items = metricas_qs.count()
        if total_items:
            suma_lines = 0
            for obj in metricas_qs:
                try:
                    ls = obj.lineas_sospechosas or []
                    suma_lines += len(ls)
                except Exception:
                    suma_lines += 0
            metricas_promedio["lineas_sospechosas"] = round(suma_lines / total_items, 1)

        return Response({
            "total_analisis": total,
            "codigo_ia": ia,
            "codigo_humano": humano,
            "promedio_confianza": round(promedio_confianza * 100, 1),
            "por_lenguaje": por_lenguaje,
            "ultimos_30_dias": {
                "total": ult_30_total,
                "ia": ult_30_ia,
                "humano": ult_30_hum,
                "promedio_confianza": round(ult_30_promedio_conf * 100, 1),
            },
            "metricas_promedio": metricas_promedio,
        })


# ===============================
#  EXPORTAR HISTORIAL COMPLETO
# ===============================
class ExportarHistorialJSONView(APIView):
    def get(self, request):
        data = AnalisisCodigoSerializer(
            AnalisisCodigo.objects.all().order_by("-fecha_analisis"),
            many=True
        ).data

        return Response({
            "exportado": True,
            "total": len(data),
            "data": data
        })
