import pandas as pd
import numpy as np
import datetime
import sys
import concurrent.futures
from .api.api_client import get_saldo_caja, get_cartera

def mark_and_filter_bad_data(token, df_final, df_websocket, ORDERS_PATH):
    # Agrega una nueva columna "Detalles" y establece su valor en una cadena vacía para los datos "malos"
    df_final['Detalles'] = ''
    df_final.loc[(df_final['Monto'] == '0') | (df_final['Monto'] == '-') 
                & (df_final['Tipo operación'] == 'C'), 'Detalles'] += 'Monto invalido - '
    df_final.loc[df_final['Tipo operación'] == '0', 'Detalles'] += 'Tipo operación invalido - '
    df_final.loc[df_final['Precio'] == '0', 'Detalles'] += 'Precio invalido - '
    for index, row in df_websocket.iterrows():
        if pd.isnull(row['Last']):
            df_final.loc[df_final['Nemotécnico'] == row['Symbol'], 'Detalles'] += 'Precio en linea no encontrado - '
    df_final['Monto'] = df_final['Monto'].str.replace(',', '.')
    df_final.loc[:, 'Monto'] = pd.to_numeric(df_final['Monto'], errors='coerce')
    df_malo = df_final[(df_final['Tipo operación'] != 'C') & (df_final['Tipo operación'] != 'V')]
    df_final_caja = df_final[df_final['Tipo operación'] == 'C']
    df_final_venta = df_final[df_final['Tipo operación'] == 'V']
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_caja = executor.submit(revisar_caja, token, df_final_caja)
        future_to_custodia = executor.submit(revisar_custodia, token, df_final_venta)
        df_final_caja = future_to_caja.result()
        df_final_venta = future_to_custodia.result()
    df_final = pd.concat([df_malo, df_final_caja, df_final_venta])
    df_final['Detalles'] = df_final['Detalles'].str.rstrip(' - ')
    df_final.to_csv(ORDERS_PATH, sep=';', index=False)  # Escribe el DataFrame con la columna de detalles al archivo original
    return df_final

def revisar_caja(token, df_final):
    today = datetime.date.today().strftime("%Y/%m/%d")
    # Crear un diccionario que mapea cada cuenta a la suma de sus montos
    account_to_amount = df_final[df_final['Tipo operación'] == 'C'].groupby('Cuenta')['Monto'].sum().to_dict()
    print(account_to_amount, flush=True)
    account_to_balance = {}
    i = 0
    for account in account_to_amount.keys():
        print(f"Getting saldo caja for {account} on {today}: Iteracion {i}", flush=True)
        response = get_saldo_caja(token, account, today)
        if response is None or len(response) == 0:
            account_to_balance[account] = None
        else:
            account_to_balance[account] = response[0]['monto']
        i += 1
    for index, row in df_final.iterrows():
        if row['Detalles'] == '':
            if account_to_balance[row['Cuenta']] is None:
                df_final.loc[index, 'Detalles'] += 'Error al obtener caja - '
            elif account_to_balance[row['Cuenta']] < account_to_amount[row['Cuenta']]:
                df_final.loc[index, 'Detalles'] += f"Saldo insuficiente: Saldo actual: {account_to_balance[row['Cuenta']]}, Saldo requerido: {account_to_amount[row['Cuenta']]}"
                print(f"Saldo insuficiente para la cuenta {row['Cuenta']}. Saldo actual: {account_to_balance[row['Cuenta']]}, Saldo requerido: {account_to_amount[row['Cuenta']]}", flush=True)
    return df_final

