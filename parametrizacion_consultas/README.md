# Configuración inicial

Para configurar correctamente este proyecto, necesitará crear una carpeta llamada data en el directorio raíz del proyecto. Dentro de esta carpeta, deberá crear los siguientes archivos:

## `__init__.py`
Este archivo debe ir vacío para que los directorios sean identificados como paquetes. 

## config.py 

Este archivo debe contener la siguiente información:

```
DB_SERVER = 'database_server'
DB_DATABASE = 'your_database'
DB_USERNAME = 'your_username'
DB_PASSWORD = 'your_password'
SMTP_SERVER = 'your_smtp_server'
SMTP_PORT = 'your_port'
SMTP_USER = 'your_smtp_user'
SMTP_PASSWORD = 'your_smtp_password'
LOGO_URL = 'https://www.vectorcapital.cl/wp-content/uploads/2020/08/Logo_VectorC2020.png'
HTML_CONTENT = 'your_html_content'
```

## mails.py 

Este archivo debe contener las siguientes listas siguiendo el mismo formato: 

```
asesores_info = [
    {'id_asesor': 'asesor_id', 'correo_destinatario': 'asesor_email'}, ... 
    {'id_asesor': 'asesor_id', 'correo_destinatario': 'asesor_email'}, ... 
    # Y así con cuantos asesores y correos se necesite 
] 

lista_correos = ["email1", "email2", ...]
```

## queries.py 

Este archivo debe contener las consultas que se quieran realizar siguiendo este mismo formato: 

```
query_templates = {
    'query_1': """
    -- Aquí va tu primera consulta SQL 
    """,
    'query_2' : """
    -- Aquí va tu segunda consulta SQL
    """,
    ...
}

query_universal = """
    -- Aquí va tu consulta SQL universal
"""
```
