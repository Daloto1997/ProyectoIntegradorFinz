import pandas as pd

def transformar_usuarios(data_frame_limpio, data_frame_original):

    # transformacion 1 (distribucion de roles principales)
    filtro1=data_frame_limpio.query("rol in ['admin', 'cliente', 'premium']")
    agrupacion1=filtro1.groupby("rol")["id"].count().reset_index(name="conteo")

    # transformacion 2 (crecimiento mensual de clientes)
    filtro2 = data_frame_limpio.query("rol in ['cliente', 'premium']").copy()
    # Creamos una columna nueva que guarda solo el año y el mes (ejemplo: "2024-03")
    filtro2["mes"] = filtro2["fecha_creacion"].dt.to_period("M").astype(str)
    # Agrupamos por esa columna de mes en lugar de por el dia exacto
    agrupacion2 = filtro2.groupby("mes")["id"].count().reset_index(name="conteo")
    # Renombramos la columna para que la grafica la siga reconociendo con el mismo nombre
    agrupacion2 = agrupacion2.rename(columns={"mes": "fecha_creacion"})

    # transformacion 3 (comparativo de genero en clientes y premium)
    filtro3=data_frame_limpio.query("rol in ['cliente', 'premium']")
    agrupacion3=filtro3.groupby(["rol", "genero"])["id"].count().reset_index(name="conteo")

    # transformacion 4 (mismos datos que agrupacion3, se usa para la grafica de barras agrupadas)
    agrupacion4 = agrupacion3.copy()

    # transformacion 5 (deteccion de roles anomalos)
    # Se hace sobre los datos ORIGINALES porque la limpieza ya elimino los roles invalidos
    roles_validos = ["admin", "cliente", "premium"]
    df_aux = data_frame_original.copy()
    df_aux["rol"] = df_aux["rol"].astype("string").str.strip().str.lower()
    filtro5 = df_aux[~df_aux["rol"].isin(roles_validos)]
    filtro5 = filtro5.dropna(subset=["rol"])
    agrupacion5 = filtro5.groupby("rol")["id"].count().reset_index(name="conteo")

    agrupacion_usuarios={
        "agrupacion1":agrupacion1,
        "agrupacion2":agrupacion2,
        "agrupacion3":agrupacion3,
        "agrupacion4":agrupacion4,
        "agrupacion5":agrupacion5
    }

    return agrupacion_usuarios