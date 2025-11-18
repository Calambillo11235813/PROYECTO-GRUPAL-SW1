# Backend/codigo/utils/generador_reporte.py

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    ListFlowable,
    ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from io import BytesIO


def generar_pdf_reporte(analisis):
    """
    Genera un PDF en memoria con todos los datos del análisis.
    Devuelve raw bytes listos para enviarse con HttpResponse.
    """

    # ---------------------------------------
    # BUFFER EN MEMORIA PARA CONSTRUIR EL PDF
    # ---------------------------------------
    buffer = BytesIO()

    # ---------------------------------------
    # ESTILOS BASE DE REPORTLAB
    # ---------------------------------------
    styles = getSampleStyleSheet()

    # Título principal
    titulo = ParagraphStyle(
        "Titulo",
        parent=styles["Title"],
        fontSize=22,
        alignment=1,  # 1 = centrado
        textColor=colors.HexColor("#1F4E79")
    )

    # Subtítulos de secciones
    subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#1F4E79")
    )

    # Texto normal
    normal = styles["BodyText"]

    # ---------------------------------------
    # CONFIGURACIÓN DEL DOCUMENTO PDF
    # ---------------------------------------
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Lista de elementos del PDF
    story = []

    # ---------------------------------------
    # PORTADA
    # ---------------------------------------
    story.append(Paragraph("📊 Informe de Análisis de Código", titulo))
    story.append(Spacer(1, 20))

    story.append(Paragraph(f"Archivo analizado: <b>{analisis.nombre_archivo}</b>", normal))
    story.append(Paragraph(f"Lenguaje detectado: <b>{analisis.lenguaje}</b>", normal))
    story.append(Paragraph(f"Fecha del análisis: <b>{analisis.fecha_analisis.strftime('%d/%m/%Y %H:%M')}</b>", normal))
    story.append(Spacer(1, 25))

    # Línea decorativa
    story.append(Paragraph(
        "<para alignment='center'><font color='#1F4E79'>────────────────────────────────────────────────────────────</font></para>",
        normal
    ))
    story.append(Spacer(1, 15))

    # ---------------------------------------
    # SECCIÓN: RESULTADO IA
    # ---------------------------------------
    story.append(Paragraph("Resultado IA", subtitulo))
    story.append(Spacer(1, 10))

    # Tabla con datos de IA
    datos_ia = [
        ["Es generado por IA", "Sí" if analisis.ia_es_generado else "No"],
        ["Confianza", f"{analisis.ia_confianza*100:.2f}%"],
        ["Probabilidad IA", f"{analisis.ia_detalles.get('ai_prob'):.4f}" if analisis.ia_detalles else "-"],
        ["Probabilidad Humano", f"{analisis.ia_detalles.get('human_prob'):.4f}" if analisis.ia_detalles else "-"],
        ["Modelo", analisis.ia_metodo],
        ["Versión modelo", analisis.version_modelo],
        ["Timestamp modelo", analisis.timestamp_modelo],
    ]

    table_ia = Table(datos_ia, hAlign="LEFT")
    table_ia.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DAE3F3")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#1F4E79")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    story.append(table_ia)
    story.append(Spacer(1, 20))

    # ---------------------------------------
    # SECCIÓN: MÉTRICAS DEL CÓDIGO
    # ---------------------------------------
    story.append(Paragraph("Métricas de Código", subtitulo))
    story.append(Spacer(1, 10))

    datos_metricas = [
        ["Complejidad ciclomatica", analisis.complejidad_ciclomatica],
        ["Variabilidad funciones", analisis.variabilidad_funciones],
        ["Índice predictibilidad", analisis.indice_predictibilidad],
    ]

    table_m = Table(datos_metricas, hAlign="LEFT")
    table_m.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DAE3F3")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#1F4E79")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    story.append(table_m)
    story.append(Spacer(1, 20))

    # ---------------------------------------
    # SECCIÓN: PATRONES SINTÁCTICOS
    # ---------------------------------------
    story.append(Paragraph("Patrones Sintácticos", subtitulo))
    story.append(Spacer(1, 10))

    patrones = analisis.patrones_comunes or {}

    # Convertimos los patrones en una lista elegante
    lista_patrones = ListFlowable(
        [
            ListItem(
                Paragraph(f"<b>{k}</b>: {v}", normal),
                bulletColor=colors.HexColor("#1F4E79")
            )
            for k, v in patrones.items()
        ],
        bulletType="bullet",
        start="circle",
        leftIndent=20
    )

    story.append(lista_patrones)
    story.append(Spacer(1, 20))
    # ---------------------------------------
    # SECCIÓN: CÓDIGO ANALIZADO (CON MARCADO IA)
    # ---------------------------------------
    story.append(Paragraph("Código Analizado", subtitulo))
    story.append(Spacer(1, 10))

    # Intentar leer el archivo original
    try:
        with open(analisis.archivo.path, "r", encoding="utf8") as f:
            codigo = f.read()
    except:
        codigo = "No se pudo recuperar el código original."

    lineas_ia = analisis.lineas_sospechosas or []

    # Convertir a formato HTML simple para resaltado
    codigo_html = "<para><font face='Courier'>"

    for i, linea in enumerate(codigo.split("\n"), start=1):
        color = "#FF4C4C" if i in lineas_ia else "#000000"
        codigo_html += f"<font color='{color}'>{str(i).zfill(3)} | {linea}</font><br/>"

    codigo_html += "</font></para>"

    story.append(Paragraph(codigo_html, normal))
    story.append(Spacer(1, 20))

    # ---------------------------------------
    # SECCIÓN: RECOMENDACIONES
    # ---------------------------------------
    story.append(Paragraph("Recomendaciones para Verificación Manual", subtitulo))
    story.append(Spacer(1, 10))

    recomendaciones = []

    # 1. Revisar líneas sospechosas
    if lineas_ia:
        recomendaciones.append(
            f"Revisar cuidadosamente las líneas sospechosas: {', '.join(map(str, lineas_ia))}."
        )

    # 2. Complejidad alta
    if analisis.complejidad_ciclomatica and analisis.complejidad_ciclomatica > 10:
        recomendaciones.append("La complejidad ciclómica es alta. Considere un refactor.")

    # 3. Variabilidad irregular
    if analisis.variabilidad_funciones and analisis.variabilidad_funciones > 5:
        recomendaciones.append("La variabilidad de funciones es elevada, puede indicar código inconsistente.")

    # 4. Índice de predictibilidad alto
    if analisis.indice_predictibilidad and analisis.indice_predictibilidad > 0.85:
        recomendaciones.append("El índice de predictibilidad es muy alto: posible código generado por IA.")

    # 5. Si no hay nada relevante
    if not recomendaciones:
        recomendaciones.append("No se detectaron anomalías significativas en el estilo del código.")

    # Lista final
    lista_reco = ListFlowable(
        [ListItem(Paragraph(r, normal)) for r in recomendaciones],
        bulletType="bullet",
        start="circle",
        leftIndent=20
    )

    story.append(lista_reco)
    story.append(Spacer(1, 20))

    # ---------------------------------------
    # GENERAR PDF FINAL
    # ---------------------------------------
    pdf.build(story)

    return buffer.getvalue()
