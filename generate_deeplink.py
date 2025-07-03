import pandas as pd
from generate_text import find_rows_by_service, find_rows_by_id, find_closest_company
from logger import logger

def generate_deeplink_simple(companyName, consumer = None):
  df = pd.read_csv("content/empresas_deeplink.csv")

  matched_name = find_closest_company(df, companyName)
  if not matched_name:
      print(f"No close match found for company: {companyName}")
      logger.warning(f"Company pending to add: {companyName}")
      return None

  row_list = find_rows_by_id(df, matched_name)
  row_df = pd.DataFrame(row_list)

  if matched_name.lower() == "claro":
    if len(consumer) == 9:
      row = find_rows_by_service(row_df, "numero de telefono")
    elif len(consumer) == 8:
      row = find_rows_by_service(row_df, "dni")
    else:
      row = find_rows_by_service(row_df, "cod cliente")
  elif matched_name.lower() == "movistar":
    if consumer.startswith("9") and len(consumer) == 9:
      row = find_rows_by_service(row_df, "movil")
    elif len(consumer) == 7:
      row = find_rows_by_service(row_df, "fijo")
    elif len(consumer) == 9:
      row = find_rows_by_service(row_df, "cuenta financiera")
    else:
      row = find_rows_by_service(row_df, "tv")
  elif matched_name.lower() == "directv": #cobranza externa recargas direct tv postpago instalación directv
    if len(consumer) == 8: #38389127
      row = find_rows_by_service(row_df, "postpago")
    else:
      row = find_rows_by_service(row_df, "instalación directv")
  else:
    if row_list:
      row = [row_list[0]]
    else:
      print(f"No rows found for company: {matched_name}") # Handle the case where no row was found by companyName
      logger.warning(f"Company pending to add: {companyName}")
      return None # Or raise an error, depending on desired behavior

  if not row: # Check if 'row' is empty after filtering
      print(f"No specific service row found for {companyName} with provided consumer code.")
      logger.warning(f"Any service for {companyName} company.")
      return None
  
  logger.info(f"Fila identificada {row}")

  logger.info(f"Fila usada {row[0]}")
  logger.info(f"Codigo de pago consumer {consumer}")
  
  if consumer == None: #Es deeplink sin codigo de pago
    return f"https://yape.com.pe/app/services-pay/pickService?logo=https://staceu2yapefrntp10.blob.core.windows.net/%24web/bill-payment/companies/{row[0]['image_name']}&companyId={row[0]['companyId']}&name={row[0]['name']}&serviceId={row[0]['serviceId']}"
  else:
    return f"https://yape.com.pe/app/services-pay/pickService?logo=https://staceu2yapefrntp10.blob.core.windows.net/%24web/bill-payment/companies/{row[0]['image_name']}&companyId={row[0]['companyId']}&name={row[0]['name']}&serviceId={row[0]['serviceId']}&consumerCode={consumer}"
