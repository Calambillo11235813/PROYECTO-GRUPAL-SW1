from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
from .predictor import get_predictor
from .models import AnalisisTexto, ArchivoAnalisis
from .file_processor import FileProcessor
import hashlib

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

@csrf_exempt
@require_http_methods(["POST"])
def comparar_modelos(request):
    """
    Endpoint para comparar la predicción de ambos modelos en el mismo texto.
    
    Parámetros esperados (JSON):
    - texto: String con el texto a analizar
    
    Respuesta (JSON):
    - texto_analizado: Texto que se analizó
    - modelo_N: Resultado del modelo principal
    - modelo_B: Resultado del modelo experimental
    - diferencia_probabilidad: Diferencia entre las predicciones
    - consenso: Si ambos modelos coinciden en la predicción
    """
    try:
        # Parsear el cuerpo de la solicitud
        data = json.loads(request.body)
        texto = data.get('texto', '')
        
        if not texto:
            return JsonResponse({
                'error': 'El texto no puede estar vacío'
            }, status=400)
        
        # Obtener predictores de ambos modelos
        predictor_N = get_predictor('N')
        predictor_B = get_predictor('B')
        
        # Realizar predicciones con ambos modelos
        resultado_N = predictor_N.predict(texto)
        resultado_B = predictor_B.predict(texto)
        
        # Verificar si hubo errores
        if 'error' in resultado_N:
            return JsonResponse({'error': f'Error modelo N: {resultado_N["error"]}'}, status=500)
        if 'error' in resultado_B:
            return JsonResponse({'error': f'Error modelo B: {resultado_B["error"]}'}, status=500)
        
        # Calcular diferencias y consenso
        diff_probabilidad = abs(resultado_N['probabilidad_ia'] - resultado_B['probabilidad_ia'])
        consenso = resultado_N['prediccion'] == resultado_B['prediccion']
        
        # Almacenar análisis comparativo en la base de datos
        try:
            analisis = AnalisisTexto(
                texto=texto[:500],
                resultado_prediccion=f"N:{resultado_N['prediccion']}, B:{resultado_B['prediccion']}",
                probabilidad_ia=(resultado_N['probabilidad_ia'] + resultado_B['probabilidad_ia']) / 2,
                probabilidad_humano=(resultado_N['probabilidad_humano'] + resultado_B['probabilidad_humano']) / 2,
            )
            analisis.save()
        except Exception as e:
            logger.error(f"Error al guardar el análisis comparativo: {str(e)}")
            # No retornar error aquí, solo loguearlo
        
        # Preparar respuesta comparativa
        response_data = {
            'texto_analizado': texto[:100] + "..." if len(texto) > 100 else texto,
            'modelo_N': resultado_N,
            'modelo_B': resultado_B,
            'diferencia_probabilidad': round(diff_probabilidad, 2),
            'consenso': consenso,
            'recomendacion': (
                'Alta confianza' if consenso and diff_probabilidad < 10 
                else 'Revisar manualmente' if not consenso 
                else 'Confianza media'
            ),
            'timestamp': json.loads(json.dumps({}))  # Para timestamp si es necesario
        }
        
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Formato JSON inválido'}, status=400)
    except Exception as e:
        logger.error(f"Error en comparar_modelos: {str(e)}")
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def analizar_texto_con_modelo(request):
    """
    Endpoint para analizar un texto con un modelo específico.
    
    Parámetros esperados (JSON):
    - texto: String con el texto a analizar
    - modelo: 'N' o 'B' (opcional, por defecto 'N')
    """
    try:
        # Parsear el cuerpo de la solicitud
        data = json.loads(request.body)
        texto = data.get('texto', '')
        modelo_tipo = data.get('modelo', 'N')
        
        if not texto:
            return JsonResponse({
                'error': 'El texto no puede estar vacío'
            }, status=400)
            
        if modelo_tipo not in ['N', 'B']:
            return JsonResponse({
                'error': 'Tipo de modelo debe ser "N" o "B"'
            }, status=400)
        
        # Obtener predictor específico
        predictor = get_predictor(modelo_tipo)
        resultado = predictor.predict(texto)
        
        # Verificar si hubo error en la predicción
        if 'error' in resultado:
            return JsonResponse({'error': resultado['error']}, status=500)
        
        # Almacenar el análisis en la base de datos
        analisis = AnalisisTexto(
            texto=texto[:500],
            resultado_prediccion=f"{modelo_tipo}:{resultado['prediccion']}",
            probabilidad_ia=resultado['probabilidad_ia'],
            probabilidad_humano=resultado['probabilidad_humano'],
        )
        analisis.save()
        
        # Devolver resultado
        return JsonResponse(resultado)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Formato JSON inválido'}, status=400)
    except Exception as e:
        logger.error(f"Error en analizar_texto_con_modelo: {str(e)}")
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

