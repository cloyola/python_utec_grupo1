import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import streamlit as st
from PIL import Image
from langchain.chains import LLMChain
from generate_qr import generate_qr_code
from main import pipeline

st.set_page_config(
    page_title="Creador de deeplink",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Creador de deeplink")
st.markdown("Convierte tus recibos en links para pagar directamente en el app Yape")

#TO DO: Mejorar el front para tener un UI similar a Yape.com.pe

image_file = st.file_uploader("Subir una imagen an image",type=["jpg","jpeg","png"])
if image_file:
    image = Image.open(image_file)
    st.markdown("### 📷 Imagen subida")
    st.image(image, caption="Imagen subida", use_container_width=300)
    
    # Procesar imagen
    deeplink = pipeline(image_file)
    print(deeplink)

    if deeplink == None:
        deeplink = "https://yape.com.pe/app/services-pay"
        result_text = "No se encontró la empresa para el pago pero puedes utilizar el enlace general"
    else:
        result_text = "Empresa encontrada!"

    # Mostrar deeplink
    st.markdown("### 🔗 Enlace generado")
    st.write(result_text)
    st.code(deeplink, language='text')

    # Generar y mostrar código QR
    generate_qr_code(deeplink, "qr/mi_codigo_qr.png")
    qr_img = Image.open("qr/mi_codigo_qr.png")

    st.markdown("### 📱 Código QR del enlace")
    st.image(qr_img, caption="Escanea para abrir el enlace", use_container_width=300)