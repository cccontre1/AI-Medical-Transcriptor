import sqlite3
import pandas as pd
from config import DB_PATH  # Importamos la ruta desde tu config.py

def iniciar_db():
    """Crea las tablas si no existen al iniciar la app."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
   # Tabla de informes, Añadimos nombre_paciente e id_examen
    c.execute('''CREATE TABLE IF NOT EXISTS informes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  nombre_paciente TEXT, 
                  id_examen TEXT, 
                  autor_carga TEXT, 
                  editor_asignado TEXT, 
                  archivo_origen TEXT, 
                  ruta_audio TEXT, 
                  texto_ia TEXT, 
                  texto_final TEXT, 
                  grado_edicion REAL, 
                  fecha_recepcion TEXT, 
                  fecha_edicion TEXT, 
                  estado TEXT)''')
    
    # Tabla de Usuarios: Para el control de acceso
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                 (nombre_usuario TEXT PRIMARY KEY, 
                  contraseña TEXT, 
                  rol TEXT)''')
    
    # Creamos un usuario admin por defecto si la tabla está vacía
    c.execute("SELECT COUNT(*) FROM usuarios")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO usuarios VALUES ('admin', 'admin123', 'Administrador')")
    
    conn.commit()
    conn.close()

def ejecutar_query(query, params=(), fetch=False, pandas=False):
    """Función universal para hablar con la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    
    # Si queremos los resultados como un DataFrame de Pandas (ideal para tablas)
    if pandas:
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    # Si es una operación normal (Insert, Update, Delete)
    c = conn.cursor()
    c.execute(query, params)
    
    res = None
    if fetch:
        res = c.fetchall()
        
    conn.commit()
    conn.close()
    return res