import pandas as pd

def describir_metas(data_frame_limpio):
    print("=== DESCRIPCIÓN DE LA TABLA METAS ===")
    print(f"Número de filas: {data_frame_limpio.shape[0]}")
    print(f"Número de columnas: {data_frame_limpio.shape[1]}")
    print(f"Columnas disponibles: {list(data_frame_limpio.columns)}\n")
    
    print("Estadísticas de valores numéricos:")
    # Calculamos estadísticas para los montos y los IDs
    print(data_frame_limpio[['id', 'usuario_id', 'monto_objetivo', 'monto_actual']].describe())
    print("\n")
    
    print("Valores categóricos (Nombres de metas más comunes):")
    # En metas, el valor categórico principal es el nombre de la meta
    print(data_frame_limpio['nombre'].value_counts())
    print("\n")
    
    print(f"Fecha límite más próxima: {data_frame_limpio['fecha_limite'].min()}")
    print(f"Fecha límite más lejana: {data_frame_limpio['fecha_limite'].max()}")
    print("-" * 40)
