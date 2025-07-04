import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
from langchain.chains import LLMChain
from generate_qr import generate_qr_code
from generate_deeplink import generate_deeplink_simple
from generate_description import describe_image
from generate_text import llm, prompt, parser, llm_id, prompt_id, parser_id, find_closest_company
from logger import logger

def pipeline(image_path):
    #Generar base64 de la imagen
    recibo = describe_image(image_path)
    logger.info(f"Texto generado del recibo {recibo}") #TEMP Logger

    #Extraer la lista de proveedores posibles
    empresas = pd.read_csv("content/empresas.csv")
    proveedores_df = empresas[["empresas"]].values

    #Encontrar el proveedor del servicio
    chain = LLMChain(llm=llm, prompt=prompt, output_parser=parser)
    result_recibo = chain.invoke({"recibo": recibo, "proveedores": proveedores_df})
    logger.info(f"El resultado del recibo (proveedor) es {result_recibo}") #TEMP Logger
    
    #Obtener el identificador
    empresas_df = empresas[["empresas", "identificador"]]
    proveedor_normalized = find_closest_company(empresas_df, result_recibo["text"]["proveedor"], "empresas")
    logger.info(f"El proveedor normalizado es {proveedor_normalized}") #TEMP Logger

    #Normalizar el servicio encontrado
    services_identifier = empresas_df[empresas_df["empresas"]==proveedor_normalized]["identificador"].values
    logger.info(f"Los servicios identificados para ese proveedor normalizado son {services_identifier}") #TEMP Logger

    #Encontrar el código de pago dentro del servicio
    chain_id = LLMChain(llm=llm_id, prompt=prompt_id, output_parser=parser_id)
    result_id = chain_id.invoke({"recibo": recibo, "services":services_identifier})
    logger.info(f"El resultado del segundo prompt es {result_id}") #TEMP Logger

    #Generación del deeplink
    link = generate_deeplink_simple(result_recibo["text"]["proveedor"], result_id["text"]["identificador"])
    return link