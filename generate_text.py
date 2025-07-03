import pandas as pd
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
import unicodedata
from fuzzywuzzy import process

class ContentGenerationScript(BaseModel):
    numero_suministro: str = Field(description="Este es el numero de suministro del recibo")
    proveedor: str = Field(description="Este es el proveedor del recibo")

def find_rows_by_id(df, id):
  # Filtrar filas que coinciden con el nombre
  matching_rows = df[df['id'].str.lower() == id.lower()]
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
    text = text.lower().replace(".", "").replace(",", "").replace(" s.a", "").strip()
    return text

def find_closest_company(df, input_name, threshold=85):
    normalized_input = normalize(input_name)
    choices = df['id'].dropna().unique()
    choices_normalized = [normalize(c) for c in choices]
    
    match, score = process.extractOne(normalized_input, choices_normalized)
    if score >= threshold:
        index = choices_normalized.index(match)
        best_match = choices[index]
        return best_match
    return None


TEMPLATE="""
Dado la informacion del siguiente recibo, necesito que me extraigas la empresa emisora y el código de pago
{recibo}

Tienes como opciones los siguientes proveedores:
- Columna "empresas": Nombre de los proveedores
- Columna "consumer": Nombre con el que aparece el código en el recibo
- Columna "pattern_regular" tiene el formato regex con el que aparece el código.
Fuente: {proveedores}

El formato de salida debe ser el siguiente:{format_instructions}. """

parser= JsonOutputParser(pydantic_object=ContentGenerationScript)

llm = ChatGroq(
    temperature=0,
    model_name="llama3-8b-8192",
    groq_api_key="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"
)

prompt = PromptTemplate(
    input_variables=["recibo","proveedores"],
    template=TEMPLATE,
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
