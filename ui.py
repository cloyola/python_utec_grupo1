import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import streamlit as st
from PIL import Image
from langchain.chains import LLMChain
from generate_qr import generate_qr_code
from main import pipeline

st.set_page_config(
    page_title="Data Visualization Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Data Visualization Dashboard")
st.markdown("Explore different types of graphs and charts in Streamlit")

image_file = st.file_uploader("Upload an image",type=["jpg","jpeg","png"])
if image_file:
    image = Image.open(image_file)
    st.markdown("### 📷 Imagen subida")
    st.image(image, caption="Uploaded Image", use_column_width=500)
    
    # Procesar imagen
    deeplink = pipeline(image_file)
    print(deeplink)

    # Mostrar deeplink
    st.markdown("### 🔗 Enlace generado")
    st.code(deeplink, language='text')

    # Generar y mostrar código QR
    generate_qr_code(deeplink, "qr/mi_codigo_qr.png")
    qr_img = Image.open("qr/mi_codigo_qr.png")

    st.markdown("### 📱 Código QR del enlace")
    st.image(qr_img, caption="Escanea para abrir el enlace", width=300)