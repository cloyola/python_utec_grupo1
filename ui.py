import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import streamlit as st
from PIL import Image
from langchain.chains import LLMChain
from generate_qr import generate_qr_code
from main import pipeline
from logger import logger

st.set_page_config(
    page_title="Yape - Creador de deeplink",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Estilos CSS personalizados (opcional, para un mejor parecido) ---
# Puedes añadir más estilos para fuentes, colores, espaciado, etc.
st.markdown("""
<style>
    .main {
        background-color: #742384; /* Fondo blanco */
        padding: 20px;
    }
    .stApp {
        background-color: #742384; /* Asegura que el fondo de la app sea blanco */
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #eee;
        margin-bottom: 20px;
    }
    .header img {
        height: 40px; /* Ajusta el tamaño del logo */
    }
    .header .nav-links a {
        margin-left: 20px;
        text-decoration: none;
        color: #fff;
        font-weight: bold;
    }
    .hero-section {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 50px 0;
        text-align: center;
    }
    .hero-section img {
        max-width: 50%;
        height: auto;
    }
    .hero-text {
        padding: 0 20px;
    }
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 50px;
        border-top: 1px solid #eee;
        color: #777;
    }
</style>
""", unsafe_allow_html=True)            

# --- Encabezado (simulando la barra de navegación) ---
st.markdown("""
<div class="header">
    <img src="https://www.yape.com.pe/images/logo-yape_negative.png" alt="Logo Yape" style="width: 80px; height: auto;">
    <div class="nav-links">
        <a href="https://www.yape.com.pe/">Inicio</a>
        <a href="https://www.yape.com.pe/preguntas-frecuentes">Centro de ayuda</a>
        <a href="https://www.yape.com.pe/crea-tu-cuenta">Crear mi cuenta</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("Creador de deeplink")
st.markdown("Convierte tus recibos en links para pagar directamente en el app Yape")

# Crear las dos columnas
col1, col2, col3 = st.columns(3, gap="medium") # Puedes ajustar el 'gap' (espacio) si lo deseas

#TO DO: Mejorar el front para tener un UI similar a Yape.com.pe

with col1:
    st.markdown("### Subir Imagen")
    image_file = st.file_uploader("Sube una imagen (JPG, JPEG, PNG)", type=["jpg","jpeg","png"])

with col2:
    if image_file:
        image = Image.open(image_file)
        st.markdown("#### 📷 Imagen Subida")
        logger.info("Imagen subida")
        st.image(image, caption="Imagen subida", use_container_width=False, width=250) # Usa use_container_width para que la imagen se ajuste a la columna
        logger.info("Imagen mostrada")

with col3:
    if image_file:
        st.markdown("#### Resultado del Procesamiento")
        # Procesar imagen
        with st.spinner("Procesando imagen..."):
            deeplink = pipeline(image_file)
        
        logger.info(f"Deeplink generado: {deeplink}")

        if deeplink is None: # Usar 'is None' es más idiomático que '== None'
            deeplink = "https://yape.com.pe/app/services-pay"
            result_text = "No se encontró la empresa para el pago, pero puedes utilizar el enlace general."
        else:
            result_text = "¡Empresa encontrada!"

        # Mostrar deeplink
        st.markdown("##### 🔗 Enlace Generado")
        st.write(result_text)
        st.code(deeplink, language='text')

        # Generar y mostrar código QR
        qr_filename = "qr/mi_codigo_qr.png" # Define el nombre del archivo QR
        generate_qr_code(deeplink, qr_filename)
        qr_img = Image.open(qr_filename)

        st.markdown("##### 📱 Código QR del Enlace")
        st.image(qr_img, caption="Escanea para abrir el enlace", use_container_width=False, width=200) # Ajusta el width si es necesario

    else:
        st.info("Sube una imagen en la columna de la izquierda para ver el resultado aquí.")
