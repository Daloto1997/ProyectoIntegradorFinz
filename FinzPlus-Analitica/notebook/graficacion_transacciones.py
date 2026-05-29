# Se importa matplotlib para crear los gráficos
import matplotlib.pyplot as plt
# Se importa seaborn para el mapa de calor con estilo mejorado
import seaborn as sns
# Se importa os para manejar rutas y crear carpetas
import os

# =====================================================================
# IDENTIDAD VISUAL CORPORATIVA FINZ+ (FIJA E INYECTADA)
# =====================================================================
VERDE_FINZ_PRINCIPAL = "#25c974"  # Color base de la plataforma
VERDE_FINZ_OSCURO = "#065f46"      # Para degradados sofisticados y títulos
AZUL_PIZARRA_TEXTO = "#1e293b"     # Títulos y etiquetas principales
GRIS_TEXTO_SECUNDARIO = "#64748b"  # Ejes y etiquetas sutiles
ROJO_FINZ_ALERTA = "#ef4444"      # SOLO para Egresos en la torta y Mapa de Calor

# Configuración de estilo global para un look premium y limpio
plt.rcParams['figure.facecolor'] = '#f8fafc'  # Fondo de la interfaz
plt.rcParams['axes.facecolor'] = '#ffffff'    # Fondo de los gráficos
plt.rcParams['font.family'] = 'sans-serif'    # Fuente moderna

# Ruta para la carpeta local de gráficos
RUTA_ASSETS = os.path.join(os.path.dirname(__file__), "graficos")


def crear_ruta_si_no_existe(ruta_destino):
    os.makedirs(ruta_destino, exist_ok=True)


def graficar_lineas(datos_agrupados, columna_eje_x, columna_eje_y,
                    titulo="Gráfico de líneas", nombre_archivo="lineas.png", 
                    ruta_destino=RUTA_ASSETS):
    # Gráfico de líneas sofisticado en Verde Finz+
    crear_ruta_si_no_existe(ruta_destino)
    figura, area_dibujo = plt.subplots(figsize=(10, 5))

    area_dibujo.plot(
        datos_agrupados[columna_eje_x],
        datos_agrupados[columna_eje_y],
        marker="o",
        markersize=6,
        color=VERDE_FINZ_PRINCIPAL,
        linewidth=2.5,
        label="Tendencia"
    )

    # Etiquetas encima de cada punto de la linea
    for pos, y_val in enumerate(datos_agrupados[columna_eje_y]):
        area_dibujo.annotate(
            str(y_val),
            xy=(pos, y_val),
            xytext=(0, 8),
            textcoords="offset points",
            ha='center',
            fontsize=9,
            color=GRIS_TEXTO_SECUNDARIO
        )

    # Estilización Premium
    area_dibujo.set_title(titulo, fontsize=14, color=AZUL_PIZARRA_TEXTO, fontweight="bold", pad=15)
    area_dibujo.set_xlabel(columna_eje_x, fontsize=11, color=GRIS_TEXTO_SECUNDARIO, labelpad=10)
    area_dibujo.set_ylabel(columna_eje_y, fontsize=11, color=GRIS_TEXTO_SECUNDARIO, labelpad=10)
    area_dibujo.grid(True, linestyle=":", alpha=0.6, color="#cbd5e1")

    # Limpieza de bordes
    for spine in ["top", "right"]:
        area_dibujo.spines[spine].set_visible(False)
    area_dibujo.spines["left"].set_color("#e2e8f0")
    area_dibujo.spines["bottom"].set_color("#e2e8f0")

    plt.xticks(rotation=45, color=GRIS_TEXTO_SECUNDARIO)
    plt.yticks(color=GRIS_TEXTO_SECUNDARIO)
    plt.tight_layout()

    ruta_completa = os.path.join(ruta_destino, nombre_archivo)
    figura.savefig(ruta_completa, dpi=150, facecolor=figura.get_facecolor())
    plt.close(figura)
    print(f"Gráfico de líneas guardado en: {ruta_completa}")