def revisar_custodia(token, df_final):
    today = datetime.date.today().strftime("%Y/%m/%d")
    # Crear un diccionario que mapea cada cuenta a la suma de sus montos
    account_to_amount = df_final[df_final['Tipo operación'] == 'V'].groupby('Cuenta')['Monto'].sum().to_dict()
    print(account_to_amount, flush=True)
    account_to_balance = {}
    i = 0
    for account in account_to_amount.keys():
        #print(f"Getting custodia for {account} on {today}: Iteracion {i}", flush=True)
        response = get_cartera(token, account, today)
        if response is None or len(response) == 0:
            print(f'Getting custodia for :{account}, ERROR AL OBTENER CUSTODIA Iteracion {i}', flush=True)
            account_to_balance[account] = None
        else: 
            nemotecnico_to_cantidad = {item['nemotecnico']: item['cantidad'] for item in response}
            account_to_balance[account] = nemotecnico_to_cantidad
            print(f'Getting custodia for :{account}, nemo: {nemotecnico_to_cantidad} Iteracion {i}', flush=True)
        i += 1
    print(account_to_balance, flush=True)
    for index, row in df_final.iterrows():
        if row['Detalles'] == '':
            if account_to_balance[row['Cuenta']] is None:
                df_final.loc[index, 'Detalles'] += 'Error al obtener custodia - '
            else: 
                balance = account_to_balance.get(row['Cuenta'], {}).get(row['Nemotécnico'], 0)
                if balance < row['Cantidad']:
                    df_final.loc[index, 'Detalles'] += f"Saldo insuficiente: Saldo actual: {balance}, Saldo requerido: {row['Cantidad']}"
                    print(f"Saldo insuficiente para la cuenta {row['Cuenta']}. Saldo actual: {balance}, Saldo requerido: {row['Cantidad']}", flush=True)
    return df_final
    

def transform_data(df):
    df['VISIBLE'] = ''
    df['VIG. HORA'] = ''
    df['VC'] = ''
    df['CORREDOR'] = ''
    df['FONDO'] = ''
    df = df[['Tipo operación', 'Nemotécnico', 'Precio', 'Monto', 'Cantidad', 'VISIBLE', 'Forma liquidación', 'Fecha vencimiento', 'VIG. HORA', 'VC', 'Cuenta', 'CORREDOR', 'FONDO', 'Detalles']]
    df.columns = ['TIPO', 'NEMO', 'PRECIO', 'MONTO', 'CANTIDAD', 'VISIBLE', 'LIQUIDACIÓN', 'VIG.FECHA', 'VIG. HORA', 'VC', 'CLIENTE', 'CORREDOR', 'FONDO', 'DETALLES']
    return df

def update_prices(df, df_websocket):
    # Filtrar las filas con montos vacíos o iguales a "-"
    df = df[(df['MONTO'] != '-') & (df['MONTO'].notna())]

    # Continuar con el procesamiento como antes
    last_prices = df_websocket.set_index('Symbol')['Last'].to_dict()
    df.loc[:, 'PRECIO'] = df['NEMO'].map(last_prices).fillna(df['PRECIO'])
    df.loc[:, 'MONTO'] = pd.to_numeric(df['MONTO'], errors='coerce')
    df.loc[:, 'PRECIO'] = pd.to_numeric(df['PRECIO'], errors='coerce')
    df.loc[:, 'MONTO'] = df['MONTO'].fillna(0)
    df.loc[:, 'PRECIO'] = df['PRECIO'].fillna(0)
    df.loc[:, 'PRECIO'] = df['PRECIO'].replace(0, 1e-10)
    # Solo actualiza la cantidad si el monto y el precio son diferentes de 0 y el tipo es "C"
    df.loc[(df['MONTO'] != 0) & (df['PRECIO'] != 0) & (df['TIPO'] == "C"), 'CANTIDAD'] = abs(np.floor(df['MONTO'] / df['PRECIO']).astype(int))
    df = df.loc[df['CANTIDAD'] != 0]
    return df

def write_new_orders(df, NEW_ORDERS_PATH):
    # Continuar con el procesamiento como antes
    df = df[df['PRECIO'] != 1e-10]
    df = df.drop(columns=['MONTO'])
    # Filtrar las filas que no tienen detalles
    df = df[df['DETALLES'].isna() | (df['DETALLES'] == '')]
    df.to_csv(NEW_ORDERS_PATH, sep=';', index=False)

def transform_and_merge(token, WEBSOCKET_FILE_PATH, ORDERS_PATH, NEW_ORDERS_PATH):
    df = pd.read_csv(ORDERS_PATH, sep=';')
    orders_final = df.copy() 
    df_websocket = pd.read_excel(WEBSOCKET_FILE_PATH)
    orders_final = mark_and_filter_bad_data(token, orders_final, df_websocket, ORDERS_PATH)
    orders_final = transform_data(orders_final)
    orders_final = update_prices(orders_final, df_websocket)
    write_new_orders(orders_final, NEW_ORDERS_PATH)