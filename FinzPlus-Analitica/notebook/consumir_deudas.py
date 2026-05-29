import requests

def consumir_deudas():
    # URL del endpoint en Spring Boot para obtener el listado de deudas
    url = "http://localhost:8080/api/deudas"
    
    # Se realiza la petición GET al servidor
    respuesta = requests.get(url)
    
    # Si el servidor responde con un error (404, 500, etc.), detiene la ejecución
    respuesta.raise_for_status()
    
    # Se transforman los datos recibidos a formato JSON (diccionarios/listas de Python)
    datos = respuesta.json()
    return datos
