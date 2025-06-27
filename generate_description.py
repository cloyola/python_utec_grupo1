import base64
from io import BytesIO
#from dotenv import load_dotenv
from PIL import Image  # Importamos la clase Image de PIL para manejar imágenes
from langchain_groq import ChatGroq  # Importamos ChatGroq para interactuar con el modelo de lenguaje
from groq import Groq  # Importamos Groq para realizar consultas a la API

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
    client = Groq(api_key='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')
    vision_model = VISION_MODEL_NAME

    # Abrimos la imagen desde la ruta proporcionada
    image = Image.open(image_path)

    # Codificamos la imagen en formato base64
    base64_image = encode_image(image)

    # Creamos una solicitud de completación al modelo de lenguaje
    # TO DO: Agregar casos de error para mejorar el prompt
    # Revisar casos en https://docs.google.com/spreadsheets/d/1V6NJeVhI53kzcUQPC_iwgI6l3hs05rnR5ayl1R-Ydnk/edit?usp=sharing
    completion = client.chat.completions.create(
        model=vision_model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extrae toda la información posible del recibo, poniendo especial énfasis en identificar el número de suministro, número de servicio, número de cliente o número de recibo, ya que estos constituyen la entidad principal del documento. Ten en cuenta que el nombre del proveedor podría aparecer como texto dentro de una imagen o logo."},
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