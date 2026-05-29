import pandas as pd

def limpiar_transacciones(df_sucio):
    df_limpio_transacciones = df_sucio.copy()

    # 1. Limpiar las columnas que son palabras (String)
    columnas_texto = ["tipo", "descripcion"]
    for columna in columnas_texto:
        df_limpio_transacciones[columna] = df_limpio_transacciones[columna].astype("string").str.strip().str.lower()

    # 2. Definir valores esperados
    tipos_validos = ["ingreso", "egreso"]
    df_limpio_transacciones["tipo"] = df_limpio_transacciones["tipo"].where(df_limpio_transacciones["tipo"].isin(tipos_validos), pd.NA)

    # 3. Evaluar columnas numericas
    df_limpio_transacciones["id"] = pd.to_numeric(df_limpio_transacciones["id"])
    df_limpio_transacciones["usuario_id"] = pd.to_numeric(df_limpio_transacciones["usuario_id"])
    df_limpio_transacciones["monto"] = pd.to_numeric(df_limpio_transacciones["monto"])

    # 4. Evaluar columna de fecha
    df_limpio_transacciones["fecha"] = pd.to_datetime(df_limpio_transacciones["fecha"])

    # 5. Eliminar registros nulos de campos obligatorios (incluyendo fecha)
    # La fecha se agrego aqui porque un registro sin fecha es invalido, no se le inventa una
    columnas_obligatorias = ["id", "usuario_id", "monto", "tipo", "fecha"]
    df_limpio_transacciones = df_limpio_transacciones.dropna(subset=columnas_obligatorias)

    # 7. Eliminar valores invalidos en campos numericos (CORREGIDO)
    df_limpio_transacciones = df_limpio_transacciones[df_limpio_transacciones["usuario_id"] > 0]
    df_limpio_transacciones = df_limpio_transacciones[df_limpio_transacciones["monto"] > 0]

    # 8. Eliminar registros duplicados
    df_limpio_transacciones = df_limpio_transacciones.drop_duplicates()

    return df_limpio_transacciones