from fpdf import FPDF
from datetime import datetime

class InformePDF(FPDF):
    def header(self):
        # Encabezado elegante
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "INFORME MÉDICO OFICIAL", border=False, ln=True, align="C")
        self.set_font("Arial", "I", 10)
        self.cell(0, 5, "Sistema de Gestión de Informes con IA", border=False, ln=True, align="C")
        self.ln(10)

    def footer(self):
        # Pie de página con numeración
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def crear_pdf_bytes(datos):
    """Genera el PDF y devuelve los bytes para que Streamlit pueda descargarlo."""
    pdf = InformePDF()
    pdf.add_page()
    
    # Sección de Datos del Paciente
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, " DATOS DEL PACIENTE Y EXAMEN", ln=True, fill=True)
    
    pdf.set_font("Arial", "", 11)
    pdf.cell(95, 10, f"Paciente: {datos['nombre_paciente']}", ln=0)
    pdf.cell(95, 10, f"ID Examen: {datos['id_examen']}", ln=1)
    pdf.cell(95, 10, f"Fecha Carga: {datos['fecha_recepcion']}", ln=0)
    pdf.cell(95, 10, f"Estado: {datos['estado']}", ln=1)
    pdf.ln(5)

    # Cuerpo del Informe
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, " RESULTADO DEL INFORME", ln=True, fill=True)
    
    pdf.set_font("Arial", "", 11)
    # multi_cell permite que el texto largo salte de línea automáticamente
    pdf.multi_cell(0, 8, datos['texto_final'])
    
    pdf.ln(10)
    
    # Firmas y Responsabilidades
    pdf.set_font("Arial", "I", 9)
    pdf.cell(0, 5, f"Editor Responsable: {datos['editor_asignado']}", ln=True)
    pdf.cell(0, 5, f"Fecha de Validación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    
    # Devolvemos el PDF como un chorro de bytes (S de string/bytes)
    return bytes(pdf.output())  # Convertimos el bytearray a bytes puros
