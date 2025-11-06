
import streamlit as st
import re
from collections import Counter

st.set_page_config(page_title="TRU-G Minimal App v3 – Clasificador simple", layout="centered")

st.title("TRU-G Minimal App v3")
st.caption("Versión con clasificador simple (Narrativo vs. Argumentativo) y salida explicada.")

st.subheader("Entrada de texto")
texto = st.text_area("Pega tu texto:", height=180, placeholder="Escribe o pega aquí...")

# --- Listas de marcadores (muy simples, editables) ---
ARG_MARKERS = [
    "porque", "por lo tanto", "por tanto", "por ende", "debido a",
    "ya que", "puesto que", "sin embargo", "no obstante",
    "por consiguiente", "en consecuencia", "por eso",
    "debería", "debe", "se debe", "considero", "pienso que",
    "a favor", "en contra", "es necesario", "propongo", "sostengo",
    "argumento", "evidencia", "fundamento", "razón", "razones"
]

NAR_MARKERS = [
    "una vez", "había", "habia", "era", "éramos", "estaba", "estabamos",
    "cuando", "entonces", "de repente", "al día siguiente", "al dia siguiente",
    "luego", "después", "despues", "mientras", "antes", "más tarde", "mas tarde",
    "personaje", "cuento", "historia", "relato", "camino", "lugar", "tiempo",
    "dijo", "contó", "conto"
]

# Normalizador simple
def normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[¡!¿?\.,;:()\[\]\-–—\"']", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

# Clasificador muy simple basado en marcadores
def classify_text(text: str):
    norm = normalize(text)
    tokens = norm.split()

    # Búsqueda por substrings para permitir multi-palabra
    def count_markers(tokens, markers):
        joined = " " .join(tokens)
        counts = Counter()
        for m in markers:
            # contar ocurrencias como palabra/frase completa
            occ = len(re.findall(rf"\\b{re.escape(m)}\\b", joined))
            if occ > 0:
                counts[m] = occ
        return counts

    arg_counts = count_markers(tokens, ARG_MARKERS)
    nar_counts = count_markers(tokens, NAR_MARKERS)

    arg_count = sum(arg_counts.values())
    nar_count = sum(nar_counts.values())

    total_hits = arg_count + nar_count
    if total_hits == 0:
        # fallback por rasgos simples: verbos deónticos vs. morfos de pasado
        deonticos = len(re.findall(r"\\b(debe|debería|deberia|necesario|propongo|considero)\\b", norm))
        pasado = len(re.findall(r"\\b(aba|ía|ia|aron|eron|ó|o|í|i)\\b", norm))
        arg_count = deonticos
        nar_count = pasado
        total_hits = max(1, arg_count + nar_count)

    arg_score = arg_count / total_hits
    nar_score = nar_count / total_hits
    label = "Argumentativo" if arg_score >= nar_score else "Narrativo"

    explanation = {
        "argumentativo_marcadores": dict(arg_counts),
        "narrativo_marcadores": dict(nar_counts),
        "arg_count": int(arg_count),
        "nar_count": int(nar_count),
        "arg_score": round(arg_score, 3),
        "nar_score": round(nar_score, 3),
        "tokens_total": len(tokens),
    }
    return label, explanation

def procesar_trug(texto: str) -> str:
    \"\"\"Pipeline TRU-G placeholder + clasificador.\"\"\"
    label, exp = classify_text(texto)
    resumen = [
        f\"Clasificación TRU-G (simple): {label}\",
        f\"Score argumentativo: {exp['arg_score']} | Score narrativo: {exp['nar_score']}\",
        f\"Marcadores argumentativos: {exp['argumentativo_marcadores']}\",
        f\"Marcadores narrativos: {exp['narrativo_marcadores']}\",
        f\"Total de tokens (aprox.): {exp['tokens_total']}\",
    ]
    return \"\\n\".join(resumen)

if st.button(\"Procesar\"):
    if not texto.strip():
        st.warning(\"Ingresa texto antes de procesar.\")
    else:
        with st.spinner(\"Procesando...\"):
            salida = procesar_trug(texto)
        st.success(\"Listo ✅\")
        st.text_area(\"Salida:\", value=salida, height=240)
        st.download_button(\"Descargar resultado\", data=salida, file_name=\"resultado_trug_clasificador.txt\")

with st.expander(\"¿Cómo funciona este clasificador simple?\"):
    st.write(
        \"\"\"
        Este clasificador inicial usa **marcadores lingüísticos** muy simples:
        - Si predominan conectores y expresiones de **argumentación** (p. ej., *porque, por lo tanto, considero, propongo*), 
          la etiqueta será *Argumentativo*.
        - Si predominan marcadores **narrativos/temporales** (p. ej., *una vez, cuando, luego, había*), 
          la etiqueta será *Narrativo*.

        > **Nota:** Es un prototipo explicable y ajustable. Puedes editar las listas `ARG_MARKERS` y `NAR_MARKERS`
        para adaptarlo a tus dominios (HPV, ELE, etc.). Más adelante podemos reemplazarlo por un modelo entrenado.
        \"\"\"
    )
