from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.conf import settings
import os

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
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Definir estilos personalizados solo si no existen
    if 'Center' not in styles:
        styles.add(ParagraphStyle(
            name='Center', 
            alignment=TA_CENTER,
            fontSize=14,
            spaceAfter=20
        ))
    
    if 'Title' not in styles:
        styles.add(ParagraphStyle(
            name='Title', 
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=30
        ))
    
    if 'BodyText' not in styles:
        styles.add(ParagraphStyle(
            name='BodyText',
            fontSize=12,
            leading=14,
            spaceAfter=10
        ))
    
    # Contenido del PDF
    elements = []
    
    # Título
    elements.append(Paragraph("CERTIFICADO DE ANÁLISIS DE AUDIO", styles['Title']))
    
    # Información del archivo
    elements.append(Paragraph(f"<b>Archivo analizado:</b> {audio_upload.original_filename}", styles['BodyText']))
    elements.append(Paragraph(f"<b>Fecha de análisis:</b> {audio_upload.created_at.strftime('%d/%m/%Y %H:%M')}", styles['BodyText']))
    
    # Resultado del análisis
    resultado = "AUTÉNTICO" if audio_upload.result == 'real' else "MANIPULADO CON IA"
    color_resultado = colors.green if audio_upload.result == 'real' else colors.red
    
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("RESULTADO DEL ANÁLISIS", styles['Center']))
    
    # Tabla de resultados
    data = [
        ["Parámetro", "Valor"],
        ["Estado", resultado],
        ["Nivel de confianza", f"{audio_upload.probability*100:.2f}%"]
    ]
    
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('TEXTCOLOR', (1, 1), (1, 1), color_resultado),
        ('TEXTCOLOR', (1, 2), (1, 2), color_resultado),
        ('FONTNAME', (1, 1), (1, 2), 'Helvetica-Bold'),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 30))
    
    # Descripción del resultado
    if audio_upload.result == 'real':
        mensaje = """
        El análisis acústico avanzado indica que este archivo de audio muestra características consistentes 
        con grabaciones de voz humana natural, sin evidencia de manipulación o síntesis por IA.
        """
    else:
        mensaje = """
        El análisis acústico avanzado ha detectado patrones característicos de manipulación o síntesis 
        por IA en este archivo de audio. La probabilidad de que este audio haya sido generado o alterado 
        mediante inteligencia artificial es significativamente alta.
        """
    
    elements.append(Paragraph(mensaje, styles['BodyText']))
    elements.append(Spacer(1, 20))
    
    # Pie de página
    elements.append(Paragraph("<i>Este certificado ha sido generado automáticamente por el sistema de análisis de autenticidad de audio.</i>", 
                            styles['BodyText']))
    elements.append(Paragraph("<i>Los resultados se basan en análisis de patrones acústicos y pueden estar sujetos a limitaciones técnicas.</i>", 
                            styles['BodyText']))
    
    # Construir el PDF
    doc.build(elements)
    
    # Obtener el contenido del PDF
    pdf_content = buffer.getvalue()
    
    # Retornar el contenido del PDF
    return pdf_content
