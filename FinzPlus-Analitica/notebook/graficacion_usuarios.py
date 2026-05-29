import matplotlib.pyplot as plt
import seaborn as sns
import os

# =====================================================================
# IDENTIDAD VISUAL CORPORATIVA FINZ+
# =====================================================================
VERDE_FINZ_PRINCIPAL = "#25c974"
VERDE_FINZ_OSCURO = "#065f46"
GRIS_TEXTO = "#1e293b"
GRIS_TEXTO_SECUNDARIO = "#64748b"
ROJO_ALERTA = "#ef4444"

# Configuracion de estilo global (igual que en graficacion_transacciones)
plt.rcParams['figure.facecolor'] = '#f8fafc'
plt.rcParams['axes.facecolor'] = '#ffffff'
plt.rcParams['font.family'] = 'sans-serif'

# Ruta para la carpeta local de gráficos
RUTA_ASSETS = os.path.join(os.path.dirname(__file__), "graficos")

def crear_ruta_si_no_existe(ruta_destino):
    os.makedirs(ruta_destino, exist_ok=True)

def graficar_crecimiento(datos_agrupados, columna_eje_x, columna_eje_y,
                         titulo="Crecimiento de Usuarios", color_barras=VERDE_FINZ_PRINCIPAL,
                         nombre_archivo="usuarios_2_crecimiento.png", ruta_destino=RUTA_ASSETS):
    crear_ruta_si_no_existe(ruta_destino)
    figura, area_dibujo = plt.subplots(figsize=(12, 6))

    area_dibujo.bar(
        datos_agrupados[columna_eje_x].astype(str),
        datos_agrupados[columna_eje_y],
        color=color_barras,
        edgecolor="none",
        alpha=0.9,
        width=0.6
    )

    # Etiquetas encima de cada barra
    area_dibujo.bar_label(area_dibujo.containers[0], fontsize=9, color=GRIS_TEXTO, padding=4)

    area_dibujo.set_title(titulo, fontsize=14, color=GRIS_TEXTO, fontweight="bold", pad=15)
    area_dibujo.set_xlabel("Mes", fontsize=11, color=GRIS_TEXTO_SECUNDARIO, labelpad=10)
    area_dibujo.set_ylabel("Cantidad de Usuarios", fontsize=11, color=GRIS_TEXTO_SECUNDARIO, labelpad=10)
    area_dibujo.grid(axis='y', linestyle=":", alpha=0.6, color="#cbd5e1")

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
    print(f"Gráfico de crecimiento guardado en: {ruta_completa}")

def graficar_barras(datos_agrupados, columna_categorias, columna_valores,
                    titulo="Gráfico de barras", color_barras=VERDE_FINZ_PRINCIPAL,
                    nombre_archivo="barras.png", ruta_destino=RUTA_ASSETS):
    crear_ruta_si_no_existe(ruta_destino)
    figura, area_dibujo = plt.subplots(figsize=(10, 5))

    area_dibujo.bar(datos_agrupados[columna_categorias], datos_agrupados[columna_valores],
                    color=color_barras, edgecolor="none", alpha=0.9, width=0.6)

    # Etiquetas encima de cada barra
    area_dibujo.bar_label(area_dibujo.containers[0], fontsize=9, color=GRIS_TEXTO, padding=4)

    area_dibujo.set_title(titulo, fontsize=14, color=GRIS_TEXTO, fontweight="bold", pad=15)
    area_dibujo.set_xlabel(columna_categorias, fontsize=11, color=GRIS_TEXTO_SECUNDARIO, labelpad=10)
    area_dibujo.set_ylabel(columna_valores, fontsize=11, color=GRIS_TEXTO_SECUNDARIO, labelpad=10)
    area_dibujo.grid(axis='y', linestyle=":", alpha=0.6, color="#cbd5e1")

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
    print(f"Gráfico de barras guardado en: {ruta_completa}")

def graficar_barras_agrupadas(datos_agrupados, columna_x, columna_y, columna_grupo,
                               titulo="Gráfico de barras agrupadas",
                               nombre_archivo="barras_agrupadas.png",
                               ruta_destino=RUTA_ASSETS):
    crear_ruta_si_no_existe(ruta_destino)
    figura, area_dibujo = plt.subplots(figsize=(10, 5))

    # seaborn agrupa automaticamente las barras usando el parametro hue
    sns.barplot(
        data=datos_agrupados,
        x=columna_x,
        y=columna_y,
        hue=columna_grupo,
        palette=[VERDE_FINZ_PRINCIPAL, VERDE_FINZ_OSCURO],
        ax=area_dibujo,
        errorbar=None  # quitamos las barras de error, no las necesitamos
    )

    # Etiquetas encima de cada barra agrupada
    for container in area_dibujo.containers:
        area_dibujo.bar_label(container, fontsize=9, color=GRIS_TEXTO, padding=4)

    area_dibujo.set_title(titulo, fontsize=14, color=GRIS_TEXTO, fontweight="bold", pad=15)
    area_dibujo.set_xlabel(columna_x, fontsize=11, color=GRIS_TEXTO_SECUNDARIO, labelpad=10)
    area_dibujo.set_ylabel(columna_y, fontsize=11, color=GRIS_TEXTO_SECUNDARIO, labelpad=10)
    area_dibujo.grid(axis="y", linestyle=":", alpha=0.6, color="#cbd5e1")

    for spine in ["top", "right"]:
        area_dibujo.spines[spine].set_visible(False)
    area_dibujo.spines["left"].set_color("#e2e8f0")
    area_dibujo.spines["bottom"].set_color("#e2e8f0")

    area_dibujo.legend(title=columna_grupo.capitalize())
    plt.xticks(color=GRIS_TEXTO_SECUNDARIO)
    plt.yticks(color=GRIS_TEXTO_SECUNDARIO)
    plt.tight_layout()

    ruta_completa = os.path.join(ruta_destino, nombre_archivo)
    figura.savefig(ruta_completa, dpi=150, facecolor=figura.get_facecolor())
    plt.close(figura)
    print(f"Gráfico de barras agrupadas guardado en: {ruta_completa}")

