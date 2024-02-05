import azure.functions as func
import logging
import time
from .conexion_websocket import on_message


async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    start_time = time.time()
    await on_message()
    end_time = time.time()
    execution_time = end_time - start_time
    return func.HttpResponse(f"Execution time: {execution_time} seconds")