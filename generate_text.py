import pandas as pd
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

TEMPLATE="""
Dado la informacion del siguiente recibo, necesito que me extraigas la empresa emisora y el tipo de servicio
{recibo}

Tienes como opciones los siguientes proveedores {proveedores}

El formato de salida debe ser el siguiente:{format_instructions}. """

class ContentGenerationScript(BaseModel):
    numero_suministro: str = Field(description="Este es el numero de suministro del recibo")
    proveedor: str = Field(description="Este es el proveedor del recibo")

def find_rows_by_id(df, id):
  # Filtrar filas que coinciden con el nombre
  matching_rows = df[df['id'] == id.lower()]

  # Convertir filas filtradas a lista de diccionarios
  list_of_dicts = matching_rows.to_dict(orient='records')

  return list_of_dicts

def find_rows_by_service(df, service):
  # Filtrar filas que coinciden con el nombre
  matching_rows = df[df['service'] == service.lower()]

  # Convertir filas filtradas a lista de diccionarios
  list_of_dicts = matching_rows.to_dict(orient='records')

  return list_of_dicts


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
