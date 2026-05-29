import pandas as pd

def transformar_transacciones(data_frame_limpio):
    # Diccionario traductor para cambiar IDs numéricos por nombres reales
    diccionario_categorias = {
        "101": "Alimentación",
        "102": "Transporte",
        "103": "Vivienda",
        "104": "Servicios",
        "105": "Entretenimiento"
    }

    # transformacion 1 (proporcion de ingresos vs egresos para grafica de torta)
    filtro1 = data_frame_limpio.query("tipo in ['ingreso', 'egreso']")
    agrupacion1 = filtro1.groupby("tipo")["id"].count().reset_index(name="conteo")

    # transformacion 2 (volumen mensual de operaciones para grafica de lineas)
    filtro2 = data_frame_limpio.query("tipo in ['ingreso', 'egreso']").copy()
    # Creamos una columna nueva que guarda solo el año y el mes (ejemplo: "2024-03")
    filtro2["mes"] = filtro2["fecha"].dt.to_period("M").astype(str)
    # Agrupamos por esa columna de mes en lugar de por el dia exacto
    agrupacion2 = filtro2.groupby("mes")["id"].count().reset_index(name="conteo")
    # Renombramos la columna para que la grafica la siga reconociendo con el mismo nombre
    agrupacion2 = agrupacion2.rename(columns={"mes": "fecha"})

    # transformacion 3 (egresos por categoria para grafica de barras verticales)
    filtro3 = data_frame_limpio.query("tipo=='egreso'")
    agrupacion3 = filtro3.groupby("categoria_id")["id"].count().reset_index(name="conteo")
    # MODIFICACIÓN AQUÍ: Convertimos a texto y traducimos el ID por el nombre
    agrupacion3["categoria_id"] = agrupacion3["categoria_id"].astype(str).replace(diccionario_categorias)

    # transformacion 4 (cuenta vs categoria en egresos para mapa de calor)
    filtro4 = data_frame_limpio.query("tipo=='egreso'")
    agrupacion4 = filtro4.groupby(["cuenta_id", "categoria_id"])["id"].count().reset_index(name="conteo")
    # MODIFICACIÓN AQUÍ: Traducimos también para el mapa de calor
    agrupacion4["categoria_id"] = agrupacion4["categoria_id"].astype(str).replace(diccionario_categorias)

    # transformacion 5 (transacciones atipicas de alto valor por descripcion)
    filtro5 = data_frame_limpio.query("monto>=1500000")
    agrupacion5 = filtro5.groupby("descripcion")["id"].count().reset_index(name="conteo")

    agrupacion_transacciones = {
        "agrupacion1": agrupacion1,
        "agrupacion2": agrupacion2,
        "agrupacion3": agrupacion3,
        "agrupacion4": agrupacion4,
        "agrupacion5": agrupacion5
    }

    return agrupacion_transacciones