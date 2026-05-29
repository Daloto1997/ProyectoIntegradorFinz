import pandas as pd

def describir_deudas(data_frame_limpio):
    print("=== DESCRIPCIÓN DE LA TABLA DEUDAS ===")
    print(f"Número de filas: {data_frame_limpio.shape[0]}")
    print(f"Número de columnas: {data_frame_limpio.shape[1]}")
    print(f"Columnas disponibles: {list(data_frame_limpio.columns)}\n")
    
    print("Estadísticas de valores numéricos:")
    # Calculamos estadísticas para los montos de la deuda
    print(data_frame_limpio[['id', 'usuario_id', 'monto_total', 'monto_pagado']].describe())
    print("\n")
    
    print("Valores categóricos (Tipos de deuda):")
    # En deudas, tenemos la columna 'tipo' (bancaria, personal, etc.)
    print(data_frame_limpio['tipo'].value_counts())
    print("\n")
    
    print("Valores categóricos (Entidades más frecuentes):")
    # También es útil saber a quién se le debe más frecuentemente
    print(data_frame_limpio['persona_entidad'].value_counts())
    print("\n")
    
    print(f"Fecha de vencimiento más próxima: {data_frame_limpio['fecha_vencimiento'].min()}")
    print(f"Fecha de vencimiento más lejana: {data_frame_limpio['fecha_vencimiento'].max()}")
    print("-" * 40)
