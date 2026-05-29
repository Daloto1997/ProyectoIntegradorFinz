from notebook.graficacion_transacciones import (
    graficar_lineas, graficar_barras, graficar_mapa_calor, graficar_torta
)

def generar_reporte_grafico_metas(agrupaciones_metas):
    """
    Toma las agrupaciones resultantes de la tabla de Metas
    y genera los archivos visuales en la carpeta de assets.
    """
    print("\n=== GENERANDO GRÁFICOS DE METAS ===")

    # 1. Gráfico de Líneas: Fechas límite de las metas
    df1 = agrupaciones_metas["agrupacion1"]
    if not df1.empty:
        graficar_lineas(
            datos_agrupados=df1,
            columna_eje_x="fecha_limite",
            columna_eje_y="conteo",
            titulo="Cronograma de Cumplimiento de Metas",
            nombre_archivo="metas_cronograma_lineas.png"
        )

    # 2. Gráfico de Barras: Metas más ambiciosas por categoría
    df2 = agrupaciones_metas["agrupacion2"]
    if not df2.empty:
        graficar_barras(
            datos_agrupados=df2,
            columna_categorias="nombre",
            columna_valores="conteo",
            titulo="Metas de Gran Volumen (>= 5M) por Categoría",
            color_fijo="#00ACC1",
            nombre_archivo="metas_ambiciosas_barras.png"
        )

    # 3. Mapa de Calor: Usuarios vs Categorías con ahorros activos
    df3 = agrupaciones_metas["agrupacion3"]
    if not df3.empty:
        graficar_mapa_calor(
            datos_agrupados=df3,
            columna_filas="usuario_id",
            columna_columnas="nombre",
            columna_valores="conteo",
            titulo="Mapa de Actividad de Ahorro por Usuario",
            paleta_color="YlGn",
            nombre_archivo="metas_usuarios_heatmap.png"
        )

    # 4. Gráfico de Torta: Metas en ceros (Procrastinadas)
    df4 = agrupaciones_metas["agrupacion4"]
    if not df4.empty:
        graficar_torta(
            datos_agrupados=df4,
            columna_etiquetas="nombre",
            columna_valores="conteo",
            titulo="Distribución de Metas Sin Iniciar (Monto Actual = 0)",
            nombre_archivo="metas_sin_iniciar_torta.png"
        )
