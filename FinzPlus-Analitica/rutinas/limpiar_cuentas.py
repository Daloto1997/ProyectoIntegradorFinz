import pandas as pd


def limpiar_cuentas(data_frame_sucio):
    data_frame_limpio = data_frame_sucio.copy()
    data_frame_limpio = data_frame_limpio.dropna(subset=["id"]).copy()
    data_frame_limpio["saldo_actual"] = data_frame_limpio["saldo_actual"].apply(
        lambda x: 0 if x is None or x < 0 else x
    )
    data_frame_limpio["usuario_id"] = data_frame_limpio["usuario_id"].astype(str).str.strip()
    data_frame_limpio["nombre"] = data_frame_limpio["nombre"].replace(
        ["ERROR_SISTEMA", "CUENTA_PRUEBA"], "Cuenta Sin Nombre"
    )
    data_frame_limpio["id_banco_externo"] = data_frame_limpio["id_banco_externo"].fillna("SIN_CONEXION")
    return data_frame_limpio


if __name__ == "__main__":
    from rutinas.simular_cuentas import simular_cuentas_sucias

    lista_resultados = simular_cuentas_sucias(20)
    df = pd.DataFrame(lista_resultados)
    df_limpio = limpiar_cuentas(df)

    print(df_limpio.head(10))
    df_limpio.to_csv("cuentas_listas_para_mysql.csv", index=False)
    print("\n¡Archivo final 'cuentas_listas_para_mysql.csv' generado!")
