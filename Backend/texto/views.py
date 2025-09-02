from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
from .predictor import get_predictor
from .models import AnalisisTexto

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def analizar_texto(request):
    """
    Endpoint para analizar un texto y determinar si fue generado por IA o por un humano.
    
    Parámetros esperados (JSON):
    - texto: String con el texto a analizar
    
    Respuesta (JSON):
    - prediccion: "IA" o "Humano"
    - probabilidad_ia: Porcentaje de probabilidad de que sea IA
    - probabilidad_humano: Porcentaje de probabilidad de que sea humano
    - confianza: Nivel de confianza general de la predicción
    """
    try:
        # Parsear el cuerpo de la solicitud
        data = json.loads(request.body)
        texto = data.get('texto', '')
        
        if not texto:
            return JsonResponse({
                'error': 'El texto no puede estar vacío'
            }, status=400)
        
        # Obtener predictor y realizar predicción
        predictor = get_predictor()
        resultado = predictor.predict(texto)
        
        # Verificar si hubo error en la predicción
        if 'error' in resultado:
            return JsonResponse({'error': resultado['error']}, status=500)
        
        # Almacenar el análisis en la base de datos
        analisis = AnalisisTexto(
            texto=texto[:500],  # Almacenar solo los primeros 500 caracteres para evitar datos excesivos
            resultado_prediccion=resultado['prediccion'],
            probabilidad_ia=resultado['probabilidad_ia'],
            probabilidad_humano=resultado['probabilidad_humano'],
            # usuario se asignaría si el sistema tiene autenticación
        )
        analisis.save()
        
        # Devolver resultado
        return JsonResponse(resultado)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Formato JSON inválido'}, status=400)
    except Exception as e:
        logger.error(f"Error en analizar_texto: {str(e)}")
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

@require_http_methods(["GET"])
def estado_servicio(request):
    """
    Endpoint para verificar si el servicio de análisis está funcionando.
    """
    try:
        # Intentar obtener el predictor para verificar que el modelo esté cargado
        predictor = get_predictor()
        return JsonResponse({
            'estado': 'online',
            'mensaje': 'El servicio de análisis de texto está funcionando correctamente',
            'modelo': 'BERT multilingüe'
        })
    except Exception as e:
        return JsonResponse({
            'estado': 'error',
            'mensaje': f'El servicio está experimentando problemas: {str(e)}'
        }, status=500)
