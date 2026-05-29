import requests

def categorias():
    url = "http://localhost:8080/api/categorias"
    respuesta = requests.get(url)
    respuesta.raise_for_status()
    datos = respuesta.json()
    return datos