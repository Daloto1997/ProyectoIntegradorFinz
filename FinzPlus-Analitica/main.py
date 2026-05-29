"""
FinzPlus - Sistema de gestión financiera
Módulo principal: consume datos reales del backend Spring Boot,
con fallback a simulación si el servidor no está activo.
"""

import os
import re
import pandas as pd

# --- Simulación (fallback si el backend no responde) ---
from utils.simulacion import simular_Categorias
from utils.simularcuentas import generar_metas, generar_deudas

# --- Consumo de API real ---
from notebook.consumir_metas import consumir_metas
from notebook.consumir_deudas import consumir_deudas

# --- Limpieza ---
from notebook.limpieza import limpiar_datos
from notebook.limpiezaDeudas import limpiar_datos_deudas
from notebook.limpiezaMetas import limpiar_datos_metas

# --- Transformación ---
from notebook.transformarDeudas import transformar_datos as transformar_deudas
from notebook.transformarMetas import transformar_datos as transformar_metas

# --- Graficación ---
from notebook.graficarDeudas import generar_reporte_grafico_deudas
from notebook.graficarMetas import generar_reporte_grafico_metas


def camel_a_snake(nombre):
    # Convierte 'montoTotal' -> 'monto_total' para que la limpieza encuentre las columnas
    return re.sub(r'(?<!^)(?=[A-Z])', '_', nombre).lower()


def normalizar_columnas(df):
    df.columns = [camel_a_snake(col) for col in df.columns]
    return df


def obtener_metas():
    """Intenta consumir la API real. Si falla, usa datos simulados."""
    try:
        datos = consumir_metas()
        print("   OK Metas obtenidas desde la API de Spring Boot")
        df = pd.DataFrame(datos)
        return normalizar_columnas(df)
    except Exception as error:
        print(f"   AVISO API no disponible ({error}). Usando simulacion de metas.")
        return pd.DataFrame(generar_metas(100))


def obtener_deudas():
    """Intenta consumir la API real. Si falla, usa datos simulados."""
    try:
        datos = consumir_deudas()
        print("   OK Deudas obtenidas desde la API de Spring Boot")
        df = pd.DataFrame(datos)
        return normalizar_columnas(df)
    except Exception as error:
        print(f"   AVISO API no disponible ({error}). Usando simulacion de deudas.")
        return pd.DataFrame(generar_deudas(100))


def main():
    print("=" * 80)
    print("INICIANDO ANALITICA FinzPlus - Datos reales desde API")
    print("=" * 80)

    # ============================================================================
    # 1. OBTENER DATOS (API real o simulacion de fallback)
    # ============================================================================
    print("\n[1] Obteniendo datos...")

    simulaciones_categorias = simular_Categorias(100000)
    print(f"   OK {len(simulaciones_categorias)} categorias/transacciones (simulacion)")

    df_metas = obtener_metas()
    print(f"   OK {len(df_metas)} metas")

    df_deudas = obtener_deudas()
    print(f"   OK {len(df_deudas)} deudas")

    # ============================================================================
    # 2. CONVERTIR A DATAFRAMES
    # ============================================================================
    print("\n[2] Preparando DataFrames...")
    categorias_ordenadas = pd.DataFrame(simulaciones_categorias)

    # ============================================================================
    # 3. LIMPIEZA DE DATOS
    # ============================================================================
    print("\n[3] Limpiando datos...")
    categorias_limpias = limpiar_datos(categorias_ordenadas)
    metas_limpias = limpiar_datos_metas(df_metas)
    deudas_limpias = limpiar_datos_deudas(df_deudas)
    print(f"   OK Categorias: {len(categorias_limpias)} filas limpias")
    print(f"   OK Metas: {len(metas_limpias)} filas limpias")
    print(f"   OK Deudas: {len(deudas_limpias)} filas limpias")

    # ============================================================================
    # 4. TRANSFORMAR (Preparar agrupaciones para graficas)
    # ============================================================================
    print("\n[4] Transformando datos para graficas...")
    agrupaciones_metas = transformar_metas(metas_limpias)
    agrupaciones_deudas = transformar_deudas(deudas_limpias)

    # ============================================================================
    # 5. GRAFICAR
    # ============================================================================
    print("\n[5] Generando graficas...")
    if not metas_limpias.empty:
        generar_reporte_grafico_metas(agrupaciones_metas)
    else:
        print("   AVISO Sin datos limpios de metas para graficar.")

    if not deudas_limpias.empty:
        generar_reporte_grafico_deudas(agrupaciones_deudas)
    else:
        print("   AVISO Sin datos limpios de deudas para graficar.")

    # ============================================================================
    # 6. GUARDAR RESULTADOS EN CSV
    # ============================================================================
    print("\n[6] Guardando resultados...")
    os.makedirs("outputs", exist_ok=True)
    categorias_limpias.to_csv("outputs/categorias_limpias.csv", index=False)
    metas_limpias.to_csv("outputs/metas_limpias.csv", index=False)
    deudas_limpias.to_csv("outputs/deudas_limpias.csv", index=False)
    print("   OK outputs/categorias_limpias.csv")
    print("   OK outputs/metas_limpias.csv")
    print("   OK outputs/deudas_limpias.csv")

    print("\n" + "=" * 80)
    print("PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 80)

    return {
        "categorias": categorias_limpias,
        "metas": metas_limpias,
        "deudas": deudas_limpias
    }


if __name__ == "__main__":
    main()
