import logging
import sys

logger = logging.getLogger("yape_scan")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    # Crear handler para escribir en consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Crear handler para escribir en archivo
    file_handler = logging.FileHandler("yape_scan.log")
    file_handler.setLevel(logging.DEBUG)

    # Crear formato de logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Agregar handlers al logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)