def graficar_torta(datos_agrupados, columna_etiquetas, columna_valores,
                   titulo="Gráfico de torta", lista_colores=None,
                   nombre_archivo="torta.png", ruta_destino=RUTA_ASSETS):
    crear_ruta_si_no_existe(ruta_destino)
    if lista_colores is None:
        lista_colores = [VERDE_FINZ_PRINCIPAL, VERDE_FINZ_OSCURO, "#cbd5e1"]

    figura, area_dibujo = plt.subplots(figsize=(8, 8))
    area_dibujo.pie(
        datos_agrupados[columna_valores],
        labels=datos_agrupados[columna_etiquetas],
        autopct="%1.1f%%",
        colors=lista_colores[:len(datos_agrupados)],
        wedgeprops={"edgecolor": "white", "linewidth": 2},
        textprops={"fontsize": 11, "color": GRIS_TEXTO}
    )

    area_dibujo.set_title(titulo, fontsize=14, color=GRIS_TEXTO, fontweight="bold", pad=20)
    plt.tight_layout()

    ruta_completa = os.path.join(ruta_destino, nombre_archivo)
    figura.savefig(ruta_completa, dpi=150, facecolor=figura.get_facecolor())
    plt.close(figura)
    print(f"Gráfico de torta guardado en: {ruta_completa}")

def graficar_barras_apiladas(datos_agrupados, columna_x, columna_y, columna_color,
                             titulo="Gráfico apilado", nombre_archivo="apilado.png",
                             ruta_destino=RUTA_ASSETS):
    crear_ruta_si_no_existe(ruta_destino)

    df_pivot = datos_agrupados.pivot(index=columna_x, columns=columna_color, values=columna_y).fillna(0)

    ax = df_pivot.plot(kind='bar', stacked=True, figsize=(10, 6),
                       color=[VERDE_FINZ_PRINCIPAL, VERDE_FINZ_OSCURO, "#cbd5e1"])

    # Etiquetas dentro de cada segmento apilado
    for container in ax.containers:
        ax.bar_label(container, label_type='center', fontsize=9, color='white', fontweight='bold', fmt='%.0f')

    plt.title(titulo, fontsize=14, color=GRIS_TEXTO, fontweight="bold", pad=15)
    plt.xticks(rotation=45, color=GRIS_TEXTO_SECUNDARIO)
    plt.yticks(color=GRIS_TEXTO_SECUNDARIO)
    plt.legend(title=columna_color.capitalize())
    plt.tight_layout()

    figura = plt.gcf()
    ruta_completa = os.path.join(ruta_destino, nombre_archivo)
    figura.savefig(ruta_completa, dpi=150, facecolor=figura.get_facecolor())
    plt.close()
    print(f"Gráfico de barras apiladas guardado en: {ruta_completa}")

# =====================================================================
# ORQUESTADOR DE REPORTES DE USUARIOS
# =====================================================================
def generar_reportes_usuarios(diccionario_usuarios):
    print("\n--- INICIANDO GENERACIÓN DE GRÁFICOS DE USUARIOS (FINZ+) ---")

    # 1. Distribución de Roles (Torta)
    if "agrupacion1" in diccionario_usuarios and not diccionario_usuarios["agrupacion1"].empty:
        graficar_torta(diccionario_usuarios["agrupacion1"], "rol", "conteo",
                       titulo="Distribución de Roles", nombre_archivo="usuarios_1_roles.png")

    # 2. Crecimiento Mensual (Barras)
    if "agrupacion2" in diccionario_usuarios and not diccionario_usuarios["agrupacion2"].empty:
        df2 = diccionario_usuarios["agrupacion2"].sort_values("fecha_creacion")
        graficar_crecimiento(df2, "fecha_creacion", "conteo",
                             titulo="Crecimiento de Usuarios por Mes",
                             nombre_archivo="usuarios_2_crecimiento.png")

    # 3. Género por Rol (Barras Apiladas)
    if "agrupacion3" in diccionario_usuarios and not diccionario_usuarios["agrupacion3"].empty:
        graficar_barras_apiladas(diccionario_usuarios["agrupacion3"],
                                 columna_x="rol", columna_y="conteo", columna_color="genero",
                                 titulo="Composición de Género por Rol",
                                 nombre_archivo="usuarios_3_genero_rol.png")

    # 4. Género por Tipo de Cuenta (Barras Agrupadas)
    if "agrupacion4" in diccionario_usuarios and not diccionario_usuarios["agrupacion4"].empty:
        graficar_barras_agrupadas(diccionario_usuarios["agrupacion4"],
                                  columna_x="genero", columna_y="conteo", columna_grupo="rol",
                                  titulo="Distribución de Género por Tipo de Cuenta",
                                  nombre_archivo="usuarios_4_densidad.png")

    # 5. Roles Anómalos (Alerta) - solo aparece si la simulacion genero roles invalidos
    if "agrupacion5" in diccionario_usuarios and not diccionario_usuarios["agrupacion5"].empty:
        graficar_barras(diccionario_usuarios["agrupacion5"], "rol", "conteo",
                        titulo="ALERTA: Roles Anómalos Detectados",
                        color_barras=ROJO_ALERTA,
                        nombre_archivo="usuarios_5_anomalias.png")

    print("--- PROCESO DE USUARIOS FINALIZADO ---\n")
