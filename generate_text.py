import pandas as pd
import unicodedata
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from rapidfuzz import process, fuzz
from logger import logger
#from langchain.globals import set_debug
import re

load_dotenv()
# set_debug(True)
groq_api_key = os.getenv("GROQ_API_KEY")

if groq_api_key is None:
    raise ValueError("La variable de entorno GROQ_API_KEY no está configurada.")

class ProviderGenerationScript(BaseModel):
    proveedor: str = Field(description="Este es el proveedor del recibo")

class IdentifierGenerationScript(BaseModel):
    identificador: str = Field(description="Este es el identificador del recibo")
    service_id: str = Field(description="Este es el ID del servicio identificado")

def find_rows_by_id(df, id, column_name):
  # Filtrar filas que coinciden con el nombre
  matching_rows = df[df[column_name].str.lower() == id.lower()]
  # Convertir filas filtradas a lista de diccionarios
  return matching_rows.to_dict(orient='records')

def find_rows_by_service(df, service):
  # Filtrar filas que coinciden con el nombre
  matching_rows = df[df['service'].str.lower() == service.lower()]
  # Convertir filas filtradas a lista de diccionarios
  return matching_rows.to_dict(orient='records')

def get_code_to_search(company):
    """
    Esta función encuentra el nombre para buscar el código de pago en un recibo

    Args: company (str): El nombre de la compañía.  
    Returns: str: El nombre del código a buscar.
    """
    df = pd.read_csv("content/empresas_deeplink.csv")
    return df[df['id']==company.lower()]['code_search'].values

def generate_service_list_text(services_df: pd.DataFrame) -> str:
    if services_df.empty:
        return "No hay servicios disponibles en este momento."

    output_text = "### Servicios Disponibles\n\n"
    output_text += "Aquí están los servicios disponibles para la compañía:\n\n"

    for index, row in services_df.iterrows():
        consumer_id = row["consumerIdentification"]
        service_id = row["service_id"]
        output_text += f"* **Identificación del código:** {consumer_id}, **ID del Servicio:** {service_id}\n"

    return output_text

def normalize(text):
    if pd.isna(text):
        return ""
    # Quitar tildes, convertir a minúsculas, eliminar signos y extras comunes
    text = unicodedata.normalize('NFKD', str(text)).encode('ASCII', 'ignore').decode('utf-8')
    text = text.lower().replace(".", "").replace(",", "").replace("s.a", "").replace("-", "").strip()
    return text

def find_closest_company(company_df, input_name, threshold=85, return_score=False): #Funciona para archivo deeplinks
    if company_df.empty or not input_name:
        return None
    logger.info(company_df["company_name"].tolist())

    logger.info(f"Input original: {input_name}")
    normalized_input = normalize(input_name)
    logger.info(f"Normalized input: {normalized_input}")

    # Paso 1: Búsqueda directa usando 'contains'
    contains_mask = company_df["company_name"].str.lower().str.contains(normalized_input, na=False)
    if contains_mask.any():
        idx = contains_mask.idxmax()
        result = company_df.loc[idx, "company_name"]
        logger.info(f"Encontró resultado por contains: {result}")
        return (result, idx) if return_score else result
    
    # Paso 2: Fuzzy matching si no encontró nada por 'contains'
    company_list = company_df["company_name"].tolist()
    normalized_choices = [normalize(name) for name in company_list]
    logger.info(f"Opciones normalizadas: {normalized_choices}")

    # Buscar con el threshold
    match_data = process.extractOne(normalized_input, normalized_choices, scorer=fuzz.token_sort_ratio)
    logger.info(f"Data que coincide: {match_data}")

    if match_data:
        match, score, _ = match_data
        if score >= threshold:
            index = normalized_choices.index(match)
            best_match = company_list[index]
            logger.info(f"Encontró resultado por best_match: {best_match}")
            return (best_match, score) if return_score else best_match
    return None

# - Columna "pattern_regular" tiene el formato regex con el que aparece el código.
TEMPLATE = """
A continuación se muestra el contenido de un recibo de servicio:

{recibo}

Tu tarea es identificar y extraer el nombre de la *empresa emisora* del recibo.

Puedes elegir únicamente entre los siguientes proveedores válidos:
{proveedores}

Importante:
- No agregues explicaciones, justificaciones ni comentarios adicionales.
- Devuelve exclusivamente el resultado en formato JSON, sin ningún texto antes o después.
- Si no encuentras un proveedor válido en el recibo, responde con null como valor.

El formato de salida debe ser el siguiente:
{format_instructions}
"""

parser= JsonOutputParser(pydantic_object=ProviderGenerationScript)

llm = ChatGroq(
    temperature=0,
    model_name="llama-3.3-70b-versatile", #llama3-8b-8192
    groq_api_key=groq_api_key
)

prompt = PromptTemplate(
    input_variables=["recibo", "proveedores"],
    template=TEMPLATE,
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# Variables para la extracción de la consulta precisa
TEMPLATE_ID = """
A continuación se muestra la información extraída de un recibo de servicio:

{recibo}

Tu tarea es extraer únicamente el valor del campo correspondiente al código del recibo, también conocido como identificador principal del cliente. Este dato puede estar etiquetado en el documento con alguno de los siguientes nombres:

{services}

No selecciones números asociados a otros campos como 'Número de suministro', 'Referencia de pago', 'N° de operación', 'Código de suministro', u otros que no estén explícitamente mencionados en la lista anterior.

Si encuentras un identificador que coincide con uno de los nombres proporcionados, **asegúrate de devolver también el 'service_id' asociado a ese nombre de identificador** tal como se indica en la lista.

Devuelve únicamente los valores en el siguiente formato JSON. *No escribas ninguna explicación o comentario*. Devuelve exclusivamente el JSON:

{format_instructions_id}
"""

parser_id = JsonOutputParser(pydantic_object=IdentifierGenerationScript)

llm_id = ChatGroq(
    temperature=0,
    model_name="llama-3.3-70b-versatile",
    groq_api_key=groq_api_key
)

prompt_id = PromptTemplate(
    input_variables=["recibo", "services"],
    template=TEMPLATE_ID,
    partial_variables={"format_instructions_id": parser_id.get_format_instructions()},
)