import random
import matplotlib.pyplot as plt
import pandas as pd


# ==========================================
# 1. SIMULADOR DE DATOS SUCIOS (FINZ+)
# ==========================================
def simular_cuentas_sucias(cantidad):
    usuarios_id = ["usr101", "usr102", "usr103", "usr104", "usr105"]
    nombres = [
        "Ahorros",
        "Nómina",
        "Corriente",
        "Inversión",
        "Fondo Emergencia",
    ]
    bancos = ["BANCO-001", "BANCO-045", "BANCO-300", "BANCO-420"]

    data = []

    for i in range(cantidad):
        cuenta = {
            "id": i + 1,
            "usuario_id": random.choice(usuarios_id),
            "nombre": random.choice(nombres),
            "saldo_actual": round(random.uniform(1000, 5000000), 2),
            "es_sincronizada": random.choice([True, False]),
            "id_banco_externo": random.choice(bancos),
        }

        # Inyección de errores controlados para la prueba
        r = random.random()
        if r < 0.1:
            cuenta["id"] = None
        elif r < 0.2:
            cuenta["nombre"] = "ERROR"
        elif r < 0.3:
            cuenta["saldo_actual"] = -1000
        elif r < 0.4:
            cuenta["usuario_id"] = " " + cuenta["usuario_id"].upper()
        elif r < 0.5:
            cuenta["id_banco_externo"] = None

        data.append(cuenta)

    return data


# ==========================================
# 2. RUTINA DE TRANSFORMACIÓN Y AGRUPACIÓN
# ==========================================
def transformar_datos(data_frame_limpio):

    # transformacion 1 (Cuentas no sincronizadas por Banco - Para Gráfico de Barras)
    filtro1 = data_frame_limpio.query(
        "es_sincronizada == False and id_banco_externo.notnull()"
    )
    agrupacion1 = (
        filtro1.groupby("id_banco_externo")["id"]
        .count()
        .reset_index(name="conteo")
    )

    # transformacion 2 (Distribución de tipos de cuenta con saldos altos - Para Torta)
    filtro2 = data_frame_limpio.query(
        "saldo_actual >= 2000000 and nombre != 'ERROR'"
    )
    agrupacion2 = (
        filtro2.groupby("nombre")["id"].count().reset_index(name="conteo")
    )

    # transformacion 3 (Alertas de saldos erróneos o negativos por Usuario)
    filtro3 = data_frame_limpio.query("saldo_actual < 0")
    agrupacion3 = (
        filtro3.groupby("usuario_id")["id"].count().reset_index(name="conteo")
    )

    # transformacion 4 (Análisis de cuentas válidas por Usuario - Para Líneas)
    filtro4 = data_frame_limpio.query("id.notnull() and nombre != 'ERROR'")
    agrupacion4 = (
        filtro4.groupby("usuario_id")["id"].count().reset_index(name="conteo")
    )

    # transformacion 5 (Relación Cuenta vs Banco para matriz / mapa de calor)
    filtro5 = data_frame_limpio.query(
        "saldo_actual > 500000 and id_banco_externo.notnull() and nombre != 'ERROR'"
    )
    agrupacion5 = (
        filtro5.groupby(["nombre", "id_banco_externo"])["id"]
        .count()
        .reset_index(name="conteo")
    )

    agrupacion_resumen = {
        "agrupacion1": agrupacion1,
        "agrupacion2": agrupacion2,
        "agrupacion3": agrupacion3,
        "agrupacion4": agrupacion4,
        "agrupacion5": agrupacion5,
    }

    return agrupacion_resumen


# ==========================================
# 3. FUNCIONES DEFINIDAS PARA GRAFICACIÓN
# ==========================================
def graficar_barras_bancos(df_agrupacion1):
    """Genera un gráfico de barras para comparar cuentas no sincronizadas por banco."""
    plt.figure(figsize=(8, 5))
    plt.bar(
        df_agrupacion1["id_banco_externo"],
        df_agrupacion1["conteo"],
        color="royalblue",
        edgecolor="black",
    )

    plt.title(
        "Cantidad de Cuentas No Sincronizadas por Banco",
        fontsize=12,
        fontweight="bold",
    )
    plt.xlabel("Código del Banco Externo", fontsize=10)
    plt.ylabel("Número de Cuentas", fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()


def graficar_torta_categorias(df_agrupacion2):
    """Genera un gráfico de torta para mostrar la proporción de cuentas con saldos altos."""
    plt.figure(figsize=(7, 7))
    colores = ["#ff9999", "#6bbf75", "#66b3ff", "#99ff99", "#ffcc99"]

    plt.pie(
        df_agrupacion2["conteo"],
        labels=df_agrupacion2["nombre"],
        autopct="%1.1f%%",
        startangle=140,
        colors=colores,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )

    plt.title(
        "Distribución Porcentual de Cuentas con Saldos > 2M",
        fontsize=12,
        fontweight="bold",
    )
    plt.tight_layout()
    plt.show()


def graficar_lineas_usuarios(df_agrupacion4):
    """Genera un gráfico de líneas para mapear la tendencia de cuentas válidas por usuario."""
    plt.figure(figsize=(8, 4))
    plt.plot(
        df_agrupacion4["usuario_id"],
        df_agrupacion4["conteo"],
        marker="o",
        linestyle="-",
        color="darkorange",
        linewidth=2.5,
        markersize=8,
    )

    plt.title(
        "Tendencia y Volumen de Cuentas Válidas por Usuario",
        fontsize=12,
        fontweight="bold",
    )
    plt.xlabel("ID del Usuario", fontsize=10)
    plt.ylabel("Total de Cuentas Registradas", fontsize=10)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.show()


# ==========================================
# 4. FLUJO PRINCIPAL DE EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    # Paso A: Generar los diccionarios aleatorios usando tu simulador (500 registros)
    datos_sucios = simular_cuentas_sucias(500)
    df_inicial = pd.DataFrame(datos_sucios)

    # Paso B: Limpieza técnica previa (Remover espacios invisibles del simulador)
    df_inicial["usuario_id"] = df_inicial["usuario_id"].astype(str).str.strip()

    # Paso C: Procesar los datos con la rutina estructurada
    resumen_tablas = transformar_datos(df_inicial)

    # Paso D: Invocar de manera independiente cada función de graficación
    print("Desplegando Gráfico de Barras...")
    graficar_barras_bancos(resumen_tablas["agrupacion1"])

    print("Desplegando Gráfico de Torta...")
    graficar_torta_categorias(resumen_tablas["agrupacion2"])

    print("Desplegando Gráfico de Líneas...")
    graficar_lineas_usuarios(resumen_tablas["agrupacion4"])

    print("¡Proceso completado con éxito, colega!")
