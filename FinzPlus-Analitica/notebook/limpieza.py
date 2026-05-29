import pandas as pd  

def limpiar_datos(data_frame_sucio):
    
    data_frame_limpio=data_frame_sucio.copy()

    #1. Limpiar las columnas String del DF
    columnas_texto=["id","nombre","tipo","usuario_id","color"]
    for columna in columnas_texto:
        data_frame_limpio[columna]=data_frame_limpio[columna].astype("string").str.strip().str.lower()
    
    #1.1 Definir valores de String esperados
    valores_validos_tipos=["gasto", "ahorro", "inversión", "ocio", "servicios publicos"]
    data_frame_limpio["tipo"]=data_frame_limpio["tipo"].where(
        data_frame_limpio["tipo"].isin(valores_validos_tipos),
        pd.NA
    )

    #2. Limpiar las columnas numericas del DF
    data_frame_limpio["id"]=pd.to_numeric(data_frame_limpio["id"], errors="coerce")
    data_frame_limpio["monto"]=pd.to_numeric(data_frame_limpio["monto"], errors="coerce")

    #2.1 Limpiando campos numericos que no tengan valores validos
    data_frame_limpio=data_frame_limpio[data_frame_limpio["monto"]>50000]
    data_frame_limpio=data_frame_limpio[data_frame_limpio["id"]>0]

    #3. Organizar las columnas de tipo fecha
    data_frame_limpio["fecha"]=pd.to_datetime(data_frame_limpio["fecha"])

    #3.1 Si una fecha no viene la reemplazamos por un valor por defecto
    fecha_default=pd.to_datetime("2026-01-01")
    data_frame_limpio["fecha"]=data_frame_limpio["fecha"].fillna(fecha_default)

    #4. Eliminar registros que tengan datos obligatorios vacios
    columnas_obligatorias=["id","nombre","monto","usuario_id","tipo"]
    data_frame_limpio=data_frame_limpio.dropna(subset=columnas_obligatorias)

    #5. ELiminar registros duplicados
    data_frame_limpio=data_frame_limpio.drop_duplicates()

    data_frame_limpio["id"] = data_frame_limpio["id"].astype(int)

    return data_frame_limpio
