import os

# WebSocket URL
WEBSOCKET_URL = "ws://10.0.1.8:8086/websocket"

def get_file_paths(date_str):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data", date_str)
    WEBSOCKET_FILE_PATH = os.path.join(BASE_DIR, "datos_websocket.xlsx")
    ORDERS_PATH = os.path.join(DATA_DIR, "orders_{}_11.00.csv".format(date_str))
    NEW_ORDERS_PATH = os.path.join(DATA_DIR, "new_orders_{}_11.00.csv".format(date_str))
    return WEBSOCKET_FILE_PATH, ORDERS_PATH, NEW_ORDERS_PATH