@require_http_methods(["GET"])
def info_modelos(request):
    """
    Endpoint para obtener información sobre los modelos disponibles.
    """
    try:
        from .predictor import get_available_models
        
        modelos_info = {}
        for model_type in get_available_models():
            try:
                predictor = get_predictor(model_type)
                modelos_info[model_type] = predictor.get_model_info()
            except Exception as e:
                modelos_info[model_type] = {'error': str(e)}
        
        return JsonResponse({
            'modelos_disponibles': modelos_info,
            'modelo_por_defecto': 'N'
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Error al obtener información de modelos: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def analizar_archivo(request):
    """Analiza archivos TXT, PDF, DOCX para detectar contenido generado por IA"""
    try:
        # Verificar que se subió un archivo
        if 'archivo' not in request.FILES:
            return JsonResponse({
                'error': 'No se encontró ningún archivo',
                'codigo': 'ARCHIVO_FALTANTE'
            }, status=400)
        
        archivo = request.FILES['archivo']
        modelo_seleccionado = request.POST.get('modelo', 'B')
        
        # Validar archivo
        es_valido, mensaje = FileProcessor.validate_file(archivo)
        if not es_valido:
            return JsonResponse({
                'error': mensaje,
                'codigo': 'ARCHIVO_INVALIDO'
            }, status=400)
        
        # Extraer texto del archivo
        exito, texto_extraido = FileProcessor.extract_text(archivo)
        if not exito:
            return JsonResponse({
                'error': texto_extraido,
                'codigo': 'ERROR_EXTRACCION'
            }, status=400)
        
        # Validar que el texto extraído no esté vacío
        if not texto_extraido or len(texto_extraido.strip()) < 10:
            return JsonResponse({
                'error': 'El archivo no contiene suficiente texto para analizar (mínimo 10 caracteres)',
                'codigo': 'TEXTO_INSUFICIENTE'
            }, status=400)
        
        # Limitar longitud del texto
        if len(texto_extraido) > 10000:
            texto_extraido = texto_extraido[:10000] + "..."
        
        # Realizar predicción
        predictor = get_predictor(modelo_seleccionado)
        resultado_dict = predictor.predict(texto_extraido)  # CORREGIDO: cambio de predecir a predict
        
        # Verificar si hubo error en la predicción
        if 'error' in resultado_dict:
            return JsonResponse({
                'error': resultado_dict['error'],
                'codigo': 'ERROR_PREDICCION'
            }, status=500)
        
        # Extraer valores del diccionario
        resultado = resultado_dict['prediccion']
        probabilidad_ia = resultado_dict['probabilidad_ia']
        probabilidad_humano = resultado_dict['probabilidad_humano']
        
        # Calcular hash del archivo
        archivo.seek(0)
        file_hash = hashlib.sha256(archivo.read()).hexdigest()
        archivo.seek(0)
        
        # Obtener información del archivo
        file_extension = archivo.name.split('.')[-1].lower()
        
        # Guardar análisis en base de datos
        analisis = AnalisisTexto.objects.create(
            texto=texto_extraido,
            resultado_prediccion=resultado,
            probabilidad_ia=probabilidad_ia,
            probabilidad_humano=probabilidad_humano,
            tipo_entrada='ARCHIVO',
            nombre_archivo=archivo.name,
            tamano_archivo=archivo.size,
            tipo_archivo=f'.{file_extension}'
        )
        
        # Guardar información adicional del archivo
        ArchivoAnalisis.objects.create(
            analisis=analisis,
            hash_archivo=file_hash
        )
        
        return JsonResponse({
            'resultado': resultado,
            'probabilidad_ia': round(probabilidad_ia, 4),
            'probabilidad_humano': round(probabilidad_humano, 4),
            'archivo_info': {
                'nombre': archivo.name,
                'tamano': archivo.size,
                'tipo': f'.{file_extension}',
                'texto_extraido_preview': texto_extraido[:200] + "..." if len(texto_extraido) > 200 else texto_extraido
            },
            'analisis_id': analisis.id,
            'modelo_utilizado': modelo_seleccionado,
            'fecha_analisis': analisis.fecha_analisis.isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error en analizar_archivo: {str(e)}")
        return JsonResponse({
            'error': f'Error interno del servidor: {str(e)}',
            'codigo': 'ERROR_INTERNO'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def comparar_modelos_archivo(request):
    """Compara ambos modelos usando un archivo subido"""
    try:
        if 'archivo' not in request.FILES:
            return JsonResponse({
                'error': 'No se encontró ningún archivo',
                'codigo': 'ARCHIVO_FALTANTE'
            }, status=400)
        
        archivo = request.FILES['archivo']
        
        # Validar archivo
        es_valido, mensaje = FileProcessor.validate_file(archivo)
        if not es_valido:
            return JsonResponse({
                'error': mensaje,
                'codigo': 'ARCHIVO_INVALIDO'
            }, status=400)
        
        # Extraer texto
        exito, texto_extraido = FileProcessor.extract_text(archivo)
        if not exito:
            return JsonResponse({
                'error': texto_extraido,
                'codigo': 'ERROR_EXTRACCION'
            }, status=400)
        
        # Limitar longitud
        if len(texto_extraido) > 10000:
            texto_extraido = texto_extraido[:10000] + "..."
        
        # Realizar predicción con ambos modelos
        predictor_b = get_predictor('B')
        predictor_n = get_predictor('N')
        
        resultado_dict_b = predictor_b.predict(texto_extraido)  # CORREGIDO: cambio de predecir a predict
        resultado_dict_n = predictor_n.predict(texto_extraido)  # CORREGIDO: cambio de predecir a predict
        
        # Verificar errores
        if 'error' in resultado_dict_b:
            return JsonResponse({
                'error': f'Error modelo B: {resultado_dict_b["error"]}',
                'codigo': 'ERROR_PREDICCION_B'
            }, status=500)
            
        if 'error' in resultado_dict_n:
            return JsonResponse({
                'error': f'Error modelo N: {resultado_dict_n["error"]}',
                'codigo': 'ERROR_PREDICCION_N'
            }, status=500)
        
        # Extraer valores de los diccionarios
        resultado_b = resultado_dict_b['prediccion']
        prob_ia_b = resultado_dict_b['probabilidad_ia']
        prob_humano_b = resultado_dict_b['probabilidad_humano']
        
        resultado_n = resultado_dict_n['prediccion']
        prob_ia_n = resultado_dict_n['probabilidad_ia']
        prob_humano_n = resultado_dict_n['probabilidad_humano']
        
        return JsonResponse({
            'archivo_info': {
                'nombre': archivo.name,
                'tamano': archivo.size,
                'tipo': archivo.name.split('.')[-1].lower()
            },
            'modelo_b': {
                'resultado': resultado_b,
                'probabilidad_ia': round(prob_ia_b, 4),
                'probabilidad_humano': round(prob_humano_b, 4)
            },
            'modelo_n': {
                'resultado': resultado_n,
                'probabilidad_ia': round(prob_ia_n, 4),
                'probabilidad_humano': round(prob_humano_n, 4)
            },
            'consenso': resultado_b if resultado_b == resultado_n else 'DISCREPANCIA',
            'texto_preview': texto_extraido[:200] + "..." if len(texto_extraido) > 200 else texto_extraido
        })
        
    except Exception as e:
        logger.error(f"Error en comparar_modelos_archivo: {str(e)}")
        return JsonResponse({
            'error': f'Error interno del servidor: {str(e)}',
            'codigo': 'ERROR_INTERNO'
        }, status=500)
