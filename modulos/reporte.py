from modulos.archivo import cargar_desde_csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, TableStyle, Paragraph
from colorama import Fore
import emoji
from datetime import datetime

def generar_reporte_pdf(usuario):
    """
    Genera un reporte PDF profesional con los datos de estudiantes.
    
    Args:
        usuario (str): Nombre de usuario para cargar los datos correspondientes
    """
    try:
        datos = cargar_desde_csv(usuario)
        if not datos:
            print(Fore.YELLOW + emoji.emojize("\U0001F50D No hay datos para generar el reporte."))
            return

        # Configuración del documento
        fecha_reporte = datetime.now().strftime("%Y-%m-%d %H:%M")
        nombre_archivo = f"reporte_estudiantes_{usuario}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        ancho, alto = letter
        
        # Estilos
        estilos = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle(
            'Titulo',
            parent=estilos['Title'],
            fontSize=16,
            alignment=1,
            spaceAfter=20
        )
        
        # Título del reporte
        titulo = Paragraph(f"Reporte de Estudiantes - {usuario}", estilo_titulo)
        titulo.wrapOn(c, ancho - 100, alto)
        titulo.drawOn(c, 50, alto - 50)
        
        # Información del reporte
        c.setFont("Helvetica", 10)
        c.drawString(50, alto - 80, f"Fecha de generación: {fecha_reporte}")
        c.drawString(50, alto - 95, f"Total de estudiantes: {len(datos)}")
        
        # Preparar datos para la tabla
        encabezados = ["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (m)", "IMC", "Presión"]
        datos_tabla = [encabezados]
        
        for estudiante in datos:
            presion = f"{estudiante[6] or 'N/A'}/{estudiante[7] or 'N/A'}"
            datos_tabla.append([
                estudiante[0],
                estudiante[1],
                estudiante[2],
                f"{estudiante[3]:.1f}",
                f"{estudiante[4]:.2f}",
                f"{estudiante[5]:.1f}",
                presion
            ])
        
        # Crear tabla
        tabla = Table(datos_tabla, colWidths=[50, 120, 40, 60, 70, 50, 60])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F81BD')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#DCE6F1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        
        # Posicionar tabla
        tabla.wrapOn(c, ancho - 100, alto - 150)
        tabla.drawOn(c, 50, alto - 450)
        
        # Pie de página
        c.setFont("Helvetica", 8)
        c.drawString(50, 30, f"Generado por Sistema Biomédico - Página 1")
        
        c.save()
        print(Fore.GREEN + emoji.emojize(f"\U0001F4C4 Reporte generado exitosamente: {nombre_archivo}"))
        
    except Exception as e:
        print(Fore.RED + emoji.emojize(f"\U0000274C Error al generar PDF: {str(e)}"))