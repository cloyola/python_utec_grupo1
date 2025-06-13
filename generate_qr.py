import qrcode

def generate_qr_code(url, output_file="qrcode.png"):
    """
    Genera un código QR a partir de un enlace web y guarda la imagen en un archivo.

    Args:
        url (str): El enlace web que se convertirá en código QR.
        output_file (str): El nombre del archivo donde se guardará la imagen QR (default: 'qrcode.png').
    """
    # Crear el objeto QRCode con configuración básica
    qr = qrcode.QRCode(
        version=1,  # tamaño del código QR (1 es pequeño, 40 es grande)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # nivel de corrección de errores
        box_size=10,  # tamaño de cada caja en pixeles
        border=4,  # grosor del borde (en cajas)
    )

    # Agregar la URL al código QR
    qr.add_data(url)
    qr.make(fit=True)

    # Crear la imagen del código QR
    img = qr.make_image(fill_color="black", back_color="#ffffff")

    # Guardar la imagen en un archivo
    img.save(output_file)
    #print(f"Código QR generado y guardado en {output_file}")