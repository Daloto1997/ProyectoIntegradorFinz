import requests

def consumir_analitica_cuentas():
    url = "http://localhost:8080/api/cuentas"
    respuesta = requests.get(url)
    respuesta.raise_for_status()
    datos = respuesta.json()
    return datos
