import requests

def consumir_deudas(usuario_email=None):
    url = "http://localhost:8080/api/deudas"
    if usuario_email:
        url += f"?usuarioEmail={usuario_email}"
    respuesta = requests.get(url)
    respuesta.raise_for_status()
    return respuesta.json()
