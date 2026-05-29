import pandas as pd

def transformar_datos(data_frame_limpio):

    # transformacion 1 (Fechas límite de metas activas -> Para gráfica de Líneas)
    # Filtramos las metas que ya tienen un monto objetivo definido (mayor a 0).
    filtro1 = data_frame_limpio.query("monto_objetivo > 0")
    agrupacion1 = filtro1.groupby("fecha_limite")["id"].count().reset_index(name="conteo")

    # transformacion 2 (Metas de alto valor por categoría -> Para gráfica de Barras)
    # Filtramos metas ambiciosas (ej. mayores o iguales a 5 millones) para ver cuáles son las más populares.
    filtro2 = data_frame_limpio.query("monto_objetivo >= 5000000")
    agrupacion2 = filtro2.groupby("nombre")["id"].count().reset_index(name="conteo")

    # transformacion 3 (Usuarios vs Categoría de meta -> Para Mapa de Calor)
    # Solo disponible si los datos incluyen usuario_id (datos simulados)
    if "usuario_id" in data_frame_limpio.columns:
        filtro3 = data_frame_limpio.query("monto_actual > 0")
        agrupacion3 = filtro3.groupby(["usuario_id", "nombre"])["id"].count().reset_index(name="conteo")
    else:
        agrupacion3 = pd.DataFrame(columns=["usuario_id", "nombre", "conteo"])

    # transformacion 4 (Metas estancadas / en ceros -> Para gráfica de Torta)
    # Filtramos las metas que no tienen ahorros para ver el porcentaje de procrastinación por categoría.
    filtro4 = data_frame_limpio.query("monto_actual == 0")
    agrupacion4 = filtro4.groupby("nombre")["id"].count().reset_index(name="conteo")

    # transformacion 5 (Usuarios con metas muy ambiciosas -> Para gráfica de Barras Horizontales)
    # Solo disponible si los datos incluyen usuario_id (datos simulados)
    if "usuario_id" in data_frame_limpio.columns:
        filtro5 = data_frame_limpio.query("monto_objetivo >= 10000000")
        agrupacion5 = filtro5.groupby("usuario_id")["id"].count().reset_index(name="conteo")
    else:
        agrupacion5 = pd.DataFrame(columns=["usuario_id", "conteo"])

    agrupacion_resumen = {
        "agrupacion1": agrupacion1,
        "agrupacion2": agrupacion2,
        "agrupacion3": agrupacion3,
        "agrupacion4": agrupacion4,
        "agrupacion5": agrupacion5
    }

    return agrupacion_resumen
