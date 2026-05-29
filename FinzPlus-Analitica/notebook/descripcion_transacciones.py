import pandas as pd

def describir_transacciones(df_limpio_transacciones):
        print("--- RESUMEN DE LA TABLA DE TRANSACCIONES ---")
        # CORREGIDO: Ajuste del nombre de la variable en todos los print
        print(f"Total de registros limpios: {df_limpio_transacciones.shape[0]}")

        print("\n--- ANÁLISIS FINANCIERO (MONTO) ---")
        print(df_limpio_transacciones['monto'].describe())

        print("\n--- DISTRIBUCIÓN POR TIPO DE MOVIMIENTO ---")
        print(df_limpio_transacciones['tipo'].value_counts())

        print("\n--- FRECUENCIA POR CATEGORÍA ---")
        print(df_limpio_transacciones['categoria_id'].value_counts())

        print("\n--- PERIODO DE TIEMPO ANALIZADO ---")
        print(f"Primera transacción: {df_limpio_transacciones['fecha'].min()}")
        print(f"Última transacción: {df_limpio_transacciones['fecha'].max()}")

        print("\n--- TOTAL DE DINERO MOVILIZADO ---")
        total = df_limpio_transacciones['monto'].sum()
        print(f"Suma total de montos: ${total:,.2f}")