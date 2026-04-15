from pathlib import Path

# --- RUTAS PRINCIPALES ---
# Detecta automáticamente la ubicación de esta carpeta
BASE_DIR = Path(__file__).resolve().parent

# Ubicación de la Base de Datos
DB_PATH = BASE_DIR / "gestion_informes_v5.db"

# Ubicación de la Carpeta de Audios
AUDIO_DIR = BASE_DIR / "repositorio_audios"

# --- CONFIGURACIÓN DE IA ---
# Puedes cambiar "base" por "small" o "medium" según la potencia de tu PC
WHISPER_MODEL = "medium"

# --- CONFIGURACIÓN DE INTERFAZ ---
APP_TITLE = "🏥 Sistema de Gestión de Informes IA"
