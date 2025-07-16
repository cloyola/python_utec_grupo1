import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
from langchain.chains import LLMChain
from generate_qr import generate_qr_code
from generate_deeplink import generate_deeplink_simple
from generate_description import describe_image
from generate_text import llm, prompt, parser, llm_id, prompt_id, parser_id, find_closest_company, generate_service_list_text
from logger import logger

def pipeline(image_path):
    logger.info("Iniciando módulo: main.py")
    logger.info("Iniciando función: pipeline")
    
    #Generar base64 de la imagen
    recibo = describe_image(image_path)
    #logger.info(f"Texto generado del recibo {recibo}") #TEMP Logger
    logger.info(f"Imagen convertida a base64")

    #Extraer la lista de proveedores posibles
    company = pd.read_csv("content/empresas.csv")
    providers_list = company["company_name"].dropna().unique()
    providers_list = "\n\n".join(providers_list)

    #Encontrar el proveedor del servicio
    chain = LLMChain(llm=llm, prompt=prompt, output_parser=parser)
    result_recibo = chain.invoke({"recibo": recibo, "proveedores": providers_list})
    #logger.info(f"El resultado del recibo (proveedor) es {result_recibo}") #TEMP Logger
    logger.info("Se obtuvo resultado del LLM para reconocer el proveedor")

    #Obtenemos el proveedor que más se asemeje de la lista
    proveedor_normalized = find_closest_company(company, result_recibo["text"]["proveedor"])
    logger.info(f"El proveedor normalizado es {proveedor_normalized}") #TEMP Logger
    
    #Obtener los servicios
    services = pd.read_csv("content/services.csv")
    services_df = services[["company_name", "service_id", "consumerIdentification"]]

    #Normalizar el servicio encontrado
    services_identifier = generate_service_list_text(services_df[services_df["company_name"]==proveedor_normalized][["consumerIdentification","service_id"]]) #traer la lista de servicios disponibles
    logger.info(f"Los servicios identificados para ese proveedor normalizado son {services_identifier}") #TEMP Logger

    #Encontrar el código de pago dentro del servicio
    chain_id = LLMChain(llm=llm_id, prompt=prompt_id, output_parser=parser_id)
    result_id = chain_id.invoke({"recibo": recibo, "services":services_identifier})
    #logger.info(f"El resultado del segundo prompt es {result_id}") #TEMP Logger
    logger.info("Se obtuvo resultado del LLM para reconocer el servicio")

    #Generación del deeplink
    link = generate_deeplink_simple(proveedor_normalized, result_id["text"]["service_id"], result_id["text"]["identificador"])
    logger.info("Proceso finalizado")
    return link