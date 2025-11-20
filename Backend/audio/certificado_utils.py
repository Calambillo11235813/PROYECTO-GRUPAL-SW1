from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.conf import settings
import os
from datetime import datetime

# --- LÓGICA DE DECISIÓN (Consistente con React) ---
def _determinar_resultado_final(result_label: str, probability: float) -> tuple[str, str, float]:
    """
    Normaliza la etiqueta del resultado y calcula la confianza.
    Retorna (etiqueta_final, color_tag, confianza_string).
    """
    
    # Asegurar que probability esté en el rango [0, 1] y se convierta a porcentaje [0, 100]
    prob_normalized = probability
    if prob_normalized > 1.0:
        prob_percentage = round(prob_normalized, 2)
    else:
        prob_percentage = round(prob_normalized * 100, 2)

    label = (result_label or '').lower()
    
    # Decisión: Es IA si la etiqueta es 'ai', 'fake', o si la probabilidad de IA es > 50%
    es_ia = label in ('ai', 'fake') or prob_percentage > 50.0

    if es_ia:
        resultado_string = "MANIPULADO CON IA"
        color_tag = 'red'
        # Usamos la probabilidad de ser IA/Fake
        confianza = f"{prob_percentage:.2f}% (IA)"
    else:
        resultado_string = "AUTÉNTICO (HUMANO)"
        color_tag = 'green'
        # Usamos la probabilidad de ser real/humano (100 - probabilidad IA)
        # Nota: Asumimos que la probabilidad dada es la de ser "fake" o "ai".
        confianza = f"{100 - prob_percentage:.2f}% (Humano)"
        
    return resultado_string, color_tag, confianza

# --- GENERADOR DE CERTIFICADO ---
def generar_certificado_pdf(audio_upload):
    """
    Genera un certificado PDF con los resultados del análisis de autenticidad del audio.
    """
    # Crear un buffer para el PDF
    buffer = BytesIO()
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=72
    )
    
    # Estilos base
    styles = getSampleStyleSheet()
    
    # Estilos personalizados para el certificado
    # Titulo principal (20pt)
    styles.add(ParagraphStyle(
        name='CustomTitle', 
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=30,
        fontName='Helvetica-Bold'
    ))
    # Títulos de sección (16pt) - Renombrado para claridad
    styles.add(ParagraphStyle(
        name='CustomSectionHeader',
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=15,
        fontName='Helvetica-Bold'
    ))
    # Texto del cuerpo (12pt)
    styles.add(ParagraphStyle(
        name='CustomBodyText',
        fontSize=12,
        leading=16,
        spaceAfter=10,
        alignment=TA_LEFT
    ))
    # Pie de página (9pt)
    styles.add(ParagraphStyle(
        name='CustomFooter',
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceBefore=30
    ))
    
    # --- PROCESAR DATOS DE AUDIO ---
    created_at = audio_upload.created_at.strftime('%d/%m/%Y %H:%M:%S') if audio_upload.created_at else "N/A"
    
    resultado_str, color_tag, confianza_str = _determinar_resultado_final(
        audio_upload.result, 
        audio_upload.probability or 0
    )
    
    color_resultado = colors.red if color_tag == 'red' else colors.green
    
    # Contenido del PDF
    elements = []
    
    # 1. Encabezado y Título (Solo el título principal)
    combined_title_text = "INFORME DE AUTENTICIDAD DE AUDIO"
    elements.append(Paragraph(combined_title_text, styles['CustomTitle']))
    elements.append(Spacer(1, 20))
    
    # 2. Detalles del Archivo (Usando CustomBodyText)
    elements.append(Paragraph(f"<b>Detalles del Archivo:</b>", styles['CustomBodyText']))
    elements.append(Paragraph(f"<b>Nombre:</b> {audio_upload.original_filename}", styles['CustomBodyText']))
    elements.append(Paragraph(f"<b>ID de Referencia:</b> {audio_upload.id}", styles['CustomBodyText']))
    elements.append(Paragraph(f"<b>Fecha de Análisis:</b> {created_at}", styles['CustomBodyText']))
    elements.append(Spacer(1, 25))
    
    # 3. Resultado Principal (Tabla) (Usando CustomSectionHeader y CustomBodyText)
    elements.append(Paragraph("CONCLUSIÓN DEL ANÁLISIS", styles['CustomSectionHeader']))

    data = [
        [
            Paragraph("<b>PARÁMETRO</b>", styles['CustomBodyText']), 
            Paragraph("<b>RESULTADO</b>", styles['CustomBodyText'])
        ],
        [
            Paragraph("Estado de Autenticidad:", styles['CustomBodyText']), 
            Paragraph(f"<font color='{color_tag}'>{resultado_str}</font>", styles['CustomBodyText'])
        ],
        [
            Paragraph("Nivel de Confianza:", styles['CustomBodyText']), 
            Paragraph(f"<font color='{color_tag}'>{confianza_str}</font>", styles['CustomBodyText'])
        ]
    ]
    
    table = Table(data, colWidths=[2.5 * inch, 3.5 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(red=0.8, green=0.8, blue=0.8)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        
        # Aplicar el color de resultado a las filas 1 y 2 de la columna 1
        ('TEXTCOLOR', (1, 1), (1, 1), color_resultado),
        ('TEXTCOLOR', (1, 2), (1, 2), color_resultado),
        ('FONTNAME', (1, 1), (1, 2), 'Helvetica-Bold'),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 30))
    
    # 4. Interpretación del Resultado (Usando CustomSectionHeader y CustomBodyText)
    elements.append(Paragraph("INTERPRETACIÓN TÉCNICA", styles['CustomSectionHeader']))
    
    if 'IA' in resultado_str:
        mensaje = """
        El sistema de análisis de autenticidad detectó patrones acústicos anómalos, 
        característicos de técnicas de síntesis o manipulación de voz por Inteligencia Artificial.
        La alta probabilidad de que el audio sea falso requiere precaución y verificación adicional.
        """
    else:
        mensaje = """
        Los marcadores acústicos del archivo son altamente consistentes con una grabación de voz 
        humana natural. No se detectaron anomalías significativas que sugieran manipulación o 
        generación por Inteligencia Artificial. El nivel de confianza en el estado 'Auténtico' es alto.
        """
    
    elements.append(Paragraph(mensaje, styles['CustomBodyText']))
    elements.append(Spacer(1, 30))
    
    # 5. Firma Digital (Placeholder) (Usando CustomBodyText)
    elements.append(Paragraph(f"<b>Generado:</b> {datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}", styles['CustomBodyText']))
    elements.append(Paragraph("Firma Digital de Autenticación:", styles['CustomBodyText']))
    elements.append(Paragraph("TS-ID-938210-A-V", styles['CustomBodyText']))
    elements.append(Spacer(1, 30))

    # 6. Pie de página legal (Usando CustomFooter)
    footer_text = """
    Este informe es una herramienta de soporte analítico basada en algoritmos de detección. 
    No constituye una prueba forense legal definitiva. Los resultados están sujetos a las limitaciones 
    de los modelos de detección y la calidad del audio fuente.
    """
    elements.append(Paragraph(footer_text, styles['CustomFooter']))

    # Construir el PDF
    doc.build(elements)
    
    # Obtener el contenido del buffer y cerrarlo
    pdf_content = buffer.getvalue()
    buffer.close()
    
    return pdf_content