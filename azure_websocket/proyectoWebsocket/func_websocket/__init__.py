import azure.functions as func
import logging
import time
from .conexion_websocket import on_message
import os
from .constantes import get_file_paths


async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    start_time = time.time()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    for date_str in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, date_str)
        # Verifica si la ruta es un directorio
        if os.path.isdir(path):
            # Llama a la función transform_orders
            WEBSOCKET_FILE_PATH, ORDERS_PATH, NEW_ORDERS_PATH = get_file_paths(date_str)
            await on_message(WEBSOCKET_FILE_PATH, ORDERS_PATH, NEW_ORDERS_PATH)


    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    return func.HttpResponse(f"Execution time: {execution_time} seconds")