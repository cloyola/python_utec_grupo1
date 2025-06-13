import pandas as pd
from generate_text import find_rows_by_service, find_rows_by_id

def generate_deeplink_simple(companyName, consumer = None):
  df = pd.read_csv("content/empresas_deeplink.csv")

  row_list = find_rows_by_id(df, companyName)
  row_df = pd.DataFrame(row_list)

  if companyName.lower() == "claro":
    if len(consumer) == 9:
      row = find_rows_by_service(row_df, "numero de telefono")
    elif len(consumer) == 8:
      row = find_rows_by_service(row_df, "dni")
    else:
      row = find_rows_by_service(row_df, "cod cliente")
  elif companyName.lower() == "movistar":
    if consumer.startswith("9") and len(consumer) == 9:
      row = find_rows_by_service(row_df, "movil")
    elif len(consumer) == 7:
      row = find_rows_by_service(row_df, "fijo")
    elif len(consumer) == 9:
      row = find_rows_by_service(row_df, "cuenta financiera")
    else:
      row = find_rows_by_service(row_df, "tv")
  elif companyName.lower() == "directv": #cobranza externa recargas direct tv postpago instalación directv
    if len(consumer) == 8: #38389127
      row = find_rows_by_service(row_df, "postpago")
    else:
      row = find_rows_by_service(row_df, "instalación directv")
  else:
    if row_list:
      row = [row_list[0]]
    else:
      print(f"No rows found for company: {companyName}") # Handle the case where no row was found by companyName
      return None # Or raise an error, depending on desired behavior

  if not row: # Check if 'row' is empty after filtering
      print(f"No specific service row found for {companyName} with provided consumer code.")
      return None

  selected_row = row[0] # TO DO
  
  if consumer == None: #Es deeplink sin codigo de pago
    return f"https://yape.com.pe/app/services-pay/pickService?logo=https://staceu2yapefrntp10.blob.core.windows.net/%24web/bill-payment/companies/{row[0]['image_name']}&companyId={row[0]['companyId']}&name={row[0]['name']}&serviceId={row[0]['serviceId']}"
  else:
    return f"https://yape.com.pe/app/services-pay/pickService?logo=https://staceu2yapefrntp10.blob.core.windows.net/%24web/bill-payment/companies/{row[0]['image_name']}&companyId={row[0]['companyId']}&name={row[0]['name']}&serviceId={row[0]['serviceId']}&consumerCode={consumer}"
