import pandas as pd

def limpiar_datos_metas(data_frame_sucio):
    data_frame_limpio = data_frame_sucio.copy()

    # --- Procesando los textos del DF SUCIO ---
    # 1. Limpiando textos (eliminar espacios y pasar a minúsculas)
    data_frame_limpio["nombre"] = data_frame_limpio["nombre"].astype("string").str.strip().str.lower()

    # 2. Controlar valores inesperados (opcional, dependiendo de si quieres limitar los nombres de las metas)
    valores_esperados_metas = ["fondo de emergencia", "viaje a europa", "cuota inicial carro", "ahorro navidad", "pc gamer"]
    data_frame_limpio["nombre"] = data_frame_limpio["nombre"].where(
        data_frame_limpio["nombre"].isin(valores_esperados_metas),
        pd.NA
    )

    # --- Limpieza de datos numéricos ---
    # 1. Verificar que los números sí sean números
    data_frame_limpio["id"] = pd.to_numeric(data_frame_limpio["id"], errors='coerce')
    data_frame_limpio["monto_objetivo"] = pd.to_numeric(data_frame_limpio["monto_objetivo"], errors='coerce')
    data_frame_limpio["monto_actual"] = pd.to_numeric(data_frame_limpio["monto_actual"], errors='coerce')

    # usuario_id solo existe en datos simulados, no en la API real
    if "usuario_id" in data_frame_limpio.columns:
        data_frame_limpio["usuario_id"] = pd.to_numeric(data_frame_limpio["usuario_id"], errors='coerce')
        data_frame_limpio = data_frame_limpio[data_frame_limpio["usuario_id"] > 0]

    # 2. Verificamos los valores numéricos esperados
    data_frame_limpio = data_frame_limpio[data_frame_limpio["id"] > 0]
    data_frame_limpio = data_frame_limpio[data_frame_limpio["monto_objetivo"] > 0]
    
    # --- Limpieza de FECHAS ---
    # 1. Verificar que el campo sí es una fecha
    data_frame_limpio["fecha_limite"] = pd.to_datetime(data_frame_limpio["fecha_limite"], errors='coerce')

    # 2. Reemplazar fechas que no llegan por una fecha por defecto
    fecha_default = pd.to_datetime("2026-12-31") # Una fecha límite por defecto a fin de año
    data_frame_limpio["fecha_limite"] = data_frame_limpio["fecha_limite"].fillna(fecha_default)

    # --- NOVEDADES de datos vacíos ---
    columnas_obligatorias = ["id", "nombre", "monto_objetivo"]
    if "usuario_id" in data_frame_limpio.columns:
        columnas_obligatorias.append("usuario_id")
    data_frame_limpio = data_frame_limpio.dropna(subset=columnas_obligatorias)

    return data_frame_limpio
