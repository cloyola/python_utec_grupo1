import pandas as pd
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
import unicodedata
from fuzzywuzzy import process
from logger import logger
from langchain.globals import set_debug

set_debug(True)

class ProviderGenerationScript(BaseModel):
    proveedor: str = Field(description="Este es el proveedor del recibo")

class IdentifierGenerationScript(BaseModel):
    identificador: str = Field(description="Este es el identificador del recibo")

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

def normalize(text):
    if pd.isna(text):
        return ""
    # Quitar tildes, convertir a minúsculas, eliminar signos y extras comunes
    text = unicodedata.normalize('NFKD', str(text)).encode('ASCII', 'ignore').decode('utf-8')
    text = text.lower().replace(".", "").replace(",", "").replace("s.a", "").strip()
    return text

def find_closest_company(df, input_name, column_name, threshold=85): #Funciona para archivo deeplinks
    normalized_input = normalize(input_name)
    choices = df[column_name].dropna().unique()
    choices_normalized = [normalize(c) for c in choices]
    
    match, score = process.extractOne(normalized_input, choices_normalized)
    if score >= threshold:
        index = choices_normalized.index(match)
        best_match = choices[index]
        logger.warning(f"Input: {normalized_input}. Score {score}. Threshold: {threshold}. Best match: {best_match}")
        return best_match
    return None 

# - Columna "pattern_regular" tiene el formato regex con el que aparece el código.
TEMPLATE="""
Dado la informacion del siguiente recibo, necesito que me extraigas la empresa emisora
{recibo}
Tienes como opciones los siguientes proveedores: 
{proveedores}

El formato de salida debe ser el siguiente:{format_instructions}. """

parser= JsonOutputParser(pydantic_object=ProviderGenerationScript)

llm = ChatGroq(
    temperature=0,
    model_name="llama-3.3-70b-versatile", #llama3-8b-8192
    groq_api_key="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"
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

Tu tarea es **extraer únicamente el valor del campo correspondiente al código del recibo**, también conocido como identificador principal del cliente. Este dato puede estar etiquetado en el documento con alguno de los siguientes nombres:

{services}

**No selecciones números asociados a otros campos** como 'Número de suministro', 'Referencia de pago', 'N° de operación', 'Código de suministro', u otros que no estén explícitamente mencionados en la lista anterior.

Devuelve solo el valor asociado al campo válido, siguiendo exactamente este formato:
{format_instructions_id}
"""

parser_id = JsonOutputParser(pydantic_object=IdentifierGenerationScript)

llm_id = ChatGroq(
    temperature=0,
    model_name="llama-3.3-70b-versatile",
    groq_api_key="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"
)

prompt_id = PromptTemplate(
    input_variables=["recibo", "services"],
    template=TEMPLATE_ID,
    partial_variables={"format_instructions_id": parser_id.get_format_instructions()},
)