def graficar_barras(datos_agrupados, columna_categorias, columna_valores,
                    titulo="Gráfico de barras", color_fijo=VERDE_FINZ_PRINCIPAL,
                    nombre_archivo="barras.png", ruta_destino=RUTA_ASSETS):
    # Gráfico de barras premium en Verde Finz+ o degradado controlado
    crear_ruta_si_no_existe(ruta_destino)
    figura, area_dibujo = plt.subplots(figsize=(10, 5))
    categorias = datos_agrupados[columna_categorias].astype(str)
    
    area_dibujo.bar(
        categorias,
        datos_agrupados[columna_valores],
        color=color_fijo,
        edgecolor="none",
        alpha=0.9,
        width=0.6
    )

    # Etiquetas encima de cada barra
    area_dibujo.bar_label(area_dibujo.containers[0], fontsize=9, color=AZUL_PIZARRA_TEXTO, padding=4)

    # Estilización Premium
    area_dibujo.set_title(titulo, fontsize=14, color=AZUL_PIZARRA_TEXTO, fontweight="bold", pad=15)
    area_dibujo.set_xlabel(columna_categorias, fontsize=11, color=GRIS_TEXTO_SECUNDARIO, labelpad=10)
    area_dibujo.set_ylabel(columna_valores, fontsize=11, color=GRIS_TEXTO_SECUNDARIO, labelpad=10)
    area_dibujo.grid(axis='y', linestyle=":", alpha=0.6, color="#cbd5e1")

    for spine in ["top", "right", "left"]:
        area_dibujo.spines[spine].set_visible(False)
    area_dibujo.spines["bottom"].set_color("#e2e8f0")

    plt.xticks(rotation=45, color=GRIS_TEXTO_SECUNDARIO)
    plt.yticks(color=GRIS_TEXTO_SECUNDARIO)
    plt.tight_layout()

    ruta_completa = os.path.join(ruta_destino, nombre_archivo)
    figura.savefig(ruta_completa, dpi=150, facecolor=figura.get_facecolor())
    plt.close(figura)
    print(f"Gráfico de barras guardado en: {ruta_completa}")


def graficar_torta(datos_agrupados, columna_etiquetas, columna_valores,
                   titulo="Gráfico de torta", nombre_archivo="torta.png", 
                   ruta_destino=RUTA_ASSETS):
    # Torta (tipo Dona) en Verde (ingreso) vs Rojo (egreso)
    crear_ruta_si_no_existe(ruta_destino)
    figura, area_dibujo = plt.subplots(figsize=(7, 7))

    # Paleta balanceada corporativa
    colores_balance = [VERDE_FINZ_PRINCIPAL if tipo == "ingreso" else ROJO_FINZ_ALERTA for tipo in datos_agrupados[columna_etiquetas]]

    # Formato de Dona Corporativa
    despliegue, textos, porcentajes = area_dibujo.pie(
        datos_agrupados[columna_valores],
        labels=datos_agrupados[columna_etiquetas],
        autopct="%1.1f%%",
        colors=colores_balance,
        startangle=140,
        pctdistance=0.75,
        textprops={'fontsize': 11, 'color': AZUL_PIZARRA_TEXTO, 'weight': 'bold'},
        wedgeprops={"edgecolor": plt.rcParams['figure.facecolor'], "linewidth": 3, "antialiased": True}
    )

    circulo_centro = plt.Circle((0, 0), 0.55, fc=plt.rcParams['figure.facecolor'])
    figura.gca().add_artist(circulo_centro)

    for texto in textos:
        texto.set_color(GRIS_TEXTO_SECUNDARIO)
        texto.set_fontsize(12)

    area_dibujo.set_title(titulo, fontsize=14, color=AZUL_PIZARRA_TEXTO, fontweight="bold", pad=20)
    plt.tight_layout()

    ruta_completa = os.path.join(ruta_destino, nombre_archivo)
    figura.savefig(ruta_completa, dpi=150, facecolor=figura.get_facecolor())
    plt.close(figura)
    print(f"Gráfico de torta guardado en: {ruta_completa}")


