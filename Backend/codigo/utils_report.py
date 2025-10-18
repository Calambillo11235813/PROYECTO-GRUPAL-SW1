from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generar_reporte(codigo_obj):
    """
    Genera un PDF detallado con las métricas del análisis de código.
    Incluye complejidad, naming, repetitividad, tipo de código y fragmento AST.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setTitle("Reporte de Análisis de Código")

    # --- Encabezado principal
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 760, "🧠 Reporte de Análisis de Código Fuente")

    p.setFont("Helvetica", 10)
    y = 730
    p.drawString(100, y, f"Archivo: {codigo_obj.filename}"); y -= 15
    p.drawString(100, y, f"Fecha: {codigo_obj.created_at.strftime('%Y-%m-%d %H:%M:%S')}"); y -= 25

    # --- Métricas detalladas
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, "🔹 Métricas Técnicas:"); y -= 20
    p.setFont("Courier", 10)
    p.drawString(120, y, f"Complejidad Ciclomática: {codigo_obj.complejidad}"); y -= 15
    p.drawString(120, y, f"Naming Score: {getattr(codigo_obj, 'naming_score', 'N/A')}"); y -= 15
    p.drawString(120, y, f"Repetitividad: {getattr(codigo_obj, 'repetitividad', 'N/A')}%"); y -= 15
    p.drawString(120, y, f"Predict Score: {codigo_obj.predict_score}"); y -= 15
    p.drawString(120, y, f"Tipo de Código: {getattr(codigo_obj, 'tipo_codigo', 'Desconocido')}"); y -= 30

    # --- Línea separadora
    p.setFont("Helvetica", 10)
    p.drawString(100, y, "--------------------------------------------"); y -= 15
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, "📄 Fragmento del AST:"); y -= 15

    # --- Texto del AST (máx. 800 caracteres)
    text = p.beginText(100, y)
    text.setFont("Courier", 7)
    ast_text = str(codigo_obj.ast_json)[:800]
    for line in ast_text.splitlines():
        text.textLine(line[:100])
    p.drawText(text)

    # --- Cierre del PDF
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf
