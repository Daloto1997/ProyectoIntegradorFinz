import pandas as pd

def describir_categorias(data_frame_limpio):
    print(f"Numero de filas {data_frame_limpio.shape[0]}")
    print(f"Numero de columna {data_frame_limpio.shape[1]}")
    print(f"Columnas disponibles {list(data_frame_limpio.columns)}")
    print(f"Estadisticas {data_frame_limpio[['id','monto']].describe()}")
    print(f"Valores categoricos {data_frame_limpio['tipo'].value_counts()}")
    print(f"Fecha minima {data_frame_limpio['fecha'].min()}")
    print(f"Fecha maxima {data_frame_limpio['fecha'].max()}")
