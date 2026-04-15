import whisper
import streamlit as st
import torch  # Librería que maneja el hardware
import config

@st.cache_resource
def obtener_modelo():
    # 1. DETECCIÓN AUTOMÁTICA DE HARDWARE
    # Si hay GPU NVIDIA disponible, usa 'cuda', si no, usa 'cpu'
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    print(f"Cargando modelo {config.WHISPER_MODEL} en modo: {device}")
    
    # Cargamos el modelo especificando el dispositivo detectado
    modelo = whisper.load_model(config.WHISPER_MODEL, device=device)
    return modelo

def procesar_audio(ruta_archivo):
    try:
        modelo = obtener_modelo()
        # El proceso de transcripción también usará el hardware detectado
        resultado = modelo.transcribe(ruta_archivo, language='es')
        return resultado['text']
    except Exception as e:
        return f"Error en la transcripción: {str(e)}"
