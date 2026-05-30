import pandas as pd
def limpiar_datos_deudas(data_frame_sucio):
    data_frame_limpio = data_frame_sucio.copy()

    # --- Procesando los textos del DF SUCIO ---
    # 1. Limpiando textos (eliminar espacios y pasar a minúsculas)
    data_frame_limpio["persona_entidad"] = data_frame_limpio["persona_entidad"].astype("string").str.strip().str.lower()
    data_frame_limpio["tipo"] = data_frame_limpio["tipo"].astype("string").str.strip().str.lower()

    # 2. Controlar valores inesperados (Tipos de deuda definidos en Finz+)
    # Se aceptan tipos del sistema Finz+ y tipos de simulación
    valores_esperados_tipos = ["bancaria", "personal", "comercial", "por_pagar", "por_cobrar"]
    data_frame_limpio["tipo"] = data_frame_limpio["tipo"].where(
        data_frame_limpio["tipo"].isin(valores_esperados_tipos),
        pd.NA
    )

    # --- Limpieza de datos numéricos ---
    # 1. Verificar que los números sí sean números
    data_frame_limpio["id"] = pd.to_numeric(data_frame_limpio["id"], errors='coerce')
    data_frame_limpio["monto_total"] = pd.to_numeric(data_frame_limpio["monto_total"], errors='coerce')
    data_frame_limpio["monto_pagado"] = pd.to_numeric(data_frame_limpio["monto_pagado"], errors='coerce')

    # usuario_id solo existe en datos simulados, no en la API real
    if "usuario_id" in data_frame_limpio.columns:
        data_frame_limpio["usuario_id"] = pd.to_numeric(data_frame_limpio["usuario_id"], errors='coerce')
        data_frame_limpio = data_frame_limpio[data_frame_limpio["usuario_id"] > 0]

    # 2. Verificamos los valores numéricos esperados
    data_frame_limpio = data_frame_limpio[data_frame_limpio["id"] > 0]
    data_frame_limpio = data_frame_limpio[data_frame_limpio["monto_total"] > 0]

    # --- Limpieza de FECHAS ---
    # 1. Verificar que el campo sí es una fecha
    data_frame_limpio["fecha_vencimiento"] = pd.to_datetime(data_frame_limpio["fecha_vencimiento"], errors='coerce')

    # 2. Reemplazar fechas que no llegan por una fecha por defecto
    fecha_default = pd.to_datetime("2026-01-01") 
    data_frame_limpio["fecha_vencimiento"] = data_frame_limpio["fecha_vencimiento"].fillna(fecha_default)

    # --- NOVEDADES de datos vacíos ---
    columnas_obligatorias = ["id", "persona_entidad", "monto_total", "tipo"]
    if "usuario_id" in data_frame_limpio.columns:
        columnas_obligatorias.append("usuario_id")
    data_frame_limpio = data_frame_limpio.dropna(subset=columnas_obligatorias)

    return data_frame_limpio
