import requests

def consumir_transacciones(usuario_email=None):
    url = "http://localhost:8080/api/transacciones"
    if usuario_email:
        url += f"?usuarioEmail={usuario_email}"
    respuesta = requests.get(url)
    respuesta.raise_for_status()
    datos = respuesta.json()

    normalizados = []
    for t in datos:
        cuenta = t.get("cuenta") or {}
        categoria = t.get("categoria") or {}
        tipo_raw = str(t.get("tipo", "")).upper()
        normalizados.append({
            "id":          t.get("id"),
            "usuario_id":  cuenta.get("id", 1),
            "cuenta_id":   cuenta.get("id"),
            "categoria_id": categoria.get("nombre", "Sin categoría") if categoria else "Sin categoría",
            "monto":       abs(float(t.get("monto", 0))),
            "tipo":        "ingreso" if tipo_raw == "INGRESO" else "egreso",
            "fecha":       t.get("fecha"),
            "descripcion": t.get("descripcion", ""),
        })
    return normalizados
