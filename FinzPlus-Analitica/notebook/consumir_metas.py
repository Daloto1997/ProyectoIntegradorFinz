import requests

def consumir_metas():
    # URL del endpoint en Spring Boot para obtener el listado de metas
    url = "http://localhost:8080/api/metas"
    
    # Se realiza la petición GET al servidor
    respuesta = requests.get(url)
    
    # Si el servidor responde con un error, detiene la ejecución
    respuesta.raise_for_status()
    
    # Se transforman los datos recibidos a formato JSON
    datos = respuesta.json()
    return datos
