import pandas as pd


def transformar_Categorias(data_frame_limpio):
  
    # transformacion 1 (Gastos por Fecha - Ideal para: Gráfico de Líneas)

    filtro1 = data_frame_limpio.query("tipo == 'gasto'")
    agrupacion1 = (
        filtro1.groupby("fecha")["monto"].sum().reset_index(name="total_gastado")
    )


    # transformacion 2 (Transacciones de Alto Valor - Ideal para: Gráfico de Barras)
    
    filtro2 = data_frame_limpio.query("monto >= 50000")
    agrupacion2 = (
        filtro2.groupby("tipo")["usuario_id"].count().reset_index(name="conteo")
    )

    
    # transformacion 3 (Distribución de Ocio - Ideal para: Gráfico de Tortas)
   
    filtro3 = data_frame_limpio.query("tipo == 'ocio'")
    agrupacion3 = (
        filtro3.groupby("nombre")["monto"].sum().reset_index(name="total_ocio")
    )

    agrupacion_resumen = {
        "agrupacion1": agrupacion1,
        "agrupacion2": agrupacion2,
        "agrupacion3": agrupacion3,
    }

    return agrupacion_resumen