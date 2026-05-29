from notebook.graficacion_transacciones import (
    graficar_lineas, graficar_barras, graficar_mapa_calor, graficar_torta
)

def generar_reporte_grafico_deudas(agrupaciones_deudas):
    """
    Toma las agrupaciones resultantes de la tabla de Deudas
    y genera los archivos visuales en la carpeta de assets.
    """
    print("\n=== GENERANDO GRÁFICOS DE DEUDAS ===")

    # 1. Gráfico de Líneas: Vencimiento de deudas activas en el tiempo
    df1 = agrupaciones_deudas["agrupacion1"]
    if not df1.empty:
        graficar_lineas(
            datos_agrupados=df1,
            columna_eje_x="fecha_vencimiento",
            columna_eje_y="conteo",
            titulo="Tendencia de Vencimiento de Deudas Activas",
            nombre_archivo="deudas_vencimiento_lineas.png"
        )

    # 2. Gráfico de Barras: Deudas de alto valor por tipo
    df2 = agrupaciones_deudas["agrupacion2"]
    if not df2.empty:
        graficar_barras(
            datos_agrupados=df2,
            columna_categorias="tipo",
            columna_valores="conteo",
            titulo="Cantidad de Deudas de Alto Valor (>= 1M) por Tipo",
            color_fijo="#FB8C00",
            nombre_archivo="deudas_alto_valor_barras.png"
        )

    # 3. Mapa de Calor: Relación Tipo vs Entidad en deudas sin abonar
    df3 = agrupaciones_deudas["agrupacion3"]
    if not df3.empty:
        graficar_mapa_calor(
            datos_agrupados=df3,
            columna_filas="tipo",
            columna_columnas="persona_entidad",
            columna_valores="conteo",
            titulo="Concentración de Deudas Intactas (Sin Abonos)",
            paleta_color="Reds",
            nombre_archivo="deudas_intactas_heatmap.png"
        )

    # 4. Gráfico de Torta: Distribución de deudas bancarias
    df4 = agrupaciones_deudas["agrupacion4"]
    if not df4.empty:
        graficar_torta(
            datos_agrupados=df4,
            columna_etiquetas="persona_entidad",
            columna_valores="conteo",
            titulo="Distribución de Acreedores en Deudas Bancarias",
            nombre_archivo="deudas_bancarias_torta.png"
        )
