import os

# WebSocket URL


def get_file_paths(date_str):
    WEBSOCKET_URL = "ws://10.0.1.8:8086/websocket"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data", date_str)
    WEBSOCKET_FILE_PATH = os.path.join(BASE_DIR, "datos_websocket.xlsx")
    ORDERS_PATH = os.path.join(DATA_DIR, "orders.csv")
    NEW_ORDERS_PATH = os.path.join(DATA_DIR, f"new_orders_{date_str}_11.00.csv")
    return WEBSOCKET_URL, WEBSOCKET_FILE_PATH, ORDERS_PATH, NEW_ORDERS_PATH
