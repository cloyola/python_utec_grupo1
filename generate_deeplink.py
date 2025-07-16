import pandas as pd
from logger import logger
from generate_text import normalize

def generate_deeplink_simple(companyName, service_id, consumer = None):
  logger.info(f"Iniciando módulo: generate_deeplink.py")
  logger.info(f"Iniciando función: generate_deeplink_simple")

  company_df = pd.read_csv("content/empresas.csv")
    
  company_selected = company_df[company_df["company_name"] == companyName]
  logger.info(f"La companía seleccionada es: {company_selected}")
  # Verifica que encontró al menos una coincidencia
  if company_selected.empty:
      raise ValueError(f"No se encontró la empresa '{companyName}' en el archivo empresas.csv")

  # Extrae los valores deseados de la primera fila coincidente
  company_id = company_selected.iloc[0]["company_id"]
  ruta_logo = company_selected.iloc[0]["ruta_logo_deeplink"]
  logger.info(f"Codigo de pago consumer {normalize(consumer)}")
  
  if consumer == None: #Es deeplink sin codigo de pago
    deeplink = f"https://yape.com.pe/app/services-pay/pickService?logo={ruta_logo}&companyId={company_id}&name={companyName}&serviceId={service_id}"
  else:
    deeplink = f"https://yape.com.pe/app/services-pay/pickService?logo={ruta_logo}&companyId={company_id}&name={companyName}&serviceId={service_id}&consumerCode={normalize(consumer)}"
  
  logger.info(f"Deeplink generado: {deeplink}")

  return deeplink