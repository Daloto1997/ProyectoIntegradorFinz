import pandas as pd

def transformar_datos(data_frame_limpio):

    # transformacion 1 (Deudas activas por fecha de vencimiento -> Para gráfica de Líneas)
    # Filtramos las deudas donde aún falta dinero por pagar.
    filtro1 = data_frame_limpio.query("monto_total > monto_pagado")
    agrupacion1 = filtro1.groupby("fecha_vencimiento")["id"].count().reset_index(name="conteo")

    # transformacion 2 (Deudas de alto valor según el tipo -> Para gráfica de Barras)
    # Filtramos deudas considerables (ej. mayores o iguales a 1 millón).
    filtro2 = data_frame_limpio.query("monto_total >= 1000000")
    agrupacion2 = filtro2.groupby("tipo")["id"].count().reset_index(name="conteo")

    # transformacion 3 (Tipo vs Entidad en deudas intactas -> Para Mapa de Calor)
    # Filtramos deudas en las que no se ha pagado absolutamente nada.
    filtro3 = data_frame_limpio.query("monto_pagado == 0")
    agrupacion3 = filtro3.groupby(["tipo", "persona_entidad"])["id"].count().reset_index(name="conteo")

    # transformacion 4 (Distribución de entidades en deudas bancarias -> Para gráfica de Torta)
    # Filtramos estrictamente las deudas de tipo bancario para ver cómo se reparten.
    filtro4 = data_frame_limpio.query("tipo == 'bancaria'")
    agrupacion4 = filtro4.groupby("persona_entidad")["id"].count().reset_index(name="conteo")

    # transformacion 5 (Volumen de deudas significativas por usuario -> Para gráfica de Barras Horizontales)
    # Solo disponible si los datos incluyen usuario_id (datos simulados)
    if "usuario_id" in data_frame_limpio.columns:
        filtro5 = data_frame_limpio.query("monto_total > 500000")
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
