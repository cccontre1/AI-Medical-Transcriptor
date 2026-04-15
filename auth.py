import streamlit as st
from database import ejecutar_query

def autenticar_usuario(usuario, password):
    """Verifica las credenciales en la base de datos."""
    query = "SELECT rol FROM usuarios WHERE nombre_usuario=? AND contraseña=?"
    resultado = ejecutar_query(query, (usuario, password), fetch=True)
    return resultado[0][0] if resultado else None

def login():
    """Muestra la interfaz de acceso y maneja el estado de la sesión."""
    st.title("🔐 Acceso al Sistema")
    
    with st.form("login_form"):
        usuario = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        boton_entrar = st.form_submit_button("Ingresar")
        
        if boton_entrar:
            rol = autenticar_usuario(usuario, password)
            if rol:
                # Guardamos la 'pulsera de identificación' en la sesión
                st.session_state['login'] = True
                st.session_state['usuario'] = usuario
                st.session_state['rol'] = rol
                st.success(f"Bienvenido/a, {usuario} ({rol})")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

def logout():
    """Borra la sesión y vuelve al login."""
    st.session_state['login'] = False
    st.session_state['usuario'] = None
    st.session_state['rol'] = None
    st.rerun()