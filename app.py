import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Generatore Stencil Tatuaggi", layout="wide")

st.title("🐍 InkFlow: Generatore Stencil Tatuaggi")
st.markdown("Trasforma le tue foto in uno stencil pulito in bianco e nero usando l'algoritmo Canny.")

# --- 1. Caricamento Immagine ---
uploaded_file = st.file_uploader("Carica la foto qui (PNG o JPG)", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    # Convertiamo il file caricato in un'immagine leggibile da OpenCV
    image = Image.open(uploaded_file)
    img_array = np.array(image.convert('RGB'))
    
    st.sidebar.header("Regola i Dettagli dello Stencil")

    # --- 2. Slider per le regolazioni (L'utente decide i dettagli) ---
    soglia1 = st.sidebar.slider("Soglia Canny Minima", 0, 255, 100)
    soglia2 = st.sidebar.slider("Soglia Canny Massima", 0, 255, 200)
    blur = st.sidebar.slider("Raggio Sfocatura (Blur)", 1, 15, 5, step=2) # Deve essere dispari

    # --- 3. La Magia (Algoritmo Canny per i bordi) ---
    
    # Convertiamo in scala di grigi
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Sfocatura per togliere il rumore
    blurred = cv2.GaussianBlur(gray, (blur, blur), 0)
    
    # Troviamo i bordi (Stencil)
    edges = cv2.Canny(blurred, soglia1, soglia2)
    
    # Invertiamo i colori (Linee nere su sfondo bianco - standard per stencil)
    edges_inverted = cv2.bitwise_not(edges)

    # Convertiamo l'array OpenCV in un'immagine PIL per il download
    img_stencil_pil = Image.fromarray(edges_inverted)
    
    # --- 4. Mostriamo il risultato ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Originale")
        st.image(image, use_column_width=True)
    
    with col2:
        st.subheader("Risultato Stencil")
        st.image(edges_inverted, use_column_width=True)
        
        # --- 5. Bottone per scaricare ---
        
        # Salviamo l'immagine in memoria come PNG per il download
        buf = io.BytesIO()
        img_stencil_pil.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="Scarica Stencil PNG",
            data=byte_im,
            file_name="inkflow_stencil.png",
            mime="image/png"
        )
        st.info("Consiglio: Stampa questo file in modalità 'Carta Copiativa' o 'Ectografica'.")

else:
    st.info("Inizia caricando un'immagine per generare il tuo stencil!")
