# Backend/codigo/views/historial_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.db import models   # IMPORTANTE
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
    def get(self, request):
        id1 = request.GET.get("id1")
        id2 = request.GET.get("id2")

        if not id1 or not id2:
            return Response({"error": "Se requieren id1 e id2"}, 400)

        try:
            a1 = AnalisisCodigo.objects.get(id=id1)
            a2 = AnalisisCodigo.objects.get(id=id2)
        except AnalisisCodigo.DoesNotExist:
            return Response({"error": "Uno de los análisis no existe"}, 404)

        return Response({
            "archivo_1": AnalisisCodigoSerializer(a1).data,
            "archivo_2": AnalisisCodigoSerializer(a2).data
        })


# ===============================
#  ESTADÍSTICAS GENERALES
# ===============================
class EstadisticasHistorialView(APIView):
    def get(self, request):

        total = AnalisisCodigo.objects.count()
        ia = AnalisisCodigo.objects.filter(ia_es_generado=True).count()
        humano = AnalisisCodigo.objects.filter(ia_es_generado=False).count()

        complej_media = AnalisisCodigo.objects.aggregate(
            avg=models.Avg("complejidad_ciclomatica")
        )["avg"]

        return Response({
            "total_analisis": total,
            "generados_por_ia": ia,
            "humanos": humano,
            "complejidad_promedio": round(complej_media or 0, 2),
            "porcentaje_ia": round((ia / total) * 100, 2) if total else 0,
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
