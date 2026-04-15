import streamlit as st
from datetime import datetime
import Levenshtein
import config
from database import iniciar_db, ejecutar_query
from transcriber import procesar_audio
from auth import login, logout
from streamlit_mic_recorder import mic_recorder
from pdf_generator import crear_pdf_bytes

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title=config.APP_TITLE, page_icon="🏥", layout="wide")
# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    /* Estilo para los títulos */
    h1, h2, h3 {
        color: #2E5A88 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    # 
    
    /* Botones más redondeados y elegantes */
    .stButton>button {
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Personalización de las tarjetas de información */
    .stAlert {
        border-radius: 10px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    iniciar_db()

    if 'login' not in st.session_state or not st.session_state['login']:
        login()
        return

    # --- BARRA LATERAL (SIDEBAR) ---
    with st.sidebar:
        st.title(f"🏥 {config.APP_TITLE}")
        st.write(f"**Usuario:** {st.session_state['usuario']}")
        st.write(f"**Rol:** {st.session_state['rol']}")
        st.divider()
        
        opciones = ["📊 Historial"]
                # Solo el Administrador puede gestionar usuarios
        if st.session_state['rol'] == 'Administrador':
            opciones.append("👥 Gestión de Usuarios")
        if st.session_state['rol'] in ['Administrador', 'Personal Técnico']:
            opciones.insert(0, "📤 Cargar Dictado")
        if st.session_state['rol'] in ['Administrador', 'Editor']:
            opciones.insert(1, "✍️ Bandeja de Edición")
        if st.session_state['rol'] in ['Administrador', 'Personal Técnico']:
            opciones.insert(2, "✅ Validación Final")
        
        menu = st.radio("Navegación", opciones)
        if st.button("🚪 Cerrar Sesión"):
            logout()

    # --- 1. SECCIÓN: CARGAR DICTADO ---
    if menu == "📤 Cargar Dictado":
        st.header("Carga de Dictados Técnicos")
        
        # Datos del paciente (Definidos al inicio de la sección)
        col_a, col_b = st.columns(2)
        with col_a:
            paciente = st.text_input("Nombre del Paciente", placeholder="Ej: Juan Pérez")
        with col_b:
            id_examen = st.text_input("ID del Examen / N° Ficha", placeholder="Ej: EX-1023")

        st.divider()
        col_c, col_d = st.columns(2)
        
        with col_c:
            st.subheader("Opción A: Grabar")
            audio_grabado = mic_recorder(start_prompt="⏺️ Iniciar Grabación", stop_prompt="⏹️ Detener", key='recorder')
            if audio_grabado:
                st.toast("Audio grabado correctamente", icon="🎙️")

        with col_d:
            st.subheader("Opción B: Subir Archivo")
            archivo_subido = st.file_uploader("Seleccionar de PC", type=["mp3", "wav", "ogg"])

        # Identificar qué audio vamos a usar
        # --- IDENTIFICAR QUÉ AUDIO VAMOS A USAR ---
        audio_data = None
        
        if audio_grabado:
            # Forzamos los bytes de la grabación
            audio_data = bytes(audio_grabado['bytes'])
            st.toast("Audio grabado correctamente", icon="🎙️")

        elif archivo_subido:
            # .read() es más directo que getbuffer() y nos entrega bytes puros
            audio_data = archivo_subido.read() 

        # --- VALIDACIÓN Y VISTA PREVIA ---
        if audio_data:
            st.success("✅ Audio detectado y listo")
            
            # Ahora st.audio no fallará porque recibe bytes puros
            st.audio(audio_data)
            
          
            if st.button("🚀 Iniciar Transcripción con IA", key="btn_procesar_unico"):
                nombre_final = paciente if paciente else "Paciente Genérico"
                id_final = id_examen if id_examen else "ID-0000"
                
                with st.spinner("Whisper está analizando el audio..."):
                    nombre_archivo = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_audio.wav"
                    ruta_completa = str(config.AUDIO_DIR / nombre_archivo)
                    
                    with open(ruta_completa, "wb") as f:
                        f.write(audio_data)
                    
                    texto_ia = procesar_audio(ruta_completa)
                    
                    query = """INSERT INTO informes (nombre_paciente, id_examen, autor_carga, archivo_origen, ruta_audio, texto_ia, fecha_recepcion, estado) 
                               VALUES (?, ?, ?, ?, ?, ?, ?, 'Cargado')"""
                    
                    ejecutar_query(query, (nombre_final, id_final, st.session_state['usuario'], nombre_archivo, ruta_completa, texto_ia, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    
                    st.success(f"Informe de {nombre_final} guardado exitosamente.")
                    st.rerun()

        st.divider()
        st.subheader("Mis cargas recientes")
        df_mis_cargas = ejecutar_query(f"SELECT nombre_paciente, fecha_recepcion, estado FROM informes WHERE autor_carga = '{st.session_state['usuario']}' ORDER BY id DESC LIMIT 5", pandas=True)
        st.table(df_mis_cargas)

    # --- 2. SECCIÓN: BANDEJA DE EDICIÓN ---
    # --- 2. SECCIÓN: BANDEJA DE EDICIÓN ---
    elif menu == "✍️ Bandeja de Edición":
        st.header("Bandeja de Edición Administrativa")
        
        # Traemos los datos necesarios
        query_e = "SELECT id, nombre_paciente, id_examen, texto_ia, ruta_audio FROM informes WHERE estado='Cargado'"
        df_p = ejecutar_query(query_e, pandas=True)
        
        if not df_p.empty:
            # Selector de informe
            opciones_e = df_p['id'].astype(str) + " - Paciente: " + df_p['nombre_paciente']
            seleccion = st.selectbox("Seleccione informe para editar:", opciones_e)
            id_sel = int(seleccion.split(" - ")[0])
            fila = df_p[df_p['id'] == id_sel].iloc[0]

            # Reproductor de audio (siempre visible arriba para referencia)
            st.audio(fila['ruta_audio'])
            st.divider()

            # --- DISEÑO EN DOS COLUMNAS ---
            col_original, col_edicion = st.columns(2)

            with col_original:
                st.subheader("🤖 Transcripción IA")
                # Usamos un st.info o un st.text_area deshabilitado para que se vea como bloque
                st.markdown(f"""
                <div style="background-color: #F0F4F8; padding: 15px; border-radius: 10px; border-left: 5px solid #2E5A88; min-height: 300px;">
                    <p style="color: #1F2937;">{fila['texto_ia']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.caption("Texto original generado por Whisper (Solo lectura)")

            with col_edicion:
                st.subheader("✍️ Edición Humana")
                # El editor trabaja aquí
                texto_final = st.text_area(
                    "Realice las correcciones necesarias:", 
                    value=fila['texto_ia'], 
                    height=320,
                    key="area_edicion_medica"
                )
            
            st.divider()
            
            # Botón de guardado centrado o a la derecha
            if st.button("🚀 Finalizar y enviar a Validación", key="btn_guardar_edicion"):
                # Calculamos el grado de cambio (Métrica de calidad)
                similitud = Levenshtein.ratio(fila['texto_ia'], texto_final)
                grado = round((1 - similitud) * 100, 2)
                
                query_u = "UPDATE informes SET editor_asignado=?, texto_final=?, grado_edicion=?, estado='Editado', fecha_edicion=? WHERE id=?"
                ejecutar_query(query_u, (st.session_state['usuario'], texto_final, grado, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id_sel))
                
                st.balloons() # Un pequeño efecto visual de éxito
                st.success(f"Informe de {fila['nombre_paciente']} actualizado. Grado de edición: {grado}%")
                st.rerun()
        else:
            st.info("No hay informes pendientes de edición.")

    # --- 3. SECCIÓN: VALIDACIÓN FINAL ---
    elif menu == "✅ Validación Final":
        st.header("Validación Profesional y PDF")
        query_v = "SELECT * FROM informes WHERE estado='Editado'"
        df_v = ejecutar_query(query_v, pandas=True)
        
        if not df_v.empty:
            opciones_v = df_v['id'].astype(str) + " - " + df_v['nombre_paciente']
            sel = st.selectbox("Seleccione informe:", opciones_v)
            id_sel = int(sel.split(" - ")[0])
            fila = df_v[df_v['id'] == id_sel].iloc[0]
            
            st.subheader(f"Paciente: {fila['nombre_paciente']} ({fila['id_examen']})")
            st.text_area("Texto corregido:", value=fila['texto_final'], height=250, disabled=True)
            
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                if st.button("✅ Aprobar Informe", key="btn_aprobar"):
                    ejecutar_query("UPDATE informes SET estado='Validado' WHERE id=?", (id_sel,))
                    st.success("Informe Validado.")
                    st.rerun()
            with col_v2:
                # El botón de PDF se muestra si está Editado o Validado
                pdf_bytes = crear_pdf_bytes(fila)
                st.download_button(label="📥 Descargar PDF", data=pdf_bytes, file_name=f"Informe_{fila['nombre_paciente']}.pdf", mime="application/pdf", key="btn_pdf")
        else:
            st.info("No hay informes esperando validación.")

    # --- 4. SECCIÓN: HISTORIAL ---
    elif menu == "📊 Historial":
        st.header("Registro Histórico")
        df_h = ejecutar_query("SELECT * FROM informes ORDER BY id DESC", pandas=True)
        st.dataframe(df_h, use_container_width=True)

# --- 5. SECCIÓN: GESTIÓN DE USUARIOS (Solo Admin) ---
    elif menu == "👥 Gestión de Usuarios":
        st.header("Administración de Personal")
        
        tab1, tab2 = st.tabs(["🆕 Crear Usuario", "📋 Lista de Personal"])
        
        with tab1:
            with st.form("nuevo_usuario"):
                nuevo_nombre = st.text_input("Nombre de Usuario (Login)")
                nueva_pass = st.text_input("Contraseña", type="password")
                nuevo_rol = st.selectbox("Rol Asignado", ["Personal Técnico", "Editor", "Administrador"])
                
                if st.form_submit_button("Registrar en el Sistema"):
                    if nuevo_nombre and nueva_pass:
                        try:
                            query_u = "INSERT INTO usuarios (nombre_usuario, contraseña, rol) VALUES (?, ?, ?)"
                            ejecutar_query(query_u, (nuevo_nombre, nueva_pass, nuevo_rol))
                            st.success(f"Usuario {nuevo_nombre} creado como {nuevo_rol}")
                        except:
                            st.error("El usuario ya existe o hubo un problema en el registro.")
                    else:
                        st.warning("Por favor, completa todos los campos.")

        with tab2:
            st.subheader("Personal con acceso")
            df_usuarios = ejecutar_query("SELECT nombre_usuario, rol FROM usuarios", pandas=True)
            st.table(df_usuarios)
            
if __name__ == "__main__":
    main()
