import json
from .constantes import SETTL_TYPE, SECURITY_TYPE, TRADE, BOOK, STATISTIC, SECURITY_EXCHANGE

def create_subscription_message(symbol, uid):
    return {
        "topic": "subscribe",
        "payload": {
            "symbol": symbol,
            "id": uid,
            "settlType": SETTL_TYPE,
            "securityType": SECURITY_TYPE,
            "trade": TRADE,
            "book": BOOK,
            "statistic": STATISTIC,
            "securityExchange": SECURITY_EXCHANGE
        }
    }

def create_unsubscription_message(uid):
    return {
        "topic": "unsubscribe",
        "payload": {
            "id": uid
        }
    }