import streamlit as st
import re
from collections import Counter

st.set_page_config(page_title="TRU-G Minimal App v3 – Clasificador simple", layout="centered")

st.title("TRU-G Minimal App v3")
st.caption("Versión con clasificador simple (Narrativo vs. Argumentativo) y salida explicada.")

st.subheader("Entrada de texto")
texto = st.text_area("Pega tu texto:", height=180, placeholder="Escribe o pega aquí...")

# --- Listas de marcadores (simple, explicables) ---
ARG_MARKERS = [
    "porque", "por lo tanto", "por tanto", "por ende", "debido a",
    "ya que", "puesto que", "sin embargo", "no obstante",
    "por consiguiente", "en consecuencia", "por eso",
    "debería", "debe", "se debe", "considero", "pienso que",
    "a favor", "en contra", "es necesario", "propongo", "sostengo",
    "argumento", "evidencia", "fundamento", "razón", "razones"
]

NAR_MARKERS = [
    "una vez", "había", "habia", "era
