import base64
import os
from dotenv import load_dotenv
from io import BytesIO
#from dotenv import load_dotenv
from PIL import Image  # Importamos la clase Image de PIL para manejar imágenes
from langchain_groq import ChatGroq  # Importamos ChatGroq para interactuar con el modelo de lenguaje
from groq import Groq  # Importamos Groq para realizar consultas a la API

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if groq_api_key is None:
    raise ValueError("La variable de entorno GROQ_API_KEY no está configurada.")

def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def describe_image(image_path):
    """
    Esta función describe una imagen proporcionada en la ruta 'image_path'.
    Extrae información relevante del recibo, como el número de suministro,número de servicio, número de cliente y número de recibo.

    Args: image_path (str): La ruta de la imagen que se va a analizar.
    Returns: str: La descripción extraída de la imagen.
    """

    # Nombre del modelo de visión que se utilizará
    VISION_MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

    # Inicializamos el cliente de Groq con la clave de API
    client = Groq(api_key=groq_api_key)
    vision_model = VISION_MODEL_NAME

    # Abrimos la imagen desde la ruta proporcionada
    image = Image.open(image_path)

    # Codificamos la imagen en formato base64
    base64_image = encode_image(image)

    # Creamos una solicitud de completación al modelo de lenguaje
    completion = client.chat.completions.create(
        model=vision_model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extrae toda la información importante del recibo, poniendo especial énfasis en identificar el número de suministro, servicio, cliente ya que estos constituyen la entidad principal del documento y puede aparecer en un cuadrado que solo son números. Ten en cuenta que el nombre del proveedor podría aparecer como texto dentro de una imagen o logo."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        temperature=1, # Controla la aleatoriedad de la respuesta
        max_completion_tokens=1024, # Número máximo de tokens en la respuesta
    )

    # Retornamos el contenido de la respuesta generada
    return completion.choices[0].message.content