import pandas as pd

def limpiar_usuarios(data_frame_sucio):
    df_limpio_usuarios = data_frame_sucio.copy()

    # 1. Limpiar las columnas del dataframe que son palabras (String)
    columnas_texto = ["nombre_usuario", "email", "rol", "genero"]
    for columna in columnas_texto:
        df_limpio_usuarios[columna] = df_limpio_usuarios[columna].astype("string").str.strip().str.lower()

    # 2. Definir valores esperados
    roles_validos = ["admin", "cliente", "premium"]
    df_limpio_usuarios["rol"] = df_limpio_usuarios["rol"].where(df_limpio_usuarios["rol"].isin(roles_validos), pd.NA)

    generos_validos = ["masculino", "femenino", "otro"]
    df_limpio_usuarios["genero"] = df_limpio_usuarios["genero"].where(df_limpio_usuarios["genero"].isin(generos_validos), pd.NA)

    # 3. Evaluar columnas numericas
    df_limpio_usuarios["id"] = pd.to_numeric(df_limpio_usuarios["id"])
    df_limpio_usuarios["id_usuario"] = pd.to_numeric(df_limpio_usuarios["id_usuario"])

    # 4. Evaluar columna de fecha
    df_limpio_usuarios["fecha_creacion"] = pd.to_datetime(df_limpio_usuarios["fecha_creacion"])

    # 5. Reemplazar fechas nulas con una fecha por defecto
    fecha_defecto = pd.to_datetime("2024-01-01")
    df_limpio_usuarios["fecha_creacion"] = df_limpio_usuarios["fecha_creacion"].fillna(fecha_defecto)

    # 6. Eliminar registros nulos de campos obligatorios
    columnas_obligatorias = ["id", "id_usuario", "nombre_usuario", "email", "rol", "genero"]
    df_limpio_usuarios = df_limpio_usuarios.dropna(subset=columnas_obligatorias)

    # 7. Eliminar valores invalidos en campos numericos
    # Filtramos para que el ID siempre sea positivo
    df_limpio_usuarios = df_limpio_usuarios[df_limpio_usuarios["id_usuario"] >= 0]

    # 8. Eliminar registros duplicados
    df_limpio_usuarios = df_limpio_usuarios.drop_duplicates()

    return df_limpio_usuarios
