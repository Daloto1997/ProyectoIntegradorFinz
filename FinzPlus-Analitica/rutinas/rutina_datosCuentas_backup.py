import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def simular_Cuentas_Sucias(numeroSimulaciones):
    # --- 1. DATOS MAESTROS (Basados en tu SQL) ---
    usuarios_id = ["usr101", "usr102", "usr103", "usr104", "usr105"]
    nombres_cuenta = ["Ahorros", "Nómina", "Corriente", "Inversión", "Fondo Emergencia"]
    bancos_externos = ["BANCO-001", "BANCO-045", "BANCO-300", "BANCO-420"]
    
    simulaciones = []

    for i in range(numeroSimulaciones):
        # --- 2. CREACIÓN DE DATOS BASE ---
        simulacion = {
            "id": i + 1,
            "usuario_id": random.choice(usuarios_id),
            "nombre": random.choice(nombres_cuenta),
            "saldo_actual": round(random.uniform(1000, 5000000), 2),
            "es_sincronizada": random.choice([True, False]),
            "id_banco_externo": random.choice(bancos_externos)
        }

        # --- 3. INYECCIÓN DE ERRORES (Estilo exacto de tu compañero) ---
        probabilidadError = random.random()

        if probabilidadError < 0.1:
            simulacion["id"] = None
        elif probabilidadError < 0.2:
            simulacion["nombre"] = random.choice(["ERROR_SISTEMA", "CUENTA_PRUEBA"])
        elif probabilidadError < 0.3:
            simulacion["saldo_actual"] = random.choice([0, -5000, None])
        elif probabilidadError < 0.4:
            # Error de formato: espacio en blanco y mayúsculas
            simulacion["usuario_id"] = " " + simulacion["usuario_id"].upper()
        elif probabilidadError < 0.5:
            simulacion["id_banco_externo"] = None

        # --- 4. AGREGAR A LA LISTA ---
        simulaciones.append(simulacion)

    return simulaciones

# --- EJECUCIÓN ---
# Generamos la lista de diccionarios
cantidad = 20
lista_resultados = simular_Cuentas_Sucias(cantidad)

# Si en algún momento necesitas pasarlo a Pandas para limpiar, harías esto:
# df = pd.DataFrame(lista_resultados)

print(f"--- LISTA DE {cantidad} SIMULACIONES (CON PANDAS IMPORTADO) ---")
for s in lista_resultados:
    print(s)
    
    # --- PROCESO DE LIMPIEZA ---

# 1. Convertimos la lista sucia en un DataFrame de Pandas
df = pd.DataFrame(lista_resultados)

print("\n--- REPORTE DE CALIDAD INICIAL ---")
print(df.isnull().sum()) # Esto nos dice cuántos valores nulos (None) hay por columna

# 2. Limpieza de IDs: Eliminamos filas que no tengan ID (porque en SQL es PRIMARY KEY)
df_limpio = df.dropna(subset=['id']).copy()

# 3. Limpieza de Saldos: Convertimos nulos o negativos a 0
df_limpio['saldo_actual'] = df_limpio['saldo_actual'].apply(lambda x: 0 if x is None or x < 0 else x)

# 4. Limpieza de Strings: Quitamos espacios en blanco extra y corregimos nombres
df_limpio['usuario_id'] = df_limpio['usuario_id'].astype(str).str.strip()
df_limpio['nombre'] = df_limpio['nombre'].replace(['ERROR_SISTEMA', 'CUENTA_PRUEBA'], 'Cuenta Sin Nombre')

# 5. Llenado de vacíos: Si el banco es nulo, ponemos 'SÍN BANCO'
df_limpio['id_banco_externo'] = df_limpio['id_banco_externo'].fillna('SIN_CONEXION')

print("\n--- VISTA PREVIA DE DATOS LIMPIOS ---")
print(df_limpio.head(10))

# 6. Guardamos el resultado final
df_limpio.to_csv('cuentas_listas_para_mysql.csv', index=False)
print("\n¡Archivo final 'cuentas_listas_para_mysql.csv' generado!")

