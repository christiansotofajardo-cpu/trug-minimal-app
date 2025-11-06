
import streamlit as st

st.set_page_config(page_title="TRU-G Minimal App", layout="centered")

st.title("TRU-G Minimal App")
st.write("Bienvenido. Esta es la versión más simple y estable para poner en línea.")

st.subheader("Entrada de texto")
texto = st.text_area("Pega tu texto:", height=150, placeholder="Escribe o pega aquí...")

st.subheader("(Opcional) Subir archivo .txt")
archivo = st.file_uploader("Sube un archivo de texto plano (.txt)", type=["txt"])

def procesar_texto(t: str) -> str:
    # ⚠️ Reemplaza esta función con tu lógica real
    return t.upper()

entrada = ""
if archivo is not None:
    try:
        entrada = archivo.read().decode("utf-8", errors="ignore")
    except Exception:
        st.error("No se pudo leer el archivo. Asegúrate de que sea .txt y esté en UTF-8.")
elif texto:
    entrada = texto

if st.button("Procesar"):
    if not entrada.strip():
        st.warning("Ingresa texto o sube un archivo .txt antes de procesar.")
    else:
        with st.spinner("Procesando..."):
            salida = procesar_texto(entrada)
        st.success("Listo ✅")
        st.download_button("Descargar resultado", data=salida, file_name="resultado.txt")
        st.text_area("Salida:", value=salida, height=200)