def graficar_mapa_calor(datos_agrupados, columna_filas, columna_columnas, columna_valores,
                        titulo="Mapa de calor", paleta_color="Greens", # <--- UNIFICADO A VERDES
                        nombre_archivo="mapa_calor.png", ruta_destino=RUTA_ASSETS):
    # Mapa de calor corporativo en escala secuencial de Verdes Finz+
    crear_ruta_si_no_existe(ruta_destino)
    tabla_pivote = datos_agrupados.pivot_table(
        index=columna_filas, columns=columna_columnas, values=columna_valores, aggfunc="sum", fill_value=0
    )

    figura, area_dibujo = plt.subplots(figsize=(10, 6))

    # Seaborn Heatmap con degradado de Verdes Finz+
    sns.heatmap(
        tabla_pivote,
        annot=True, fmt=".0f",
        cmap="Greens", # <--- ESCALA SECUENCIAL DE VERDES PREMIUM
        ax=area_dibujo,
        linewidths=2,
        linecolor=plt.rcParams['figure.facecolor'],
        cbar_kws={"shrink": 0.75},
        annot_kws={"size": 11, "weight": "bold", "color": AZUL_PIZARRA_TEXTO}
    )

    area_dibujo.set_title(titulo, fontsize=14, color=AZUL_PIZARRA_TEXTO, fontweight="bold", pad=15)
    area_dibujo.set_xlabel(columna_columnas, fontsize=11, color=GRIS_TEXTO_SECUNDARIO, labelpad=10)
    area_dibujo.set_ylabel(columna_filas, fontsize=11, color=GRIS_TEXTO_SECUNDARIO, labelpad=10)

    plt.xticks(rotation=45, color=GRIS_TEXTO_SECUNDARIO)
    plt.yticks(color=GRIS_TEXTO_SECUNDARIO)
    plt.tight_layout()

    ruta_completa = os.path.join(ruta_destino, nombre_archivo)
    figura.savefig(ruta_completa, dpi=150, facecolor=figura.get_facecolor())
    plt.close(figura)
    print(f"Mapa de calor guardado en: {ruta_completa}")


# =====================================================================
# RUTINA PRINCIPAL DE GENERACIÓN (Unificada a Verdes Finz+)
# =====================================================================
def generar_reportes_transacciones(diccionario_transacciones):
    print("\nIniciando generación de gráficos de transacciones para Finz+...")

    # 1. Dona de Balance: Ingreso (Verde) vs Egreso (Rojo)
    df1 = diccionario_transacciones["agrupacion1"]
    if not df1.empty:
        graficar_torta(df1, "tipo", "conteo", 
                       titulo="Distribución de Movimientos Financieros", 
                       nombre_archivo="transacciones_1_proporcion.png")

    # 2. Tendencia: Volumen en Verde Finz+
    df2 = diccionario_transacciones["agrupacion2"]
    if not df2.empty:
        df2 = df2.sort_values("fecha")
        graficar_lineas(df2, "fecha", "conteo", 
                        titulo="Volumen de Transacciones en el Tiempo", 
                        nombre_archivo="transacciones_2_tendencia.png")

    # 3. Egresos por categoría: Barras en Degradado de Verde Sophisticado
    df3 = diccionario_transacciones["agrupacion3"]
    if not df3.empty:
        # Usamos degradado de Verdes Finz+ para diferenciar categorías, pero manteniendo la paleta
        color_finz_sophisticated = [VERDE_FINZ_PRINCIPAL, VERDE_FINZ_OSCURO, "#34d399", "#a7f3d0", VERDE_FINZ_PRINCIPAL]
        graficar_barras(df3, "categoria_id", "conteo", 
                        titulo="Volumen de Egresos por Categoría (Traducidas)", 
                        color_fijo=color_finz_sophisticated[:len(df3)], 
                        nombre_archivo="transacciones_3_egresos_cat.png")

    # 4. Mapa de Calor: Cuentas vs Categorías (Escala de Verdes Premium)
    df4 = diccionario_transacciones["agrupacion4"]
    if not df4.empty:
        # Traducidas también por transformación, unificado a paleta Greens
        graficar_mapa_calor(df4, "cuenta_id", "categoria_id", "conteo", 
                            titulo="Densidad de Egresos: Cuentas vs Categorías (Traducidas)", 
                            paleta_color="Greens", # <--- ESCALA DE VERDES
                            nombre_archivo="transacciones_4_mapa_egresos.png")

    # 5. Atípicas: Barras en Verde Finz+ Principal
    df5 = diccionario_transacciones["agrupacion5"]
    if not df5.empty:
        # Sin morado ni gris, usamos el verde Finz+ directo
        graficar_barras(df5, "descripcion", "conteo", 
                        titulo="Frecuencia de Transacciones de Alto Valor (> $1.5M)", 
                        color_fijo=VERDE_FINZ_PRINCIPAL, # <--- VERDE FINZ+ PRINCIPAL
                        nombre_archivo="transacciones_5_alertas.png")

    print("¡Gráficos corporativos de Finz+ generados con éxito!")