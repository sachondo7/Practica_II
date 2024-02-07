import pymssql
import pandas as pd
from data.config import DB_USERNAME, DB_PASSWORD, DB_SERVER, DB_DATABASE
from .excel_operations import estandarizar_fechas

def create_and_format_personalized_dataframes(query_templates, asesores_info):
    connection = pymssql.connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    cursor = connection.cursor()
    query_result_dict = {}
    try:
        for asesor in asesores_info:
            id_asesor = asesor['id_asesor']
            correo_destinatario = asesor['correo_destinatario']
            query_result_dict[correo_destinatario] = []
            for query_name, query_template in query_templates.items():
                # Sustituye los parámetros directamente utilizando el método 'execute'
                cursor.execute(query_template, (id_asesor,))
                rows = cursor.fetchall()
                df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
                formatos_posibles = ["%Y-%m-%d", "%d/%m/%Y", "%A, %d de %B de %Y"]
                estandarizar_fechas(df, formatos_posibles)
                query_result_dict[correo_destinatario].append(df)
    except pymssql.Error as e:
        print(f"Error de conexión a SQL Server: {e}")
    finally:
        if connection:
            connection.close()
    return query_result_dict

def create_universal_dataframe(query_universal, lista_correos):
    # Conectarse a la base de datos
    connection = pymssql.connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    cursor = connection.cursor()
    query_result_dict = {}
    try:
        for correo in lista_correos:
            query_result_dict[correo] = []
            for query_name, query in query_universal.items():
                # Sustituye los parámetros directamente utilizando el método 'execute'
                cursor.execute(query)
                rows = cursor.fetchall()
                df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
                formatos_posibles = ["%Y-%m-%d", "%d/%m/%Y", "%A, %d de %B de %Y"]
                estandarizar_fechas(df, formatos_posibles)
                query_result_dict[correo].append(df)

    except pymssql.Error as e:
        print(f"Error de conexión a SQL Server: {e}")
    finally:
        if connection:
            connection.close()
    return query_result_dict
