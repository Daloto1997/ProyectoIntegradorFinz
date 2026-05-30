import requests

def consumir_usuarios():
    url = "http://localhost:8080/api/usuarios"
    respuesta = requests.get(url)
    respuesta.raise_for_status()
    datos = respuesta.json()

    normalizados = []
    for u in datos:
        normalizados.append({
            "id":             u.get("id"),
            "id_usuario":     u.get("id"),
            "nombre_usuario": u.get("nombre", ""),
            "email":          u.get("email", ""),
            "rol":            str(u.get("rol", "CLIENTE")).lower(),
            "genero":         "otro",
            "fecha_creacion": u.get("fechaCreacion"),
        })
    return normalizados
