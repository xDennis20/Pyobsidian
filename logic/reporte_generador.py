import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime


def generar_pdf_documentos(lista_documentos, nombre_usuario):
    """
    Recibe la lista de objetos Documento y dibuja el PDF en memoria.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    ancho, alto = A4
    y_actual = alto - 50

    # --- ENCABEZADO ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y_actual, "Reporte de Bóveda - Pyobsidian")

    y_actual -= 20
    c.setFont("Helvetica", 12)
    c.drawString(50, y_actual, f"Usuario: {nombre_usuario}")

    fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.drawRightString(ancho - 50, y_actual, f"Generado: {fecha_hoy}")

    y_actual -= 15
    c.line(50, y_actual, ancho - 50, y_actual)

    # --- CABECERAS DE LA TABLA ---
    y_actual -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y_actual, "ID")
    c.drawString(100, y_actual, "Título de la Nota")
    c.drawString(400, y_actual, "Fecha de Creación")

    y_actual -= 10
    c.line(50, y_actual, ancho - 50, y_actual)

    # --- LISTADO DE NOTAS ---
    c.setFont("Helvetica", 10)
    y_actual -= 20

    for doc in lista_documentos:
        # Paginación automática si llegamos al final de la hoja
        if y_actual < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y_actual = alto - 50

        # Dibujamos los atributos del objeto Documento
        c.drawString(50, y_actual, str(doc.id_documento))

        # Recortamos el título si es muy largo para que no se superponga
        titulo = (doc.titulo[:45] + '...') if len(doc.titulo) > 45 else doc.titulo
        c.drawString(100, y_actual, titulo)

        # Validamos la fecha por si alguna nota no la tiene
        fecha_str = str(doc.fecha_creacion) if doc.fecha_creacion else "S/N"
        c.drawString(400, y_actual, fecha_str)

        y_actual -= 20

    # Guardamos y preparamos el buffer
    c.save()
    buffer.seek(0)
    return buffer