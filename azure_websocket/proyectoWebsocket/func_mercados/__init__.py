import azure.functions as func
import logging
import time
import os
from .constantes import get_file_paths
from .transform_csv import transform_and_merge

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
            print("-----------------")
            print(f"ORDERS_PATH: {ORDERS_PATH}")
            print(f"NEW_ORDERS_PATH: {NEW_ORDERS_PATH}")
            #transform_and_merge(ORDERS_PATH, NEW_ORDERS_PATH, WEBSOCKET_FILE_PATH)

    end_time = time.time()
    execution_time = end_time - start_time
    return func.HttpResponse(f"Execution time: {execution_time} seconds")