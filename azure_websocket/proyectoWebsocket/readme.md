# Documentación del Proyecto

## Descripción

Este proyecto es una combinación de código JavaScript y Python, diseñado para trabajar con Azure Functions. 
Se compone de dos partes principales: `func_mercados` y `func_websocket`.

## Instalación

Para instalar las librerías, primero, navega a la raíz de tu proyecto en la terminal. 
Luego, sigue estos pasos:

1. Instala las dependencias de JavaScript con npm:
    ` npm install `

2. Instala las dependencias de Python con pip:
    ` pip install -r requirements.txt `
Este comando leerá el archivo requirements.txt en tu proyecto y descargará todas las dependencias necesarias.

3. Instalar extensión de Azure Tools en VSCode y luego ejecutar: 
    `npm install -g azure-functions-core-tools@4 --unsafe-perm true`

4. Configurar archivo `local.settings.json`, asegurate de agregar las credenciales en la parte de "Values":

```
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
    "AzureWebJobsStorage": "", 
    "API_USERNAME": {username},
    "API_PASSWORD": {password}, 
    "API_AUTHENTICATE_URL": "https://apiwebcbvoultechcertificacion.azurewebsites.net/api/publicapi/shared/auth/signin",
    "API_REFRESH_TOKEN_URL": "https://apiwebcbvoultechcertificacion.azurewebsites.net/api/publicapi/shared/auth/RefreshToken",
    "API_CAJA_URL": "https://apiwebcbvoultechcertificacion.azurewebsites.net/api/publicapi/creasys/Cajas/ConSaldoOnline",
    "API_CARTERA_URL": "https://apiwebcbvoultechcertificacion.azurewebsites.net/api/publicapi/creasys/Cartera"
  }
}
```

## Ejecución del código 

5. Una vez instaladas las librerías, debes dirigirte a el directorio principal e iniciar la función de azure localmente.  
    ` func start `

6. Una vez que el servidor de funciones esté en marcha, puedes abrir las URLs de las funciones en tu navegador para ejecutarlas. 
Por ejemplo, si tienes una función llamada `func_mercados` y otra llamada `func_websocket`, puedes abrir las siguientes URLs en tu navegador:

    ``` 
    http://localhost:7071/api/func_websocket
    http://localhost:7071/api/func_mercados
    ```

Por la manera que está construido el programa, es necesario ejecutar primero func_websocket y luego func_mercado para que el programa funcione como se espera. 


## Estructura de Directorios

```
├── .DS_Store
├── .funcignore
├── .gitignore
├── .vscode
│   ├── extensions.json
│   ├── launch.json
│   ├── settings.json
│   └── tasks.json
├── data
│   ├── {fecha}
│   │   ├── datos_websocket_{fecha}.xlsx
│   │   ├── orders_{fecha}.csv
│   │   ├── orders_details_{fecha}.csv
│   │   └── new_orders_{fecha}.csv
│   ├── carga_automatica_final (1).bpm
│   └── FORMATO_CARGA_AUTOMATICA.xlsx
├── func_mercados
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── api_client.py
│   ├── carga_automatica_final (1).bpm
│   ├── __pycache__
│   ├── constantes.py
│   ├── function.json
│   └── transform_csv.py
├── func_websocket
│   ├── __init__.py
│   ├── __pycache__
│   ├── conexion_websocket.py
│   ├── constantes.py
│   ├── function.json
│   ├── messages.py
│   └── utils.py
├── host.json
├── package.json
├── readme.md
└── requirements.txt
```

### func_websocket

Esta parte del proyecto se encarga de manejar las conexiones WebSocket para así obtener los precios en línea de los distintos nemos. 
Para que funcione correctamente, debes asegurarte de tener dentro del directorio data un subdirectorio con la fecha del día que estes ejecutando el programa. Este subdirectorio tambien debe contener el csv con las órdenes de compra de ese día. 
Por ejemplo si es 08 de febrero de 2024, el subdirectorio dentro de data debiese llamarse **20240208**.
La función principal se define en `__init__.py`. 
Una vez ejecutada la función, se creará solo dentro del directorio de la fecha un nuevo archivo excel **datos_websocket_{fecha}.xlsx** el cual contiene todos los nemos de las órdenes transadas ese día con sus respectivos precios en línea. 

### func_mercados

Esta parte del proyecto se encarga de transformar y fusionar archivos CSV. 
Para que funcione correctamente, también debe existir el subdirectorio con la fecha del día que estes ejecutando el programa, el cual ahora tengra el csv de las órdenes de ese día junto a los datos obtenidos del websocket ese día. 
La función principal se define en `__init__.py`. 
Una vez ejecutada, creará 2 nuevos archivos csv dentro del subdirectorio fecha: 
    1. **orders_details_{fecha}.csv**: Contiene todas las órdenes originales más los detalles de los errores de las que no pudieron ser procesadas. 
    2. **new_orders_{fecha}.csv**: Contiene todas las órdenes que pudieron ser procesadas correctamente. 


## Contribuciones

Si deseas contribuir a este proyecto, por favor sigue los siguientes pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu contribución: `git checkout -b feature/nueva-funcionalidad`
3. Realiza tus cambios y realiza commits: `git commit -m "Agrega nueva funcionalidad"`
4. Sube tus cambios a tu repositorio: `git push origin feature/nueva-funcionalidad`
5. Abre un pull request en este repositorio.

