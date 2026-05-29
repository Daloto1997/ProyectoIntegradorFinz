import pandas as pd

def describir_datos(df_limpio_usuarios):
    print("--- RESUMEN DE LA TABLA DE USUARIOS ---")
    print(f"Número de filas: {df_limpio_usuarios.shape[0]}")
    print(f"Número de columnas: {df_limpio_usuarios.shape[1]}")
    print(f"Columnas disponibles: {list(df_limpio_usuarios.columns)}")
    
    print("\n--- ESTADÍSTICAS NUMÉRICAS ---")
    print(df_limpio_usuarios[['id', 'id_usuario']].describe())
    
    print("\n--- DISTRIBUCIÓN POR GÉNERO ---")
    print(df_limpio_usuarios['genero'].value_counts())
    
    print("\n--- DISTRIBUCIÓN POR ROL ---")
    print(df_limpio_usuarios['rol'].value_counts())
    
    print("\n--- RANGO DE FECHAS ---")
    print(f"Fecha mínima: {df_limpio_usuarios['fecha_creacion'].min()}")
    print(f"Fecha máxima: {df_limpio_usuarios['fecha_creacion'].max()}")