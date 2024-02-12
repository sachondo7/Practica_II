import requests
import os
import sys

def authenticate():
    api_url = os.environ['API_AUTHENTICATE_URL']
    api_username = os.getenv('API_USERNAME')
    api_password = os.getenv('API_PASSWORD')
    response = requests.post(
        api_url,
        json={
            "userName": api_username,
            "password": api_password
        }
    )
    if response.status_code == 200:
        return response.json()['token']
    else:
        return None

def refresh_token(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    api_refresh_token_url = os.getenv('API_REFRESH_TOKEN_URL')
    response = requests.get(api_refresh_token_url, headers=headers)
    if response.status_code == 200:
        print("Token refreshed")
        return response.json()
    else:
        return None


def get_saldo_caja(token, num_cuenta, fecha):
    url_caja = os.environ['API_CAJA_URL']
    url_caja = f"{url_caja}?NumCuenta={num_cuenta}&Fecha={fecha}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url_caja, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_cartera(token, numCuenta, fecha): 
    url_cartera = os.environ['API_CARTERA_URL']
    url_cartera = f"{url_cartera}?Fecha={fecha}&NumCuenta={numCuenta}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url_cartera, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
