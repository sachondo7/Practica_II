import os
from datetime import datetime

# WebSocket URL
WEBSOCKET_URL = "ws://10.0.1.8:8086/websocket"

# Parameters for the subscription message
SETTL_TYPE = "T2"
SECURITY_TYPE = "CS"
TRADE = False
BOOK = False
STATISTIC = True
SECURITY_EXCHANGE = "BCS"


def get_file_paths(date_str):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data", date_str)
    ORDERS_PATH = os.path.join(DATA_DIR, "orders_{}_11.00.csv".format(date_str))
    current_time = datetime.now().strftime("%H.%M")
    OUTPUT_EXCEL_PATH = os.path.join(DATA_DIR, "datos_websocket_{}_{}.xlsx".format(date_str, current_time))
    # Eliminar archivos antiguos
    for filename in os.listdir(DATA_DIR):
        if filename.startswith("datos_websocket_"):
            os.remove(os.path.join(DATA_DIR, filename))

            

    return WEBSOCKET_URL, OUTPUT_EXCEL_PATH, ORDERS_PATH





    





