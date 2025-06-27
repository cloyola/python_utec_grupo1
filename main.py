import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
from langchain.chains import LLMChain
from generate_qr import generate_qr_code
from generate_deeplink import generate_deeplink_simple
from generate_description import describe_image
from generate_text import llm, prompt, parser

def pipeline(image_path):
    empresas = pd.read_csv("content/empresas.csv")
    empresas_df = empresas["empresas"]

    #Generar base64 de la imagen
    #image_path = "img/WhatsApp Image 2025-05-15 at 9.56.31 PM (1).jpeg" # TO-DO:extraer imagen dinámicamente
    recibo = describe_image(image_path)

    #Describir la imagen generada
    chain = LLMChain(llm=llm, prompt=prompt, output_parser=parser)
    result = chain.invoke({"recibo": recibo, "proveedores":empresas_df})

    link = generate_deeplink_simple(result["text"]["proveedor"], result["text"]["numero_suministro"])
    return link
    """ generate_qr_code(link, "qr/mi_codigo_qr.png")

    img = mpimg.imread('qr/mi_codigo_qr.png')
    # Display the image
    plt.imshow(img)
    plt.axis('off')
    plt.show() """