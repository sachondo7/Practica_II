import os

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
    ORDERS_PATH = os.path.join(DATA_DIR, "data", "orders.csv")
    OUTPUT_EXCEL_PATH = os.path.join(BASE_DIR, "data", "datos_websocket.xlsx")
    return WEBSOCKET_URL, OUTPUT_EXCEL_PATH, ORDERS_PATH




