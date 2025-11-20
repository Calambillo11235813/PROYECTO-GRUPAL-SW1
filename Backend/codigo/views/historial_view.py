# Backend/codigo/views/historial_view.py
import logging
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.db import models
from django.utils import timezone
from ..models import AnalisisCodigo
from ..serializers import AnalisisCodigoSerializer

logger = logging.getLogger(__name__)


class AnalisisPagination(PageNumberPagination):
    """Paginación para listados de análisis"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# ===============================
#  HISTORIAL + FILTROS
# ===============================
class HistorialAnalisisView(APIView):
    pagination_class = AnalisisPagination

    def get(self, request):
        """
        Lista análisis con filtros opcionales.
        Usuarios autenticados solo ven sus propios análisis (excepto staff).
        """
        try:
            # Filtrar por usuario si está autenticado
            if request.user.is_authenticated:
                if request.user.is_staff:
                    # Staff puede ver todos
                    qs = AnalisisCodigo.objects.all()
                else:
                    # Usuarios normales solo ven sus propios análisis
                    qs = AnalisisCodigo.objects.filter(usuario=request.user)
            else:
                # Usuarios anónimos solo ven análisis sin usuario
                qs = AnalisisCodigo.objects.filter(usuario__isnull=True)

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

            # Filtro por fecha con validación
            fecha_inicio = request.GET.get("inicio")
            fecha_fin = request.GET.get("fin")
            if fecha_inicio and fecha_fin:
                try:
                    # Validar formato de fecha (YYYY-MM-DD)
                    datetime.strptime(fecha_inicio, "%Y-%m-%d")
                    datetime.strptime(fecha_fin, "%Y-%m-%d")
                    qs = qs.filter(fecha_analisis__date__range=[fecha_inicio, fecha_fin])
                except ValueError:
                    return Response(
                        {"error": "Formato de fecha inválido. Use YYYY-MM-DD"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Orden descendente
            qs = qs.order_by("-fecha_analisis")

            # Paginación
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(qs, request)
            if page is not None:
                serializer = AnalisisCodigoSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            serializer = AnalisisCodigoSerializer(qs, many=True)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error en HistorialAnalisisView: {e}", exc_info=True)
            return Response(
                {"error": "Error al obtener el historial"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
            return Response(
                {"error": "Se requieren id1 e id2 como parámetros de consulta"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Validar que sean números
            id1 = int(id1)
            id2 = int(id2)
        except ValueError:
            return Response(
                {"error": "Los IDs deben ser números válidos"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Filtrar por usuario si está autenticado
            if request.user.is_authenticated and not request.user.is_staff:
                a1 = AnalisisCodigo.objects.get(id=id1, usuario=request.user)
                a2 = AnalisisCodigo.objects.get(id=id2, usuario=request.user)
            else:
                a1 = AnalisisCodigo.objects.get(id=id1)
                a2 = AnalisisCodigo.objects.get(id=id2)
        except AnalisisCodigo.DoesNotExist:
            return Response(
                {"error": "Uno de los análisis no existe o no tienes permiso para verlo"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error al comparar análisis: {e}")
            return Response(
                {"error": "Error al obtener los análisis para comparar"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
        ids = request.data.get("ids")
        if not ids or not isinstance(ids, (list, tuple)):
            return Response(
                {"error": "Se requiere 'ids' como lista en el cuerpo de la petición"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar que todos los IDs sean números
        try:
            ids = [int(id_val) for id_val in ids]
        except (ValueError, TypeError):
            return Response(
                {"error": "Todos los IDs deben ser números válidos"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filtrar por usuario si está autenticado
        if request.user.is_authenticated and not request.user.is_staff:
            objects = AnalisisCodigo.objects.filter(id__in=ids, usuario=request.user)
        else:
            objects = AnalisisCodigo.objects.filter(id__in=ids)

        if not objects.exists():
            return Response(
                {"error": "No se encontraron análisis para los ids proporcionados o no tienes permiso para verlos"},
                status=status.HTTP_404_NOT_FOUND
            )

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
        """
        Estadísticas generales del historial.
        Usuarios autenticados solo ven estadísticas de sus propios análisis.
        """
        try:
            # Filtrar por usuario si está autenticado
            if request.user.is_authenticated:
                if request.user.is_staff:
                    base_qs = AnalisisCodigo.objects.all()
                else:
                    base_qs = AnalisisCodigo.objects.filter(usuario=request.user)
            else:
                base_qs = AnalisisCodigo.objects.filter(usuario__isnull=True)

            total = base_qs.count()
            ia = base_qs.filter(ia_es_generado=True).count()
            humano = base_qs.filter(ia_es_generado=False).count()

            # Promedio de complejidad
            complej_media = base_qs.aggregate(
                avg=models.Avg("complejidad_ciclomatica")
            )["avg"]

            # Promedio de confianza IA
            promedio_confianza = base_qs.aggregate(
                avg=models.Avg("ia_confianza")
            )["avg"] or 0

            # Distribución por lenguaje
            por_lenguaje_qs = base_qs.values_list("lenguaje", flat=True)
            por_lenguaje = {}
            for lang in por_lenguaje_qs:
                key = lang or "Unknown"
                por_lenguaje[key] = por_lenguaje.get(key, 0) + 1

            # Últimos 30 días
            now = timezone.now()
            inicio_30 = now - datetime.timedelta(days=30)
            ult_30_qs = base_qs.filter(fecha_analisis__gte=inicio_30)
            ult_30_total = ult_30_qs.count()
            ult_30_ia = ult_30_qs.filter(ia_es_generado=True).count()
            ult_30_hum = ult_30_qs.filter(ia_es_generado=False).count()
            ult_30_promedio_conf = ult_30_qs.aggregate(avg=models.Avg("ia_confianza"))["avg"] or 0

            # Métricas promedio adicionales
            metricas_qs = base_qs
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

        except Exception as e:
            logger.error(f"Error en EstadisticasHistorialView: {e}", exc_info=True)
            return Response(
                {"error": "Error al obtener las estadísticas"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ===============================
#  EXPORTAR HISTORIAL COMPLETO
# ===============================
class ExportarHistorialJSONView(APIView):
    def get(self, request):
        """
        Exporta el historial completo en formato JSON.
        Usuarios autenticados solo exportan sus propios análisis.
        """
        try:
            # Filtrar por usuario si está autenticado
            if request.user.is_authenticated:
                if request.user.is_staff:
                    qs = AnalisisCodigo.objects.all()
                else:
                    qs = AnalisisCodigo.objects.filter(usuario=request.user)
            else:
                qs = AnalisisCodigo.objects.filter(usuario__isnull=True)

            data = AnalisisCodigoSerializer(
                qs.order_by("-fecha_analisis"),
                many=True
            ).data

            return Response({
                "exportado": True,
                "total": len(data),
                "data": data
            })

        except Exception as e:
            logger.error(f"Error en ExportarHistorialJSONView: {e}", exc_info=True)
            return Response(
                {"error": "Error al exportar el historial"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ===============================
#  ELIMINAR HISTORIAL
# ===============================
class EliminarHistorialView(APIView):
    def delete(self, request):
        """
        Elimina todo el historial del usuario autenticado.
        Staff puede eliminar todo el historial si se especifica 'todos=true' en query params.
        """
        try:
            # Verificar si el usuario quiere eliminar todo (solo para staff)
            eliminar_todos = request.GET.get("todos", "false").lower() == "true"
            
            if request.user.is_authenticated:
                if request.user.is_staff and eliminar_todos:
                    # Staff puede eliminar todo el historial
                    qs = AnalisisCodigo.objects.all()
                    total = qs.count()
                    
                    # Eliminar archivos físicos antes de eliminar registros
                    for obj in qs:
                        try:
                            if obj.archivo:
                                obj.archivo.delete(save=False)
                        except Exception as e:
                            logger.warning(f"Error al eliminar archivo {obj.archivo.path}: {e}")
                    
                    qs.delete()
                    
                    logger.info(f"Staff {request.user.username} eliminó todo el historial ({total} análisis)")
                    return Response({
                        "mensaje": f"Se eliminaron {total} análisis del historial completo",
                        "total_eliminados": total
                    }, status=status.HTTP_200_OK)
                else:
                    # Usuario normal solo elimina sus propios análisis
                    qs = AnalisisCodigo.objects.filter(usuario=request.user)
                    total = qs.count()
                    
                    # Eliminar archivos físicos antes de eliminar registros
                    for obj in qs:
                        try:
                            if obj.archivo:
                                obj.archivo.delete(save=False)
                        except Exception as e:
                            logger.warning(f"Error al eliminar archivo {obj.archivo.path}: {e}")
                    
                    qs.delete()
                    
                    logger.info(f"Usuario {request.user.username} eliminó su historial ({total} análisis)")
                    return Response({
                        "mensaje": f"Se eliminaron {total} análisis de tu historial",
                        "total_eliminados": total
                    }, status=status.HTTP_200_OK)
            else:
                # Usuarios anónimos solo pueden eliminar análisis sin usuario
                qs = AnalisisCodigo.objects.filter(usuario__isnull=True)
                total = qs.count()
                
                # Eliminar archivos físicos antes de eliminar registros
                for obj in qs:
                    try:
                        if obj.archivo:
                            obj.archivo.delete(save=False)
                    except Exception as e:
                        logger.warning(f"Error al eliminar archivo {obj.archivo.path}: {e}")
                
                qs.delete()
                
                return Response({
                    "mensaje": f"Se eliminaron {total} análisis sin usuario",
                    "total_eliminados": total
                }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error en EliminarHistorialView: {e}", exc_info=True)
            return Response(
                {"error": "Error al eliminar el historial"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
