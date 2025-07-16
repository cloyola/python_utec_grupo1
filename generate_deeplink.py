import pandas as pd
from logger import logger
from generate_text import normalize
import urllib.parse

def generate_deeplink_simple(companyName, service_id, consumer = None):
  logger.info(f"Iniciando módulo -> función: generate_deeplink.py -> generate_deeplink_simple")

  company_df = pd.read_csv("content/empresas.csv")
  company_selected = company_df[company_df["company_name"] == companyName]
  logger.info(f"La companía seleccionada es: {company_selected}")
  # Verifica que encontró al menos una coincidencia
  if company_selected.empty:
      raise ValueError(f"No se encontró la empresa '{companyName}' en el archivo empresas.csv")

  # Extrae los valores deseados de la primera fila coincidente
  company_id = company_selected.iloc[0]["company_id"]
  ruta_logo = company_selected.iloc[0]["ruta_logo_deeplink"]
  consumer_nomalized = normalize(consumer)
  logger.info(f"Codigo de pago consumer {consumer_nomalized}")
  company_encoded = urllib.parse.quote(companyName, safe='')
  
  if consumer == None: #Es deeplink sin codigo de pago
    deeplink = f"https://yape.com.pe/app/services-pay/pickService?logo={ruta_logo}&companyId={company_id}&name={company_encoded}&serviceId={service_id}"
  else:
    deeplink = f"https://yape.com.pe/app/services-pay/pickService?logo={ruta_logo}&companyId={company_id}&name={company_encoded}&serviceId={service_id}&consumerCode={consumer_nomalized}"
  
  logger.info(f"Deeplink generado: {deeplink}")

  return deeplink