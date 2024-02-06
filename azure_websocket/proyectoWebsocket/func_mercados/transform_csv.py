import pandas as pd
import numpy as np


def mark_and_filter_bad_data(df, df_final, df_websocket, ORDERS_PATH):
    # Agrega una nueva columna "Detalles" y establece su valor en una cadena vacía para los datos "malos"
    df_final['Detalles'] = ''
    df_final.loc[(df_final['Monto'] == '0') | (df_final['Monto'] == '-'), 'Detalles'] += 'Monto inválido - '
    df_final.loc[df_final['Tipo operación'] == '0', 'Detalles'] += 'Tipo operación inválido - '
    df_final.loc[df_final['Precio'] == '0', 'Detalles'] += 'Precio inválido - '

    for index, row in df_websocket.iterrows():
        if pd.isnull(row['Last']):
            df_final.loc[df_final['Nemotécnico'] == row['Symbol'], 'Detalles'] += 'Precio en linea no encontrado - '
    
    df_final['Detalles'] = df_final['Detalles'].str.rstrip(' - ')
    #df_final = df_final[df_final['Detalles'] != '']
    df_final.to_csv(ORDERS_PATH, sep=';', index=False)  # Escribe el DataFrame con la columna de detalles al archivo original

def transform_data(df):
    df['VISIBLE'] = ''
    df['VIG. HORA'] = ''
    df['VC'] = ''
    df['CORREDOR'] = ''
    df['FONDO'] = ''
    df = df[['Tipo operación', 'Nemotécnico', 'Precio', 'Monto', 'Cantidad', 'VISIBLE', 'Forma liquidación', 'Fecha vencimiento', 'VIG. HORA', 'VC', 'Cuenta', 'CORREDOR', 'FONDO']]
    df.columns = ['TIPO', 'NEMO', 'PRECIO', 'MONTO', 'CANTIDAD', 'VISIBLE', 'LIQUIDACIÓN', 'VIG.FECHA', 'VIG. HORA', 'VC', 'CLIENTE', 'CORREDOR', 'FONDO']
    return df

def update_prices(df, df_websocket):
    # Filtrar las filas con montos vacíos o iguales a "-"
    df = df[(df['MONTO'] != '-') & (df['MONTO'].notna())]

    # Continuar con el procesamiento como antes
    last_prices = df_websocket.set_index('Symbol')['Last'].to_dict()
    df['PRECIO'] = df['NEMO'].map(last_prices).fillna(df['PRECIO'])
    df['MONTO'] = pd.to_numeric(df['MONTO'], errors='coerce')
    df['PRECIO'] = pd.to_numeric(df['PRECIO'], errors='coerce')
    df['MONTO'] = df['MONTO'].fillna(0)
    df['PRECIO'] = df['PRECIO'].fillna(0)
    df['PRECIO'] = df['PRECIO'].replace(0, 1e-10)
    # Solo actualiza la cantidad si el monto y el precio son diferentes de 0
    df.loc[(df['MONTO'] != 0) & (df['PRECIO'] != 0), 'CANTIDAD'] = abs(np.floor(df['MONTO'] / df['PRECIO']).astype(int))
    df = df.loc[df['CANTIDAD'] != 0]
    return df

def write_new_orders(df, NEW_ORDERS_PATH):
    # Continuar con el procesamiento como antes
    df = df[df['PRECIO'] != 1e-10]
    df = df.drop(columns=['MONTO'])
    df.to_csv(NEW_ORDERS_PATH, sep=';', index=False)

def transform_and_merge(WEBSOCKET_FILE_PATH, ORDERS_PATH, NEW_ORDERS_PATH):
    df = pd.read_csv(ORDERS_PATH, sep=';')
    orders_final = df.copy()  # Creo una copia del DataFrame original
    df = transform_data(df)
    df_websocket = pd.read_excel(WEBSOCKET_FILE_PATH)
    df = update_prices(df, df_websocket)
    write_new_orders(df, NEW_ORDERS_PATH)
    mark_and_filter_bad_data(df, orders_final, df_websocket, ORDERS_PATH)