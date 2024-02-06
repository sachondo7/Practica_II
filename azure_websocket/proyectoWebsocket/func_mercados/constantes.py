import os
import pandas as pd
import sys
from datetime import datetime
from shutil import copyfile
import glob

def get_file_paths(date_str):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data", date_str)
    WEBSOCKET_FILE_PATH = glob.glob(os.path.join(DATA_DIR, "datos_websocket*.xlsx"))
    if not WEBSOCKET_FILE_PATH:
        raise FileNotFoundError("No se encontró el archivo de datos del websocket")
    WEBSOCKET_FILE_PATH = WEBSOCKET_FILE_PATH[0]
    ORDERS_PATH = os.path.join(DATA_DIR, "orders_{}_11.00.csv".format(date_str))

    # Obtener la hora actual y formatearla como una cadena de texto
    current_time = datetime.now().strftime("%H.%M")
    
    ORDER_DETAILS_PATH = os.path.join(DATA_DIR, "order_details_{}_{}.csv".format(date_str, current_time))  # Nuevo archivo
    NEW_ORDERS_PATH = os.path.join(DATA_DIR, "new_orders_{}_{}.csv".format(date_str, current_time))

    # Eliminar archivos antiguos
    for filename in os.listdir(DATA_DIR):
        if filename.startswith("order_details_") or filename.startswith("new_orders_"):
            os.remove(os.path.join(DATA_DIR, filename))

    # Copiar ORDERS_PATH a ORDER_DETAILS_PATH
    try:
        copyfile(ORDERS_PATH, ORDER_DETAILS_PATH)
    except IOError as e:
        print(f"Unable to copy file. {e}")
    except:
        print("Unexpected error:", sys.exc_info())

    # Crear NEW_ORDERS_PATH
    pd.DataFrame().to_csv(NEW_ORDERS_PATH)

    return WEBSOCKET_FILE_PATH, ORDER_DETAILS_PATH, NEW_ORDERS_PATH  # Devolver la ruta del nuevo archivo