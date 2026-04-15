Python
￼
from IPython.display import display, Markdown

# Contenido del archivo README.md basado en la versión refinada previa
readme_content = """# 🏥 AI-Medical Transcriptor: Gestión Digital de Informes Médicos

### 🚀 Automatización y Trazabilidad de Reportes Clínicos con IA

Este proyecto surge para optimizar el flujo de creación de informes médicos mediante el uso de Inteligencia Artificial. El objetivo es transformar dictados técnicos en documentos estructurados, reduciendo los tiempos de transcripción manual y minimizando errores humanos en el registro de procedimientos clínicos.

---

## 📋 Descripción del Proyecto
La aplicación ofrece un entorno seguro para que los profesionales de la salud carguen o graben dictados técnicos. El sistema integra un flujo de trabajo de tres etapas (**Carga -> Edición -> Validación**) que garantiza que cada informe emitido cuente con supervisión humana y respaldo digital.

**Funcionalidades Clave:**
* **Captura Multicanal:** Grabación directa desde el navegador (micrófono nativo) o carga de archivos de audio (WAV, MP3, OGG).
* **Identificación Unívoca:** Registro asociado a Nombre de Paciente e ID de Examen/Ficha para asegurar la trazabilidad.
* **Flujo de Calidad:** Herramienta de edición profesional en paralelo (Original vs. Editado) con cálculo automático de "Grado de Edición".
* **Exportación Formal:** Generación automática de reportes en PDF con formato clínico oficial.

---

## 🧠 Filosofía de Desarrollo: Clinician-Led Development

Este proyecto no ha sido desarrollado por un ingeniero de software tradicional, sino por una **Enfermera Clínica en transición a Hybrid Clinician-Developer**. Integro más de una década de experiencia en cuidados críticos con el desarrollo avanzado de herramientas de inteligencia artificial aplicada. El enfoque aplicado es el **Clinician-Led Development**:

* **Dominio del Problema:** El diseño y la lógica del sistema responden a necesidades reales detectadas tras 12 años de experiencia en servicios clínicos de urgencia.
* **Desarrollo Aumentado (AI-Augmented):** La implementación técnica ha sido orquestada mediante metodologías de **"Vibe Coding"** y el uso estratégico de **Agentes de IA**.
* **Supervisión Humana:** Como autora con conocimientos de Python, he dirigido la arquitectura y validado cada línea de código, asegurando que la tecnología actúe como un copiloto experto bajo una dirección clínica rigurosa.

---

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.13
- **Interfaz:** [Streamlit](https://streamlit.io/) (con `streamlit-mic-recorder` para captura de audio web).
- **IA/ML:** OpenAI Whisper `large-v3-turbo` (Procesamiento local de alta velocidad).
- **Base de Datos & Análisis:** SQLite3 y Pandas (Persistencia de datos y DataFrames para logs de auditoría).
- **Documentación:** fpdf2 (Motor de renderizado de PDFs nativo).
- **Infraestructura:** Optimizado para hardware con GPU dedicada y 64GB de RAM, con dependencias abstractas para compatibilidad multiplataforma.

---

## 🏗️ Arquitectura Modular
* `app.py`: Interfaz de usuario y orquestación de estados.
* `transcriber.py`: Lógica de transcripción neuronal (Whisper).
* `database.py`: Gestión de esquemas SQL e integridad de datos.
* `pdf_generator.py`: Plantillas y generación de documentos finales.
* `auth.py`: Control de acceso basado en roles (Administrador, Técnico, Editor).

---

## ⚙️ Requisitos del Sistema (Multiplataforma)

Para procesar audio, este proyecto requiere **FFmpeg** instalado a nivel de sistema operativo:

* **Linux:** `sudo apt install ffmpeg`
* **Mac:** `brew install ffmpeg`
* **Windows:** Descargar desde [ffmpeg.org](https://ffmpeg.org/download.html) y añadir el ejecutable al PATH del sistema.

---

---

## 🚀 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/cccontre1/AI-Medical-Transcriptor.git](https://github.com/cccontre1/AI-Medical-Transcriptor.git)
   cd AI-Medical-Transcriptor
   ```

2. **Configurar el entorno virtual:**
   ```bash
   python3 -m venv venv
   ```

3. **Activar el entorno virtual:**
   - **En Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```
   - **En Windows:**
     ```bash
     venv\Scripts\activate
     ```
   
4. **Instalar dependencias:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt 
   ```
  
5. **Ejecutar la aplicación:**
   ```bash
   streamlit run app.py
